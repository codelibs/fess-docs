===========================================
Searching Database, CSV and Salesforce Data
===========================================

Introduction
============

The product master lives in an internal database, the customer list in a CSV file that the core business system writes out every night, and the records of opportunities and inquiries in Salesforce.
Business data like this can often be found only through the screens of each system.
With the Fess data store plugins, you can import this data record by record and search it from the same search page as the documents on your file servers and internal sites.

This article explains how to configure the import of each of the three sources, and how to narrow results by source, schedule the runs and check the results.
The steps common to all data stores, such as installing plugins, writing the handler name, parameters and script, and creating jobs, are covered in :doc:`datastore-basics`.
Read that article before continuing.
The settings in this article are based on Fess 15.9 and version 15.9.0 of each plugin.

What We Will Build
==================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Source
     - Plugin
     - Handler name
     - What to prepare in advance
   * - Database (product master)
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - The JDBC driver jar file, and a DB user that can only run SELECT
   * - CSV (customer list)
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - A directory the CSV files are written to (a location the crawler can read)
   * - Salesforce (accounts, opportunities, cases)
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - A connected app, and a key pair for signing the JWT

If you run Fess with Docker, list the three plugins, separated by spaces, in the ``environment`` of ``fess01`` in ``compose.yaml``.

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

If you install them from the admin console or with ``fess-setup``, you need to restart Fess.

Decide First: Who Can See the Results
=====================================

None of the three plugins carries the access rights (ACLs) of the original system over into Fess.
The roles of the imported documents are determined solely by the value of the "Permissions" field in the data store configuration.
This field contains ``{role}guest`` from the start, so as it is, even users who are not logged in can search the data.

For data that includes prices or customer information, change the field to the groups that should see it (e.g. ``{group}sales``).
All documents registered from one configuration get the same permissions.
Put data meant for different audiences into separate data store configurations.
For designing groups, see :doc:`guide-05`.

Database: Importing the Product Master
======================================

Placing the JDBC Driver
-----------------------

``fess-ds-db`` does not include any JDBC driver.
Obtain the driver jar file that matches your database (``postgresql-<version>.jar`` for PostgreSQL, ``mysql-connector-j-<version>.jar`` for MySQL) and put it on the crawler's class path.
Data store crawling runs in a crawler process separate from Fess itself, and its class path includes the jars in the following two directories.

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

With the ZIP package they are under the directory where you extracted Fess; with RPM / DEB they are under ``/usr/share/fess/``.
After placing the file, restart Fess.

In the Docker image, too, Fess is located in ``/usr/share/fess/``.
A jar copied into the container disappears when the container is recreated, so mount just the single jar file into ``fess01`` in ``compose.yaml``.

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

If you mount the whole directory, the jars that the image places in it become invisible, and the crawler can no longer start.
Always mount individual files.
After the change, recreate the containers with ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d``.

Parameters and SQL
------------------

Here we use a PostgreSQL ``products`` table as the example.
As the link target of the search results, we use the product master's lookup screen (e.g. ``https://erp.example.com/products/<product ID>``).
In [Crawler] > [Data Store] > [Create New], select ``DatabaseDataStore`` as the handler name and set the parameters as follows.

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

The script is as follows.

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

Write ``sql`` on a single line.
The SQL is sent to the database as is, and each row of the result becomes one document.
If you build the link URL and the body inside the SQL, the script only needs to list column names.
``concat_ws`` skips NULL columns when concatenating, so the body does not become NULL even for products with an empty description.
In MySQL, ``CONCAT_WS`` behaves the same way, but ``CONCAT`` returns NULL for the whole result if any argument is NULL.

If you run Fess with Docker, ``localhost`` in ``url`` refers to the Fess container itself, not to the database server.
Write the host name or IP address of the database.

Mapping Column Names to the Script
----------------------------------

On the right-hand side of the script, write the column labels of the SELECT result (the aliases given with ``AS``) as they are.
Keep the following three points in mind.

- The case of column labels depends on the database. PostgreSQL turns unquoted aliases into lowercase, Oracle and H2 into uppercase, and MySQL returns them as written. In the script, use exactly the case the database returns. If they do not match, the field gets no value
- The values of the parameters field are also visible to the script as variables with the same names. If you write ``url=url`` while the result has no ``url`` column, the JDBC connection URL becomes the document's URL. Give the link column a name that does not clash with a parameter, such as ``page_url``
- A hung query does not stop even if you stop the job. Always set ``query_timeout`` (in seconds)

``fess-ds-db`` has no option for incremental crawling.
Each run executes the entire ``sql`` and registers all rows again.
For tables with many rows, run the job at a time when the database load is low (see "Creating a Job for Each Source" below).

CSV: Importing the Customer List Written Out by the Core System
===============================================================

The basic use of the CSV connector is explained in the CSV file example in :doc:`datastore-basics`.
Here we only add the points you need when importing CSV files that the core business system writes out periodically.

As an example, suppose the core system, a Japanese one, writes out a ``customers_20261128.csv`` like the following every night at 2:00.
The encoding is MS932 (the Windows variant of Shift_JIS), and the first row holds Japanese headings (customer code, customer name, location, responsible department, business status).

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

Where to Put the Files
----------------------

Write the CSV files to a path that can be read from the server where the Fess crawler runs.
With Docker, mount the output directory into ``fess01`` read-only.

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

Parameters and Script
---------------------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- When you specify ``directories``, all files with the extension ``.csv`` / ``.tsv`` in that directory are read, oldest modification time first. If a file with a date in its name is written out every day, you do not have to rewrite the parameters. If you leave old files in place, their rows are also read every time
- CSV files written out by Japanese Excel or by systems built for Japanese Windows are usually MS932. If you specify ``Shift_JIS``, characters such as ``①`` and ``㈱`` become replacement characters, so specify ``MS932``
- Even when the headings are non-ASCII, as in this Japanese example, ``has_header_line=true`` skips the first row. In the script, referring to columns by number (``cell1``, ``cell2`` ...) is the reliable way. Columns whose headings contain spaces or symbols cannot be referred to by heading name
- For tab-separated files, add ``separator_character=\t``
- Rows whose ``url`` becomes ``null`` are not registered. In this example, customers whose status is 取引終了 (ended) are excluded, and only 取引中 (active) ones are registered. The number of excluded rows is logged in ``fess-crawler.log`` as a WARN: ``Skipped 1 row(s) in ... because the script did not set the url field.``

If the crawler reads a file that is still being written, only the rows written so far are registered.
Run the job after the time the CSV export finishes.

Salesforce: Importing Accounts, Opportunities and Cases
=======================================================

Preparing Salesforce
--------------------

``fess-ds-salesforce`` supports two authentication methods: ``auth_type=oauth_token`` (JWT bearer flow) and ``auth_type=oauth_password`` (user name and password).
Here we use ``oauth_token``, which does not require storing a password.
The username-password OAuth flow used by ``oauth_password`` may be disabled, depending on the settings of your Salesforce org.

1. Create a key pair and a certificate

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. In Salesforce Setup, create a connected app, enable OAuth settings, and upload ``certificate.crt`` under "Use digital signatures". Select the OAuth scopes as described in the reference
3. In the connected app's policies, set "Permitted Users" to "Admin approved users are pre-authorized", and assign the profile or permission set of the user used for crawling
4. Note down the connected app's consumer key

Salesforce's screens and names may change, so also check the description of the JWT bearer flow in the Salesforce help for details.

Fess can import only the records and fields that the user used for crawling can read.
If you specify a field that user cannot read in ``contents`` (described below), retrieval of that object fails.

Parameters and Script
---------------------

For ``private_key``, write the contents of ``private_key.pem`` on a single line, replacing line breaks with ``\n``.
The plugin can read only the PKCS#8 format (the format that starts with ``-----BEGIN PRIVATE KEY-----``).
A key that starts with ``-----BEGIN RSA PRIVATE KEY-----``, created by older OpenSSL versions, must first be converted with ``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem``.

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

To target a sandbox, set ``base_url=https://test.salesforce.com``.

Every item on the right-hand side starts with ``object.``.
If you write it without the prefix, as in ``url=url``, evaluating the expression fails, and the record is not registered but recorded as a failure URL.
``object.url`` has the form ``<instance URL>/<record ID>``, and clicking it opens the record page in Salesforce.

Narrowing What Is Imported
--------------------------

``fess-ds-salesforce`` always reads all 23 kinds of standard objects, including Account, Contact, Lead, Opportunity, Case, Task and User.
There is no setting for reading only selected objects.
To narrow the scope, combine the following three.

- ``include_pattern`` / ``exclude_pattern``: regular expressions matched against the whole ``object.url`` that select which records are registered. The first three characters of a Salesforce record ID are fixed per object (Account ``001``, Opportunity ``006``, Case ``500``, and so on). The example above registers only these three kinds. Retrieval itself still runs for all objects; the other records are just discarded before registration
- ``<object name>.title`` / ``<object name>.contents``: specify the fields used for the title and body by their API names. Standard object names are in upper snake case, such as ``ACCOUNT``, ``OPPORTUNITY`` and ``CASE``. If you do not specify them, the plugin's default fields are used
- ``custom``: specify the API names of custom objects, comma-separated, to read them in addition to the standard objects

Custom objects have no default fields, so always specify ``.title`` and ``.contents``.
Include the title field in the body fields as well.
The plugin retrieves only the fields written in ``.contents`` and the like, so a field written only in ``.title`` is not retrieved, and the title ends up empty.

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

Narrowing by Source with Labels
===============================

In the examples so far, the script's ``label`` assigns ``products``, ``customers`` and ``salesforce``.
To show them as label choices on the search page, create labels with the same "Value" in [Crawler] > [Label] ("Included Paths" can be left empty).
Label values can contain only alphanumeric characters and ``_``.

To split Salesforce data by object, create labels whose "Included Paths" look at the first three characters of the record ID, instead of using the script's ``label``.
For example, a label with the value ``sf_case`` and the included path ``https://example\.my\.salesforce\.com/500.*`` is assigned only to cases.
If a label matches the URL, the label assigned by the script is lost.
Use only one of the two methods in a single data store configuration (for details, see the section on labels in :doc:`datastore-basics`).

Creating a Job for Each Source
==============================

In the initial state, "Default Crawler" crawls all configurations together every day at 0:00.
Each source has its own convenient time, so create a job for each data store configuration.
On the details page of each configuration, click [Create New Job] and enter the time in cron format in "Schedule" (for the steps, see the section on scheduling in :doc:`datastore-basics`).

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Source
     - Example schedule
     - Considerations
   * - Database
     - ``0 3 * * *``
     - All rows are read every time, so choose a time when the database load is low
   * - CSV
     - ``30 2 * * *``
     - Schedule it after the time the export finishes
   * - Salesforce
     - ``0 7,12,18 * * *``
     - Each run creates one Bulk API job per standard and custom object. Decide the frequency based on how much of the org's API limit remains

Default Crawler also continues to crawl these configurations.
If you do not want them to run twice, set the "Status" of the data store configuration to "Disabled" (a job that specifies a configuration ID crawls the configuration even when it is disabled).

Handling Rows That Disappear from the Source Data
=================================================

Even if you delete a row from the database, or a row disappears from the CSV, the corresponding document is not deleted on the next crawl.
Documents registered by a data store get an expiration date, which is extended each time they are registered.
A document that is no longer registered is deleted automatically once the number of days in "Delete old documents" under [System] > [General] (3 days by default) has passed since it was last registered.

This mechanism also has a side that needs care.
If the database cannot be reached for several days in a row and that number of days passes, all documents of that configuration disappear from the search results.
Detect import failures early, using the methods in the next section.

Checking the Results
====================

How to read the job log, [System Info] > [Crawling Info], failure URLs and ``fess-crawler.log`` is explained in the section on checking the results in :doc:`datastore-basics`.
Data store crawling can end with the job showing "OK" even if the import failed, so judge by the document counts and the logs.

1. In [System Info] > [Search], search for ``label:products``, ``label:customers`` and ``label:salesforce``, and compare the counts with the source data (for a database, a ``SELECT count(*)`` with the same conditions as ``sql``)
2. Check the WARN and ERROR entries in ``fess-crawler.log``. With the setup in this article, the following messages are the most likely

   - ``The JDBC driver ... is not on the crawler classpath.``: the driver's location or the class name in ``driver`` is wrong
   - ``Failed to connect to ...``: check the database's host name, port, user name and password
   - ``is not a directory.`` or ``No CSV file.``: there is no CSV file readable by the crawler at the ``directories`` path
   - ``Batch:... Failed caused by ...``: some Salesforce objects could not be retrieved. Check the field names in ``.contents`` and the field permissions of the user used for crawling
   - ``Failed to process a data crawling: <configuration name>``: the whole configuration failed. For Salesforce, authentication failures fall into this case. Check the cause in the stack trace that follows

3. For configurations whose "Permissions" field you changed, log in as a user of the target group and confirm that the documents appear in the search results, and that they do not appear when logged out

Summary
=======

- None of the three plugins carries over the permissions of the original system, so change ``{role}guest`` in the "Permissions" field to the groups that should see the data
- For a database, put the JDBC driver on the crawler's class path and build the link URL and the body in SQL. All rows are read every time
- Read CSV files from the core system with ``directories`` and ``file_encoding=MS932``, and refer to columns with ``cellN``. Rows whose ``url`` is set to ``null`` are not registered
- Write the Salesforce script with ``object.*``. Standard objects cannot be selected, so narrow the scope with ``include_pattern`` and ``<object name>.contents``
- Create a job for each source, and operate on the assumption that rows removed from the source data disappear after the number of days in "Delete old documents"

What to Read Next
=================

- The common mechanisms of data stores (scripts, permissions, labels, checking the results): :doc:`datastore-basics`
- To import Git, Confluence, Jira and Slack: :doc:`guide-06`
- To import Google Drive, SharePoint and Box: :doc:`guide-07`
- To show different search results per department: :doc:`guide-05`
- To monitor import failures: :doc:`guide-10`

References
==========

- `Database Connector <https://fess.codelibs.org/stable/config/datastore/ds-database.html>`__
- `CSV Connector <https://fess.codelibs.org/stable/config/datastore/ds-csv.html>`__
- `Salesforce Connector <https://fess.codelibs.org/stable/config/datastore/ds-salesforce.html>`__
- `Data Store Configuration <https://fess.codelibs.org/stable/admin/dataconfig-guide.html>`__
- `Scheduler <https://fess.codelibs.org/stable/admin/scheduler-guide.html>`__
- `Label <https://fess.codelibs.org/stable/admin/labeltype-guide.html>`__
- `General <https://fess.codelibs.org/stable/admin/general-guide.html>`__
