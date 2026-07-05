==========================
API de BadWord
==========================

Vision General
==============

La API de BadWord es para gestionar palabras prohibidas (exclusion de palabras de sugerencia inapropiadas) de |Fess|.
Puede configurar palabras clave que no desea mostrar en la funcion de sugerencias.

URL Base
========

::

    /api/admin/badword

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

Obtener Lista de Palabras Prohibidas
====================================

Solicitud
---------

::

    GET /api/admin/badword/settings
    PUT /api/admin/badword/settings

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
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word",
            "targetRole": "",
            "targetLabel": ""
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
          "suggestWord": "inappropriate_word",
          "targetRole": "",
          "targetLabel": ""
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
      "suggestWord": "spam_keyword",
      "targetRole": "guest",
      "targetLabel": ""
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
     - Palabra clave a excluir
   * - ``targetRole``
     - No
     - Rol objetivo (vacio para todos los roles)
   * - ``targetLabel``
     - No
     - Etiqueta objetivo (vacio para todas las etiquetas)

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
      "targetRole": "guest",
      "targetLabel": "",
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

Ejemplos de Uso
===============

Excluir Palabra Clave de Spam
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam",
           "targetRole": "",
           "targetLabel": ""
         }'

Palabra Prohibida para Rol Especifico
-------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "internal",
           "targetRole": "guest",
           "targetLabel": ""
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-suggest` - API de gestion de sugerencias
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/badword-guide` - Guia de gestion de palabras prohibidas
