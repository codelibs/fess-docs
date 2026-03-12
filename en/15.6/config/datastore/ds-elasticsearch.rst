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

    hosts=http://localhost:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

Authenticated connection:

::

    hosts=https://elasticsearch.example.com:9200
    index=myindex
    username=elastic
    password=changeme
    scroll_size=100
    scroll_timeout=5m

Multiple hosts:

::

    hosts=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``hosts``
     - Yes
     - Elasticsearch/OpenSearch hosts (comma-separated for multiple)
   * - ``index``
     - Yes
     - Target index name
   * - ``username``
     - No
     - Authentication username
   * - ``password``
     - No
     - Authentication password
   * - ``scroll_size``
     - No
     - Number of documents per scroll (default: 100)
   * - ``scroll_timeout``
     - No
     - Scroll timeout (default: 5m)
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

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Accessing nested fields:

::

    url=data.metadata.url
    title=data.title
    content=data.body.content
    author=data.author.name
    created=data.created_at
    last_modified=data.updated_at

Available Fields
~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - Elasticsearch document field
- ``data._id`` - Document ID
- ``data._index`` - Index name
- ``data._type`` - Document type (Elasticsearch < 7)
- ``data._score`` - Search score

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

    hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    scroll_size=100

To retrieve all fields, do not specify ``fields`` or leave it empty.

Usage Examples
==============

Basic Index Crawl
-----------------

Parameters:

::

    hosts=http://localhost:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

Script:

::

    url=data.url
    title=data.title
    content=data.content
    created=data.created_at
    last_modified=data.updated_at

Authenticated Cluster Crawl
---------------------------

Parameters:

::

    hosts=https://es.example.com:9200
    index=products
    username=elastic
    password=changeme
    scroll_size=200
    scroll_timeout=10m

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " " + data.specifications
    digest=data.category
    last_modified=data.updated_at

Multiple Indices Crawl
----------------------

Parameters:

::

    hosts=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    scroll_size=100

Script:

::

    url="https://logs.example.com/view/" + data._id
    title=data.message
    content=data.stack_trace
    digest=data.service + " - " + data.level
    last_modified=data.timestamp

OpenSearch Cluster Crawl
------------------------

Parameters:

::

    hosts=https://opensearch.example.com:9200
    index=documents
    username=admin
    password=admin
    scroll_size=100
    scroll_timeout=5m

Script:

::

    url=data.url
    title=data.title
    content=data.body
    last_modified=data.modified_date

Crawl with Limited Fields
-------------------------

Parameters:

::

    hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    scroll_size=100

Script:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Load Balancing with Multiple Hosts
----------------------------------

Parameters:

::

    hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

Script:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

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

1. Increase ``scroll_timeout``:

   ::

       scroll_timeout=10m

2. Decrease ``scroll_size``:

   ::

       scroll_size=50

3. Check cluster resources

Large Data Crawl
----------------

**Symptom**: Crawl is slow or times out

**Solution**:

1. Adjust ``scroll_size`` (too large can slow down):

   ::

       scroll_size=100  # Default
       scroll_size=500  # Larger

2. Limit fields with ``fields``
3. Filter documents with ``query``
4. Split into multiple data stores (by index, time range, etc.)

Out of Memory
-------------

**Symptom**: OutOfMemoryError

**Solution**:

1. Decrease ``scroll_size``
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

    url=data.full_url
    title=data.title
    content=data.content

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_

