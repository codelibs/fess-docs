==========================
API de CrawlingInfo
==========================

Vision General
==============

La API de CrawlingInfo es para obtener informacion de rastreo de |Fess|.
Puede consultar el estado de las sesiones de rastreo, progreso e informacion estadistica.

URL Base
========

::

    /api/admin/crawlinginfo

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
     - Obtener lista de informacion de rastreo
   * - GET
     - /{sessionId}
     - Obtener detalles de sesion de rastreo
   * - DELETE
     - /{sessionId}
     - Eliminar sesion de rastreo

Obtener Lista de Informacion de Rastreo
=======================================

Solicitud
---------

::

    GET /api/admin/crawlinginfo

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

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``sessionId``
     - ID de sesion
   * - ``name``
     - Nombre del rastreador
   * - ``status``
     - Estado (running/completed/failed)
   * - ``startTime``
     - Hora de inicio
   * - ``endTime``
     - Hora de finalizacion
   * - ``crawlingInfoCount``
     - Numero de informacion de rastreo
   * - ``createdDocCount``
     - Numero de documentos creados
   * - ``updatedDocCount``
     - Numero de documentos actualizados
   * - ``deletedDocCount``
     - Numero de documentos eliminados

Obtener Detalles de Sesion de Rastreo
=====================================

Solicitud
---------

::

    GET /api/admin/crawlinginfo/{sessionId}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

Eliminar Sesion de Rastreo
==========================

Solicitud
---------

::

    DELETE /api/admin/crawlinginfo/{sessionId}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

Ejemplos de Uso
===============

Obtener Lista de Informacion de Rastreo
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Sesiones de Rastreo en Ejecucion
----------------------------------------

.. code-block:: bash

    # Obtener todas las sesiones y filtrar por running
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

Obtener Detalles de Sesion Especifica
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Sesion Antigua
-----------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Monitoreo de Progreso
---------------------

.. code-block:: bash

    # Verificar periodicamente el progreso de sesiones en ejecucion
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-failureurl` - API de URLs fallidas
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/crawlinginfo-guide` - Guia de informacion de rastreo
