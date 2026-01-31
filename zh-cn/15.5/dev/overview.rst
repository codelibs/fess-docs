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

开发环境
========

推荐环境
--------

- **JDK**: OpenJDK 21以上
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **构建工具**: Maven 3.9以上
- **Git**: 版本管理

环境配置
--------

1. 获取源代码:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. 构建:

::

    mvn package -DskipTests

3. 启动开发服务器:

::

    ./bin/fess

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
     - 通过DBFlute与OpenSearch集成
   * - 爬虫
     - 使用fess-crawler库进行内容收集
   * - 搜索引擎
     - 基于OpenSearch的全文搜索

主要框架
--------

- **LastaFlute**: Web框架（Action、Form、Validation）
- **DBFlute**: 数据访问框架（OpenSearch集成）
- **Lasta Di**: 依赖注入容器

目录结构
========

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # 控制器（Action）
    │   │   ├── service/     # 服务
    │   │   └── pager/       # 分页
    │   ├── api/             # REST API
    │   ├── helper/          # 辅助类
    │   ├── crawler/         # 爬虫相关
    │   ├── opensearch/      # OpenSearch集成（DBFlute生成）
    │   ├── llm/             # LLM集成
    │   └── ds/              # 数据存储连接器
    ├── src/main/resources/
    │   ├── fess_config.properties  # 配置
    │   └── fess_*.xml              # DI配置
    └── src/main/webapp/
        └── WEB-INF/view/    # JSP模板

扩展点
======

|Fess| 提供以下扩展点:

插件
----

使用插件可以添加功能。

- **数据存储插件**: 从新数据源爬取
- **脚本引擎插件**: 支持新的脚本语言
- **Web应用插件**: 扩展Web界面
- **Ingest插件**: 索引时的数据处理

详情: :doc:`plugin-architecture`

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

- 编写单元测试（``*Test.java``）
- 集成测试使用 ``*Tests.java``

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

