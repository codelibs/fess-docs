==========================
Storage API
==========================

Overview
========

Storage API is an API for managing |Fess| object storage.
You can list files and directories in storage and download, delete, and upload files.

Base URL
========

::

    /api/admin/storage

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
     - /upload/{pathId}
     - Upload a file

List Files and Directories
==========================

Returns a list of files and directories under the specified directory.
Specify an encoded path for ``{id}``. If ``{id}`` is omitted, the list of the root directory is retrieved.

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
     - Encoded identifier (used as ``{id}`` for download and delete)
   * - ``path``
     - Parent path
   * - ``name``
     - File name or directory name
   * - ``hashCode``
     - Hash code
   * - ``size``
     - Size (bytes)
   * - ``directory``
     - Whether it is a directory (boolean)
   * - ``lastModified``
     - Last modified date/time (files only)

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

Downloads a file from storage. For ``{id}``, specify the ``id`` obtained from the list.
The response is returned as an ``application/octet-stream`` stream.

Request
-------

::

    GET /api/admin/storage/download/{id}

Response
--------

A binary stream of the file (``Content-Type: application/octet-stream``).

Delete a File
=============

Deletes a file from storage. For ``{id}``, specify the ``id`` obtained from the list.

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

Uploads a file to storage. Send it in ``multipart/form-data`` format.

Request
-------

::

    PUT /api/admin/storage/upload/{pathId}
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
     - Upload destination path (default location if not specified)
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

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
