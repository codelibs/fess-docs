==========================
API de CrawlingInfo
==========================

Visión General
==============

La API de CrawlingInfo es para consultar y gestionar la información de rastreo (sesiones de rastreo) de |Fess|.
Permite operaciones como obtener la lista de sesiones de rastreo, obtenerlas individualmente y eliminarlas.

URL Base
========

::

    /api/admin/crawlinginfo

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /logs
     - Obtener lista de información de rastreo
   * - GET
     - /progress
     - Obtener el progreso de los rastreos en ejecución
   * - GET
     - /log/{id}
     - Obtener información de rastreo
   * - DELETE
     - /log/{id}
     - Eliminar información de rastreo
   * - DELETE
     - /all
     - Eliminar en lote sesiones de rastreo (excepto las activas)

Obtener Lista de Información de Rastreo
=======================================

Solicitud
---------

::

    GET /api/admin/crawlinginfo/logs

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
     - Número de elementos por página (predeterminado: 25; se puede cambiar con ``paging.page.size`` en ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Número de página (basado en 1, predeterminado: 1)
   * - ``session_id``
     - String
     - No
     - Filtro por ID de sesión (coincidencia parcial)

Estos parámetros se indican en el cuerpo de la solicitud JSON (por ejemplo, ``{"size": 50, "page": 1}``). Los valores indicados en la cadena de consulta de la URL (por ejemplo, ``?size=50``) se ignoran, por lo que, si no se indican en el cuerpo, siempre se devuelven los primeros 25 elementos.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "session_id": "20250129100000",
            "name": "Default Crawler",
            "expired_time": "1738200000000",
            "created_time": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "session_id": "20250128100000",
            "name": "Default Crawler",
            "expired_time": "1738113600000",
            "created_time": 1738022400000
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
     - Descripción
   * - ``id``
     - ID de información de rastreo
   * - ``session_id``
     - ID de sesión
   * - ``name``
     - Nombre de sesión
   * - ``expired_time``
     - Fecha de expiración (milisegundos epoch; devuelto como cadena de texto)
   * - ``created_time``
     - Hora de creación (milisegundos epoch; devuelto como número)

.. note::

   Cada objeto de registro en la respuesta incluye también un campo interno ``crud_mode``
   (un entero que indica el modo de operación CRUD, siempre ``0`` para operaciones de lectura).
   Los clientes pueden ignorarlo sin problema.

Obtener el progreso de los rastreos en ejecución
================================================

Devuelve el progreso de los rastreos que se están ejecutando, una entrada por cada configuración de rastreo (web, sistema de archivos o almacén de datos). Es la misma información que "Rastreos en ejecución" en la página Información de rastreo de la interfaz de administración (consulte :doc:`../../admin/crawlinginfo-guide`).

Solicitud
---------

::

    GET /api/admin/crawlinginfo/progress

Este endpoint no acepta parámetros.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "progress": [
          {
            "config_id": "Wabc123",
            "name": "Example Site",
            "count": 4200,
            "last_count": 10000,
            "updated_time": 1738144800000,
            "percent": 42
          },
          {
            "config_id": "Ddef456",
            "name": "Example Database",
            "count": 1500,
            "last_count": 0,
            "updated_time": 1738144795000
          }
        ],
        "total": 2
      }
    }

Campos de la respuesta
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``progress``
     - Matriz de los rastreos en ejecución, ordenada por el nombre de la configuración de rastreo. Una matriz vacía si no hay ningún rastreo en ejecución
   * - ``total``
     - Número de elementos de ``progress``

Cada elemento de ``progress`` tiene los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``config_id``
     - ID de la configuración de rastreo (empieza por ``W`` para web, ``F`` para sistema de archivos y ``D`` para almacén de datos)
   * - ``name``
     - Nombre de la configuración de rastreo (``config_id`` si no se encuentra la configuración)
   * - ``count``
     - Número de documentos que el rastreo en ejecución ha procesado hasta ahora
   * - ``last_count``
     - Número de documentos del último rastreo completado (``0`` si se desconoce)
   * - ``updated_time``
     - Momento en que se escribió ``count`` (milisegundos epoch, un número)
   * - ``percent``
     - ``count`` como porcentaje de ``last_count`` (de ``0`` a ``99``). Se omite si no hay un rastreo completado anterior

.. note::

   Un rastreo terminado o detenido no se incluye. Si el rastreador se detiene sin registrarlo (por ejemplo, porque se mata el proceso), el rastreo deja de incluirse cuando han pasado unos 30 segundos (de forma predeterminada) desde su última actualización. El ``count`` de un rastreo web o de sistema de archivos es el número de resultados de acceso; el de un rastreo de almacén de datos es el número de documentos indexados para la configuración de rastreo.

Obtener Información de Rastreo
==============================

Solicitud
---------

::

    GET /api/admin/crawlinginfo/log/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "session_id": "20250129100000",
          "name": "Default Crawler",
          "expired_time": "1738200000000",
          "created_time": 1738108800000
        }
      }
    }

Eliminar Información de Rastreo
===============================

Solicitud
---------

::

    DELETE /api/admin/crawlinginfo/log/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Eliminar en Lote Sesiones de Rastreo
=====================================

Elimina todas las sesiones de rastreo (y sus datos de parámetros), excepto las que están en ejecución en ese momento. No existe umbral de antigüedad ni de tiempo; se eliminan todas las sesiones que no estén en ejecución.

Solicitud
---------

::

    DELETE /api/admin/crawlinginfo/all

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

Obtener Lista de Información de Rastreo
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

Filtrar por Sesión Específica
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"session_id": "20250129100000"}'

Obtener Información de Rastreo
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Información de Rastreo
-------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar en Lote Sesiones
-------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-failureurl` - API de URLs fallidas
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/crawlinginfo-guide` - Guía de información de rastreo
