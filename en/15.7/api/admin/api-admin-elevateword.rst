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
   * - GET
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
   * - PUT
     - /upload
     - Upload elevate word CSV
   * - GET
     - /download
     - Download elevate word CSV

List Elevate Words
==================

Request
-------

::

    GET /api/admin/elevateword/settings

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
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
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
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
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

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
     - Access permissions (one entry per line, newline-separated string. Form default value: default display permissions for search)
   * - ``boost``
     - Yes
     - Boost value (form default value: 100.0)
   * - ``labelTypeIds``
     - No
     - Target label IDs (array of strings)

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
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
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

Upload Elevate Word CSV
=======================

Bulk-registers elevate words from a CSV file. The file is sent as ``multipart/form-data``. The import is executed asynchronously on the server side.

Request
-------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``elevateWordFile``
     - Yes
     - Elevate word CSV file to upload

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Download Elevate Word CSV
=========================

Downloads the registered elevate words as a CSV file (``elevate.csv``). The response is an ``application/octet-stream`` stream.

Request
-------

::

    GET /api/admin/elevateword/download

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
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

Elevate to Specific Label
-------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

Upload CSV File
---------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

Download CSV File
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-keymatch` - Key Match API
- :doc:`api-admin-boostdoc` - Document Boost API
- :doc:`../../admin/elevateword-guide` - Elevate Word Management Guide

