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
   * - GET/PUT
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

List Bad Words
==============

Request
-------

::

    GET /api/admin/badword/settings
    PUT /api/admin/badword/settings

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
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word",
            "targetRole": "",
            "targetLabel": ""
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
          "suggestWord": "inappropriate_word",
          "targetRole": "",
          "targetLabel": ""
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
      "suggestWord": "spam_keyword",
      "targetRole": "guest",
      "targetLabel": ""
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
     - Keyword to exclude
   * - ``targetRole``
     - No
     - Target role (empty = all roles)
   * - ``targetLabel``
     - No
     - Target label (empty = all labels)

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
      "targetRole": "guest",
      "targetLabel": "",
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

Usage Examples
==============

Exclude Spam Keyword
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam",
           "targetRole": "",
           "targetLabel": ""
         }'

Bad Word for Specific Role
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "internal",
           "targetRole": "guest",
           "targetLabel": ""
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-suggest` - Suggest Management API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/badword-guide` - Bad Word Management Guide

