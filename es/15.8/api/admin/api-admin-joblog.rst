==========================
API de JobLog
==========================

Vision General
==============

La API de JobLog es para consultar y gestionar los registros de ejecucion de trabajos de |Fess|.
Permite obtener y eliminar el historial de ejecucion, los resultados y la informacion de errores
de trabajos programados y de rastreo.

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
     - /logs
     - Obtener lista de registros de trabajos
   * - GET
     - /log/{id}
     - Obtener registro de trabajo
   * - DELETE
     - /log/{id}
     - Eliminar registro de trabajo

Obtener Lista de Registros de Trabajos
=======================================

Solicitud
---------

::

    GET /api/admin/joblog/logs

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
     - Numero de pagina (basado en 1, predeterminado: 1)
   * - ``id``
     - String
     - No
     - Filtro por ID de registro de trabajo (coincidencia exacta)

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
            "startTime": "1738116000000",
            "endTime": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "1738029600000",
            "endTime": "1738030215000"
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
     - Estado del trabajo (``ok``: exitoso, ``fail``: fallido, ``running``: en ejecucion)
   * - ``target``
     - Objetivo de ejecucion (nombre del objetivo del programador; el valor predeterminado es ``all``)
   * - ``scriptType``
     - Tipo de script (ejemplo: ``groovy``)
   * - ``scriptData``
     - Script ejecutado
   * - ``scriptResult``
     - Resultado de la ejecucion
   * - ``startTime``
     - Hora de inicio (milisegundos epoch; devuelto como cadena de texto)
   * - ``endTime``
     - Hora de finalizacion (milisegundos epoch; devuelto como cadena de texto). No se devuelve para trabajos en ejecucion.

.. note::

   Cada objeto de registro en la respuesta incluye tambien un campo interno ``crudMode``
   (un entero que indica el modo de operacion CRUD, siempre ``0`` para operaciones de lectura).
   Los clientes pueden ignorarlo sin problema.

Obtener Registro de Trabajo
============================

Solicitud
---------

::

    GET /api/admin/joblog/log/{id}

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
          "startTime": "1738116000000",
          "endTime": "1738118723000"
        }
      }
    }

Si el registro de trabajo con el ID especificado no existe, se devuelve una respuesta de error
con ``status`` establecido en un valor distinto de 0.

Eliminar Registro de Trabajo
=============================

Solicitud
---------

::

    DELETE /api/admin/joblog/log/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Si el registro de trabajo con el ID especificado no existe, se devuelve una respuesta de error
con ``status`` establecido en un valor distinto de 0.

Ejemplos de Uso
===============

Obtener Lista de Registros de Trabajos
--------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraer Solo Trabajos Fallidos
------------------------------

.. code-block:: bash

    # Filtrar trabajos fallidos con jq
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

Obtener Registro de Trabajo
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Registro de Trabajo
-----------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Calcular Tasa de Exito de Trabajos
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-scheduler` - API del programador
- :doc:`api-admin-crawlinginfo` - API de informacion de rastreo
- :doc:`../../admin/joblog-guide` - Guia de gestion de registros de trabajos
