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

Authentication
==============

As with other Admin APIs, authentication using an access token is required. The access token must have the ``Radmin-api`` permission (configured via ``api.admin.access.permissions``; the default value is ``Radmin-api``).
Specify the access token in the request header.

::

    Authorization: Bearer <access token>

For details on authentication and how to obtain an access token, see :doc:`api-admin-overview`.

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
The files are returned sorted in ascending order by file name.

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
        "version": "15.8.0",
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

.. note::

   ``version`` is set to the product version of the running |Fess|. The contents and count of ``files``
   vary depending on the log files on the server, so the above is just an example.

Download Log File
=================

Downloads the contents of the specified log file.
For ``{id}``, specify the ``id`` (the file name encoded with Base64 URL encoding) returned by the file list retrieval as-is.
The response is returned as an ``application/octet-stream`` stream.
For security, only names ending with ``.log`` or ``.log.gz`` are accepted, and names containing path manipulation sequences such as ``..`` are rejected.
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
