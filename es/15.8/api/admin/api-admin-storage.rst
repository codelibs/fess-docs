===========
Storage API
===========

Visión General
==============

Storage API es una API para gestionar el almacenamiento de objetos de |Fess|.
Permite obtener el listado de archivos y directorios en el almacenamiento, así como descargar, eliminar y subir archivos.

URL Base
========

::

    /api/admin/storage

Autenticación
=============

Todos los endpoints de Admin API, incluida Storage API, requieren autenticación mediante un token de acceso.
Especifique el token de acceso en el encabezado ``Authorization`` de la solicitud.

::

    Authorization: Bearer <token de acceso>

Para obtener información sobre cómo obtener el token de acceso y los permisos necesarios (de forma predeterminada, el rol ``admin-api``),
consulte :doc:`api-admin-overview`.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /list/{id}
     - Obtener listado de archivos y directorios
   * - GET
     - /download/{id}
     - Descargar un archivo
   * - DELETE
     - /delete/{id}
     - Eliminar un archivo
   * - PUT
     - /upload
     - Subir un archivo

Obtener Listado de Archivos y Directorios
=========================================

Devuelve el listado de archivos y directorios ubicados bajo el directorio especificado.
En ``{id}`` especifique el ``id`` del directorio obtenido en el listado. Si se omite ``{id}``, se obtiene el listado del directorio raíz.

Solicitud
---------

::

    GET /api/admin/storage/list/{id}

Respuesta
---------

En ``items`` se almacena un array de objetos que representan la información de archivos y directorios (primero los directorios, luego los archivos).
Cada objeto tiene los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``id``
     - Identificador codificado. Cadena que representa la ruta del objeto codificada en Base64 seguro para URL, utilizada como ``{id}`` al descargar o eliminar.
   * - ``path``
     - Ruta del directorio padre
   * - ``name``
     - Nombre del archivo o directorio
   * - ``hashCode``
     - Valor de hash utilizado en el procesamiento interno (no es un valor estable que represente el contenido del objeto)
   * - ``size``
     - Tamaño (en bytes)
   * - ``directory``
     - Indica si es un directorio (boolean)
   * - ``lastModified``
     - Fecha y hora de la última modificación (formato ISO 8601; incluido solo para archivos)

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

Descargar un Archivo
====================

Descarga un archivo del almacenamiento. En ``{id}`` especifique el ``id`` obtenido en el listado.
La respuesta se devuelve como un flujo de datos de tipo ``application/octet-stream``.

Solicitud
---------

::

    GET /api/admin/storage/download/{id}

Respuesta
---------

Flujo binario del archivo (``Content-Type: application/octet-stream``).

.. note::

   La respuesta de esta API no incluye el encabezado ``Content-Disposition``.
   El nombre del archivo con el que se guarda debe especificarse en el lado del cliente (en cURL, utilice la opción ``-o``).

Eliminar un Archivo
===================

Elimina un archivo del almacenamiento. En ``{id}`` especifique el ``id`` obtenido en el listado.

Solicitud
---------

::

    DELETE /api/admin/storage/delete/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Subir un Archivo
================

Sube un archivo al almacenamiento. El envío se realiza en formato ``multipart/form-data``.
El directorio de destino se especifica mediante el campo de formulario ``path``, no como parte de la ruta URL.

Solicitud
---------

::

    PUT /api/admin/storage/upload
    Content-Type: multipart/form-data

Descripción de los Campos
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripción
   * - ``path``
     - No
     - Ruta del directorio de destino (sin barras al inicio ni al final). Si se omite, el archivo se guarda en el raíz (directamente bajo el bucket).
   * - ``file``
     - Sí
     - Archivo a subir

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Errores
=======

Cada endpoint devuelve una respuesta con ``status`` distinto de 0 (``1`` en caso de error de validación) cuando el procesamiento falla.
El campo ``message`` del cuerpo de la respuesta contiene el detalle del error. Para obtener información sobre los valores de status y los códigos de estado HTTP, consulte :doc:`api-admin-overview`.

Los principales casos de error son los siguientes.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Principales casos en que se produce un error
   * - Obtener listado de archivos y directorios
     - Cuando el número de elementos supera el límite
   * - Descargar un archivo
     - Cuando el ``id`` es inválido o la descarga falla
   * - Eliminar un archivo
     - Cuando el ``id`` es inválido o la eliminación falla
   * - Subir un archivo
     - Cuando no se especifica ``file`` o la subida falla

Ejemplos de Uso
===============

Obtener Listado del Directorio Raíz
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Descargar un Archivo
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Eliminar un Archivo
-------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Subir un Archivo
----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
