==========================
Storage API
==========================

Overview
========

Storage API is an API for managing |Fess| storage.
You can view index storage usage and perform optimization operations.

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
     - /
     - Get storage information
   * - POST
     - /optimize
     - Optimize index
   * - POST
     - /flush
     - Flush index

Get Storage Information
=======================

Request
-------

::

    GET /api/admin/storage

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "storage": {
          "indices": [
            {
              "name": "fess.20250129",
              "status": "open",
              "health": "green",
              "docsCount": 123456,
              "docsDeleted": 234,
              "storeSize": "5.2gb",
              "primariesStoreSize": "2.6gb",
              "shards": 5,
              "replicas": 1
            }
          ],
          "totalStoreSize": "5.2gb",
          "totalDocsCount": 123456,
          "clusterHealth": "green",
          "diskUsage": {
            "total": "107374182400",
            "available": "53687091200",
            "used": "53687091200",
            "usedPercent": 50.0
          }
        }
      }
    }

Response Fields
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``indices``
     - Index list
   * - ``name``
     - Index name
   * - ``status``
     - Index status (open/close)
   * - ``health``
     - Health status (green/yellow/red)
   * - ``docsCount``
     - Document count
   * - ``docsDeleted``
     - Deleted document count
   * - ``storeSize``
     - Storage size
   * - ``primariesStoreSize``
     - Primary shard size
   * - ``shards``
     - Shard count
   * - ``replicas``
     - Replica count
   * - ``totalStoreSize``
     - Total storage size
   * - ``totalDocsCount``
     - Total document count
   * - ``clusterHealth``
     - Cluster health
   * - ``diskUsage``
     - Disk usage information

Optimize Index
==============

Request
-------

::

    POST /api/admin/storage/optimize
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129",
      "maxNumSegments": 1,
      "onlyExpungeDeletes": false,
      "flush": true
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``index``
     - No
     - Index name (all indices if not specified)
   * - ``maxNumSegments``
     - No
     - Maximum number of segments (default: 1)
   * - ``onlyExpungeDeletes``
     - No
     - Only remove deleted documents (default: false)
   * - ``flush``
     - No
     - Flush after optimization (default: true)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index optimization started"
      }
    }

Flush Index
===========

Request
-------

::

    POST /api/admin/storage/flush
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``index``
     - No
     - Index name (all indices if not specified)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index flushed successfully"
      }
    }

Usage Examples
==============

Get Storage Information
-----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN"

Optimize All Indices
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "maxNumSegments": 1,
           "flush": true
         }'

Optimize Specific Index
-----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129",
           "maxNumSegments": 1,
           "onlyExpungeDeletes": false
         }'

Expunge Deleted Documents
-------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "onlyExpungeDeletes": true
         }'

Flush Index
-----------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/flush" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129"
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`../../admin/storage-guide` - Storage Management Guide

