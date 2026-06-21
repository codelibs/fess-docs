==========================
RelatedContent API
==========================

Overview
========

RelatedContent API is an API for managing |Fess| related content.
You can display custom content related to specific keywords.

Base URL
========

::

    /api/admin/relatedcontent

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
     - List related content
   * - GET
     - /setting/{id}
     - Get related content
   * - POST
     - /setting
     - Create related content
   * - PUT
     - /setting
     - Update related content
   * - DELETE
     - /setting/{id}
     - Delete related content

List Related Content
====================

Request
-------

::

    GET /api/admin/relatedcontent/settings

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
     - Number of items per page (default: 25; configurable via ``paging.page.size`` in ``fess_config.properties``)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1, default: 1; values of 0 or less are treated as 1)
   * - ``term``
     - String
     - No
     - Filter by search keyword (wildcard search)
   * - ``content``
     - String
     - No
     - Filter by content body (wildcard search)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Each element of ``settings`` and the ``setting`` object returned by the get
   endpoint contain the fields of the stored entity as-is. In addition to
   ``term``, ``content``, ``sortOrder``, and ``virtualHost``, the audit fields
   ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` and the
   optimistic-locking field ``versionNo`` are also returned. ``createdTime`` and
   ``updatedTime`` are expressed as milliseconds since the epoch (numbers). Fields
   that are not set (null) are omitted from the response. In addition, the
   ``response`` object of every response always includes ``version``, which
   indicates the product version (see :doc:`api-admin-overview` for details).

Get Related Content
===================

Request
-------

::

    GET /api/admin/relatedcontent/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   The ``versionNo`` required when updating (PUT) is the value included in this
   get response.

Create Related Content
======================

Request
-------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``term``
     - Yes
     - Search keyword (max 10000 characters)
   * - ``content``
     - Yes
     - HTML content to display (max 10000 characters)
   * - ``sortOrder``
     - No
     - Display order (integer between 0 and 2147483647)
   * - ``virtualHost``
     - No
     - Virtual host (max 1000 characters)

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Update Related Content
======================

Request
-------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Field
     - Required
     - Description
   * - ``id``
     - Yes
     - ID of the related content to update (max 1000 characters)
   * - ``term``
     - Yes
     - Search keyword (max 10000 characters)
   * - ``content``
     - Yes
     - HTML content to display (max 10000 characters)
   * - ``sortOrder``
     - No
     - Display order (integer between 0 and 2147483647)
   * - ``virtualHost``
     - No
     - Virtual host (max 1000 characters)
   * - ``versionNo``
     - Yes
     - Version number for optimistic locking. Specify the value included in the response of ``setting/{id}``.

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   Audit fields such as ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` and ``crudMode`` are ignored even if included in the request
   body, because they are set automatically on the server side. You do not need
   to specify them when creating or updating.

Delete Related Content
======================

Request
-------

::

    DELETE /api/admin/relatedcontent/setting/{id}

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

Product Information Related Content
-----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

Support Information Related Content
-----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-relatedquery` - Related Query API
- :doc:`../../admin/relatedcontent-guide` - Related Content Management Guide
