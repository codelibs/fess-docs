==================================
插件架构
==================================

概述
====

|Fess| 的插件系统允许您扩展核心功能。
插件以JAR文件形式分发，并动态加载。

插件类型
========

|Fess| 支持以下类型的插件:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 类型
     - 说明
   * - 数据存储
     - 从新数据源获取内容（Box、Slack等）
   * - 脚本引擎
     - 支持新的脚本语言
   * - Web应用
     - 扩展Web界面
   * - Ingest
     - 索引时的数据处理

插件结构
========

基本结构
--------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # 数据存储实现
        └── ExampleDataStoreHandler.java # 处理器（可选）

pom.xml示例
-----------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.5.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.5.0</fess.version>
            <java.version>21</java.version>
        </properties>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <version>${fess.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

插件注册
========

DI容器注册
----------

插件在 ``fess_ds.xml`` 等配置文件中注册:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

自动注册
--------

许多插件使用 ``@PostConstruct`` 注解自动注册:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

插件生命周期
============

初始化
------

1. JAR文件被加载
2. DI容器初始化组件
3. 调用 ``@PostConstruct`` 方法
4. 插件注册到管理器

终止
----

1. 调用 ``@PreDestroy`` 方法（如果定义）
2. 清理资源

依赖关系
========

与Fess本体的依赖
----------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
        <scope>provided</scope>
    </dependency>

外部库
------

插件可以包含自己的依赖库:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

依赖库与插件JAR一起分发，
或使用Maven Shade Plugin创建fat JAR。

获取配置
========

从FessConfig获取
----------------

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(DataConfig dataConfig, IndexUpdateCallback callback,
                Map<String, String> paramMap, Map<String, String> scriptMap,
                Map<String, Object> defaultDataMap) {

            // 获取参数
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // 获取FessConfig
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

构建和安装
==========

构建
----

::

    mvn clean package

安装
----

1. **从管理界面**:

   - "系统" -> "插件" -> "安装"
   - 输入插件名称进行安装

2. **命令行**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **手动**:

   - 将JAR文件复制到 ``plugins/`` 目录
   - 重启 |Fess|

调试
====

日志输出
--------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

开发模式
--------

开发时可以从IDE启动 |Fess| 进行调试:

1. 以调试模式运行 ``FessBoot`` 类
2. 将插件源代码包含在项目中
3. 设置断点

公开插件列表
============

|Fess| 项目公开的主要插件:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 插件
     - 说明
   * - fess-ds-box
     - Box.com连接器
   * - fess-ds-dropbox
     - Dropbox连接器
   * - fess-ds-slack
     - Slack连接器
   * - fess-ds-atlassian
     - Confluence/Jira连接器
   * - fess-ds-git
     - Git仓库连接器
   * - fess-theme-*
     - 自定义主题

这些插件在
`GitHub <https://github.com/codelibs>`__ 上公开，可作为开发参考。

参考信息
========

- :doc:`datastore-plugin` - 数据存储插件开发
- :doc:`script-engine-plugin` - 脚本引擎插件
- :doc:`webapp-plugin` - Web应用插件
- :doc:`ingest-plugin` - Ingest插件

