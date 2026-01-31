==========================
User API
==========================

Overview
========

User API is an API for managing |Fess| user accounts.
You can create, update, delete users, and configure permissions.

Base URL
========

::

    /api/admin/user

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
     - List users
   * - GET
     - /setting/{id}
     - Get user
   * - POST
     - /setting
     - Create user
   * - PUT
     - /setting
     - Update user
   * - DELETE
     - /setting/{id}
     - Delete user

List Users
==========

Request
-------

::

    GET /api/admin/user/settings
    PUT /api/admin/user/settings

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
            "id": "user_id_1",
            "name": "admin",
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "roles": ["admin"],
            "groups": []
          }
        ],
        "total": 10
      }
    }

Get User
========

Request
-------

::

    GET /api/admin/user/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "user_id_1",
          "name": "admin",
          "surname": "Administrator",
          "givenName": "System",
          "mail": "admin@example.com",
          "telephoneNumber": "",
          "homePhone": "",
          "homePostalAddress": "",
          "labeledUri": "",
          "roomNumber": "",
          "description": "",
          "title": "",
          "pager": "",
          "street": "",
          "postalCode": "",
          "physicalDeliveryOfficeName": "",
          "destinationIndicator": "",
          "internationaliSDNNumber": "",
          "state": "",
          "employeeNumber": "",
          "facsimileTelephoneNumber": "",
          "postOfficeBox": "",
          "initials": "",
          "carLicense": "",
          "mobile": "",
          "postalAddress": "",
          "city": "",
          "teletexTerminalIdentifier": "",
          "x121Address": "",
          "businessCategory": "",
          "registeredAddress": "",
          "displayName": "",
          "preferredLanguage": "",
          "departmentNumber": "",
          "uidNumber": "",
          "gidNumber": "",
          "homeDirectory": "",
          "roles": ["admin"],
          "groups": []
        }
      }
    }

Create User
===========

Request
-------

::

    POST /api/admin/user/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "surname": "Test",
      "givenName": "User",
      "mail": "testuser@example.com",
      "roles": ["user"],
      "groups": ["group_id_1"]
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
     - Username (login ID)
   * - ``password``
     - Yes
     - Password
   * - ``surname``
     - No
     - Surname
   * - ``givenName``
     - No
     - Given name
   * - ``mail``
     - No
     - Email address
   * - ``telephoneNumber``
     - No
     - Phone number
   * - ``roles``
     - No
     - Role ID array
   * - ``groups``
     - No
     - Group ID array

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

Update User
===========

Request
-------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "surname": "Test",
      "givenName": "User Updated",
      "mail": "testuser.updated@example.com",
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

Delete User
===========

Request
-------

::

    DELETE /api/admin/user/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

Usage Examples
==============

Create New User
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "surname": "Doe",
           "givenName": "John",
           "mail": "john.doe@example.com",
           "roles": ["user"],
           "groups": []
         }'

Change User Roles
-----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-role` - Role Management API
- :doc:`api-admin-group` - Group Management API
- :doc:`../../admin/user-guide` - User Management Guide

