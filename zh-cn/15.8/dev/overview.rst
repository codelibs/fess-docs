==================================
开发者文档概述
==================================

概述
====

本节介绍 |Fess| 的扩展开发。
提供插件开发、自定义连接器创建、主题定制等
扩展 |Fess| 所需的信息。

目标读者
========

- 想要开发 |Fess| 自定义功能的开发者
- 想要创建插件的开发者
- 想要理解 |Fess| 源代码的开发者

前提知识
--------

- Java 21的基本知识
- Maven（构建系统）基础
- Web应用程序开发经验
- OpenSearch的基本知识（|Fess| 使用OpenSearch作为搜索引擎）

开发环境
========

推荐环境
--------

- **JDK**: OpenJDK 21以上
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **构建工具**: Maven（构建过程未强制规定最低版本，但推荐使用支持Java 21的较新3.x版本）
- **Git**: 版本管理
- **OpenSearch**: 搜索引擎后端（从IDE启动时，所需的模块和插件会在构建时下载）

环境配置
--------

|Fess| 作为Maven项目进行构建。开发时最简单的方式是从IDE启动。

1. 获取源代码:

   ::

       git clone https://github.com/codelibs/fess.git

2. 导入到IDE:

   将获取到的目录作为Maven项目导入到IDE中。

3. 下载OpenSearch所需的模块和插件:

   仅首次需要执行以下命令，将搜索引擎的模块和插件获取到 ``plugins`` 目录中。

   ::

       mvn antrun:run

4. 启动开发服务器（从IDE）:

   在IDE中运行或以调试方式运行 ``org.codelibs.fess.FessBoot``，
   然后在浏览器中打开 http://localhost:8080/。
   管理界面为 http://localhost:8080/admin/ （初始账号: ``admin`` / ``admin``）。

5. 构建软件包（生成分发包）:

   如果需要分发包，请执行 ``package`` 目标。
   生成的成果物会输出到 ``target/releases`` 中（如需跳过单元测试，请添加 ``-DskipTests``）。

   ::

       mvn package

   展开生成的分发包后，即可使用 ``bin/fess`` 启动脚本。

   ::

       unzip target/releases/fess-*.zip
       ./fess-*/bin/fess

.. note::

    ``bin/fess`` 启动脚本包含在分发包（zip/rpm/deb）中。
    仅在源代码目录中执行 ``mvn package``，并不会在仓库根目录下生成 ``bin/fess``。
    在基于源代码进行开发时，请按照上文所述在IDE中运行 ``FessBoot``，
    或使用展开后的分发包中的 ``bin/fess``。

架构概述
========

|Fess| 由以下主要组件构成:

组件构成
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 组件
     - 说明
   * - Web层
     - 基于LastaFlute框架的MVC实现
   * - 服务层
     - 业务逻辑
   * - 数据访问层
     - 通过DBFlute（ESFlute/FreeGen）实现的类型安全的OpenSearch访问
   * - 爬虫
     - 使用fess-crawler库进行内容收集
   * - 搜索引擎
     - 基于OpenSearch的全文搜索

主要框架
--------

- **LastaFlute**: Web框架（Action、Form、Validation）
- **DBFlute**: 数据访问框架。面向OpenSearch的类型安全访问类（``Bhv`` / ``ConditionBean``）
  由DBFlute的FreeGen功能与ESFlute模板生成
  （重新生成命令为 ``mvn dbflute:freegen``）
- **Lasta Di**: 依赖注入容器

目录结构
========

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # 控制器（Action）
    │   │   ├── service/     # 服务
    │   │   ├── logic/       # 逻辑
    │   │   └── pager/       # 分页
    │   ├── api/             # REST API（如api/v2）
    │   ├── helper/          # 辅助类
    │   ├── crawler/         # 爬虫相关
    │   ├── indexer/         # 索引处理
    │   ├── opensearch/      # OpenSearch访问（ESFlute/FreeGen生成）
    │   ├── llm/             # LLM集成
    │   ├── ds/              # 数据存储连接器
    │   ├── ingest/          # Ingest（索引时的数据加工）
    │   ├── script/          # 脚本引擎
    │   ├── entity/          # 实体
    │   └── mylasta/         # LastaFlute配置（DI、消息、类型安全配置）
    ├── src/main/resources/
    │   ├── fess_config.properties  # 配置
    │   └── fess_*.xml              # DI配置（如app.xml、fess_ds.xml）
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP模板

扩展点
======

|Fess| 提供以下扩展点:

插件
----

使用插件可以添加功能。

- **数据存储插件**: 从新数据源进行爬取（继承 ``AbstractDataStore``）
- **脚本引擎插件**: 支持新的脚本语言（实现 ``ScriptEngine``）
- **Web应用插件**: 扩展Web界面（通过Lasta Di的组件覆盖与资源合并）
- **Ingest插件**: 索引时的数据加工（继承 ``Ingester``）

详情: :doc:`plugin-architecture`

.. note::

    |Fess| 本体以 ``war`` 形式打包。在本地构建插件时，
    如果无法将 |Fess| 解析为依赖项，请将 ``pom.xml`` 中的 ``<packaging>`` 临时改为 ``jar``，
    执行 ``mvn clean install -DskipTests``，然后再改回 ``war``。

主题
----

可以自定义搜索界面的设计。

详情: :doc:`theme-development`

配置
----

可以通过 ``fess_config.properties`` 自定义许多行为。

详情: :doc:`../config/intro`

插件开发
========

有关插件开发的详细信息，请参阅以下内容:

- :doc:`plugin-architecture` - 插件架构
- :doc:`datastore-plugin` - 数据存储插件开发
- :doc:`script-engine-plugin` - 脚本引擎插件
- :doc:`webapp-plugin` - Web应用插件
- :doc:`ingest-plugin` - Ingest插件

主题开发
========

- :doc:`theme-development` - 主题自定义

最佳实践
========

编码规范
--------

- 遵循 |Fess| 现有的代码风格
- 使用 ``mvn formatter:format`` 格式化代码
- 使用 ``mvn license:format`` 添加许可证头

测试
----

- 单元测试（``*Test.java``）: 在默认的 ``build`` 配置文件下作为 ``mvn test`` 执行
- 集成测试（``*Tests.java``）: 通过 ``mvn test -P integrationTests`` 执行。
  执行集成测试需要运行中的 |Fess| 服务器与OpenSearch

日志
----

- 使用Log4j2
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- 不要在日志中输出敏感信息

资源
====

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
