==========================
API de Documents
==========================

Visión General
==============

La API de Documents es una Admin API de |Fess| para registrar documentos de forma masiva en el índice.
Permite a sistemas externos agregar documentos generados directamente al índice sin necesidad de un rastreador.
Se pueden registrar varios documentos en una sola solicitud.

URL Base
========

::

    /api/admin/documents

Autenticación
=============

Para llamar a esta API se requiere autenticación mediante token de acceso, tal como se describe en :doc:`api-admin-overview`.
El token debe tener el permiso de acceso a Admin API (por defecto ``Radmin-api``).
Este permiso se puede cambiar mediante la clave de configuración ``api.admin.access.permissions``.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - PUT
     - /bulk
     - Registro masivo de documentos

.. note::

   Este endpoint acepta únicamente el método ``PUT``.

Registro Masivo de Documentos
==============================

Registra varios documentos en el índice de forma masiva.

Solicitud
---------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "Pagina de ejemplo 1",
          "content": "Este es el texto del cuerpo de la pagina 1."
        },
        {
          "url": "https://example.com/page2",
          "title": "Pagina de ejemplo 2",
          "content": "Este es el texto del cuerpo de la pagina 2."
        }
      ]
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``documents``
     - Sí
     - Arreglo de documentos a registrar. Cada documento se especifica como un mapa de nombres de campo y valores. Si es ``null`` o un arreglo vacío, se devuelve un error (``status`` = ``1``).

Campos del Documento
~~~~~~~~~~~~~~~~~~~~

En cada documento se pueden especificar libremente los campos del índice como un mapa de nombres y valores.
Como mínimo, se deben especificar ``url`` y ``title`` (según la configuración de campos requeridos
``index.admin.required.fields``; el valor predeterminado es ``url,title,role,boost``, y dado que
``role`` y ``boost`` se autocompletan como se describe más adelante, en la práctica ``url`` y ``title`` son obligatorios).

Los siguientes campos se completan automáticamente si se omiten:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Valor predeterminado al omitir
   * - ``content_length``
     - Suma del número de caracteres de ``title`` y ``content``
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - Rol de búsqueda para invitados (rol de búsqueda configurado para usuarios invitados)
   * - ``last_modified``
     - Hora actual
   * - ``timestamp``
     - Hora actual

Además, los siguientes campos se generan automáticamente al registrar:

- ``id`` - Se genera de forma determinista a partir de la ``url`` del documento (y de ``role`` y ``virtual_host``),
  y se utiliza como ID de documento en OpenSearch (``_id``). Este valor se devuelve en ``items[].id``
  de la respuesta.
- ``doc_id`` - Se genera un UUID aleatorio en cada registro y se almacena como campo del documento.

.. note::

   Dado que ``id`` se genera de forma determinista a partir de ``url``, si se registra de nuevo
   un documento con la misma ``url``, el documento existente será actualizado
   (``items[].result`` será ``OK``).

Notas Adicionales
~~~~~~~~~~~~~~~~~

- Si se incluye ``"auto"`` en el campo ``lang``, el idioma se detecta automáticamente a partir del cuerpo del documento.
- Si se especifica ``config_id``, se aplica el pipeline de ingesta (ingest pipeline) de la configuración de rastreo correspondiente.
- Si la generación de miniaturas está habilitada (``thumbnail.crawler.enabled``), se intentará generar una miniatura al registrar.
- Los valores de cada campo se validan según la configuración de tipo del campo (``index.admin.array.fields``,
  ``index.admin.date.fields``, ``index.admin.long.fields``, etc.).
  Si el tipo no coincide, se devuelve un error (``status`` = ``1``).

Respuesta
---------

La respuesta devuelve el resultado de procesamiento de cada documento registrado en el arreglo ``items``.
Los elementos exitosos incluyen ``result`` e ``id``, y los elementos fallidos incluyen ``result`` y ``message``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

Cuando ``status`` es ``0``, indica que todos los documentos se registraron correctamente.
En ``items[].result`` se establece ``CREATED`` para nuevos documentos y ``OK`` para documentos existentes actualizados.

Si el registro falla en alguno de los elementos, ``status`` será ``9`` (FAILED) y
el elemento correspondiente incluirá el campo ``message`` (en ``result`` se establecerá
el nombre del estado de error, como ``CONFLICT`` o ``BAD_REQUEST``). Los elementos exitosos devuelven su ``id`` normalmente.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

.. note::

   Si la solicitud en sí es inválida (``documents`` no especificado o vacío, campos requeridos ausentes,
   tipo de campo incorrecto, etc.), el proceso de registro de documentos no se ejecuta y
   se devuelve una respuesta de error con ``status`` = ``1`` (BAD_REQUEST) y ``message``.
   En este caso, no se devuelve el arreglo ``items``.

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``items``
     - Arreglo de resultados de procesamiento de cada documento
   * - ``items[].result``
     - Nombre del estado del resultado de procesamiento. ``CREATED`` para nuevos documentos, ``OK`` para actualizaciones, o nombre del estado de error como ``BAD_REQUEST`` en caso de fallo
   * - ``items[].id``
     - ID del documento registrado (solo en caso de éxito)
   * - ``items[].message``
     - Mensaje con el motivo del fallo (solo en caso de fallo)

Ejemplos de Uso
===============

Registro Masivo de Documentos
------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "Pagina de ejemplo 1",
               "content": "Este es el texto del cuerpo de la pagina 1."
             }
           ]
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-searchlist` - API de búsqueda y gestión de documentos
- :doc:`api-admin-crawlinginfo` - API de información de rastreo
- :doc:`../../admin/searchlist-guide` - Guía de gestión de lista de búsqueda
