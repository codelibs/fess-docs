============================================================
第17回：通过插件扩展搜索 -- 自定义数据源与 Ingest 管道的实现
============================================================

前言
====

Fess 默认支持许多数据源，但要适配企业特有的系统和数据格式，可能需要通过插件进行扩展。

本文将介绍 Fess 的插件架构，并说明如何实现自定义数据源插件和 Ingest 插件。

目标读者
========

- 希望将 Fess 连接到自定义数据源的用户
- 对插件开发感兴趣的 Java 开发者
- 希望了解 Fess 内部架构的用户

插件架构
========

Fess 提供以下类型的插件。

.. list-table:: 插件类型
   :header-rows: 1
   :widths: 25 35 40

   * - 类型
     - 作用
     - 示例
   * - 数据存储 (fess-ds-*)
     - 从外部数据源获取数据
     - Slack、Salesforce、DB
   * - Ingest (fess-ingest-*)
     - 对爬取数据进行加工和转换
     - Example
   * - 主题 (fess-theme-*)
     - 搜索界面设计
     - Simple、Code Search
   * - 脚本 (fess-script-*)
     - 脚本语言支持
     - OGNL
   * - Web 应用 (fess-webapp-*)
     - Web 应用程序扩展
     - MCP Server

插件部署
--------

插件以 JAR 文件的形式提供，放置在 Fess 的插件目录中。
可以通过管理界面的 [系统] > [插件] 进行安装和管理。

自定义数据源插件开发
====================

本节以企业内部拥有自有文档管理系统为前提，介绍数据源插件的开发流程。

项目结构
--------

参考现有的数据存储插件（例如 fess-ds-git），创建 Maven 项目。

::

    fess-ds-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── java/
                └── org/codelibs/fess/ds/custom/
                    └── CustomDataStore.java

pom.xml 配置
-------------

指定 fess-parent 作为父 POM，并配置所需的依赖项。

.. code-block:: xml

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.5.0</version>
    </parent>

    <artifactId>fess-ds-custom</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

数据存储类的实现
----------------

数据存储插件的核心是负责获取数据并向 Fess 注册文档的类。

实现要点如下：

1. 与外部系统的连接和认证
2. 数据获取（API 调用、文件读取等）
3. 将获取的数据转换为 Fess 的文档格式
4. 文档注册

**字段映射**

将获取的数据映射到 Fess 的字段。
主要字段如下：

- ``title``：文档标题
- ``url``：文档 URL（搜索结果中的链接目标）
- ``content``：文档正文（搜索对象）
- ``mimetype``：MIME 类型
- ``last_modified``：最后修改时间

构建与部署
----------

::

    $ mvn clean package

将生成的 JAR 文件放置到 Fess 的插件目录中，然后重启 Fess。

Ingest 插件开发
================

Ingest 插件是一种在将爬取获得的文档注册到索引之前对其进行加工和转换的机制。

使用场景
--------

- 为爬取的文档添加额外字段
- 正文文本清洗（去除不必要的字符）
- 通过外部 API 添加信息（翻译、分类等）
- 日志输出（用于调试）

实现要点
--------

在 Ingest 插件中，可以访问文档注册到索引之前的数据，并执行转换处理。

例如，可以实现为所有文档添加组织名称元数据的处理，或从正文中去除特定模式的处理。

主题插件开发
=============

如果需要完全自定义搜索界面的设计，可以开发主题插件。

主题结构
--------

主题插件由 JSP 文件、CSS、JavaScript 和图片文件组成。

::

    fess-theme-custom/
    ├── pom.xml
    └── src/
        └── main/
            └── resources/
                ├── css/
                ├── js/
                ├── images/
                └── view/
                    ├── index.jsp
                    ├── search.jsp
                    └── header.jsp

参考现有主题，通过修改 JSP 和 CSS 实现自定义设计。

开发最佳实践
=============

参考现有插件
------------

在开发新插件时，强烈建议参考现有插件的源代码。
所有插件的源代码都在 CodeLibs 的 GitHub 仓库中公开。

例如，开发数据存储插件时，``fess-ds-git`` 和 ``fess-ds-slack`` 是很好的参考。

测试
----

从以下几个方面对插件进行测试：

- 与外部系统的连接测试
- 数据转换的准确性
- 错误处理（连接失败、数据异常等）
- 性能（大量数据的处理时间）

版本兼容性
----------

在升级 Fess 时，请确认插件的兼容性。
Fess 的主版本升级时，API 可能会发生变更。

总结
====

本文介绍了 Fess 的插件开发。

- 插件架构概述（数据存储、Ingest、主题、脚本）
- 自定义数据源插件的开发流程
- 通过 Ingest 插件进行文档加工
- 通过主题插件进行 UI 自定义
- 开发最佳实践

通过插件，可以将 Fess 扩展以满足组织特有的需求。
架构与扩展篇到此结束。从下一篇开始，将进入 AI 与下一代搜索篇，介绍语义搜索的基础知识。

参考资料
========

- `Fess 插件管理 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__

- `CodeLibs GitHub <https://github.com/codelibs>`__
