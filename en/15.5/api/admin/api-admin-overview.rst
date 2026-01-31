==========================
Admin API Overview
==========================

Overview
========

|Fess| Admin API is a RESTful API for programmatic access to administrative functions.
You can perform most operations available in the admin console via API, including crawl configuration, user management, and scheduler control.

Using this API, you can automate |Fess| configuration and integrate with external systems.

Base URL
========

The Admin API base URL follows this format:

::

    http://<Server Name>/api/admin/

For example, in a local environment:

::

    http://localhost:8080/api/admin/

Authentication
==============

Access to the Admin API requires authentication using an access token.

Obtaining an Access Token
-------------------------

1. Log in to the admin console
2. Navigate to "System" -> "Access Token"
3. Click "Create New"
4. Enter a token name and select required permissions
5. Click "Create" to obtain the token

Using the Token
---------------

Include the access token in the request header:

::

    Authorization: Bearer <access_token>

Or specify it as a query parameter:

::

    ?token=<access_token>

cURL Example
~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Required Permissions
--------------------

To use the Admin API, the token requires the following permissions:

- ``admin-*`` - Access to all administrative functions
- ``admin-scheduler`` - Scheduler management only
- ``admin-user`` - User management only
- Other function-specific permissions

Common Patterns
===============

List Retrieval (GET/PUT /settings)
----------------------------------

Retrieves a list of settings.

Request
~~~~~~~

::

    GET /api/admin/<resource>/settings
    PUT /api/admin/<resource>/settings

Parameters (pagination):

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - ``size``
     - Integer
     - Number of items per page (default: 20)
   * - ``page``
     - Integer
     - Page number (starts from 0)

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

Single Setting Retrieval (GET /setting/{id})
--------------------------------------------

Retrieves a single setting by ID.

Request
~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

Create New (POST /setting)
--------------------------

Creates a new setting.

Request
~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

Update (PUT /setting)
---------------------

Updates an existing setting.

Request
~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

Delete (DELETE /setting/{id})
-----------------------------

Deletes a setting.

Request
~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

Response Format
===============

Success Response
----------------

.. code-block:: json

    {
      "response": {
        "status": 0,
        ...
      }
    }

``status: 0`` indicates success.

Error Response
--------------

.. code-block:: json

    {
      "response": {
        "status": 1,
        "errors": [
          {"code": "errors.failed_to_create", "args": ["...", "..."]}
        ]
      }
    }

HTTP Status Codes
-----------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Request successful
   * - 400
     - Invalid request parameters
   * - 401
     - Authentication required (token missing or invalid)
   * - 403
     - Access denied
   * - 404
     - Resource not found
   * - 500
     - Internal server error

Available APIs
==============

|Fess| provides the following Admin APIs.

Crawl Configuration
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-webconfig`
     - Web crawl configuration
   * - :doc:`api-admin-fileconfig`
     - File crawl configuration
   * - :doc:`api-admin-dataconfig`
     - Data store configuration

Index Management
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-documents`
     - Document bulk operations
   * - :doc:`api-admin-crawlinginfo`
     - Crawl information
   * - :doc:`api-admin-failureurl`
     - Failure URL management
   * - :doc:`api-admin-backup`
     - Backup/Restore

Scheduler
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-scheduler`
     - Job scheduling
   * - :doc:`api-admin-joblog`
     - Job log retrieval

User & Permission Management
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-user`
     - User management
   * - :doc:`api-admin-role`
     - Role management
   * - :doc:`api-admin-group`
     - Group management
   * - :doc:`api-admin-accesstoken`
     - API token management

Search Tuning
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-labeltype`
     - Label types
   * - :doc:`api-admin-keymatch`
     - Key match
   * - :doc:`api-admin-boostdoc`
     - Document boost
   * - :doc:`api-admin-elevateword`
     - Elevate word
   * - :doc:`api-admin-badword`
     - Bad word (excluded suggestions)
   * - :doc:`api-admin-relatedcontent`
     - Related content
   * - :doc:`api-admin-relatedquery`
     - Related query
   * - :doc:`api-admin-suggest`
     - Suggest management

System
------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-general`
     - General settings
   * - :doc:`api-admin-systeminfo`
     - System information
   * - :doc:`api-admin-stats`
     - System statistics
   * - :doc:`api-admin-log`
     - Log retrieval
   * - :doc:`api-admin-storage`
     - Storage management
   * - :doc:`api-admin-plugin`
     - Plugin management

Dictionary
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-dict`
     - Dictionary management (synonyms, stop words, etc.)

Usage Examples
==============

Create Web Crawl Configuration
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

Start a Scheduled Job
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

List Users
----------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`../api-overview` - API Overview
- :doc:`../../admin/accesstoken-guide` - Access Token Management Guide

