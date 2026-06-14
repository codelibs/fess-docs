==========================
API de WebConfig
==========================

Vision General
==============

La API de WebConfig es para gestionar la configuracion de rastreo web de |Fess|.
Puede operar configuraciones como URLs de rastreo, profundidad de rastreo y patrones de exclusion.

URL Base
========

::

    /api/admin/webconfig

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /settings
     - Obtener lista de configuraciones de rastreo web
   * - GET
     - /setting/{id}
     - Obtener configuracion de rastreo web
   * - POST
     - /setting
     - Crear configuracion de rastreo web
   * - PUT
     - /setting
     - Actualizar configuracion de rastreo web
   * - DELETE
     - /setting/{id}
     - Eliminar configuracion de rastreo web

Obtener Lista de Configuraciones de Rastreo Web
===============================================

Solicitud
---------

::

    GET /api/admin/webconfig/settings

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "Sitio de ejemplo",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtener Configuracion de Rastreo Web
====================================

Solicitud
---------

::

    GET /api/admin/webconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "Sitio de ejemplo",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "labelTypeIds": []
        }
      }
    }

Crear Configuracion de Rastreo Web
==================================

Solicitud
---------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user",
      "labelTypeIds": ["label_id_1"]
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre de la configuracion
   * - ``description``
     - No
     - Descripcion de la configuracion
   * - ``urls``
     - Si
     - URL de inicio de rastreo (separadas por salto de linea si son multiples)
   * - ``includedUrls``
     - No
     - Patron de expresion regular para URLs a rastrear
   * - ``excludedUrls``
     - No
     - Patron de expresion regular para URLs a excluir del rastreo
   * - ``includedDocUrls``
     - No
     - Patron de expresion regular para URLs a indexar
   * - ``excludedDocUrls``
     - No
     - Patron de expresion regular para URLs a excluir del indice
   * - ``configParameter``
     - No
     - Parametros de configuracion adicionales
   * - ``depth``
     - No
     - Profundidad de rastreo
   * - ``maxAccessCount``
     - No
     - Numero maximo de accesos
   * - ``userAgent``
     - Si
     - Cadena User-Agent
   * - ``numOfThread``
     - Si
     - Numero de hilos paralelos
   * - ``intervalTime``
     - Si
     - Intervalo entre solicitudes (milisegundos)
   * - ``boost``
     - Si
     - Valor de impulso en resultados de busqueda
   * - ``available``
     - Si
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Si
     - Orden de visualizacion
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de linea si son varios)
   * - ``virtualHosts``
     - No
     - Hosts virtuales (separados por saltos de linea si son varios)
   * - ``labelTypeIds``
     - No
     - IDs de tipo de etiqueta (arreglo)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

Actualizar Configuracion de Rastreo Web
=======================================

Solicitud
---------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_webconfig_id",
        "created": false
      }
    }

Eliminar Configuracion de Rastreo Web
=====================================

Solicitud
---------

::

    DELETE /api/admin/webconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Ejemplos de Patrones de URL
===========================

includedUrls / excludedUrls
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Patron
     - Descripcion
   * - ``.*example\\.com.*``
     - Todas las URLs que contienen example.com
   * - ``https://example\\.com/docs/.*``
     - Solo bajo /docs/
   * - ``.*\\.(pdf|doc|docx)$``
     - Archivos PDF, DOC, DOCX
   * - ``.*\\?.*``
     - URLs con parametros de consulta
   * - ``.*/(login|logout|admin)/.*``
     - URLs que contienen rutas especificas

Ejemplos de Uso
===============

Configuracion de Rastreo de Sitio Corporativo
---------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Configuracion de Rastreo de Sitio de Documentacion
--------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0,
           "labelTypeIds": ["documentation_label_id"]
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-fileconfig` - API de configuracion de rastreo de archivos
- :doc:`api-admin-dataconfig` - API de configuracion de almacen de datos
- :doc:`../../admin/webconfig-guide` - Guia de configuracion de rastreo web
