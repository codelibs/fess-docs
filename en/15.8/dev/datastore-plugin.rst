==================================
Data Store Plugin Development
==================================

Overview
========

By developing a Data Store plugin, you can add functionality to |Fess| for
retrieving content from new data sources. A Data Store retrieves records from
external systems such as databases, APIs, and files, converts them into index
fields according to the mapping script configured in the admin console, and
registers them into the |Fess| index.

Published connectors (``fess-ds-*``) for CSV, JSON, databases, Git, and
various cloud services are all implemented using this mechanism. Because
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ is published
as an implementation template, the easiest way to create a new connector is
to copy it as a starting point.

Basic Structure
===============

A Data Store plugin consists of the following three parts:

- Create a class that extends ``AbstractDataStore``
- Implement the two methods ``getName()`` and ``storeData()``
- Register it as a component in ``fess_ds++.xml``

Minimum Implementation
----------------------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // Used as the handler name. Convention is to return the class's simple name
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Implement data retrieval and processing here
        }
    }

.. note::

   Both ``getName()`` and ``storeData()`` are ``protected`` abstract methods.
   Note that in |Fess| 15.x, the package for ``DataConfig`` is
   ``org.codelibs.fess.opensearch.config.exentity`` (the former
   ``org.codelibs.fess.es.config.exentity`` has been removed).

Component Registration
----------------------

To make |Fess| recognize the Data Store you created, register the component
in ``src/main/resources/fess_ds++.xml``.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

With ``<postConstruct name="register">``, the ``register()`` method inherited
from ``AbstractDataStore`` is automatically invoked after the component is
created, registering itself with the ``DataStoreFactory``. The name
registered at this time is the return value of ``getName()`` (``ExampleDataStore``
in the example above), and this becomes the "handler name" selected in the
Data Store settings in the admin console.

AbstractDataStore
=================

Main Methods
------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Method
     - Category
     - Description
   * - ``getName()``
     - Implementation (required)
     - Abstract method that returns the Data Store's handler name. Convention
       is to return ``getClass().getSimpleName()``
   * - ``storeData()``
     - Implementation (required)
     - Abstract method that performs data retrieval, conversion, and index
       registration
   * - ``register()``
     - Inherited (normally no changes needed)
     - Automatically invoked from the ``postConstruct`` in ``fess_ds++.xml``
       and registers with ``DataStoreFactory``
   * - ``store()``
     - Inherited (called by the framework)
     - The entry point invoked by the framework. Prepares ``defaultDataMap``
       and other data, then calls ``storeData()``
   * - ``convertValue()``
     - Inherited (helper)
     - Evaluates the value (template) in ``scriptMap`` using the script engine
   * - ``getScriptType()``
     - Inherited (helper)
     - Retrieves the ``script_type`` parameter (default is Groovy)
   * - ``getReadInterval()``
     - Inherited (helper)
     - Retrieves the ``readInterval`` parameter (in milliseconds)
   * - ``sleep()``
     - Inherited (helper)
     - Sleeps for the specified number of milliseconds (used to wait between
       records)

storeData Parameters
--------------------

Parameters passed to the ``storeData()`` method:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Parameter
     - Type
     - Description
   * - ``dataConfig``
     - ``DataConfig``
     - Data Store configuration (ID, handler name, parameters, scripts, etc.)
   * - ``callback``
     - ``IndexUpdateCallback``
     - Callback for registering generated documents to the index
   * - ``paramMap``
     - ``DataStoreParams``
     - Configuration values from the "Parameters" field in the admin console.
       Access them using ``getAsString(key)`` / ``getAsString(key, default)`` /
       ``get(key)`` / ``asMap()`` / ``containsKey(key)``
   * - ``scriptMap``
     - ``Map<String, String>``
     - Configuration from the "Scripts" field in the admin console. The key
       is the index field name, and the value is the script template to be
       evaluated
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - Default field values for each document (config ID, boost, role,
       mimetype, virtual host, etc.), prepared by the framework

.. warning::

   The type of ``paramMap`` is ``DataStoreParams``, not
   ``Map<String, String>``. Since ``DataStoreParams`` does not implement
   ``Map``, use ``getAsString()``, which returns a string, instead of
   ``get()`` to retrieve values.

Data Processing Flow
--------------------

The implementation of ``storeData()`` processes data in the following flow.

#. Retrieve source records from the external system.
#. Merge the source record's fields into ``paramMap.asMap()`` to build
   ``resultMap`` (scripts are evaluated against this ``resultMap``).
#. Evaluate each entry in ``scriptMap`` with
   ``convertValue(scriptType, template, resultMap)`` and store the result in
   ``dataMap``. The important point is that the mapping is not hardcoded in
   the code, but defined by the administrator in the "Scripts" field.
#. Call ``callback.store(paramMap, dataMap)`` to register the document to
   the index.

Implementation Examples
=======================

Simple Data Store
------------------

An example of retrieving records from an external API and registering them
to the index.

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Get parameters (use getAsString with DataStoreParams)
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // Script evaluation type (default is Groovy)
        final String scriptType = getScriptType(paramMap);
        // Wait time between records (milliseconds)
        final long readInterval = getReadInterval(paramMap);

        try {
            // Retrieve data from the external system
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // Copy default fields to initialize dataMap
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Build resultMap by merging parameters and the source record
                // (scripts are evaluated against this resultMap)
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // Evaluate each entry in scriptMap to generate index fields
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // Register to the index
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` is a custom method that retrieves a list of records from
the external system. The field names of each retrieved record
(``Map<String, Object>``) become the names that can be referenced from the
scripts in ``scriptMap``. ``DataStoreException`` is a class in the
``org.codelibs.fess.exception`` package.

Pagination Support
-------------------

When handling large volumes of data, process the data page by page while
retrieving it. By extracting the per-record processing (building
``resultMap``, evaluating ``scriptMap``, and calling ``callback.store()``)
into a method such as ``processRecord()``, you can separate it from the
retrieval logic.

.. code-block:: java

    int offset = 0;
    final int pageSize = 100;

    while (true) {
        final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey, offset, pageSize);

        if (records.isEmpty()) {
            break;
        }

        for (final Map<String, Object> record : records) {
            processRecord(record, callback, paramMap, scriptMap, defaultDataMap);
        }

        offset += pageSize;
    }

Authentication Implementation
=============================

Authentication with the external system is implemented on the connector
side. The following is an example implementation using a common HTTP client
library; it is not an API provided by |Fess|. Include the library you use
as a dependency of the plugin.

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // Example of obtaining an access token using a refresh token
        final OkHttpClient client = new OkHttpClient();

        final RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        final Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            final JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

API Key Authentication
----------------------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Error Handling
==============

For fatal errors that should abort processing, throw ``DataStoreException``.

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Processing
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // Retry logic
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   In actual connectors such as ``fess-ds-example``, to avoid stopping the
   entire crawl due to an error in a single record, ``CrawlingAccessException``
   is caught per record and the error URL is recorded in
   ``FailureUrlService``. The interrupt flag of ``DataStoreCrawlingException``
   is also used to control whether to abort the entire crawl. When
   implementing a robust connector, refer to the implementation of
   ``ExampleDataStore``.

Testing
=======

Unit Testing
------------

|Fess| plugins are tested using UTFlute's ``LastaDiTestCase``. Tests are
written in JUnit 5 (Jupiter). By replacing ``IndexUpdateCallback`` with an
implementation that collects the registered ``dataMap``, you can verify the
mapping results without using a mock library.

.. code-block:: java

    public class ExampleDataStoreTest extends LastaDiTestCase {

        public ExampleDataStore dataStore;

        @Override
        protected String prepareConfigFile() {
            return "test_app.xml";
        }

        @Override
        public void setUp(final TestInfo testInfo) throws Exception {
            super.setUp(testInfo);
            dataStore = new ExampleDataStore();
        }

        @Test
        public void test_getName() {
            assertEquals("ExampleDataStore", dataStore.getName());
        }

        @Test
        public void test_storeData() {
            final TestIndexUpdateCallback callback = new TestIndexUpdateCallback();
            final DataStoreParams paramMap = new DataStoreParams();

            final Map<String, String> scriptMap = new HashMap<>();
            scriptMap.put("title", "title");

            dataStore.storeData(new DataConfig(), callback, paramMap, scriptMap, new HashMap<>());

            assertFalse(callback.getDataMapList().isEmpty());
        }

        // Test callback that collects the registered dataMap
        private static class TestIndexUpdateCallback implements IndexUpdateCallback {
            private final List<Map<String, Object>> dataMapList = new ArrayList<>();

            @Override
            public void store(final DataStoreParams paramMap, final Map<String, Object> dataMap) {
                dataMapList.add(new HashMap<>(dataMap));
            }

            @Override
            public long getExecuteTime() {
                return 0;
            }

            @Override
            public long getDocumentSize() {
                return dataMapList.size();
            }

            @Override
            public void commit() {
                // Do nothing
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   Since ``setUp`` is annotated with ``@BeforeEach`` in the base class, there
   is no need to re-annotate the lifecycle annotation on the overriding side.
   Add ``@Test`` (``org.junit.jupiter.api.Test``) to each test method.

Build and Installation
=======================

pom.xml
-------

The plugin is built as a jar with ``fess-parent`` as the parent POM.
Dependencies on ``fess`` and ``opensearch`` are set to ``provided`` because
they are supplied by the |Fess| core at runtime.

.. code-block:: xml

    <project xmlns="http://maven.apache.org/POM/4.0.0" ...>
        <modelVersion>4.0.0</modelVersion>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

JUnit 5 and ``org.dbflute.utflute:utflute-lastaflute`` are used for testing.

Build
-----

.. code-block:: bash

    mvn clean package

``fess-ds-example-15.8.0.jar`` is generated in the ``target/`` directory.

Installation
------------

Install the generated JAR into |Fess| and restart |Fess|. For details on the
installation procedure, see :doc:`../admin/plugin-guide`. After installation,
create a new configuration from "Crawler > Data Store" in the admin console,
and specify the name returned by ``getName()`` (``ExampleDataStore`` in this
example) as the "handler name".

Configuration Example
======================

Example configuration in the admin console:

Parameters
----------

In the "Parameters" field, describe the keys and values that the connector
reads from ``paramMap``.

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

Scripts
-------

In the "Scripts" field, describe the mapping in the form
``left-hand side=right-hand side``. The left-hand side is the index field
name, and the right-hand side is a script (Groovy by default) that
references a field of the source record. The following is an example where
the source record has the ``url`` / ``title`` / ``content`` /
``updated_at`` / ``content_type`` fields.

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   The field names that can be referenced on the right-hand side depend on
   the values that the connector stores in ``resultMap`` (the values of
   ``paramMap`` and the fields of the source record). Existing connectors
   such as CSV and JSON may use a custom prefix such as ``data.*``, so refer
   to the documentation for each connector.

Reference
=========

- :doc:`plugin-architecture` - Plugin Architecture
- :doc:`../admin/plugin-guide` - Plugin Installation
- :doc:`../config/datastore/ds-overview` - Data Store Connector Overview
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ - Data Store plugin implementation template
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Examples of published connectors
