==========================
API de Log
==========================

Visión General
==============

La API de Log es para consultar y descargar los archivos de registro de |Fess|.
Puede obtener la lista de los archivos de registro generados en el servidor y descargar archivos de registro individuales.

URL Base
========

::

    /api/admin/log

Autenticación
=============

Al igual que con el resto de Admin APIs, se requiere autenticación mediante token de acceso. El token de acceso debe tener el permiso ``Radmin-api`` (configurado en ``api.admin.access.permissions``; el valor predeterminado es ``Radmin-api``).
El token de acceso se especifica en el encabezado de la solicitud.

::

    Authorization: Bearer <token de acceso>

Para más detalles sobre la autenticación y cómo obtener el token de acceso, consulte :doc:`api-admin-overview`.

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
     - /files
     - Obtener lista de archivos de registro
   * - GET
     - /file/{id}
     - Descargar archivo de registro

Obtener Lista de Archivos de Registro
=====================================

Devuelve la lista de los archivos de registro (``.log`` y ``.log.gz``) presentes en el directorio de salida de registros del servidor.
Los archivos se devuelven ordenados de forma ascendente por nombre de archivo.

Solicitud
---------

::

    GET /api/admin/log/files

Respuesta
---------

En ``files`` se almacena un arreglo de objetos que representan la información de cada archivo de registro, y en ``total`` el número de elementos.
Cada objeto tiene los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripción
   * - ``id``
     - Valor del nombre de archivo codificado en Base64 URL (se usa como ``{id}`` al descargar)
   * - ``name``
     - Nombre del archivo de registro
   * - ``lastModified``
     - Fecha/hora de la última modificación

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

.. note::

   En ``version`` se establece la versión del producto de |Fess| en ejecución. El contenido y la cantidad de elementos en ``files`` dependen de los archivos de registro presentes en el servidor, por lo que el ejemplo anterior es solo una muestra.

Descargar Archivo de Registro
=============================

Descarga el contenido del archivo de registro especificado.
En ``{id}`` se especifica el ``id`` devuelto en la lista (el valor del nombre de archivo codificado en Base64 URL) tal cual.
La respuesta se devuelve como un flujo ``application/octet-stream``.
Por razones de seguridad, solo se aceptan nombres que terminen en ``.log`` o ``.log.gz``; los nombres que contienen operaciones de ruta como ``..`` no son aceptados.
Si se especifica un nombre de archivo inexistente o un nombre no permitido como archivo de registro, se devuelve una respuesta vacía.

Solicitud
---------

::

    GET /api/admin/log/file/{id}

Respuesta
---------

Flujo binario del archivo de registro (``Content-Type: application/octet-stream``).

Ejemplos de Uso
===============

Obtener Lista de Archivos de Registro
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Descargar Archivo de Registro
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-backup` - API de respaldo
