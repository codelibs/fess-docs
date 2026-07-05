==================
Admin API Overview
==================

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
4. Enter a token name and set the permissions to grant to the token in the "Permissions" field (to use the Admin API, enter ``{role}admin-api``)
5. Click "Create" to obtain the token

Using the Token
---------------

Include the access token in the request header:

::

    Authorization: Bearer <access_token>

You can also omit ``Bearer`` and specify only the token:

::

    Authorization: <access_token>

Specifying the token as a query parameter is also possible, but it is disabled by default.
If you set a parameter name in ``api.access.token.request.parameter`` in ``fess_config.properties``,
you can pass the token using that name (the default value is empty, so only specification via the
header is enabled). For example, if you set ``api.access.token.request.parameter=token``:

::

    ?token=<access_token>

cURL Example
~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Required Permissions
--------------------

Access to the Admin API is controlled by a single permission set, not per function. To use any
endpoint of the Admin API, the access token must be granted one of the permissions configured in
``api.admin.access.permissions`` in ``fess_config.properties``.

The default value is ``Radmin-api``, which is the encoded form of the role ``admin-api``
(the leading ``R`` is the value of ``role.search.role.prefix``). When creating an access token,
if you enter ``{role}admin-api`` in the permissions field, it is stored internally as ``Radmin-api``.

.. note::

   There are no per-resource permissions (such as ``admin-scheduler`` or ``admin-user``) and no
   wildcard (``admin-*``). A token that has the configured permission can access all Admin API
   endpoints. If you want to change the permissions that grant access, change the value of
   ``api.admin.access.permissions``.

Common Patterns
===============

Resources that have settings (webconfig, user, role, etc.) follow the common CRUD pattern below.
However, some resources (systeminfo, stats, storage, plugin, log, backup, documents, suggest, dict root, etc.)
have their own endpoint structure that differs from this common pattern, so refer to each resource's page.

List Retrieval (GET /settings)
------------------------------

Retrieves a list of settings.

Request
~~~~~~~

::

    GET /api/admin/<resource>/settings

Parameters (pagination):

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - ``size``
     - Integer
     - Number of items per page (default: 25. Configurable via ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - Page number (starts from 1. Default: 1. Values of 0 or less are treated as 1)

Response
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   The ``response`` object of every response always contains ``version`` (e.g., ``"15.8.0"``)
   indicating the product version. It may be omitted in the following examples for brevity.

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

The format of the delete response differs per resource (action). Many resources return
only ``status``.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

For some resources, the delete result is returned as an ``ApiUpdateResponse``, with the
``id`` of the deleted setting and ``created`` (``false`` on deletion).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

In addition, for resources that return an ``ApiDeleteResponse``, ``count`` (default ``1``)
indicating the number of deleted items may be added. For the actual format, refer to each
resource's page.

Response Format
===============

Every response is wrapped in a ``response`` object that always contains ``version``
indicating the product version, and ``status`` indicating the processing result.

The values of ``status`` are as follows.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Value
     - Description
   * - ``0``
     - OK (success)
   * - ``1``
     - BAD_REQUEST (invalid request)
   * - ``2``
     - SYSTEM_ERROR (system error)
   * - ``3``
     - UNAUTHORIZED (authentication error)
   * - ``9``
     - FAILED (processing failed)

Success Response
----------------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` indicates success.

Error Response
--------------

On error, a non-zero value is set in ``status``, and ``message`` contains the error
message.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

HTTP Status Codes
-----------------

In most cases, the Admin API returns HTTP status ``200``, and the processing result is
expressed by the ``status`` field in the response body. Therefore, determine success or
failure by the value of ``status`` in the body, not by the HTTP status code.

The HTTP status codes that are actually returned are as follows.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Normal response. In addition to success (``status: 0``), most errors are also returned
       with this code. For example, when the access token is missing or invalid, or when
       permissions are insufficient, ``status: 3`` is returned, and a system error returns
       ``status: 2``; both are returned with HTTP ``200``.
   * - 400
     - A request parameter validation error. The ``status`` in the response body is ``1``.
       Attempting to retrieve a non-existent resource is also returned with this code.
   * - 401
     - When an exception related to login authentication occurs. The ``status`` in the response
       body is ``3``. Note that when the access token is missing or invalid, ``status: 3`` is
       returned with HTTP ``200``, not this code.

.. note::

   The Admin API does not return HTTP status codes such as ``403``, ``404``, or ``500``.
   Insufficient permissions and the non-existence of a resource are also indicated by the
   ``status`` contained in the response body of an HTTP ``200`` or ``400`` response.

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

.. note::

   In addition, the following resources related to authentication information and crawl control are also
   provided as APIs (individual pages are not yet available): ``webauth`` (Web authentication),
   ``fileauth`` (File authentication), ``reqheader`` (Request headers), ``pathmap`` (Path mapping),
   ``duplicatehost`` (Duplicate host), ``searchlist`` (search/document list operations).

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
     - Bad words
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
   * - :doc:`api-admin-searchlist`
     - Document search and management
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
           "userAgent": "Mozilla/5.0 (compatible; Fess)",
           "numOfThread": 1,
           "intervalTime": 1000,
           "boost": 1.0,
           "maxAccessCount": 1000,
           "depth": 3,
           "sortOrder": 1,
           "available": "true"
         }'

.. note::

   When creating a Web crawl configuration, ``name``, ``urls``, ``userAgent``, ``numOfThread``,
   ``intervalTime``, ``boost``, ``available``, and ``sortOrder`` are required. Omitting any of
   these results in a validation error (``status: 1``). Specify ``available`` as a string, setting
   it to ``"true"`` or ``"false"``.

Start a Scheduled Job
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

List Users
----------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`../api-overview` - API Overview
- :doc:`../../admin/accesstoken-guide` - Access Token Management Guide
