==========================
AccessToken API
==========================

Overview
========

AccessToken API is an API for managing |Fess| API access tokens.
You can create, update, and delete tokens.

Base URL
========

::

    /api/admin/accesstoken

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
     - List access tokens
   * - GET
     - /setting/{id}
     - Get access token
   * - POST
     - /setting
     - Create access token
   * - PUT
     - /setting
     - Update access token
   * - DELETE
     - /setting/{id}
     - Delete access token

List Access Tokens
==================

Request
-------

::

    GET /api/admin/accesstoken/settings
    PUT /api/admin/accesstoken/settings

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expiredTime": 1735689600000,
            "permissions": ["admin"]
          }
        ],
        "total": 5
      }
    }

Get Access Token
================

Request
-------

::

    GET /api/admin/accesstoken/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "token",
          "expiredTime": 1735689600000,
          "permissions": ["admin"]
        }
      }
    }

Create Access Token
===================

Request
-------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "parameterName": "token",
      "permissions": ["user"]
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
     - Token name
   * - ``token``
     - No
     - Token string (auto-generated if not specified)
   * - ``parameterName``
     - No
     - Parameter name (default: "token")
   * - ``expiredTime``
     - No
     - Expiration time (Unix timestamp in milliseconds)
   * - ``permissions``
     - No
     - Permitted roles

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "token": "generated_token_string",
        "created": true
      }
    }

Update Access Token
===================

Request
-------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "parameterName": "token",
      "expiredTime": 1767225600000,
      "permissions": ["user", "editor"],
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

Delete Access Token
===================

Request
-------

::

    DELETE /api/admin/accesstoken/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_token_id",
        "created": false
      }
    }

Usage Examples
==============

Create API Token
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "External App Token",
           "parameterName": "token",
           "permissions": ["guest"]
         }'

API Call Using Token
--------------------

.. code-block:: bash

    # Use token as parameter
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # Use token as Authorization header
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../api-search` - Search API
- :doc:`../../admin/accesstoken-guide` - Access Token Management Guide

