==================================
Developpement de plugins DataStore
==================================

Vue d'ensemble
==============

En developpant un plugin DataStore, vous pouvez ajouter a |Fess| la capacite
de recuperer du contenu depuis de nouvelles sources de donnees.

Structure de base
=================

Un plugin DataStore herite de ``AbstractDataStore``.

Implementation minimale
-----------------------

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

            // Implementer la recuperation et le traitement des donnees ici
        }
    }

AbstractDataStore
=================

Methodes principales
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Methode
     - Description
   * - ``getName()``
     - Retourne le nom du DataStore (obligatoire)
   * - ``storeData()``
     - Effectue la recuperation et l'enregistrement dans l'index (obligatoire)
   * - ``register()``
     - Enregistre le plugin

Parametres
----------

Parametres passes a la methode ``storeData()``:

- ``dataConfig``: Configuration du DataStore
- ``callback``: Callback pour la mise a jour de l'index
- ``paramMap``: Parametres configures dans l'interface d'administration
- ``scriptMap``: Configuration des scripts
- ``defaultDataMap``: Map de donnees par defaut

Exemple d'implementation
========================

DataStore simple
----------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Recuperation des parametres
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // Recuperation des donnees
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // Traitement de chaque document
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Mapping des donnees
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // Execution du script (mapping)
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // Enregistrement dans l'index
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

Gestion de la pagination
------------------------

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

Implementation de l'authentification
====================================

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // Rafraichissement du token
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

Authentification par cle API
----------------------------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Gestion des erreurs
===================

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Traitement
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // Logique de retry
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

Tests
=====

Tests unitaires
---------------

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
            // Test avec des mocks
        }
    }

Exemple de configuration
========================

Exemple de configuration dans l'interface d'administration:

Parametres
----------

::

    api.url=https://api.example.com/v1
    api.key=your_api_key
    max.items=1000
    include.folders=folder1,folder2

Script
------

::

    url=data.url
    title=data.name
    content=data.content
    lastModified=data.updated_at
    mimetype=data.content_type

Informations complementaires
============================

- :doc:`plugin-architecture` - Architecture des plugins
- :doc:`../config/datastore/ds-overview` - Vue d'ensemble des connecteurs DataStore
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Exemples de plugins publies
