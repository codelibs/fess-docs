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
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": "true",
            "crawler": "true",
            "available": "true",
            "sortOrder": 0,
            "versionNo": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   El objeto ``response`` siempre incluye ``version`` (versión del producto) y ``status`` (código de resultado). Consulte la descripción general de Admin API (:doc:`api-admin-overview`) para conocer el formato de respuesta común. Los ejemplos posteriores pueden omitir ``version`` por brevedad.

.. note::

   En las respuestas, ``jobLogging`` / ``crawler`` / ``available`` se devuelven como cadenas (``"true"`` / ``"false"``). ``running`` es un campo booleano exclusivo de respuesta que indica si el trabajo se está ejecutando en ese momento (no puede especificarse en las solicitudes). ``total`` es el número total de trabajos que coinciden con la consulta.

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
          "jobLogging": "true",
          "crawler": "true",
          "available": "true",
          "sortOrder": 0,
          "versionNo": 1,
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
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1
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
   * - ``cronExpression``
     - No
     - Expresión Cron (segundo minuto hora día mes día-semana). Max. 100 caracteres, validada como expresión cron. Si está vacía, el trabajo no se ejecuta de forma programada y solo puede iniciarse manualmente
   * - ``scriptType``
     - Sí
     - Tipo de script (max. 100 caracteres). Actualmente solo se admite ``groovy``
   * - ``scriptData``
     - No
     - Script de ejecución. El tamaño máximo sigue ``form.admin.max.input.size`` en ``fess_config.properties``
   * - ``jobLogging``
     - No
     - Habilitar registro de trabajos (cadena)
   * - ``crawler``
     - No
     - Si es un trabajo de rastreo (cadena)
   * - ``available``
     - No
     - Habilitado/Deshabilitado (cadena)
   * - ``sortOrder``
     - Sí
     - Orden de visualización (entero entre 0 y 2147483647)

.. note::

   ``jobLogging`` / ``crawler`` / ``available`` son campos de cadena. En las solicitudes, especificar ``"on"`` o ``"true"`` (sin distinción de mayúsculas y minúsculas) los habilita; cualquier otro valor (``"false"``, cadena vacía o no especificado) se trata como deshabilitado. En las respuestas se devuelven como ``"true"`` / ``"false"``.

.. note::

   ``crudMode`` se establece automáticamente en el servidor y no es necesario especificarlo en las solicitudes. Los campos de auditoría como ``createdBy`` / ``createdTime`` también se establecen en el servidor.

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
   * - ``0 0 2 * * ?``
     - Ejecutar diariamente a las 2 AM
   * - ``0 0 0/6 * * ?``
     - Ejecutar cada 6 horas
   * - ``0 0 2 * * MON``
     - Ejecutar cada lunes a las 2 AM
   * - ``0 0 2 1 * ?``
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
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1,
      "versionNo": 1
    }

.. note::

   Para las actualizaciones, ``id`` (max. 1000 caracteres) y ``versionNo`` son obligatorios. ``versionNo`` se utiliza para el bloqueo optimista; especifique el valor devuelto en la respuesta de obtención. Si el valor no coincide, la actualización falla. Los demás campos obligatorios (``name`` / ``target`` / ``scriptType`` / ``sortOrder``) son los mismos que para la creación.

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
        "jobLogId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``jobLogId``
     - ID del registro del trabajo iniciado. Se emite cuando el registro de trabajos está habilitado. Es ``null`` cuando el registro de trabajos está deshabilitado.

Notas
-----

- Si el trabajo ya está en ejecución, el inicio falla y se devuelve un error (``status`` distinto de ``0``).
- Si el trabajo está deshabilitado (``available`` no está habilitado), el inicio también falla con un error.
- ``jobLogId`` solo se emite cuando el registro de trabajos está habilitado (``jobLogging`` está habilitado).

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
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": "true",
           "crawler": "true",
           "available": "true",
           "sortOrder": 1
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
