==================================
Google Workspace连接器
==================================

概述
====

Google Workspace连接器提供从Google Drive（原G Suite）获取文件并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-gsuite`` 插件。

15.9的变更
==========

|Fess| 15.9对该连接器进行了大幅重构。升级现有的数据存储配置之前，请先阅读本节。

.. warning::

   ``crawl_target`` 的默认值变为 ``shared_drives``\ ，且除 ``legacy`` 以外的值都要求设置
   ``impersonate_user``\ 。因此，将现有配置原样升级后，爬取会在启动时抛出
   ``DataStoreException`` 而 **无法启动** 。

   这是有意为之的行为。原有行为只能访问到显式共享给服务账号的文件，若继续沿用，将出现一次
   什么都没有索引却悄然成功的爬取。请将 ``impersonate_user`` 设置为域管理员账号；如需保留
   原有行为，请设置 ``crawl_target=legacy``\ 。

行为变更
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 变更内容
     - 需要采取的措施
   * - ``crawl_target`` 的默认值变为 ``shared_drives``\ ，并要求设置 ``impersonate_user``
     - 设置 ``impersonate_user``\ ，或设置 ``crawl_target=legacy``\ 。否则爬取会在启动时失败。
   * - 默认OAuth范围从 ``https://www.googleapis.com/auth/drive`` 收窄为 ``https://www.googleapis.com/auth/drive.readonly``
     - Google Workspace管理控制台的域全域委派会明确列出各个范围，因此需要更新该配置。
   * - ``crawl_target=users`` 和 ``crawl_target=both`` 额外需要 ``https://www.googleapis.com/auth/admin.directory.user.readonly``
     - 需要同时在 ``scopes`` 参数和管理控制台的委派配置中添加该范围。这会在启动时进行校验。
   * - 索引的URL改为可在浏览器中打开的链接（``webViewLink``\ ），而不再是下载链接
     - 需要执行一次全量重新爬取才能采用新的URL。
   * - ``default_permissions`` 现在是回退值，而不是追加值
     - 能够解析出ACL的文档只会获得该ACL，不再与 ``default_permissions`` 取并集。结果严格更为严格。
   * - 仅通过链接共享不再授予搜索角色
     - ``allowFileDiscovery=false`` 的 ``domain`` 和 ``anyone`` 权限表示「知道链接的任何人」，Drive自身同样不会让这类文件可被搜索发现。
   * - ACL解析结果为空的文档会被跳过，而不再以无角色的方式索引
     - 如需继续索引，请设置 ``default_permissions``\ 。此前角色列表为空会导致权限过滤失效，这类文档对所有用户可见。
   * - ``fields`` 的默认值不再是 ``*``\ ，而是一份明确的字段列表
     - 引用了不常用字段的爬取脚本现在会读到null。设置 ``fields=*`` 可恢复原有行为。
   * - Google文档的导出格式由纯文本改为Markdown，电子表格由CSV改为TSV
     - 所有Google文档的索引文本中都会包含Markdown语法字符。需要执行全量重新爬取。
   * - ``refresh_token_interval`` 会被忽略
     - 令牌刷新由认证库负责。现有配置仍可正常工作，并会输出一条警告日志。
   * - Google表单和Google协作平台仅索引元数据
     - 因为Drive API中没有它们的导出格式。此前每一个这类文件都会产生爬取错误。

新功能
------

- ``crawl_target`` 用于选择爬取对象：服务账号自身的视角（``legacy``\ ）、域内的所有共享云端
  硬盘（``shared_drives``\ ）、目录中所有用户的「我的云端硬盘」（``users``\ ），或两者
  （``both``\ ）。请参阅 `爬取目标`_\ 。
- 共享云端硬盘中的项目现在会获得正确的ACL。请参阅 `权限和访问控制`_\ 。
- 支持基于Drive变更源的增量爬取。请参阅 `增量爬取`_\ 。
- 支持 ``Retry-After`` 的指数退避速率限制处理，且单个共享云端硬盘或用户的失败不再中断整个
  爬取。请参阅 `速率限制与重试`_\ 。
- 新增 ``proxy_username`` 和 ``proxy_password``\ ，用于需要认证的代理。

支持的服务
==========

- Google Drive（我的云端硬盘、共享云端硬盘）
- Google文档、电子表格、幻灯片、绘图、Apps Script
- Google表单、Google协作平台（没有导出格式，仅索引元数据）

前提条件
========

1. 需要安装插件
2. 需要创建Google Cloud Platform项目
3. 需要创建服务账号并获取认证信息
4. 需要设置Google Workspace域全域委派
5. 除非使用 ``crawl_target=legacy``\ ，否则需要一个用于模拟身份的Google Workspace管理员账号

插件安装
--------

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
--------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com

参数列表
~~~~~~~~

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
   * - ``impersonate_user``
     - 视情况
     - 通过域全域委派模拟的Google Workspace账号。除 ``crawl_target=legacy`` 外均为必需，未设置时爬取会在启动时失败。``shared_drives`` 和 ``both`` 以域管理员权限枚举共享云端硬盘，因此该账号必须是域管理员。
   * - ``crawl_target``
     - 否
     - 爬取对象：``legacy``\ 、``shared_drives``\ 、``users`` 或 ``both``\ 。默认值：``shared_drives``\ 。请参阅 `爬取目标`_\ 。
   * - ``scopes``
     - 否
     - OAuth范围（逗号分隔）。默认值：``https://www.googleapis.com/auth/drive.readonly``\ 。``crawl_target=users`` 和 ``both`` 额外需要 ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ 。
   * - ``user_query``
     - 否
     - 用于缩小 ``crawl_target=users`` 和 ``both`` 所枚举用户范围的Admin SDK ``query``\ 。默认值：未指定（客户账号下的所有用户）
   * - ``query``
     - 否
     - Google Drive API搜索查询字符串。不会应用于增量爬取所使用的变更源
   * - ``corpora``
     - 否
     - 搜索对象的语料库。默认值：``allDrives``\ 。仅在 ``crawl_target=legacy`` 时生效，因此在默认爬取对象下没有作用：``shared_drives`` 以 ``drive`` 枚举每个云端硬盘，``users`` 以 ``user`` 枚举每个「我的云端硬盘」，两者均为固定值
   * - ``spaces``
     - 否
     - 要搜索的空间（Google Drive API 的 ``spaces`` 参数，例如 ``drive``\ 、``appDataFolder``\ ）。默认值：未指定（API 默认值）。在 ``crawl_target=legacy`` 和 ``users`` 时使用，``shared_drives`` 时被忽略
   * - ``fields``
     - 否
     - 从 Google Drive API 请求的文件字段。默认值 **不是** ``*``\ ，而是一份明确的字段列表。它涵盖了脚本上下文、ACL解析、索引URL和增量爬取所需的全部字段；不在该列表中的字段在爬取脚本中为null。如需像旧版本那样请求全部字段，请设置 ``fields=*``
   * - ``default_permissions``
     - 否
     - 文档的Drive ACL解析结果为空时使用的权限（逗号分隔，例：``{role}drive-users``\ ）。这是回退值而非追加值：能够解析出ACL的文档只会获得该ACL
   * - ``max_size``
     - 否
     - 索引对象的最大文件大小（字节）。默认值：``10000000``\ （约 10MB）
   * - ``number_of_threads``
     - 否
     - 并行处理线程数。默认值：``1``
   * - ``incremental``
     - 否
     - 是否通过Drive变更源进行爬取，而不是列出全部内容。默认值：``false``\ 。该值在爬取开始前直接从数据存储配置的参数栏读取。请参阅 `增量爬取`_\ 。

高级参数
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数
     - 说明
   * - ``domain_permission_format``
     - 应用于 ``type=domain`` 的Drive权限的角色格式。``{domain}`` 会被替换为域名。默认值：``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - 爬取结束时等待工作线程结束的时间（秒）。默认值：``60``
   * - ``page_size``
     - ``files.list`` 和 ``changes.list`` 的分页大小。默认值：``1000``\ ；超过 ``1000`` 的值会被自动收窄
   * - ``permission_page_size``
     - ``permissions.list`` 和 ``drives.list`` 的分页大小。默认值：``100``\ ；超过 ``100`` 的值会被自动收窄
   * - ``max_cached_content_size``
     - 在内存中保留的内容的最大大小（字节）；超过此大小的内容将转存到临时文件。默认值：``1048576``\ （1MB）
   * - ``max_retries``
     - Drive API出现速率限制或临时性失败时的最大重试次数。默认值：``5``
   * - ``retry_initial_interval_ms``
     - 首次重试前的退避间隔（毫秒）。默认值：``1000``
   * - ``max_backoff_ms``
     - 单次等待时间的上限（毫秒）。默认值：``32000``
   * - ``read_timeout``
     - HTTP读取超时时间（毫秒）。默认值：``20000``
   * - ``connect_timeout``
     - HTTP连接超时时间（毫秒）。默认值：``20000``
   * - ``proxy_host``
     - 代理服务器的主机名。仅当 ``proxy_host`` 和 ``proxy_port`` 同时设置时才会使用代理，只设置其中一个不起作用
   * - ``proxy_port``
     - 代理服务器的端口号。请参阅 ``proxy_host``
   * - ``proxy_username``
     - 需要认证的代理的用户名。设置后，每个请求都会附加 ``Proxy-Authorization`` 头。关于它能认证什么、不能认证什么，请参阅 `限制事项`_
   * - ``proxy_password``
     - 需要认证的代理的密码
   * - ``ignore_folder``
     - 是否跳过文件夹。默认值：``true``
   * - ``ignore_error``
     - 发生错误时是否继续处理。默认值：``true``
   * - ``supported_mimetypes``
     - 索引对象的MIME类型（正则表达式，逗号分隔）。默认值：``.*``\ （所有类型）
   * - ``include_pattern``
     - 索引对象URL的正则表达式模式
   * - ``exclude_pattern``
     - 排除URL的正则表达式模式
   * - ``refresh_token_interval``
     - 自15.9起被忽略。访问令牌由认证库负责刷新。现有设置仍可正常工作，并会输出一条警告日志

.. note::

   ``private_key``\ 、``private_key_id``\ 、``client_email``\ 、``proxy_username`` 和
   ``proxy_password`` 会从脚本的求值上下文中移除，因此爬取脚本无法将其写入索引，搜索结果中
   也不会泄露这些值。

.. note::

   启用增量爬取后，连接器会将 ``start_page_tokens`` 和 ``crawl_signature`` 写回数据存储配置
   的参数栏。这些值由连接器管理，会与您设置的参数一同显示，但请不要修改。一旦修改或删除，
   下次执行时所有范围都会变成全量爬取。

爬取目标
--------

服务账号没有自己的Drive，也不属于任何Google群组，因此以服务账号自身身份认证的爬取，只能访问到
显式共享给服务账号地址的文件。``crawl_target`` 因此用于选择以谁的视角来爬取Drive。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 值
     - 说明
   * - ``legacy``
     - 与旧版本相同，以服务账号自身的视角进行爬取。不需要 ``impersonate_user``\ 。只能找到显式共享给服务账号的文件
   * - ``shared_drives``
     - 默认值。枚举域内的所有共享云端硬盘，并逐个遍历
   * - ``users``
     - 通过Admin SDK枚举目录中的所有用户，并逐个模拟其身份遍历「我的云端硬盘」
   * - ``both``
     - 先执行 ``shared_drives``\ ，再执行 ``users``\ 。出现在多个范围中的文件只会被索引一次

以下内容会在爬取启动时校验，组合不合法时不会执行，而是抛出 ``DataStoreException``\ ：

1. ``crawl_target`` 必须是 ``legacy``\ 、``shared_drives``\ 、``users`` 或 ``both`` 之一
2. 除 ``crawl_target=legacy`` 外，必须设置 ``impersonate_user``
3. 当 ``crawl_target`` 为 ``users`` 或 ``both`` 时，``scopes`` 必须包含
   ``https://www.googleapis.com/auth/admin.directory.user.readonly``

.. note::

   ``shared_drives`` 和 ``both`` 以域管理员权限枚举共享云端硬盘，因此 ``impersonate_user``
   指定的账号必须是Google Workspace的域管理员。该枚举决定了整个爬取的范围，因此永久性失败会
   中断爬取，而不是记录后跳过：一次未能枚举出任何云端硬盘的爬取并非部分成功，不应在什么都没有
   索引的情况下报告为成功。

增量爬取
--------

设置 ``incremental=true`` 后，每个范围（一个共享云端硬盘，或一位被模拟用户的视角）都会读取
Drive的变更源，而不是列出全部内容。没有保存令牌的范围会被完整爬取，并为下次执行记录变更源的
起始位置。

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   增量爬取执行时 ``delete_old_docs`` 会被强制设为 ``false``\ ，即使显式指定
   ``delete_old_docs=true`` 也会被覆盖而不是被采纳（并会输出警告日志）。删除旧文档的处理会
   删除本次爬取中未重新注册的、属于该数据配置的所有文档，其前提是全量爬取；而增量爬取只处理
   发生变更的文档，因此该删除处理会把索引中其余全部内容删掉。

   如需删除已从Drive中消失的文档，请另行调度一个 ``incremental=false`` 的数据存储配置。

只有在爬取完成且工作线程全部结束时，变更源的起始位置才会被保存。中途停止的爬取不会保存，
下次执行会重新读取相同的变更。

当决定某个范围返回内容的配置发生变化时——即 ``crawl_target``\ 、``impersonate_user``\ 、
``user_query``\ 、``query``\ 、``corpora``\ 、``spaces`` 中的任意一项——已保存的起始位置也会
被丢弃，所有范围都改为全量爬取。已保存的起始位置只描述取得它时的对象集合，配置变更后从该处
续读会在索引中留下永久性的缺失。

速率限制与重试
--------------

Drive API的速率限制或临时性失败会在 ``max_retries``\ 、``retry_initial_interval_ms``\ 、
``max_backoff_ms`` 的范围内以指数退避方式重试。``Retry-After`` 头优先于指数退避，但会受
``max_backoff_ms`` 的上限约束，以免错误的取值让爬取停滞数小时。``Retry-After`` 仅支持秒数
形式；HTTP日期形式会回退为指数退避。

``429``\ 、``500``\ 、``502``\ 、``503``\ 、``504`` 总是会重试。``403`` 仅在属于速率限制错误
时才会重试；其他 ``403`` 属于重试也无法解决的授权失败，会立即记录。

文件列表获取失败不再中断整个爬取：其余共享云端硬盘和用户仍会继续爬取，失败会记录到爬虫日志
以及管理界面的失败URL列表中。

脚本设置
--------

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
~~~~~~~~

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
     - 文件的URL。使用 ``webViewLink``\ ；若文件没有该值，则使用 ``https://drive.google.com/open?id=<文件ID>``
   * - ``file.thumbnail_link``
     - 缩略图链接（短期有效）
   * - ``file.size``
     - 文件大小（字节）
   * - ``file.roles``
     - 访问权限

.. note::

   只有 ``fields`` 参数中列出的字段才会被填充。未请求的字段在脚本中为null。如需像旧版本那样
   请求全部字段，请设置 ``fields=*``\ 。

详情请参阅 `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_\ 。

Google原生格式的文本提取
------------------------

Google原生格式的文件无法下载，必须导出。导出目标格式并非取自固定的对照表，而是从Drive API
实际返回的导出格式中选择，且单次导出上限为10MB。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 类型
     - 导出格式
   * - Google文档
     - Markdown（``text/markdown``\ ）。不可用时依次回退为纯文本、HTML
   * - Google电子表格
     - TSV（``text/tab-separated-values``\ ）。不可用时回退为CSV
   * - Google幻灯片
     - 纯文本
   * - Google绘图
     - PNG。没有可索引的文本，因此仅注册元数据
   * - Apps Script
     - 从导出的JSON中提取脚本源代码并索引
   * - Google表单、Google协作平台
     - 无法导出。仅注册元数据，且不会产生错误

.. note::

   由于Google文档现在以Markdown导出，所有Google文档的索引文本中都会包含Markdown语法字符。
   要让该变更作用于已索引的文档，需要执行一次全量重新爬取。

.. note::

   导出格式每次爬取会从Drive API获取一次。若该调用失败，连接器会回退到Drive一直以来支持的
   转换方式（Google文档为纯文本，Google电子表格为CSV），并输出一条警告日志。

Google Cloud Platform设置
=========================

1. 创建项目
-----------

访问 https://console.cloud.google.com/:

1. 创建新项目
2. 输入项目名称
3. 选择组织和位置

2. 启用Google Drive API
-----------------------

在「API和服务」→「库」中:

1. 搜索「Google Drive API」
2. 点击「启用」
3. 当 ``crawl_target`` 为 ``users`` 或 ``both`` 时，同时启用「Admin SDK API」

3. 创建服务账号
---------------

在「API和服务」→「凭据」中:

1. 选择「创建凭据」→「服务账号」
2. 输入服务账号名称（例: fess-crawler）
3. 点击「创建并继续」
4. 角色无需设置（跳过）
5. 点击「完成」

4. 创建服务账号密钥
-------------------

在创建的服务账号中:

1. 点击服务账号
2. 打开「密钥」选项卡
3. 「添加密钥」→「创建新密钥」
4. 选择JSON格式
5. 保存下载的JSON文件

5. 启用域全域委派
-----------------

在服务账号设置中:

1. 勾选「启用G Suite域全域委派」
2. 点击「保存」
3. 复制「OAuth 2客户端ID」

6. 在Google Workspace管理控制台授权
-----------------------------------

访问 https://admin.google.com/:

1. 打开「安全」→「访问和数据控制」→「API控制」
2. 选择「域全域委派」
3. 点击「新增」
4. 输入客户端ID
5. 输入OAuth范围:

   ::

       https://www.googleapis.com/auth/drive.readonly

   当 ``crawl_target`` 为 ``users`` 或 ``both`` 时，请输入两个范围:

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. 点击「授权」

.. warning::

   委派配置会明确列出各个范围，因此从旧版本升级时必须更新。15.9中默认范围已从
   ``https://www.googleapis.com/auth/drive`` 收窄为
   ``https://www.googleapis.com/auth/drive.readonly``\ ，此处授予的范围必须与数据存储配置的
   ``scopes`` 参数保持一致。

认证信息设置
============

从JSON文件获取信息
------------------

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
~~~~~~~~

``private_key`` 的换行保持为 ``\n``:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

使用示例
========

爬取所有共享云端硬盘
--------------------

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com

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
    role=file.roles
    filename=file.name

爬取所有用户的「我的云端硬盘」
------------------------------

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=users
    impersonate_user=admin@example.com
    scopes=https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

如需缩小用户范围，可添加Admin SDK查询:

::

    user_query=orgUnitPath=/Sales

保留原有行为
------------

``crawl_target=legacy`` 保留15.9之前的遍历方式，只能找到显式共享给服务账号的文件。
不需要 ``impersonate_user``\ 。

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=legacy

带权限爬取
----------

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

``default_permissions`` 仅用于Drive ACL解析结果为空的文档。

只爬取特定文件类型
------------------

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
========

爬取无法启动
------------

**症状**: 爬取立即以 ``DataStoreException`` 结束

**解决方法**:

1. ``parameter 'crawl_target' must be one of ...`` : ``crawl_target`` 的值不是 ``legacy``\ 、
   ``shared_drives``\ 、``users``\ 、``both`` 中的任何一个
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'`` :
   请将 ``impersonate_user`` 设置为域管理员账号，或设置 ``crawl_target=legacy``
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'`` :
   请将该范围添加到 ``scopes`` 以及域全域委派的配置中

将现有配置原样升级时，这是预期结果。请参阅 `15.9的变更`_\ 。

认证错误
--------

**症状**: ``401 Unauthorized`` 或 ``403 Forbidden``

**确认事项**:

1. 确认服务账号的认证信息是否正确:

   - ``private_key`` 的换行是否为 ``\n``
   - ``private_key_id`` 是否正确
   - ``client_email`` 是否正确

2. 确认Google Drive API是否已启用
3. 确认是否已设置域全域委派
4. 确认是否已在Google Workspace管理控制台授权
5. 确认OAuth范围是否正确（``https://www.googleapis.com/auth/drive.readonly``\ ；当
   ``crawl_target`` 为 ``users`` 或 ``both`` 时还需要
   ``https://www.googleapis.com/auth/admin.directory.user.readonly``\ ）

域全域委派错误
--------------

**症状**: ``Not Authorized to access this resource/api``

**解决方法**:

1. 在Google Workspace管理控制台确认授权:

   - 客户端ID是否正确注册
   - OAuth范围是否正确。委派配置会明确列出各个范围，因此需要配合15.9的范围变更进行更新

2. 确认服务账号是否启用了域全域委派
3. 当 ``crawl_target`` 为 ``shared_drives`` 或 ``both`` 时，确认 ``impersonate_user``
   指定的账号是否为域管理员

无法获取文件
------------

**症状**: 爬取成功但文件数为0

**确认事项**:

1. 确认 ``crawl_target`` 是否为预期的值。使用 ``legacy`` 时，由于服务账号没有自己的Drive
   且不属于任何群组，只能找到显式共享的文件
2. 确认Google Drive中是否存在文件
3. 确认服务账号是否有读取权限
4. 确认域全域委派是否正确设置
5. 确认是否可以访问目标用户的Drive

文档被跳过
----------

**症状**: 爬虫日志中输出 ``Skipped ... because no permission could be resolved``

**解决方法**:

该文档的Drive ACL未能解析出任何搜索角色，因此被跳过而未被索引。以无角色的方式索引会使该文档
的 |Fess| 权限过滤失效，从而对所有用户可见，因此选择跳过。跳过不属于爬取失败，只会输出到爬虫
日志，不会出现在失败URL列表中。

1. 如需以回退权限索引这类文档，请设置 ``default_permissions``
2. 为了能够读取共享云端硬盘的ACL，请确认 ``impersonate_user`` 指定的账号是域管理员
3. 确认该文档是否仅通过链接共享。``allowFileDiscovery=false`` 的 ``domain`` 和 ``anyone``
   权限不会授予搜索角色，因为Drive自身同样不会让这类文档可被搜索发现

API配额错误
-----------

**症状**: ``403 Rate Limit Exceeded`` 或 ``429 Too Many Requests``

**解决方法**:

1. 这类失败会以指数退避自动重试。若仍然失败，请调大 ``max_retries`` 或 ``max_backoff_ms``
2. 调小 ``number_of_threads`` 以降低请求频率
3. 在Google Cloud Platform确认配额
4. 增加爬取间隔
5. 如需要，请求增加配额

私钥格式错误
------------

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
----------------

.. note::
   使用 ``crawl_target=shared_drives``\ （默认值）时，会以域管理员权限枚举共享云端硬盘，
   因此不需要把服务账号逐一加入各个共享云端硬盘。取而代之的是，``impersonate_user`` 必须
   指定一个域管理员。

使用 ``crawl_target=legacy`` 时，需要将服务账号添加到每个共享云端硬盘:

1. 在Google Drive中打开共享云端硬盘
2. 点击「管理成员」
3. 添加服务账号的邮箱地址
4. 将权限级别设置为「查看者」

有大量文件的情况
----------------

**症状**: 爬取耗时长或超时

**解决方法**:

1. 启用 ``incremental=true``\ ，只爬取自上次执行以来的变更
2. 不使用 ``crawl_target=both``\ ，而是将共享云端硬盘和用户拆分到不同的数据存储配置中
3. 使用 ``query``\ 、``user_query``\ 、``supported_mimetypes`` 缩小范围
4. 通过计划设置分散负载
5. 调整爬取间隔

权限和访问控制
==============

Drive权限到Fess角色的转换
-------------------------

文档的ACL按以下三个阶段解析，使额外的API调用次数与共享云端硬盘的数量成正比，而不是与文件数量
成正比：

1. 文件列表中已包含的内联权限，不产生额外开销；
2. 对于Drive API不返回内联权限的共享云端硬盘项目，使用共享云端硬盘自身的ACL。它以域管理员
   权限按云端硬盘获取一次并被缓存；
3. 对于自身带有额外权限的项目，使用该项目自身的权限。

每条Drive权限按下表转换为 |Fess| 的搜索角色：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Drive权限
     - 搜索角色
   * - ``user``
     - 该用户邮箱地址对应的搜索角色。文件的所有者也始终以这种方式添加
   * - ``group``
     - 该群组邮箱地址对应的搜索角色。Google群组的成员不会被展开，需要由 |Fess| 一侧通过SSO或LDAP解析
   * - ``domain``
     - 将 ``domain_permission_format`` 中的 ``{domain}`` 替换为域名后的结果。默认值：``{group}{domain}``
   * - ``anyone``
     - ``guest`` 角色
   * - 上述权限中 ``allowFileDiscovery=false`` 的，以及已删除的权限
     - 无角色。因为仅通过链接共享在Drive自身也无法被搜索发现

当解析结果为空时，会改用 ``default_permissions``\ ——作为回退值，而非追加值。若
``default_permissions`` 也未设置，则该文档会被跳过。

反映Google Drive的共享权限
--------------------------

将Google Drive的共享设置反映到Fess的权限:

参数:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

限制事项
========

- Drive表示「已移除」的变更通知不仅包含删除，也包含访问权限的丧失。当 ``crawl_target=users``
  或 ``both`` 时，撤销某个用户的访问权限会使该文档从索引中删除，即使另一个用户仍然可以读取它。
  该文档会在下一次变更时，或下一次全量爬取时恢复。
- 增量爬取过程中某个范围回退为全量爬取时，删除旧文档的处理仍然处于关闭状态，因此在该范围
  未记录起始位置期间从Drive删除的文档会残留在索引中。要删除它们，需要另行准备一个
  ``incremental=false`` 的数据存储配置。
- 删除的传播以索引URL中包含Drive文件ID为前提。``webViewLink`` 和回退URL满足该条件，但如果
  爬取脚本将 ``url`` 改写为不包含文件ID的值，删除将无法传播。
- 变更源不会按 ``query`` 过滤。设置了 ``query`` 且 ``incremental=true`` 时，即使发生变更的
  文件不匹配该查询，也仍会被索引。
- 在大型域中使用 ``crawl_target=both`` 时，大约会产生
  ``2 + 共享云端硬盘数量 + 用户数量`` 次列表获取。将共享云端硬盘和用户拆分到不同的数据存储
  配置中是切实可行的缓解方式。
- ``proxy_username`` 和 ``proxy_password`` 以 ``Proxy-Authorization`` 请求头发送，因此只能
  认证明文HTTP请求。Google API的通信全部为HTTPS，而经由需要认证的代理建立HTTPS连接是通过
  ``CONNECT`` 完成的，该过程由JDK的 ``java.net.Authenticator`` 处理，而不是请求头。这类环境
  需要改用JVM选项 ``-Djdk.http.auth.tunneling.disabledSchemes=`` 并配置 ``Authenticator``\ 。

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-microsoft365` - Microsoft 365连接器
- :doc:`ds-box` - Box连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
