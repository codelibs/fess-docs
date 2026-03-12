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

Configure from admin console via "Crawler" -> "Data Store" -> "Create New".

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

    file_path=/path/to/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

HTTP file:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Multiple files:

::

    file_path=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``file_path``
     - Yes
     - CSV file path (local, HTTP, multiple separated by comma)
   * - ``encoding``
     - No
     - Character encoding (default: UTF-8)
   * - ``has_header``
     - No
     - Whether header row exists (default: true)
   * - ``separator``
     - No
     - Separator character (default: comma ``,``)
   * - ``quote``
     - No
     - Quote character (default: double quote ``"``)

Script Settings
---------------

With header row:

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

Without header row (column index):

::

    url="https://example.com/product/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Available Fields
~~~~~~~~~~~~~~~~

- ``data.<column_name>`` - Header row column name (when has_header=true)
- ``data.col<N>`` - Column index (when has_header=false, 0-based)

CSV Format Details
==================

Standard CSV (RFC 4180 compliant)
---------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

Changing Separator
------------------

Tab-separated (TSV):

::

    # Parameter
    separator=\t

Semicolon-separated:

::

    # Parameter
    separator=;

Custom Quote Character
----------------------

Single quote:

::

    # Parameter
    quote='

Encoding
--------

Japanese file (Shift_JIS):

::

    encoding=Shift_JIS

Japanese file (EUC-JP):

::

    encoding=EUC-JP

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

    file_path=/var/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Category: " + data.category + " Price: $" + data.price
    digest=data.category
    price=data.price

Filtering by stock status:

::

    if (data.in_stock == "true") {
        url="https://shop.example.com/product/" + data.product_id
        title=data.name
        content=data.description
        price=data.price
    }

Employee Directory CSV
----------------------

CSV file (employees.csv):

::

    emp_id,name,department,email,phone,position
    E001,John Smith,Sales,john@example.com,555-1234,Manager
    E002,Jane Doe,Development,jane@example.com,555-2345,Senior Developer
    E003,Bob Wilson,HR,bob@example.com,555-3456,Coordinator

Parameters:

::

    file_path=/var/data/employees.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="Department: " + data.department + "\nPosition: " + data.position + "\nEmail: " + data.email + "\nPhone: " + data.phone
    digest=data.department

CSV Without Header
------------------

CSV file (data.csv):

::

    1,Product A,This is product A,1000
    2,Product B,This is product B,2000
    3,Product C,This is product C,3000

Parameters:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=false
    separator=,
    quote="

Script:

::

    url="https://example.com/item/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Multiple CSV Files Integration
------------------------------

Parameters:

::

    file_path=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

Fetch CSV from HTTP
-------------------

Parameters:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description

Tab-Separated (TSV) File
------------------------

TSV file (data.tsv):

::

    id	title	content	category
    1	Article 1	This is article 1 content	News
    2	Article 2	This is article 2 content	Blog

Parameters:

::

    file_path=/var/data/data.tsv
    encoding=UTF-8
    has_header=true
    separator=\t
    quote="

Script:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

Troubleshooting
===============

File Not Found
--------------

**Symptom**: ``FileNotFoundException`` or ``No such file``

**Check**:

1. Verify the file path is correct (absolute path recommended)
2. Verify the file exists
3. Verify read permissions on the file
4. Verify |Fess| user can access the file

Character Encoding Issues
-------------------------

**Symptom**: Japanese or other characters not displayed correctly

**Solution**:

Specify the correct character encoding:

::

    # UTF-8
    encoding=UTF-8

    # Shift_JIS
    encoding=Shift_JIS

    # EUC-JP
    encoding=EUC-JP

    # Windows standard (CP932)
    encoding=Windows-31J

Check file encoding:

::

    file -i data.csv
    # or
    nkf -g data.csv

Columns Not Recognized Correctly
--------------------------------

**Symptom**: Column separation not recognized correctly

**Check**:

1. Verify separator is correct:

   ::

       # Comma
       separator=,

       # Tab
       separator=\t

       # Semicolon
       separator=;

2. Verify quote character setting
3. Verify CSV file format (RFC 4180 compliant)

Header Row Handling
-------------------

**Symptom**: First row is recognized as data

**Solution**:

When header row exists:

::

    has_header=true

When header row does not exist:

::

    has_header=false

No Data Retrieved
-----------------

**Symptom**: Crawl succeeds but count is 0

**Check**:

1. Verify CSV file is not empty
2. Verify script settings are correct
3. Verify column names are correct (when has_header=true)
4. Check logs for error messages

Large CSV Files
---------------

**Symptom**: Out of memory or timeout

**Solution**:

1. Split CSV file into multiple files
2. Use only necessary columns in script
3. Increase |Fess| heap size
4. Filter unnecessary rows

Fields with Line Breaks
-----------------------

RFC 4180 format allows handling fields with line breaks by enclosing in quotes:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Parameters:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Advanced Script Examples
========================

Data Processing
---------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseInt(data.price)
    category=data.category.toLowerCase()

Conditional Indexing
--------------------

::

    # Only products with price >= 10000
    if (parseInt(data.price) >= 10000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Combining Multiple Columns
--------------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\nSpecifications:\n" + data.specs + "\n\nNotes:\n" + data.notes
    category=data.category

Date Formatting
---------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # Additional processing if date format conversion is needed

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-json` - JSON Connector
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `RFC 4180 - CSV Format <https://datatracker.ietf.org/doc/html/rfc4180>`_

