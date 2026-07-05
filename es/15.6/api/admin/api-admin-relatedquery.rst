==========================
API de RelatedQuery
==========================

Vision General
==============

La API de RelatedQuery es para gestionar consultas relacionadas de |Fess|.
Puede sugerir palabras clave de busqueda relacionadas para consultas de busqueda especificas.

URL Base
========

::

    /api/admin/relatedquery

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
     - Obtener lista de consultas relacionadas
   * - GET
     - /setting/{id}
     - Obtener consulta relacionada
   * - POST
     - /setting
     - Crear consulta relacionada
   * - PUT
     - /setting
     - Actualizar consulta relacionada
   * - DELETE
     - /setting/{id}
     - Eliminar consulta relacionada

Obtener Lista de Consultas Relacionadas
=======================================

Solicitud
---------

::

    GET /api/admin/relatedquery/settings
    PUT /api/admin/relatedquery/settings

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
            "id": "query_id_1",
            "term": "fess",
            "queries": ["fess tutorial", "fess installation", "fess configuration"]
          }
        ],
        "total": 5
      }
    }

Obtener Consulta Relacionada
============================

Solicitud
---------

::

    GET /api/admin/relatedquery/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": ["fess tutorial", "fess installation", "fess configuration"],
          "virtualHost": ""
        }
      }
    }

Crear Consulta Relacionada
==========================

Solicitud
---------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search"],
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
   * - ``queries``
     - Si
     - Array de consultas relacionadas
   * - ``virtualHost``
     - No
     - Host virtual

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Actualizar Consulta Relacionada
===============================

Solicitud
---------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search", "search tips"],
      "virtualHost": "",
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Eliminar Consulta Relacionada
=============================

Solicitud
---------

::

    DELETE /api/admin/relatedquery/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_query_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Consultas Relacionadas con Productos
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": ["product features", "product pricing", "product comparison", "product reviews"]
         }'

Consultas Relacionadas con Ayuda
--------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": ["help center", "help documentation", "help contact support"]
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-relatedcontent` - API de contenido relacionado
- :doc:`api-admin-suggest` - API de gestion de sugerencias
- :doc:`../../admin/relatedquery-guide` - Guia de gestion de consultas relacionadas
