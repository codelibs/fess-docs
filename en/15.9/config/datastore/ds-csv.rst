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

Multiple files:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

.. note::

   Quote processing and escape processing are **enabled by default** in
   |Fess| 15.9. CSV files (RFC 4180 compliant) where quoted fields contain
   delimiters or line breaks are parsed correctly without specifying any
   parameters.
   For how to revert to the previous behavior (disabling quote processing)
   and important caveats, see "Disabling Quote and Escape Processing" below.

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
     - Quote character (default: double quote ``"``). Quote processing is enabled by default (see ``quote_disabled``).
   * - ``escape_character``
     - No
     - Escape character (default: same character as ``quote_character``. Per RFC 4180, quotes are escaped by doubling them). Whether escape processing is enabled follows the resolved value of ``quote_disabled`` (see ``escape_disabled``).

.. note::

   If both ``files`` and ``directories`` are empty, an error (``DataStoreException``) is raised.
   At least one of them must be specified.

Advanced Parameters
~~~~~~~~~~~~~~~~~~~

The following parameters provide fine-grained control over CSV parsing and indexing behaviour:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``quote_disabled``
     - Whether to disable quote processing (default: false). RFC 4180 compliant quoted fields are parsed correctly by default. Set to ``true`` to revert to the previous behavior (treating quotes as ordinary characters).
   * - ``escape_disabled``
     - Whether to disable escape processing (default: same as the resolved value of ``quote_disabled``). An explicitly specified value takes precedence.
   * - ``delete_old_docs``
     - Whether to delete, after the crawl completes, documents that belong to this data store config and were not re-registered during the current crawl session (default: true). If you feed multiple CSV files into the same data store config at different times, set this to ``false`` -- otherwise documents registered by the earlier files will be deleted (see the troubleshooting section below for details).
   * - ``keep_expires_docs``
     - When deleting documents via ``delete_old_docs``, whether to exclude documents whose expiration (the "expires" value set via e.g. ``time_to_live``) has not yet arrived (default: true). Set to ``false`` to delete unregistered documents even within their expiration period.
   * - ``time_to_live``
     - How many minutes after registration a document's expiration should be set (in minutes; default: unset, meaning no expiration).
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
   ``"Book, Programming"`` above, it is parsed as a single field as-is with
   the default (quote processing enabled).
   To revert to the previous behavior (treating quotes as ordinary characters
   and splitting fields on the delimiter), see "Disabling Quote and Escape
   Processing" below.

Disabling Quote and Escape Processing
--------------------------------------

Quote processing and escape processing are enabled by default in |Fess| 15.9.
The default quote character is double quote ``"``, and the default escape
character is the same as the quote character (escaped by doubling it, per
RFC 4180); standard RFC 4180 CSV files can be parsed as-is without any
parameters.

.. warning::

   With quote processing enabled, if a CSV file contains even a single ``"``
   with no matching closing quote, everything in the file from that quote
   onward (including subsequent lines) is read as a single field value, and
   no documents are generated from the remaining rows. Because previous
   versions parsed each line independently, this behavior can surface for the
   first time only after upgrading.
   Since ``delete_old_docs`` (described above) is enabled by default, this
   can delete not only the documents that failed to be generated, but also
   documents that were already registered by a previous crawl.
   Before upgrading, check your CSV files for unmatched quotes, or consider
   setting ``quote_disabled=true`` to revert to the previous parsing method.

To disable quote processing (revert to the previous behavior):

::

    # Parameter
    quote_disabled=true

Setting ``quote_disabled=true`` also disables escape processing at the same
time (unless you explicitly set ``escape_disabled=false``).

To disable escape processing only:

::

    # Parameter
    escape_disabled=true

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

Single quote:

::

    # Parameter
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

2. Quoted fields (fields containing the delimiter character) are parsed correctly
   by default. Check that you have not unintentionally set ``quote_disabled=true``.
3. Verify the CSV file format (RFC 4180 compliant). If it contains a ``"`` with no
   matching closing quote, everything in the file from that point onward is read
   as a single field value.

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
5. Verify that no parameter name is misspelled (an unrecognized parameter name is
   ignored without any warning; ``has_headerline=true``, for example, leaves
   ``has_header_line`` at its default ``false``)

Index From a Previous Crawl Disappears on a Second CSV Import
-------------------------------------------------------------

**Symptom**: After crawling a first CSV file, crawling a second CSV file with the
same data store config on a later day causes the documents registered from the
first CSV file to disappear from search results.

**Cause**:

After a crawl completes, |Fess| deletes from the index any documents that belong
to that data store config and were not re-registered during the current session
(``delete_old_docs``, default: true). If you feed multiple CSV files into the same
data store config at different times, then at the time the later file is crawled,
the content registered by the earlier file is treated as "not re-registered during
the current session" and is deleted.

**Solution**:

If you feed multiple CSV files into the same data store config at different times
and want their content to accumulate, specify the following.

::

    delete_old_docs=false

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
Since quote processing is enabled by default, it is parsed as-is without specifying any parameters:

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
   * - ``delete_processed_file``
     - No
     - Whether to delete the CSV file after processing completes (default: true)
   * - ``ignore_data_store_exception``
     - No
     - Whether to continue the overall crawl even if an exception occurs while processing one CSV file (default: true)

.. warning::

   ``CsvListDataStore`` automatically **deletes** CSV files after processing completes (``delete_processed_file`` defaults to ``true``). If an error occurs during processing, the file is renamed to ``.txt`` instead (if renaming fails, the file is deleted). If you do not want files to be deleted, specify ``delete_processed_file=false``.

CSV Row Format (Event Type)
-------------------------------------

CSV files passed to ``CsvListDataStore`` must have at least two columns per row: an
"event type" and a "URL". Additional columns can be added and referenced as
``cell3``, ``cell4``, ... (for example, to feed a value into ``timestamp.overwrite``).

::

    <event_type>,<URL>

The event type can be one of the following three values.

- ``create`` - a file was created
- ``modify`` - a file was updated
- ``delete`` - a file was deleted

``create`` and ``modify`` are treated as the same operation (crawling and indexing
the target URL). There is no difference in behavior between them.

The column name (when a header row is present) and the value for each event type
can be changed using the following parameters.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``field.event_type``
     - Column name that holds the event type (default: ``event_type``)
   * - ``event.create``
     - Value representing "created" (default: ``create``)
   * - ``event.modify``
     - Value representing "updated" (default: ``modify``)
   * - ``event.delete``
     - Value representing "deleted" (default: ``delete``)

Example CSV file:

::

    modify,smb://servername/data/testfile1.txt
    delete,smb://servername/data/testfile2.txt

Example script (without a header row):

::

    event_type=cell1
    url=cell2

Overwriting Field Values (.overwrite)
----------------------------------------

Appending ``.overwrite`` to the name of an indexed field assembled in the script
causes that field's value to be overwritten with the value set from the CSV,
instead of the value obtained from the actual crawl of the target file.

::

    timestamp.overwrite=cell3

.. note::

   The date facet on the search screen filters using the ``timestamp`` field, not
   ``created``. If you want to overwrite the timestamp with a value from the CSV,
   specify ``timestamp.overwrite`` rather than ``created.overwrite``.

Carrying Over Authentication and Proxy Settings
---------------------------------------------------

``CsvListDataStore`` actually crawls the URLs written in the CSV, but authentication
and proxy settings configured on a file crawl or web crawl data store config are not
carried over. Specify any required settings individually as parameters of this data
store config.

Example SMB authentication:

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

Example proxy settings:

::

    crawler.web.proxyHost=proxy.example.com
    crawler.web.proxyPort=8080

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

.. note::

   As shown above, a row where ``url`` returns ``null`` is silently skipped
   rather than treated as a failure. The number of skipped rows is tallied per
   CSV file and is output as a single summary WARN log each time that file's
   read finishes (individual failed URLs are not logged per row; when
   processing multiple CSV files, one WARN log is output per file).

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
