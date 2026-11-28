=============================================
搜索 Google Drive、SharePoint 和 Box 中的文件
=============================================

前言
====

各部门分别使用 Google Drive、SharePoint Online 和 Box 时，花在回想“那份资料放在哪里了”上的时间就会越来越多。
使用 Fess 的数据存储插件，可以在一个搜索页面中查找这 3 个服务中的文件。

不过，云存储中混杂着访问权限各不相同的文件。
如果配置出错，合同等机密文件甚至会出现在未登录用户的搜索结果中。
本文针对每个服务，介绍“照抄即可运行的最小配置”，以及如何把原有的权限带入 Fess。

安装插件、处理程序名称·参数·脚本的写法、创建作业等数据存储通用的步骤，汇总在 :doc:`datastore-basics` 中。
请先阅读该文再继续。
文中的设置值以 Fess 15.9 和各插件的 15.9.0 版为准。

本文搭建的配置
==============

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - 服务
     - 插件
     - 处理程序名称
     - 需要在服务端准备的内容
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - 服务账号的 JSON 密钥，以及全网域委派
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - Entra ID 中的应用注册（客户端密码），以及 Microsoft Graph 的应用程序权限
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - 使用 JWT 认证的 Box 自定义应用

如果在 Docker 中运行 Fess，在环境变量 ``FESS_PLUGINS`` 中以空格分隔列出插件名和版本，即可在启动时一并安装。

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

如果通过管理界面或 ``fess-setup`` 安装，安装后需要重启 Fess（\ ``FESS_PLUGINS`` 在 Fess 启动前进行安装，因此不需要重启）。

先决定：把搜索结果展示给谁
==========================

新建数据存储配置时，「权限」栏中一开始就填有 ``{role}guest``。
如果保留这个值，导入的文件也会被未登录的用户搜索到。
3 个插件都会把根据原有共享设置生成的角色放入 ``file.roles``。
因此，3 个插件在以下 2 点上的设置方法是相同的。

- 删除「权限」栏中的 ``{role}guest``，使其为空
- 在脚本中写入 ``role=file.roles``

之所以需要这 2 点，是因为各插件对「权限」栏的处理方式不同。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 插件
     - 「权限」栏的值
     - ``default_permissions`` 参数
   * - Google Drive
     - 写了 ``role=file.roles`` 就不会使用。不写的话，栏中的值（初始值为 ``{role}guest``\ ）会原样附加到所有文件上
     - 仅用于从 Drive 的 ACL 中什么也没获取到的文件。如果它也未设置，该文件不会被导入
   * - SharePoint（OneDriveDataStore）
     - 合并到 ``file.roles`` 中。保留 ``{role}guest`` 会使所有文件公开
     - 添加到所有文件
   * - Box
     - 合并到 ``file.roles`` 中。保留 ``{role}guest`` 会使所有文件公开
     - 添加到所有文件

``file.roles`` 中放入的是表示各服务用户和组的字符串。

- Google Drive：用户和组是电子邮件地址，文件所有者也是同样的格式。网域共享为 ``{group}<域名>``\ （可通过 ``domain_permission_format`` 更改），可通过搜索找到的公开共享（\ ``anyone``\ ）为 ``guest`` 角色。仅共享给知道链接的人的设置不会成为角色。
- SharePoint：用户是对象 ID 和 UPN，组是 ID 和显示名称。面向“组织内所有人”的共享链接会成为组 ``EVERYONE_IN_TENANT``。
- Box：用户是 Box 用户 ID 和登录名（电子邮件地址），组是 Box 组 ID。除了文件本身的协作之外，还包括上级文件夹的协作和所有者。

搜索时与这些值进行比对的，是登录 Fess 的用户的用户名和组名。
例如，要让 Google Drive 的用户权限生效，Fess 的用户名必须与电子邮件地址一致。
关于角色的概念请参阅 :doc:`guide-05`，关于通过 SSO 登录请参阅 :doc:`guide-15`。

用于按服务筛选搜索结果的标签，在数据存储配置中没有专用的栏。
可以在脚本中添加 ``label="box"`` 这样的行，或者创建与 URL 匹配的标签（详见 :doc:`datastore-basics`\ ）。
标签的值只能使用英文字母、数字和 ``_``，无法创建 ``google-drive`` 这样包含连字符的值。

Google Drive：导入共享云端硬盘
==============================

Google 端的准备
---------------

15.9 的 ``fess-ds-gsuite`` 默认以 ``crawl_target=shared_drives`` 运行。
这种方式通过模拟网域管理员，读取网域内所有的共享云端硬盘。

1. 在 Google Cloud 控制台中创建项目，并启用 Google Drive API
2. 创建服务账号，在 [Keys] 标签页中创建 JSON 格式的密钥并下载
3. 为服务账号启用全网域委派，并记下 OAuth 2 客户端 ID
4. 在 Google Workspace 管理控制台的 [Security] > [Access and data control] > [API controls] > [Domain-wide delegation] 中，为该客户端 ID 授权范围 ``https://www.googleapis.com/auth/drive.readonly``

``impersonate_user`` 中指定的账号必须是 Google Workspace 的网域管理员。
如果 ``crawl_target`` 不是 ``legacy`` 且没有 ``impersonate_user``，爬取在开始时就会因错误而停止。

参数和脚本
----------

在 [爬虫] > [数据存储] > [新建] 中，「处理程序名称」选择 ``GoogleDriveDataStore``，并清空「权限」栏。
在 ``private_key``、\ ``private_key_id``、\ ``client_email`` 中填入 JSON 密钥中同名的值。
``private_key`` 中的换行保持 ``\n`` 的形式，写成一行。

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url`` 是文件的 ``webViewLink``。
删除的反映以已索引的 URL 中包含 Drive 文件 ID 为前提。
因此，请不要改写 ``url``，直接这样使用。

其他导入范围如下。

- ``crawl_target=users``\ ：读取所有用户的“我的云端硬盘”。需要启用 Admin SDK API，并添加范围 ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ （委派设置和 ``scopes`` 参数两处都要添加）。
- ``crawl_target=legacy``\ ：只读取直接共享给服务账号地址的文件。不需要委派和 ``impersonate_user``。

增量爬取
--------

添加 ``incremental=true`` 后，从第 2 次起只读取 Drive 的变更提要。
此时 ``delete_old_docs`` 会被强制设为 ``false``，从 Drive 中删除的文件可能会残留在索引中。
另外，未变更的文件不会被重新登记，因此如果不做处理，经过「删除以前的文档」的天数（初始值 3 天）后，它们就会从搜索结果中消失（参见 :doc:`datastore-basics` 中关于文档有效期的一节）。

使用增量爬取时，请按以下方式组合。

- 另外创建一个不带 ``incremental`` 的全量爬取配置，每周 1 次等定期执行
- 在两个配置中都指定比全量爬取间隔稍长的 ``time_to_live``\ （每周 1 次全量爬取时为 ``time_to_live=11520``，即 8 天）

从 Drive 中删除的文件，会在该期限到期时从搜索结果中消失。
变更提要的位置由插件写回到「参数」栏中，请不要编辑写回的值。

SharePoint Online：导入文档库中的文件
=====================================

使用哪个处理程序
----------------

要搜索 SharePoint 文档库中文件的正文，请使用 ``fess-ds-microsoft365`` 的 ``OneDriveDataStore``。

- ``SharePointDocLibDataStore`` 只是把一个文档库登记为 1 条，不会导入其中的文件。
- ``fess-ds-sharepoint``\ （\ ``SharePointDataStore``\ ）面向本地部署的 SharePoint Server。它不支持 Microsoft Graph，并且文档中说明 SharePoint Online 应使用 ``fess-ds-microsoft365``。

Entra ID 端的准备
-----------------

1. 在 Azure Portal 的 [App registrations] 中新建注册
2. 在 [Certificates & secrets] 中新建客户端密码，并记下其值（有效期在这里决定）
3. 在 [API permissions] > [Microsoft Graph] > [Application permissions] 中添加下面 4 项
4. 执行 [Grant admin consent]

需要添加的应用程序权限如下。

- ``Files.Read.All``
- ``User.Read.All``、\ ``Group.Read.All``\ ：为查询 ACL 中的用户名和组名，任何导入范围都需要
- ``Sites.Read.All``\ ：以 ``shared_documents_drive_crawler=true`` 枚举站点时需要

参数和脚本
----------

``OneDriveDataStore`` 在不做任何指定时，除 SharePoint 的所有站点外，还会读取所有用户的 OneDrive 和所有 Microsoft 365 组的驱动器。
如果只以 SharePoint 为对象，请明确指定 3 个标志。

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

如果只想限定于特定的文档库，请把 3 个标志全部设为 ``false``，并在 ``drive_id`` 中指定驱动器 ID。
驱动器 ID 可以通过 Microsoft Graph 的 ``GET /sites/{site-id}/drives`` 确认。
如果只指定 ``drive_id`` 而保留标志，该驱动器只是被“追加”到整体导入中。

权限遗漏与重试
--------------

文件的 ACL 是对每个文件分别调用 Graph 获取的。
该调用失败时的处理由 ``permission_failure_policy`` 决定。
默认的 ``skip`` 不会登记该文件，而是记录到 [系统信息] > [失败URL] 和 WARN 日志中。
如果改为 ``index_without_acl``，文件会在 ACL 不完整的状态下被登记，因此对于机密性高的文档库，保持默认值比较安全。

Graph 调用的重试可以通过 ``max_retry_count``\ （默认 3，上限 10）和 ``retry_interval``\ （秒，默认 3，上限 180）调整。
``OneDriveDataStore`` 没有增量爬取选项，每次都读取全部内容。

Box：带权限导入合同文件夹
=========================

Box 端的准备
------------

``fess-ds-box`` 只支持使用 JWT 的服务器认证。

1. 在 Box Developer Console 中创建「Custom App」，认证方式选择「Server Authentication (with JWT)」
2. 在 [Configuration] 标签页的 Application Scopes 中启用「Read all files and folders stored in Box」
3. App Access Level 选择「App + Enterprise Access」
4. 通过 [Generate a Public/Private Keypair] 生成密钥对，并保存 JSON 文件
5. 在 Box 管理控制台中批准该应用

JSON 文件中的 ``clientID``、\ ``clientSecret``、\ ``publicKeyID``、\ ``privateKey``、\ ``passphrase``、\ ``enterpriseID`` 分别对应 ``client_id``、\ ``client_secret``、\ ``public_key_id``、\ ``private_key``、\ ``passphrase``、\ ``enterprise_id``。
6 项全部为必填。

把目标文件夹限定为一个
----------------------

像法务部的合同这样对象已经确定的情况，用 ``root_folder_id`` 只读取一个文件夹。
在这种模式下不会模拟用户，而是以应用的服务账号身份读取文件夹。
因此，需要事先把服务账号添加为目标文件夹的协作者。
文件夹 ID 是在 Box 网页界面中打开该文件夹时 URL 末尾的数字。

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

请务必删除「权限」栏中的 ``{role}guest``。
在 Box 中，栏中的值会合并到 ``file.roles`` 中，如果保留，合同也会被未登录的用户搜索到。

Box 的组以组 ID 的形式成为角色，因此与 Fess 端的组名并不能直接对应。
本例通过 ``default_permissions={group}legal``，让 Fess 的 ``legal`` 组可以看到所有文件。
在 Box 中被单独共享的用户，只要其登录名（电子邮件地址）与 Fess 的用户名一致，也可以额外搜索到这些文件。
如果想为带有面向全公司的共享链接的文件添加角色，请使用 ``company_shared_link_role``。

读取所有用户的文件
------------------

省略 ``root_folder_id`` 时，会枚举企业中的所有用户，并逐个模拟他们来读取文件。
目标用户可以用 ``filter_term`` 筛选。
通过模拟进行的 API 调用需要在 Box 端的应用设置中被允许，请在 Box 的开发者文档中确认相关设置。

应对速率限制
------------

``429`` 和 ``5xx`` 响应的重试次数为 ``max_retry_attempts``\ （默认 5）。
``max_retry_count``\ （默认 10）是收到 ``401`` 响应时重新建立连接的次数，与速率限制无关。
如果想降低 API 调用频率，可以用 ``readInterval``\ （毫秒）为每一条设置等待时间。
``fess-ds-box`` 没有增量爬取选项。

运维中需要注意的事项
====================

认证信息的有效期
----------------

- Entra ID 的客户端密码有创建时设定的有效期。过期后会出现认证错误而无法导入，因此请在到期前创建新的密码，并替换参数中的 ``client_secret``。
- Google 的访问令牌由插件使用的库自动更新。在 15.9 中，\ ``refresh_token_interval`` 会被忽略，并在日志中输出警告。
- Box 的访问令牌每隔 ``refresh_token_interval``\ （默认 3540 秒）自动更新。

无法全部导入时
--------------

3 个插件在爬取结束时，默认都会等待工作线程结束 60 秒，未完成的部分不会被导入。
在大型租户中文档数量不足时，请延长等待时间。
参数名在 Google Drive 中为 ``thread_pool_timeout_seconds``，在 SharePoint 中为 ``executor_shutdown_timeout``，在 Box 中为 ``thread_pool_await_timeout``\ （单位均为秒）。

在 Google Drive 中，429、500、502、503、504 响应以及由速率限制导致的 403，会以指数退避方式重试。
重试可以通过 ``max_retries``\ （默认 5）、\ ``retry_initial_interval_ms``\ （默认 1000）、\ ``max_backoff_ms``\ （默认 32000）调整。

确认运行结果
============

作业结果和日志的查看方法在 :doc:`datastore-basics` 中有说明。
数据存储爬取即使获取文件失败，作业也可能显示为「OK」，因此请根据文档数量和日志来判断。
对于本文的配置，还要确认以下 3 点。

1. 在注销状态下搜索导入文件中包含的词语，确认 1 条结果也没有（检查是否忘记清空「权限」栏）
2. 用被共享的用户登录后，确认能搜到同一文件
3. 对于 Google Drive 的配置，确认 ``fess-crawler.log`` 中没有出现 ``Skipped ... because no permission could be resolved``\ （这是因 ACL 为空而未被导入的文件）

如果第 2 步中搜不到，请检查用户的用户名和组名是否与 ``file.roles`` 中的值一致。

总结
====

- SharePoint 的文件正文用 ``OneDriveDataStore`` 导入，不需要的话把 OneDrive 和组驱动器设为 ``false``。
- 3 个服务都要删除「权限」栏中的 ``{role}guest``，并在脚本中写入 ``role=file.roles``。
- ``default_permissions`` 在 Google Drive 中用于替代空的 ACL，在 SharePoint 和 Box 中则添加到所有文件。
- 只有 Google Drive 支持增量爬取（\ ``incremental=true``\ ）。使用时请与全量爬取配置组合，并在两者中都指定 ``time_to_live``。

参考资料
========

- `Google Workspace 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-gsuite.html>`__
- `Microsoft 365 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-microsoft365.html>`__
- `Box 连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-box.html>`__
- `数据存储配置 <https://fess.codelibs.org/zh-cn/stable/admin/dataconfig-guide.html>`__
- `fess-ds-microsoft365 15.9.0 README（Graph 权限一览） <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `fess-ds-box 15.9.0 README（file.roles 和 root_folder_id） <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
