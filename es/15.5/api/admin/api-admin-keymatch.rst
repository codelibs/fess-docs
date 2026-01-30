==========================
API de KeyMatch
==========================

Vision General
==============

La API de KeyMatch es para gestionar coincidencias de claves (vinculacion de palabras clave de busqueda con resultados) de |Fess|.
Puede hacer que documentos especificos aparezcan en los primeros lugares para ciertas palabras clave.

URL Base
========

::

    /api/admin/keymatch

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
     - Obtener lista de coincidencias de claves
   * - GET
     - /setting/{id}
     - Obtener coincidencia de clave
   * - POST
     - /setting
     - Crear coincidencia de clave
   * - PUT
     - /setting
     - Actualizar coincidencia de clave
   * - DELETE
     - /setting/{id}
     - Eliminar coincidencia de clave

Obtener Lista de Coincidencias de Claves
========================================

Solicitud
---------

::

    GET /api/admin/keymatch/settings
    PUT /api/admin/keymatch/settings

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
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

Obtener Coincidencia de Clave
=============================

Solicitud
---------

::

    GET /api/admin/keymatch/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "maxSize": 10,
          "boost": 10.0
        }
      }
    }

Crear Coincidencia de Clave
===========================

Solicitud
---------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "maxSize": 5,
      "boost": 20.0
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
   * - ``query``
     - Si
     - Consulta de condicion de coincidencia
   * - ``maxSize``
     - No
     - Numero maximo de resultados (predeterminado: 10)
   * - ``boost``
     - No
     - Valor de impulso (predeterminado: 1.0)

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

Actualizar Coincidencia de Clave
================================

Solicitud
---------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

Eliminar Coincidencia de Clave
==============================

Solicitud
---------

::

    DELETE /api/admin/keymatch/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_keymatch_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Crear Coincidencia de Clave para Pagina de Producto
---------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

Coincidencia de Clave para Pagina de Soporte
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "maxSize": 5,
           "boost": 20.0
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/keymatch-guide` - Guia de gestion de coincidencias de claves
