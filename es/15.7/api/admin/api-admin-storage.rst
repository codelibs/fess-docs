==========================
API de Storage
==========================

Vision General
==============

La API de Storage es para gestionar el almacenamiento de objetos de |Fess|.
Puede obtener la lista de archivos y directorios del almacenamiento, y descargar, eliminar y subir archivos.

URL Base
========

::

    /api/admin/storage

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /list/{id}
     - Obtener lista de archivos y directorios
   * - GET
     - /download/{id}
     - Descargar archivo
   * - DELETE
     - /delete/{id}
     - Eliminar archivo
   * - PUT
     - /upload/{pathId}
     - Subir archivo

Obtener Lista de Archivos y Directorios
=======================================

Devuelve la lista de archivos y directorios bajo el directorio especificado.
En ``{id}`` se indica la ruta codificada. Si se omite ``{id}``, se obtiene la lista del directorio raiz.

Solicitud
---------

::

    GET /api/admin/storage/list/{id}

Respuesta
---------

En ``items`` se almacena un arreglo de objetos que representan la informacion de archivos y directorios (primero los directorios y despues los archivos).
Cada objeto tiene los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``id``
     - Identificador codificado (se usa como ``{id}`` al descargar o eliminar)
   * - ``path``
     - Ruta del padre
   * - ``name``
     - Nombre del archivo o del directorio
   * - ``hashCode``
     - Codigo hash
   * - ``size``
     - Tamano (bytes)
   * - ``directory``
     - Si es un directorio (boolean)
   * - ``lastModified``
     - Fecha/hora de la ultima modificacion (solo archivos)

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

Descargar Archivo
=================

Descarga un archivo del almacenamiento. En ``{id}`` se indica el ``id`` obtenido en la lista.
La respuesta se devuelve como un flujo ``application/octet-stream``.

Solicitud
---------

::

    GET /api/admin/storage/download/{id}

Respuesta
---------

Flujo binario del archivo (``Content-Type: application/octet-stream``).

Eliminar Archivo
================

Elimina un archivo del almacenamiento. En ``{id}`` se indica el ``id`` obtenido en la lista.

Solicitud
---------

::

    DELETE /api/admin/storage/delete/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Subir Archivo
=============

Sube un archivo al almacenamiento. Se envia en formato ``multipart/form-data``.

Solicitud
---------

::

    PUT /api/admin/storage/upload/{pathId}
    Content-Type: multipart/form-data

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``path``
     - No
     - Ruta de destino de la subida (si no se especifica, la ubicacion predeterminada)
   * - ``file``
     - Si
     - Archivo a subir

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Ejemplos de Uso
===============

Obtener Lista del Directorio Raiz
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Descargar Archivo
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Eliminar Archivo
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Subir Archivo
-------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
