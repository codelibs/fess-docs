=========================
Fess 能做什么以及如何引入
=========================

前言
====

企业内部的文档分散存放在网站、文件服务器、云存储、聊天和工单管理等 SaaS 以及数据库中。
即使各个工具都有搜索功能，也无法跨越这些位置一次性进行查找。
Fess 是一款搜索服务器，它从这些位置收集文档并汇总到一个索引中，让用户可以通过一个搜索页面或 API 进行查找。

本文面向正在考虑引入 Fess 的信息系统部门负责人和开发人员，介绍以下内容：

- Fess 由哪些部分组成，以及它如何运行
- 哪些功能可以直接使用，哪些功能需要添加插件
- 根据不同目的，应该从哪篇文章开始阅读

各功能的配置步骤将在相应的文章中介绍。

本实践指南面向的版本
====================

实践指南中的各篇文章均以 Fess 15.9 为对象。
页面上的项目名称、配置键和默认值均已在 15.9 中确认。
介绍仅在 15.10 及以后版本中可用的功能时，会在文中明确注明。

指向参考文档的链接以 ``https://fess.codelibs.org/zh-cn/stable/`` 开头，指向当前稳定版的文档。
如果使用的是其他版本，请将 URL 中的 ``stable`` 替换为版本号（例如 ``15.9``\ ），在相应页面上确认项目名称和默认值。

什么是 Fess
===========

Fess 是一款用 Java 编写的开源全文搜索服务器。
它采用 Apache License 2.0 许可证，在商业环境中也可以免费使用。

文档的存储和搜索使用 OpenSearch。
Fess 15.9 在启动时会检查连接目标，如果不是 OpenSearch 3 及以上版本，就会中止启动。
它无法连接 OpenSearch 2 及更早版本，也无法连接 Elasticsearch。
15.9 移除了以前内置在 Fess 中的搜索引擎，因此必须另外准备 OpenSearch（在 Docker 配置中，OpenSearch 容器也会一同启动）。

一个 Fess 实例包含以下全部内容：

- 收集文档的爬虫（Web、文件服务器，以及通过插件接入的各种服务）
- 用于配置爬取设置、用户、权限、词典、计划等的管理页面
- 供用户使用的搜索页面
- 供外部系统调用搜索和建议功能的 API（\ ``/api/v2/``\ ）

搜索页面由打包了 HTML、CSS 和 JavaScript 的静态主题显示。
Fess 自带 ``bootstrap`` 主题，其他主题可以作为 ZIP 文件在 [系统] > [主题] 中添加。

Fess 的组成
===========

运行 Fess 时涉及的组件如下。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 组件
     - 作用
   * - Fess 本体（Web 应用程序）
     - 提供搜索页面、管理页面和 API。调度器也在这里运行，会在设定的时间启动爬取等作业
   * - 爬虫（独立进程）
     - 爬取作业作为独立于 Fess 本体的 Java 进程启动。它获取网页和文件，提取正文并注册到 OpenSearch。生成建议、生成缩略图以及为语义搜索生成向量的作业，也同样在独立的进程中运行
   * - OpenSearch
     - 保存待搜索文档的索引并执行搜索。爬取设置、用户、作业日志、搜索日志等在管理页面中注册的大部分信息也保存在这里

由于爬虫是独立的 Java 进程，其使用的内存也需要与 Fess 本体分开配置（在 :doc:`guide-14` 中介绍）。

文档变为可搜索的流程如下：

1. 在管理页面中注册爬取设置（目标 URL 或路径、决定向谁显示搜索结果的权限等）
2. 调度器启动爬取作业。也可以在管理页面中通过 [立即开始] 手动启动
3. 爬虫获取文档，提取正文，并将其与权限一起注册到 OpenSearch
4. 用户搜索时，Fess 会先按照用户的角色和组筛选结果，然后再返回

从用 Docker 启动到爬取、搜索的整个操作流程，可以在 :doc:`guide-02` 中实际体验。

本体功能与插件
==============

在 Fess 15.9 中，许多功能以插件的形式与本体分开提供。
所需的插件是否已预先安装，取决于安装方式。

- 通过 ZIP、RPM、DEB 安装的 Fess 不包含任何插件
- Docker 标准镜像（例如 ``ghcr.io/codelibs/fess:15.9.0``\ ）预装了以下 7 个插件：\ ``fess-script-groovy``\ 、\ ``fess-storage-s3``\ 、\ ``fess-storage-gcs``\ 、\ ``fess-sso-saml``\ 、\ ``fess-sso-spnego``\ 、\ ``fess-sso-entraid``\ 、\ ``fess-sso-oidc``
- Docker slim 镜像（例如 ``15.9.0-slim``\ ）不包含插件

下表汇总了主要功能及其所需的插件。

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - 功能
     - 仅本体即可使用
     - 需要插件
   * - 爬取
     - Web（http、https）、文件系统、文件服务器（SMB）、FTP
     - Amazon S3（\ ``fess-storage-s3``\ ）、Google Cloud Storage（\ ``fess-storage-gcs``\ ）、在浏览器中执行 JavaScript 来获取页面的 Web 爬取（\ ``fess-crawler-playwright``\ ）
   * - SaaS、数据库等
     - 数据存储的配置页面及其运行机制
     - 针对每种导入对象的数据存储插件（\ ``fess-ds-*``\ ）。Slack、Confluence 和 Jira、Google Drive、Microsoft 365、Box、数据库、CSV、Git 等
   * - 登录与权限
     - 在 Fess 中注册的用户、角色、组，以及与 LDAP / Active Directory 的集成
     - SSO（OpenID Connect 使用 ``fess-sso-oidc``\ ，SAML 使用 ``fess-sso-saml``\ ，Entra ID 使用 ``fess-sso-entraid``\ ，SPNEGO 使用 ``fess-sso-spnego``\ ）
   * - 脚本
     - JavaScript
     - Groovy（\ ``fess-script-groovy``\ ）、OGNL（\ ``fess-script-ognl``\ ）
   * - 搜索页面
     - 自带主题 ``bootstrap``
     - 不是插件，而是添加主题的 ZIP 文件
   * - API
     - ``/api/v2/``\ （搜索、标签、建议、热门词、健康检查等）和管理 API
     - ``/api/v1/``\ （\ ``fess-webapp-v1-api``\ ）、\ ``/json`` 和 ``/suggest``\ （\ ``fess-webapp-classic-api``\ ）。Fess Site Search 使用 ``/api/v1/``\ ，因此需要 ``fess-webapp-v1-api``
   * - AI 相关
     - 语义搜索和 AI 搜索模式（RAG）的机制。如果使用部署在 OpenSearch 中的嵌入模型，语义搜索不需要插件
     - 与 LLM 或外部嵌入模型的连接（\ ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、\ ``fess-llm-gemini``\ 、\ ``fess-llm-bedrock``\ ）、MCP 服务器（\ ``fess-webapp-mcp``\ ）、图像搜索（\ ``fess-webapp-multimodal``\ ）

在表中“需要插件”一列中，Docker 标准镜像只包含 S3 和 GCS、4 种 SSO 以及 Groovy。
其他插件无论采用哪种安装方式，都需要另外安装。

脚本类型指定为 Groovy 的设置，以及从以前版本沿用下来、没有记录脚本类型的设置，都会作为 Groovy 执行。
要使用这些设置，需要 ``fess-script-groovy``\ 。
新建的数据存储设置中，脚本类型的初始值为 JavaScript。

可以通过以下任一方式安装插件。
安装或删除插件后，需要重启 Fess。
插件的版本应与 Fess 的版本保持一致（Fess 15.9 对应 15.9.x）。

- 在管理页面的 [系统] > [插件] 中点击 [安装]，然后从列表中选择
- 在命令行中执行 ``bin/fess-setup install plugin <插件名>:<版本>``
- 在 Docker 中，在环境变量 ``FESS_PLUGINS`` 中以空格分隔指定，例如 ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0``

数据存储插件的用法在 :doc:`datastore-basics` 中介绍，自行开发插件的方法在 :doc:`guide-17` 中介绍。

可搜索的文件格式
================

从文件中提取正文时，使用 Apache Tika 等提取处理。
可以搜索 HTML、PDF、Microsoft Office 文档、文本、压缩文件中的内容等。
已确认的格式列表请参阅 `搜索对象文件 <https://fess.codelibs.org/zh-cn/supported-files.html>`__\ 。

图像以及扫描生成的 PDF 中的文字，默认情况下无法搜索。
在运行爬虫的主机上安装 ``tesseract`` 并启用 OCR 后，就可以搜索了。
具体步骤请参阅 `OCR（图像文字识别）配置 <https://fess.codelibs.org/zh-cn/stable/config/crawler-ocr.html>`__\ 。

选择安装方式
============

Fess 以 Docker、ZIP、RPM、DEB 的形式发布。
如果想先试用，可以一并启动 Fess 和 OpenSearch 的 Docker 是最快捷的方式。
具体步骤在 :doc:`guide-02` 中介绍。

在生产环境中，也可以将 OpenSearch 作为独立的服务器或集群来准备。
所需的 Java 和 OpenSearch 版本，以及 CPU、内存、磁盘的参考配置，请确认 `系统要求 <https://fess.codelibs.org/zh-cn/stable/install/prerequisites.html>`__\ 。

按目的选择阅读路线
==================

文章按照目的划分，便于按需阅读。
请选择最接近您目的的一行，从左到右依次阅读文章。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 目的
     - 要阅读的文章
   * - 想先试用一下
     - :doc:`guide-02`
   * - 想搜索文件服务器
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - 想搜索云端和 SaaS 中的数据
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - 想在现有网站或系统中嵌入搜索
     - :doc:`guide-03` → :doc:`guide-11`
   * - 想按部门或用户区分显示的信息
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - 想用 AI 增强搜索
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - 开始生产环境运维
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

此外还有以下文章：

- 提升搜索质量：\ :doc:`guide-08`\ 、\ :doc:`guide-09`\ 、\ :doc:`guide-22`
- 同时搜索图像和文本：\ :doc:`guide-21`
- 自行开发插件：\ :doc:`guide-17`
- 规划全公司推广：\ :doc:`guide-23`
- 应用案例以及与其他产品的比较：\ :doc:`use-cases`\ 、\ :doc:`comparison`

文章列表也汇总在 :doc:`../guide` 页面中。

参考资料
========

- `Fess 文档（稳定版） <https://fess.codelibs.org/zh-cn/stable/>`__
- `系统要求 <https://fess.codelibs.org/zh-cn/stable/install/prerequisites.html>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `插件架构 <https://fess.codelibs.org/zh-cn/stable/dev/plugin-architecture.html>`__
- `主题 <https://fess.codelibs.org/zh-cn/stable/admin/theme-guide.html>`__
- `搜索对象文件 <https://fess.codelibs.org/zh-cn/supported-files.html>`__
- `docker-fess（GitHub） <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess（GitHub） <https://github.com/codelibs/fess>`__
