==========================
API de SearchLog
==========================

Vision General
==============

La API de SearchLog es para obtener y gestionar registros de busqueda de |Fess|.
Se puede utilizar para analizar el comportamiento de busqueda del usuario y mejorar la calidad de busqueda.

URL Base
========

::

    /api/admin/searchlog

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /
     - Obtener lista de registros de busqueda
   * - GET
     - /{id}
     - Obtener detalle del registro de busqueda
   * - DELETE
     - /{id}
     - Eliminar registro de busqueda
   * - DELETE
     - /delete-all
     - Eliminar registros de busqueda en masa
   * - GET
     - /stats
     - Obtener estadisticas de busqueda

Obtener Lista de Registros de Busqueda
======================================

Solicitud
---------

::

    GET /api/admin/searchlog

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
     - Filtrar por consulta de busqueda
   * - ``user``
     - String
     - No
     - Filtrar por ID de usuario

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "searchlog_id_1",
            "searchWord": "Fess instalacion",
            "requestedAt": "2025-01-29T10:00:00Z",
            "responseTime": 125,
            "hitCount": 234,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user001",
            "userSessionId": "session_abc123",
            "clientIp": "192.168.1.100",
            "referer": "https://example.com/",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user", "admin"],
            "languages": ["ja"]
          },
          {
            "id": "searchlog_id_2",
            "searchWord": "configuracion busqueda",
            "requestedAt": "2025-01-29T09:55:00Z",
            "responseTime": 98,
            "hitCount": 567,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user002",
            "userSessionId": "session_def456",
            "clientIp": "192.168.1.101",
            "referer": "",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user"],
            "languages": ["ja", "en"]
          }
        ],
        "total": 10000
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``id``
     - ID del registro de busqueda
   * - ``searchWord``
     - Palabra clave de busqueda
   * - ``requestedAt``
     - Fecha/hora de busqueda
   * - ``responseTime``
     - Tiempo de respuesta (milisegundos)
   * - ``hitCount``
     - Numero de resultados
   * - ``queryOffset``
     - Desplazamiento de resultados
   * - ``queryPageSize``
     - Tamano de pagina
   * - ``user``
     - ID de usuario
   * - ``userSessionId``
     - ID de sesion
   * - ``clientIp``
     - Direccion IP del cliente
   * - ``referer``
     - Referencia
   * - ``userAgent``
     - Agente de usuario
   * - ``roles``
     - Roles de usuario
   * - ``languages``
     - Idiomas de busqueda

Obtener Detalle del Registro de Busqueda
========================================

Solicitud
---------

::

    GET /api/admin/searchlog/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "searchlog_id_1",
          "searchWord": "Fess instalacion",
          "requestedAt": "2025-01-29T10:00:00Z",
          "responseTime": 125,
          "hitCount": 234,
          "queryOffset": 0,
          "queryPageSize": 10,
          "user": "user001",
          "userSessionId": "session_abc123",
          "clientIp": "192.168.1.100",
          "referer": "https://example.com/",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "roles": ["user", "admin"],
          "languages": ["ja"],
          "clickLogs": [
            {
              "url": "https://fess.codelibs.org/install.html",
              "docId": "doc_123",
              "order": 1,
              "clickedAt": "2025-01-29T10:00:15Z"
            }
          ]
        }
      }
    }

Eliminar Registro de Busqueda
=============================

Solicitud
---------

::

    DELETE /api/admin/searchlog/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search log deleted successfully"
      }
    }

Eliminar Registros de Busqueda en Masa
======================================

Solicitud
---------

::

    DELETE /api/admin/searchlog/delete-all

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
     - No
     - Eliminar registros anteriores a esta fecha/hora (formato ISO 8601)
   * - ``user``
     - String
     - No
     - Eliminar solo registros de un usuario especifico

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

Obtener Estadisticas de Busqueda
================================

Solicitud
---------

::

    GET /api/admin/searchlog/stats

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``from``
     - String
     - No
     - Fecha/hora de inicio (formato ISO 8601)
   * - ``to``
     - String
     - No
     - Fecha/hora de fin (formato ISO 8601)
   * - ``interval``
     - String
     - No
     - Intervalo de agregacion (hour/day/week/month)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalSearches": 50000,
          "uniqueUsers": 1234,
          "averageResponseTime": 156,
          "averageHitCount": 345,
          "zeroHitRate": 0.05,
          "topSearchWords": [
            {"word": "Fess", "count": 1500},
            {"word": "instalacion", "count": 800},
            {"word": "configuracion", "count": 650}
          ],
          "searchesByDate": [
            {"date": "2025-01-29", "count": 2500},
            {"date": "2025-01-28", "count": 2300},
            {"date": "2025-01-27", "count": 2100}
          ]
        }
      }
    }

Ejemplos de Uso
===============

Obtener Lista de Registros de Busqueda
--------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener por Periodo Especifico
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?from=2025-01-01T00:00:00Z&to=2025-01-31T23:59:59Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Registros de Busqueda de un Usuario Especifico
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?user=user001" \
         -H "Authorization: Bearer YOUR_TOKEN"

Registros de Busqueda de una Palabra Clave Especifica
-----------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?query=Fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Estadisticas de Busqueda
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31&interval=day" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Registros de Busqueda Antiguos
---------------------------------------

.. code-block:: bash

    # Eliminar registros anteriores a 30 dias
    curl -X DELETE "http://localhost:8080/api/admin/searchlog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraer Palabras Clave Populares de Busqueda
--------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.topSearchWords'

Analisis de Calidad de Busqueda
-------------------------------

.. code-block:: bash

    # Verificar la tasa de cero resultados
    curl -X GET "http://localhost:8080/api/admin/searchlog/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '{zeroHitRate: .response.stats.zeroHitRate, averageHitCount: .response.stats.averageHitCount}'

Tendencia de Busquedas por Dia
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?interval=day&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.searchesByDate'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-stats` - API de estadisticas del sistema
- :doc:`../../admin/searchlog-guide` - Guia de gestion de registros de busqueda
- :doc:`../../config/search-analytics` - Guia de configuracion de analisis de busqueda
