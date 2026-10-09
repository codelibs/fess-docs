==========================
API de Scheduler
==========================

Visión General
==============

La API de Scheduler es para gestionar trabajos programados de |Fess|.
Puede iniciar/detener trabajos de rastreo, crear/actualizar/eliminar configuraciones de programación.

URL Base
========

::

    /api/admin/scheduler

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
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

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (por defecto: 25; configurable mediante ``paging.page.size`` en ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Número de página (a partir de 1; por defecto: 1)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cron_expression": "0 0 * * *",
            "script_type": "javascript",
            "script_data": "...",
            "job_logging": "true",
            "crawler": "true",
            "available": "true",
            "sort_order": 0,
            "version_no": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   El objeto ``response`` siempre incluye ``version`` (versión del producto) y ``status`` (código de resultado). Consulte la descripción general de Admin API (:doc:`api-admin-overview`) para conocer el formato de respuesta común. Los ejemplos posteriores pueden omitir ``version`` por brevedad.

.. note::

   En las respuestas, ``job_logging`` / ``crawler`` / ``available`` se devuelven como cadenas (``"true"`` / ``"false"``). ``running`` es un campo booleano exclusivo de respuesta que indica si el trabajo se está ejecutando en ese momento (no puede especificarse en las solicitudes). ``total`` es el número total de trabajos que coinciden con la consulta.

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
          "cron_expression": "0 0 * * *",
          "script_type": "javascript",
          "script_data": "return container.getComponent(\"crawlJob\").execute();",
          "job_logging": "true",
          "crawler": "true",
          "available": "true",
          "sort_order": 0,
          "version_no": 1,
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
      "cron_expression": "0 2 * * *",
      "script_type": "javascript",
      "script_data": "return container.getComponent(\"crawlJob\").execute();",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``name``
     - Sí
     - Nombre del trabajo (max. 100 caracteres)
   * - ``target``
     - Sí
     - Objetivo de ejecución (max. 100 caracteres). Especifique ``all`` o un nombre de objetivo específico
   * - ``cron_expression``
     - No
     - Expresión Cron (cinco campos: minuto hora día mes día-semana, en formato cron4j). Max. 100 caracteres, validada como expresión cron. No se puede usar un campo de segundos al estilo Quartz ni ``?`` (``0 0 * * * ?`` se rechaza). Si está vacía, el trabajo no se ejecuta de forma programada y solo puede iniciarse manualmente
   * - ``script_type``
     - Sí
     - Tipo de script (max. 100 caracteres). ``javascript`` (valor predeterminado para trabajos nuevos, determinado por la propiedad ``job.default.script``) o ``groovy`` (requiere el plugin ``fess-script-groovy``)
   * - ``script_data``
     - No
     - Script de ejecución. El tamaño máximo sigue ``form.admin.max.input.size`` en ``fess_config.properties``
   * - ``job_logging``
     - No
     - Habilitar registro de trabajos (cadena)
   * - ``crawler``
     - No
     - Si es un trabajo de rastreo (cadena)
   * - ``available``
     - No
     - Habilitado/Deshabilitado (cadena)
   * - ``sort_order``
     - Sí
     - Orden de visualización (entero entre 0 y 2147483647)

.. note::

   ``job_logging`` / ``crawler`` / ``available`` son campos de cadena. En las solicitudes, especificar ``"on"`` o ``"true"`` (sin distinción de mayúsculas y minúsculas) los habilita; cualquier otro valor (``"false"``, cadena vacía o no especificado) se trata como deshabilitado. En las respuestas se devuelven como ``"true"`` / ``"false"``.

.. note::

   ``crud_mode`` se establece automáticamente en el servidor y no es necesario especificarlo en las solicitudes. Los campos de auditoría como ``created_by`` / ``created_time`` también se establecen en el servidor.

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

   * - Expresión Cron
     - Descripción
   * - ``0 2 * * *``
     - Ejecutar diariamente a las 2 AM
   * - ``0 */6 * * *``
     - Ejecutar cada 6 horas
   * - ``0 2 * * 1``
     - Ejecutar cada lunes a las 2 AM (los días de la semana van de ``0`` para domingo a ``6`` para sábado)
   * - ``0 2 1 * *``
     - Ejecutar el día 1 de cada mes a las 2 AM

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
      "cron_expression": "0 3 * * *",
      "script_type": "javascript",
      "script_data": "...",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1,
      "version_no": 1
    }

.. note::

   Para las actualizaciones, ``id`` (max. 1000 caracteres) y ``version_no`` son obligatorios. ``version_no`` se utiliza para el bloqueo optimista; especifique el valor devuelto en la respuesta de obtención. Si el valor no coincide, la actualización falla. Los demás campos obligatorios (``name`` / ``target`` / ``script_type`` / ``sort_order``) son los mismos que para la creación.

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
        "status": 0,
        "job_log_id": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``job_log_id``
     - ID del registro del trabajo iniciado. Se emite cuando el registro de trabajos está habilitado. Se omite de la respuesta cuando el registro de trabajos está deshabilitado.

Notas
-----

- Si el trabajo ya está en ejecución, el inicio falla y se devuelve un error (``status`` distinto de ``0``).
- Si el trabajo está deshabilitado (``available`` no está habilitado), el inicio también falla con un error.
- ``job_log_id`` solo se emite cuando el registro de trabajos está habilitado (``job_logging`` está habilitado).

Detener Trabajo
===============

Detiene un trabajo en ejecución.

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
           "cron_expression": "0 * * * *",
           "script_type": "javascript",
           "script_data": "return container.getComponent(\"crawlJob\").execute();",
           "job_logging": "true",
           "crawler": "true",
           "available": "true",
           "sort_order": 1
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

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/scheduler-guide` - Guía de gestión del programador
