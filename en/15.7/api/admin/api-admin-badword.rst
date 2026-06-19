==========================
BadWord API
==========================

Overview
========

BadWord API is an API for managing |Fess| bad words (excluding inappropriate suggestion words).
You can configure keywords that should not appear in the suggest feature.

Base URL
========

::

    /api/admin/badword

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
     - List bad words
   * - GET
     - /setting/{id}
     - Get bad word
   * - POST
     - /setting
     - Create bad word
   * - PUT
     - /setting
     - Update bad word
   * - DELETE
     - /setting/{id}
     - Delete bad word
   * - PUT
     - /upload
     - Upload bad word CSV
   * - GET
     - /download
     - Download bad word CSV

List Bad Words
==============

Request
-------

::

    GET /api/admin/badword/settings

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
     - Page number (starts from 1, default: 1)
   * - ``id``
     - String
     - No
     - Filter to only the bad word with the specified ID

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

Get Bad Word
============

Request
-------

::

    GET /api/admin/badword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

Create Bad Word
===============

Request
-------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
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
     - Keyword to exclude (cannot contain whitespace characters)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

Update Bad Word
===============

Request
-------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

Delete Bad Word
===============

Request
-------

::

    DELETE /api/admin/badword/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

Upload Bad Word CSV
===================

Bulk-registers bad words from a CSV file. The file is sent as ``multipart/form-data``. The import is executed asynchronously on the server side.

Request
-------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``badWordFile``
     - Yes
     - Bad word CSV file to upload

CSV Format
~~~~~~~~~~

- The first line is skipped as a header row (the column name is arbitrary; ``BadWord`` is written on download).
- From the second line onward, write one bad word per line as the ``suggestWord``.
- Lines whose value is blank are ignored.
- Prefix a word with ``--`` to delete it (e.g., ``--spam`` deletes ``spam``).
- Specifying an already-registered word is treated as an update (the updater and update time are reset).

.. note::

   Because the import runs asynchronously on the server side, a ``status: 0`` response
   indicates that the request was accepted, not that the import has completed.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Download Bad Word CSV
=====================

Downloads the registered bad words as a CSV file (``badword.csv``). The response is an ``application/octet-stream`` stream.
The CSV has a ``BadWord`` header row on the first line, followed by one registered bad word per line.

Request
-------

::

    GET /api/admin/badword/download

Usage Examples
==============

Exclude Spam Keyword
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

Upload CSV File
---------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

Download CSV File
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-suggest` - Suggest Management API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/badword-guide` - Bad Word Management Guide

