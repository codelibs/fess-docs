==========================
API de Documents
==========================

Vision General
==============

La API de Documents es una API para registrar documentos de forma masiva en el indice de |Fess|.
Permite agregar varios documentos al indice de una sola vez.

URL Base
========

::

    /api/admin/documents

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - PUT
     - /bulk
     - Registro masivo de documentos

Registro Masivo de Documentos
=============================

Registra varios documentos en el indice de forma masiva.

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
          "title": "Pagina de Ejemplo 1",
          "content": "Este es el texto del cuerpo de la pagina 1."
        },
        {
          "url": "https://example.com/page2",
          "title": "Pagina de Ejemplo 2",
          "content": "Este es el texto del cuerpo de la pagina 2."
        }
      ]
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``documents``
     - Si
     - Arreglo de documentos a registrar. Cada documento se especifica como un mapa de nombres de campo y valores. No se puede especificar un arreglo vacio.

En cada documento se pueden especificar libremente campos de indice como ``url``, ``title``, ``content``, etc.
Si se omiten ``content_length``, ``favorite_count``, ``click_count``, ``boost``, ``role``, ``last_modified``, ``timestamp``, etc., se completan automaticamente con valores predeterminados.
Ademas, ``doc_id`` y el ID se generan automaticamente al registrar.

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

Si el registro falla en alguno de los elementos, ``status`` sera ``9`` (FAILED) y el elemento correspondiente incluira el campo ``message``.

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

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``items``
     - Arreglo de resultados de procesamiento de cada documento
   * - ``items[].result``
     - Estado del resultado de procesamiento (ej: ``CREATED``)
   * - ``items[].id``
     - ID del documento registrado (en caso de exito)
   * - ``items[].message``
     - Mensaje del motivo del fallo (en caso de fallo)

Ejemplos de Uso
===============

Registro Masivo de Documentos
-----------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "Pagina de Ejemplo 1",
               "content": "Este es el texto del cuerpo de la pagina 1."
             }
           ]
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-searchlist` - API de busqueda y gestion de documentos
- :doc:`api-admin-crawlinginfo` - API de informacion de rastreo
- :doc:`../../admin/searchlist-guide` - Guia de gestion de lista de busqueda
