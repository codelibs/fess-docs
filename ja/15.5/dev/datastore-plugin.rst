==================================
データストアプラグイン開発
==================================

概要
====

データストアプラグインを開発することで、|Fess| に新しいデータソースからの
コンテンツ取得機能を追加できます。

基本構造
========

データストアプラグインは ``AbstractDataStore`` を継承して実装します。

最小実装
--------

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

            // データの取得と処理をここに実装
        }
    }

AbstractDataStore
=================

主要メソッド
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 説明
   * - ``getName()``
     - データストアの名前を返す（必須）
   * - ``storeData()``
     - データの取得とインデックス登録を行う（必須）
   * - ``register()``
     - プラグインを登録する

パラメーター
------------

``storeData()`` メソッドに渡されるパラメーター:

- ``dataConfig``: データストア設定
- ``callback``: インデックス更新用コールバック
- ``paramMap``: 管理画面で設定されたパラメーター
- ``scriptMap``: スクリプト設定
- ``defaultDataMap``: デフォルトのデータマップ

実装例
======

シンプルなデータストア
----------------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // パラメーターの取得
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // データの取得
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // 各ドキュメントを処理
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // データのマッピング
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // スクリプトの実行（マッピング）
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // インデックスに登録
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

ページネーション対応
--------------------

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

認証の実装
==========

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // トークンのリフレッシュ
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

APIキー認証
-----------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

エラーハンドリング
==================

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // 処理
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // リトライロジック
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

テスト
======

ユニットテスト
--------------

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
            // モックを使用したテスト
        }
    }

設定例
======

管理画面での設定例:

パラメーター
------------

::

    api.url=https://api.example.com/v1
    api.key=your_api_key
    max.items=1000
    include.folders=folder1,folder2

スクリプト
----------

::

    url=data.url
    title=data.name
    content=data.content
    lastModified=data.updated_at
    mimetype=data.content_type

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`../config/datastore/ds-overview` - データストアコネクタ概要
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - 公開プラグインの例
