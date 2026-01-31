==========================
API de JobLog
==========================

Vision General
==============

La API de JobLog es para obtener registros de ejecucion de trabajos de |Fess|.
Puede verificar el historial de ejecucion e informacion de errores de trabajos programados y de rastreo.

URL Base
========

::

    /api/admin/joblog

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
     - Obtener lista de registros de trabajos
   * - GET
     - /{id}
     - Obtener detalles de registro de trabajo
   * - DELETE
     - /{id}
     - Eliminar registro de trabajo
   * - DELETE
     - /delete-all
     - Eliminar todos los registros de trabajos

Obtener Lista de Registros de Trabajos
======================================

Solicitud
---------

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - No
     - Filtro de estado (ok/fail/running)
   * - ``from``
     - String
     - No
     - Fecha/hora de inicio (formato ISO 8601)
   * - ``to``
     - String
     - No
     - Fecha/hora de fin (formato ISO 8601)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
          }
        ],
        "total": 100
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
     - ID del registro de trabajo
   * - ``jobName``
     - Nombre del trabajo
   * - ``jobStatus``
     - Estado del trabajo (ok/fail/running)
   * - ``target``
     - Objetivo de ejecucion
   * - ``scriptType``
     - Tipo de script
   * - ``scriptData``
     - Script ejecutado
   * - ``scriptResult``
     - Resultado de ejecucion
   * - ``startTime``
     - Hora de inicio
   * - ``endTime``
     - Hora de finalizacion
   * - ``executionTime``
     - Tiempo de ejecucion (milisegundos)

Obtener Detalles de Registro de Trabajo
=======================================

Solicitud
---------

::

    GET /api/admin/joblog/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

Eliminar Registro de Trabajo
============================

Solicitud
---------

::

    DELETE /api/admin/joblog/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

Eliminar Todos los Registros de Trabajos
========================================

Solicitud
---------

::

    DELETE /api/admin/joblog/delete-all

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
   * - ``status``
     - String
     - No
     - Eliminar solo registros con estado especifico

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

Ejemplos de Uso
===============

Obtener Lista de Registros de Trabajos
--------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Solo Trabajos Fallidos
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Registros de Trabajos de Periodo Especifico
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Detalles de Registro de Trabajo
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Registros de Trabajos Antiguos
---------------------------------------

.. code-block:: bash

    # Eliminar registros de mas de 30 dias
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Solo Registros de Trabajos Fallidos
--------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Detectar Trabajos con Tiempo de Ejecucion Largo
-----------------------------------------------

.. code-block:: bash

    # Extraer trabajos que tardaron mas de 1 hora
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

Calcular Tasa de Exito de Trabajos
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-scheduler` - API del programador
- :doc:`api-admin-crawlinginfo` - API de informacion de rastreo
- :doc:`../../admin/joblog-guide` - Guia de gestion de registros de trabajos
