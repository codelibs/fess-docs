==================================
插件架构
==================================

概述
====

通过 |Fess| 的插件系统，可以扩展核心功能。
插件以 JAR 文件的形式分发，添加到类路径后，会由 DI 容器（Lasta Di）
加载其中的组件，并注册到相应的工厂或管理器中。

插件类型
========

|Fess| 通过构件（artifact）名称的前缀来判断插件的类型
（``PluginHelper.ArtifactType``）。主要类型如下：

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 类型
     - 前缀
     - 说明
   * - 数据存储
     - ``fess-ds-*``
     - 从新数据源获取内容（Box、Slack、Git 等）
   * - Web应用
     - ``fess-webapp-*``
     - 扩展Web界面或搜索功能
   * - 脚本引擎
     - ``fess-script-*``
     - 支持新的脚本语言
   * - Ingest
     - ``fess-ingest-*``
     - 索引注册时对文档进行加工处理
   * - 主题
     - ``fess-theme-*``
     - 自定义搜索界面设计
   * - 缩略图
     - ``fess-thumbnail-*``
     - 添加缩略图生成方式
   * - LLM
     - ``fess-llm-*``
     - 添加 RAG/聊天功能中使用的 LLM 提供方
   * - 爬虫
     - ``fess-crawler-*``
     - 扩展爬虫客户端

插件结构
========

基本结构
--------

以数据存储插件的实现模板
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ 为例，
插件由"实现类"和"DI 注册文件"构成：

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # 数据存储实现
        └── resources/
            └── fess_ds++.xml             # DI组件注册

pom.xml示例
-----------

插件以 ``fess-parent`` 作为父 POM，构建为 jar。``fess``、``opensearch``
等在运行时由 |Fess| 本体提供的库，需以 ``provided`` 作用域声明。版本号
及构建配置（格式化工具、许可证头等）均从父 POM 继承。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
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

.. note::

   在开发中的分支上，版本号会带有 ``-SNAPSHOT`` 后缀，例如
   ``15.8.0-SNAPSHOT``。插件特有的依赖库以普通的 Maven 依赖关系声明。
   由于这些库不包含在 |Fess| 本体中，因此需要与插件一起分发。

插件注册
========

DI容器注册
----------

插件通过文件名以 ``++`` 结尾的 DI 配置文件（如 ``fess_ds++.xml``）来
注册组件。Lasta Di 会将在类路径中找到的带 ``++`` 的文件，自动合并到
|Fess| 本体对应的配置文件中（本例中为 ``fess_ds.xml``）。借助这一机
制，插件无需修改 |Fess| 本体的文件，即可添加自身的组件。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

不同类型的插件，合并目标文件也不同。例如脚本引擎使用
``fess_se++.xml``、Ingest 使用 ``fess_ingest++.xml``、LLM 提供方使用
``fess_llm++.xml``、Web应用使用 ``app++.xml``。

组件初始化
----------

``<postConstruct name="register">`` 是 Lasta Di 的生命周期设置，用于
指定组件生成后要调用的方法。对于数据存储而言，会调用
``AbstractDataStore`` 所具有的 ``register()`` 方法，将自身注册到
``DataStoreFactory`` 中：

.. code-block:: java

    // AbstractDataStore 的实现（通常无需重写）
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   这并非 Java 的 ``@PostConstruct`` 注解，而是通过 DI 配置文件中的
   ``<postConstruct>`` 元素进行的初始化。注册的名称即为 ``getName()``
   的返回值，也就是在管理界面中选择插件时使用的名称。

插件生命周期
============

初始化
------

1. 插件 JAR 被添加到类路径中
2. DI 容器合并 ``fess_*++.xml``，生成组件
3. 调用 ``<postConstruct>`` 中指定的方法（例如 ``register``）
4. 插件注册到对应的工厂/管理器中

终止
----

1. DI 容器终止时，会调用 ``<preDestroy>`` 中指定的方法（如果已定义）
2. 清理资源

.. note::

   对于数据存储而言，正在运行的爬取会通过 ``AbstractDataStore.stop()``
   设置停止标志，使记录处理循环安全结束。

依赖关系
========

与Fess本体的依赖
----------------

由于 |Fess| 本体的类在运行时已存在于服务器的类路径中，因此以
``provided`` 作用域进行依赖（不会包含在插件 JAR 中）。

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

外部库
------

插件可以包含自己的依赖库：

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

由于这些库不包含在 |Fess| 本体中，因此需要与插件一起分发。

获取配置
========

获取参数和FessConfig
--------------------

在数据存储的 ``storeData()`` 中，可从 ``DataStoreParams`` 获取在管理
界面中设置的参数。获取值时请使用 ``getAsString()``（由于
``DataStoreParams`` 并未实现 ``Map`` 接口，``get()`` 不会返回字符
串）。此外，|Fess| 的配置值可通过 ``ComponentUtil.getFessConfig()``
获取：

.. code-block:: java

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

            // 获取参数
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // 获取FessConfig
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

关于 ``storeData()`` 的详细实现方法（数据获取、脚本求值、索引注册的
流程），请参考 :doc:`datastore-plugin`。

构建与安装
==========

构建
----

::

    mvn clean package

会在 ``target/`` 目录下生成 JAR 文件（例如
``fess-ds-example-15.8.0.jar``）。

安装
----

1. **从管理界面**：

   - 打开[系统 > 插件 > 安装]
   - 从插件仓库列表中选择，或上传已构建的 JAR 文件进行安装

2. **手动安装**：

   - 将 JAR 文件复制到 ``app/WEB-INF/plugin/`` 目录
   - 重启 |Fess|

安装步骤的详细信息请参考 :doc:`../admin/plugin-guide`。

调试
====

日志输出
--------

|Fess| 使用 Log4j2。日志记录器（logger）可通过
``LogManager.getLogger()`` 获取：

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   请不要将密码、令牌等敏感信息输出到日志中。

开发模式
--------

开发时可以从 IDE 启动 |Fess| 进行调试：

1. 以调试模式运行 ``org.codelibs.fess.FessBoot`` 类
2. 将插件的源代码包含在项目中
3. 设置断点

公开插件列表
============

|Fess| 项目公开了大量插件，以下是其中的代表示例（并非全部列举）：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 插件
     - 说明
   * - ``fess-ds-box``
     - Box 连接器
   * - ``fess-ds-dropbox``
     - Dropbox 连接器
   * - ``fess-ds-slack``
     - Slack 连接器
   * - ``fess-ds-atlassian``
     - JIRA / Confluence 连接器
   * - ``fess-ds-git``
     - Git 仓库连接器
   * - ``fess-llm-openai``
     - OpenAI LLM 提供方
   * - ``fess-theme-*``
     - 自定义主题

除此之外，还公开了 ``fess-ds-csv`` / ``fess-ds-db`` / ``fess-ds-json`` /
``fess-ds-microsoft365`` / ``fess-ds-sharepoint`` 等数据存储连接器，以及
``fess-llm-ollama`` / ``fess-llm-gemini`` 等 LLM 提供方。这些插件已在
`GitHub <https://github.com/codelibs>`__ 上公开，可作为开发参考。

参考信息
========

- :doc:`datastore-plugin` - 数据存储插件开发
- :doc:`script-engine-plugin` - 脚本引擎插件
- :doc:`webapp-plugin` - Web应用插件
- :doc:`ingest-plugin` - Ingest插件
- :doc:`theme-development` - 主题自定义
- :doc:`../admin/plugin-guide` - 插件安装
