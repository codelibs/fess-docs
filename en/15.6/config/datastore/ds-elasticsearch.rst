==================================
Elasticsearch/OpenSearch Connector
==================================

Overview
========

The Elasticsearch/OpenSearch Connector provides functionality to retrieve data from
Elasticsearch or OpenSearch clusters and register it in the |Fess| index.

This feature requires the ``fess-ds-elasticsearch`` plugin.

Supported Versions
==================

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

Prerequisites
=============

1. Plugin installation is required
2. Read access to the Elasticsearch/OpenSearch cluster is required
3. Query execution permissions are required

Plugin Installation
-------------------

Method 1: Place JAR file directly

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # Place the file
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - External Elasticsearch
   * - Handler Name
     - ElasticsearchDataStore
   * - Enabled
     - On

Parameter Settings
------------------

Basic connection:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    size=100
    scroll=5m

Authenticated connection:

::

    settings.fesen.http.url=https://elasticsearch.example.com:9200
    index=myindex
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=100
    scroll=5m

Multiple hosts:

::

    settings.fesen.http.url=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    size=100
    scroll=5m

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``settings.fesen.http.url``
     - Yes
     - Elasticsearch/OpenSearch hosts (comma-separated for multiple)
   * - ``index``
     - Yes
     - Target index name
   * - ``settings.fesen.username``
     - No
     - Authentication username
   * - ``settings.fesen.password``
     - No
     - Authentication password
   * - ``size``
     - No
     - Number of documents per scroll (default: 100)
   * - ``scroll``
     - No
     - Scroll timeout (default: 1m)
   * - ``query``
     - No
     - Query JSON (default: match_all)
   * - ``fields``
     - No
     - Fields to retrieve (comma-separated)

Script Settings
---------------

Basic mapping:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Accessing nested fields:

::

    url=source.metadata.url
    title=source.title
    content=source.body.content
    author=source.author.name
    created=source.created_at
    last_modified=source.updated_at

Available Fields
~~~~~~~~~~~~~~~~

- ``source.<field_name>`` - Elasticsearch document ``_source`` field
- ``id`` - Document ID
- ``index`` - Index name
- ``score`` - Search score

Query Configuration
===================

Retrieve All Documents
----------------------

By default, all documents are retrieved.
If the ``query`` parameter is not specified, ``match_all`` is used.

Filtering with Specific Conditions
----------------------------------

::

    query={"query":{"term":{"status":"published"}}}

Range query:

::

    query={"query":{"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}}

Multiple conditions:

::

    query={"query":{"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}}

Sorting:

::

    query={"query":{"match_all":{}},"sort":[{"timestamp":{"order":"desc"}}]}

Retrieving Specific Fields Only
===============================

Limiting fields with fields parameter
-------------------------------------

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

To retrieve all fields, do not specify ``fields`` or leave it empty.

Usage Examples
==============

Basic Index Crawl
-----------------

Parameters:

::

    settings.fesen.http.url=http://localhost:9200
    index=articles
    size=100
    scroll=5m

Script:

::

    url=source.url
    title=source.title
    content=source.content
    created=source.created_at
    last_modified=source.updated_at

Authenticated Cluster Crawl
---------------------------

Parameters:

::

    settings.fesen.http.url=https://es.example.com:9200
    index=products
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=200
    scroll=10m

Script:

::

    url="https://shop.example.com/product/" + source.product_id
    title=source.name
    content=source.description + " " + source.specifications
    digest=source.category
    last_modified=source.updated_at

Multiple Indices Crawl
----------------------

Parameters:

::

    settings.fesen.http.url=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    size=100

Script:

::

    url="https://logs.example.com/view/" + id
    title=source.message
    content=source.stack_trace
    digest=source.service + " - " + source.level
    last_modified=source.timestamp

OpenSearch Cluster Crawl
------------------------

Parameters:

::

    settings.fesen.http.url=https://opensearch.example.com:9200
    index=documents
    settings.fesen.username=admin
    settings.fesen.password=admin
    size=100
    scroll=5m

Script:

::

    url=source.url
    title=source.title
    content=source.body
    last_modified=source.modified_date

Crawl with Limited Fields
-------------------------

Parameters:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    size=100

Script:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Load Balancing with Multiple Hosts
----------------------------------

Parameters:

::

    settings.fesen.http.url=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=5m

Script:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Troubleshooting
===============

Connection Error
----------------

**Symptom**: ``Connection refused`` or ``No route to host``

**Check**:

1. Verify host URL is correct (protocol, hostname, port)
2. Verify Elasticsearch/OpenSearch is running
3. Check firewall settings
4. For HTTPS, verify certificate is valid

Authentication Error
--------------------

**Symptom**: ``401 Unauthorized`` or ``403 Forbidden``

**Check**:

1. Verify username and password are correct
2. Verify user has appropriate permissions:

   - Read permission on index
   - Scroll API usage permission

3. If Elasticsearch Security (X-Pack) is enabled, verify proper configuration

Index Not Found
---------------

**Symptom**: ``index_not_found_exception``

**Check**:

1. Verify index name is correct (including case)
2. Verify index exists:

   ::

       GET /_cat/indices

3. Verify wildcard pattern is correct (e.g., ``logs-*``)

Query Error
-----------

**Symptom**: ``parsing_exception`` or ``search_phase_execution_exception``

**Check**:

1. Verify query JSON is correct
2. Verify query is compatible with Elasticsearch/OpenSearch version
3. Verify field names are correct
4. Test query directly on Elasticsearch/OpenSearch:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

Scroll Timeout
--------------

**Symptom**: ``No search context found`` or ``Scroll timeout``

**Solution**:

1. Increase ``scroll``:

   ::

       scroll=10m

2. Decrease ``size``:

   ::

       size=50

3. Check cluster resources

Large Data Crawl
----------------

**Symptom**: Crawl is slow or times out

**Solution**:

1. Adjust ``size`` (too large can slow down):

   ::

       size=100  # Default
       size=500  # Larger

2. Limit fields with ``fields``
3. Filter documents with ``query``
4. Split into multiple data stores (by index, time range, etc.)

Out of Memory
-------------

**Symptom**: OutOfMemoryError

**Solution**:

1. Decrease ``size``
2. Limit fields with ``fields``
3. Increase |Fess| heap size
4. Exclude large fields (binary data, etc.)

SSL/TLS Connection
==================

Self-Signed Certificate
-----------------------

.. warning::
   Use properly signed certificates in production environments.

For self-signed certificates, add certificate to Java keystore:

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Client Certificate Authentication
---------------------------------

For client certificate authentication, additional parameter configuration is required.
Refer to Elasticsearch client documentation for details.

Advanced Query Examples
=======================

Query with Aggregation
----------------------

.. note::
   Aggregation results are not retrieved, only documents.

::

    query={"query":{"match_all":{}},"aggs":{"categories":{"terms":{"field":"category"}}}}

Script Fields
-------------

::

    query={"query":{"match_all":{}},"script_fields":{"full_url":{"script":"doc['protocol'].value + '://' + doc['host'].value + doc['path'].value"}}}

Script:

::

    url=source.full_url
    title=source.title
    content=source.content

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_

