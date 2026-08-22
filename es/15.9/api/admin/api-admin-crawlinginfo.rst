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
     - Número de elementos por página (predeterminado: 20)
   * - ``page``
     - Integer
     - No
     - Número de página (basado en 1, predeterminado: 1)
   * - ``sessionId``
     - String
     - No
     - Filtro por ID de sesión (coincidencia parcial)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
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
   * - ``sessionId``
     - ID de sesión
   * - ``name``
     - Nombre de sesión
   * - ``expiredTime``
     - Fecha de expiración (milisegundos epoch; devuelto como cadena de texto)
   * - ``createdTime``
     - Hora de creación (milisegundos epoch; devuelto como número)

.. note::

   Cada objeto de registro en la respuesta incluye también un campo interno ``crudMode``
   (un entero que indica el modo de operación CRUD, siempre ``0`` para operaciones de lectura).
   Los clientes pueden ignorarlo sin problema.

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
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
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

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Sesión Específica
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

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
