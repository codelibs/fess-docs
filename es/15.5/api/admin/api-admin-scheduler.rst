==========================
API de Scheduler
==========================

Vision General
==============

La API de Scheduler es para gestionar trabajos programados de |Fess|.
Puede iniciar/detener trabajos de rastreo, crear/actualizar/eliminar configuraciones de programacion.

URL Base
========

::

    /api/admin/scheduler

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET/PUT
     - /settings
     - Obtener lista de trabajos programados
   * - GET
     - /setting/{id}
     - Obtener trabajo programado
   * - POST
     - /setting
     - Crear trabajo programado
   * - PUT
     - /setting
     - Actualizar trabajo programado
   * - DELETE
     - /setting/{id}
     - Eliminar trabajo programado
   * - PUT
     - /{id}/start
     - Iniciar trabajo
   * - PUT
     - /{id}/stop
     - Detener trabajo

Obtener Lista de Trabajos Programados
=====================================

Solicitud
---------

::

    GET /api/admin/scheduler/settings
    PUT /api/admin/scheduler/settings

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
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": true,
            "crawler": true,
            "available": true,
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

Obtener Trabajo Programado
==========================

Solicitud
---------

::

    GET /api/admin/scheduler/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cronExpression": "0 0 0 * * ?",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "jobLogging": true,
          "crawler": true,
          "available": true,
          "sortOrder": 0,
          "running": false
        }
      }
    }

Crear Trabajo Programado
========================

Solicitud
---------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre del trabajo
   * - ``target``
     - Si
     - Objetivo de ejecucion ("all" u objetivo especifico)
   * - ``cronExpression``
     - Si
     - Expresion Cron (segundos minutos horas dia mes dia-semana)
   * - ``scriptType``
     - Si
     - Tipo de script ("groovy")
   * - ``scriptData``
     - Si
     - Script de ejecucion
   * - ``jobLogging``
     - No
     - Habilitar registro (predeterminado: true)
   * - ``crawler``
     - No
     - Es trabajo de rastreo (predeterminado: false)
   * - ``available``
     - No
     - Habilitado/Deshabilitado (predeterminado: true)
   * - ``sortOrder``
     - No
     - Orden de visualizacion

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Ejemplos de Expresiones Cron
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Expresion Cron
     - Descripcion
   * - ``0 0 2 * * ?``
     - Ejecutar diariamente a las 2 AM
   * - ``0 0 0/6 * * ?``
     - Ejecutar cada 6 horas
   * - ``0 0 2 * * MON``
     - Ejecutar cada lunes a las 2 AM
   * - ``0 0 2 1 * ?``
     - Ejecutar el dia 1 de cada mes a las 2 AM

Actualizar Trabajo Programado
=============================

Solicitud
---------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

Eliminar Trabajo Programado
===========================

Solicitud
---------

::

    DELETE /api/admin/scheduler/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

Iniciar Trabajo
===============

Ejecuta inmediatamente un trabajo programado.

Solicitud
---------

::

    PUT /api/admin/scheduler/{id}/start

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Notas
-----

- Se devuelve un error si el trabajo ya esta en ejecucion
- Se devuelve un error si el trabajo esta deshabilitado (``available: false``)

Detener Trabajo
===============

Detiene un trabajo en ejecucion.

Solicitud
---------

::

    PUT /api/admin/scheduler/{id}/stop

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplos de Uso
===============

Crear y Ejecutar Trabajo de Rastreo
-----------------------------------

.. code-block:: bash

    # Crear trabajo
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": true,
           "crawler": true,
           "available": true
         }'

    # Ejecutar trabajo inmediatamente
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verificar Estado del Trabajo
----------------------------

.. code-block:: bash

    # Verificar estado de todos los trabajos
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Puede verificar el estado de ejecucion con el campo running

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/scheduler-guide` - Guia de gestion del programador
