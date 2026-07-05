==================================
Database Connector
==================================

Overview
========

The Database Connector provides functionality to retrieve data from JDBC-compatible relational databases
and register it in the |Fess| index.

This feature requires the ``fess-ds-db`` plugin.

Supported Databases
===================

All JDBC-compatible databases are supported. Main examples:

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

Prerequisites
=============

1. Installation of the ``fess-ds-db`` plugin is required
2. A JDBC driver compatible with the target database is required
3. Read access to the database is required
4. Proper query design is important when retrieving large amounts of data

Plugin Installation
-------------------

Method 1: Place the JAR file directly

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Place the file
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Method 2: Install from the admin console

1. Open "System" -> "Plugin"
2. Upload the JAR file
3. Restart |Fess|

Installing JDBC Drivers
-----------------------

Place the JDBC driver compatible with your target database in the |Fess| classpath (``app/WEB-INF/lib/`` directory):

::

    # Example: MySQL driver
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

After placing the JDBC driver, restart |Fess| to load it.

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
     - Products Database
   * - Handler Name
     - DatabaseDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

MySQL/MariaDB example:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

PostgreSQL example:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Parameter
     - Required
     - Description
   * - ``driver``
     - Yes
     - JDBC driver class name (if not specified, a ``DataStoreException`` is raised)
   * - ``url``
     - Yes
     - JDBC connection URL (required for connection)
   * - ``sql``
     - Yes
     - SQL query for data retrieval (if not specified, a ``DataStoreException`` is raised)
   * - ``username``
     - No
     - Database username
   * - ``password``
     - No
     - Database password
   * - ``fetch_size``
     - No
     - JDBC fetch size. Set to ``MIN_VALUE`` for MySQL streaming result sets
   * - ``default_mimetype``
     - No
     - Default MIME type used when extracting content from BLOB or binary columns
   * - ``column_label.mimetype``
     - No
     - Column name that contains the MIME type used for extracting BLOB or binary columns (e.g., ``column_label.mimetype=content_type``)
   * - ``column_label.filename``
     - No
     - Column name that contains the filename used for extracting BLOB or binary columns (MIME type is inferred from the file extension)
   * - ``info.*``
     - No
     - Additional JDBC connection properties (e.g., ``info.ssl=true``). The key with ``info.`` removed is passed to the JDBC driver
   * - ``readInterval``
     - No
     - Delay in milliseconds between processing each row. Default: 0
   * - ``script_type``
     - No
     - Script engine type. Default: groovy

Script Configuration
--------------------

Map SQL column names to index fields:

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

Available fields:

- ``<column_name>`` - SQL query result columns (accessed directly by the column label name; no prefix such as ``data.`` is used)

.. note::
   Column names must match the column labels (aliases) in the ``SELECT`` clause.
   When using aggregate functions or expressions, assign an explicit alias with ``AS``
   (e.g., ``COUNT(*) AS total``).

Loading BLOB/Binary Data
========================

Columns of type BLOB, CLOB, NCLOB, byte array, or binary stream are automatically passed through the
content extraction process (the same extractor used for file crawling) and ingested as text.
Array-type columns are converted to space-separated strings. NULL values become empty strings.

To correctly extract text from BLOB or binary streams, the data type (MIME type) must be determined.
The following priority order is used:

1. ``column_label.mimetype=<column name>`` - Use the value of the specified column as the MIME type
2. ``column_label.filename=<column name>`` - Treat the value of the specified column as a filename and infer the MIME type from the file extension
3. ``default_mimetype`` - Default MIME type used when the above methods cannot determine the type

Example (extract BLOB in the ``file_data`` column using the MIME type from the ``content_type`` column):

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

SQL Query Design
================

Efficient Queries
-----------------

Query performance is important when handling large amounts of data.
SQL is sent to the database as-is (parameter binding is not performed):

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

Incremental Crawling
--------------------

Methods to retrieve only updated records:

::

    # Filter by update date
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Specify range by ID
    sql=SELECT * FROM articles WHERE id > 10000

URL Generation
--------------

Generate document URLs in the script:

::

    # Fixed pattern
    url="https://example.com/article/" + id

    # Combination of multiple fields
    url="https://example.com/" + category + "/" + slug

    # Use URL stored in database
    url=url

Multi-byte Character Support
=============================

When handling data with multi-byte characters such as Japanese:

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL uses UTF-8 by default. If needed:

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

Security
========

Protecting Database Credentials
--------------------------------

.. warning::
   Writing passwords directly in configuration files poses a security risk.

Recommended methods:

1. Use environment variables
2. Use |Fess| encryption features
3. Use read-only users

Principle of Least Privilege
-----------------------------

Grant only the minimum necessary permissions to database users:

::

    -- MySQL example
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Usage Examples
==============

Product Catalog Search
----------------------

Parameters:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

Script:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " Category: " + category + " Price: " + price
    lastModified=updated_at

Knowledge Base Articles
-----------------------

Parameters:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

Script:

::

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

Troubleshooting
===============

JDBC Driver Not Found
---------------------

**Symptom**: ``ClassNotFoundException`` or ``No suitable driver``

**Resolution**:

1. Verify that the JDBC driver is placed in ``lib/``
2. Verify that the driver class name is correct
3. Restart |Fess|

Connection Errors
-----------------

**Symptom**: ``Connection refused`` or authentication errors

**Check**:

1. Is the database running?
2. Is the hostname and port correct?
3. Is the username and password correct?
4. Firewall settings

Query Errors
------------

**Symptom**: ``SQLException`` or SQL syntax errors

**Check**:

1. Test the SQL query directly on the database
2. Verify that column names are correct
3. Verify that table names are correct

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-json` - JSON Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
