==========================
AccessToken API
==========================

Overview
========

The AccessToken API is an API for managing |Fess| API access tokens.
You can create, retrieve, update, and delete tokens.

Access tokens are used for authentication when calling the |Fess| Search API or Admin API programmatically.
For common specifications of the Admin API including this API (authentication methods, response format, ``status`` values, error responses,
and HTTP status codes), refer to :doc:`api-admin-overview`.

.. note::

   To access this API, the access token used in the request must have a permission matching ``api.admin.access.permissions``
   (default value: ``{role}admin-api`` ).

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
   * - GET
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
     - Number of items per page (default: 25; configurable via ``paging.page.size``)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1; default: 1)
   * - ``id``
     - String
     - No
     - Filter to retrieve only the token with the specified ID

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Each token object also includes audit and version information such as ``createdBy`` , ``createdTime`` , ``updatedBy`` ,
   ``updatedTime`` , and ``versionNo`` .
   ``createdTime`` and ``updatedTime`` are milliseconds since epoch (numeric).
   Fields with a value of ``null`` are excluded from the response.
   ``permissions`` is returned as a newline ( ``\n`` ) separated string.

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
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
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
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
    }

Field Descriptions
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``name``
     - Yes
     - Token name (maximum 1000 characters)
   * - ``permissions``
     - No
     - Permissions granted to this token. Multiple permissions can be specified separated by newlines ( ``\n`` ) (example: ``{role}admin-api`` ). Tokens that call the Admin API require a permission matching ``api.admin.access.permissions`` (default value: ``{role}admin-api`` ).
   * - ``parameterName``
     - No
     - Request parameter name for passing additional permissions. If a request authenticated with this token contains a parameter with the name specified here, its value will be added to ``permissions`` . If omitted, this is not configured.
   * - ``expires``
     - No
     - Expiration time. Specified as a string in ``YYYY-MM-DDTHH:MM:SS`` format (example: ``2026-01-01T00:00:00`` ). If omitted, the token does not expire.

.. note::

   The token string ( ``token`` ) is automatically generated on the server side. Even if ``token``
   is specified in the request body, it will be ignored. Since the creation response does not include the token string,
   retrieve the generated token string using "Get Access Token" ( ``GET /setting/{id}`` ).

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
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
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

Field Descriptions
~~~~~~~~~~~~~~~~~~

For updates, the following fields are used in addition to the fields used at creation time.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``id``
     - Yes
     - ID of the token to update
   * - ``versionNo``
     - Yes
     - Version number for optimistic locking. Specify the ``versionNo`` of the token retrieved beforehand.

.. note::

   The token string ( ``token`` ) cannot be updated. Even if ``token`` is specified in the request body,
   it will be ignored and the existing value will be retained.

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
        "status": 0
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
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

API Call Using a Token
----------------------

The created token is used for authentication when calling the Search API and other APIs.

.. code-block:: bash

    # Use token as Authorization header
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # Use token as query parameter (requires configuration of api.access.token.request.parameter)
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

References
==========

- :doc:`api-admin-overview` - Admin API Overview (authentication, response format, errors)
- :doc:`../api-search` - Search API
- :doc:`../../admin/accesstoken-guide` - Access Token Management Guide
