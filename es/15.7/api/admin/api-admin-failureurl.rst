==========================
API de FailureUrl
==========================

Visión General
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

   * - Método
     - Ruta
     - Descripción
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
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``url``
     - String
     - No
     - Filtro por URL (se admiten comodines ``*`` ``?``)
   * - ``errorCountMin``
     - Integer
     - No
     - Límite inferior del número de errores (mayor o igual al valor especificado)
   * - ``errorCountMax``
     - Integer
     - No
     - Límite superior del número de errores (menor o igual al valor especificado)
   * - ``errorName``
     - String
     - No
     - Filtro por nombre de error (coincidencia con comodin sobre el nombre de clase completamente calificado almacenado; se admiten ``*`` ``?``)

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
            "errorName": "java.net.ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": "3",
            "lastAccessTime": "1738144800000",
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "org.codelibs.fess.exception.ContentNotFoundException",
            "errorLog": "Not found: https://example.com/not-found",
            "errorCount": "1",
            "lastAccessTime": "1738143000000",
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
     - Descripción
   * - ``id``
     - ID de URL fallida
   * - ``url``
     - URL que fallo
   * - ``threadName``
     - Nombre del hilo
   * - ``errorName``
     - Nombre del error (nombre de clase completamente calificado de la excepción ocurrida; por ejemplo, ``java.net.ConnectException``)
   * - ``errorLog``
     - Registro de error (mensaje de la excepción o traza de pila)
   * - ``errorCount``
     - Número de ocurrencias del error (valor numérico representado como cadena)
   * - ``lastAccessTime``
     - Hora del último acceso (milisegundos epoch representados como cadena)
   * - ``configId``
     - ID de configuración de rastreo

.. note::

   Todos los campos de respuesta se devuelven como cadenas (JSON string). ``errorCount`` es un valor numérico representado como cadena y ``lastAccessTime`` son milisegundos epoch representados como cadena.

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
          "errorName": "java.net.ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": "3",
          "lastAccessTime": "1738144800000",
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

Elimina todas las URLs fallidas. No tiene parámetros.

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

``errorName`` almacena el nombre de clase completamente calificado de la excepción ocurrida durante el rastreo, tal como fue capturado. No es una enumeración fija; puede aparecer cualquier nombre de clase dependiendo de la excepción que se haya producido. A continuación se muestran ejemplos representativos.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Nombre de Error (ejemplo)
     - Descripción
   * - ``java.net.ConnectException``
     - Conexión rechazada (no se puede conectar al servidor)
   * - ``java.net.UnknownHostException``
     - No se pudo resolver el nombre de host (error de DNS)
   * - ``java.net.SocketTimeoutException``
     - Tiempo de espera de conexión o lectura agotado
   * - ``javax.net.ssl.SSLException``
     - Error en el protocolo de enlace SSL/TLS o en el certificado
   * - ``java.io.IOException``
     - Error de entrada/salida
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - URL que devolvió un código de estado HTTP configurado en ``crawler.failure.url.status.codes`` (predeterminado: 403, 404, 410)
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - El contenido superó la longitud máxima

Ejemplos de Uso
===============

Obtener Lista de URLs Fallidas
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Número de Errores
-----------------------------

.. code-block:: bash

    # Obtener solo URLs con 3 o mas errores
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrar por Nombre de Error
---------------------------

.. code-block:: bash

    # errorName almacena el nombre de clase completamente calificado, por lo que debe especificarse con un comodin
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=*ConnectException" \
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

Agregación por Tipo de Error
----------------------------

.. code-block:: bash

    # Contar por tipo de error
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-crawlinginfo` - API de información de rastreo
- :doc:`api-admin-joblog` - API de registro de trabajos
- :doc:`../../admin/failureurl-guide` - Guía de gestión de URLs fallidas
