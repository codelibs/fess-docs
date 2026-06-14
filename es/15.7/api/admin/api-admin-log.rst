==========================
API de Log
==========================

Vision General
==============

La API de Log es para consultar y descargar los archivos de registro de |Fess|.
Puede obtener la lista de los archivos de registro generados en el servidor y descargar archivos de registro individuales.

URL Base
========

::

    /api/admin/log

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET
     - /files
     - Obtener lista de archivos de registro
   * - GET
     - /file/{id}
     - Descargar archivo de registro

Obtener Lista de Archivos de Registro
=====================================

Devuelve la lista de los archivos de registro (``.log`` y ``.log.gz``) presentes en el directorio de salida de registros del servidor.

Solicitud
---------

::

    GET /api/admin/log/files

Respuesta
---------

En ``files`` se almacena un arreglo de objetos que representan la informacion de cada archivo de registro, y en ``total`` el numero de elementos.
Cada objeto tiene los siguientes campos.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Campo
     - Descripcion
   * - ``id``
     - Valor del nombre de archivo codificado en Base64 URL (se usa como ``{id}`` al descargar)
   * - ``name``
     - Nombre del archivo de registro
   * - ``lastModified``
     - Fecha/hora de la ultima modificacion

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

Descargar Archivo de Registro
=============================

Descarga el contenido del archivo de registro especificado.
En ``{id}`` se indica el ``id`` obtenido en la lista (el nombre de archivo codificado en Base64).
La respuesta se devuelve como un flujo ``application/octet-stream``.
Si se especifica un nombre de archivo inexistente o un nombre no permitido como archivo de registro, se devuelve una respuesta vacia.

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

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-backup` - API de respaldo
