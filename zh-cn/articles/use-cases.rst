=========================
Fess 用例
=========================

简介
============

Fess 被各行各业不同规模的组织所采用。
本页介绍 Fess 部署的代表性用例和实际案例。

.. note::

   以下示例展示了 Fess 的常见部署模式。
   如需了解实际案例，请联系 `商业支持 <../support-services.html>`__。

----

按行业分类的用例
===========================

制造业
-------------

**挑战**: 设计图纸、技术文档和质量管理文档分散在多个文件服务器上，查找所需信息非常耗时。

**Fess 解决方案**:

- 对文件服务器上的 CAD 图纸、PDF 技术文档和 Office 文档进行统一搜索
- 按产品型号、图纸编号和项目名称进行跨搜索
- 基于访问权限显示搜索结果（基于角色的搜索）

**架构示例**:

.. code-block:: text

    [文件服务器]  →  [Fess]  →  [企业内部门户]
         │               │
         ├─ 图纸          ├─ OpenSearch 集群
         ├─ 技术文档      └─ Active Directory 集成
         └─ 质量记录

**相关功能**:

- `文件服务器爬取 <https://fess.codelibs.org/zh-cn/15.5/config/config-filecrawl.html>`__
- `基于角色的搜索 <https://fess.codelibs.org/zh-cn/15.5/config/config-role.html>`__
- `缩略图显示 <https://fess.codelibs.org/zh-cn/15.5/admin/admin-general.html>`__

金融保险业
------------------------------

**挑战**: 合规文档、合同和内部规章内容庞大，审计应对和咨询处理非常耗时。

**Fess 解决方案**:

- 内部规章、操作手册和 FAQ 的跨搜索
- 合同和申请文档的全文搜索
- 从过去的咨询记录中进行知识搜索

**安全功能**:

- 通过 LDAP/Active Directory 集成进行认证
- 通过 SAML 实现单点登录
- 通过访问令牌进行 API 认证

**相关功能**:

- `LDAP 认证 <https://fess.codelibs.org/zh-cn/15.5/config/config-security.html>`__
- `SAML 认证 <https://fess.codelibs.org/zh-cn/15.5/config/config-saml.html>`__

教育机构
---------

**挑战**: 研究论文、讲义资料和校园文档分散在各院系服务器上，信息共享困难。

**Fess 解决方案**:

- 从校园门户进行统一搜索
- 研究论文库搜索
- 讲义资料和课程大纲搜索

**架构示例**:

- 校园网站爬取
- 与论文库（DSpace 等）集成
- Google Drive / SharePoint 上的资料搜索

**相关功能**:

- `网页爬取 <https://fess.codelibs.org/zh-cn/15.5/config/config-webcrawl.html>`__
- `Google Drive 爬取 <https://fess.codelibs.org/zh-cn/15.5/config/config-crawl-gsuite.html>`__

IT 和软件行业
-------------

**挑战**: 源代码、文档、Wiki 和工单管理系统的信息分散，降低了开发效率。

**Fess 解决方案**:

- GitHub/GitLab 仓库的代码搜索
- Confluence/Wiki 页面搜索
- Slack/Teams 消息搜索

**开发者功能**:

- 通过搜索 API 与现有系统集成
- 代码高亮显示
- 按文件类型过滤

**相关功能**:

- `Git 仓库爬取 <https://fess.codelibs.org/zh-cn/15.5/config/config-crawl-git.html>`__
- `Confluence 爬取 <https://fess.codelibs.org/zh-cn/15.5/config/config-crawl-atlassian.html>`__
- `Slack 爬取 <https://fess.codelibs.org/zh-cn/15.5/config/config-crawl-slack.html>`__

----

按企业规模分类的用例
=====================

小型企业（100人以下）
------------------------------------

**特点**: 希望在有限的 IT 资源下轻松部署和运维。

**推荐配置**:

- 通过 Docker Compose 轻松部署
- 单服务器配置（Fess + OpenSearch）
- 所需内存：8GB 以上

**部署步骤**:

.. code-block:: bash

    # 5 分钟即可完成部署
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**费用**:

- 软件：免费（开源）
- 仅需服务器费用（云或本地部署）

中型企业（100-1000人）
----------------------------------------

**特点**: 多部门使用，需要一定程度的可用性保证。

**推荐配置**:

- 2 台 Fess 服务器（冗余配置）
- 3 节点 OpenSearch 集群
- 负载均衡器进行流量分配
- Active Directory 集成

**容量指南**:

- 文档数：最多 500 万
- 并发搜索用户：最多 100 人

**相关功能**:

- `集群配置 <https://fess.codelibs.org/zh-cn/15.5/install/clustering.html>`__
- `备份和恢复 <https://fess.codelibs.org/zh-cn/15.5/admin/admin-backup.html>`__

大型企业（1000人以上）
----------------------------------

**特点**: 大规模数据、高可用性、严格的安全要求。

**推荐配置**:

- 多台 Fess 服务器（运行在 Kubernetes 上）
- OpenSearch 集群（专用节点配置）
- 专用爬取服务器
- 与监控和日志收集基础设施集成

**可扩展性**:

- 文档数：可达数亿
- 通过 OpenSearch 分片拆分实现水平扩展

**企业功能**:

- 按部门的标签管理
- 详细的访问日志
- 通过 API 与其他系统集成

.. note::

   对于大规模部署，建议使用 `商业支持 <../support-services.html>`__。

----

技术用例
===================

内部 Wiki / 知识库搜索
-------------------------------------

**概述**: 实现跨 Confluence、MediaWiki 和内部 Wiki 的统一搜索。

**优势**:

- 跨多个 Wiki 系统的统一搜索
- 基于更新频率的自动爬取
- Wiki 页面的附件也纳入搜索范围

**实施步骤**:

1. 安装 Confluence Data Store 插件
2. 在管理面板中配置连接设置
3. 设置爬取计划（例如每天一次）

文件服务器统一搜索
--------------------------

**概述**: 搜索 Windows 文件服务器和 NAS 上的文档。

**支持的协议**:

- SMB/CIFS（Windows 共享文件夹）
- NFS
- 本地文件系统

**安全性**:

- 基于 NTLM 认证的访问控制
- 文件 ACL 反映在搜索结果中

**配置要点**:

- 创建专用的爬取账户
- 对大量文件进行分阶段爬取
- 考虑网络带宽

网站搜索（站内搜索）
----------------------------

**概述**: 为公共网站添加搜索功能。

**部署方式**:

1. **JavaScript 嵌入**

   使用 Fess Site Search（FSS），只需几行 JavaScript 即可添加搜索框

2. **API 集成**

   使用搜索 API 构建自定义搜索界面

**FSS 示例**:

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

数据库搜索
---------------

**概述**: 使关系型数据库中的数据可被搜索。

**支持的数据库**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**用例**:

- 客户主数据搜索
- 产品目录搜索
- FAQ 数据库搜索

**实施步骤**:

1. 配置 Database Data Store 插件
2. 使用 SQL 查询指定爬取目标
3. 配置字段映射

----

总结
=======

Fess 凭借其灵活的设计，可以满足各种行业、规模和用例的需求。

**考虑部署的用户**:

1. 首先通过 `快速构建指南 <../quick-start.html>`__ 试用 Fess
2. 在 `文档 <../documentation.html>`__ 中确认所需功能
3. 如需生产环境部署，请咨询 `商业支持 <../support-services.html>`__

**相关资源**:

- `文章列表 <../articles.html>`__ - 详细的技术文章
- `讨论论坛 <https://discuss.codelibs.org/c/fessja/>`__ - 社区支持
- `GitHub <https://github.com/codelibs/fess>`__ - 源代码和问题跟踪
