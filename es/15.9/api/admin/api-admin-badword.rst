==========================
API de BadWord
==========================

Visión General
==============

La API de BadWord es para gestionar las palabras prohibidas (exclusión de palabras de sugerencia inapropiadas) de |Fess|.
Puede configurar palabras clave que no desea mostrar en la función de sugerencias.

URL Base
========

::

    /api/admin/badword

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
     - Obtener lista de palabras prohibidas
   * - GET
     - /setting/{id}
     - Obtener palabra prohibida
   * - POST
     - /setting
     - Crear palabra prohibida
   * - PUT
     - /setting
     - Actualizar palabra prohibida
   * - DELETE
     - /setting/{id}
     - Eliminar palabra prohibida
   * - PUT
     - /upload
     - Subir CSV de palabras prohibidas
   * - GET
     - /download
     - Descargar CSV de palabras prohibidas

Obtener Lista de Palabras Prohibidas
====================================

Solicitud
---------

::

    GET /api/admin/badword/settings

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (predeterminado: 20)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``id``
     - String
     - No
     - Filtrar solo la palabra prohibida con el ID especificado

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

Obtener Palabra Prohibida
=========================

Solicitud
---------

::

    GET /api/admin/badword/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

Crear Palabra Prohibida
=======================

Solicitud
---------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
    }

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripción
   * - ``suggestWord``
     - Sí
     - Palabra clave a excluir (no puede contener espacios en blanco)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

Actualizar Palabra Prohibida
============================

Solicitud
---------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

Eliminar Palabra Prohibida
==========================

Solicitud
---------

::

    DELETE /api/admin/badword/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

Subir CSV de Palabras Prohibidas
================================

Registra palabras prohibidas en bloque a partir de un archivo CSV. El archivo se envía como ``multipart/form-data``. La importación se ejecuta de forma asíncrona en el servidor.

Solicitud
---------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``badWordFile``
     - Sí
     - Archivo CSV de palabras prohibidas a subir

Formato CSV
~~~~~~~~~~~

- La primera línea se omite como fila de encabezado (el nombre de la columna es arbitrario; al descargar se escribe ``BadWord``).
- A partir de la segunda línea, escriba una palabra prohibida por línea como ``suggestWord``.
- Las líneas cuyo valor está en blanco se ignoran.
- Anteponga ``--`` a una palabra para eliminarla (por ejemplo, ``--spam`` elimina ``spam``).
- Especificar una palabra ya registrada se trata como una actualización (se restablecen el usuario y la fecha de actualización).

.. note::

   Dado que la importación se ejecuta de forma asíncrona en el servidor, una respuesta ``status: 0``
   indica que la solicitud fue aceptada, no que la importación se haya completado.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Descargar CSV de Palabras Prohibidas
====================================

Descarga las palabras prohibidas registradas como archivo CSV (``badword.csv``). La respuesta es un flujo ``application/octet-stream``.
El CSV tiene una fila de encabezado ``BadWord`` en la primera línea, seguida de una palabra prohibida registrada por línea.

Solicitud
---------

::

    GET /api/admin/badword/download

Ejemplos de Uso
===============

Excluir Palabra Clave de Spam
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

Subir Archivo CSV
-----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

Descargar Archivo CSV
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-suggest` - API de gestión de sugerencias
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/badword-guide` - Guía de gestión de palabras prohibidas
