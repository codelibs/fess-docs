==========================
API de FailureUrl
==========================

Vision General
==============

La API de FailureUrl es para gestionar URLs de rastreo fallidas de |Fess|.
Puede verificar y eliminar URLs que tuvieron errores durante el rastreo.

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
     - /
     - Obtener lista de URLs fallidas
   * - DELETE
     - /{id}
     - Eliminar URL fallida
   * - DELETE
     - /delete-all
     - Eliminar todas las URLs fallidas

Obtener Lista de URLs Fallidas
==============================

Solicitud
---------

::

    GET /api/admin/failureurl

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
     - Numero de pagina (comienza en 0)
   * - ``errorCountMin``
     - Integer
     - No
     - Filtro de numero minimo de errores
   * - ``configId``
     - String
     - No
     - Filtro de ID de configuracion

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
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
   * - ``configId``
     - ID de configuracion de rastreo
   * - ``errorName``
     - Nombre del error
   * - ``errorLog``
     - Registro de error
   * - ``errorCount``
     - Numero de veces que ocurrio el error
   * - ``lastAccessTime``
     - Hora del ultimo acceso
   * - ``threadName``
     - Nombre del hilo

Eliminar URL Fallida
====================

Solicitud
---------

::

    DELETE /api/admin/failureurl/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

Eliminar Todas las URLs Fallidas
================================

Solicitud
---------

::

    DELETE /api/admin/failureurl/delete-all

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``configId``
     - String
     - No
     - Eliminar solo URLs fallidas de ID de configuracion especifico
   * - ``errorCountMin``
     - Integer
     - No
     - Eliminar solo errores con numero de veces especificado o mas

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
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

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Numero de Errores
-----------------------------

.. code-block:: bash

    # Obtener solo URLs con 3 o mas errores
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtener URLs Fallidas de Configuracion Especifica
-------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar URL Fallida
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eliminar Todas las URLs Fallidas
--------------------------------

.. code-block:: bash

    # Eliminar todas las URLs fallidas
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Eliminar solo URLs fallidas de configuracion especifica
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Eliminar solo URLs con 3 o mas errores
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Agregacion por Tipo de Error
----------------------------

.. code-block:: bash

    # Contar por tipo de error
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-crawlinginfo` - API de informacion de rastreo
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/failureurl-guide` - Guia de gestion de URLs fallidas
