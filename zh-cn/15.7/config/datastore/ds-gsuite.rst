==================================
Google Workspace连接器
==================================

概述
====

Google Workspace连接器提供从Google Drive（原G Suite）获取文件并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-gsuite`` 插件。

支持的服务
============

- Google Drive（我的云端硬盘、共享云端硬盘）
- Google文档、电子表格、幻灯片、表单等

前提条件
========

1. 需要安装插件
2. 需要创建Google Cloud Platform项目
3. 需要创建服务账号并获取认证信息
4. 需要设置Google Workspace域全域委派

插件安装
------------------------

方法1: 直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # 放置
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或者
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 从管理界面安装

1. 打开「系统」→「插件」
2. 上传JAR文件
3. 重启 |Fess|

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
     - Company Google Drive
   * - 处理器名称
     - GoogleDriveDataStore
   * - 启用
     - 开

参数设置
----------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

参数列表
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``private_key``
     - 是
     - 服务账号的私钥（PEM格式，换行使用 ``\n``）
   * - ``private_key_id``
     - 是
     - 私钥ID
   * - ``client_email``
     - 是
     - 服务账号的邮箱地址
   * - ``max_size``
     - 否
     - 索引对象的最大文件大小（字节）。默认值：``10000000``\ （约 10MB）
   * - ``ignore_folder``
     - 否
     - 是否跳过文件夹。默认值：``true``
   * - ``ignore_error``
     - 否
     - 发生错误时是否继续处理。默认值：``true``
   * - ``supported_mimetypes``
     - 否
     - 索引对象的MIME类型（正则表达式，逗号分隔）。默认值：``.*``\ （所有类型）
   * - ``include_pattern``
     - 否
     - 索引对象URL的正则表达式模式
   * - ``exclude_pattern``
     - 否
     - 排除URL的正则表达式模式
   * - ``default_permissions``
     - 否
     - 默认权限（逗号分隔，例：``{role}drive-users``）
   * - ``number_of_threads``
     - 否
     - 并行处理线程数。默认值：``1``
   * - ``query``
     - 否
     - Google Drive API搜索查询字符串
   * - ``corpora``
     - 否
     - 搜索对象的语料库。默认值：``allDrives``
   * - ``spaces``
     - 否
     - 要搜索的空间（Google Drive API 的 ``spaces`` 参数，例如 ``drive``、``appDataFolder``）。默认值：未指定（API 默认值）。
   * - ``fields``
     - 否
     - 从 Google Drive API 请求的文件字段。默认值：``*``\ （所有字段）。
   * - ``read_timeout``
     - 否
     - HTTP读取超时时间（毫秒）。默认值：``20000``
   * - ``connect_timeout``
     - 否
     - HTTP连接超时时间（毫秒）。默认值：``20000``
   * - ``refresh_token_interval``
     - 否
     - 刷新 OAuth 访问令牌的间隔（秒）。默认值：``3540``\ （59 分钟）。
   * - ``max_cached_content_size``
     - 否
     - 在内存中保留的内容的最大大小（字节）；超过此大小的内容将转存到临时文件。默认值：``1048576``\ （1MB）。
   * - ``proxy_host``
     - 否
     - 代理服务器的主机名
   * - ``proxy_port``
     - 否
     - 代理服务器的端口号

脚本设置
--------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

可用字段
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``file.name``
     - 文件名
   * - ``file.description``
     - 文件描述
   * - ``file.contents``
     - 文件的文本内容
   * - ``file.mimetype``
     - 文件的MIME类型
   * - ``file.filetype``
     - 文件类型
   * - ``file.created_time``
     - 创建时间
   * - ``file.modified_time``
     - 最后更新时间
   * - ``file.web_view_link``
     - 在浏览器中打开的链接
   * - ``file.url``
     - 文件的URL
   * - ``file.thumbnail_link``
     - 缩略图链接（短期有效）
   * - ``file.size``
     - 文件大小（字节）
   * - ``file.roles``
     - 访问权限

详情请参阅 `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_\ 。

Google Cloud Platform设置
=========================

1. 创建项目
---------------------

访问 https://console.cloud.google.com/:

1. 创建新项目
2. 输入项目名称
3. 选择组织和位置

2. 启用Google Drive API
---------------------------

在「API和服务」→「库」中:

1. 搜索「Google Drive API」
2. 点击「启用」

3. 创建服务账号
---------------------------

在「API和服务」→「凭据」中:

1. 选择「创建凭据」→「服务账号」
2. 输入服务账号名称（例: fess-crawler）
3. 点击「创建并继续」
4. 角色无需设置（跳过）
5. 点击「完成」

4. 创建服务账号密钥
-------------------------------

在创建的服务账号中:

1. 点击服务账号
2. 打开「密钥」选项卡
3. 「添加密钥」→「创建新密钥」
4. 选择JSON格式
5. 保存下载的JSON文件

5. 启用域全域委派
-----------------------------

在服务账号设置中:

1. 勾选「启用G Suite域全域委派」
2. 点击「保存」
3. 复制「OAuth 2客户端ID」

6. 在Google Workspace管理控制台授权
---------------------------------------

访问 https://admin.google.com/:

1. 打开「安全」→「访问和数据控制」→「API控制」
2. 选择「域全域委派」
3. 点击「新增」
4. 输入客户端ID
5. 输入OAuth范围:

   ::

       https://www.googleapis.com/auth/drive

6. 点击「授权」

认证信息设置
==============

从JSON文件获取信息
--------------------------

下载的JSON文件:

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

将以下信息设置到参数:

- ``private_key_id`` → ``private_key_id``
- ``private_key`` → ``private_key`` （换行保持为 ``\n``）
- ``client_email`` → ``client_email``

私钥格式
~~~~~~~~~~~~

``private_key`` 的换行保持为 ``\n``:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

使用示例
======

Google Drive全体爬取
--------------------------

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com

脚本:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    filename=file.name

带权限爬取
----------------

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

脚本:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

只爬取特定文件类型
--------------------------------

只爬取Google文档:

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

故障排除
======================

认证错误
----------

**症状**: ``401 Unauthorized`` 或 ``403 Forbidden``

**确认事项**:

1. 确认服务账号的认证信息是否正确:

   - ``private_key`` 的换行是否为 ``\n``
   - ``private_key_id`` 是否正确
   - ``client_email`` 是否正确

2. 确认Google Drive API是否已启用
3. 确认是否已设置域全域委派
4. 确认是否已在Google Workspace管理控制台授权
5. 确认OAuth范围是否正确（``https://www.googleapis.com/auth/drive``）

域全域委派错误
------------------------

**症状**: ``Not Authorized to access this resource/api``

**解决方法**:

1. 在Google Workspace管理控制台确认授权:

   - 客户端ID是否正确注册
   - OAuth范围是否正确（``https://www.googleapis.com/auth/drive``）

2. 确认服务账号是否启用了域全域委派

无法获取文件
----------------------

**症状**: 爬取成功但文件数为0

**确认事项**:

1. 确认Google Drive中是否存在文件
2. 确认服务账号是否有读取权限
3. 确认域全域委派是否正确设置
4. 确认是否可以访问目标用户的Drive

API配额错误
-----------------

**症状**: ``403 Rate Limit Exceeded`` 或 ``429 Too Many Requests``

**解决方法**:

1. 在Google Cloud Platform确认配额
2. 增加爬取间隔
3. 如需要，请求增加配额

私钥格式错误
--------------------------

**症状**: ``Invalid private key format``

**解决方法**:

确认换行是否正确为 ``\n``:

::

    # 正确
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # 错误（包含实际换行）
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

共享云端硬盘爬取
----------------------

.. note::
   使用服务账号爬取共享云端硬盘时，
   需要将服务账号作为成员添加到共享云端硬盘。

1. 在Google Drive中打开共享云端硬盘
2. 点击「管理成员」
3. 添加服务账号的邮箱地址
4. 将权限级别设置为「查看者」

有大量文件的情况
------------------------

**症状**: 爬取耗时长或超时

**解决方法**:

1. 分割成多个数据存储
2. 通过计划设置分散负载
3. 调整爬取间隔
4. 只爬取特定文件夹

权限和访问控制
==================

反映Google Drive的共享权限
----------------------------

将Google Drive的共享设置反映到Fess的权限:

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

脚本:

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles`` 包含Google Drive的共享信息。

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-microsoft365` - Microsoft 365连接器
- :doc:`ds-box` - Box连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
