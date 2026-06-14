==========================
API de FailureUrl
==========================

Vision General
==============

La API de FailureUrl es para gestionar las URLs de rastreo fallidas de |Fess|.
Permite operaciones como obtener la lista de URLs que tuvieron errores durante el rastreo, obtenerlas individualmente y eliminarlas.

URL Base
========

::

    /api/admin/failureurl

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
     - Obtener lista de URLs fallidas
   * - GET
     - /log/{id}
     - Obtener URL fallida
   * - DELETE
     - /log/{id}
     - Eliminar URL fallida
   * - DELETE
     - /all
     - Eliminar todas las URLs fallidas

Obtener Lista de URLs Fallidas
==============================

Solicitud
---------

::

    GET /api/admin/failureurl/logs

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
     - Numero de elementos por pagina
   * - ``page``
     - Integer
     - No
     - Numero de pagina
   * - ``url``
     - String
     - No
     - Filtro por URL
   * - ``errorCountMin``
     - Integer
     - No
     - Filtro de numero minimo de errores
   * - ``errorCountMax``
     - Integer
     - No
     - Filtro de numero maximo de errores
   * - ``errorName``
     - String
     - No
     - Filtro por nombre de error

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "threadName": "Crawler-1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": 1738144800000,
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": 1738143000000,
            "configId": "webConfig_id_1"
          }
        ],
        "total": 45
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
     - ID de URL fallida
   * - ``url``
     - URL que fallo
   * - ``threadName``
     - Nombre del hilo
   * - ``errorName``
     - Nombre del error
   * - ``errorLog``
     - Registro de error
   * - ``errorCount``
     - Numero de veces que ocurrio el error
   * - ``lastAccessTime``
     - Hora del ultimo acceso (milisegundos epoch)
   * - ``configId``
     - ID de configuracion de rastreo

Obtener URL Fallida
===================

Solicitud
---------

::

    GET /api/admin/failureurl/log/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "threadName": "Crawler-1",
          "errorName": "ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": 3,
          "lastAccessTime": 1738144800000,
          "configId": "webConfig_id_1"
        }
      }
    }

Eliminar URL Fallida
====================

Solicitud
---------

::

    DELETE /api/admin/failureurl/log/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Eliminar Todas las URLs Fallidas
================================

Elimina todas las URLs fallidas. No tiene parametros.

Solicitud
---------

::

    DELETE /api/admin/failureurl/all

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Tipos de Error
==============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nombre de Error
     - Descripcion
   * - ``ConnectException``
     - Error de conexion
   * - ``HttpStatusException``
     - Error de estado HTTP (404, 500, etc.)
   * - ``SocketTimeoutException``
     - Error de tiempo de espera agotado
   * - ``UnknownHostException``
     - Error de resolucion de nombre de host
   * - ``SSLException``
     - Error de certificado SSL
   * - ``IOException``
     - Error de entrada/salida

Ejemplos de Uso
===============

Obtener Lista de URLs Fallidas
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Numero de Errores
-----------------------------

.. code-block:: bash

    # Obtener solo URLs con 3 o mas errores
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Nombre de Error
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener URL Fallida
-------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar URL Fallida
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Todas las URLs Fallidas
--------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Agregacion por Tipo de Error
----------------------------

.. code-block:: bash

    # Contar por tipo de error
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-crawlinginfo` - API de informacion de rastreo
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/failureurl-guide` - Guia de gestion de URLs fallidas
