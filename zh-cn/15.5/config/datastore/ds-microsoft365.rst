==================================
Microsoft 365连接器
==================================

概述
====

Microsoft 365连接器提供从Microsoft 365服务（OneDrive、OneNote、Teams、SharePoint）获取数据并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-microsoft365`` 插件。

支持的服务
============

- **OneDrive**: 用户云端硬盘、组云端硬盘、共享文档
- **OneNote**: 笔记本（站点、用户、组）
- **Teams**: 频道、消息、聊天
- **SharePoint Document Libraries**: 文档库元数据
- **SharePoint Lists**: 列表和列表项
- **SharePoint Pages**: 站点页面、新闻文章

前提条件
========

1. 需要安装插件
2. 需要Azure AD应用程序注册
3. 需要Microsoft Graph API权限设置和管理员同意
4. Java 21以上、Fess 15.2.0以上

插件安装
------------------------

方法1: 直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # 放置
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或者
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 从源代码构建

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

安装后，请重启 |Fess|。

配置方法
========

从管理界面的「爬虫」→「数据存储」→「新建」进行配置。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 名称
     - Microsoft 365 OneDrive
   * - 处理器名称
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - 启用
     - 开

参数设置（通用）
------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

通用参数列表
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``tenant``
     - 是
     - Azure AD租户ID
   * - ``client_id``
     - 是
     - 应用注册的客户端ID
   * - ``client_secret``
     - 是
     - 应用注册的客户端密钥
   * - ``number_of_threads``
     - 否
     - 并行处理线程数（默认: 1）
   * - ``ignore_error``
     - 否
     - 出错时继续处理（默认: false）
   * - ``include_pattern``
     - 否
     - 包含内容的正则表达式模式
   * - ``exclude_pattern``
     - 否
     - 排除内容的正则表达式模式
   * - ``default_permissions``
     - 否
     - 默认角色分配

Azure AD应用程序注册
============================

1. 在Azure Portal注册应用程序
---------------------------------------

在 https://portal.azure.com 打开Azure Active Directory:

1. 点击「应用注册」→「新注册」
2. 输入应用程序名称
3. 选择支持的账户类型
4. 点击「注册」

2. 创建客户端密钥
---------------------------------

在「证书和密钥」中:

1. 点击「新建客户端密钥」
2. 设置描述和有效期
3. 复制密钥值（之后无法再查看，请注意）

3. 添加API权限
----------------

在「API权限」中:

1. 点击「添加权限」
2. 选择「Microsoft Graph」
3. 选择「应用程序权限」
4. 添加所需权限（参见下文）
5. 点击「授予管理员同意」

各数据存储所需权限
==========================

OneDriveDataStore
-----------------

必需权限:

- ``Files.Read.All``

条件权限:

- ``User.Read.All`` - user_drive_crawler=true 时
- ``Group.Read.All`` - group_drive_crawler=true 时
- ``Sites.Read.All`` - shared_documents_drive_crawler=true 时

OneNoteDataStore
----------------

必需权限:

- ``Notes.Read.All``

条件权限:

- ``User.Read.All`` - user_note_crawler=true 时
- ``Group.Read.All`` - group_note_crawler=true 时
- ``Sites.Read.All`` - site_note_crawler=true 时

TeamsDataStore
--------------

必需权限:

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

条件权限:

- ``Chat.Read.All`` - 指定chat_id时
- ``Files.Read.All`` - append_attachment=true 时

SharePointDocLibDataStore
-------------------------

必需权限:

- ``Files.Read.All``
- ``Sites.Read.All``

或 ``Sites.Selected``（指定site_id时，需要为每个站点设置）

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

必需权限:

- ``Sites.Read.All``

或 ``Sites.Selected``（指定site_id时，需要为每个站点设置）

脚本设置
==============

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

可用字段:

- ``file.name`` - 文件名
- ``file.description`` - 文件描述
- ``file.contents`` - 文本内容
- ``file.mimetype`` - MIME类型
- ``file.filetype`` - 文件类型
- ``file.created`` - 创建时间
- ``file.last_modified`` - 最后更新时间
- ``file.size`` - 文件大小
- ``file.web_url`` - 在浏览器中打开的URL
- ``file.roles`` - 访问权限

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

可用字段:

- ``notebook.name`` - 笔记本名称
- ``notebook.contents`` - 节和页面的整合内容
- ``notebook.size`` - 内容大小（字符数）
- ``notebook.created`` - 创建时间
- ``notebook.last_modified`` - 最后更新时间
- ``notebook.web_url`` - 在浏览器中打开的URL
- ``notebook.roles`` - 访问权限

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

可用字段:

- ``message.title`` - 消息标题
- ``message.content`` - 消息内容
- ``message.created_date_time`` - 创建时间
- ``message.last_modified_date_time`` - 最后更新时间
- ``message.web_url`` - 在浏览器中打开的URL
- ``message.roles`` - 访问权限
- ``message.from`` - 发送者信息

SharePoint Document Libraries
------------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

可用字段:

- ``doclib.name`` - 文档库名称
- ``doclib.description`` - 库描述
- ``doclib.content`` - 搜索用整合内容
- ``doclib.created`` - 创建时间
- ``doclib.modified`` - 最后更新时间
- ``doclib.url`` - SharePoint URL
- ``doclib.site_name`` - 站点名称

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

可用字段:

- ``item.title`` - 列表项标题
- ``item.content`` - 文本内容
- ``item.created`` - 创建时间
- ``item.modified`` - 最后更新时间
- ``item.url`` - SharePoint URL
- ``item.fields`` - 所有字段的映射
- ``item.roles`` - 访问权限

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

可用字段:

- ``page.title`` - 页面标题
- ``page.content`` - 页面内容
- ``page.created`` - 创建时间
- ``page.modified`` - 最后更新时间
- ``page.url`` - SharePoint URL
- ``page.type`` - 页面类型（news/article/page）
- ``page.roles`` - 访问权限

各数据存储的附加参数
================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
-----------------------------

::

    site_id=
    exclude_site_id=
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    ignore_system_pages=true
    page_type_filter=

使用示例
======

OneDrive全云端硬盘爬取
----------------------------

参数:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

脚本:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

爬取特定团队的Teams消息
------------------------------------

参数:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+08:00

脚本:

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

爬取SharePoint列表
--------------------------

参数:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

脚本:

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

故障排除
======================

认证错误
----------

**症状**: ``Authentication failed`` 或 ``Insufficient privileges``

**确认事项**:

1. 确认租户ID、客户端ID、客户端密钥是否正确
2. 确认在Azure Portal中是否授予了所需的API权限
3. 确认是否授予了管理员同意
4. 确认客户端密钥的有效期

API速率限制错误
-------------------

**症状**: ``429 Too Many Requests``

**解决方法**:

1. 减少 ``number_of_threads``（设置为1或2）
2. 增加爬取间隔
3. 设置 ``ignore_error=true`` 继续处理

无法获取数据
--------------------

**症状**: 爬取成功但文档数为0

**确认事项**:

1. 确认目标数据是否存在
2. 确认API权限是否正确设置
3. 确认用户/组云端硬盘爬虫设置
4. 在日志中确认错误信息

确认SharePoint站点ID的方法
----------------------------

使用PowerShell确认:

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

或者，使用Microsoft Graph API:

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

大量数据爬取
--------------------

**解决方法**:

1. 分割成多个数据存储（按站点、云端硬盘等）
2. 通过计划设置分散负载
3. 调整 ``number_of_threads`` 进行并行处理
4. 只爬取特定文件夹/站点

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-gsuite` - Google Workspace连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
