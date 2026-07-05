==========================
SearchList API
==========================

Descripción General
===================

La SearchList API es una Admin API de |Fess| para buscar y gestionar documentos en el índice.
Permite buscar, obtener, crear, actualizar y eliminar documentos.

Todos los nombres de campo en la respuesta usan ``snake_case``. Los campos cuyo valor es ``null`` se omiten de la respuesta.

URL Base
========

::

    /api/admin/searchlist

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
   * - GET / PUT
     - /docs
     - Buscar documentos
   * - GET
     - /doc/{id}
     - Obtener documento
   * - POST
     - /doc
     - Crear documento
   * - PUT
     - /doc
     - Actualizar documento
   * - DELETE
     - /doc/{id}
     - Eliminar documento (por ID)
   * - DELETE
     - /query
     - Eliminar documentos (por consulta)

Buscar Documentos
=================

Busca documentos que coincidan con las condiciones de búsqueda.

Solicitud
---------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``q``
     - String
     - No
     - Consulta de búsqueda (máximo 1000 caracteres). Si no se especifica, se apunta a todos los documentos.
   * - ``sort``
     - String
     - No
     - Campo y dirección de ordenación (ej. ``last_modified.desc``).
   * - ``start``
     - Integer
     - No
     - Posición de inicio desde 0 (valor predeterminado ``0``).
   * - ``offset``
     - Integer
     - No
     - Desplazamiento desde ``start`` (valor predeterminado ``0``).
   * - ``pn``
     - Integer
     - No
     - Número de página.
   * - ``num``
     - Integer
     - No
     - Número de elementos a obtener (valor predeterminado ``10``). Los valores que superen el máximo configurado (por defecto ``100``) o los valores de ``0`` o menos se ajustan al máximo.
   * - ``size``
     - Integer
     - No
     - Número de elementos a obtener (alias de ``num``, proporcionado por compatibilidad con otras Admin APIs).
   * - ``lang``
     - String[]
     - No
     - Idioma de búsqueda. Se puede especificar repetidamente (array). Ej. ``en``.
   * - ``ex_q``
     - String[]
     - No
     - Expresiones de consulta adicionales. Se pueden especificar repetidamente (array).
   * - ``fields.<name>``
     - String[]
     - No
     - Filtra por valor de campo. El caso más común es ``fields.label`` (filtrar por nombre de etiqueta); cualquier ``fields.<name>`` restringe los resultados a aquellos cuyo campo de documento ``<name>`` coincida con el valor dado. Se puede especificar repetidamente.
   * - ``as.<name>``
     - String[]
     - No
     - Condiciones de búsqueda avanzada. Cualquier ``as.<name>`` (ej. ``as.q``) se pasa al constructor de condiciones de búsqueda avanzada. Se puede especificar repetidamente por nombre.
   * - ``sdh``
     - String
     - No
     - Hash de documentos similares (similar-document hash).

.. note::

   Este endpoint no admite facetado, resaltado ni búsqueda geográfica. Dichos parámetros se ignoran si se especifican.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
            "content_description": "..."
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
     - Descripción
   * - ``version``
     - La versión de |Fess| en ejecución (el valor del ejemplo es ilustrativo).
   * - ``status``
     - Código de estado (``0`` para éxito; véase "Códigos de Estado").
   * - ``query_id``
     - ID de la consulta de búsqueda.
   * - ``docs``
     - Array de documentos resultantes de la búsqueda. Cada documento es un mapa de nombres de campo y valores, usando los nombres de campo del índice tal como son (``doc_id``, ``url``, ``title``, ``content_description``, etc.).
   * - ``exec_time``
     - Tiempo de ejecución de la búsqueda (segundos, cadena de texto).
   * - ``query_time``
     - Tiempo de consulta del motor de búsqueda (milisegundos).
   * - ``page_size``
     - Número de elementos por página.
   * - ``page_number``
     - Número de página actual.
   * - ``record_count``
     - Número de elementos coincidentes.
   * - ``record_count_relation``
     - Relación del recuento de coincidencias. ``eq`` indica un recuento exacto; ``gte`` indica que solo se conoce el límite inferior.
   * - ``page_count``
     - Número total de páginas.
   * - ``next_page``
     - Si existe una página siguiente (bool).
   * - ``prev_page``
     - Si existe una página anterior (bool).
   * - ``start_record_number``
     - Número de registro de inicio de esta página.
   * - ``end_record_number``
     - Número de registro de fin de esta página.
   * - ``page_numbers``
     - Array de números de página para mostrar en el paginador (cadenas de texto).
   * - ``partial``
     - Si los resultados son parciales (bool).
   * - ``search_query``
     - La consulta de búsqueda que se ejecutó realmente.
   * - ``requested_time``
     - Hora de la solicitud (epoch en milisegundos).
   * - ``highlight_params``
     - Cadena de parámetros de consulta para resaltado (normalmente vacía para esta Admin API).

Obtener Documento
=================

Recupera un único documento especificando el ID del documento.

Solicitud
---------

::

    GET /api/admin/searchlist/doc/{id}

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``id``
     - String
     - Sí
     - ID del documento (el valor de ``doc_id``, parámetro de ruta).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

Si no existe ningún documento para el ID especificado, se devuelve una respuesta de error (``status`` = ``1``).

Crear Documento
===============

Crea un nuevo documento en el índice.

Solicitud
---------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "Sample Page 1",
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``doc``
     - Sí
     - El documento a registrar. Se especifica como un mapa de nombres de campo del índice y valores.

Entre los campos especificados en ``doc``, se deben proporcionar todos los campos obligatorios configurados en ``index.admin.required.fields`` (valor predeterminado ``url,title,role,boost``).
A diferencia de la :doc:`Documents API <api-admin-documents>` de registro masivo, este endpoint no completa automáticamente valores predeterminados como ``role`` o ``boost``, por lo que los campos obligatorios deben especificarse explícitamente en la solicitud.
``doc_id`` se genera automáticamente en el servidor y no se especifica al crear.

El valor de cada campo se valida según la configuración del tipo de campo. Si el tipo no coincide, se devuelve un error (``status`` = ``1``).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Clave de Configuración
     - Valor Predeterminado
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - (vacío)
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - (vacío)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``id``
     - El ``doc_id`` del documento registrado.
   * - ``created``
     - ``true`` al crear.

Actualizar Documento
====================

Actualiza un documento existente.

Solicitud
---------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "Updated Title",
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``doc``
     - Sí
     - El documento a actualizar. Se especifica como un mapa de nombres de campo del índice y valores.

El documento a actualizar se identifica mediante ``doc_id`` dentro de ``doc``. Si ``doc_id`` no está especificado, o no existe ningún documento coincidente, se devuelve un error (``status`` = ``1``).
Al igual que en la creación, se deben proporcionar todos los campos obligatorios configurados en ``index.admin.required.fields`` (valor predeterminado ``url,title,role,boost``), y el valor de cada campo se valida según la configuración de tipo.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``id``
     - El ``doc_id`` del documento actualizado.
   * - ``created``
     - ``false`` al actualizar.

Eliminar Documento (por ID)
===========================

Elimina un documento especificando el ID del documento.

Solicitud
---------

::

    DELETE /api/admin/searchlist/doc/{id}

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``id``
     - String
     - Sí
     - ID del documento (el valor de ``doc_id``, parámetro de ruta).

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Eliminar Documentos (por consulta)
===================================

Elimina de forma masiva los documentos que coincidan con una consulta de búsqueda.

Solicitud
---------

::

    DELETE /api/admin/searchlist/query

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``q``
     - String
     - Sí
     - Consulta de búsqueda de los documentos a eliminar.

El objetivo de eliminación se construye con la misma consulta que "Buscar Documentos", por lo que se pueden usar conjuntamente parámetros de filtrado como ``fields.<name>`` y ``ex_q``. Si ``q`` no está especificado, se devuelve un error (``status`` = ``1``).

Respuesta
---------

Devuelve el número de documentos eliminados en ``count``.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "count": 150
      }
    }

Códigos de Estado
=================

El campo ``status`` en la respuesta se establece con uno de los siguientes valores.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Valor
     - Nombre
     - Descripción
   * - ``0``
     - OK
     - Éxito.
   * - ``1``
     - BAD_REQUEST
     - La solicitud no es válida (campo obligatorio ausente, tipo incompatible, documento destino no encontrado, consulta inválida, etc.).
   * - ``2``
     - SYSTEM_ERROR
     - Error de sistema.
   * - ``3``
     - UNAUTHORIZED
     - Error de autenticación.
   * - ``9``
     - FAILED
     - El procesamiento falló.

Ejemplos de Uso
===============

Buscar Documentos
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Documento
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

Crear Documento
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

Eliminar Documentos por Consulta
---------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

Información de Referencia
=========================

- :doc:`api-admin-overview` - Descripción general de Admin API
- :doc:`api-admin-documents` - API de registro masivo de documentos
- :doc:`api-admin-crawlinginfo` - API de información de rastreo
- :doc:`../../admin/searchlist-guide` - Guía de gestión de lista de búsqueda
