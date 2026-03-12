==================================
Atlassian连接器
==================================

概述
====

Atlassian连接器提供从Atlassian产品（Jira、Confluence）获取数据并
注册到 |Fess| 索引的功能。

此功能需要 ``fess-ds-atlassian`` 插件。

支持的产品
========

- Jira（Cloud / Server / Data Center）
- Confluence（Cloud / Server / Data Center）

前提条件
========

1. 需要安装插件
2. 需要Atlassian产品的适当认证信息
3. Cloud版可使用OAuth 2.0，Server版可使用OAuth 1.0a或Basic认证

插件安装
------------------------

从管理界面的"系统"→"插件"安装：

1. 从Maven Central下载 ``fess-ds-atlassian-X.X.X.jar``
2. 从插件管理界面上传并安装
3. 重启 |Fess|

设置方法
========

从管理界面的"爬虫"→"数据存储"→"新建"进行设置。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 名称
     - Company Jira/Confluence
   * - 处理器名
     - JiraDataStore 或 ConfluenceDataStore
   * - 启用
     - 开

参数设置
----------------

Cloud版（OAuth 2.0）示例：

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Server版（Basic认证）示例：

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Server版（OAuth 1.0a）示例：

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必须
     - 说明
   * - ``home``
     - 是
     - Atlassian实例的URL
   * - ``is_cloud``
     - 是
     - Cloud版为 ``true``，Server版为 ``false``
   * - ``auth_type``
     - 是
     - 认证类型：``oauth``、``oauth2``、``basic``
   * - ``oauth.consumer_key``
     - OAuth 1.0a时
     - Consumer Key（通常为 ``OauthKey``）
   * - ``oauth.private_key``
     - OAuth 1.0a时
     - RSA私钥（PEM格式）
   * - ``oauth.secret``
     - OAuth 1.0a时
     - 验证码
   * - ``oauth.access_token``
     - OAuth 1.0a时
     - 访问令牌
   * - ``oauth2.client_id``
     - OAuth 2.0时
     - 客户端ID
   * - ``oauth2.client_secret``
     - OAuth 2.0时
     - 客户端密钥
   * - ``oauth2.access_token``
     - OAuth 2.0时
     - 访问令牌
   * - ``oauth2.refresh_token``
     - 否
     - 刷新令牌（OAuth 2.0）
   * - ``oauth2.token_url``
     - 否
     - 令牌URL（OAuth 2.0，有默认值）
   * - ``basic.username``
     - Basic认证时
     - 用户名
   * - ``basic.password``
     - Basic认证时
     - 密码
   * - ``issue.jql``
     - 否
     - JQL（仅Jira，高级搜索条件）

脚本设置
--------------

Jira的情况
~~~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

可用字段：

- ``issue.view_url`` - 问题的URL
- ``issue.summary`` - 问题摘要
- ``issue.description`` - 问题描述
- ``issue.comments`` - 问题评论
- ``issue.last_modified`` - 最后更新时间

Confluence的情况
~~~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

可用字段：

- ``content.view_url`` - 页面URL
- ``content.title`` - 页面标题
- ``content.body`` - 页面正文
- ``content.comments`` - 页面评论
- ``content.last_modified`` - 最后更新时间

OAuth 2.0认证设置
===================

Cloud版的情况（推荐）
---------------------

1. 在Atlassian Developer Console创建应用程序
2. 获取OAuth 2.0认证信息
3. 设置所需范围：

   - Jira：``read:jira-work``、``read:jira-user``
   - Confluence：``read:confluence-content.all``、``read:confluence-user``

4. 获取访问令牌和刷新令牌

OAuth 1.0a认证设置
====================

Server版的情况
--------------

1. 在Jira或Confluence中创建Application Link
2. 生成RSA密钥对：

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. 将公钥注册到Application Link
4. 将私钥设置到参数中

Basic认证设置
===============

Server版的简单设置
------------------------

.. warning::
   Basic认证在安全方面不推荐使用。请尽可能使用OAuth认证。

使用Basic认证时：

1. 准备具有管理员权限的用户账户
2. 将用户名和密码设置到参数中
3. 使用HTTPS确保安全连接

JQL高级搜索
===================

用JQL筛选Jira问题
--------------------------

仅抓取符合特定条件的问题：

::

    # 仅特定项目
    issue.jql=project = "MYPROJECT"

    # 排除特定状态
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # 指定时间段
    issue.jql=updated >= -30d

    # 组合多个条件
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

有关JQL的详细信息，请参阅 `Atlassian JQL文档 <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_。

使用示例
======

Jira Cloud抓取
--------------------

参数：

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

脚本：

::

    url=issue.view_url
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\n\n评论：\n" + issue.comments
    last_modified=issue.last_modified

Confluence Server抓取
---------------------------

参数：

::

    home=https://wiki.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

脚本：

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n评论：\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

故障排除
======================

认证错误
----------

**症状**：``401 Unauthorized`` 或 ``403 Forbidden``

**检查项**：

1. 确认认证信息是否正确
2. Cloud版时，确认是否设置了适当的范围
3. Server版时，确认用户是否有适当权限
4. OAuth 2.0时，确认令牌的有效期

连接错误
----------

**症状**：``Connection refused`` 或连接超时

**检查项**：

1. 确认 ``home`` URL是否正确
2. 检查防火墙设置
3. 确认Atlassian实例是否正在运行
4. 确认 ``is_cloud`` 参数是否正确设置

无法获取数据
--------------------

**症状**：抓取成功但文档数为0

**检查项**：

1. 确认是否JQL过滤条件过于严格
2. 确认用户是否有读取权限的项目/空间
3. 确认脚本设置是否正确
4. 检查日志中是否有错误

OAuth 2.0令牌更新
-----------------------

**症状**：过一段时间后出现认证错误

**解决方法**：

OAuth 2.0访问令牌有有效期。通过设置刷新令牌可以自动更新：

::

    oauth2.refresh_token=your_refresh_token

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-database` - 数据库连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
- `Atlassian Developer <https://developer.atlassian.com/>`_
