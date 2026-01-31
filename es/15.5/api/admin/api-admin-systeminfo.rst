==========================
API de SystemInfo
==========================

Vision General
==============

La API de SystemInfo es para obtener informacion del sistema de |Fess|.
Puede verificar informacion de version, variables de entorno, informacion de JVM, etc.

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

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "fessVersion": "15.5.0",
          "opensearchVersion": "2.11.0",
          "javaVersion": "21.0.1",
          "serverName": "Apache Tomcat/10.1.15",
          "osName": "Linux",
          "osVersion": "5.15.0-89-generic",
          "osArchitecture": "amd64",
          "jvmTotalMemory": "2147483648",
          "jvmFreeMemory": "1073741824",
          "jvmMaxMemory": "4294967296",
          "processorCount": "8",
          "fileEncoding": "UTF-8",
          "userLanguage": "ja",
          "userTimezone": "Asia/Tokyo"
        },
        "environmentInfo": {
          "JAVA_HOME": "/usr/lib/jvm/java-21",
          "FESS_DICTIONARY_PATH": "/var/lib/fess/dict",
          "FESS_LOG_PATH": "/var/log/fess"
        },
        "systemProperties": {
          "java.version": "21.0.1",
          "java.vendor": "Oracle Corporation",
          "os.name": "Linux",
          "os.version": "5.15.0-89-generic",
          "user.dir": "/opt/fess",
          "user.home": "/home/fess",
          "user.name": "fess"
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
   * - ``fessVersion``
     - Version de Fess
   * - ``opensearchVersion``
     - Version de OpenSearch
   * - ``javaVersion``
     - Version de Java
   * - ``serverName``
     - Nombre del servidor de aplicaciones
   * - ``osName``
     - Nombre del SO
   * - ``osVersion``
     - Version del SO
   * - ``osArchitecture``
     - Arquitectura del SO
   * - ``jvmTotalMemory``
     - Memoria total de JVM (bytes)
   * - ``jvmFreeMemory``
     - Memoria libre de JVM (bytes)
   * - ``jvmMaxMemory``
     - Memoria maxima de JVM (bytes)
   * - ``processorCount``
     - Numero de procesadores
   * - ``fileEncoding``
     - Codificacion de archivos
   * - ``userLanguage``
     - Idioma del usuario
   * - ``userTimezone``
     - Zona horaria del usuario

Ejemplos de Uso
===============

Obtener Informacion del Sistema
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verificar Version
-----------------

.. code-block:: bash

    # Extraer solo la version de Fess
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo.fessVersion'

Verificar Uso de Memoria
------------------------

.. code-block:: bash

    # Extraer informacion de memoria JVM
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo | {total: .jvmTotalMemory, free: .jvmFreeMemory, max: .jvmMaxMemory}'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-stats` - API de estadisticas
- :doc:`api-admin-general` - API de configuracion general
- :doc:`../../admin/systeminfo-guide` - Guia de informacion del sistema
