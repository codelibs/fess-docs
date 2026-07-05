==============
JSON Connector
==============

Overview
========

The JSON Connector provides functionality to retrieve data from local JSONL files
(JSON Lines format) and register them in the |Fess| index.

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
   :widths: 20 10 70

   * - Parameter
     - Required
     - Description
   * - ``files``
     - No
     - Path to the JSON file(s) to process (multiple paths allowed: comma-separated). Only files with a ``.json`` or ``.jsonl`` extension are processed.
   * - ``directories``
     - No
     - Path to the directory containing JSON files (multiple paths allowed: comma-separated)
   * - ``fileEncoding``
     - No
     - Character encoding (default: UTF-8)

.. warning::
   Either ``files`` or ``directories`` must be specified.
   If neither is specified (both are empty), a ``DataStoreException`` will be thrown.
   If both are specified, ``files`` takes precedence and ``directories`` is ignored.

.. note::
   The parameter name uses camelCase: ``fileEncoding`` (not the snake_case form ``file_encoding``).

Directory Behavior
~~~~~~~~~~~~~~~~~~

When ``directories`` is specified, files directly inside each directory are processed according to the following rules.

- **Subdirectories are not traversed** (no recursive search is performed).
- Only files with a ``.json`` or ``.jsonl`` extension are targeted (case-insensitive).
- Files are processed in ascending order of their last-modified timestamp.

.. note::
   This connector targets only JSON files on the local filesystem. HTTP access and API authentication are not supported.

Script Configuration
--------------------

The value of each field is assembled by referencing the fields of the JSON object.
Top-level fields of a JSON object can be referenced directly inside scripts as
**variables without a prefix** (no ``data.`` prefix is used).

Simple JSON object:

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

Nested JSON object (nested objects are referenced as maps):

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

Array element processing:

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

Available Fields
~~~~~~~~~~~~~~~~

- ``<field_name>`` - Reference a top-level field of the JSON object directly by name
- ``<parent>.<child>`` - Field of a nested object
- ``<array>[<index>]`` - Array element
- ``<array>.<method>`` - Array methods (``join``, ``collect``, ``size``, etc.)

.. note::

   If a field name contains characters that are invalid as a Groovy identifier,
   such as spaces or hyphens, that field cannot be referenced directly as a variable name.

JSON Format Details
===================

JSON File Format
----------------

The JSON Connector reads files in JSONL (JSON Lines) format.
This format places one JSON object per line. Files are read line by line,
and each line is parsed as an independent JSON object.

.. note::
   Files with a ``.json`` extension are also processed, but their content must be in
   JSONL format (one object per line).
   Array-format JSON files (``[{...}, {...}]``) and pretty-printed JSON spanning
   multiple lines cannot be read directly. Please convert them to JSONL format.

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

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Price: " + price + " yen"
    digest=category
    price=price

Merging Multiple JSON Files
---------------------------

Parameters:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Script:

::

    url="https://example.com/item/" + id
    title=title
    content=content

Troubleshooting
===============

File Not Found
--------------

**Symptom**: The log outputs ``... is not found.`` or ``Source file ... does not exist.``

**Checklist**:

1. Verify the file path is correct
2. Verify the file exists
3. Verify the file extension is ``.json`` or ``.jsonl``
4. Verify read permissions on the file

JSON Parse Error
----------------

**Symptom**: The log outputs ``Crawling Access Exception`` and ``JsonParseException`` or similar messages

When a line contains invalid content, only that line is skipped and recorded as a
failed URL; the crawl itself continues from the next line.

**Checklist**:

1. Verify the JSON file is in the correct format (JSONL: one object per line):

   ::

       # Validate that each line is a valid JSON object
       cat data.json | jq -c .

2. Verify the character encoding is correct
3. Check that a single object is not split across multiple lines
4. Check for comments (comments are not allowed in standard JSON)

No Data Retrieved
-----------------

**Symptom**: Crawl succeeds but item count is 0

**Checklist**:

1. Verify the JSON structure
2. Verify the script configuration is correct (check that field references do not use the ``data.`` prefix)
3. Verify field names are correct (including case sensitivity)
4. Check log messages for errors

Large JSON Files
----------------

**Symptom**: Out of memory or timeout

Files are read line by line, so the total file size does not directly affect memory usage.
However, problems may occur when a single line (object) is extremely large or when the
indexing load is high.

**Solution**:

1. Split the JSON file into multiple files
2. Increase the |Fess| heap size

Advanced Script Examples
========================

Conditional Processing
----------------------

Each field is evaluated as an independent expression. Use ternary operators for conditional values:

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

Joining Arrays
--------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

Setting Default Values
----------------------

::

    url="https://example.com/item/" + id
    title=title ?: "Untitled"
    content=description ?: (summary ?: "No description")
    price=price ?: 0

Date Formatting
---------------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

Numeric Processing
------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

Reference
=========

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
