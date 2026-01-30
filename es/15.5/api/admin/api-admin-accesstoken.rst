==========================
API de AccessToken
==========================

Vision General
==============

La API de AccessToken es para gestionar tokens de acceso API de |Fess|.
Puede operar creacion, actualizacion y eliminacion de tokens.

URL Base
========

::

    /api/admin/accesstoken

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
     - Obtener lista de tokens de acceso
   * - GET
     - /setting/{id}
     - Obtener token de acceso
   * - POST
     - /setting
     - Crear token de acceso
   * - PUT
     - /setting
     - Actualizar token de acceso
   * - DELETE
     - /setting/{id}
     - Eliminar token de acceso

Obtener Lista de Tokens de Acceso
=================================

Solicitud
---------

::

    GET /api/admin/accesstoken/settings
    PUT /api/admin/accesstoken/settings

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expiredTime": 1735689600000,
            "permissions": ["admin"]
          }
        ],
        "total": 5
      }
    }

Obtener Token de Acceso
=======================

Solicitud
---------

::

    GET /api/admin/accesstoken/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "token",
          "expiredTime": 1735689600000,
          "permissions": ["admin"]
        }
      }
    }

Crear Token de Acceso
=====================

Solicitud
---------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "parameterName": "token",
      "permissions": ["user"]
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
     - Nombre del token
   * - ``token``
     - No
     - Cadena del token (generado automaticamente si no se especifica)
   * - ``parameterName``
     - No
     - Nombre del parametro (predeterminado: "token")
   * - ``expiredTime``
     - No
     - Tiempo de expiracion (milisegundos Unix)
   * - ``permissions``
     - No
     - Roles permitidos

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "token": "generated_token_string",
        "created": true
      }
    }

Actualizar Token de Acceso
==========================

Solicitud
---------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "parameterName": "token",
      "expiredTime": 1767225600000,
      "permissions": ["user", "editor"],
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

Eliminar Token de Acceso
========================

Solicitud
---------

::

    DELETE /api/admin/accesstoken/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_token_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Crear Token API
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "External App Token",
           "parameterName": "token",
           "permissions": ["guest"]
         }'

Llamada API Usando Token
------------------------

.. code-block:: bash

    # Usar token como parametro
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # Usar token en encabezado Authorization
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`../api-search` - API de busqueda
- :doc:`../../admin/accesstoken-guide` - Guia de gestion de tokens de acceso
