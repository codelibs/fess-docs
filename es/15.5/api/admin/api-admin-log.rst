==========================
API de Log
==========================

Vision General
==============

La API de Log es para obtener informacion de registros de |Fess|.
Puede consultar registros de busqueda, registros de clics, registros del sistema, etc.

URL Base
========

::

    /api/admin/log

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /search
     - Obtener registros de busqueda
   * - GET
     - /click
     - Obtener registros de clics
   * - GET
     - /favorite
     - Obtener registros de favoritos
   * - DELETE
     - /search/delete
     - Eliminar registros de busqueda

Obtener Registros de Busqueda
=============================

Solicitud
---------

::

    GET /api/admin/log/search

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``size``
     - Integer
     - No
     - Numero de elementos por pagina (predeterminado: 20)
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 0)
   * - ``from``
     - String
     - No
     - Fecha/hora de inicio (formato ISO 8601)
   * - ``to``
     - String
     - No
     - Fecha/hora de fin (formato ISO 8601)
   * - ``query``
     - String
     - No
     - Filtro de consulta de busqueda

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "log_id_1",
            "queryId": "query_id_1",
            "query": "fess search",
            "requestedAt": "2025-01-29T10:30:00Z",
            "responseTime": 123,
            "hitCount": 567,
            "user": "guest",
            "roles": ["guest"],
            "languages": ["ja"],
            "clientIp": "192.168.1.100",
            "userAgent": "Mozilla/5.0..."
          }
        ],
        "total": 1234
      }
    }

Obtener Registros de Clics
==========================

Solicitud
---------

::

    GET /api/admin/log/click

Parametros
~~~~~~~~~~

Ademas de los mismos parametros que los registros de busqueda, se pueden especificar los siguientes:

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``url``
     - String
     - No
     - Filtro de URL clicada
   * - ``queryId``
     - String
     - No
     - Filtro de ID de consulta de busqueda

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "click_log_id_1",
            "queryId": "query_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "order": 1,
            "clickedAt": "2025-01-29T10:31:00Z",
            "user": "guest",
            "clientIp": "192.168.1.100"
          }
        ],
        "total": 567
      }
    }

Obtener Registros de Favoritos
==============================

Solicitud
---------

::

    GET /api/admin/log/favorite

Parametros
~~~~~~~~~~

Los mismos parametros que los registros de clics.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "favorite_log_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "createdAt": "2025-01-29T10:32:00Z",
            "user": "user123"
          }
        ],
        "total": 123
      }
    }

Eliminar Registros de Busqueda
==============================

Solicitud
---------

::

    DELETE /api/admin/log/search/delete

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``before``
     - String
     - Si
     - Eliminar registros anteriores a esta fecha/hora (formato ISO 8601)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deletedCount": 5678
      }
    }

Ejemplos de Uso
===============

Obtener Registros de Busqueda Recientes
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Registros de Busqueda de un Periodo Especifico
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Registros de Busqueda de una Consulta Especifica
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?query=fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Registros de Clics
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/click?size=100" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Registros de Busqueda Antiguos
---------------------------------------

.. code-block:: bash

    # Eliminar registros anteriores a 30 dias
    curl -X DELETE "http://localhost:8080/api/admin/log/search/delete?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-stats` - API de estadisticas
- :doc:`../../admin/log-guide` - Guia de gestion de registros
