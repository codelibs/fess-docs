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
   * - GET
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
     - Number of items per page (default: 25)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1, default: 1)
   * - ``id``
     - String
     - No
     - Filters by exact match on the specified group ID

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
          "attributes": {
            "gidNumber": "1000"
          },
          "versionNo": 1
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
      "attributes": {
        "gidNumber": "1002"
      }
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
     - Group name (max 100 characters)
   * - ``attributes``
     - No
     - Map of attributes (includes LDAP attributes such as ``gidNumber``). Values are specified as strings

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
      "attributes": {
        "gidNumber": "1002"
      },
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
     - Group ID to update
   * - ``name``
     - Yes
     - Group name (max 100 characters)
   * - ``attributes``
     - No
     - Map of attributes (includes LDAP attributes such as ``gidNumber``). Values are specified as strings
   * - ``versionNo``
     - Yes
     - Version number for optimistic locking. Specify the ``versionNo`` value obtained from Get Group

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
           "attributes": {
             "gidNumber": "2000"
           }
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

