============================================================
Part 12: Making SaaS Data Searchable -- Integration Scenarios with Salesforce and Databases
============================================================

Introduction
============

Important corporate data is stored not only on file servers and cloud storage, but also in SaaS applications and databases.
Customer information in Salesforce, product master data in internal databases, list data managed in CSV files -- these data sets are typically searchable only within their respective systems.

This article covers scenarios for importing SaaS and database data into the Fess index, enabling cross-source searching alongside other documents.

Target Audience
===============

- Those who want to include SaaS and database information in search results
- Those who want to learn how to use data store plugins
- Those who want to build a search platform spanning multiple data sources

Scenario
========

A sales organization has data distributed across the following systems.

.. list-table:: Data Source Overview
   :header-rows: 1
   :widths: 20 35 45

   * - System
     - Stored Data
     - Current Challenge
   * - Salesforce
     - Customer information, deal records, activity history
     - Searchable only within Salesforce
   * - Internal DB
     - Product master, price lists, inventory information
     - Accessible only through a dedicated management interface
   * - CSV Files
     - Client lists, event attendee lists
     - Can only be found by opening in Excel and scanning visually
   * - File Server
     - Proposals, quotes, contracts
     - Already crawled by Fess

The goal is to enable cross-source searching of all this data with Fess, so that information needed for sales activities can be found from a single search box.

Salesforce Data Integration
============================

To make Salesforce data searchable in Fess, use the Salesforce data store plugin.

Plugin Installation
--------------------

1. Navigate to [System] > [Plugins] in the admin panel
2. Install ``fess-ds-salesforce``

Connection Settings
--------------------

Integration with Salesforce requires configuring a Connected App.

**Salesforce-Side Preparation**

1. Create a Connected App in the Salesforce settings
2. Enable OAuth settings
3. Obtain the consumer key and secret

**Fess-Side Configuration**

1. Navigate to [Crawler] > [Data Store] > [Create New]
2. Handler Name: Select SalesforceDataStore
3. Configure parameters and scripts
4. Label: Set ``salesforce``

**Parameter Configuration Example**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**Script Configuration Example**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

For ``auth_type``, specify ``oauth_password`` (username/password authentication) or ``oauth_token`` (JWT Bearer token authentication). When using JWT authentication, set the RSA private key in ``private_key``.

Selecting Target Data
----------------------

Salesforce contains many objects, but not all of them need to be searchable.
Focus on the objects that the sales team searches for frequently.

.. list-table:: Example Target Objects
   :header-rows: 1
   :widths: 25 35 40

   * - Object
     - Searchable Fields
     - Purpose
   * - Account
     - Name, industry, address, description
     - Search for basic account information
   * - Opportunity
     - Name, stage, description, amount
     - Search for active deals
   * - Case
     - Subject, description, status
     - Search inquiry history

Database Integration
=====================

To make internal database data searchable, use the database data store plugin.

Plugin Installation
--------------------

Install the ``fess-ds-db`` plugin.
This plugin can connect to various databases (MySQL, PostgreSQL, Oracle, SQL Server, etc.) via JDBC.

Configuration
--------------

1. Navigate to [Crawler] > [Data Store] > [Create New]
2. Handler Name: Select DatabaseDataStore
3. Configure parameters and scripts
4. Label: Set ``database``

**Parameter Configuration Example**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**Script Configuration Example**

.. code-block:: properties

    url=url
    title=product_name
    content=description

The results of the SQL query specified in ``sql`` are crawled. In scripts, use SQL column names (or column labels) to map to Fess index fields.

SQL Query Design
-----------------

Key points when designing the SQL query for the ``sql`` parameter:

- Include a ``url`` column that serves as the link destination in search results (e.g., ``CONCAT('https://.../', id) AS url``)
- Include columns that serve as the searchable body text
- Use a ``WHERE`` clause to exclude unnecessary data (e.g., ``status = 'active'``)

In scripts, use the SQL column names directly to map to Fess index fields.

CSV File Integration
=====================

CSV file data can also be made searchable.

Configuration
--------------

Use the ``fess-ds-csv`` plugin or the CSV data store functionality.

1. Navigate to [Crawler] > [Data Store] > [Create New]
2. Handler Name: Select CsvDataStore
3. Configure parameters and scripts
4. Label: Set ``csv-data``

**Parameter Configuration Example**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**Script Configuration Example** (use column names when a header line is present)

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

When ``has_header_line=true``, column names from the header line can be used in scripts. When there is no header line, columns are referenced by number, such as ``cell1``, ``cell2``, ``cell3``. Scripts can contain Groovy expressions, including string concatenation.

If CSV files are updated regularly, fix the file placement location and set a crawl schedule so that the latest data is automatically reflected in the index.

Cross-Source Searching
========================

Once all data source configurations are complete, you can experience cross-source searching.

Search Example
---------------

Searching for "ABC Corporation" returns results such as:

1. Salesforce account information (Account)
2. Proposals from the file server (PDF)
3. Product purchase history from the database
4. Trade show attendee list from CSV

Users can find the information they need without having to be aware of where it is stored.

Filtering by Label
--------------------

When there are many search results, use labels to narrow them down.

- ``salesforce``: Salesforce data only
- ``database``: Database data only
- ``csv-data``: CSV data only
- ``shared-files``: File server documents only

Operational Considerations
===========================

Data Freshness
---------------

SaaS and database data may be updated frequently.
Set the crawl frequency appropriately to keep search results fresh.

.. list-table:: Recommended Crawl Frequency
   :header-rows: 1
   :widths: 25 25 50

   * - Data Source
     - Recommended Frequency
     - Reason
   * - Salesforce
     - Every 4-6 hours
     - Deal and customer information is updated during business hours
   * - Database
     - Every 2-4 hours
     - Data with high volatility, such as inventory information
   * - CSV
     - Daily
     - Typically updated via batch processing

Database Connection Security
------------------------------

When connecting directly to a database, pay careful attention to security.

- Use a read-only database user
- Restrict connections to the Fess server's IP address
- Do not grant access permissions to unnecessary tables
- Be careful with password management

Summary
========

This article covered scenarios for making Salesforce, database, and CSV file data searchable with Fess.

- CRM data integration using the Salesforce data store plugin
- Internal DB integration using the database data store plugin
- List data integration using the CSV data store
- Field mapping and SQL query design
- Leveraging labels in cross-source searching

By eliminating data silos, you can achieve an environment where all information sources are searchable from a single platform.
This concludes the Practical Solutions section. Starting from the next part, we will cover the Architecture and Scaling section, beginning with multi-tenant design.

References
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
