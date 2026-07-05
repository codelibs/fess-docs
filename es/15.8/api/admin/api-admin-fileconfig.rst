==========================
API de FileConfig
==========================

Vision General
==============

La API de FileConfig es para gestionar la configuracion de rastreo de archivos de |Fess|.
Puede operar configuraciones de rastreo para sistemas de archivos locales, carpetas compartidas SMB/CIFS, FTP y diversos almacenes de objetos.

URL Base
========

::

    /api/admin/fileconfig

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
========================================================

Solicitud
---------

::

    GET /api/admin/fileconfig/settings

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
   * - ``paths``
     - String
     - No
     - Filtrar por ruta de rastreo
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
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "Documentos compartidos",
            "paths": "smb://server/share/documents",
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
          "description": "Documentos compartidos",
          "paths": "smb://server/share/documents",
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
   ``versionNo`` es obligatorio al actualizar (consulte la seccion "Actualizar configuracion de rastreo de archivos" a continuacion).

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
      "numOfThread": 2,
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
   * - ``paths``
     - Si
     - Ruta de inicio de rastreo (separadas por salto de linea si son multiples). Se especifica con uno de los protocolos: ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``storage:``, ``s3:`` o ``gcs:``
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
     - Parametros de configuracion adicionales (formato ``key=value``, un elemento por linea)
   * - ``depth``
     - No
     - Profundidad de rastreo (0 o mas)
   * - ``maxAccessCount``
     - No
     - Numero maximo de accesos (0 o mas)
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

Al actualizar, ademas de los campos de creacion, son obligatorios ``id`` para identificar
el registro a actualizar y ``versionNo`` como numero de version.
En ``versionNo`` se debe especificar el valor actual incluido en la respuesta de la API de consulta (GET).

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
        "status": 0
      }
    }

Formato de Rutas
================

En ``paths`` se pueden utilizar los siguientes protocolos (los protocolos disponibles pueden modificarse mediante la configuracion ``crawler.file.protocols``).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Protocolo
     - Formato de Ruta
   * - Archivo local
     - ``file:///path/to/directory``
   * - Recurso compartido SMB/CIFS
     - ``smb://server/share/path``
   * - Recurso compartido SMB/CIFS (SMB1)
     - ``smb1://server/share/path``
   * - FTP
     - ``ftp://server/path``
   * - Almacenamiento de objetos compatible con S3 (MinIO, etc.)
     - ``storage://bucket/path``
   * - Amazon S3
     - ``s3://bucket/path``
   * - Google Cloud Storage
     - ``gcs://bucket/path``

.. note::

   Las credenciales de autenticacion (nombre de usuario y contrasena) para SMB/CIFS y FTP
   no se incluyen en la ruta, sino que se configuran en la seccion "Autenticacion de archivos".
   Consulte :doc:`../../admin/fileauth-guide` para mas informacion.

Ejemplos de Uso
===============

Configuracion de Rastreo de Archivos Locales
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Local Files",
           "paths": "file:///data/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|backup)/.*",
           "numOfThread": 2,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Configuracion de Rastreo de Recurso Compartido SMB
--------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

.. note::

   Si el acceso al recurso compartido SMB requiere autenticacion, registre previamente
   las credenciales del host de destino en la configuracion de "Autenticacion de archivos".

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-webconfig` - API de configuracion de rastreo web
- :doc:`api-admin-dataconfig` - API de configuracion de almacen de datos
- :doc:`../../admin/fileconfig-guide` - Guia de configuracion de rastreo de archivos
- :doc:`../../admin/fileauth-guide` - Guia de configuracion de autenticacion de archivos
