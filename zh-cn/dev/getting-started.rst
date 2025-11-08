================================================
开源全文检索服务器 - |Fess| 开发概述
================================================

本页面提供 |Fess| 开发的整体概况和开始开发的基本信息。

.. contents:: 目录
   :local:
   :depth: 2

概述
====

|Fess| 是用 Java 开发的开源全文检索服务器。
旨在轻松构建企业搜索，
提供强大的搜索功能和易用的管理界面。

|Fess| 的特点
-------------

- **简单的设置**: 有 Java 环境即可立即启动
- **强大的爬虫**: 支持网站、文件系统、数据库等多种数据源
- **日语支持**: 针对日语全文检索优化
- **可扩展性**: 可通过插件扩展功能
- **REST API**: 可从其他应用程序使用搜索功能

技术栈
==========

|Fess| 使用以下技术开发。

目标版本
------------

本文档针对以下版本：

- **Fess**: 15.3.0
- **Java**: 21 及以上
- **OpenSearch**: 3.3.0
- **Maven**: 3.x

主要技术和框架
----------------------

Java 21
~~~~~~~

|Fess| 是在 Java 21 及以上运行的应用程序。
利用最新的 Java 功能，提高性能和可维护性。

- **推荐**: Eclipse Temurin 21（原 AdoptOpenJDK）
- **最低版本**: Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ 是
|Fess| Web 应用层使用的框架。

**主要功能:**

- DI（依赖注入）容器
- 基于 Action 的 Web 框架
- 验证
- 消息管理
- 配置管理

**学习资源:**

- `LastaFlute 官方文档 <https://github.com/lastaflute/lastaflute>`__
- 通过阅读 Fess 的代码可以学习实用用法

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ 是
用于数据库访问的 O/R 映射工具。
|Fess| 使用它从 OpenSearch 的模式自动生成 Java 代码。

**主要功能:**

- 类型安全的 SQL 构建器
- 从模式自动生成代码
- 自动生成数据库文档

**学习资源:**

- `DBFlute 官方网站 <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ 是
|Fess| 作为搜索引擎使用的分布式搜索・分析引擎。

**支持版本**: OpenSearch 3.3.0

**必需插件:**

- opensearch-analysis-fess: Fess 专用的形态素分析插件
- opensearch-analysis-extension: 附加语言分析功能
- opensearch-minhash: 相似文档检测
- opensearch-configsync: 配置同步

**学习资源:**

- `OpenSearch 文档 <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven 作为 |Fess| 的构建工具使用。

**主要用途:**

- 管理依赖库
- 执行构建处理
- 执行测试
- 创建包

开发工具
========

推荐的开发环境
----------------

Eclipse
~~~~~~~

官方文档说明使用 Eclipse 的开发方法。

**推荐版本**: Eclipse 2023-09 及以上

**必要插件:**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

也可以使用 IntelliJ IDEA 进行开发。

**推荐版本**: Community Edition 或 Ultimate Edition

**必要功能:**

- Maven 支持（默认包含）
- Java 支持

VS Code
~~~~~~~

轻量级开发也可以使用 VS Code。

**必要扩展:**

- Java Extension Pack
- Maven for Java

版本管理
~~~~~~~~~~~~

- **Git**: 源代码管理
- **GitHub**: 仓库托管、Issue 管理、拉取请求

必要知识
========

基础知识
--------

|Fess| 的开发需要以下知识：

**必需**

- **Java 编程**: 类、接口、泛型、Lambda 表达式等
- **面向对象**: 继承、多态、封装
- **Maven**: 基本命令和 pom.xml 的理解
- **Git**: clone、commit、push、pull、branch、merge 等

**推荐**

- **LastaFlute**: Action、Form、Service 的概念
- **DBFlute**: Behavior、ConditionBean 的用法
- **OpenSearch/Elasticsearch**: 索引、映射、查询的基础
- **Web 开发**: HTML、CSS、JavaScript（特别是前端开发的情况）
- **Linux 命令**: 服务器环境的开发・调试

学习资源
----------

初次接触 |Fess| 开发时，以下资源会有帮助：

官方文档
~~~~~~~~~~~~~~

- `Fess 用户手册 <https://fess.codelibs.org/ja/>`__
- `Fess 管理员指南 <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

社区
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 问题和讨论
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__: 错误报告和功能请求
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 日语社区论坛

源代码
~~~~~~~~~~

阅读实际代码是最有效的学习方法：

- 首先从小功能开始阅读
- 使用调试器跟踪代码的运行
- 参考现有的测试代码

开发的基本流程
==============

|Fess| 的开发一般按照以下流程进行：

1. **确认・创建 Issue**

   确认 GitHub 的 Issue，决定要处理的内容。
   对于新功能或错误修复，创建 Issue。

2. **创建分支**

   创建工作分支：

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **编码**

   进行功能实现或错误修复。

4. **测试**

   创建・执行单元测试，确认更改正确运行。

5. **提交**

   提交更改：

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **拉取请求**

   推送到 GitHub 并创建拉取请求：

   .. code-block:: bash

       git push origin feature/my-new-feature

详情请参阅 :doc:`workflow`。

项目结构概述
==================

|Fess| 的源代码具有以下结构：

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # Web 应用层
    │   │   │       │   ├── web/       # 搜索界面
    │   │   │       │   └── service/   # 服务层
    │   │   │       ├── crawler/       # 爬虫功能
    │   │   │       ├── es/            # OpenSearch 相关
    │   │   │       ├── helper/        # 辅助类
    │   │   │       ├── job/           # 作业处理
    │   │   │       ├── util/          # 实用工具
    │   │   │       └── FessBoot.java  # 启动类
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # JSP 文件
    │   └── test/
    │       └── java/                  # 测试代码
    ├── pom.xml                        # Maven 配置文件
    └── README.md

主要包
--------------

app
~~~

Web 应用层的代码。
包含管理界面和搜索界面的 Action、Form、Service 等。

crawler
~~~~~~~

Web 爬虫、文件爬虫、数据存储爬虫等
数据收集功能的代码。

es
~~

与 OpenSearch 集成的代码。
包含索引操作、构建搜索查询等。

helper
~~~~~~

应用程序中使用的辅助类。

job
~~~

定时执行的作业代码。
包含爬取作业、索引优化作业等。

详情请参阅 :doc:`architecture`。

开发环境的快速入门
=======================

说明以最少步骤设置开发环境并运行 |Fess| 的方法。

前提条件
--------

- 已安装 Java 21 及以上
- 已安装 Git
- 已安装 Maven 3.x

步骤
----

1. **克隆仓库**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **下载 OpenSearch 插件**

   .. code-block:: bash

       mvn antrun:run

3. **运行**

   从 Maven 运行：

   .. code-block:: bash

       mvn compile exec:java

   或者，从 IDE（Eclipse、IntelliJ IDEA 等）运行 ``org.codelibs.fess.FessBoot`` 类。

4. **访问**

   在浏览器中访问以下地址：

   - 搜索界面: http://localhost:8080/
   - 管理界面: http://localhost:8080/admin/
     - 默认用户: admin / admin

详细设置步骤请参阅 :doc:`setup`。

开发提示
==========

调试运行
----------

在 IDE 中调试运行时，运行 ``FessBoot`` 类。
通过设置断点可以详细跟踪代码的运行。

热部署
------------

LastaFlute 可以在不重启的情况下反映部分更改。
但是，类结构的更改等需要重启。

确认日志
--------

日志输出到 ``target/fess/logs/`` 目录。
出现问题时，请确认日志文件。

OpenSearch 的操作
----------------

内置的 OpenSearch 放置在 ``target/fess/es/``。
也可以直接调用 OpenSearch API 进行调试：

.. code-block:: bash

    # 确认索引
    curl -X GET http://localhost:9201/_cat/indices?v

    # 搜索文档
    curl -X GET http://localhost:9201/fess.search/_search?pretty

社区和支持
==================

问题和咨询
--------

开发中有问题或咨询时，请使用以下资源：

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 一般问题和讨论
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__: 错误报告和功能请求
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 日语论坛

贡献方法
--------

关于对 |Fess| 的贡献方法，请参阅 :doc:`contributing`。

下一步
==========

准备好设置开发环境后，请进入 :doc:`setup`。

关于详细信息，也请参阅以下文档：

- :doc:`architecture` - 架构和代码结构
- :doc:`workflow` - 开发工作流程
- :doc:`building` - 构建和测试
- :doc:`contributing` - 贡献指南

参考资料
========

官方资源
----------

- `Fess 官方网站 <https://fess.codelibs.org/ja/>`__
- `GitHub 仓库 <https://github.com/codelibs/fess>`__
- `下载页面 <https://fess.codelibs.org/ja/downloads.html>`__

技术文档
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

社区
----------

- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
