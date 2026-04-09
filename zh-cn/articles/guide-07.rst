============================================================
第7回 云存储时代的搜索策略 -- Google Drive、SharePoint、Box 的跨平台搜索
============================================================

前言
========

在许多企业中，使用云存储已经成为常态。
然而，不同部门和用途使用不同云存储的情况也并不少见。
"那个文件是在 Google Drive 上，还是在 SharePoint 上，又或者在 Box 上"——这样的困扰会降低工作效率。

本文将介绍如何通过 Fess 整合多个云存储，构建一个从单一搜索框即可跨平台搜索所有云端文件的环境。

目标读者
========

- 使用多个云存储的组织管理员
- 对云存储搜索存在困扰的人员
- 了解 OAuth 认证基本概念的人员

场景
========

某企业使用了以下云存储服务。

.. list-table:: 云存储使用情况
   :header-rows: 1
   :widths: 25 35 40

   * - 服务
     - 使用部门
     - 主要用途
   * - Google Drive
     - 销售部、市场部
     - 提案书、报告书、电子表格
   * - SharePoint Online
     - 全公司通用
     - 公司内部门户、共享文档
   * - Box
     - 法务部、财务部
     - 合同、发票、机密文档

云存储连接准备
=============================

安装数据存储插件
------------------------------------

云存储的爬取需要使用以下插件。

- ``fess-ds-gsuite``: Google Drive / Google Workspace 的爬取
- ``fess-ds-microsoft365``: SharePoint Online / OneDrive 的爬取
- ``fess-ds-box``: Box 的爬取

从管理界面的 [系统] > [插件] 进行安装。

OAuth 认证设置
----------------

访问云存储的 API 需要进行 OAuth 认证设置。
在各服务的管理控制台中注册应用程序，获取客户端 ID 和密钥。

**通用步骤**

1. 在各服务的管理控制台中注册应用程序
2. 设置所需的 API 作用域（权限）（只读权限即可）
3. 获取客户端 ID 和客户端密钥
4. 在 Fess 的数据存储设置中配置这些信息

各服务的设置
=================

Google Drive 的设置
--------------------

将 Google Drive 的文件设为搜索对象。

**在 Google Cloud Console 中的准备工作**

1. 在 Google Cloud Console 中创建项目
2. 启用 Google Drive API
3. 创建服务账号并下载 JSON 密钥文件
4. 将服务账号添加到目标云端硬盘或文件夹的共享设置中

**在 Fess 中的设置**

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称：选择 GoogleDriveDataStore
3. 设置参数和脚本
4. 标签：设置为 ``google-drive``

**参数设置示例**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**脚本设置示例**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

从服务账号的 JSON 密钥文件中获取 ``private_key``、``private_key_id``、``client_email`` 的值并进行设置。Google 文档、电子表格、幻灯片等 Google 专有格式也可以作为文本进行提取和搜索。

SharePoint Online 的设置
-------------------------

将 SharePoint Online 的文档库设为搜索对象。

**在 Entra ID（Azure AD）中的准备工作**

1. 在 Entra ID 中注册应用程序
2. 设置 Microsoft Graph API 的权限（如 Sites.Read.All 等）
3. 创建客户端密钥或证书

**在 Fess 中的设置**

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称：选择 SharePointDocLibDataStore（适用于文档库。根据用途还可以使用 SharePointListDataStore、SharePointPageDataStore、OneDriveDataStore 等）
3. 设置参数和脚本
4. 标签：设置为 ``sharepoint``

**参数设置示例**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**脚本设置示例**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

``tenant``、``client_id``、``client_secret`` 设置为在 Entra ID 应用程序注册中获取的值。指定 ``site_id`` 后将仅爬取特定站点。省略时将爬取所有可访问的站点。

Box 的设置
-----------

将 Box 的文件设为搜索对象。

**在 Box Developer Console 中的准备工作**

1. 在 Box Developer Console 中创建自定义应用程序
2. 认证方式选择"服务器认证（附带客户端凭据）"
3. 请管理员审批应用程序授权

**在 Fess 中的设置**

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称：选择 BoxDataStore
3. 设置参数和脚本
4. 标签：设置为 ``box``

**参数设置示例**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**脚本设置示例**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

设置在 Box Developer Console 中创建的自定义应用程序的认证信息。可以通过 ``supported_mimetypes`` 使用正则表达式筛选爬取目标的文件格式。

跨平台搜索优化
=================

增量爬取的应用
------------------

在爬取云存储时，与其每次获取所有文件，不如只获取自上次爬取以来更新的文件，即增量爬取，这样更加高效。

请确认各插件的设置中是否提供了增量爬取选项。
通过增量爬取可以减少 API 调用次数，缩短爬取时间。

搜索结果的 URL
--------------

对于从云存储爬取的文档，点击搜索结果中的链接将在各服务的 Web UI 中打开文件。
这对于用户来说是自然的操作，通常不需要特别的设置。

运维注意事项
===============

OAuth 令牌的更新
--------------------

在与云存储的集成中，需要注意 OAuth 令牌的有效期。

- **Google Drive**: 使用服务账号时，令牌会自动更新
- **SharePoint Online**: 客户端密钥有有效期，需要定期更新
- **Box**: 可能需要重新审批应用程序授权

建议将令牌有效期登记到日历中，以防止因过期导致爬取中断。

API 用量监控
----------------

云存储的 API 存在用量限制。
特别是在爬取大量文件时，需要监控 API 用量，调整爬取设置以避免超出限制。

权限与安全
------------------

请为 Fess 使用的云存储服务账号设置只读访问权限。
不需要写入权限，应遵循最小化安全风险的原则。

此外，结合第5回中介绍的基于角色的搜索功能，还可以实现与云存储权限体系相匹配的搜索结果控制。

总结
======

本文介绍了如何通过 Fess 整合 Google Drive、SharePoint Online、Box 三个云存储，构建跨平台搜索环境。

- 各云存储的数据存储插件和 OAuth 认证设置
- 通过标签区分和筛选信息来源
- 通过增量爬取优化搜索体验
- OAuth 令牌管理和 API 用量监控

无需考虑"文件在哪个云端"，即可立即找到所需文件的环境由此实现。

下一回将介绍持续改善搜索质量的调优循环。

参考资料
========

- `Fess 数据存储设置 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess 插件一览 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
