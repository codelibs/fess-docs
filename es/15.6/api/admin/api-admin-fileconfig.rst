==========================
API de FileConfig
==========================

Vision General
==============

La API de FileConfig es para gestionar la configuracion de rastreo de archivos de |Fess|.
Puede operar configuraciones de rastreo para sistemas de archivos y carpetas compartidas SMB/CIFS.

URL Base
========

::

    /api/admin/fileconfig

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
     - Obtener lista de configuraciones de rastreo de archivos
   * - GET
     - /setting/{id}
     - Obtener configuracion de rastreo de archivos
   * - POST
     - /setting
     - Crear configuracion de rastreo de archivos
   * - PUT
     - /setting
     - Actualizar configuracion de rastreo de archivos
   * - DELETE
     - /setting/{id}
     - Eliminar configuracion de rastreo de archivos

Obtener Lista de Configuraciones de Rastreo de Archivos
=======================================================

Solicitud
---------

::

    GET /api/admin/fileconfig/settings
    PUT /api/admin/fileconfig/settings

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
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "paths": "file://///server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtener Configuracion de Rastreo de Archivos
============================================

Solicitud
---------

::

    GET /api/admin/fileconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "paths": "file://///server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

Crear Configuracion de Rastreo de Archivos
==========================================

Solicitud
---------

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 2,
      "intervalTime": 500,
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
   * - ``paths``
     - Si
     - Ruta de inicio de rastreo (separadas por salto de linea si son multiples)
   * - ``includedPaths``
     - No
     - Patron de expresion regular para rutas a rastrear
   * - ``excludedPaths``
     - No
     - Patron de expresion regular para rutas a excluir del rastreo
   * - ``includedDocPaths``
     - No
     - Patron de expresion regular para rutas a indexar
   * - ``excludedDocPaths``
     - No
     - Patron de expresion regular para rutas a excluir del indice
   * - ``configParameter``
     - No
     - Parametros de configuracion adicionales
   * - ``depth``
     - No
     - Profundidad de rastreo (predeterminado: -1=ilimitado)
   * - ``maxAccessCount``
     - No
     - Numero maximo de accesos (predeterminado: 100)
   * - ``numOfThread``
     - No
     - Numero de hilos paralelos (predeterminado: 1)
   * - ``intervalTime``
     - No
     - Intervalo de acceso (milisegundos, predeterminado: 0)
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
        "id": "new_fileconfig_id",
        "created": true
      }
    }

Actualizar Configuracion de Rastreo de Archivos
===============================================

Solicitud
---------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": true,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

Eliminar Configuracion de Rastreo de Archivos
=============================================

Solicitud
---------

::

    DELETE /api/admin/fileconfig/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_fileconfig_id",
        "created": false
      }
    }

Formato de Rutas
================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Protocolo
     - Formato de Ruta
   * - Archivo local
     - ``file:///path/to/directory``
   * - Recurso compartido de Windows (SMB)
     - ``file://///server/share/path``
   * - SMB con autenticacion
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

Ejemplos de Uso
===============

Configuracion de Rastreo de Recurso Compartido SMB
--------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "available": true,
           "permissions": ["guest"]
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-webconfig` - API de configuracion de rastreo web
- :doc:`api-admin-dataconfig` - API de configuracion de almacen de datos
- :doc:`../../admin/fileconfig-guide` - Guia de configuracion de rastreo de archivos
