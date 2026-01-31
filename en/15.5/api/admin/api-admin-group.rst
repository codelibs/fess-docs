==========================
Group API
==========================

Overview
========

Group API is an API for managing |Fess| groups.
You can create, update, and delete groups.

Base URL
========

::

    /api/admin/group

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
     - List groups
   * - GET
     - /setting/{id}
     - Get group
   * - POST
     - /setting
     - Create group
   * - PUT
     - /setting
     - Update group
   * - DELETE
     - /setting/{id}
     - Delete group

List Groups
===========

Request
-------

::

    GET /api/admin/group/settings
    PUT /api/admin/group/settings

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
            "id": "group_id_1",
            "name": "Engineering",
            "gidNumber": 1000
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "gidNumber": 1001
          }
        ],
        "total": 5
      }
    }

Get Group
=========

Request
-------

::

    GET /api/admin/group/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "gidNumber": 1000
        }
      }
    }

Create Group
============

Request
-------

::

    POST /api/admin/group/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "gidNumber": 1002
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
     - Group name
   * - ``gidNumber``
     - No
     - Group ID number

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

Update Group
============

Request
-------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "gidNumber": 1002,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

Delete Group
============

Request
-------

::

    DELETE /api/admin/group/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

Usage Examples
==============

Create New Group
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "gidNumber": 2000
         }'

List Groups
-----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-user` - User Management API
- :doc:`api-admin-role` - Role Management API
- :doc:`../../admin/group-guide` - Group Management Guide

