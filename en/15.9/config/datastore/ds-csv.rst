==================================
CSV Connector
==================================

Overview
========

The CSV Connector provides functionality to retrieve data from CSV files
and register it in the |Fess| index.

This feature requires the ``fess-ds-csv`` plugin.

Prerequisites
=============

1. Plugin installation is required
2. Access to the CSV file is required
3. You must know the character encoding of the CSV file

Plugin Installation
-------------------

Method 1: Place JAR file directly

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # Place the file
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Method 2: Install from admin console

1. Open "System" -> "Plugins"
2. Upload the JAR file
3. Restart |Fess|

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
     - Products CSV
   * - Handler Name
     - CsvDataStore
   * - Enabled
     - On

Parameter Settings
------------------

Local file:

::

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

Multiple files:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   Quote processing and escape processing are **disabled** by default.
   If you need to handle CSV files where fields enclosed in quotes contain
   delimiters or line breaks (RFC 4180 compliant), explicitly set
   ``quote_disabled=false`` to enable quote processing.
   See "Enabling Quote and Escape Processing" below for details.

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
     - CSV file path (local path; multiple paths can be specified separated by commas). Either ``files`` or ``directories`` must be specified. If both are specified, ``files`` takes precedence. Files must have a ``.csv`` or ``.tsv`` extension; files with any other extension are skipped.
   * - ``directories``
     - No
     - Path to a directory containing CSV files (multiple paths can be specified separated by commas). Only ``.csv`` and ``.tsv`` files within the directory are processed. Used when ``files`` is not specified.
   * - ``file_encoding``
     - No
     - Character encoding (default: UTF-8)
   * - ``has_header_line``
     - No
     - Whether a header row exists (default: false)
   * - ``separator_character``
     - No
     - Separator character (default: comma ``,``). Escape sequences such as ``\t`` can be specified (for tab-separated files).
   * - ``quote_character``
     - No
     - Quote character (default: double quote ``"``). Note that quote processing is disabled by default (see ``quote_disabled``).
   * - ``escape_character``
     - No
     - Escape character (default: backslash ``\``). Note that escape processing is disabled by default (see ``escape_disabled``).

.. note::

   If both ``files`` and ``directories`` are empty, an error (``DataStoreException``) is raised.
   At least one of them must be specified.

Advanced Parameters
~~~~~~~~~~~~~~~~~~~

The following parameters provide fine-grained control over CSV parsing behaviour:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``quote_disabled``
     - Whether to disable quote processing (default: true). Set to ``false`` to handle RFC 4180 quoted fields.
   * - ``escape_disabled``
     - Whether to disable escape processing (default: true). Set to ``false`` to enable escaping via ``escape_character``.
   * - ``skip_lines``
     - Number of leading lines to skip (default: 0)
   * - ``ignore_line_patterns``
     - Regular expression pattern for lines to ignore (e.g., ``^#.*`` to ignore comment lines)
   * - ``ignore_empty_lines``
     - Whether to ignore empty lines (default: false)
   * - ``ignore_trailing_whitespaces``
     - Whether to ignore trailing whitespace (default: false)
   * - ``ignore_leading_whitespaces``
     - Whether to ignore leading whitespace (default: false)
   * - ``null_string``
     - String value to treat as null
   * - ``break_string``
     - String used to replace line breaks within field values
   * - ``readInterval``
     - Wait time in milliseconds between processing each record (default: 0)

Script Settings
---------------

Field values are assembled by referencing the values of each CSV column.
CSV columns are referenced directly in scripts as **variables without any prefix**
(there is no ``data.`` prefix).

With header row (reference by column name):

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

Without header row (reference by column index):

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

Available Fields
~~~~~~~~~~~~~~~~

- ``<column_name>`` - Reference by header row column name (only when ``has_header_line=true`` and the column name is not blank)
- ``cell<N>`` - Reference by column index (1-based: ``cell1``, ``cell2``, ...; available regardless of whether a header row is present)
- ``csvfile`` - Full path of the CSV file being processed
- ``csvfilename`` - File name of the CSV file being processed

.. note::

   If a column name contains characters that are invalid as a Groovy identifier,
   such as spaces or hyphens, the column cannot be referenced by name.
   Use ``cell<N>`` instead.

CSV Format Details
==================

Standard CSV (RFC 4180 compliant)
---------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

.. note::

   To include a delimiter inside a field by enclosing it in quotes, as in
   ``"Book, Programming"`` above, you must set ``quote_disabled=false`` to
   enable quote processing.
   When quote processing is disabled (the default), quotes are treated as
   ordinary characters and fields are split on the delimiter character.

Enabling Quote and Escape Processing
-------------------------------------

Quote processing and escape processing are disabled by default.
Enable them explicitly as follows.

To enable quote processing:

::

    # Parameter
    quote_disabled=false
    quote_character="

To enable escape processing:

::

    # Parameter
    escape_disabled=false
    escape_character=\

Changing Separator
------------------

Tab-separated (TSV):

::

    # Parameter
    separator_character=\t

Semicolon-separated:

::

    # Parameter
    separator_character=;

Custom Quote Character
----------------------

Single quote (quote processing must be enabled):

::

    # Parameter
    quote_disabled=false
    quote_character='

Encoding
--------

Non-ASCII file (Shift_JIS):

::

    file_encoding=Shift_JIS

Non-ASCII file (EUC-JP):

::

    file_encoding=EUC-JP

Usage Examples
==============

Product Catalog CSV
-------------------

CSV file (products.csv):

::

    product_id,name,description,price,category,in_stock
    1001,Laptop,High-performance laptop,120000,Computers,true
    1002,Mouse,Wireless mouse,2500,Peripherals,true
    1003,Keyboard,Mechanical keyboard,8500,Peripherals,false

Parameters:

::

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Category: " + category + " Price: $" + price
    digest=category
    price=price

Filtering by stock status:

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

Employee Directory CSV
----------------------

CSV file (employees.csv):

::

    emp_id,name,department,email,phone,position
    E001,Taro Yamada,Sales Dept.,yamada@example.com,03-1234-5678,General Manager
    E002,Hanako Sato,Engineering Dept.,sato@example.com,03-2345-6789,Manager
    E003,Ichiro Suzuki,Administration Dept.,suzuki@example.com,03-3456-7890,Staff

Parameters:

::

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script:

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="Department: " + department + "\nPosition: " + position + "\nEmail: " + email + "\nPhone: " + phone
    digest=department

CSV Without Header
------------------

CSV file (data.csv):

::

    1,Product A,This is product A,1000
    2,Product B,This is product B,2000
    3,Product C,This is product C,3000

Parameters:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,

Script:

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

Multiple CSV Files Integration
------------------------------

Parameters:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script:

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

Tab-Separated (TSV) File
-------------------------

TSV file (data.tsv):

::

    id	title	content	category
    1	Article 1	This is the content of article 1	News
    2	Article 2	This is the content of article 2	Blog

Parameters:

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t

Script:

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

Troubleshooting
===============

File Not Found
--------------

**Symptom**: The crawl runs but no files are processed; ``is not found`` appears in the log

**Check**:

1. Verify the file path is correct (absolute path recommended)
2. Verify the file exists
3. Verify the file extension is ``.csv`` or ``.tsv`` (files with other extensions are skipped)
4. Verify the file has read permissions
5. Verify the file is accessible by the |Fess| process user

Character Encoding Issues
-------------------------

**Symptom**: Non-ASCII characters are not displayed correctly

**Solution**:

Specify the correct character encoding:

::

    # UTF-8
    file_encoding=UTF-8

    # Shift_JIS
    file_encoding=Shift_JIS

    # EUC-JP
    file_encoding=EUC-JP

    # Windows standard (CP932)
    file_encoding=Windows-31J

Check file encoding:

::

    file -i data.csv
    # or
    nkf -g data.csv

Columns Not Recognized Correctly
---------------------------------

**Symptom**: Column separation is not recognized correctly, or a quoted field is split

**Check**:

1. Verify the separator is correct:

   ::

       # Comma
       separator_character=,

       # Tab
       separator_character=\t

       # Semicolon
       separator_character=;

2. To handle quoted fields (fields that contain the delimiter character), enable quote processing:

   ::

       quote_disabled=false

3. Verify the CSV file format (RFC 4180 compliant)

Header Row Handling
-------------------

**Symptom**: The first row is recognized as data

**Solution**:

When a header row is present:

::

    has_header_line=true

When no header row is present:

::

    has_header_line=false

No Data Retrieved
-----------------

**Symptom**: Crawl succeeds but the document count is 0

**Check**:

1. Verify the CSV file is not empty
2. Verify the script settings are correct (column names and ``cell<N>`` references must be used without a ``data.`` prefix)
3. Verify the column names are correct (when has_header_line=true)
4. Check the log for error messages

Large CSV Files
---------------

**Symptom**: Out of memory or timeout

**Solution**:

1. Split the CSV file into multiple smaller files
2. Use only the necessary columns in the script
3. Increase the |Fess| heap size
4. Filter out unnecessary rows

Fields with Line Breaks
-----------------------

In RFC 4180 format, fields containing line breaks can be handled by enclosing them in quotes.
Since quote processing is disabled by default, ``quote_disabled=false`` must be specified:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Parameters:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_disabled=false
    quote_character="

CsvListDataStore
================

The ``fess-ds-csv`` plugin also includes the ``CsvListDataStore`` handler in addition to ``CsvDataStore``.

``CsvListDataStore`` extends ``CsvDataStore`` and provides the following additional features:

- Multi-threaded processing (controlled by the ``numOfThreads`` parameter)
- Automatic deletion of processed CSV files
- Timestamp-based file filtering (skips files that may still be written to)

All parameters and script settings of ``CsvDataStore`` are available as-is.

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Handler Name
     - CsvListDataStore

Additional Parameters
---------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``timestamp_margin``
     - No
     - Elapsed time in milliseconds since the file's last modification time. Files that have not yet exceeded this threshold are considered to still be written to and are skipped (default: 10000).
   * - ``numOfThreads``
     - No
     - Number of processing threads (default: 1)

.. note::

   ``CsvListDataStore`` automatically deletes CSV files after processing is complete. If an error occurs during processing, the file is renamed to ``.txt`` (if renaming fails, the file is deleted).

Advanced Script Examples
========================

Data Processing
---------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

Conditional Indexing
--------------------

::

    // Only index products with a price of 10000 or more
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

Combining Multiple Columns
--------------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\nSpecifications:\n" + specs + "\n\nNotes:\n" + notes
    category=category

Date Formatting
---------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // Add further processing here if date format conversion is required

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-json` - JSON Connector
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `RFC 4180 - CSV Format <https://datatracker.ietf.org/doc/html/rfc4180>`_
