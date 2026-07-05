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
   * - GET/PUT
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
    PUT /api/admin/keymatch/settings

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
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

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
          "maxSize": 10,
          "boost": 10.0
        }
      }
    }

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
      "maxSize": 5,
      "boost": 20.0
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``term``
     - Yes
     - Search keyword
   * - ``query``
     - Yes
     - Match condition query
   * - ``maxSize``
     - No
     - Maximum display count (default: 10)
   * - ``boost``
     - No
     - Boost value (default: 1.0)

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
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_keymatch_id",
        "created": false
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
           "maxSize": 10,
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
           "maxSize": 5,
           "boost": 20.0
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/keymatch-guide` - Key Match Management Guide

