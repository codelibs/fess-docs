==========================
BoostDoc API
==========================

Overview
========

BoostDoc API is an API for managing |Fess| document boost settings.
By configuring document boosts, you can raise the score of documents matching specific conditions
and make them appear higher in search results.

Boosts are applied to each document at index time (during crawling).
Both the condition (``url_expr``) and the boost value (``boost_expr``) are evaluated using the scripting
engine specified in the ``script_type`` field. ``script_type`` can be ``javascript`` or ``groovy`` (which
requires the ``fess-script-groovy`` plugin). The admin console's create screen prefills ``script_type``
with ``javascript``, but if this API's request body omits ``script_type``, it is not auto-filled and the
expressions are evaluated as Groovy.
Multiple rules are evaluated in ascending order of ``sort_order``, and only the boost value of the first
matching rule is applied (once a matching rule is found, subsequent rules are not evaluated).

.. note::

   In the admin console, ``url_expr`` is displayed as "Condition", ``boost_expr`` as "Boost Expression", and
   ``script_type`` as "Script Type". ``script_type`` appears only in the create/update/detail (list and single)
   request bodies and responses, not in the list filter parameters (``url_expr``, ``boost_expr``).
   For details on configuration items, refer to :doc:`../../admin/boostdoc-guide`.

Base URL
========

::

    /api/admin/boostdoc

Authentication
==============

To use this API, an access token with the ``Radmin-api`` permission is required.
For how to obtain and specify an access token, refer to :doc:`api-admin-overview`.

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
     - List document boosts
   * - GET
     - /setting/{id}
     - Get document boost
   * - POST
     - /setting
     - Create document boost
   * - PUT
     - /setting
     - Update document boost
   * - DELETE
     - /setting/{id}
     - Delete document boost

List Document Boosts
====================

Request
-------

::

    GET /api/admin/boostdoc/settings

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
     - Number of items per page (default: 25)
   * - ``page``
     - Integer
     - No
     - Page number (starts from 1; default: 1)
   * - ``url_expr``
     - String
     - No
     - Filter by condition expression (partial match)
   * - ``boost_expr``
     - String
     - No
     - Filter by boost expression (partial match)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "url_expr": "url.startsWith(\"https://docs.example.com/\")",
            "boost_expr": "3.0",
            "script_type": "javascript",
            "sort_order": 1,
            "version_no": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   In addition to the fields shown above, each setting object in the response also includes
   creation/update metadata (``created_by``, ``created_time``, ``updated_by``, ``updated_time``).
   ``version_no`` is required when updating (PUT), so retrieve its current value via the get or list API before updating.

Get Document Boost
==================

Request
-------

::

    GET /api/admin/boostdoc/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "url_expr": "url.startsWith(\"https://docs.example.com/\")",
          "boost_expr": "3.0",
          "script_type": "javascript",
          "sort_order": 1,
          "version_no": 1
        }
      }
    }

Create Document Boost
=====================

Request
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "url_expr": "url.startsWith(\"https://important.example.com/\")",
      "boost_expr": "5.0",
      "script_type": "javascript",
      "sort_order": 0
    }

Field Descriptions
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``url_expr``
     - Yes
     - Condition expression. A script expression that determines whether a document should be boosted, returning ``Boolean``. Corresponds to "Condition" in the admin console (maximum 10,000 characters).
   * - ``boost_expr``
     - Yes
     - Boost expression. A script expression that returns the boost value (numeric). A fixed value such as ``3.0`` can also be specified. Corresponds to "Boost Expression" in the admin console (maximum 10,000 characters).
   * - ``script_type``
     - No
     - The scripting engine used to evaluate ``url_expr`` and ``boost_expr``. Either ``javascript`` or ``groovy`` (which requires the ``fess-script-groovy`` plugin). Corresponds to "Script Type" in the admin console (maximum 100 characters). If omitted, the expressions are evaluated as Groovy.
   * - ``sort_order``
     - Yes
     - Evaluation order. Rules are evaluated in ascending order, and the boost value of the first matching rule is applied (form default value: 0; must be an integer of 0 or greater).

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Update Document Boost
=====================

Request
-------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "url_expr": "url.startsWith(\"https://important.example.com/\")",
      "boost_expr": "10.0",
      "script_type": "javascript",
      "sort_order": 0,
      "version_no": 1
    }

For updates, in addition to the fields used when creating, ``id`` (the ID of the target rule, up to 1000 characters) and ``version_no`` (the version number for optimistic locking) are required.
Specify the current version number from the get or list API response for ``version_no``. The update fails if the version number does not match.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Delete Document Boost
=====================

Request
-------

::

    DELETE /api/admin/boostdoc/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Condition and Boost Expressions
================================

Both ``url_expr`` (condition) and ``boost_expr`` (boost expression) are evaluated using the scripting engine
specified by ``script_type`` (default: Groovy; only the admin console's create screen prefills
``javascript``).
Inside an expression, the field values of the document being indexed can be referenced as variables by field name.

- ``url_expr`` must return ``Boolean`` (e.g., ``url.startsWith("https://docs.example.com/")``). A plain regular expression string (e.g., ``.*docs\.example\.com.*``) does not return ``Boolean`` as a script expression and therefore does not function as a condition. To use regular expressions, use ``String#matches`` (available with the same notation in both Groovy and JavaScript).
- ``boost_expr`` must return a numeric value. The result is converted to ``float``, and the boost is applied only when the value is greater than 0.

.. note::

   Key field variables available inside expressions: ``url``, ``title``, ``content``, ``content_length``, ``last_modified``, and others.
   ``click_count`` and ``favorite_count`` are available when ``indexer.click.count.enabled`` and
   ``indexer.favorite.count.enabled`` are enabled (both enabled by default), respectively.
   OpenSearch date-math syntax such as ``now - 7d`` cannot be used in either Groovy or JavaScript.

url_expr Examples
-----------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Condition Expression
     - Description
   * - ``url.startsWith("https://docs.example.com/")``
     - Target documents whose URL starts with the specified value
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - Evaluate the URL with a regular expression (``String#matches``)
   * - ``title.contains("Release Notes")``
     - Target documents whose title contains a specific term

boost_expr Examples
-------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Boost Expression
     - Description
   * - ``3.0``
     - Boost by a fixed value
   * - ``click_count * 0.1 + 1``
     - Boost proportional to click count
   * - ``Math.log(click_count + 1)``
     - Logarithmic-scale boost based on click count

Usage Examples
==============

Boost a Documentation Site
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url_expr": "url.startsWith(\"https://docs.example.com/\")",
           "boost_expr": "5.0",
           "sort_order": 0
         }'

Boost Frequently Clicked Content
---------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url_expr": "url.startsWith(\"https://www.example.com/\")",
           "boost_expr": "click_count * 0.1 + 1",
           "sort_order": 10
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-elevateword` - ElevateWord API
- :doc:`../../admin/boostdoc-guide` - Document Boost Management Guide
