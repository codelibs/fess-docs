==========================
ElevateWord API
==========================

Overview
========

ElevateWord API is an API for managing |Fess| elevate words (search ranking manipulation for specific keywords).
You can place specific documents higher or lower for specific search queries.

Base URL
========

::

    /api/admin/elevateword

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
     - List elevate words
   * - GET
     - /setting/{id}
     - Get elevate word
   * - POST
     - /setting
     - Create elevate word
   * - PUT
     - /setting
     - Update elevate word
   * - DELETE
     - /setting/{id}
     - Delete elevate word

List Elevate Words
==================

Request
-------

::

    GET /api/admin/elevateword/settings
    PUT /api/admin/elevateword/settings

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "",
            "permissions": [],
            "boost": 10.0,
            "targetRole": "",
            "targetLabel": ""
          }
        ],
        "total": 5
      }
    }

Get Elevate Word
================

Request
-------

::

    GET /api/admin/elevateword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "",
          "permissions": [],
          "boost": 10.0,
          "targetRole": "",
          "targetLabel": ""
        }
      }
    }

Create Elevate Word
===================

Request
-------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "",
      "permissions": ["guest"],
      "boost": 15.0,
      "targetRole": "user",
      "targetLabel": "docs"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``suggestWord``
     - Yes
     - Keyword to elevate
   * - ``reading``
     - No
     - Phonetic reading
   * - ``permissions``
     - No
     - Access permission roles
   * - ``boost``
     - No
     - Boost value (default: 1.0)
   * - ``targetRole``
     - No
     - Target role
   * - ``targetLabel``
     - No
     - Target label

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

Update Elevate Word
===================

Request
-------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "",
      "permissions": ["guest", "user"],
      "boost": 20.0,
      "targetRole": "user",
      "targetLabel": "docs",
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

Delete Elevate Word
===================

Request
-------

::

    DELETE /api/admin/elevateword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

Usage Examples
==============

Elevate Product Name
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 20.0,
           "permissions": ["guest"]
         }'

Elevate to Specific Label
-------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 10.0,
           "targetLabel": "technical_docs",
           "permissions": ["guest"]
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-keymatch` - Key Match API
- :doc:`api-admin-boostdoc` - Document Boost API
- :doc:`../../admin/elevateword-guide` - Elevate Word Management Guide

