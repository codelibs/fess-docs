==========================
API de Stats
==========================

Vision General
==============

La API de Stats es para obtener informacion estadistica de |Fess|.
Puede verificar datos estadisticos de consultas de busqueda, clics, favoritos, etc.

URL Base
========

::

    /api/admin/stats

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
     - Obtener informacion estadistica

Obtener Informacion Estadistica
===============================

Solicitud
---------

::

    GET /api/admin/stats

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
   * - ``type``
     - String
     - No
     - Tipo de estadistica (query/click/favorite)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 12345,
          "uniqueQueries": 5678,
          "totalClicks": 9876,
          "totalFavorites": 543,
          "averageResponseTime": 123.45,
          "topQueries": [
            {
              "query": "fess",
              "count": 567
            },
            {
              "query": "search",
              "count": 432
            }
          ],
          "topClickedDocuments": [
            {
              "url": "https://example.com/doc1",
              "title": "Document 1",
              "count": 234
            }
          ],
          "queryTrends": [
            {
              "date": "2025-01-01",
              "count": 234
            },
            {
              "date": "2025-01-02",
              "count": 267
            }
          ]
        }
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``totalQueries``
     - Numero total de consultas de busqueda
   * - ``uniqueQueries``
     - Numero de consultas de busqueda unicas
   * - ``totalClicks``
     - Numero total de clics
   * - ``totalFavorites``
     - Numero total de favoritos
   * - ``averageResponseTime``
     - Tiempo de respuesta promedio (milisegundos)
   * - ``topQueries``
     - Consultas de busqueda populares
   * - ``topClickedDocuments``
     - Documentos populares
   * - ``queryTrends``
     - Tendencias de consultas

Estadisticas de Consultas de Busqueda
=====================================

Solicitud
---------

::

    GET /api/admin/stats?type=query&from=2025-01-01&to=2025-01-31

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 5678,
          "uniqueQueries": 2345,
          "topQueries": [
            {
              "query": "documentation",
              "count": 234,
              "avgResponseTime": 98.7
            }
          ],
          "queriesByHour": [
            {
              "hour": 0,
              "count": 45
            },
            {
              "hour": 1,
              "count": 23
            }
          ],
          "queriesByDay": [
            {
              "day": "Monday",
              "count": 567
            }
          ]
        }
      }
    }

Estadisticas de Clics
=====================

Solicitud
---------

::

    GET /api/admin/stats?type=click&from=2025-01-01&to=2025-01-31

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalClicks": 3456,
          "topClickedDocuments": [
            {
              "url": "https://example.com/popular-doc",
              "title": "Popular Document",
              "count": 234,
              "clickThroughRate": 0.45
            }
          ],
          "clicksByPosition": [
            {
              "position": 1,
              "count": 1234
            },
            {
              "position": 2,
              "count": 567
            }
          ]
        }
      }
    }

Ejemplos de Uso
===============

Obtener Todas las Estadisticas
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Estadisticas de Periodo Especifico
------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Estadisticas de Consultas de Busqueda
---------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener TOP 10 de Consultas Populares
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.stats.topQueries[:10]'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-log` - API de registros
- :doc:`api-admin-systeminfo` - API de informacion del sistema
