==================================
数据存储插件开发
==================================

概述
====

通过开发数据存储插件，可以为 |Fess| 添加从新数据源获取内容的功能。

基本结构
========

数据存储插件通过继承 ``AbstractDataStore`` 来实现。

最小实现
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

            // 在此实现数据获取和处理
        }
    }

AbstractDataStore
=================

主要方法
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 方法
     - 说明
   * - ``getName()``
     - 返回数据存储名称（必需）
   * - ``storeData()``
     - 执行数据获取和索引注册（必需）
   * - ``register()``
     - 注册插件

参数
----

传递给 ``storeData()`` 方法的参数:

- ``dataConfig``: 数据存储配置
- ``callback``: 索引更新回调
- ``paramMap``: 管理界面设置的参数
- ``scriptMap``: 脚本设置
- ``defaultDataMap``: 默认数据映射

实现示例
========

简单的数据存储
--------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // 获取参数
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // 获取数据
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // 处理每个文档
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // 数据映射
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // 执行脚本（映射）
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // 注册到索引
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

分页支持
--------

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

认证实现
========

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // 刷新令牌
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

API密钥认证
-----------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

错误处理
========

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // 处理
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // 重试逻辑
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

测试
====

单元测试
--------

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
            // 使用mock进行测试
        }
    }

配置示例
========

管理界面的配置示例:

参数
----

::

    api.url=https://api.example.com/v1
    api.key=your_api_key
    max.items=1000
    include.folders=folder1,folder2

脚本
----

::

    url=data.url
    title=data.name
    content=data.content
    lastModified=data.updated_at
    mimetype=data.content_type

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`../config/datastore/ds-overview` - 数据存储连接器概述
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - 公开插件示例

