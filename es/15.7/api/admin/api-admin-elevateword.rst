==========================
API de ElevateWord
==========================

Vision General
==============

La API de ElevateWord es para gestionar las palabras elevadas (manipulacion del orden de busqueda para palabras clave especificas) de |Fess|.
Puede colocar documentos especificos en posiciones superiores o inferiores para ciertas consultas de busqueda.

URL Base
========

::

    /api/admin/elevateword

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
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

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametro
     - Tipo
     - Requerido
     - Descripcion
   * - ``size``
     - Integer
     - No
     - Numero de elementos por pagina (predeterminado: 20)
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1, predeterminado: 1)
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
            "reading": "フェス",
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
          "reading": "フェス",
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
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Campo
     - Requerido
     - Descripcion
   * - ``suggestWord``
     - Si
     - Palabra clave a elevar
   * - ``reading``
     - No
     - Lectura fonetica
   * - ``permissions``
     - No
     - Permisos de acceso (cadena separada por saltos de linea, uno por linea. Valor inicial del formulario: permisos de visualizacion predeterminados de la busqueda)
   * - ``boost``
     - Si
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
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   Al actualizar, los siguientes campos son obligatorios ademas de los campos utilizados para la creacion:

   - ``id`` - ID de la palabra elevada a actualizar
   - ``versionNo`` - Numero de version para el bloqueo optimista. Especifique el valor obtenido de ``GET /setting/{id}``.

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

Registra palabras elevadas en bloque a partir de un archivo CSV. El archivo se envia como ``multipart/form-data``. La importacion se ejecuta de forma asincrona en el servidor.

Solicitud
---------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

Parametros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``elevateWordFile``
     - Si
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

Elevar a Etiqueta Especifica
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

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-keymatch` - API de coincidencia de claves
- :doc:`api-admin-boostdoc` - API de impulso de documentos
- :doc:`../../admin/elevateword-guide` - Guia de gestion de palabras elevadas
