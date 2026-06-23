==========================
User API
==========================

Overview
========

User API is a REST API for managing |Fess| user accounts.
You can create, get, update, and delete users, and assign roles and groups.

This is an admin API, and access requires authentication with an admin access token.
See :doc:`api-admin-overview` for the authentication method and common specifications.

Every response is wrapped in a ``response`` object and includes the following common fields:

- ``version`` : The |Fess| product version string.
- ``status`` : The result status code (``0`` =success, ``1`` =bad request, ``2`` =system error, ``3`` =unauthorized, ``9`` =failed).

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
   * - GET
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

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - Parameter
     - Type
     - Required
     - Description
   * - ``size``
     - Integer
     - No
     - Number of items per page. The default is the configured value ``paging.page.size`` (default: 25).
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1). The default is 1.

.. note::

   In the current implementation, the user list endpoint does not apply the ``size`` and ``page`` parameters.
   It always returns the first page, with the number of items defined by the server setting ``paging.page.size`` (default: 25), sorted by username (``name``) in ascending order.
   The total number of matching users is available in ``response.total``.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : The array of users on the current page.
- ``total`` : The total number of matching users.

Get User
========

Request
-------

::

    GET /api/admin/user/setting/{id}

Specify the document ID of the target user in ``{id}``.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["admin"],
          "groups": [],
          "versionNo": 1
        }
      }
    }

.. note::

   ``attributes`` includes all attributes stored for the user, except ``name``, ``password``, ``roles``, and ``groups``.
   ``password`` is not included in the response.

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
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Username (login ID)
   * - ``password``
     - No
     - Password
   * - ``confirmPassword``
     - No
     - Confirmation password
   * - ``attributes``
     - No
     - Map of attributes (see below)
   * - ``roles``
     - No
     - Array of role IDs
   * - ``groups``
     - No
     - Array of group IDs

.. note::

   The REST API does not perform a password-required check, a match check between ``password`` and ``confirmPassword``, or password policy validation (these are applied only in the admin UI).
   In practice, it is recommended to specify a valid ``password`` whose value matches ``confirmPassword``.

The keys of ``attributes`` are the user entity attribute names (the schema item names derived from LDAP).
The most common keys are:

- ``surname``, ``givenName``, ``displayName``, ``mail``
- ``telephoneNumber``, ``mobile``, ``homePhone``
- ``employeeNumber``, ``title``, ``description``, ``homeDirectory``
- ``uidNumber``, ``gidNumber``

``uidNumber`` and ``gidNumber`` must be numeric (their type is validated on update).
Many other LDAP attribute keys can also be specified.

.. note::

   On creation, the user ID (document ID) is automatically generated as the Base64 URL-encoded value of the username
   (for example, the username ``admin`` becomes ``YWRtaW4=``).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` : The document ID of the created user.
- ``created`` : ``true`` when created.

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
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Field
     - Required
     - Description
   * - ``id``
     - Yes
     - The document ID of the user to update.
   * - ``name``
     - Yes
     - Username (login ID)
   * - ``versionNo``
     - Yes
     - Version number (for optimistic locking)
   * - ``password``
     - No
     - New password (updated only when specified)
   * - ``confirmPassword``
     - No
     - Confirmation password
   * - ``attributes``
     - No
     - Map of attributes (see "Create User")
   * - ``roles``
     - No
     - Array of role IDs
   * - ``groups``
     - No
     - Array of group IDs

.. note::

   On update, ``id``, ``name``, and ``versionNo`` are required.
   ``versionNo`` is the value returned when getting the target user (GET), and it corresponds to the OpenSearch document version.
   If it does not match the current version, the request is treated as a conflict and the update is rejected.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : ``false`` for an update.

Delete User
===========

Request
-------

::

    DELETE /api/admin/user/setting/{id}

Specify the document ID of the user to delete in ``{id}``.

.. note::

   You cannot delete the currently logged-in user.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` : The document ID of the deleted user.

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
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
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
