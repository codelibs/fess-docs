==========================
API de Role
==========================

Vision General
==============

La API de Role es para gestionar roles de |Fess|.
Puede operar creacion, actualizacion y eliminacion de roles.

URL Base
========

::

    /api/admin/role

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
     - Obtener lista de roles
   * - GET
     - /setting/{id}
     - Obtener rol
   * - POST
     - /setting
     - Crear rol
   * - PUT
     - /setting
     - Actualizar rol
   * - DELETE
     - /setting/{id}
     - Eliminar rol

Obtener Lista de Roles
======================

Solicitud
---------

::

    GET /api/admin/role/settings
    PUT /api/admin/role/settings

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
            "id": "role_id_1",
            "name": "admin"
          },
          {
            "id": "role_id_2",
            "name": "user"
          }
        ],
        "total": 5
      }
    }

Obtener Rol
===========

Solicitud
---------

::

    GET /api/admin/role/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin"
        }
      }
    }

Crear Rol
=========

Solicitud
---------

::

    POST /api/admin/role/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
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
     - Nombre del rol

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

Actualizar Rol
==============

Solicitud
---------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

Eliminar Rol
============

Solicitud
---------

::

    DELETE /api/admin/role/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Crear Nuevo Rol
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

Obtener Lista de Roles
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-user` - API de gestion de usuarios
- :doc:`api-admin-group` - API de gestion de grupos
- :doc:`../../admin/role-guide` - Guia de gestion de roles
