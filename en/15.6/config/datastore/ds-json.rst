==================================
JSON Connector
==================================

Overview
========

The JSON Connector provides functionality to retrieve data from local JSON files
and JSONL files and register them in the |Fess| index.

This feature requires the ``fess-ds-json`` plugin.

Prerequisites
=============

1. Plugin installation is required
2. Access to JSON files is required
3. Understanding of JSON structure is necessary

Plugin Installation
-------------------

Method 1: Place JAR file directly

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Place the file
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Method 2: Install from admin console

1. Open "System" -> "Plugins"
2. Upload the JAR file
3. Restart |Fess|

Configuration
=============

Configure in the admin console under "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - Products JSON
   * - Handler Name
     - JsonDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

Local file:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

Multiple files:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

Directory:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``files``
     - No
     - JSON file path (multiple allowed: comma-separated)
   * - ``directories``
     - No
     - Directory path containing JSON files
   * - ``fileEncoding``
     - No
     - Character encoding (default: UTF-8)

.. warning::
   Either ``files`` or ``directories`` must be specified.
   If neither is specified, a ``DataStoreException`` will be thrown.
   If both are specified, ``files`` takes precedence and ``directories`` is ignored.

.. note::
   This connector only supports JSON files on the local filesystem. HTTP access and API authentication are not supported.

Script Configuration
--------------------

Simple JSON object:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

Nested JSON object:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

Array element processing:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

Available Fields
~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - JSON object field
- ``data.<parent>.<child>`` - Nested object
- ``data.<array>[<index>]`` - Array element
- ``data.<array>.<method>`` - Array methods (join, length, etc.)

JSON Format Details
===================

JSON File Format
----------------

The JSON Connector reads files in JSONL (JSON Lines) format.
This format has one JSON object per line.

.. note::
   JSON array format files ( ``[{...}, {...}]`` ) cannot be read directly.
   Please convert them to JSONL format.

JSONL format file:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

Usage Examples
==============

Product Catalog
---------------

Parameters:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Price: " + data.price + " USD"
    digest=data.category
    price=data.price

Merging Multiple JSON Files
----------------------------

Parameters:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Troubleshooting
===============

File Not Found
--------------

**Symptom**: ``FileNotFoundException``

**Checklist**:

1. Verify the file path is correct
2. Verify the file exists
3. Verify read permissions on the file

JSON Parse Error
----------------

**Symptom**: ``JsonParseException`` or ``Unexpected character``

**Checklist**:

1. Verify the JSON file is in correct format:

   ::

       # Validate JSON
       cat data.json | jq .

2. Verify the character encoding is correct
3. Check for invalid characters or line breaks
4. Check for comments (comments are not allowed in standard JSON)

No Data Retrieved
-----------------

**Symptom**: Crawl succeeds but item count is 0

**Checklist**:

1. Verify the JSON structure
2. Verify the script configuration is correct
3. Verify field names are correct (including case sensitivity)
4. Check log messages for errors

Large JSON Files
----------------

**Symptom**: Out of memory or timeout

**Solution**:

1. Split the JSON file into multiple files
2. Increase the |Fess| heap size

Advanced Script Examples
========================

Conditional Processing
----------------------

Each field is evaluated as an independent expression. Use ternary operators for conditional values:

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

Joining Arrays
--------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

Setting Default Values
----------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "Untitled"
    content=data.description ?: (data.summary ?: "No description")
    price=data.price ?: 0

Date Formatting
---------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Numeric Processing
------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price as Float
    stock=data.stock_quantity as Integer

Reference
=========

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
