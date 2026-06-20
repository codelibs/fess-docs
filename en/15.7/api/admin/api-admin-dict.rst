==========================
Dict API
==========================

Overview
========

Dict API is an API for managing |Fess| dictionaries.
The root endpoint can retrieve the list of available dictionaries.
Reading, creating, updating, and deleting individual dictionary items, as well as uploading and downloading dictionary files,
are performed via the sub-endpoints for each dictionary type (synonym, kuromoji, mapping, protwords, stopwords, stemmeroverride).

Base URL
========

::

    /api/admin/dict

Endpoint List
=============

Dictionary Root
---------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - List dictionaries

Endpoints per Dictionary Type
-----------------------------

For ``{type}``, specify one of ``synonym``, ``kuromoji``, ``mapping``, ``protwords``, ``stopwords``, or ``stemmeroverride``.
These values match the value of the ``type`` field included in the dictionary list response.
``{dictId}`` is the ID of the dictionary obtained from the dictionary list.

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Method
     - Path
     - Description
   * - GET
     - /{type}/settings/{dictId}
     - List dictionary items
   * - GET
     - /{type}/setting/{dictId}/{id}
     - Get dictionary item
   * - POST
     - /{type}/setting/{dictId}
     - Create dictionary item
   * - PUT
     - /{type}/setting/{dictId}
     - Update dictionary item
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - Delete dictionary item
   * - PUT
     - /{type}/upload/{dictId}
     - Upload dictionary file
   * - GET
     - /{type}/download/{dictId}
     - Download dictionary file

List Dictionaries
=================

Retrieve the list of available dictionary files.

Request
-------

::

    GET /api/admin/dict

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
          }
        ],
        "total": 2
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``settings[].id``
     - Dictionary ID (used as ``{dictId}`` in individual dictionary operations)
   * - ``settings[].type``
     - Dictionary type
   * - ``settings[].path``
     - Path of the dictionary file
   * - ``settings[].timestamp``
     - Update date/time of the dictionary file
   * - ``total``
     - Total number of dictionary files

List Dictionary Items
=====================

List the items in the specified dictionary.

Request
-------

::

    GET /api/admin/dict/{type}/settings/{dictId}

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``dictId``
     - String
     - Yes
     - Dictionary ID (path parameter)
   * - ``size``
     - Integer
     - No
     - Number of items per page (default: 25)
   * - ``page``
     - Integer
     - No
     - Page number (starts at 1, default: 1)

Response
--------

The fields of each item in the ``settings`` array of the response differ by dictionary type (see "Item Fields per Dictionary Type" below).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "検索,サーチ",
            "outputs": "検索,サーチ,リサーチ"
          }
        ],
        "total": 1
      }
    }

The above is an example of the ``synonym`` dictionary.

Get Dictionary Item
===================

Retrieve a specific item in the dictionary.

Request
-------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``dictId``
     - String
     - Yes
     - Dictionary ID (path parameter)
   * - ``id``
     - Long
     - Yes
     - Item ID (path parameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

Create Dictionary Item
======================

Create a new item in the dictionary.

Request
-------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Request Body (synonym example)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

Update Dictionary Item
======================

Update an existing item in the dictionary.

Request
-------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Request Body (synonym example)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Delete Dictionary Item
======================

Delete an item in the dictionary.

Request
-------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``dictId``
     - String
     - Yes
     - Dictionary ID (path parameter)
   * - ``id``
     - Long
     - Yes
     - Item ID (path parameter)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Upload Dictionary File
======================

Upload and replace the entire dictionary file.

Request
-------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

The name of the file field differs by dictionary type (see "Item Fields per Dictionary Type" below).

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Download Dictionary File
========================

Download the dictionary file.

Request
-------

::

    GET /api/admin/dict/{type}/download/{dictId}

The response is the binary of the dictionary file (``application/octet-stream``).

Item Fields per Dictionary Type
===============================

The fields of the request body and response for creating and updating dictionary items differ by dictionary type.
``id`` (item ID) and ``dictId`` (dictionary ID) are commonly included in the response.

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - Type
     - Item Fields
     - Upload File Field
   * - ``synonym``
     - ``inputs`` (required), ``outputs`` (required)
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` (required), ``segmentation`` (required), ``reading`` (required), ``pos`` (required)
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` (required), ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` (required)
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` (required)
     - ``stopwordsFile``
   * - ``stemmeroverride``
     - ``input`` (required), ``output`` (required)
     - ``stemmerOverrideFile``

Usage Examples
==============

List Dictionaries
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

List Synonym Dictionary Items
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

Add an Item to the Synonym Dictionary
-------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

Upload a Synonym Dictionary File
--------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

Download a Synonym Dictionary File
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../../admin/dict-guide` - Dictionary Management Guide
