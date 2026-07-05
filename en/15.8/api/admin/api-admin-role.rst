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
   * - GET
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
     - Number of items per page (default: 25, configurable via ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1, default: 1; values of 0 or less are treated as 1)
   * - ``id``
     - String
     - No
     - Filters by exact match on the specified role ID

Response
--------

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
          "name": "admin",
          "versionNo": 1
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
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Role name (max 100 characters)
   * - ``attributes``
     - No
     - Map of attributes. Values are specified as strings

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

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``id``
     - Yes
     - Role ID to update
   * - ``name``
     - Yes
     - Role name (max 100 characters)
   * - ``attributes``
     - No
     - Map of attributes. Values are specified as strings
   * - ``versionNo``
     - Yes
     - Version number for optimistic locking. Specify the ``versionNo`` value obtained from Get Role

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

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-user` - User Management API
- :doc:`api-admin-group` - Group Management API
- :doc:`../../admin/role-guide` - Role Management Guide
