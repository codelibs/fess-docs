==================================
Database Connector
==================================

Overview
========

The Database Connector provides functionality to retrieve data from JDBC-compatible relational databases
and register it in the |Fess| index.

This feature is built into |Fess| and requires no additional plugins.

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

1. JDBC driver is required
2. Read access to the database is required
3. Proper query design is important when retrieving large amounts of data

Installing JDBC Drivers
-----------------------

Place the JDBC driver in the ``lib/`` directory:

::

    # Example: MySQL driver
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

Restart |Fess| to load the driver.

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
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``driver``
     - Yes
     - JDBC driver class name
   * - ``url``
     - Yes
     - JDBC connection URL
   * - ``username``
     - Yes
     - Database username
   * - ``password``
     - Yes
     - Database password
   * - ``sql``
     - Yes
     - SQL query for data retrieval
   * - ``fetch.size``
     - No
     - Fetch size (default: 100)

Script Configuration
--------------------

Map SQL column names to index fields:

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

Available fields:

- ``data.<column_name>`` - SQL query result columns

SQL Query Design
================

Efficient Queries
-----------------

Query performance is important when handling large amounts of data:

::

    # Efficient query using indexes
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
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
    url="https://example.com/article/" + data.id

    # Combination of multiple fields
    url="https://example.com/" + data.category + "/" + data.slug

    # Use URL stored in database
    url=data.url

Multi-byte Character Support
============================

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

Connection Pooling
==================

Consider connection pooling when processing large amounts of data:

::

    # HikariCP configuration
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

Security
========

Protecting Database Credentials
-------------------------------

.. warning::
   Writing passwords directly in configuration files poses a security risk.

Recommended methods:

1. Use environment variables
2. Use |Fess| encryption features
3. Use read-only users

Principle of Least Privilege
----------------------------

Grant only minimum necessary permissions to database users:

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

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " Category: " + data.category + " Price: $" + data.price
    lastModified=data.updated_at

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

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

Troubleshooting
===============

JDBC Driver Not Found
---------------------

**Symptom**: ``ClassNotFoundException`` or ``No suitable driver``

**Resolution**:

1. Verify that JDBC driver is placed in ``lib/``
2. Verify driver class name is correct
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
2. Verify column names are correct
3. Verify table names are correct

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-json` - JSON Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
