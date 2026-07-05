==========================
API de Suggest
==========================

Vision General
==============

La API de Suggest es para gestionar la funcionalidad de sugerencias de |Fess|.
Puede operar agregar, eliminar y actualizar palabras de sugerencia.

URL Base
========

::

    /api/admin/suggest

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
   * - GET/PUT
     - /settings
     - Obtener lista de palabras de sugerencia
   * - GET
     - /setting/{id}
     - Obtener palabra de sugerencia
   * - POST
     - /setting
     - Crear palabra de sugerencia
   * - PUT
     - /setting
     - Actualizar palabra de sugerencia
   * - DELETE
     - /setting/{id}
     - Eliminar palabra de sugerencia
   * - DELETE
     - /delete-all
     - Eliminar todas las palabras de sugerencia

Obtener Lista de Palabras de Sugerencia
=======================================

Solicitud
---------

::

    GET /api/admin/suggest/settings
    PUT /api/admin/suggest/settings

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
     - Numero de pagina (comienza en 0)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "suggest_id_1",
            "text": "fess",
            "reading": "fess",
            "fields": ["title", "content"],
            "tags": ["product"],
            "roles": ["guest"],
            "lang": "ja",
            "score": 1.0
          }
        ],
        "total": 100
      }
    }

Obtener Palabra de Sugerencia
=============================

Solicitud
---------

::

    GET /api/admin/suggest/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "suggest_id_1",
          "text": "fess",
          "reading": "fess",
          "fields": ["title", "content"],
          "tags": ["product"],
          "roles": ["guest"],
          "lang": "ja",
          "score": 1.0
        }
      }
    }

Crear Palabra de Sugerencia
===========================

Solicitud
---------

::

    POST /api/admin/suggest/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "text": "search engine",
      "reading": "search engine",
      "fields": ["title"],
      "tags": ["feature"],
      "roles": ["guest"],
      "lang": "en",
      "score": 1.0
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``text``
     - Si
     - Texto de sugerencia
   * - ``reading``
     - No
     - Lectura fonetica
   * - ``fields``
     - No
     - Campos objetivo
   * - ``tags``
     - No
     - Etiquetas
   * - ``roles``
     - No
     - Roles con permiso de acceso
   * - ``lang``
     - No
     - Codigo de idioma
   * - ``score``
     - No
     - Puntuacion (predeterminado: 1.0)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_suggest_id",
        "created": true
      }
    }

Actualizar Palabra de Sugerencia
================================

Solicitud
---------

::

    PUT /api/admin/suggest/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_suggest_id",
      "text": "search engine",
      "reading": "search engine",
      "fields": ["title", "content"],
      "tags": ["feature", "popular"],
      "roles": ["guest"],
      "lang": "en",
      "score": 2.0,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_suggest_id",
        "created": false
      }
    }

Eliminar Palabra de Sugerencia
==============================

Solicitud
---------

::

    DELETE /api/admin/suggest/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_suggest_id",
        "created": false
      }
    }

Eliminar Todas las Palabras de Sugerencia
=========================================

Solicitud
---------

::

    DELETE /api/admin/suggest/delete-all

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "count": 250
      }
    }

Ejemplos de Uso
===============

Agregar Palabra Clave Popular
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/suggest/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "getting started",
           "fields": ["title"],
           "tags": ["tutorial"],
           "roles": ["guest"],
           "lang": "en",
           "score": 5.0
         }'

Eliminacion Masiva de Sugerencias
---------------------------------

.. code-block:: bash

    # Eliminar todas las sugerencias
    curl -X DELETE "http://localhost:8080/api/admin/suggest/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-badword` - API de palabras prohibidas
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/suggest-guide` - Guia de gestion de sugerencias
