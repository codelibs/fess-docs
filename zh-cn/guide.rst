========
实践指南
========

用 Fess 实现知识活用
====================

本实践指南介绍如何用 Fess 让企业内部的信息可被搜索，并将其发展为持续被使用的搜索平台。
各篇文章均以 Fess 15.9 为对象，具体说明设置页面中的项目、配置键，以及如何确认操作是否成功。
仅在 15.10 及以后版本中可用的功能，会在文中明确注明。

按目的选择
==========

- **想先试用一下**\ ：\ :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **想搜索文件服务器**\ ：\ :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **想搜索云端和 SaaS 中的数据**\ ：\ :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **想在现有网站或系统中嵌入搜索**\ ：\ :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **想按部门或用户区分显示的信息**\ ：\ :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **想用 AI 增强搜索**\ ：\ :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **开始生产环境运维**\ ：\ :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

入门
====

- :doc:`articles/guide-01` - Fess 的组成、本体与插件的分工，以及按目的选择的阅读路线
- :doc:`articles/guide-02` - 用 Docker Compose 启动 Fess，完整体验从爬取到搜索的流程

收集信息
========

- :doc:`articles/guide-04` - 爬取网站和文件服务器，并支持用标签筛选结果
- :doc:`articles/datastore-basics` - 数据存储插件的设置项、权限、标签、计划，以及结果的确认方法
- :doc:`articles/guide-07` - 将 Google Drive、SharePoint Online / OneDrive、Box 中的文件纳入搜索范围
- :doc:`articles/guide-06` - 将 Git 仓库、Confluence、Jira、Slack 中的信息纳入搜索范围
- :doc:`articles/guide-12` - 将数据库、CSV 文件、Salesforce 中的数据纳入搜索范围

嵌入搜索与调整显示方式
======================

- :doc:`articles/guide-03` - 在现有网站中放置搜索框，并用主题调整搜索页面的外观
- :doc:`articles/guide-11` - 使用搜索 API 和访问令牌，从业务系统中进行搜索和注册

控制访问
========

- :doc:`articles/guide-05` - 按角色和组区分显示搜索结果，并与 LDAP / Active Directory 集成
- :doc:`articles/guide-15` - 引入 SSO（OIDC / SAML / Entra ID / SPNEGO），保护来自外部的访问
- :doc:`articles/guide-13` - 通过虚拟主机和角色，让多个组织共用一个 Fess

提升搜索质量
============

- :doc:`articles/guide-08` - 在搜索日志的分析页面中发现问题，并通过同义词和关键词匹配加以改进
- :doc:`articles/guide-09` - 了解多语言文档如何被索引和搜索，并按语言进行调整
- :doc:`articles/guide-22` - 使用 OpenSearch Dashboards 自行统计和可视化搜索日志

运维
====

- :doc:`articles/guide-10` - 健康检查、日志、通知、备份与恢复，以及失败 URL 的处理
- :doc:`articles/guide-16` - 使用 fessctl 和管理 API 将设置作为代码管理，并重现环境
- :doc:`articles/guide-14` - 内存设置、外部 OpenSearch 集群，以及 Fess 的多台服务器配置
- :doc:`articles/guide-17` - 自行开发数据存储插件或 Ingester 来添加功能

用 AI 增强搜索
==============

- :doc:`articles/guide-18` - 借助向量搜索和排名融合，即使措辞不同也能找到文档
- :doc:`articles/guide-19` - 连接 LLM，使用以企业内部文档为依据进行回答的 AI 搜索模式
- :doc:`articles/guide-20` - 通过 MCP 服务器插件，让 AI 代理搜索 Fess
- :doc:`articles/guide-21` - 构建可同时搜索图像和文本的多模态搜索

规划全公司推广
==============

- :doc:`articles/guide-23` - 按从引入到全公司推广的各个阶段，整理需要配置和确认的事项

用例与比较
==========

- :doc:`articles/use-cases` - 按行业和规模划分的应用案例，以及对各案例有帮助的文章
- :doc:`articles/comparison` - Fess 与其他搜索解决方案（单独使用 OpenSearch、Solr、商业产品等）的比较
- :doc:`articles/file-server-search` - 引入文件服务器全文搜索之前需要确认的事项

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
