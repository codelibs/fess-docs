==========================
API de Backup
==========================

Visión General
==============

La API de Backup es una API para consultar y descargar los datos objetivo de copia de seguridad de |Fess|.
Permite obtener la lista de objetivos de copia de seguridad y descargar archivos de copia de seguridad individuales (propiedades del sistema, datos masivos de cada índice, datos NDJSON de registros).

Esta API es exclusivamente de consulta y descarga (solo lectura). La funcionalidad de restauración para subir archivos de copia de seguridad no está disponible a través de la API; si necesita restaurar, utilice Información del sistema → Copia de seguridad en la pantalla de administración.

URL Base
========

::

    /api/admin/backup

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
     - Obtener lista de objetivos de copia de seguridad
   * - GET
     - /file/{id}
     - Descargar archivo de copia de seguridad

Obtener Lista de Objetivos de Copia de Seguridad
================================================

Devuelve la lista de objetivos de copia de seguridad. Los objetivos se determinan en función de la configuración de ``index.backup.targets`` e ``index.backup.log.targets``, y se devuelve una lista combinada de ambos.

Solicitud
---------

::

    GET /api/admin/backup/files

Respuesta
---------

En ``files`` se almacena un arreglo de objetos que representan los objetivos de copia de seguridad, y en ``total`` el número de elementos.
Cada objeto tiene ``id`` y ``name``, y en ambos se establece el nombre del objetivo (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson``, etc.).

A continuación se muestra un ejemplo con la configuración predeterminada (cuando ``index.backup.targets`` e ``index.backup.log.targets`` tienen sus valores por defecto).

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "files": [
          { "id": "fess_basic_config.bulk", "name": "fess_basic_config.bulk" },
          { "id": "fess_config.bulk", "name": "fess_config.bulk" },
          { "id": "fess_user.bulk", "name": "fess_user.bulk" },
          { "id": "system.properties", "name": "system.properties" },
          { "id": "fess.json", "name": "fess.json" },
          { "id": "doc.json", "name": "doc.json" },
          { "id": "click_log.ndjson", "name": "click_log.ndjson" },
          { "id": "favorite_log.ndjson", "name": "favorite_log.ndjson" },
          { "id": "search_log.ndjson", "name": "search_log.ndjson" },
          { "id": "user_info.ndjson", "name": "user_info.ndjson" }
        ],
        "total": 10
      }
    }

.. note::

   En ``version`` se establece la versión del producto de |Fess| en ejecución. El contenido de ``files`` varía
   según la configuración de ``index.backup.targets`` / ``index.backup.log.targets``, por lo que
   el ejemplo anterior corresponde a los valores por defecto.

Descargar Archivo de Copia de Seguridad
=======================================

Descarga el contenido del archivo de copia de seguridad especificado. En ``{id}`` se especifica el ``id`` (nombre del objetivo) obtenido en la lista.
Según el tipo de ``{id}``, el contenido de la respuesta cambia de la siguiente manera.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - Contenido
   * - ``system.properties``
     - Contenido de las propiedades del sistema (``application/octet-stream``)
   * - ``*.bulk`` o nombre de índice sin extensión
     - Datos masivos generados al recorrer el índice con el mismo nombre que el objetivo (``application/octet-stream``). El nombre sin ``.bulk`` se trata como nombre del índice.
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - Datos NDJSON del registro correspondiente (``application/x-ndjson``)

.. note::

   ``fess.json`` y ``doc.json`` son archivos de definición de mapeo (esquema) del índice.
   Se incluyen en la lista de objetivos (``/files``), pero en la descarga de esta API se tratan
   como procesamiento de desplazamiento del índice, al igual que ``.bulk``. Para realizar copias de
   seguridad y restauraciones que incluyan la definición de mapeo, utilice
   Información del sistema → Copia de seguridad en la pantalla de administración.

Si se especifica un ``{id}`` que no existe entre los objetivos de copia de seguridad, se devuelve una respuesta de error con un valor distinto de 0 en ``status`` y el mensaje de error (``Could not find any backup index.``).

Solicitud
---------

::

    GET /api/admin/backup/file/{id}

Respuesta
---------

El flujo del archivo de copia de seguridad. En formato NDJSON se devuelve con ``Content-Type: application/x-ndjson``, y en los demás casos con ``application/octet-stream``.

.. note::

   La exportación de registros (``*.ndjson``) está sujeta a la restricción de ``index.backup.log.load.timeout`` (valor predeterminado ``60000`` milisegundos).
   Si la salida tarda demasiado, los datos del registro pueden quedar truncados.

Ejemplos de Uso
===============

Obtener Lista de Objetivos de Copia de Seguridad
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Descargar Índice de Configuración
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

Descargar Registro de Búsqueda
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-log` - API de registros
