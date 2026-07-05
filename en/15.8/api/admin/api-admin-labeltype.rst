==========================
LabelType API
==========================

Overview
========

LabelType API is an API for managing label types in |Fess|.
Label types allow you to classify search results based on crawled paths or virtual hosts,
and can be used for label-based filtering on the search screen.

For common specifications regarding authentication, responses (``status`` codes, ``version`` field,
error format, HTTP status codes, etc.), refer to :doc:`api-admin-overview`.
To access this API, you must provide an access token with admin API permission (``admin-api``)
in the ``Authorization: Bearer <access_token>`` header.

Base URL
========

::

    /api/admin/labeltype

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
     - List label types
   * - GET
     - /setting/{id}
     - Get label type
   * - POST
     - /setting
     - Create label type
   * - PUT
     - /setting
     - Update label type
   * - DELETE
     - /setting/{id}
     - Delete label type

List Label Types
================

Request
-------

::

    GET /api/admin/labeltype/settings

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
     - Number of items per page. Default is the ``paging.page.size`` setting value (``25`` by default).
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1). Default is ``1``.
   * - ``name``
     - String
     - No
     - Filter by display name (wildcard search).
   * - ``value``
     - String
     - No
     - Filter by label value (wildcard search).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Each settings object also includes ``createdBy`` / ``createdTime`` / ``updatedBy`` /
   ``updatedTime`` for auditing, and ``versionNo`` for optimistic locking (fields with a
   ``null`` value are omitted). The ``response`` object always includes ``version``
   indicating the product version, but it may be omitted in subsequent examples for brevity.

Get Label Type
==============

Request
-------

::

    GET /api/admin/labeltype/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "permissions": "{role}admin",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

Create Label Type
=================

Request
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest"
    }

Field Descriptions
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Field
     - Type
     - Required
     - Description
   * - ``name``
     - String
     - Yes
     - Label display name (max 100 characters).
   * - ``value``
     - String
     - Yes
     - Label value (used with the ``label`` parameter in searches). Only alphanumeric characters and underscores (``_``) are allowed; must match the regex ``^[a-zA-Z0-9_]+$`` (max 100 characters).
   * - ``includedPaths``
     - String
     - No
     - Regular expressions for paths to be labelled. Separate multiple entries with a newline (``\n``).
   * - ``excludedPaths``
     - String
     - No
     - Regular expressions for paths to exclude from labelling. Separate multiple entries with a newline (``\n``).
   * - ``permissions``
     - String
     - No
     - Roles/groups/users permitted to access (e.g. ``{role}admin``). Separate multiple entries with a newline (``\n``).
   * - ``sortOrder``
     - Integer
     - No
     - Display order (non-negative integer). Defaults to ``0`` if not specified.
   * - ``virtualHost``
     - String
     - No
     - Virtual host (max 1000 characters).

.. note::

   Audit fields such as ``createdBy`` / ``createdTime`` are set automatically on the server side
   and do not need to be specified in the request.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

On successful creation, ``created`` is ``true``.

Update Label Type
=================

Request
-------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest",
      "versionNo": 1
    }

When updating, the following fields are required in addition to the fields used at creation time.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Field
     - Type
     - Required
     - Description
   * - ``id``
     - String
     - Yes
     - The ID of the label type to update.
   * - ``versionNo``
     - Integer
     - Yes
     - Version number for optimistic locking. Specify the ``versionNo`` included in the response when the setting was retrieved. If the specified version does not match the current one, the update will fail.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

On update, ``created`` is ``false``.

Delete Label Type
=================

Request
-------

::

    DELETE /api/admin/labeltype/setting/{id}

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

Create Documentation Label
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

List Label Types
----------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Search with Label
-----------------

.. code-block:: bash

    # Filter by label
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

See Also
========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../api-search` - Search API
- :doc:`../../admin/labeltype-guide` - Label Type Management Guide
