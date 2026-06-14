==========================
Log API
==========================

Overview
========

The Log API is an API for referencing and downloading the log files of |Fess|.
It allows you to retrieve a list of log files output on the server and download individual log files.

Base URL
========

::

    /api/admin/log

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /files
     - Retrieve log file list
   * - GET
     - /file/{id}
     - Download log file

Retrieve Log File List
======================

Returns a list of log files (``.log`` and ``.log.gz``) that exist in the server's log output directory.

Request
-------

::

    GET /api/admin/log/files

Response
--------

``files`` contains an array of objects representing the information of each log file, and ``total`` contains the count.
Each object has the following fields.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - The file name encoded with Base64 URL encoding (used for ``{id}`` when downloading)
   * - ``name``
     - Log file name
   * - ``lastModified``
     - Last modified date and time

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

Download Log File
=================

Downloads the contents of the specified log file.
For ``{id}``, specify the ``id`` (the file name encoded with Base64) obtained from the file list retrieval.
The response is returned as an ``application/octet-stream`` stream.
If you specify a non-existent file name or a name that is not permitted as a log file, an empty response is returned.

Request
-------

::

    GET /api/admin/log/file/{id}

Response
--------

A binary stream of the log file (``Content-Type: application/octet-stream``).

Usage Examples
==============

Retrieve Log File List
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

Download Log File
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-backup` - Backup API
