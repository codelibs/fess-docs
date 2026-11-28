=============================
Fess 与其他搜索解决方案的比较
=============================

前言
====

在为企业内部文档或网站内搜索选型时，候选方案除了 Fess 这样的搜索系统之外，还有基于 OpenSearch 或 Apache Solr 等搜索引擎的自主开发、外部 Web 搜索服务，以及商业企业搜索产品。
本文先以便于核对的形式整理 Fess 15.9 提供的功能，然后比较它与其他选项在定位上的差异。

.. note::

   关于 Fess 的描述以 15.9 为准。
   对于其他产品和服务，本文只讨论不易变化的架构差异。功能、价格和供应情况可能会变化，请以各产品的最新资料为准。

Fess 提供的功能
===============

Fess 是使用 OpenSearch 作为搜索引擎的搜索系统。
它将爬虫、管理界面、搜索界面和 API 作为一个应用程序提供，并将索引和爬取设置保存在 OpenSearch 中。
不能使用 Elasticsearch 或 Solr 作为搜索引擎。
许可证为 Apache License 2.0。

许多功能以插件形式提供，只需安装需要的插件。
下表中“所需条件”为空的项目，仅凭 Fess 本体即可使用。

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - 项目
     - 15.9 提供的功能
     - 所需条件
   * - Web 爬取
     - 爬取 HTTP/HTTPS 网站。可以设置 Web 认证、请求头和路径映射
     -
   * - 文件爬取
     - 爬取 ``file``\ 、\ ``smb``\ 、\ ``smb1``\ 、\ ``ftp`` 路径
     -
   * - 云存储爬取
     - ``s3://``\ （Amazon S3 及兼容 S3 的存储）、\ ``gcs://``\ （Google Cloud Storage）
     - ``fess-storage-s3``\ 、\ ``fess-storage-gcs``
   * - 数据库和 SaaS
     - 通过数据存储连接器导入（列表见下一节）
     - ``fess-ds-*`` 插件
   * - 文档格式
     - Office 文档、PDF、HTML、文本、压缩文件等。图像和扫描 PDF 的 OCR 默认禁用
     - OCR 需要 ``tesseract`` 命令
   * - 访问控制
     - 按角色、组、用户区分显示搜索结果。在 SMB 和文件爬取中，文件的访问权限会作为角色导入。与 LDAP（包括 Active Directory）的集成是本体功能
     -
   * - 单点登录
     - OpenID Connect、SAML、SPNEGO（Kerberos）、Microsoft Entra ID
     - ``fess-sso-oidc``\ 、\ ``fess-sso-saml``\ 、\ ``fess-sso-spnego``\ 、\ ``fess-sso-entraid``
   * - 搜索界面
     - 通过静态主题（将 HTML、CSS、JavaScript 打包成 ZIP）显示。内置主题为 ``bootstrap``
     -
   * - API
     - 用于搜索、标签、建议词、热门词、健康检查、AI 搜索模式等的 ``/api/v2``\ ，以及管理用的 ``/api/admin``
     -
   * - 旧版 API
     - ``/api/v1``\ 、\ ``/json``\ 和 ``/suggest``
     - ``fess-webapp-v1-api``\ 、\ ``fess-webapp-classic-api``
   * - 语义搜索
     - 将正文分块并向量化，再通过 Rank Fusion 与关键词搜索的结果合并。默认禁用
     - 嵌入模型（OpenSearch 的 ML Commons 或 ``fess-llm-*`` 插件）
   * - AI 搜索模式（RAG）
     - 由 LLM 以搜索结果为依据进行回答。默认禁用
     - ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、\ ``fess-llm-gemini``\ 、\ ``fess-llm-bedrock`` 中的任意一个
   * - MCP 服务器
     - 让 AI 代理可以通过 ``/mcp`` 搜索 Fess
     - ``fess-webapp-mcp``
   * - 图像搜索
     - 用文字查找图像（GIF、JPEG、PNG）的多模态搜索
     - ``fess-webapp-multimodal`` 和 CLIP 服务器

Docker 镜像内置了 4 个 SSO 插件、\ ``fess-storage-s3``\ 、\ ``fess-storage-gcs`` 和 ``fess-script-groovy``\ 。
其他插件请在 [系统] > [插件] 中安装，然后重启 Fess。
插件版本请选择与 Fess 相同的次版本（15.9 则为 15.9.x）。

数据存储连接器
--------------

面向 15.9 发布了以下数据存储插件。
设置方法请参阅各连接器的参考文档。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 分类
     - 插件（对象）
   * - 云存储
     - ``fess-ds-box``\ （Box）、\ ``fess-ds-dropbox``\ （Dropbox）、\ ``fess-ds-gsuite``\ （Google 云端硬盘）、\ ``fess-ds-microsoft365``\ （OneDrive、SharePoint Online、Teams 等）
   * - 协作
     - ``fess-ds-atlassian``\ （Confluence、Jira）、\ ``fess-ds-slack``\ （Slack）、\ ``fess-ds-notion``\ （Notion）、\ ``fess-ds-backlog``\ （Backlog）、\ ``fess-ds-sharepoint``\ （本地部署的 SharePoint Server）
   * - 开发与业务系统
     - ``fess-ds-git``\ （Git 仓库）、\ ``fess-ds-salesforce``\ （Salesforce）
   * - 数据
     - ``fess-ds-db``\ （可通过 JDBC 连接的数据库）、\ ``fess-ds-csv``\ （CSV）、\ ``fess-ds-json``\ （JSON）、\ ``fess-ds-wikipedia``\ （Wikipedia 转储）

此处没有列出的数据源，可以通过自行开发数据存储插件（:doc:`guide-17`），或通过管理用 API 注册文档（:doc:`guide-11`）使其成为搜索对象。

与基于搜索引擎（OpenSearch、Apache Solr）的自主开发的区别
=========================================================

OpenSearch 和 Apache Solr 是搜索引擎。
它们负责创建索引和执行搜索，但不包含收集数据的爬虫、供用户使用的搜索界面，以及按文档的访问控制。
这些部分需要自行开发，或组合其他软件。
例如，Web 爬取有 Apache Nutch 这样的独立项目。

Fess 是在 OpenSearch 之上提供了这些部分的应用程序。
区别如下。

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - 方面
     - Fess
     - 基于搜索引擎的自主开发
   * - 数据收集
     - 在管理界面中设置 Web、文件、数据存储的爬取
     - 自行编写爬虫和导入处理，或组合其他软件
   * - 搜索界面
     - 通过主题显示。如需改变外观，可以制作主题，或使用 API 构建自己的界面
     - 可以自由构建，但全部需要开发
   * - 访问控制
     - 将角色和文件访问权限记录在文档中，搜索时按登录用户进行筛选
     - 需要设计并实现文档权限的导入和搜索时的筛选
   * - 索引设计
     - 使用 Fess 定义的索引。已配置包括中文在内的多语言分析器
     - 可以根据用途自由设计
   * - 需要运维的部分
     - Fess 和 OpenSearch
     - 搜索引擎以及自行开发的所有部分

如果想从零开始设计搜索机制，或想搜索自有的数据结构，直接使用搜索引擎更为合适。
另一方面，如果目的是收集文档并让企业内部可以搜索，那么从 Fess 开始，再用 API 或插件补足不够的部分，可以缩小开发范围。

Fess 也可以连接到现有的 OpenSearch 集群。
在 Amazon OpenSearch Service 等无法安装 CodeLibs 插件的环境中，将 ``search_engine.type`` 设置为 ``aws`` 或 ``vanilla``\ 。
在这种情况下，词典管理、重复文档检测等部分功能无法使用（参见 `搜索引擎类型 <https://fess.codelibs.org/zh-cn/stable/config/search-engine-type.html>`__\ ）。

与使用外部 Web 搜索服务的站内搜索的区别
=======================================

也可以利用搜索服务提供商的索引来提供站内搜索。
采用这种方式时，能搜索到的仅限于提供商的爬虫抓取到的公开页面。
需要登录的页面和企业内部的文件服务器无法作为对象，何时爬取、以什么顺序显示也取决于提供商。

使用 Fess 时，由您自己决定爬取的对象和时间，索引放在自己的环境中。
调整搜索结果时，可以使用关键词匹配（让特定文档在特定词语下排在前面）、文档提升、相关查询等功能。
将其嵌入现有网站的方式有两种。

- 放置搜索表单，跳转到 Fess 的搜索界面（主题）
- 嵌入 Fess Site Search（FSS）的 JavaScript，在页面内显示搜索结果

FSS 会调用 ``/api/v1``\ ，因此在 15.9 中需要 ``fess-webapp-v1-api`` 插件。
操作步骤请参阅 :doc:`guide-03`\ 。

与商业企业搜索产品的区别
========================

与商业产品比较时，各产品的覆盖范围差异很大，无法一概而论孰优孰劣。
建议按以下方面，在相同条件下核对候选产品与 Fess。

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 方面
     - Fess 的情况
   * - 支持的数据源
     - 参见上一节的表格和数据存储连接器列表。如有不足，可以自行开发插件
   * - 访问控制
     - 按角色、组、用户控制，支持 LDAP 和 4 种 SSO 方式
   * - 生成式 AI
     - AI 搜索模式（RAG）、语义搜索、MCP 服务器。LLM 可从 Ollama（自行运维）、OpenAI、Gemini、Amazon Bedrock 中选择
   * - 数据存放位置
     - 索引存放在自行运维的 OpenSearch 中。如果对 LLM 或嵌入使用外部服务，问题和文档正文会被发送到该服务
   * - 运维形态
     - 自行运维的软件。可以通过 Docker、Linux（ZIP、RPM、DEB）、Windows 安装。也可以在 Kubernetes 上运行，但没有官方的 Helm Chart
   * - 费用与支持
     - 不需要许可证费用。费用为服务器和运维工时。商业支持请参见 `商业支持 <https://fess.codelibs.org/zh-cn/support-services.html>`__
   * - 修改的自由度
     - 源代码公开，可以通过主题、插件和 API 进行扩展

商业产品适合的情况是：产品已具备所需的连接器和管理功能，并希望将运维交给供应商。
Fess 适合的情况是：希望将数据保留在自己的环境中，组合所需的功能来构建搜索平台。

选型参考
========

按顺序回答以下问题，即可判断 Fess 是否可以作为候选。

1. 想要搜索的数据是否包含在 Fess 的爬取对象或数据存储连接器中？

   - 如果不包含，请估算自行开发插件（:doc:`guide-17`）或通过 API 注册（:doc:`guide-11`）所需的开发量。

2. 是否需要根据用户显示不同的文档？

   - 如需利用文件服务器的访问权限，请参阅 :doc:`file-server-search`\ ；角色设计请参阅 :doc:`guide-05`\ ；SSO 请参阅 :doc:`guide-15`\ 。

3. Fess 的主题能否满足搜索界面的需求？

   - 如需将搜索嵌入自己的应用程序，请使用 ``/api/v2``\ （:doc:`guide-11`）。

4. 能否自行运维 Fess 和 OpenSearch？

   - 如果无法运维，或希望将运维交给供应商，请考虑 Fess 的商业支持或商业产品。

5. 是否需要基于生成式 AI 的回答或语义搜索？

   - 确定要使用的 LLM，并在 :doc:`guide-19` 和 :doc:`guide-18` 中确认所需的配置。

如果 1 和 4 的答案为“是”，最可靠的做法是先试用 Fess，用实际文档确认搜索结果。

试用确认
========

仅凭比较表，无法了解自己的文档能被搜索到什么程度。
按照 :doc:`guide-02` 的步骤用 Docker 启动 Fess，爬取想要搜索的部分内容，然后确认以下几点。

- 目标文档是否已被导入（在 [系统信息] > [作业日志] 和 [失败URL] 中确认是否有出错的 URL）
- 用常用词语搜索时，期望的文档是否排在前面
- 切换登录用户后，不应看到的文档是否没有显示（需要访问控制时）

延伸阅读
========

- 想了解 Fess 的结构和整体文章的阅读顺序：:doc:`guide-01`
- 想先在本地运行起来：:doc:`guide-02`
- 想在现有网站中嵌入搜索：:doc:`guide-03`
- 想搜索数据库或 SaaS 中的数据：:doc:`datastore-basics`
- 想在搜索结果中反映文件服务器的访问权限：:doc:`file-server-search`
- 想让生成式 AI 根据企业内部文档回答：:doc:`guide-19`
- 想为规模扩大做准备：:doc:`guide-14`
- 想了解应用案例：:doc:`use-cases`

参考资料
========

- `数据存储连接器概述 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-overview.html>`__
- `文件抓取（文件服务器搜索） <https://fess.codelibs.org/zh-cn/stable/admin/fileconfig-guide.html>`__
- `搜索对象文件 <https://fess.codelibs.org/zh-cn/supported-files.html>`__
- `OCR 配置 <https://fess.codelibs.org/zh-cn/stable/config/crawler-ocr.html>`__
- `主题 <https://fess.codelibs.org/zh-cn/stable/admin/theme-guide.html>`__
- `API 概述 <https://fess.codelibs.org/zh-cn/stable/api/api-overview.html>`__
- `语义搜索 <https://fess.codelibs.org/zh-cn/stable/config/search-semantic.html>`__
- `AI 搜索（RAG）与 LLM 集成概述 <https://fess.codelibs.org/zh-cn/stable/config/llm-overview.html>`__
- `搜索引擎类型 <https://fess.codelibs.org/zh-cn/stable/config/search-engine-type.html>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
