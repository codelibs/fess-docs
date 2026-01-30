==========================
Role API
==========================

Overview
========

Role API is an API for managing |Fess| roles.
You can create, update, and delete roles.

Base URL
========

::

    /api/admin/role

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET/PUT
     - /settings
     - List roles
   * - GET
     - /setting/{id}
     - Get role
   * - POST
     - /setting
     - Create role
   * - PUT
     - /setting
     - Update role
   * - DELETE
     - /setting/{id}
     - Delete role

List Roles
==========

Request
-------

::

    GET /api/admin/role/settings
    PUT /api/admin/role/settings

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``size``
     - Integer
     - No
     - Number of items per page (default: 20)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 0)

Response
--------

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

Get Role
========

Request
-------

::

    GET /api/admin/role/setting/{id}

Response
--------

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

Create Role
===========

Request
-------

::

    POST /api/admin/role/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Role name

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

Update Role
===========

Request
-------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

Delete Role
===========

Request
-------

::

    DELETE /api/admin/role/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

Usage Examples
==============

Create New Role
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

List Roles
----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-user` - User Management API
- :doc:`api-admin-group` - Group Management API
- :doc:`../../admin/role-guide` - Role Management Guide

