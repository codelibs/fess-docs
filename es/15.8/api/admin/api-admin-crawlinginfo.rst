==========================
API de CrawlingInfo
==========================

Vision General
==============

La API de CrawlingInfo es para consultar y gestionar la informacion de rastreo (sesiones de rastreo) de |Fess|.
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

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /logs
     - Obtener lista de informacion de rastreo
   * - GET
     - /log/{id}
     - Obtener informacion de rastreo
   * - DELETE
     - /log/{id}
     - Eliminar informacion de rastreo
   * - DELETE
     - /all
     - Eliminar en lote sesiones de rastreo (excepto las activas)

Obtener Lista de Informacion de Rastreo
=======================================

Solicitud
---------

::

    GET /api/admin/crawlinginfo/logs

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
   * - ``sessionId``
     - String
     - No
     - Filtro por ID de sesion (coincidencia parcial)

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
     - Descripcion
   * - ``id``
     - ID de informacion de rastreo
   * - ``sessionId``
     - ID de sesion
   * - ``name``
     - Nombre de sesion
   * - ``expiredTime``
     - Fecha de expiracion (milisegundos epoch; devuelto como cadena de texto)
   * - ``createdTime``
     - Hora de creacion (milisegundos epoch; devuelto como numero)

.. note::

   Cada objeto de registro en la respuesta incluye tambien un campo interno ``crudMode``
   (un entero que indica el modo de operacion CRUD, siempre ``0`` para operaciones de lectura).
   Los clientes pueden ignorarlo sin problema.

Obtener Informacion de Rastreo
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

Eliminar Informacion de Rastreo
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

Elimina todas las sesiones de rastreo (y sus datos de parametros), excepto las que estan en ejecucion en ese momento. No existe umbral de antiguedad ni de tiempo; se eliminan todas las sesiones que no esten en ejecucion.

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

Obtener Lista de Informacion de Rastreo
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Sesion Especifica
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener Informacion de Rastreo
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Informacion de Rastreo
-------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar en Lote Sesiones
-------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-failureurl` - API de URLs fallidas
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/crawlinginfo-guide` - Guia de informacion de rastreo
