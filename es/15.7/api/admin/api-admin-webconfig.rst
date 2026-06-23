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

.. note::

   Todos los endpoints requieren privilegios de administrador y un token de acceso valido.
   Consulte :doc:`api-admin-overview` para obtener informacion sobre la autenticacion.

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

.. note::

   El endpoint de lista tambien acepta ``PUT`` ademas de ``GET``.

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1, predeterminado: 1)
   * - ``size``
     - Integer
     - No
     - Numero de elementos por pagina (predeterminado: 25, segun la configuracion ``paging.page.size``)
   * - ``name``
     - String
     - No
     - Filtrar por nombre de configuracion
   * - ``urls``
     - String
     - No
     - Filtrar por URL de rastreo
   * - ``description``
     - String
     - No
     - Filtrar por descripcion

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

``total`` indica el numero total de configuraciones que coinciden con los criterios de busqueda.

Obtener Configuracion de Rastreo Web
=====================================

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
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   La respuesta incluye los campos de auditoria ``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime`` y ``versionNo``, que son asignados automaticamente
   en el momento del registro o la actualizacion.
   ``versionNo`` es obligatorio al actualizar (consulte la seccion "Actualizar configuracion de rastreo web" a continuacion).

Crear Configuracion de Rastreo Web
===================================

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
      "permissions": "{role}admin\n{role}user"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre de la configuracion (maximo 200 caracteres)
   * - ``description``
     - No
     - Descripcion de la configuracion (maximo 1000 caracteres)
   * - ``urls``
     - Si
     - URL de inicio de rastreo (separadas por salto de linea si son multiples). Se especifica con ``http:`` o ``https:``
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
     - Parametros de configuracion adicionales (formato ``key=value``, un elemento por linea)
   * - ``depth``
     - No
     - Profundidad de rastreo (0 o mas)
   * - ``maxAccessCount``
     - No
     - Numero maximo de accesos (0 o mas)
   * - ``userAgent``
     - Si
     - Cadena User-Agent (maximo 200 caracteres)
   * - ``numOfThread``
     - Si
     - Numero de hilos paralelos (1 o mas)
   * - ``intervalTime``
     - Si
     - Intervalo de acceso (milisegundos, 0 o mas)
   * - ``boost``
     - Si
     - Valor de impulso en resultados de busqueda
   * - ``available``
     - Si
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Si
     - Orden de visualizacion (0 o mas)
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de linea si son varios)
   * - ``virtualHosts``
     - No
     - Hosts virtuales (separados por saltos de linea si son varios)

.. note::

   Los campos de auditoria como ``createdBy``, ``createdTime``, ``updatedBy`` y ``updatedTime``
   son asignados automaticamente por el servidor, por lo que no es necesario incluirlos en el cuerpo de la solicitud.

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
=========================================

Solicitud
---------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

Al actualizar, ademas de los campos de creacion, son obligatorios ``id`` para identificar
el registro a actualizar y ``versionNo`` como numero de version.
En ``versionNo`` se debe especificar el valor actual incluido en la respuesta de la API de consulta (GET).

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

Campos Adicionales para la Actualizacion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripcion
   * - ``id``
     - Si
     - ID de la configuracion a actualizar (maximo 1000 caracteres)
   * - ``versionNo``
     - Si
     - Numero de version actual del registro a actualizar. Se especifica el valor de ``versionNo`` incluido en la respuesta de la API de consulta (GET)

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
=======================================

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
============================

En ``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` se utilizan expresiones regulares.

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
----------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-fileconfig` - API de configuracion de rastreo de archivos
- :doc:`api-admin-dataconfig` - API de configuracion de almacen de datos
- :doc:`../../admin/webconfig-guide` - Guia de configuracion de rastreo web
