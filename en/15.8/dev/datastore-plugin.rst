==================================
DataStore Plugin Development
==================================

Overview
========

By developing a DataStore plugin, you can add content retrieval functionality
from new data sources to |Fess|.

Basic Structure
===============

DataStore plugins extend ``AbstractDataStore``.

Minimum Implementation
----------------------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(
                final DataConfig dataConfig,
                final IndexUpdateCallback callback,
                final Map<String, String> paramMap,
                final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // Implement data retrieval and processing here
        }
    }

AbstractDataStore
=================

Main Methods
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Description
   * - ``getName()``
     - Returns the DataStore name (required)
   * - ``storeData()``
     - Performs data retrieval and index registration (required)
   * - ``register()``
     - Registers the plugin

Parameters
----------

Parameters passed to the ``storeData()`` method:

- ``dataConfig``: DataStore configuration
- ``callback``: Index update callback
- ``paramMap``: Parameters configured in admin console
- ``scriptMap``: Script configuration
- ``defaultDataMap``: Default data map

Implementation Examples
=======================

Simple DataStore
----------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Get parameters
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // Fetch data
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // Process each document
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Map data
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // Execute scripts (mapping)
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // Register to index
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

Pagination Support
------------------

.. code-block:: java

    @Override
    protected void storeData(...) {
        int page = 0;
        int pageSize = 100;

        while (true) {
            List<Document> documents = fetchDocuments(apiUrl, apiKey, page, pageSize);

            if (documents.isEmpty()) {
                break;
            }

            for (Document doc : documents) {
                processDocument(doc, callback, paramMap, scriptMap, defaultDataMap);
            }

            page++;
        }
    }

Authentication Implementation
=============================

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // Token refresh
        OkHttpClient client = new OkHttpClient();

        RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

API Key Authentication
----------------------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Error Handling
==============

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Processing
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // Retry logic
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

Testing
=======

Unit Testing
------------

.. code-block:: java

    public class ExampleDataStoreTest {

        private ExampleDataStore dataStore;

        @Before
        public void setUp() {
            dataStore = new ExampleDataStore();
        }

        @Test
        public void testGetName() {
            assertEquals("Example", dataStore.getName());
        }

        @Test
        public void testFetchDocuments() {
            // Test using mocks
        }
    }

Configuration Example
=====================

Example configuration in admin console:

Parameters
----------

::

    api.url=https://api.example.com/v1
    api.key=your_api_key
    max.items=1000
    include.folders=folder1,folder2

Scripts
-------

::

    url=data.url
    title=data.name
    content=data.content
    lastModified=data.updated_at
    mimetype=data.content_type

Reference
=========

- :doc:`plugin-architecture` - Plugin Architecture
- :doc:`../config/datastore/ds-overview` - DataStore Connector Overview
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Published plugin examples

