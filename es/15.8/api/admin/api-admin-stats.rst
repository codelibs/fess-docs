==========================
API de Stats
==========================

Visión General
==============

La API de Stats es una API para obtener métricas del sistema del servidor donde se ejecuta |Fess|.
Puede ver información estadística de la JVM, el sistema operativo, el proceso, el cluster del motor de búsqueda (OpenSearch) y el sistema de archivos.

.. note::

   Esta API no devuelve datos de análisis de búsqueda como consultas de búsqueda o clics.
   Para buscar y gestionar documentos del índice, consulte :doc:`api-admin-searchlist`.

URL Base
========

::

    /api/admin/stats

El acceso a esta API requiere un token de acceso con el permiso ``Radmin-api``.
Para obtener detalles sobre la autenticación, consulte :doc:`api-admin-overview`.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /
     - Obtener información estadística del sistema

Obtener Información Estadística del Sistema
===========================================

Solicitud
---------

::

    GET /api/admin/stats

Este endpoint no acepta parámetros de consulta.

Respuesta
---------

La respuesta incluye ``version``, que indica la versión del producto, ``status``, que indica
el resultado del procesamiento, y un objeto ``stats`` que almacena las métricas del sistema.
``stats`` tiene cinco claves: ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. note::

   Los nombres de campo de los objetos bajo ``stats`` se presentan en snake_case (palabras en minúsculas separadas por guiones bajos, por ejemplo ``non_heap``).
   Los campos cuyo valor es ``null`` se omiten de la respuesta.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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
              "non_heap": {
                "used": 134217728,
                "committed": 268435456,
                "max": 0,
                "percent": 0
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
              "swap_space": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "load_averages": [0.5, 0.4, 0.3]
          },
          "process": {
            "file_fescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtual_memory": {"total": 4294967296}
          },
          "engine": {
            "cluster_name": "fess",
            "number_of_nodes": 1,
            "number_of_data_nodes": 1,
            "active_primary_shards": 10,
            "active_shards": 10,
            "active_shards_percent": 100.0,
            "relocating_shards": 0,
            "initializing_shards": 0,
            "unassigned_shards": 0,
            "delayed_unassigned_shards": 0,
            "number_of_pending_tasks": 0,
            "number_of_in_flight_fetch": 0,
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

Campos de Respuesta (Nivel Superior)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Campo
     - Descripción
   * - ``version``
     - La versión del producto de |Fess| (por ejemplo, ``15.8.0``).
   * - ``status``
     - Código que indica el resultado del procesamiento. ``0`` indica que se completó correctamente.
   * - ``stats``
     - Objeto que almacena las métricas del sistema. Tiene cinco claves: ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

``jvm``: Estadísticas de la JVM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Descripción
   * - ``memory.heap.used``
     - Memoria heap utilizada (bytes).
   * - ``memory.heap.committed``
     - Memoria heap comprometida (bytes).
   * - ``memory.heap.max``
     - Memoria heap máxima (bytes).
   * - ``memory.heap.percent``
     - Porcentaje de uso de la memoria heap (%).
   * - ``memory.non_heap.used``
     - Memoria no-heap utilizada (bytes).
   * - ``memory.non_heap.committed``
     - Memoria no-heap comprometida (bytes).
   * - ``memory.non_heap.max``
     - Memoria no-heap máxima (bytes). En la implementación actual este valor no se establece y siempre devuelve ``0``.
   * - ``memory.non_heap.percent``
     - Porcentaje de uso de la memoria no-heap (%). En la implementación actual este valor no se establece y siempre devuelve ``0``.
   * - ``pools``
     - Arreglo de grupos de buffers. Cada elemento incluye ``key`` (nombre del grupo), ``count`` (número de buffers), ``used`` (memoria utilizada, bytes) y ``capacity`` (capacidad total, bytes).
   * - ``gc``
     - Arreglo de recolectores de basura. Cada elemento incluye ``key`` (nombre del recolector), ``count`` (número de recolecciones) y ``time`` (tiempo acumulado de recolección, milisegundos).
   * - ``threads.count``
     - Número actual de hilos.
   * - ``threads.peak``
     - Número máximo de hilos alcanzado.
   * - ``classes.loaded``
     - Número de clases cargadas actualmente.
   * - ``classes.total_loaded``
     - Número total de clases cargadas desde que se inició la JVM.
   * - ``classes.unloaded``
     - Número total de clases descargadas.
   * - ``uptime``
     - Tiempo de actividad de la JVM (milisegundos).

``os``: Estadísticas del Sistema Operativo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Descripción
   * - ``memory.physical.free``
     - Memoria física libre (bytes).
   * - ``memory.physical.total``
     - Memoria física total (bytes).
   * - ``memory.swap_space.free``
     - Espacio de intercambio libre (bytes).
   * - ``memory.swap_space.total``
     - Espacio de intercambio total (bytes).
   * - ``cpu.percent``
     - Porcentaje de uso de CPU a nivel del sistema (%).
   * - ``load_averages``
     - Arreglo de promedios de carga (1, 5 y 15 minutos). Los valores que no se pueden obtener pueden ser ``-1``.

``process``: Estadísticas del Proceso
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Descripción
   * - ``file_fescriptor.open``
     - Número de descriptores de archivo abiertos actualmente.
   * - ``file_fescriptor.max``
     - Número máximo de descriptores de archivo que se pueden abrir.
   * - ``cpu.percent``
     - Porcentaje de uso de CPU del proceso (%).
   * - ``cpu.total``
     - Tiempo de CPU acumulado utilizado por el proceso (milisegundos).
   * - ``virtual_memory.total``
     - Tamaño total de la memoria virtual del proceso (bytes).

.. note::

   El nombre de clave ``process.file_fescriptor`` es la conversión a snake_case del nombre de campo del código fuente
   ``fileFescriptor`` (que se origina de una falta de ortografía de ``fileDescriptor``). Coincide con
   la implementación y no es un error tipográfico en este documento.

``engine``: Estadísticas del Cluster del Motor de Búsqueda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Información de salud del cluster del motor de búsqueda (OpenSearch).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Descripción
   * - ``cluster_name``
     - Nombre del cluster.
   * - ``number_of_nodes``
     - Número total de nodos en el cluster.
   * - ``number_of_data_nodes``
     - Número de nodos de datos.
   * - ``active_primary_shards``
     - Número de shards primarios activos.
   * - ``active_shards``
     - Número de shards activos.
   * - ``active_shards_percent``
     - Porcentaje de shards activos (%).
   * - ``relocating_shards``
     - Número de shards en reubicación.
   * - ``initializing_shards``
     - Número de shards en inicialización.
   * - ``unassigned_shards``
     - Número de shards sin asignar.
   * - ``delayed_unassigned_shards``
     - Número de shards sin asignar con retraso.
   * - ``number_of_pending_tasks``
     - Número de tareas pendientes.
   * - ``number_of_in_flight_fetch``
     - Número de operaciones de recuperación en curso.
   * - ``status``
     - Estado de salud del cluster (``green`` / ``yellow`` / ``red``).
   * - ``exception``
     - Mensaje de error que se incluye solo cuando ocurre un error, como cuando no se puede alcanzar el cluster. En este caso, ``status`` se vuelve ``red``.

``fs``: Estadísticas del Sistema de Archivos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Arreglo de estadísticas para cada raíz (las raíces obtenidas de ``File.listRoots()``).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Campo
     - Descripción
   * - ``path``
     - Ruta absoluta de la raíz.
   * - ``total``
     - Capacidad total (bytes).
   * - ``free``
     - Capacidad libre (bytes).
   * - ``usable``
     - Capacidad utilizable (bytes).
   * - ``used``
     - Capacidad utilizada (bytes). Es ``total`` menos ``usable``.
   * - ``percent``
     - Porcentaje de uso (%).

Ejemplos de Uso
===============

Obtener Información Estadística del Sistema
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verificar el Uso del Heap de la JVM
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Verificar el Estado del Cluster del Motor de Búsqueda
------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-systeminfo` - API de información del sistema
- :doc:`api-admin-searchlist` - API de búsqueda y gestión de documentos
