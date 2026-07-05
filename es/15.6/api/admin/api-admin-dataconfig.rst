==========================
API de DataConfig
==========================

Vision General
==============

La API de DataConfig es para gestionar la configuracion de almacen de datos de |Fess|.
Puede operar configuraciones de rastreo para fuentes de datos como bases de datos, CSV y JSON.

URL Base
========

::

    /api/admin/dataconfig

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET/PUT
     - /settings
     - Obtener lista de configuraciones de almacen de datos
   * - GET
     - /setting/{id}
     - Obtener configuracion de almacen de datos
   * - POST
     - /setting
     - Crear configuracion de almacen de datos
   * - PUT
     - /setting
     - Actualizar configuracion de almacen de datos
   * - DELETE
     - /setting/{id}
     - Eliminar configuracion de almacen de datos

Obtener Lista de Configuraciones de Almacen de Datos
====================================================

Solicitud
---------

::

    GET /api/admin/dataconfig/settings
    PUT /api/admin/dataconfig/settings

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

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtener Configuracion de Almacen de Datos
=========================================

Solicitud
---------

::

    GET /api/admin/dataconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

Crear Configuracion de Almacen de Datos
=======================================

Solicitud
---------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre de la configuracion
   * - ``handlerName``
     - Si
     - Nombre del manejador de almacen de datos
   * - ``handlerParameter``
     - No
     - Parametros del manejador (informacion de conexion, etc.)
   * - ``handlerScript``
     - Si
     - Script de transformacion de datos
   * - ``boost``
     - No
     - Valor de impulso en resultados de busqueda (predeterminado: 1.0)
   * - ``available``
     - No
     - Habilitado/Deshabilitado (predeterminado: true)
   * - ``sortOrder``
     - No
     - Orden de visualizacion
   * - ``permissions``
     - No
     - Roles con permiso de acceso
   * - ``virtualHosts``
     - No
     - Hosts virtuales
   * - ``labelTypeIds``
     - No
     - IDs de tipo de etiqueta

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

Actualizar Configuracion de Almacen de Datos
============================================

Solicitud
---------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
      "available": true,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

Eliminar Configuracion de Almacen de Datos
==========================================

Solicitud
---------

::

    DELETE /api/admin/dataconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_dataconfig_id",
        "created": false
      }
    }

Tipos de Manejador
==================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nombre del Manejador
     - Descripcion
   * - ``DatabaseDataStore``
     - Conecta a base de datos via JDBC
   * - ``CsvDataStore``
     - Lee datos de archivos CSV
   * - ``JsonDataStore``
     - Lee datos de archivos JSON o API JSON

Ejemplos de Uso
===============

Configuracion de Rastreo de Base de Datos
-----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": true
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-webconfig` - API de configuracion de rastreo web
- :doc:`api-admin-fileconfig` - API de configuracion de rastreo de archivos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de almacen de datos
