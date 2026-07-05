==========================
RelatedQuery API
==========================

Overview
========

RelatedQuery API is an API for managing related queries in |Fess|.
For a specific search keyword entered by the user (``term``), you can register and manage
related search keyword suggestions (``queries``). Registered related queries are displayed
as related search suggestions on the search screen.

For details on authentication, the common response format (the ``version`` field and
``status`` codes), pagination, and error responses, refer to :doc:`api-admin-overview`.

Base URL
========

::

    /api/admin/relatedquery

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
     - List related queries
   * - GET
     - /setting/{id}
     - Get related query
   * - POST
     - /setting
     - Create related query
   * - PUT
     - /setting
     - Update related query
   * - DELETE
     - /setting/{id}
     - Delete related query

List Related Queries
====================

Request
-------

::

    GET /api/admin/relatedquery/settings

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
     - Number of items per page (default: 25. Configurable via ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1. Default: 1)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Each setting includes ``versionNo`` (a version number for optimistic locking). ``virtualHost``
   and audit fields (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``) are included
   only when a value is set. A ``virtualHost`` with an empty value is not included in the response.

Get Related Query
=================

Request
-------

::

    GET /api/admin/relatedquery/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

Create Related Query
====================

Request
-------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Field
     - Required
     - Description
   * - ``term``
     - Yes
     - Search keyword (maximum 10,000 characters)
   * - ``queries``
     - Yes
     - Related queries. A newline-separated string with one entry per line (empty lines are ignored. Maximum 10,000 characters)
   * - ``virtualHost``
     - No
     - Virtual host (maximum 1,000 characters)

.. note::

   ``crudMode`` is set automatically on the API side and does not need to be included in the request body.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Update Related Query
====================

Request
-------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
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
     - ID of the related query to update (maximum 1,000 characters)
   * - ``term``
     - Yes
     - Search keyword (maximum 10,000 characters)
   * - ``queries``
     - Yes
     - Related queries. A newline-separated string with one entry per line (empty lines are ignored. Maximum 10,000 characters)
   * - ``virtualHost``
     - No
     - Virtual host (maximum 1,000 characters)
   * - ``versionNo``
     - Yes
     - Version number for optimistic locking. Specify the value included in the response when the setting was retrieved.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Delete Related Query
====================

Request
-------

::

    DELETE /api/admin/relatedquery/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Error Response
==============

When a request fails, ``status`` is set to a non-zero value and ``message`` contains the
error details. For example, a validation error such as a missing required field results in
``status`` being ``1``. For the list of status codes, refer to :doc:`api-admin-overview`.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "..."
      }
    }

Usage Examples
==============

Product Related Queries
-----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

Help Related Queries
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-relatedcontent` - Related Content API
- :doc:`api-admin-suggest` - Suggest Management API
- :doc:`../../admin/relatedquery-guide` - Related Query Management Guide
