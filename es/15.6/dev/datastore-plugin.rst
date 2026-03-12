==================================
Desarrollo de Plugins de Almacen de Datos
==================================

Vision General
==============

Al desarrollar un plugin de almacen de datos, puede agregar funcionalidad a |Fess|
para obtener contenido desde nuevas fuentes de datos.

Estructura Basica
=================

El plugin de almacen de datos se implementa heredando de ``AbstractDataStore``.

Implementacion Minima
---------------------

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

            // Implementar la obtencion y procesamiento de datos aqui
        }
    }

AbstractDataStore
=================

Metodos Principales
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Metodo
     - Descripcion
   * - ``getName()``
     - Devuelve el nombre del almacen de datos (obligatorio)
   * - ``storeData()``
     - Realiza la obtencion de datos y registro en el indice (obligatorio)
   * - ``register()``
     - Registra el plugin

Parametros
----------

Parametros pasados al metodo ``storeData()``:

- ``dataConfig``: Configuracion del almacen de datos
- ``callback``: Callback para actualizacion del indice
- ``paramMap``: Parametros configurados en la pantalla de administracion
- ``scriptMap``: Configuracion de scripts
- ``defaultDataMap``: Mapa de datos predeterminado

Ejemplo de Implementacion
=========================

Almacen de Datos Simple
-----------------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // Obtener parametros
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // Obtener datos
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // Procesar cada documento
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // Mapeo de datos
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // Ejecutar script (mapeo)
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // Registrar en el indice
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

Soporte de Paginacion
---------------------

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

Implementacion de Autenticacion
===============================

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // Refrescar el token
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

Autenticacion con Clave API
---------------------------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

Manejo de Errores
=================

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // Procesamiento
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // Logica de reintento
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

Pruebas
=======

Pruebas Unitarias
-----------------

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
            // Pruebas usando mocks
        }
    }

Ejemplo de Configuracion
========================

Ejemplo de configuracion en la pantalla de administracion:

Parametros
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

Informacion de Referencia
=========================

- :doc:`plugin-architecture` - Arquitectura de plugins
- :doc:`../config/datastore/ds-overview` - Vision general de conectores de almacen de datos
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - Ejemplos de plugins publicos
