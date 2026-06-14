==========================
API de Backup
==========================

Vision General
==============

La API de Backup es una API para consultar y descargar los datos objetivo de copia de seguridad de |Fess|.
Permite obtener la lista de objetivos de copia de seguridad y descargar archivos de copia de seguridad individuales (propiedades del sistema, datos masivos de cada indice, datos NDJSON de registros).

URL Base
========

::

    /api/admin/backup

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
     - Obtener lista de objetivos de copia de seguridad
   * - GET
     - /file/{id}
     - Descargar archivo de copia de seguridad

Obtener Lista de Objetivos de Copia de Seguridad
================================================

Devuelve la lista de objetivos de copia de seguridad. Los objetivos se basan en la configuracion de ``index.backup.targets`` e ``index.backup.log.targets``.

Solicitud
---------

::

    GET /api/admin/backup/files

Respuesta
---------

En ``files`` se almacena un arreglo de objetos que representan los objetivos de copia de seguridad, y en ``total`` el numero de elementos.
Cada objeto tiene ``id`` y ``name``, y en ambos se establece el nombre del objetivo (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``, etc.).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "fess_config.bulk",
            "name": "fess_config.bulk"
          },
          {
            "id": "system.properties",
            "name": "system.properties"
          },
          {
            "id": "search_log.ndjson",
            "name": "search_log.ndjson"
          }
        ],
        "total": 3
      }
    }

Descargar Archivo de Copia de Seguridad
=======================================

Descarga el contenido del archivo de copia de seguridad especificado. En ``{id}`` se especifica el ``id`` (nombre del objetivo) obtenido en la lista.
Segun el tipo de ``{id}``, el contenido de la respuesta cambia de la siguiente manera.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - Contenido
   * - ``system.properties``
     - Contenido de las propiedades del sistema
   * - ``*.bulk`` o nombre de indice sin la extension ``.bulk``
     - Datos masivos generados al recorrer el indice objetivo
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - Datos NDJSON del registro correspondiente

Si se especifica un ``{id}`` que no existe entre los objetivos de copia de seguridad, se produce un error.

Solicitud
---------

::

    GET /api/admin/backup/file/{id}

Respuesta
---------

El flujo del archivo de copia de seguridad. En formato NDJSON se devuelve con ``Content-Type: application/x-ndjson``, y en los demas casos con ``application/octet-stream``.

Ejemplos de Uso
===============

Obtener Lista de Objetivos de Copia de Seguridad
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Descargar Indice de Configuracion
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

Descargar Registro de Busqueda
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-log` - API de registros
