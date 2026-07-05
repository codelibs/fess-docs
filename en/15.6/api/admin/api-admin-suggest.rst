==========================
Suggest API
==========================

Overview
========

Suggest API is an API for managing |Fess| suggest functionality.
You can add, delete, and update suggest words.

Base URL
========

::

    /api/admin/suggest

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
     - List suggest words
   * - GET
     - /setting/{id}
     - Get suggest word
   * - POST
     - /setting
     - Create suggest word
   * - PUT
     - /setting
     - Update suggest word
   * - DELETE
     - /setting/{id}
     - Delete suggest word
   * - DELETE
     - /delete-all
     - Delete all suggest words

List Suggest Words
==================

Request
-------

::

    GET /api/admin/suggest/settings
    PUT /api/admin/suggest/settings

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
            "id": "suggest_id_1",
            "text": "fess",
            "reading": "",
            "fields": ["title", "content"],
            "tags": ["product"],
            "roles": ["guest"],
            "lang": "en",
            "score": 1.0
          }
        ],
        "total": 100
      }
    }

Get Suggest Word
================

Request
-------

::

    GET /api/admin/suggest/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "suggest_id_1",
          "text": "fess",
          "reading": "",
          "fields": ["title", "content"],
          "tags": ["product"],
          "roles": ["guest"],
          "lang": "en",
          "score": 1.0
        }
      }
    }

Create Suggest Word
===================

Request
-------

::

    POST /api/admin/suggest/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "text": "search engine",
      "reading": "",
      "fields": ["title"],
      "tags": ["feature"],
      "roles": ["guest"],
      "lang": "en",
      "score": 1.0
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``text``
     - Yes
     - Suggest text
   * - ``reading``
     - No
     - Phonetic reading
   * - ``fields``
     - No
     - Target fields
   * - ``tags``
     - No
     - Tags
   * - ``roles``
     - No
     - Access permission roles
   * - ``lang``
     - No
     - Language code
   * - ``score``
     - No
     - Score (default: 1.0)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_suggest_id",
        "created": true
      }
    }

Update Suggest Word
===================

Request
-------

::

    PUT /api/admin/suggest/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_suggest_id",
      "text": "search engine",
      "reading": "",
      "fields": ["title", "content"],
      "tags": ["feature", "popular"],
      "roles": ["guest"],
      "lang": "en",
      "score": 2.0,
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_suggest_id",
        "created": false
      }
    }

Delete Suggest Word
===================

Request
-------

::

    DELETE /api/admin/suggest/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_suggest_id",
        "created": false
      }
    }

Delete All Suggest Words
========================

Request
-------

::

    DELETE /api/admin/suggest/delete-all

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "count": 250
      }
    }

Usage Examples
==============

Add Popular Keyword
-------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/suggest/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "getting started",
           "fields": ["title"],
           "tags": ["tutorial"],
           "roles": ["guest"],
           "lang": "en",
           "score": 5.0
         }'

Bulk Delete Suggests
--------------------

.. code-block:: bash

    # Delete all suggests
    curl -X DELETE "http://localhost:8080/api/admin/suggest/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-badword` - Bad Word API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/suggest-guide` - Suggest Management Guide

