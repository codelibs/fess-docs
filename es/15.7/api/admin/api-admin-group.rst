==========================
API de Group
==========================

Vision General
==============

La API de Group es para gestionar grupos de |Fess|.
Puede operar creacion, actualizacion y eliminacion de grupos.

URL Base
========

::

    /api/admin/group

Lista de Endpoints
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Metodo
     - Ruta
     - Descripcion
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
     - Numero de elementos por pagina (predeterminado: 25)
   * - ``page``
     - Integer
     - No
     - Numero de pagina (comienza en 1, predeterminado: 1)
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

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``name``
     - Si
     - Nombre del grupo (maximo 100 caracteres)
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

Descripcion de Campos
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Campo
     - Requerido
     - Descripcion
   * - ``id``
     - Si
     - ID del grupo a actualizar
   * - ``name``
     - Si
     - Nombre del grupo (maximo 100 caracteres)
   * - ``attributes``
     - No
     - Mapa de atributos (incluye atributos LDAP como ``gidNumber``). Los valores se especifican como cadenas
   * - ``versionNo``
     - Si
     - Numero de version para el bloqueo optimista. Especifique el valor de ``versionNo`` obtenido al obtener el grupo

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

Informacion de Referencia
=========================

- :doc:`api-admin-overview` - Vision general de Admin API
- :doc:`api-admin-user` - API de gestion de usuarios
- :doc:`api-admin-role` - API de gestion de roles
- :doc:`../../admin/group-guide` - Guia de gestion de grupos
