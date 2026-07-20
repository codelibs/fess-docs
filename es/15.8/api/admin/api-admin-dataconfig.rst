==========================
API de DataConfig
==========================

Visión General
==============

La API de DataConfig es para gestionar la configuración de almacén de datos de |Fess|.
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

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /settings
     - Obtener lista de configuraciones de almacén de datos
   * - GET
     - /setting/{id}
     - Obtener configuración de almacén de datos
   * - POST
     - /setting
     - Crear configuración de almacén de datos
   * - PUT
     - /setting
     - Actualizar configuración de almacén de datos
   * - DELETE
     - /setting/{id}
     - Eliminar configuración de almacén de datos

Obtener Lista de Configuraciones de Almacén de Datos
====================================================

Solicitud
---------

::

    GET /api/admin/dataconfig/settings

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
     - Número de elementos por página (predeterminado: 25)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``name``
     - String
     - No
     - Filtrar por nombre de configuración
   * - ``handlerName``
     - String
     - No
     - Filtrar por nombre de manejador
   * - ``description``
     - String
     - No
     - Filtrar por descripción

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
            "description": "Rastreador de base de datos",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
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

Obtener Configuración de Almacén de Datos
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
          "description": "Rastreador de base de datos",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
        }
      }
    }

Crear Configuración de Almacén de Datos
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
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``name``
     - Sí
     - Nombre de la configuración
   * - ``description``
     - No
     - Descripción de la configuración
   * - ``handlerName``
     - Sí
     - Nombre del manejador de almacén de datos
   * - ``handlerParameter``
     - No
     - Parámetros del manejador (información de conexión, etc.)
   * - ``handlerScript``
     - No
     - Script de transformación de datos
   * - ``boost``
     - Sí
     - Valor de impulso en resultados de búsqueda
   * - ``available``
     - Sí
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Sí
     - Orden de visualización
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de línea si son varios)
   * - ``virtualHosts``
     - No
     - Hosts virtuales (separados por saltos de línea si son varios)

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

Actualizar Configuración de Almacén de Datos
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
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Las solicitudes de actualización requieren los mismos campos obligatorios que la creación (``name``, ``handlerName``, ``boost``, ``available``, ``sortOrder``), además de los siguientes campos:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - ID de la configuración a actualizar
   * - ``versionNo``
     - Sí
     - Número de versión para el bloqueo optimista (especifique el valor obtenido al recuperar la configuración)

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

Eliminar Configuración de Almacén de Datos
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
        "status": 0
      }
    }

Tipos de Manejador
==================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nombre del Manejador
     - Descripción
   * - ``DatabaseDataStore``
     - Conecta a base de datos vía JDBC
   * - ``CsvDataStore``
     - Lee datos de un archivo CSV (procesa cada fila como un documento)
   * - ``CsvListDataStore``
     - Lee archivos CSV y elimina automáticamente los archivos procesados (una extensión de ``CsvDataStore`` con filtrado basado en marcas de tiempo)
   * - ``JsonDataStore``
     - Lee datos de archivos JSON o API JSON

.. note::

   Los tipos de manejador disponibles dependen de los plugins de almacén de datos instalados.
   Los manejadores indicados arriba se incluyen de forma predeterminada. Al instalar plugins de
   almacén de datos como SharePoint, Slack o Salesforce, los nombres de manejador correspondientes
   quedan disponibles.

Ejemplos de Uso
===============

Configuración de Rastreo de Base de Datos
-----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-webconfig` - API de configuración de rastreo web
- :doc:`api-admin-fileconfig` - API de configuración de rastreo de archivos
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de almacén de datos
