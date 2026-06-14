==========================
API de SystemInfo
==========================

Vision General
==============

La API de SystemInfo es para obtener informacion del sistema de |Fess|.
Permite verificar las variables de entorno, las propiedades del sistema de Java, las propiedades de configuracion de |Fess| y la informacion para reportes de errores.

URL Base
========

::

    /api/admin/systeminfo

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
     - Obtener informacion del sistema

Obtener Informacion del Sistema
===============================

Solicitud
---------

::

    GET /api/admin/systeminfo

Respuesta
---------

La respuesta incluye ``version``, que indica la version del producto, ``status``, que indica el resultado del procesamiento, y los siguientes cuatro grupos de propiedades. Cada grupo de propiedades es un arreglo de objetos que tienen ``key`` y ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

Campos de Respuesta
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``envProps``
     - Lista de variables de entorno (arreglo de ``key`` / ``value``)
   * - ``systemProps``
     - Lista de propiedades del sistema de Java (arreglo de ``key`` / ``value``)
   * - ``fessProps``
     - Lista de propiedades de configuracion de |Fess| (arreglo de ``key`` / ``value``)
   * - ``bugReportProps``
     - Lista de informacion recopilada para reportes de errores (arreglo de ``key`` / ``value``)

Ejemplos de Uso
===============

Obtener Informacion del Sistema
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraer una Propiedad del Sistema Especifica
--------------------------------------------

.. code-block:: bash

    # Extraer solo el valor de java.version
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

Mostrar la Lista de Variables de Entorno
----------------------------------------

.. code-block:: bash

    # Mostrar las variables de entorno en formato key=value
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-stats` - API de estadisticas
- :doc:`api-admin-general` - API de configuracion general
- :doc:`../../admin/systeminfo-guide` - Guia de informacion del sistema
