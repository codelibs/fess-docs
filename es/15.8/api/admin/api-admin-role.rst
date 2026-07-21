==========================
API de Role
==========================

Visión General
==============

La API de Role es para gestionar roles de |Fess|.
Puede operar creación, actualización y eliminación de roles.

URL Base
========

::

    /api/admin/role

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Método
     - Ruta
     - Descripción
   * - GET
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

Parámetros
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parámetro
     - Tipo
     - Requerido
     - Descripción
   * - ``size``
     - Integer
     - No
     - Número de elementos por página (predeterminado: 25. Configurable mediante ``paging.page.size`` en ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1. Los valores de 0 o menos se tratan como 1)
   * - ``id``
     - String
     - No
     - Filtra por coincidencia exacta con el ID de rol especificado

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "role_id_1",
            "name": "admin",
            "versionNo": 1
          },
          {
            "id": "role_id_2",
            "name": "user",
            "versionNo": 1
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
          "name": "admin",
          "versionNo": 1
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

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripción
   * - ``name``
     - Sí
     - Nombre del rol (máximo 100 caracteres)
   * - ``attributes``
     - No
     - Mapa de atributos. Los valores se especifican como cadenas

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

Descripción de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripción
   * - ``id``
     - Sí
     - ID del rol a actualizar
   * - ``name``
     - Sí
     - Nombre del rol (máximo 100 caracteres)
   * - ``attributes``
     - No
     - Mapa de atributos. Los valores se especifican como cadenas
   * - ``versionNo``
     - Sí
     - Número de versión para el bloqueo optimista. Especifique el valor de ``versionNo`` obtenido al obtener el rol

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

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-user` - API de gestión de usuarios
- :doc:`api-admin-group` - API de gestión de grupos
- :doc:`../../admin/role-guide` - Guía de gestión de roles
