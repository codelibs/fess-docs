====================================
Database Connector (Database Search)
====================================

Overview
========

The Database Connector registers records from JDBC-compatible relational databases (MySQL, PostgreSQL, Oracle, SQL Server, and others) into the |Fess| index, enabling database search (full-text search of database content). Each column retrieved by a ``SELECT`` statement is mapped to a search field and registered.

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

Method 1: Install from the admin console

1. Open "System" -> "Plugin"
2. Upload the JAR file
3. Restart |Fess|

Method 2: Place the JAR file directly

::

    # Download from the CodeLibs repository
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Place the file, in the same directory the admin console installs into
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # or
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

Installing JDBC Drivers
-----------------------

The JDBC driver is not bundled with the plugin. Obtain the driver for your database separately and place it yourself.

Data store crawling runs in the crawler process, so the driver has to be on the **crawler process classpath**. Either of these directories works:

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # Example: MySQL driver
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

After placing the JDBC driver, restart |Fess| to load it.

.. note::
   When the driver is missing, the crawl fails with
   ``The JDBC driver ... is not on the crawler classpath.``

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
     - JDBC fetch size. ``MIN_VALUE`` asks MySQL to read the result set one row at a time; other drivers reject a negative value, and the crawl continues with the driver default after a warning. A negative or non-numeric value is reported and ignored
   * - ``query_timeout``
     - No
     - Query timeout in seconds. ``0`` means no limit, which is the JDBC default. No timeout is set when the parameter is absent
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

.. note::
   Stopping the job does not release the crawler thread while a query is hanging.
   The stop request is only checked between rows, so it cannot interrupt a call
   blocked inside the driver. Set ``query_timeout`` for queries that may run long.

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
- ``crawlingConfig`` - the data store configuration
- ``crawlingContext`` - the crawling context; ``crawlingContext.doc`` holds the document being built

.. note::
   Column names must match the column labels (aliases) in the ``SELECT`` clause.
   When using aggregate functions or expressions, assign an explicit alias with ``AS``
   (e.g., ``COUNT(*) AS total``).

.. note::
   Column label casing differs between databases. PostgreSQL folds unquoted
   identifiers to lower case, H2 folds them to upper case, and MySQL reports them
   as declared. A name that does not resolve leaves the field unset rather than
   raising an error, so assign an explicit alias with ``AS`` when portability
   matters.

.. warning::
   Scripts can reference the **entire data store parameter map**, not only the SQL
   result columns. ``driver``, ``url``, ``username``, ``password`` and ``sql`` are
   all visible as variables of the same name, so a column can be shadowed
   unintentionally, or a parameter value can appear where a missing column was
   expected. When both exist, the column value wins.

Loading BLOB/Binary Data
========================

Binary columns (BLOB, ``BYTEA``, byte array, binary stream) are passed through the content
extraction process - the same extractor used for file crawling - and ingested as text.

CLOB, NCLOB and character streams are **not** passed through an extractor. They are read as
text as they are, and the MIME type hints described below do not apply to them.

Array-type columns become their elements joined with spaces. NULL values become empty strings.

.. note::
   Whether a BLOB column arrives as ``java.sql.Blob`` or as a byte array is decided by
   the JDBC driver - MySQL and PostgreSQL return a byte array. Both are extracted the
   same way.

.. note::
   CLOB and NCLOB are read into memory whole, with no size limit. For very large text
   columns, consider truncating in SQL with ``SUBSTRING`` or similar. The extractor path
   does honour the crawler's maximum content length.

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

.. warning::
   Narrowing the query this way does not turn the crawl into an incremental one.
   When a crawl finishes, |Fess| deletes the documents of this data store
   configuration that were not part of the crawl that just ran, so a filtered
   query leaves only the matching rows in the index.

   Add ``delete_old_docs=false`` to the data store parameters to keep the
   documents indexed by earlier crawls. Rows deleted from the database are then
   no longer removed from the index either, so run a full crawl periodically.

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

.. warning::
   ``url=url`` only does what it looks like when the ``SELECT`` result has a column
   labelled ``url``. With no such column, the data store parameter of the same name -
   the **JDBC connection URL** - becomes the document URL. Alias the column, as in
   ``SELECT page_url AS url``, or name it in the script, as in ``url=page_url``.

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

1. Rely on automatic encryption

   A parameter whose name matches ``app.encrypt.property.pattern`` (default
   ``.*password|.*key|.*token|.*secret``) is encrypted when saved from the admin
   console and stored with a ``{cipher}`` prefix. ``password`` matches that pattern,
   so it is not stored in cleartext when set from the admin console.

2. Use environment variables

   An environment variable whose name starts with ``FESS_ENV_`` is expanded inside a
   data store parameter as ``${variable name}``:

   ::

       password=${FESS_ENV_DB_PASSWORD}

   Which names are expanded is controlled by ``crawler.data.env.param.key.pattern``
   (default ``^FESS_ENV_.*``).

3. Use read-only users

.. note::
   Raising ``org.codelibs.fess.ds`` to DEBUG does not expose credentials: the values of
   parameters matching ``app.encrypt.property.pattern``, and credentials embedded in the
   JDBC URL, are masked in the log.

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

When a crawl fails, the log message identifies which step failed.

JDBC Driver Not Found
---------------------

**Symptom**: ``The JDBC driver ... is not on the crawler classpath.``

**Resolution**:

1. Verify that the JDBC driver is placed in ``app/WEB-INF/lib/`` or ``app/WEB-INF/env/crawler/lib/``
2. Verify that the class name given in ``driver`` is correct
3. Restart |Fess|

Connection Errors
-----------------

**Symptom**: ``Failed to connect to <URL>.``

**Check**:

1. Is the database running?
2. Is the hostname and port correct?
3. Is the username and password correct?
4. Firewall settings

Query Errors
------------

**Symptom**: ``Failed to execute the query.``

**Check**:

1. Test the SQL query directly on the database
2. Verify that column names are correct
3. Verify that table names are correct

Missing Parameters
------------------

**Symptom**: ``The driver parameter is required.``, ``The url parameter is required.`` or ``The sql parameter is required.``

A required parameter is not set. Check the parameter field.

Only Some Rows Fail
-------------------

A row that fails does not stop the crawl; it is recorded under "System" -> "Failure URL".
The document URL is used when the scripts produced one, and
``datastore://<data store configuration id>/<row number>`` when they did not.

Documents Do Not Appear in Search Results
-----------------------------------------

1. Verify that the scripts set ``url``, ``title`` and ``content``
2. Verify that the column label casing matches what the scripts use (see "Script Configuration")
3. Check the document count in the crawl job log

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-json` - JSON Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../crawler-basic` - Basic Crawler Configuration
- :doc:`../search-basic` - Search Features
