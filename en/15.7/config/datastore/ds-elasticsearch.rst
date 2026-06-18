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
     - ElasticsearchDataStore / ElasticsearchListDataStore
   * - Enabled
     - On

.. note::
   ``ElasticsearchListDataStore`` is an extension of ``ElasticsearchDataStore`` that processes
   retrieved data as a file list and supports multi-threaded index registration.
   The number of threads can be specified with the ``numOfThreads`` parameter (default: 1).

Parameter Settings
------------------

Basic connection:

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    size=100
    scroll=1m

Authenticated connection:

::

    settings.http.hosts=https://elasticsearch.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=myindex
    size=100
    scroll=1m

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Parameter
     - Required
     - Description
   * - ``settings.http.hosts``
     - No
     - Host URL of Elasticsearch/OpenSearch. Multiple hosts can be specified with comma separation (e.g., ``http://host1:9200,http://host2:9200``). A connection error will occur if not specified
   * - ``settings.fesen.username``
     - No
     - Authentication username
   * - ``settings.fesen.password``
     - No
     - Authentication password
   * - ``index``
     - No
     - Target index name (default: ``_all``). Multiple indices can be specified with comma separation
   * - ``size``
     - No
     - Number of documents to retrieve per scroll (if unspecified, the Elasticsearch/OpenSearch server default is used)
   * - ``scroll``
     - No
     - Scroll timeout (default: 1m)
   * - ``timeout``
     - No
     - Request timeout (default: 1m)
   * - ``query``
     - No
     - Query JSON (default: match_all). Specify query body only (outer ``{"query":...}`` wrapper is not needed)
   * - ``fields``
     - No
     - Fields to retrieve (comma-separated)
   * - ``preference``
     - No
     - Shard replica preference for search execution (default: ``_local``)
   * - ``delete.processed.doc``
     - No
     - Whether to delete processed documents from source index (default: false)
   * - ``readInterval``
     - No
     - Wait time between processing each document in milliseconds (default: 0)
   * - ``numOfThreads``
     - No
     - Number of threads for index registration (valid for ``ElasticsearchListDataStore`` only, default: 1)

Additional Connection Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters with the ``settings.`` prefix are passed as configuration to the internal
Elasticsearch/OpenSearch client (fesen HTTP client). The main additional settings are as follows.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Parameter
     - Description
   * - ``settings.http.ssl.certificate_authorities``
     - Path to the CA certificate file (X.509 format) to trust for HTTPS connections
   * - ``settings.http.compression``
     - Whether to enable HTTP compression (default: true)
   * - ``settings.http.proxy_host``
     - Proxy server hostname (``settings.https.proxy_host`` also works)
   * - ``settings.http.proxy_port``
     - Proxy server port number (``settings.https.proxy_port`` also works)
   * - ``settings.http.proxy_username``
     - Proxy authentication username (``settings.https.proxy_username`` also works)
   * - ``settings.http.proxy_password``
     - Proxy authentication password (``settings.https.proxy_password`` also works)

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
- ``version`` - Document version
- ``seqNo`` - Sequence number
- ``primaryTerm`` - Primary term
- ``clusterAlias`` - Cluster alias (for cross-cluster search)
- ``hit`` - SearchHit object (advanced usage)

Query Configuration
===================

Retrieve All Documents
----------------------

By default, all documents are retrieved.
If the ``query`` parameter is not specified, ``match_all`` is used.

Filtering with Specific Conditions
-----------------------------------

::

    query={"term":{"status":"published"}}

Range query:

::

    query={"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}

Multiple conditions:

::

    query={"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}

.. note::
   The ``query`` parameter accepts only the query body. The outer ``{"query":...}`` wrapper is not needed.
   Search-level options such as sort cannot be specified in this parameter.

Retrieving Specific Fields Only
================================

Limiting fields with the fields parameter
------------------------------------------

::

    settings.http.hosts=http://localhost:9200
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

    settings.http.hosts=http://localhost:9200
    index=articles
    size=100
    scroll=1m

Script:

::

    url=source.url
    title=source.title
    content=source.content
    created=source.created_at
    last_modified=source.updated_at

Authenticated Cluster Crawl
----------------------------

Parameters:

::

    settings.http.hosts=https://es.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=products
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
-----------------------

Parameters:

::

    settings.http.hosts=http://localhost:9200
    index=logs-2024-*
    query={"term":{"level":"error"}}
    size=100

Script:

::

    url="https://logs.example.com/view/" + id
    title=source.message
    content=source.stack_trace
    digest=source.service + " - " + source.level
    last_modified=source.timestamp

OpenSearch Cluster Crawl
-------------------------

Parameters:

::

    settings.http.hosts=https://opensearch.example.com:9200
    settings.fesen.username=admin
    settings.fesen.password=admin
    index=documents
    size=100
    scroll=1m

Script:

::

    url=source.url
    title=source.title
    content=source.body
    last_modified=source.modified_date

Crawl with Limited Fields
--------------------------

Parameters:

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    size=100

Script:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Load Balancing Across Multiple Hosts
--------------------------------------

Specifying multiple hosts in ``settings.http.hosts`` with comma separation distributes
requests across each host.

Parameters:

::

    settings.http.hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=1m

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
---------------------

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

       size=100
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
------------------------

.. warning::
   Use properly signed certificates in production environments.

Method 1: Specify the CA certificate with the ``settings.http.ssl.certificate_authorities`` parameter (recommended)

Specify the path to the CA certificate file (X.509 format) to trust. This method does not affect the |Fess|-wide keystore.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.ssl.certificate_authorities=/path/to/es-cert.crt
    index=myindex

Method 2: Add certificate to Java keystore

Add the certificate to the trust store of the JVM that starts |Fess|.

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Connecting via Proxy
---------------------

To connect through a proxy server, specify ``settings.http.proxy_host`` and ``settings.http.proxy_port``.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.proxy_host=proxy.example.com
    settings.http.proxy_port=8080
    index=myindex

Advanced Query Examples
=======================

Query with Aggregation
-----------------------

.. note::
   The ``query`` parameter accepts only the query body. Aggregations (aggs), sort, and other
   search-level options cannot be specified. Only documents are retrieved.

Script Fields
-------------

.. note::
   Elasticsearch/OpenSearch script fields are not included in ``_source``, so they cannot be
   accessed via the ``source.*`` prefix. To use script fields, access them via the ``hit``
   object using ``hit.getFields()``.

Reference
=========

- :doc:`ds-overview` - DataStore Connector Overview
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
