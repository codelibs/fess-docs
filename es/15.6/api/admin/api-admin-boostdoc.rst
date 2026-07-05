==========================
API de BoostDoc
==========================

Vision General
==============

La API de BoostDoc es para gestionar la configuracion de impulso de documentos de |Fess|.
Puede ajustar la clasificacion de busqueda de documentos que coinciden con condiciones especificas.

URL Base
========

::

    /api/admin/boostdoc

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
     - Obtener lista de impulsos de documentos
   * - GET
     - /setting/{id}
     - Obtener impulso de documento
   * - POST
     - /setting
     - Crear impulso de documento
   * - PUT
     - /setting
     - Actualizar impulso de documento
   * - DELETE
     - /setting/{id}
     - Eliminar impulso de documento

Obtener Lista de Impulsos de Documentos
=======================================

Solicitud
---------

::

    GET /api/admin/boostdoc/settings
    PUT /api/admin/boostdoc/settings

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
            "id": "boostdoc_id_1",
            "urlExpr": ".*docs\\.example\\.com.*",
            "boostExpr": "3.0",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtener Impulso de Documento
============================

Solicitud
---------

::

    GET /api/admin/boostdoc/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": ".*docs\\.example\\.com.*",
          "boostExpr": "3.0",
          "sortOrder": 0
        }
      }
    }

Crear Impulso de Documento
==========================

Solicitud
---------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``urlExpr``
     - Si
     - Patron de expresion regular de URL
   * - ``boostExpr``
     - Si
     - Expresion de impulso (numero o expresion)
   * - ``sortOrder``
     - No
     - Orden de aplicacion

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Actualizar Impulso de Documento
===============================

Solicitud
---------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Eliminar Impulso de Documento
=============================

Solicitud
---------

::

    DELETE /api/admin/boostdoc/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_boostdoc_id",
        "created": false
      }
    }

Ejemplos de Expresiones de Impulso
==================================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Expresion de Impulso
     - Descripcion
   * - ``2.0``
     - Impulso con valor fijo
   * - ``doc['boost'].value * 2``
     - Duplicar el valor de impulso del documento
   * - ``Math.log(doc['click_count'].value + 1)``
     - Impulso con escala logaritmica basado en conteo de clics
   * - ``doc['last_modified'].value > now - 7d ? 3.0 : 1.0``
     - Triple impulso si fue actualizado en la ultima semana

Ejemplos de Uso
===============

Impulso para Sitio de Documentacion
-----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*docs\\.example\\.com.*",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

Impulso para Contenido Nuevo
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*",
           "boostExpr": "doc[\"last_modified\"].value > now - 30d ? 2.0 : 1.0",
           "sortOrder": 10
         }'

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-elevateword` - API de palabras elevadas
- :doc:`../../admin/boostdoc-guide` - Guia de gestion de impulso de documentos
