==========================
API de Storage
==========================

Vision General
==============

La API de Storage es para gestionar el almacenamiento de |Fess|.
Puede operar el estado de uso del almacenamiento de indices y la optimizacion.

URL Base
========

::

    /api/admin/storage

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
     - Obtener informacion de almacenamiento
   * - POST
     - /optimize
     - Optimizar indice
   * - POST
     - /flush
     - Vaciar indice

Obtener Informacion de Almacenamiento
=====================================

Solicitud
---------

::

    GET /api/admin/storage

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "storage": {
          "indices": [
            {
              "name": "fess.20250129",
              "status": "open",
              "health": "green",
              "docsCount": 123456,
              "docsDeleted": 234,
              "storeSize": "5.2gb",
              "primariesStoreSize": "2.6gb",
              "shards": 5,
              "replicas": 1
            }
          ],
          "totalStoreSize": "5.2gb",
          "totalDocsCount": 123456,
          "clusterHealth": "green",
          "diskUsage": {
            "total": "107374182400",
            "available": "53687091200",
            "used": "53687091200",
            "usedPercent": 50.0
          }
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
   * - ``indices``
     - Lista de indices
   * - ``name``
     - Nombre del indice
   * - ``status``
     - Estado del indice (open/close)
   * - ``health``
     - Estado de salud (green/yellow/red)
   * - ``docsCount``
     - Numero de documentos
   * - ``docsDeleted``
     - Numero de documentos eliminados
   * - ``storeSize``
     - Tamano de almacenamiento
   * - ``primariesStoreSize``
     - Tamano de shards primarios
   * - ``shards``
     - Numero de shards
   * - ``replicas``
     - Numero de replicas
   * - ``totalStoreSize``
     - Tamano total de almacenamiento
   * - ``totalDocsCount``
     - Numero total de documentos
   * - ``clusterHealth``
     - Estado de salud del cluster
   * - ``diskUsage``
     - Uso de disco

Optimizar Indice
================

Solicitud
---------

::

    POST /api/admin/storage/optimize
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129",
      "maxNumSegments": 1,
      "onlyExpungeDeletes": false,
      "flush": true
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``index``
     - No
     - Nombre del indice (si no se especifica, todos los indices)
   * - ``maxNumSegments``
     - No
     - Numero maximo de segmentos (predeterminado: 1)
   * - ``onlyExpungeDeletes``
     - No
     - Solo eliminar documentos eliminados (predeterminado: false)
   * - ``flush``
     - No
     - Vaciar despues de optimizar (predeterminado: true)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index optimization started"
      }
    }

Vaciar Indice
=============

Solicitud
---------

::

    POST /api/admin/storage/flush
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``index``
     - No
     - Nombre del indice (si no se especifica, todos los indices)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index flushed successfully"
      }
    }

Ejemplos de Uso
===============

Obtener Informacion de Almacenamiento
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN"

Optimizar Todos los Indices
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "maxNumSegments": 1,
           "flush": true
         }'

Optimizar un Indice Especifico
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129",
           "maxNumSegments": 1,
           "onlyExpungeDeletes": false
         }'

Eliminar Solo Documentos Eliminados
-----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "onlyExpungeDeletes": true
         }'

Vaciar un Indice
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/flush" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129"
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`../../admin/storage-guide` - Guia de gestion de almacenamiento
