==========================
API de LabelType
==========================

Vision General
==============

La API de LabelType es para gestionar tipos de etiqueta de |Fess|.
Puede operar tipos de etiqueta para clasificacion y filtrado de resultados de busqueda.

URL Base
========

::

    /api/admin/labeltype

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
     - Obtener lista de tipos de etiqueta
   * - GET
     - /setting/{id}
     - Obtener tipo de etiqueta
   * - POST
     - /setting
     - Crear tipo de etiqueta
   * - PUT
     - /setting
     - Actualizar tipo de etiqueta
   * - DELETE
     - /setting/{id}
     - Eliminar tipo de etiqueta

Obtener Lista de Tipos de Etiqueta
==================================

Solicitud
---------

::

    GET /api/admin/labeltype/settings
    PUT /api/admin/labeltype/settings

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
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtener Tipo de Etiqueta
========================

Solicitud
---------

::

    GET /api/admin/labeltype/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "sortOrder": 0,
          "permissions": [],
          "virtualHost": ""
        }
      }
    }

Crear Tipo de Etiqueta
======================

Solicitud
---------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": ["guest"]
    }

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre de visualizacion de la etiqueta
   * - ``value``
     - Si
     - Valor de la etiqueta (usado en busquedas)
   * - ``includedPaths``
     - No
     - Expresion regular para rutas con etiqueta (separadas por salto de linea si son multiples)
   * - ``excludedPaths``
     - No
     - Expresion regular para rutas excluidas de etiqueta (separadas por salto de linea si son multiples)
   * - ``sortOrder``
     - No
     - Orden de visualizacion
   * - ``permissions``
     - No
     - Roles con permiso de acceso
   * - ``virtualHost``
     - No
     - Host virtual

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

Actualizar Tipo de Etiqueta
===========================

Solicitud
---------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": ["guest"],
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

Eliminar Tipo de Etiqueta
=========================

Solicitud
---------

::

    DELETE /api/admin/labeltype/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_label_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Crear Etiqueta para Documentacion
---------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": ["guest"]
         }'

Busqueda Usando Etiqueta
------------------------

.. code-block:: bash

    # Filtrar por etiqueta
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`../api-search` - API de busqueda
- :doc:`../../admin/labeltype-guide` - Guia de gestion de tipos de etiqueta
