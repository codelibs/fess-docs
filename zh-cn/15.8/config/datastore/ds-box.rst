==================================
Box连接器
==================================

概述
====

Box连接器提供从Box.com云存储获取文件并
注册到 |Fess| 索引的功能。

本连接器使用JWT（服务器认证）方式对企业进行认证，通过模拟（impersonation）企业中各用户的身份，
递归爬取这些用户可访问的文件。可通过 ``filter_term`` 参数缩小爬取的用户范围。

此功能需要 ``fess-ds-box`` 插件。

前提条件
========

1. 需要安装插件
2. 需要Box开发者账户和应用程序创建
3. 需要设置JWT（JSON Web Token）认证

插件安装
------------------------

方法1：直接放置JAR文件

::

    # 从Maven Central下载
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # 放置
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # 或
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2：从管理界面安装

1. 打开"系统"→"插件"
2. 上传JAR文件
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
     - Company Box Storage
   * - 处理器名
     - BoxDataStore
   * - 启用
     - 开

参数设置
----------------

JWT认证示例：

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

参数列表
~~~~~~~~~~~~~~~~

认证参数（必填）
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必填
     - 说明
   * - ``client_id``
     - 是
     - Box应用的客户端ID
   * - ``client_secret``
     - 是
     - Box应用的客户端密钥
   * - ``public_key_id``
     - 是
     - 公钥ID
   * - ``private_key``
     - 是
     - 私钥（PEM格式，换行用 ``\n`` 表示）
   * - ``passphrase``
     - 是
     - 私钥的密码短语
   * - ``enterprise_id``
     - 是
     - Box企业ID

爬取参数（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 参数
     - 默认值
     - 说明
   * - ``max_size``
     - ``10000000``
     - 爬取对象的最大文件大小（字节）。默认为10MB。
   * - ``supported_mimetypes``
     - ``.*``
     - 爬取对象的MIME类型（正则表达式）。可用逗号分隔指定多个。
   * - ``include_pattern``
     - （无）
     - 纳入爬取对象的URL模式
   * - ``exclude_pattern``
     - （无）
     - 从爬取对象中排除的URL模式
   * - ``number_of_threads``
     - ``1``
     - 爬取处理的线程数
   * - ``ignore_folder``
     - ``true``
     - 是否将文件夹排除在索引之外。当前实现中，文件夹本身不会被索引（仅以文件为对象），因此本参数无效。
   * - ``ignore_error``
     - ``true``
     - 发生错误时是否继续处理
   * - ``filter_term``
     - （无）
     - 用于缩小爬取范围的企业用户筛选条件。未指定时，以企业内所有用户为对象。
   * - ``fields``
     - （全部字段）
     - 指定从Box API获取的字段

连接参数（可选）
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 参数
     - 默认值
     - 说明
   * - ``base_url``
     - ``https://app.box.com``
     - 用于构建在浏览器中打开文件的URL（``file.url``）的基础URL。不影响Box SDK所使用的API端点。
   * - ``max_retry_count``
     - ``10``
     - API调用的最大重试次数
   * - ``proxy_host``
     - （无）
     - HTTP代理的主机名
   * - ``proxy_port``
     - （无）
     - HTTP代理的端口号
   * - ``refresh_token_interval``
     - ``3540``
     - 令牌的更新间隔（秒）。默认为59分钟。

脚本设置
--------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

可用字段
~~~~~~~~~~~~~~~~~~~~

主要字段
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``file.url``
     - 在浏览器中打开文件的链接
   * - ``file.contents``
     - 文件的文本内容
   * - ``file.mimetype``
     - 文件的MIME类型
   * - ``file.filetype``
     - 文件类型
   * - ``file.name``
     - 文件名
   * - ``file.size``
     - 文件大小（字节）
   * - ``file.created_at``
     - 创建日期时间
   * - ``file.modified_at``
     - 最后更新日期时间
   * - ``file.download_url``
     - Box直接下载URL
   * - ``file.id``
     - Box项目ID
   * - ``file.description``
     - 文件描述
   * - ``file.extension``
     - 文件扩展名
   * - ``file.sha1``
     - 文件的SHA1哈希值
   * - ``file.path_collection``
     - 文件夹路径列表

元数据字段
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``file.type``
     - 项目类型（"file"或"folder"）
   * - ``file.file_version``
     - 文件版本信息
   * - ``file.sequence_id``
     - 序列ID
   * - ``file.etag``
     - ETag哈希值
   * - ``file.trashed_at``
     - 移至回收站的日期时间
   * - ``file.purged_at``
     - 永久删除的日期时间
   * - ``file.content_created_at``
     - 内容创建日期时间
   * - ``file.content_modified_at``
     - 内容更新日期时间
   * - ``file.created_by``
     - 创建者信息
   * - ``file.modified_by``
     - 更新者信息
   * - ``file.owned_by``
     - 所有者信息
   * - ``file.shared_link``
     - 共享链接信息
   * - ``file.parent``
     - 父文件夹信息
   * - ``file.item_status``
     - 项目状态
   * - ``file.version_number``
     - 版本号
   * - ``file.comment_count``
     - 评论数
   * - ``file.permissions``
     - 权限信息
   * - ``file.tags``
     - 标签信息
   * - ``file.lock``
     - 锁定信息
   * - ``file.is_package``
     - 包标志
   * - ``file.is_watermark``
     - 水印标志
   * - ``file.collections``
     - 收藏夹信息
   * - ``file.representations``
     - 表现形式信息
   * - ``file.api``
     - Box文件API对象（用于获取协作及权限信息）

详细信息请参阅 `Box File Object <https://developer.box.com/reference#file-object>`_。

Box认证设置
=============

JWT认证设置步骤
-----------------

1. 在Box Developer Console创建应用程序
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

访问 https://app.box.com/developers/console：

1. 点击"Create New App"
2. 选择"Custom App"
3. 在认证方法中选择"Server Authentication (with JWT)"
4. 输入应用名称并创建

2. 应用程序设置
~~~~~~~~~~~~~~~~~~~~~~~~~

在"Configuration"标签页设置：

**Application Scopes**：

- 勾选"Read all files and folders stored in Box"

**Advanced Features**：

- 点击"Generate a Public/Private Keypair"
- 下载生成的JSON文件（重要！）

**App Access Level**：

- 选择"App + Enterprise Access"

3. 在企业中批准
~~~~~~~~~~~~~~~~~~~~~~~~~

在Box管理控制台：

1. 打开"Apps"→"Custom Apps"
2. 批准创建的应用

4. 获取认证信息
~~~~~~~~~~~~~~~~~

从下载的JSON文件获取以下信息：

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

私钥格式
~~~~~~~~~~~~

``private_key`` 将换行替换为 ``\n`` 成为一行：

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

使用示例
========

爬取企业整个Box存储
---------------------------------

参数：

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

脚本：

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

仅爬取特定文件夹
----------------------------

可通过 ``include_pattern`` 参数按文件夹路径进行筛选。

参数：

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    include_pattern=.*Documents/Projects/.*

脚本：

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

仅爬取PDF文件
-------------------------

可通过 ``supported_mimetypes`` 参数按MIME类型进行筛选。

参数：

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    supported_mimetypes=application/pdf

脚本：

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

故障排除
======================

认证错误
----------

**症状**：``Authentication failed`` 或 ``Invalid grant``

**检查项**：

1. 确认 ``client_id`` 和 ``client_secret`` 是否正确
2. 确认私钥是否正确复制（换行是否变成 ``\n``）
3. 确认密码短语是否正确
4. 确认应用在Box管理控制台中是否已被批准
5. 确认 ``enterprise_id`` 是否正确

私钥格式错误
--------------------------

**症状**：``Invalid private key format``

**解决方法**：

确认私钥的换行是否正确转换为 ``\n``：

::

    # 正确格式
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # 错误格式（包含实际换行）
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

无法获取文件
----------------------

**症状**：爬取成功但文件数为0

**检查项**：

1. 确认Application Scopes中"Read all files and folders"是否启用
2. 确认App Access Level是否为"App + Enterprise Access"
3. 确认Box存储中是否确实存在文件
4. 确认服务账户是否有适当权限

文件数量庞大时
------------------------

**症状**：爬取耗时过长或超时

**解决方法**：

在数据存储设置中分割处理：

1. 调整爬取间隔
2. 拆分为多个数据存储进行设置（按文件夹单位等）
3. 通过 ``number_of_threads`` 参数增加线程数
4. 通过计划设置分散负载

权限与访问控制
==================

映射Box协作权限
-------------------------------

通过 ``file.api`` 字段提供的 ``BoxFileAPI`` 对象，可将Box的协作信息映射到 |Fess| 的搜索角色。
``file.api.collaborationRoles`` 返回与可访问该文件的用户及组对应的搜索角色列表。

在脚本中设置权限：

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.api.collaborationRoles
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

.. note::
   ``file.api.collaborationRoles`` 会对每个文件获取协作信息，因此会增加Box API的调用次数，
   可能导致爬取速度下降。

若要对所有文件分配固定角色，请按如下方式指定：

::

    role="{role}box-users"

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-dropbox` - Dropbox连接器
- :doc:`ds-gsuite` - Google Workspace连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
