==================================
数据存储插件开发
==================================

概述
====

通过开发数据存储插件，可以为 |Fess| 添加从新数据源获取内容的功能。数据存储会从数据库、
API、文件等外部系统中获取记录，并按照在管理界面中设置的映射脚本，将其转换为索引字段后，
注册到 |Fess| 的索引中。

CSV、JSON、数据库、Git、各类云服务等公开的连接器（``fess-ds-*``）都是基于这一机制实现
的。作为实现模板，官方公开了
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ ，创建新连接器时，
复制该模板作为起点会比较简单。

基本结构
========

数据存储插件由以下三个要素构成：

- 创建继承 ``AbstractDataStore`` 的类
- 实现 ``getName()`` 和 ``storeData()`` 两个方法
- 在 ``fess_ds++.xml`` 中注册为组件

最小实现
--------

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
            // 用作处理器名。按照惯例返回类的简单名称
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // 在此实现数据的获取与处理
        }
    }

.. note::

   ``getName()`` 和 ``storeData()`` 都是 ``protected`` 的抽象方法。请注意，在 |Fess|
   15.x 中，``DataConfig`` 所在的包是 ``org.codelibs.fess.opensearch.config.exentity``
   （此前的 ``org.codelibs.fess.es.config.exentity`` 已被废弃）。

组件注册
--------------------

为了让 |Fess| 识别所创建的数据存储，需要在 ``src/main/resources/fess_ds++.xml`` 中
注册组件。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

通过 ``<postConstruct name="register">``，组件生成后会自动调用 ``AbstractDataStore``
所具有的 ``register()`` 方法，将自身注册到 ``DataStoreFactory`` 中。此时注册的名称即为
``getName()`` 的返回值（上例中为 ``ExampleDataStore``），也就是在管理界面的数据存储设置
中选择的"处理器名"。

AbstractDataStore
=================

主要方法
------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - 方法
     - 类别
     - 说明
   * - ``getName()``
     - 实现（必需）
     - 返回数据存储处理器名的抽象方法。按照惯例返回 ``getClass().getSimpleName()``
   * - ``storeData()``
     - 实现（必需）
     - 执行数据获取、转换及索引注册的抽象方法
   * - ``register()``
     - 继承（通常无需修改）
     - 由 ``fess_ds++.xml`` 的 ``postConstruct`` 自动调用，注册到 ``DataStoreFactory``
   * - ``store()``
     - 继承（框架调用）
     - 框架调用的入口。准备好 ``defaultDataMap`` 等后调用 ``storeData()``
   * - ``convertValue()``
     - 继承（辅助方法）
     - 通过脚本引擎对 ``scriptMap`` 的值（模板）进行求值
   * - ``getScriptType()``
     - 继承（辅助方法）
     - 获取 ``script_type`` 参数（默认为 Groovy）
   * - ``getReadInterval()``
     - 继承（辅助方法）
     - 获取 ``readInterval`` 参数（毫秒）
   * - ``sleep()``
     - 继承（辅助方法）
     - 休眠指定的毫秒数（用于记录间的等待）

storeData 的参数
------------------------

传递给 ``storeData()`` 方法的参数：

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 参数
     - 类型
     - 说明
   * - ``dataConfig``
     - ``DataConfig``
     - 数据存储设置（ID、处理器名、参数、脚本等）
   * - ``callback``
     - ``IndexUpdateCallback``
     - 将生成的文档注册到索引的回调
   * - ``paramMap``
     - ``DataStoreParams``
     - 管理界面"参数"栏中设置的值。可通过 ``getAsString(key)`` / ``getAsString(key, default)`` / ``get(key)`` / ``asMap()`` / ``containsKey(key)`` 进行访问
   * - ``scriptMap``
     - ``Map<String, String>``
     - 管理界面"脚本"栏中的设置。键为索引字段名，值为待求值的脚本模板
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - 各文档的默认字段值（配置ID、boost、role、mimetype、虚拟主机等）。由框架准备

.. warning::

   ``paramMap`` 的类型不是 ``Map<String, String>``，而是 ``DataStoreParams``\ 。由于
   ``DataStoreParams`` 并未实现 ``Map`` 接口，获取值时请使用返回字符串的
   ``getAsString()``，而不是 ``get()``\ 。

数据处理流程
----------------

``storeData()`` 的实现按以下流程处理数据：

#. 从外部系统获取源记录。
#. 将源记录的字段合并到 ``paramMap.asMap()`` 中，构建 ``resultMap``
   （脚本将针对该 ``resultMap`` 进行求值）。
#. 使用 ``convertValue(scriptType, template, resultMap)`` 对 ``scriptMap`` 中的每个
   条目求值，并将结果存入 ``dataMap``\ 。需要注意的是，映射关系并非硬编码在代码中，而是由
   管理员在"脚本"栏中定义。
#. 调用 ``callback.store(paramMap, dataMap)``，将其作为文档注册到索引中。

实现示例
========

简单的数据存储
----------------------

以下是从外部 API 获取记录并注册到索引的示例。

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // 获取参数（DataStoreParams 需使用 getAsString）
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // 脚本的求值类型（默认为 Groovy）
        final String scriptType = getScriptType(paramMap);
        // 记录之间的等待时间（毫秒）
        final long readInterval = getReadInterval(paramMap);

        try {
            // 从外部系统获取数据
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // 复制默认字段以初始化 dataMap
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // 构建合并了参数与源记录的 resultMap
                // （脚本将针对此 resultMap 进行求值）
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // 对 scriptMap 中的每个条目求值，生成索引字段
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // 注册到索引
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` 是从外部系统获取记录列表的自定义方法。获取到的每条记录
（``Map<String, Object>``）的字段名，即为可在 ``scriptMap`` 的脚本中引用的名称。
``DataStoreException`` 是 ``org.codelibs.fess.exception`` 包中的类。

分页支持
--------------------

在处理大量数据时，需要按页获取并处理数据。将每条记录的处理逻辑（构建 ``resultMap``、
对 ``scriptMap`` 求值、调用 ``callback.store()``）拆分到类似 ``processRecord()`` 的
方法中，可以将其与获取逻辑分离。

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

认证实现
==========

外部系统的认证由连接器一侧负责实现。以下是使用常见 HTTP 客户端库的实现示例，并非
|Fess| 提供的 API。请将所使用的库作为插件的依赖项一并打包。

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // 使用刷新令牌获取访问令牌的示例
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

API密钥认证
-----------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

错误处理
==================

对于应中断处理的致命错误，请抛出 ``DataStoreException``\ 。

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // 处理
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // 重试逻辑
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   在以 ``fess-ds-example`` 为代表的实际连接器中，为了避免单条记录的错误导致整个爬取
   中断，会以记录为单位捕获 ``CrawlingAccessException``，并将出错的 URL 记录到
   ``FailureUrlService`` 中。此外，还会利用 ``DataStoreCrawlingException`` 的中断
   标志，来控制是否中断整个爬取过程。如需实现健壮的连接器，请参考 ``ExampleDataStore``
   的实现。

测试
======

单元测试
--------------

|Fess| 的插件使用 UTFlute 的 ``LastaDiTestCase`` 进行测试。测试使用 JUnit 5
（Jupiter）编写。通过将 ``IndexUpdateCallback`` 替换为收集已注册 ``dataMap`` 的实现，
无需使用模拟（mock）库即可验证映射结果。

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

        // 用于收集已注册 dataMap 的测试用回调
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
                // 不执行任何操作
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   由于基类中的 ``setUp`` 已附加了 ``@BeforeEach``，因此重写时无需在其上重新附加生命
   周期注解。请为每个测试方法附加 ``@Test``\ （``org.junit.jupiter.api.Test``）。

构建与安装
====================

pom.xml
-------

插件以 ``fess-parent`` 作为父 POM，构建为 jar。对 ``fess`` 和 ``opensearch`` 的依赖，
由于在运行时由 |Fess| 本体提供，因此设置为 ``provided``\ 。

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

测试使用 JUnit 5 和 ``org.dbflute.utflute:utflute-lastaflute``\ 。

构建
------

.. code-block:: bash

    mvn clean package

会在 ``target/`` 目录下生成 ``fess-ds-example-15.8.0.jar``\ 。

安装
------------

将生成的 JAR 安装到 |Fess| 中，并重启 |Fess|\ 。安装步骤的详细信息请参考
:doc:`../admin/plugin-guide`。安装后，从管理界面的"爬虫 > 数据存储"创建新设置，并在
"处理器名"中指定 ``getName()`` 返回的名称（本例中为 ``ExampleDataStore``）。

配置示例
========

管理界面中的配置示例：

参数
------------

"参数"栏中填写连接器从 ``paramMap`` 读取的键和值。

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

脚本
----------

"脚本"栏中以 ``左边=右边`` 的形式描述映射关系。左边为索引字段名，右边为引用源记录字段
的脚本（默认使用 Groovy）。以下是源记录具有 ``url`` / ``title`` / ``content`` /
``updated_at`` / ``content_type`` 字段时的示例。

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   右边可引用的字段名，取决于连接器存入 ``resultMap`` 中的值（``paramMap`` 的值以及
   源记录的字段）。在 CSV、JSON 等现有连接器中，可能会带有类似 ``data.*`` 的专属前缀，
   请参考各连接器的文档。

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`../admin/plugin-guide` - 插件安装
- :doc:`../config/datastore/ds-overview` - 数据存储连接器概述
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ - 数据存储插件的实现模板
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - 公开连接器示例
