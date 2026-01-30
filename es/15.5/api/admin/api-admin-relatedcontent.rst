==========================
API de RelatedContent
==========================

Vision General
==============

La API de RelatedContent es para gestionar contenido relacionado de |Fess|.
Puede mostrar contenido personalizado relacionado con palabras clave especificas.

URL Base
========

::

    /api/admin/relatedcontent

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
     - Obtener lista de contenido relacionado
   * - GET
     - /setting/{id}
     - Obtener contenido relacionado
   * - POST
     - /setting
     - Crear contenido relacionado
   * - PUT
     - /setting
     - Actualizar contenido relacionado
   * - DELETE
     - /setting/{id}
     - Eliminar contenido relacionado

Obtener Lista de Contenido Relacionado
======================================

Solicitud
---------

::

    GET /api/admin/relatedcontent/settings
    PUT /api/admin/relatedcontent/settings

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
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtener Contenido Relacionado
=============================

Solicitud
---------

::

    GET /api/admin/relatedcontent/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "sortOrder": 0,
          "virtualHost": ""
        }
      }
    }

Crear Contenido Relacionado
===========================

Solicitud
---------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``term``
     - Si
     - Palabra clave de busqueda
   * - ``content``
     - Si
     - Contenido HTML a mostrar
   * - ``sortOrder``
     - No
     - Orden de visualizacion
   * - ``virtualHost``
     - No
     - Host virtual

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Actualizar Contenido Relacionado
================================

Solicitud
---------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

Eliminar Contenido Relacionado
==============================

Solicitud
---------

::

    DELETE /api/admin/relatedcontent/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_content_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Contenido Relacionado de Informacion del Producto
-------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

Contenido Relacionado de Informacion de Soporte
-----------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-relatedquery` - API de consultas relacionadas
- :doc:`../../admin/relatedcontent-guide` - Guia de gestion de contenido relacionado
