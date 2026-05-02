==================================
DataStore-Plugin-Entwicklung
==================================

Übersicht
=========

Durch die Entwicklung eines DataStore-Plugins konnen Sie |Fess| die Fahigkeit
zur Inhaltserfassung von neuen Datenquellen hinzufugen.

Grundstruktur
=============

Ein DataStore-Plugin wird durch Vererbung von ``AbstractDataStore`` implementiert.

Minimale Implementierung
------------------------

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

            // Datenabruf und -verarbeitung hier implementieren
        }
    }

AbstractDataStore
=================

Wichtige Methoden
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Methode
     - Beschreibung
   * - ``getName()``
     - Gibt den Namen des DataStore zuruck (erforderlich)
   * - ``storeData()``
     - Fuhrt Datenabruf und Index-Registrierung durch (erforderlich)
   * - ``register()``
     - Registriert das Plugin

Parameter
---------

Parameter, die an die ``storeData()``-Methode ubergeben werden:

- ``dataConfig``: DataStore-Konfiguration
- ``callback``: Callback fur Index-Updates
- ``paramMap``: In der Administrationsoberflache konfigurierte Parameter
- ``scriptMap``: Skript-Konfiguration
- ``defaultDataMap``: Standard-Daten-Map

Implementierungsbeispiel
========================

Einfacher DataStore
-------------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Parameter abrufen
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // Daten abrufen
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // Jedes Dokument verarbeiten
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Daten-Mapping
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // Skript ausfuhren (Mapping)
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // Im Index registrieren
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

Mit Paginierung
---------------

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

Authentifizierung
=================

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // Token-Aktualisierung
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

API-Key-Authentifizierung
-------------------------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Fehlerbehandlung
================

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Verarbeitung
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // Retry-Logik
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

Tests
=====

Unit-Tests
----------

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
            // Test mit Mocks
        }
    }

Konfigurationsbeispiel
======================

Konfigurationsbeispiel in der Administrationsoberflache:

Parameter
---------

::

    api.url=https://api.example.com/v1
    api.key=your_api_key
    max.items=1000
    include.folders=folder1,folder2

Skript
------

::

    url=data.url
    title=data.name
    content=data.content
    lastModified=data.updated_at
    mimetype=data.content_type

Referenzinformationen
=====================

- :doc:`plugin-architecture` - Plugin-Architektur
- :doc:`../config/datastore/ds-overview` - DataStore-Konnektor-Übersicht
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Beispiele fur veroffentlichte Plugins
