==========================
API de ElevateWord
==========================

Vision General
==============

La API de ElevateWord es para gestionar palabras elevadas (manipulacion del orden de busqueda para palabras clave especificas) de |Fess|.
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
   * - GET/PUT
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

Obtener Lista de Palabras Elevadas
==================================

Solicitud
---------

::

    GET /api/admin/elevateword/settings
    PUT /api/admin/elevateword/settings

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "fess",
            "permissions": [],
            "boost": 10.0,
            "targetRole": "",
            "targetLabel": ""
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
          "reading": "fess",
          "permissions": [],
          "boost": 10.0,
          "targetRole": "",
          "targetLabel": ""
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
      "reading": "documentacion",
      "permissions": ["guest"],
      "boost": 15.0,
      "targetRole": "user",
      "targetLabel": "docs"
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

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
     - Roles con permiso de acceso
   * - ``boost``
     - No
     - Valor de impulso (predeterminado: 1.0)
   * - ``targetRole``
     - No
     - Rol objetivo
   * - ``targetLabel``
     - No
     - Etiqueta objetivo

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
      "reading": "documentacion",
      "permissions": ["guest", "user"],
      "boost": 20.0,
      "targetRole": "user",
      "targetLabel": "docs",
      "versionNo": 1
    }

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
           "boost": 20.0,
           "permissions": ["guest"]
         }'

Elevar a Etiqueta Especifica
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 10.0,
           "targetLabel": "technical_docs",
           "permissions": ["guest"]
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-keymatch` - API de coincidencia de claves
- :doc:`api-admin-boostdoc` - API de impulso de documentos
- :doc:`../../admin/elevateword-guide` - Guia de gestion de palabras elevadas
