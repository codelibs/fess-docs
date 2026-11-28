=========================
Fess 的应用案例与使用场景
=========================

前言
====

本页按行业、规模和技术目的，介绍 Fess 常见的使用场景。
对于每个场景，说明要解决的问题、使用的 Fess 功能和插件，以及讲解具体步骤的文章。
设置步骤本身在各篇文章中，请从与自己情况相近的场景出发，选择要阅读的文章。

本文中的功能和插件名称以 Fess 15.9 为准。
在 15.9 中，从数据库和 SaaS 导入、SSO 以及 S3・GCS 的爬取都由插件提供。
插件请使用与 Fess 相同的 15.9.x 版本，安装后重启 Fess。
安装方法请参阅 `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__。

.. note::

   以下是一般的使用模式。关于实际的部署案例，请咨询 `商业支持 <../support-services.html>`__。

按目的查找功能
==============

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - 想做的事情
     - 使用的功能・插件
     - 要阅读的文章
   * - 先在本地运行试用
     - Docker Compose（docker-fess）
     - :doc:`guide-02`
   * - 统一搜索内部网站和文件服务器
     - Web 爬取、文件系统爬取、文件认证、标签
     - :doc:`guide-04`、:doc:`file-server-search`
   * - 按部门或职位显示不同的文档
     - 权限、角色・组、LDAP（Active Directory）
     - :doc:`guide-05`
   * - 在现有网站上放置搜索框
     - 搜索表单、Fess Site Search（``fess-webapp-v1-api``）、主题
     - :doc:`guide-03`
   * - 搜索 Git・Confluence・Jira・Slack
     - ``fess-ds-git``、``fess-ds-atlassian``、``fess-ds-slack``
     - :doc:`datastore-basics`、:doc:`guide-06`
   * - 搜索 Google Drive・SharePoint Online・Box
     - ``fess-ds-gsuite``、``fess-ds-microsoft365``、``fess-ds-box``
     - :doc:`datastore-basics`、:doc:`guide-07`
   * - 搜索数据库・CSV・Salesforce
     - ``fess-ds-db``、``fess-ds-csv``、``fess-ds-salesforce``
     - :doc:`datastore-basics`、:doc:`guide-12`
   * - 从业务系统中搜索
     - 搜索 API（``/api/v2``）、访问令牌
     - :doc:`guide-11`
   * - 使用企业内部的登录进行搜索
     - ``fess-sso-entraid``、``fess-sso-oidc``、``fess-sso-saml``、``fess-sso-spnego``
     - :doc:`guide-15`
   * - 一个 Fess 供多个组织分别使用
     - 虚拟主机、角色、标签
     - :doc:`guide-13`
   * - 调查搜不到的词和使用方式并加以改进
     - [系统信息] > [搜索日志]
     - :doc:`guide-08`
   * - 查找意思相近的文档、让 AI 回答问题
     - 语义搜索、AI 搜索模式、``fess-webapp-mcp``
     - :doc:`guide-18`、:doc:`guide-19`、:doc:`guide-20`
   * - 为文档数和用户的增长做准备
     - OpenSearch 的分离・集群化、Fess 的多台部署
     - :doc:`guide-14`
   * - 在生产环境中稳定运行
     - ``/api/v2/health``、备份、日志
     - :doc:`guide-10`

按行业的使用场景
================

制造业：查找分散的技术文档
--------------------------

**问题**：设计书、规格书和质量记录分散在各部门的文件服务器上，根据图纸编号或型号查找相关资料很费时间。

**使用的功能**：

- 用 ``smb://`` 爬取文件服务器，使 PDF 和 Office 文档的正文可以被搜索。Windows 的访问权限（ACL）默认会作为文档的权限导入
- 创建显示名称为“设计”“质量”之类的标签，按其覆盖的路径对文档分类，使用户可以在搜索页面上筛选
- 扫描的纸质记录在启用 OCR 后可以搜索正文。OCR 默认处于禁用状态，需要在运行爬虫的主机上安装 ``tesseract``\ （`OCR 配置 <https://fess.codelibs.org/zh-cn/stable/config/crawler-ocr.html>`__）

Fess 无法提取正文的格式的文件，只能通过文件名或路径找到。
支持的格式请在 `支持的文件 <../supported-files.html>`__ 中确认。

**要阅读的文章**：用 :doc:`guide-04` 搭建结构，在 :doc:`file-server-search` 中确认 ACL 的前提条件，再用 :doc:`guide-05` 设置按部门区分的显示范围。

金融・保险业：按权限查找规章和合同
----------------------------------

**问题**：内部规章、手册和合同数量庞大，每次应对咨询或审计时查找都很费力。同时，又希望按部门严格区分谁可以阅读。

**使用的功能**：

- 通过每个文档的权限，限定在搜索结果中显示给谁。新建爬取配置的权限中一开始就包含 ``{role}guest``，对于不公开的文档请将其删除
- 如果不允许未登录的用户搜索，请在 [通用] 中启用「需要登录」
- 通过企业内部的身份平台登录时使用 SSO。SAML 使用 ``fess-sso-saml``，Entra ID 使用 ``fess-sso-entraid``\ （Docker 镜像中已包含 4 个 SSO 插件）
- 从业务系统中搜索时，将访问令牌保存在服务器端，再调用搜索 API

**要阅读的文章**：用 :doc:`guide-05` 设计权限，用 :doc:`guide-15` 设置 SSO 和 HTTPS。与业务系统的集成请参阅 :doc:`guide-11`。

教育机构：跨校内网站和共享云端硬盘搜索
--------------------------------------

**问题**：各院系的网站、课程资料和校内文档分散在不同的地方，学生和教职员工都找不到想要的信息。

**使用的功能**：

- 通过 Web 爬取导入校内网站。机构知识库（DSpace 等）没有专用的连接器，因此对其公开页面进行 Web 爬取
- Google Drive 的共享云端硬盘用 ``fess-ds-gsuite`` 导入，SharePoint Online 用 ``fess-ds-microsoft365`` 导入
- 如果要为学生和教职员工区分可见范围，请用角色和权限加以区分。如果要拆分站点本身，请使用虚拟主机

**要阅读的文章**：:doc:`guide-04`、:doc:`guide-07`、:doc:`guide-05`。拆分站点时请参阅 :doc:`guide-13`。

IT・软件业：在一个地方查找开发信息
----------------------------------

**问题**：代码在 Git，设计在 Confluence，问题在 Jira，讨论在 Slack 或 Teams，过去的来龙去脉很难追溯。

**使用的功能**：

- 用 ``fess-ds-git`` 导入代码库中的文件，用 ``fess-ds-atlassian`` 导入 Confluence 和 Jira，用 ``fess-ds-slack`` 导入 Slack 的消息
- Teams 的频道和聊天可以用 ``fess-ds-microsoft365`` 的 ``TeamsDataStore`` 导入（`Microsoft 365 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-microsoft365.html>`__）
- 作为专门用于源代码搜索的结构，已公开 `docker-codesearch <https://github.com/codelibs/docker-codesearch>`__
- 在内部工具中嵌入搜索时使用搜索 API，让 AI 代理进行搜索时使用 ``fess-webapp-mcp``

**要阅读的文章**：先读 :doc:`datastore-basics`，再读 :doc:`guide-06`。与 AI 代理的集成请参阅 :doc:`guide-20`。

按规模的使用场景
================

所需的服务器台数和内存，并不只由用户数或文档数决定。
负载会随正文长度、附件所占比例以及是否登录使用而变化，因此请先小规模运行并进行测量，再增加不足的部分。
判断步骤汇总在 :doc:`guide-14` 中关于规模参考的一节。
生产环境服务器的推荐配置（CPU 4 核以上、内存 8GB 以上等）请参阅 `系统要求 <https://fess.codelibs.org/zh-cn/stable/install/prerequisites.html>`__。

从 1 台开始
-----------

在以部门为单位的部署或试运行中，将 Fess 和 OpenSearch 运行在 1 台服务器上。
使用 Docker Compose 时，用 ``compose.yaml`` 和 ``compose-opensearch3.yaml`` 两个文件启动。
步骤见 :doc:`guide-02`。

即使是 1 台的结构，也要从一开始就确定以下两点。

- 备份方式。设置可以在 [系统信息] > [备份] 中获取，但不包含词典（:doc:`guide-10`）
- 使用 Docker 时，在 [系统] > [通用] 中更改的设置保存在容器内的 ``system.properties`` 中，重新创建容器后会恢复原状（见 :doc:`guide-02` 中关于停止与重新启动的一节）

使用部门增加时
--------------

当搜索或爬取变慢时，首先确认原因在于 Fess 本身、爬虫还是 OpenSearch。
多数情况下，按以下顺序扩展。

1. 保持 1 台，调整 Fess、爬虫和 OpenSearch 的堆内存以及爬取的并行度
2. 将 OpenSearch 分离到另一台服务器
3. 将 OpenSearch 组成 3 台的集群
4. 将 Fess 增加到多台，并用负载均衡器分配请求

将 Fess 部署为多台时，要在所有服务器上统一 [通用] 中的设置、``fess_config.properties`` 中的 ``app.cipher.key`` 以及已安装的插件。
Fess 15.9 的登录会话保存在各台服务器的内存中，因此在分配需要登录使用的页面时，请在负载均衡器上启用粘性会话。
将会话保存到 OpenSearch 以在多台服务器之间共享的功能，从 15.10 起可以使用。

**要阅读的文章**：:doc:`guide-14`、:doc:`guide-10`。

在全公司使用
------------

在全公司规模下，除上述结构外还要考虑以下几点。

- 确定由 1 台 Fess 负责爬取（``scheduler.target.name`` 和作业的「目标」）。这样可以避免让接受搜索的服务器承担爬取负载
- 将 ``/api/v2/health`` 用于负载均衡器和监控。当 OpenSearch 集群为 ``RED`` 或无法连接时，它会返回 503
- 如果要按组织区分搜索页面或搜索对象，请使用虚拟主机，或者分开 Fess 实例（:doc:`guide-13`）
- 定期在搜索日志中检查结果为 0 条的词和未被点击的词（:doc:`guide-08`）

也可以在 Kubernetes 上运行，但没有提供官方的 Helm Chart。
请转换 Docker Compose 的文件，或者自行编写清单（见 `Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__ 中的 FAQ）。

在大规模环境中部署时，也请考虑利用 `商业支持 <../support-services.html>`__。

技术性使用场景
==============

跨内部 Wiki・知识库搜索
-----------------------

导入方式因 Wiki 的种类而异。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 对象
     - 导入方式
     - 参考
   * - Confluence
     - ``fess-ds-atlassian``\ （``ConfluenceDataStore``）
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Notion 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Backlog 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-backlog.html>`__
   * - MediaWiki 等可在 Web 上浏览的 Wiki
     - Web 爬取（需要登录时也要设置 Web认证）
     - :doc:`guide-04`

通过数据存储导入的文档，其权限中一开始也包含 ``{role}guest``。
导入只有特定人员可以阅读的空间时，请先阅读 :doc:`guide-06` 中关于决定向谁显示搜索结果的一节。

文件服务器的统一搜索
--------------------

Fess 15.9 的文件爬取支持的协议如下。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 路径格式
     - 对象
   * - ``smb://``
     - Windows 的共享文件夹，或通过 SMB 共享的 NAS
   * - ``smb1://``
     - 仅支持 SMB1 的旧服务器
   * - ``file:``
     - 从 Fess 服务器可以访问的目录。NFS 共享需先在操作系统中挂载，再以此格式指定
   * - ``ftp://``
     - FTP 服务器
   * - ``s3://`` / ``gcs://``
     - Amazon S3 兼容存储 / Google Cloud Storage。需要 ``fess-storage-s3`` / ``fess-storage-gcs``\ （Docker 镜像中已包含）

默认启用的是 ``file``、``smb``、``smb1`` 和 ``ftp``\ （``crawler.file.protocols``）。
要在搜索结果中反映 SMB 的 ACL，需要从爬取配置的权限中删除 ``{role}guest``。
原因和确认方法见 :doc:`file-server-search`，具体设置见 :doc:`guide-04`。

网站内搜索
----------

为公开网站添加搜索功能的方法有 3 种，可以组合使用。

- 放置搜索表单，跳转到 Fess 的搜索页面。Fess 端无需额外设置
- 用 Fess Site Search（FSS）在现有页面中显示搜索结果。FSS 会调用 ``/api/v1``，因此在 15.9 中需要插件 ``fess-webapp-v1-api``。Fess 不提供 FSS 的 JavaScript，请用 FSS JS Generator 生成后放到自己的网站上
- 用主题使 Fess 的搜索页面与现有网站的外观保持一致

步骤见 :doc:`guide-03`。
如果要制作自己的搜索页面，请使用 ``/api/v2/search``\ （:doc:`guide-11`）。

数据库搜索
----------

像产品主数据或 FAQ 这样存放在数据库中的信息，用 ``fess-ds-db`` 导入。
支持兼容 JDBC 的数据库（MySQL、PostgreSQL、Oracle、SQL Server 等），需要另外准备与连接对象匹配的 JDBC 驱动。
通过脚本将 SELECT 语句获取的列映射到 ``title``、``content`` 等字段。

如果拼接出原业务页面的 URL 并放入 ``url``，用户就可以通过搜索结果的链接直接打开原始数据。
步骤见 :doc:`guide-12`。

与生成式 AI 结合
----------------

- 即使关键词不一致，也能找到意思相近的文档：语义搜索（:doc:`guide-18`）
- 以内部文档为依据让 AI 回答：AI 搜索模式。即使没有向量搜索也可以使用（:doc:`guide-19`）
- 让 Claude Code 等 AI 代理搜索 Fess：``fess-webapp-mcp``\ （:doc:`guide-20`）

无论哪种方法，被搜索的文档都按与普通搜索相同的权限进行筛选（AI 搜索模式使用已登录用户的权限，MCP 使用访问令牌的权限；在 MCP 中不使用认证时则为访客的权限）。
传递给 AI 的文档也由这些权限决定，因此请先完成 :doc:`guide-05` 中的权限设计。

部署的推进方式
==============

1. 用 :doc:`guide-02` 启动 Fess，爬取部分对象并尝试搜索
2. 从上面的表格中选择符合自己问题的文章并进行设置
3. 确定权限（:doc:`guide-05`）和运维（:doc:`guide-10`）之后，再向用户开放

参考资料
========

- `快速入门 <../quick-start.html>`__
- `文档 <../documentation.html>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `数据存储连接器指南 <https://fess.codelibs.org/zh-cn/stable/config/datastore/index.html>`__
- `讨论论坛 <https://discuss.codelibs.org/c/FessEN/>`__
- `GitHub <https://github.com/codelibs/fess>`__
