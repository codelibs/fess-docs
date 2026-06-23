==========================
Storage API
==========================

Overview
========

The Storage API is an API for managing |Fess| object storage.
You can list files and directories in storage, and download, delete, and upload files.

Base URL
========

::

    /api/admin/storage

Authentication
==============

All endpoints of the Admin API, including the Storage API, require authentication using an access token.
Specify the access token in the ``Authorization`` header of the request.

::

    Authorization: Bearer <access_token>

For details on how to obtain an access token and the required permissions (``admin-api`` role by default),
see :doc:`api-admin-overview`.

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /list/{id}
     - List files and directories
   * - GET
     - /download/{id}
     - Download a file
   * - DELETE
     - /delete/{id}
     - Delete a file
   * - PUT
     - /upload
     - Upload a file

List Files and Directories
==========================

Returns a list of files and directories under the specified directory.
Specify the ``id`` of a directory obtained from a previous list response for ``{id}``. If ``{id}`` is omitted, the list of the root directory is retrieved.

Request
-------

::

    GET /api/admin/storage/list/{id}

Response
--------

``items`` stores an array of objects representing file and directory information (directories first, then files).
Each object has the following fields.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Encoded identifier. A URL-safe Base64 encoding of the object path, used as ``{id}`` for download and delete operations.
   * - ``path``
     - Path of the parent directory
   * - ``name``
     - File name or directory name
   * - ``hashCode``
     - A hash value used internally (not a stable value representing the content of the object)
   * - ``size``
     - Size (bytes)
   * - ``directory``
     - Whether the entry is a directory (boolean)
   * - ``lastModified``
     - Last modified date and time (ISO 8601 format; included only for files)

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

Download a File
===============

Downloads a file from storage. Specify the ``id`` obtained from the list for ``{id}``.
The response is returned as an ``application/octet-stream`` stream.

Request
-------

::

    GET /api/admin/storage/download/{id}

Response
--------

A binary stream of the file (``Content-Type: application/octet-stream``).

.. note::

   The response of this API does not include a ``Content-Disposition`` header.
   Specify the filename to save on the client side (use the ``-o`` option with cURL).

Delete a File
=============

Deletes a file from storage. Specify the ``id`` obtained from the list for ``{id}``.

Request
-------

::

    DELETE /api/admin/storage/delete/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Upload a File
=============

Uploads a file to storage. Send the request in ``multipart/form-data`` format.
The upload destination directory is specified via the form field ``path``, not as a URL path parameter.

Request
-------

::

    PUT /api/admin/storage/upload
    Content-Type: multipart/form-data

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``path``
     - No
     - Directory path for the upload destination (no leading or trailing slashes). If omitted, the file is stored at the root (directly under the bucket).
   * - ``file``
     - Yes
     - File to upload

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Errors
======

Each endpoint returns a response with a ``status`` value other than 0 (``1`` for validation errors) when processing fails.
The ``message`` field in the response body contains the error details. For information on status values and HTTP status codes, see :doc:`api-admin-overview`.

The main error cases are as follows.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Main cases where an error occurs
   * - List Files and Directories
     - When the number of retrieved items exceeds the limit
   * - Download a File
     - When ``id`` is invalid, or when the download fails
   * - Delete a File
     - When ``id`` is invalid, or when the deletion fails
   * - Upload a File
     - When ``file`` is not specified, or when the upload fails

Usage Examples
==============

List the Root Directory
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

Download a File
---------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

Delete a File
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

Upload a File
-------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
