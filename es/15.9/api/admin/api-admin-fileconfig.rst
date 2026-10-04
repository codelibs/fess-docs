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
            "included_paths": ".*\\.pdf$",
            "excluded_paths": ".*/(temp|cache)/.*",
            "included_doc_paths": "",
            "excluded_doc_paths": "",
            "config_parameter": "",
            "depth": 10,
            "max_access_count": 1000,
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
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
          "included_paths": ".*\\.pdf$",
          "excluded_paths": ".*/(temp|cache)/.*",
          "included_doc_paths": "",
          "excluded_doc_paths": "",
          "config_parameter": "",
          "depth": 10,
          "max_access_count": 1000,
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   La respuesta incluye los campos de auditoría ``created_by``, ``created_time``,
   ``updated_by``, ``updated_time`` y ``version_no``, que son asignados automáticamente
   en el momento del registro o la actualización.
   ``version_no`` es obligatorio al actualizar (consulte la sección "Actualizar configuración de rastreo de archivos" a continuación).

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
      "included_paths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excluded_paths": ".*/(temp|backup)/.*",
      "num_of_thread": 2,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
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
     - Ruta de inicio de rastreo (separadas por salto de línea si son múltiples). Se especifica con uno de los protocolos: ``file:``, ``smb:``, ``smb1:``, ``ftp:``, ``s3:`` o ``gcs:``
   * - ``included_paths``
     - No
     - Patrón de expresión regular para rutas a rastrear
   * - ``excluded_paths``
     - No
     - Patrón de expresión regular para rutas a excluir del rastreo
   * - ``included_doc_paths``
     - No
     - Patrón de expresión regular para rutas a indexar
   * - ``excluded_doc_paths``
     - No
     - Patrón de expresión regular para rutas a excluir del índice
   * - ``config_parameter``
     - No
     - Parámetros de configuración adicionales (formato ``key=value``, un elemento por línea)
   * - ``depth``
     - No
     - Profundidad de rastreo (0 o más)
   * - ``max_access_count``
     - No
     - Número máximo de accesos (0 o más)
   * - ``num_of_thread``
     - Sí
     - Número de hilos paralelos (1 o más)
   * - ``interval_time``
     - Sí
     - Intervalo de acceso (milisegundos, 0 o más)
   * - ``boost``
     - Sí
     - Valor de impulso en resultados de búsqueda
   * - ``available``
     - Sí
     - Habilitado/Deshabilitado (cadena ``"true"`` / ``"false"``)
   * - ``sort_order``
     - Sí
     - Orden de visualización (0 o más)
   * - ``permissions``
     - No
     - Roles con permiso de acceso (separados por saltos de línea si son varios)
   * - ``virtual_hosts``
     - No
     - Hosts virtuales (separados por saltos de línea si son varios)

.. note::

   Los campos de auditoría como ``created_by``, ``created_time``, ``updated_by`` y ``updated_time``
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
el registro a actualizar y ``version_no`` como número de versión.
En ``version_no`` se debe especificar el valor actual incluido en la respuesta de la API de consulta (GET).

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "included_paths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excluded_paths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 3,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
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
   * - ``version_no``
     - Sí
     - Número de versión actual del registro a actualizar. Se especifica el valor de ``version_no`` incluido en la respuesta de la API de consulta (GET)

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
   * - Amazon S3 / Almacenamiento de objetos compatible con S3 (MinIO, etc.)
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
           "included_paths": ".*\\.(pdf|doc|docx)$",
           "excluded_paths": ".*/(temp|backup)/.*",
           "num_of_thread": 2,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
           "included_paths": ".*\\.(pdf|doc|docx)$",
           "excluded_paths": ".*/(temp|private)/.*",
           "max_access_count": 50000,
           "num_of_thread": 3,
           "interval_time": 200,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
