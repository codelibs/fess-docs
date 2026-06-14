==========================
API de Stats
==========================

Vision General
==============

La API de Stats es para obtener metricas del sistema del servidor donde se ejecuta |Fess|.
Puede verificar las estadisticas de JVM, OS, proceso, cluster del motor de busqueda (OpenSearch) y sistema de archivos.

.. note::

   Esta API no devuelve datos de analisis de busqueda como consultas de busqueda o clics.
   Para buscar y gestionar documentos del indice, consulte :doc:`api-admin-searchlist`.

URL Base
========

::

    /api/admin/stats

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
     - Obtener informacion estadistica del sistema

Obtener Informacion Estadistica del Sistema
===========================================

Solicitud
---------

::

    GET /api/admin/stats

Este endpoint no acepta parametros de consulta.

Respuesta
---------

La respuesta incluye ``version``, que indica la version del producto, ``status``, que indica el resultado del procesamiento, y el objeto ``stats``, que almacena las metricas del sistema.
``stats`` tiene cinco claves: ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "stats": {
          "jvm": {
            "memory": {
              "heap": {
                "used": 536870912,
                "committed": 1073741824,
                "max": 2147483648,
                "percent": 25
              },
              "nonHeap": {
                "used": 134217728,
                "committed": 268435456
              }
            },
            "pools": [
              {"key": "mapped", "count": 1, "used": 4096, "capacity": 4096}
            ],
            "gc": [
              {"key": "young", "count": 12, "time": 345}
            ],
            "threads": {"count": 80, "peak": 95},
            "classes": {"loaded": 12000, "total_loaded": 12500, "unloaded": 500},
            "uptime": 3600000
          },
          "os": {
            "memory": {
              "physical": {"free": 2147483648, "total": 8589934592},
              "swapSpace": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "loadAverages": [0.5, 0.4, 0.3]
          },
          "process": {
            "fileFescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtualMemory": {"total": 4294967296}
          },
          "engine": {
            "clusterName": "fess",
            "numberOfNodes": 1,
            "numberOfDataNodes": 1,
            "activePrimaryShards": 10,
            "activeShards": 10,
            "activeShardsPercent": 100.0,
            "relocatingShards": 0,
            "initializingShards": 0,
            "unassignedShards": 0,
            "delayedUnassignedShards": 0,
            "numberOfPendingTasks": 0,
            "numberOfInFlightFetch": 0,
            "status": "green"
          },
          "fs": [
            {
              "path": "/",
              "total": 107374182400,
              "free": 53687091200,
              "usable": 53687091200,
              "used": 53687091200,
              "percent": 50
            }
          ]
        }
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Campo
     - Descripcion
   * - ``jvm``
     - Estadisticas de la JVM. Incluye ``memory`` (``heap`` / ``nonHeap``), ``pools`` (grupos de buffers), ``gc`` (GC), ``threads``, ``classes`` y ``uptime`` (milisegundos).
   * - ``os``
     - Estadisticas del OS. Incluye ``memory`` (``physical`` / ``swapSpace``), ``cpu`` y ``loadAverages`` (arreglo de promedios de carga).
   * - ``process``
     - Estadisticas del proceso. Incluye ``fileFescriptor`` (numero de descriptores de archivo abiertos/maximos), ``cpu`` y ``virtualMemory``.
   * - ``engine``
     - Estado del cluster del motor de busqueda (OpenSearch). Incluye ``clusterName``, numero de nodos, numero de shards, ``status``, etc. Si no se puede conectar al cluster, ``status`` sera ``"red"`` y ``exception`` contendra el mensaje de error.
   * - ``fs``
     - Arreglo de estadisticas del sistema de archivos. Para cada raiz incluye ``path``, ``total``, ``free``, ``usable``, ``used`` (bytes) y ``percent`` (porcentaje de uso).

.. note::

   El nombre de clave ``process.fileFescriptor`` se ajusta a la implementacion del codigo fuente (no es la grafia ``fileDescriptor``).

Ejemplos de Uso
===============

Obtener Informacion Estadistica del Sistema
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verificar el Uso del Heap de la JVM
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Verificar el Estado del Cluster del Motor de Busqueda
-----------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-systeminfo` - API de informacion del sistema
- :doc:`api-admin-searchlist` - API de busqueda y gestion de documentos
