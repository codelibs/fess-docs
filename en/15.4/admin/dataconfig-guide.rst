===============
Data Store Crawling
===============

Overview
========

|Fess| supports crawling data sources such as databases and CSV files.
This section describes the data store configuration required for this functionality.

Configuration Management
========================

Display Method
--------------

To open the Data Store configuration list page shown below, click [Crawler > Data Store] in the left menu.

|image0|

Click the configuration name to edit it.

Creating a Configuration
------------------------

Click the "Create New" button to open the Data Store configuration page.

|image1|

Configuration Options
---------------------

Name
::::

Specifies the name of the crawl configuration.

Handler Name
::::::::::::

The handler name for processing the data store.

* DatabaseDataStore: Crawls a database
* CsvDataStore: Crawls CSV/TSV files
* CsvListDataStore: Crawls a CSV file containing file paths to index

Parameters
::::::::::

Specifies parameters related to the data store.

Script
::::::

Specifies which fields to assign values retrieved from the data store.
Expressions can be written in Groovy.

Boost Value
:::::::::::

Specifies the boost value for documents crawled with this configuration.

Permissions
:::::::::::

Specifies permissions for this configuration.
The permission format is as follows: to display search results to users in the developer group, specify {group}developer.
User-level: {user}username, Role-level: {role}rolename, Group-level: {group}groupname.

Virtual Host
::::::::::::

Specifies the virtual host hostname.
For details, see :doc:`Virtual Hosts in the Configuration Guide <../config/virtual-host>`.

Status
::::::

Specifies whether to use this crawl configuration.

Description
:::::::::::

Enter a description.

Deleting a Configuration
------------------------

Click the configuration name on the list page, then click the "Delete" button to display a confirmation screen.
Click the "Delete" button to remove the configuration.

Examples
========

DatabaseDataStore
-----------------

This section describes database crawling.

As an example, assume the following table exists in a MySQL database named "testdb," and you can connect using username "hoge" and password "fuga".

::

    CREATE TABLE doc (
        id BIGINT NOT NULL AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        content VARCHAR(255) NOT NULL,
        latitude VARCHAR(20),
        longitude VARCHAR(20),
        versionNo INTEGER NOT NULL,
        PRIMARY KEY (id)
    );

Here, populate the table with the following data:

::

    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 1', 'コンテンツ 1 です．', '37.77493', ' -122.419416', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 2', 'コンテンツ 2 です．', '34.701909', '135.494977', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 3', 'コンテンツ 3 です．', '-33.868901', '151.207091', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 4', 'コンテンツ 4 です．', '51.500152', '-0.113736', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 5', 'コンテンツ 5 です．', '35.681137', '139.766084', 1);

Parameters
::::::::::

An example parameter configuration is as follows:

::

    driver=com.mysql.jdbc.Driver
    url=jdbc:mysql://localhost:3306/testdb?useUnicode=true&characterEncoding=UTF-8
    username=hoge
    password=fuga
    sql=select * from doc

Parameters are in "key=value" format. Key descriptions are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - driver
     - Driver class name
   * - url
     - URL
   * - username
     - Username for DB connection
   * - password
     - Password for DB connection
   * - sql
     - SQL statement to retrieve crawl targets

Table: DB Configuration Parameters Example


Script
::::::

An example script configuration is as follows:
::

    url="http://SERVERNAME/" + id
    host="SERVERNAME"
    site="SERVERNAME"
    title=title
    content=content
    cache=content
    digest=content
    anchor=
    content_length=content.length()
    last_modified=new java.util.Date()
    location=latitude + "," + longitude
    latitude=latitude
    longitude=longitude

Parameters are in "key=value" format. Key descriptions are as follows:

Values are written in Groovy.
Enclose strings in double quotation marks. Access database column names to retrieve their values.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - url
     - URL (Set an accessible URL to the data for your environment)
   * - host
     - Hostname
   * - site
     - Site path
   * - title
     - Title
   * - content
     - Document content (indexed text)
   * - cache
     - Document cache (not indexed)
   * - digest
     - Digest portion displayed in search results
   * - anchor
     - Links contained in the document (normally not necessary)
   * - content_length
     - Document length
   * - last_modified
     - Last modified date of the document

Table: Script Configuration


Driver
::::::

A driver is required to connect to the database. Place the jar file in app/WEB-INF/lib.

CsvDataStore
------------

This section describes crawling CSV files.

For example, create a test.csv file with the following content in the /home/taro/csv directory.
Set the file encoding to Shift_JIS.

::

    1,Title 1,This is test 1.
    2,Title 2,This is test 2.
    3,Title 3,This is test 3.
    4,Title 4,This is test 4.
    5,Title 5,This is test 5.
    6,Title 6,This is test 6.
    7,Title 7,This is test 7.
    8,Title 8,This is test 8.
    9,Title 9,This is test 9.

Parameters
::::::::::

Here's an example of parameter configuration:

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

Parameters are in "key=value" format. Key descriptions are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - directories
     - Directory containing CSV files (.csv or .tsv)
   * - files
     - CSV files (for direct specification)
   * - fileEncoding
     - CSV file encoding
   * - separatorCharacter
     - Separator character

Table: CSV File Configuration Parameters Example


Script
::::::

An example script configuration is as follows:

::

    url="http://SERVERNAME/" + cell1
    host="SERVERNAME"
    site="SERVERNAME"
    title=cell2
    content=cell3
    cache=cell3
    digest=cell3
    anchor=
    content_length=cell3.length()
    last_modified=new java.util.Date()

Parameters are in "key=value" format.
Keys are the same as for database crawling.
CSV file data is stored in cell[number] format (numbers start from 1).
Cells with no data may be null.

EsDataStore
-----------

The data source is Elasticsearch, but the basic usage is the same as CsvDataStore.

Parameters
::::::::::

An example parameter configuration is as follows:

::

    settings.cluster.name=elasticsearch
    hosts=SERVERNAME:9300
    index=logindex
    type=data

Parameters are in "key=value" format. Key descriptions are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - settings.*
     - Elasticsearch Settings information
   * - hosts
     - Elasticsearch connection destination
   * - index
     - Index name
   * - type
     - Type name
   * - query
     - Query for retrieval conditions

Table: Elasticsearch Configuration Parameters Example


Script
::::::

An example script configuration is as follows:

::

    url=source.url
    host="SERVERNAME"
    site="SERVERNAME"
    title=source.title
    content=source.content
    digest=
    anchor=
    content_length=source.size
    last_modified=new java.util.Date()

Parameters are in "key=value" format.
Keys are the same as for database crawling.
Values can be retrieved and set using source.*.

CsvListDataStore
----------------

Use this when crawling a large number of files.
By placing a CSV file containing the paths of updated files and crawling only the specified paths, you can shorten crawl execution time.

The format for specifying paths is as follows:

::

    [Action]<Separator>[Path]

Specify one of the following actions:

* create: File was created
* modify: File was updated
* delete: File was deleted

For example, create a test.csv file with the following content in the /home/taro/csv directory.
Set the file encoding to Shift_JIS.

Paths are specified in the same format as when specifying file crawl paths.
Specify like "file:/[path]" or "smb://[path]".

::

    modify,smb://servername/data/testfile1.txt
    modify,smb://servername/data/testfile2.txt
    modify,smb://servername/data/testfile3.txt
    modify,smb://servername/data/testfile4.txt
    modify,smb://servername/data/testfile5.txt
    modify,smb://servername/data/testfile6.txt
    modify,smb://servername/data/testfile7.txt
    modify,smb://servername/data/testfile8.txt
    modify,smb://servername/data/testfile9.txt
    modify,smb://servername/data/testfile10.txt


Parameters
::::::::::

An example parameter configuration is as follows:

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

Parameters are in "key=value" format. Key descriptions are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - directories
     - Directory containing CSV files (.csv or .tsv)
   * - fileEncoding
     - CSV file encoding
   * - separatorCharacter
     - Separator character

Table: CSV File Configuration Parameters Example


Script
::::::

An example script configuration is as follows:

::

    event_type=cell1
    url=cell2

Parameters are in "key=value" format.
Keys are the same as for database crawling.

If authentication is required at the crawl destination, the following settings are also necessary:

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

.. |image0| image:: ../../../resources/images/en/15.4/admin/dataconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/dataconfig-2.png
