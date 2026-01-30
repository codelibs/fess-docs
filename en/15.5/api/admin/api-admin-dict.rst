==========================
Dict API
==========================

Overview
========

Dict API is an API for managing |Fess| dictionary files.
You can manage synonym dictionaries, mapping dictionaries, protected word dictionaries, and more.

Base URL
========

::

    /api/admin/dict

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - List dictionaries
   * - GET
     - /{id}
     - Get dictionary content
   * - PUT
     - /{id}
     - Update dictionary content
   * - POST
     - /upload
     - Upload dictionary file

List Dictionaries
=================

Request
-------

::

    GET /api/admin/dict

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dicts": [
          {
            "id": "synonym",
            "name": "Synonym Dictionary",
            "path": "/var/lib/fess/dict/synonym.txt",
            "type": "synonym",
            "updatedAt": "2025-01-29T10:00:00Z"
          },
          {
            "id": "mapping",
            "name": "Mapping Dictionary",
            "path": "/var/lib/fess/dict/mapping.txt",
            "type": "mapping",
            "updatedAt": "2025-01-28T15:30:00Z"
          },
          {
            "id": "protwords",
            "name": "Protected Words Dictionary",
            "path": "/var/lib/fess/dict/protwords.txt",
            "type": "protwords",
            "updatedAt": "2025-01-27T12:00:00Z"
          }
        ],
        "total": 3
      }
    }

Get Dictionary Content
======================

Request
-------

::

    GET /api/admin/dict/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dict": {
          "id": "synonym",
          "name": "Synonym Dictionary",
          "path": "/var/lib/fess/dict/synonym.txt",
          "type": "synonym",
          "content": "search,retrieval,lookup\nFess,fess\nfull-text search,fulltext search",
          "updatedAt": "2025-01-29T10:00:00Z"
        }
      }
    }

Update Dictionary Content
=========================

Request
-------

::

    PUT /api/admin/dict/{id}
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "content": "search,retrieval,lookup,find\nFess,fess\nfull-text search,fulltext search,text search"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``content``
     - Yes
     - Dictionary content (newline separated)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary updated successfully"
      }
    }

Upload Dictionary File
======================

Request
-------

::

    POST /api/admin/dict/upload
    Content-Type: multipart/form-data

Request Body
~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="type"

    synonym
    --boundary
    Content-Disposition: form-data; name="file"; filename="synonym.txt"
    Content-Type: text/plain

    search,retrieval,lookup
    Fess,fess
    --boundary--

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``type``
     - Yes
     - Dictionary type (synonym/mapping/protwords/stopwords)
   * - ``file``
     - Yes
     - Dictionary file

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary uploaded successfully"
      }
    }

Dictionary Types
================

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type
     - Description
   * - ``synonym``
     - Synonym dictionary (expands synonyms during search)
   * - ``mapping``
     - Mapping dictionary (character normalization)
   * - ``protwords``
     - Protected words dictionary (words excluded from stemming)
   * - ``stopwords``
     - Stopwords dictionary (words excluded from indexing)
   * - ``kuromoji``
     - Kuromoji dictionary (Japanese morphological analysis)

Dictionary Format Examples
==========================

Synonym Dictionary
------------------

::

    # Specify synonyms with comma separation
    search,retrieval,lookup,find
    Fess,fess,FESS
    full-text search,fulltext search,text search

Mapping Dictionary
------------------

::

    # before => after
    0 => 0
    1 => 1
    2 => 2

Protected Words Dictionary
--------------------------

::

    # Words to protect from stemming
    running
    searching
    indexing

Usage Examples
==============

List Dictionaries
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Get Synonym Dictionary Content
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN"

Update Synonym Dictionary
-------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "content": "search,retrieval,find\nFess,fess\ndocument,doc,file"
         }'

Upload Dictionary File
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "type=synonym" \
         -F "file=@synonym.txt"

Important Notes
===============

- Index rebuilding may be required after updating dictionaries
- Large dictionary files may affect search performance
- Use UTF-8 encoding for dictionary files

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../../admin/dict-guide` - Dictionary Management Guide
- :doc:`../../config/dict-config` - Dictionary Configuration Guide

