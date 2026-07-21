==========================
API de Group
==========================

Visión General
==============

La API de Group es para gestionar grupos de |Fess|.
Puede operar creación, actualización y eliminación de grupos.

URL Base
========

::

    /api/admin/group

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
     - Obtener lista de grupos
   * - GET
     - /setting/{id}
     - Obtener grupo
   * - POST
     - /setting
     - Crear grupo
   * - PUT
     - /setting
     - Actualizar grupo
   * - DELETE
     - /setting/{id}
     - Eliminar grupo

Obtener Lista de Grupos
=======================

Solicitud
---------

::

    GET /api/admin/group/settings

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
     - Número de elementos por página (predeterminado: 25)
   * - ``page``
     - Integer
     - No
     - Número de página (comienza en 1, predeterminado: 1)
   * - ``id``
     - String
     - No
     - Filtra por coincidencia exacta con el ID de grupo especificado

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "group_id_1",
            "name": "Engineering",
            "attributes": {
              "gidNumber": "1000"
            },
            "versionNo": 1
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "attributes": {
              "gidNumber": "1001"
            },
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

Obtener Grupo
=============

Solicitud
---------

::

    GET /api/admin/group/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "attributes": {
            "gidNumber": "1000"
          },
          "versionNo": 1
        }
      }
    }

Crear Grupo
===========

Solicitud
---------

::

    POST /api/admin/group/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "attributes": {
        "gidNumber": "1002"
      }
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
     - Nombre del grupo (máximo 100 caracteres)
   * - ``attributes``
     - No
     - Mapa de atributos (incluye atributos LDAP como ``gidNumber``). Los valores se especifican como cadenas

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

Actualizar Grupo
================

Solicitud
---------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

Cuerpo de la Solicitud
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "attributes": {
        "gidNumber": "1002"
      },
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
     - ID del grupo a actualizar
   * - ``name``
     - Sí
     - Nombre del grupo (máximo 100 caracteres)
   * - ``attributes``
     - No
     - Mapa de atributos (incluye atributos LDAP como ``gidNumber``). Los valores se especifican como cadenas
   * - ``versionNo``
     - Sí
     - Número de versión para el bloqueo optimista. Especifique el valor de ``versionNo`` obtenido al obtener el grupo

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

Eliminar Grupo
==============

Solicitud
---------

::

    DELETE /api/admin/group/setting/{id}

Respuesta
---------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

Ejemplos de Uso
===============

Crear Nuevo Grupo
-----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "attributes": {
             "gidNumber": "2000"
           }
         }'

Obtener Lista de Grupos
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Información de Referencia
=========================

- :doc:`api-admin-overview` - Visión general de Admin API
- :doc:`api-admin-user` - API de gestión de usuarios
- :doc:`api-admin-role` - API de gestión de roles
- :doc:`../../admin/group-guide` - Guía de gestión de grupos
