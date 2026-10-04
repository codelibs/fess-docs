==========================
KeyMatch API
==========================

Overview
========

KeyMatch API is an API for managing |Fess| key match settings (linking search keywords to results).
You can display specific documents at the top for specific keywords.

Base URL
========

::

    /api/admin/keymatch

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
     - List key matches
   * - GET
     - /setting/{id}
     - Get key match
   * - POST
     - /setting
     - Create key match
   * - PUT
     - /setting
     - Update key match
   * - DELETE
     - /setting/{id}
     - Delete key match

List Key Matches
================

Request
-------

::

    GET /api/admin/keymatch/settings

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
     - Number of items per page (default: 25; the value of ``paging.page.size``)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1, default: 1)
   * - ``term``
     - String
     - No
     - Filter by search keyword (wildcard match)
   * - ``query``
     - String
     - No
     - Filter by match condition query (wildcard match)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "max_size": 10,
            "boost": 10.0,
            "version_no": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``total`` contains the total number of records matching the filter conditions (not the count of items on the current page).
   In addition to the fields above, each settings object may include ``virtual_host``,
   ``created_by``, ``created_time``, ``updated_by``, and ``updated_time`` when values are set.

Get Key Match
=============

Request
-------

::

    GET /api/admin/keymatch/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "max_size": 10,
          "boost": 10.0,
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   ``version_no`` is the version number used for optimistic locking. When updating a key match, include the
   ``version_no`` obtained from this response in the request body. An error is returned if the specified ID does not exist.

Create Key Match
================

Request
-------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "max_size": 5,
      "boost": 20.0
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Field
     - Type
     - Required
     - Description
   * - ``term``
     - String
     - Yes
     - Search keyword (maximum 100 characters)
   * - ``query``
     - String
     - Yes
     - Match condition query (maximum length follows the value of ``form.admin.max.input.size``)
   * - ``max_size``
     - Integer
     - Yes
     - Maximum display count (integer of 0 or greater; form initial value: 10)
   * - ``boost``
     - Float
     - Yes
     - Boost value (form initial value: 100.0)
   * - ``virtual_host``
     - String
     - No
     - Virtual host name (maximum 1000 characters; specify when switching key matches per virtual host)

.. note::

   ``max_size`` and ``boost`` are required when using the API. The initial values are those shown in the admin console form and
   are not applied via the API. Omitting them results in a validation error.
   Note that ``created_by`` and ``created_time`` are overwritten by the server even if specified in the request.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

Update Key Match
================

Request
-------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "max_size": 10,
      "boost": 15.0,
      "version_no": 1
    }

Field Description
~~~~~~~~~~~~~~~~~

In addition to the fields used for creation (``term``, ``query``, ``max_size``, ``boost``, ``virtual_host``),
specify the following fields.

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Field
     - Type
     - Required
     - Description
   * - ``id``
     - String
     - Yes
     - ID of the key match to update (maximum 1000 characters)
   * - ``version_no``
     - Integer
     - Yes
     - Version number for optimistic locking; specify the value obtained when retrieving the record

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

Delete Key Match
================

Request
-------

::

    DELETE /api/admin/keymatch/setting/{id}

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

Create Product Page Key Match
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "max_size": 10,
           "boost": 15.0
         }'

Support Page Key Match
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "max_size": 5,
           "boost": 20.0
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/keymatch-guide` - Key Match Management Guide
