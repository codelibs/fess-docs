==================================
JSON Connector
==================================

Overview
========

The JSON Connector provides functionality to retrieve data from JSON files
on the local file system and register it in the |Fess| index.

This feature requires the ``fess-ds-json`` plugin.

It supports the following three formats, which are automatically detected
from the file content by default.

- JSON Lines format (one JSON object per line)
- An array of JSON objects (either pretty-printed or on a single line)
- A single JSON object

Records are read one at a time, so even for a large array, the entire file
is never held in memory.

.. note::

   This connector only targets JSON files on the local file system. It does
   not support remote retrieval such as HTTP, and specifying the ``urls``
   parameter results in an error rather than being ignored.

Prerequisites
=============

1. Plugin installation is required
2. Access to the JSON file is required
3. You must understand the structure of the JSON

Plugin Installation
--------------------

Method 1: Install from the admin console

1. Open "System" -> "Plugins"
2. Upload the JAR file
3. Restart |Fess|

Method 2: Place the JAR file directly

::

    # Download from the CodeLibs repository
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Place the file
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # or
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   From 15.8.0 onward, JARs are distributed via the
   `CodeLibs repository <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_.
   For 15.7.0 and earlier, they are available on
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_.

Configuration
=============

Configure from the admin console via "Crawler" -> "Data Store" -> "Create New".

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

Parameter Settings
-------------------

Local file:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Multiple files:

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

Directory specification:

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Parameter
     - Default
     - Description
   * - ``files``
     -
     - Path(s) of the JSON files to process (multiple paths can be specified,
       separated by commas). Files are processed in the order specified.
   * - ``directories``
     -
     - Path(s) of directories containing JSON files (multiple paths can be
       specified, separated by commas).
   * - ``recursive``
     - ``false``
     - Whether to traverse ``directories`` into subdirectories.
   * - ``max_depth``
     - ``10``
     - When ``recursive=true``, how many levels down into each directory to
       descend. Specifying ``0`` behaves the same as ``recursive=false``.
   * - ``include_pattern``
     -
     - Regular expression that the file's absolute path must fully match.
   * - ``exclude_pattern``
     -
     - Regular expression that the file's absolute path must not match.
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - Suffixes of the files to target (multiple suffixes can be specified,
       separated by commas). Case-insensitive.
   * - ``file_encoding``
     - ``UTF-8``
     - Character encoding of the file.
   * - ``format``
     - ``auto``
     - The document format. One of ``auto``, ``jsonl``, or ``json``.
   * - ``root_path``
     -
     - JSON Pointer specifying where to read records from (e.g.,
       ``/data/items``).

.. note::

   Parameter names are written in snake_case above, but camelCase spellings
   (such as ``fileEncoding`` for ``file_encoding``) can be used in the same
   way.

.. note::

   Specify at least one of ``files`` or ``directories``. If both are empty,
   an error occurs. The two are not mutually exclusive; if both are
   specified, both are processed. If the same file is reachable from both,
   it is read only once.

File Discovery Order
~~~~~~~~~~~~~~~~~~~~~

- Files specified in ``files`` are processed in the order specified.
- Files found under ``directories`` are processed in ascending order of
  last-modified time.
- Files specified in ``files`` are processed before files under
  ``directories``.

Filtering by ``file_suffixes`` also applies to files specified directly in
``files``. Files whose suffix does not match are skipped, with the reason
logged.

Non-existent paths, directories specified in ``files``, and files specified
in ``directories`` are all recorded as warnings in the log, and the crawl
itself continues.

``format``
----------

``auto`` reads the start of the document and determines the format from its
grammar. This can correctly identify any of the three formats, as long as
the file is well-formed.

Specify ``format=jsonl`` explicitly when the file is in JSON Lines format
and the lines near the start might be malformed (banner lines, progress
logs, records cut off mid-transfer, etc.), since automatic detection needs
to skip over such lines to make its determination.

This setting also determines the scope of impact of a malformed record.

- **JSON Lines format**: Since each line is parsed independently, the cost
  of a malformed line is limited to that line. The failure is recorded in
  the failure URL under the key ``<file's absolute path>@<line number>``,
  and processing continues with the next line.
- **Other formats**: Since the file is read as a token stream, a single
  failure can involve subsequent records. A document cut off in the middle
  of an object cannot recover, and if failures occur a certain number of
  times in a row, that file is aborted with a warning.

``root_path``
-------------

Specifying a JSON Pointer that points to a nested array registers each of
its elements as a record.

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- If it points to an array, each element becomes one record.
- If it points to an object, that object becomes one record.
- If it does not match anything, this is not an error; the number of
  records is 0.
- JSON Pointer escaping (``~1`` for ``/``, ``~0`` for ``~``) can be used.

``root_path`` takes precedence over ``format``. This is because the
document reached via the JSON Pointer is not read line by line; if
specified together with ``format=jsonl``, a warning to that effect is
output to the log.

.. warning::

   ``root_path`` must start with ``/``. If you forget the leading ``/``, as
   in ``data/items``, it cannot be interpreted as a JSON Pointer, and the
   entire data store config fails with an error. In this case, the failure
   URL is recorded as the data store config rather than the parameter name,
   so determine which parameter is responsible from
   ``JSON Pointer expression must start with '/'`` in the log.

.. note::

   If you load, without specifying ``root_path``, a document formatted
   across multiple lines (a so-called wrapper format containing metadata
   and an array), line-by-line parsing is attempted, so the intended
   records cannot be obtained and failures are recorded. For such
   documents, specify ``root_path``.

Script Settings
----------------

The value of each field is assembled by referencing the values of each
field in the JSON object. Top-level fields of the JSON object can be
referenced directly in scripts as **variables without any prefix** (there
is no ``data.`` prefix).

Simple JSON object:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

Nested objects can be referenced as maps, and nested arrays as lists:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

Available Fields
~~~~~~~~~~~~~~~~~

- ``<field name>`` - References a top-level field of the JSON object
  directly by name
- ``<parent>.<child>`` - A field of a nested object
- ``<array>[<index>]`` - An array element

.. note::

   If a field's value is ``null``, that field is not registered in the
   document.

.. note::

   In |Fess| 15.9, the built-in scripting engine has become JavaScript.
   Groovy is provided as the ``fess-script-groovy`` plugin. The engine to
   use is specified via the data store parameter ``script_type`` (e.g.,
   ``script_type=javascript``). If omitted, ``groovy`` is used. Simple
   references and string concatenation, as in the examples above, work the
   same way regardless of engine, but other notations differ between
   engines.

Notes
=====

Parameters whose names match ``app.encrypt.property.pattern`` (by default,
those ending in ``password``, ``key``, ``token``, or ``secret``) are
referenced from the script as ``null``. This is to prevent credentials
written in data store parameters from being copied into index fields.

If a field with the same name exists on the record side, the record's
value takes precedence, just as with other parameters.

.. note::

   The match is a case-sensitive exact match against the parameter name.
   ``access_token`` is subject to this, but the camelCase ``accessToken``
   is not. When writing credentials in parameters, use snake_case.

Incorrect Parameters and Errors
================================

If an unusable value is specified for ``format``, ``include_pattern``,
``exclude_pattern``, or ``urls``, the crawl ends before any files are read,
and a failure URL containing that parameter name (e.g.,
``JsonDataStore:format``) is recorded.

If a non-numeric value is specified for ``max_depth``, it is logged and
the default value is used.

.. note::

   A data store crawl completes as a normal job even if no targets were
   retrieved at all. If the number of items retrieved differs from what
   you expect, check the index count, the failure URLs, and
   ``fess-crawler.log``.

Usage Examples
==============

Product Catalog
----------------

Parameters:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Script:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

A File Containing a Saved API Response
----------------------------------------

Parameters:

::

    files=/var/data/response.json
    root_path=/data/items

Script:

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

Processing a Directory Recursively
------------------------------------

Parameters:

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

Troubleshooting
================

File Not Found
----------------

**Symptom**: The log outputs ``... does not exist.``, ``... is not a
file.``, or ``... is skipped because its suffix is not one of ...``

**Check**:

1. Verify the file path is correct
2. Verify the file exists
3. Verify the file suffix matches ``file_suffixes`` (default: ``.json`` or
   ``.jsonl``)
4. Verify the |Fess| process user has read permission

JSON Parse Errors
-------------------

**Symptom**: The log outputs ``Failed to parse ...`` or ``Failed to read
...``, or a failure URL is recorded

**Check**:

1. Verify the file is valid JSON

   ::

       # For JSON Lines format, verify each line is a valid JSON object
       cat data.jsonl | jq -c .

       # For an array or a single object
       jq . data.json

2. Verify the character encoding is correct
3. Verify the file is not cut off partway through
4. Verify the file does not contain comments (comments are not allowed by
   the JSON standard)

No Data Retrieved
--------------------

**Symptom**: The crawl succeeds but the count is 0

**Check**:

1. If you specified ``root_path``, verify that the JSON Pointer matches
   the document's structure (if it does not match, this is not an error;
   the count is simply 0)
2. Verify that ``include_pattern``, ``exclude_pattern``, and
   ``file_suffixes`` are not excluding all targets. In this case,
   ``No sources to process`` is output to the log
3. Verify the script settings are correct (field references must not have
   a ``data.`` prefix)
4. Verify the field names are correct (including case)
5. Verify that ``url`` is being assembled. If ``url`` is empty, it results
   in a failure for that record

Garbled Characters
--------------------

**Symptom**: Characters in the registered document are corrupted

If you specify a ``file_encoding`` value that exists but is incorrect,
this does not result in an error; the document is registered with garbled
characters. Verify the file's actual encoding. If you specify a
nonexistent encoding name, a failure URL is recorded for that file.

Large JSON Files
-------------------

**Symptom**: Out of memory or timeout

Records are read one at a time, so the overall file size does not
directly affect memory usage. However, problems can occur if a single
record is extremely large or if the load from indexing is high.

**Solution**:

1. Split the JSON file into multiple files
2. Increase the |Fess| heap size

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
