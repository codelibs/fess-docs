==========================
API de ElevateWord
==========================

Visión General
==============

La API de ElevateWord es para gestionar las palabras elevadas (manipulación del orden de búsqueda para palabras clave específicas) de |Fess|.
Puede colocar documentos específicos en posiciones superiores o inferiores para ciertas consultas de búsqueda.

URL Base
========

::

    /api/admin/elevateword

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
     - Obtener lista de palabras elevadas
   * - GET
     - /setting/{id}
     - Obtener palabra elevada
   * - POST
     - /setting
     - Crear palabra elevada
   * - PUT
     - /setting
     - Actualizar palabra elevada
   * - DELETE
     - /setting/{id}
     - Eliminar palabra elevada
   * - PUT
     - /upload
     - Subir CSV de palabras elevadas
   * - GET
     - /download
     - Descargar CSV de palabras elevadas

Obtener Lista de Palabras Elevadas
==================================

Solicitud
---------

::

    GET /api/admin/elevateword/settings

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
     - Filtro de coincidencia exacta por ID de palabra elevada

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

Obtener Palabra Elevada
=======================

Solicitud
---------

::

    GET /api/admin/elevateword/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

Crear Palabra Elevada
=====================

Solicitud
---------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
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
     - Palabra clave a elevar
   * - ``reading``
     - No
     - Lectura fonética
   * - ``permissions``
     - No
     - Permisos de acceso (cadena separada por saltos de línea, uno por línea. Valor inicial del formulario: permisos de visualización predeterminados de la búsqueda)
   * - ``boost``
     - Sí
     - Valor de impulso (valor inicial del formulario: 100.0)
   * - ``labelTypeIds``
     - No
     - IDs de etiqueta objetivo (arreglo de cadenas)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

Actualizar Palabra Elevada
==========================

Solicitud
---------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   Al actualizar, los siguientes campos son obligatorios además de los campos utilizados para la creación:

   - ``id`` - ID de la palabra elevada a actualizar
   - ``versionNo`` - Número de versión para el bloqueo optimista. Especifique el valor obtenido de ``GET /setting/{id}``.

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

Eliminar Palabra Elevada
========================

Solicitud
---------

::

    DELETE /api/admin/elevateword/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

Subir CSV de Palabras Elevadas
==============================

Registra palabras elevadas en bloque a partir de un archivo CSV. El archivo se envía como ``multipart/form-data``. La importación se ejecuta de forma asíncrona en el servidor.

Solicitud
---------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``elevateWordFile``
     - Sí
     - Archivo CSV de palabras elevadas a subir

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Descargar CSV de Palabras Elevadas
==================================

Descarga las palabras elevadas registradas como archivo CSV (``elevate.csv``). La respuesta es un flujo ``application/octet-stream``.

Solicitud
---------

::

    GET /api/admin/elevateword/download

Ejemplos de Uso
===============

Elevar Nombre de Producto
-------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

Elevar a Etiqueta Específica
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

Subir Archivo CSV
-----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

Descargar Archivo CSV
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-keymatch` - API de coincidencia de claves
- :doc:`api-admin-boostdoc` - API de impulso de documentos
- :doc:`../../admin/elevateword-guide` - Guía de gestión de palabras elevadas
