==========================
API de FileConfig
==========================

Visión General
==============

La API de FileConfig es para gestionar la configuración de rastreo de archivos de |Fess|.
Puede operar configuraciones de rastreo para sistemas de archivos locales, carpetas compartidas SMB/CIFS, FTP y diversos almacenes de objetos.

URL Base
========

::

    /api/admin/fileconfig

.. note::

   Todos los endpoints requieren privilegios de administrador y un token de acceso válido.
   Consulte :doc:`api-admin-overview` para obtener información sobre la autenticación.

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
     - Obtener lista de configuraciones de rastreo de archivos
   * - GET
     - /setting/{id}
     - Obtener configuración de rastreo de archivos
   * - POST
     - /setting
     - Crear configuración de rastreo de archivos
   * - PUT
     - /setting
     - Actualizar configuración de rastreo de archivos
   * - DELETE
     - /setting/{id}
     - Eliminar configuración de rastreo de archivos

Obtener Lista de Configuraciones de Rastreo de Archivos
========================================================

Solicitud
---------

::

    GET /api/admin/fileconfig/settings

.. note::

   El endpoint de lista también acepta ``PUT`` además de ``GET``.

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (predeterminado: 25, según la configuración ``paging.page.size``)
   * - ``name``
     - String
     - No
     - Filtrar por nombre de configuración
   * - ``paths``
     - String
     - No
     - Filtrar por ruta de rastreo
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

``total`` indica el número total de configuraciones que coinciden con los criterios de búsqueda.

Obtener Configuración de Rastreo de Archivos
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

   La respuesta incluye los campos de auditoría ``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime`` y ``versionNo``, que son asignados automáticamente
   en el momento del registro o la actualización.
   ``versionNo`` es obligatorio al actualizar (consulte la sección "Actualizar configuración de rastreo de archivos" a continuación).

Crear Configuración de Rastreo de Archivos
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

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``name``
     - Sí
     - Nombre de la configuración (máximo 200 caracteres)
   * - ``description``
     - No
     - Descripción de la configuración (máximo 1000 caracteres)
   * - ``paths``
     - Sí
     - Ruta de inicio de rastreo (separadas por salto de línea si son múltiples). Se especifica con uno de los protocolos: ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``storage:``, ``s3:`` o ``gcs:``
   * - ``includedPaths``
     - No
     - Patrón de expresión regular para rutas a rastrear
   * - ``excludedPaths``
     - No
     - Patrón de expresión regular para rutas a excluir del rastreo
   * - ``includedDocPaths``
     - No
     - Patrón de expresión regular para rutas a indexar
   * - ``excludedDocPaths``
     - No
     - Patrón de expresión regular para rutas a excluir del índice
   * - ``configParameter``
     - No
     - Parámetros de configuración adicionales (formato ``key=value``, un elemento por línea)
   * - ``depth``
     - No
     - Profundidad de rastreo (0 o más)
   * - ``maxAccessCount``
     - No
     - Número máximo de accesos (0 o más)
   * - ``numOfThread``
     - Sí
     - Número de hilos paralelos (1 o más)
   * - ``intervalTime``
     - Sí
     - Intervalo de acceso (milisegundos, 0 o más)
   * - ``boost``
     - Sí
     - Valor de impulso en resultados de búsqueda
   * - ``available``
     - Sí
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Sí
     - Orden de visualización (0 o más)
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de línea si son varios)
   * - ``virtualHosts``
     - No
     - Hosts virtuales (separados por saltos de línea si son varios)

.. note::

   Los campos de auditoría como ``createdBy``, ``createdTime``, ``updatedBy`` y ``updatedTime``
   son asignados automáticamente por el servidor, por lo que no es necesario incluirlos en el cuerpo de la solicitud.

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

Actualizar Configuración de Rastreo de Archivos
===============================================

Solicitud
---------

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

Al actualizar, además de los campos de creación, son obligatorios ``id`` para identificar
el registro a actualizar y ``versionNo`` como número de versión.
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

Campos Adicionales para la Actualización
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - ID de la configuración a actualizar (máximo 1000 caracteres)
   * - ``versionNo``
     - Sí
     - Número de versión actual del registro a actualizar. Se especifica el valor de ``versionNo`` incluido en la respuesta de la API de consulta (GET)

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

Eliminar Configuración de Rastreo de Archivos
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

En ``paths`` se pueden utilizar los siguientes protocolos (los protocolos disponibles pueden modificarse mediante la configuración ``crawler.file.protocols``).

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

   Las credenciales de autenticación (nombre de usuario y contraseña) para SMB/CIFS y FTP
   no se incluyen en la ruta, sino que se configuran en la sección "Autenticación de archivos".
   Consulte :doc:`../../admin/fileauth-guide` para más información.

Ejemplos de Uso
===============

Configuración de Rastreo de Archivos Locales
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

Configuración de Rastreo de Recurso Compartido SMB
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

   Si el acceso al recurso compartido SMB requiere autenticación, registre previamente
   las credenciales del host de destino en la configuración de "Autenticación de archivos".

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-webconfig` - API de configuración de rastreo web
- :doc:`api-admin-dataconfig` - API de configuración de almacén de datos
- :doc:`../../admin/fileconfig-guide` - Guía de configuración de rastreo de archivos
- :doc:`../../admin/fileauth-guide` - Guía de configuración de autenticación de archivos
