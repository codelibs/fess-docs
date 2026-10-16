==================================
Backlog连接器
==================================

概述
====

Backlog连接器提供从Backlog空间获取问题、Wiki页面、文档和文件并注册到
|Fess| 索引的功能。
它使用API密钥对空间进行认证。
每个已建立索引的文档都被限制为只有其所属Backlog项目的成员才能搜索（参见下文的“权限”）。

此功能需要 ``fess-ds-backlog`` 插件。

支持的内容
==========

- 问题（包含评论）
- Wiki页面
- 文档
- 问题、Wiki页面和文档的附件
- 项目的共享文件

每次爬取都是完整爬取。默认情况下，已从Backlog中消失的文档不会在爬取结束时删除，
而是在有效期过期时删除（参见“已删除的内容与已撤销的访问权限”）。

前提条件
========

1. 需要安装插件
2. 需要爬取专用的Backlog用户及其API密钥
3. 该用户必须是所有要爬取的项目的成员

插件安装
--------

从管理界面的「系统」→「插件」进行安装，或执行 ``bin/fess-setup install plugin fess-ds-backlog`` 后
重启 |Fess|。
详情请参阅 :doc:`../../admin/plugin-guide`。

Backlog端设置
-------------

1. 创建爬取专用的Backlog用户，并为其发放API密钥（「个人设置」→「API」）。
   爬取所看到的内容与该用户看到的完全相同。
2. 将该用户添加到所有要爬取的项目中。连接器不会获取用户未加入的项目，
   即使该用户是空间管理员也是如此。
3. 为该用户授予没有限制的角色（管理员或普通用户）。使用有限制的角色时，
   Backlog会对某些功能返回HTTP 403。“仅查看”用户无法下载问题的附件，而只有没有限制的用户才能下载共享文件。
   遇到这样的403时，连接器会针对每个项目和功能向日志输出一条警告，跳过该项目的该功能
   （问题附件、Wiki附件、文档附件或共享文件），并继续爬取其余内容。
4. 如果空间要求API访问使用两步验证，Backlog会返回错误代码12
   （RequiredMFAError），爬取会中止。

API密钥只通过 ``Backlog-API-Key`` 请求头发送。它不会传递给脚本，
此连接器也不会将其输出到日志。不会跟随HTTP重定向，因此密钥不会离开空间的主机。

.. warning::

   请不要启用 ``org.codelibs.curl`` 日志记录器的 ``FINE`` 日志。HTTP客户端会在该级别输出请求头，
   而它只会屏蔽 ``Authorization`` 和 ``Cookie`` 之类的请求头，因此 ``Backlog-API-Key`` 请求头会被写入日志。

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
     - Company Backlog
   * - 处理器名称
     - BacklogDataStore
   * - 权限
     - （留空。参见“权限”）
   * - 启用
     - 开

参数设置
--------

::

    api_key=**********************************************
    space_url=https://example.backlog.com

参数列表
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``api_key``
     - 是
     - Backlog的API密钥。不会传递给脚本，也不会输出到日志
   * - ``space_url``
     - 是
     - 空间的URL（例如 ``https://example.backlog.com``）。只接受 ``https``，且只能指定协议和主机（末尾的斜杠会被忽略）。未指定、格式错误或为 ``http`` 时，爬取会中止
   * - ``project_keys``
     - 否
     - 要爬取的项目键，以逗号分隔（不区分大小写）。为空时爬取该用户可见的所有项目。用户不可见的键会作为警告输出到日志
   * - ``include_archived``
     - 否
     - 同时爬取已归档的项目（默认: ``false``）
   * - ``include_issues``
     - 否
     - 为问题建立索引（默认: ``true``）
   * - ``include_comments``
     - 否
     - 将问题的评论并入问题的文档（默认: ``true``）
   * - ``include_wikis``
     - 否
     - 在启用了Wiki的项目中为Wiki页面建立索引（默认: ``true``）
   * - ``include_documents``
     - 否
     - 在启用了文档的项目中为文档建立索引（默认: ``true``）
   * - ``include_attachments``
     - 否
     - 下载问题、Wiki页面和文档的附件并建立索引（默认: ``true``）
   * - ``include_shared_files``
     - 否
     - 在启用了文件共享的项目中下载共享文件并建立索引（默认: ``true``）
   * - ``permission_sync``
     - 否
     - 为项目的每个文档按项目成员各授予一个 ``{user}`` 角色（默认: ``true``）。参见“权限”
   * - ``default_permissions``
     - 否
     - 添加到所有文档的权限，以逗号分隔（``{user}name``、``{group}name``、``{role}name``）
   * - ``max_file_size``
     - 否
     - 超过此字节数的文件会被跳过，不建立索引（默认: ``10485760``）
   * - ``include_pattern``
     - 否
     - ``backlog.url`` 必须匹配的正则表达式
   * - ``exclude_pattern``
     - 否
     - ``backlog.url`` 不得匹配的正则表达式。问题、Wiki页面或文档被排除时，其附件也会被跳过
   * - ``request_interval``
     - 否
     - 每次API请求之前等待的毫秒数（默认: ``200``）
   * - ``search_request_interval``
     - 否
     - 两次搜索类请求（问题列表、Wiki列表）之间的最小间隔（毫秒）。Backlog要求客户端至少间隔1秒（默认: ``1000``）
   * - ``max_retry_count``
     - 否
     - 对HTTP 429、5xx和连接失败的重试次数（默认: ``5``）
   * - ``connection_timeout``
     - 否
     - 连接超时（毫秒，默认: ``10000``）
   * - ``read_timeout``
     - 否
     - 读取超时（毫秒，默认: ``30000``）
   * - ``ignore_error``
     - 否
     - 已下载文件的文本提取失败时，不记录为失败，而是以空内容建立索引（默认: ``true``）

.. note::

   无效的值（非数字、负的间隔或重试次数、不大于0的超时或 ``max_file_size``、``true`` / ``false`` 以外的布尔值）
   会向日志输出警告并使用默认值。
   ``request_interval``、``search_request_interval`` 和 ``max_retry_count`` 允许 ``0``。

脚本设置
--------

::

    title=backlog.title
    content=backlog.content
    url=backlog.url
    mimetype=backlog.mimetype
    created=backlog.created
    last_modified=backlog.updated
    role=backlog.roles

.. important::

   要使对项目成员的限制生效，必须指定 ``role=backlog.roles``。
   未指定时，反映到索引中的只有数据存储配置的“权限”字段的值。

可用字段
~~~~~~~~

所有文档都可以在脚本中通过 ``backlog`` 对象引用。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 字段
     - 类型
     - 说明
   * - ``backlog.type``
     - 全部
     - ``issue``、``wiki``、``document``、``attachment``、``file`` 之一
   * - ``backlog.id``
     - 全部
     - 问题、Wiki页面、文档、附件或共享文件在Backlog中的ID
   * - ``backlog.project_key``、``backlog.project_name``
     - 全部
     - 项目
   * - ``backlog.title``
     - 全部
     - 问题为 ``[KEY-1] 摘要``。其他为页面名称、文档标题或文件名
   * - ``backlog.content``
     - 全部
     - 问题: 描述、属性、自定义字段和评论。Wiki页面: 页面内容。文档: 纯文本。附件和文件: 提取的文本
   * - ``backlog.url``
     - 全部
     - 参见“URL”
   * - ``backlog.mimetype``
     - 全部
     - 问题、Wiki页面和文档为 ``text/plain``。文件为检测到的类型
   * - ``backlog.created``、``backlog.updated``
     - 全部
     - ISO 8601格式的UTC时间（Backlog返回时）
   * - ``backlog.created_by``、``backlog.updated_by``
     - 全部
     - 用户名（Backlog返回时）
   * - ``backlog.roles``
     - 全部
     - 搜索角色（参见“权限”）
   * - ``backlog.issue_key``、``backlog.issue_type``、``backlog.status``、``backlog.priority``、``backlog.assignee``
     - 问题
     - 问题的属性（名称）
   * - ``backlog.categories``、``backlog.milestones``、``backlog.versions``
     - 问题
     - 名称列表
   * - ``backlog.custom_fields``
     - 问题
     - 自定义字段名到值文本的映射
   * - ``backlog.comments``
     - 问题
     - ``作者: 内容`` 形式的评论文本（以空行分隔）
   * - ``backlog.tags``
     - Wiki页面、文档
     - 标签名称列表
   * - ``backlog.parent_type``、``backlog.parent_url``、``backlog.parent_title``
     - 附件
     - 附件所属的问题、Wiki页面或文档
   * - ``backlog.size``
     - 附件、文件
     - 下载的字节数
   * - ``backlog.path``
     - 文件
     - 共享文件的路径（例如 ``/docs/spec.pdf``）

URL
---

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 类型
     - URL
   * - 问题
     - ``{space_url}/view/{ISSUE-KEY}``
   * - Wiki页面
     - ``{space_url}/alias/wiki/{ID}``
   * - 文档
     - ``{space_url}/document/{PROJECT}/{ID}``
   * - 文件
     - ``{space_url}/file/{PROJECT}{目录}{名称}`` （路径的每一段都会进行百分号编码）
   * - 附件
     - ``{父级的URL}#attachment-{ID}``

.. note::

   文档和共享文件的URL形式，以及文档附件的下载端点，
   尚未在真实的Backlog空间中确认。即使链接没有打开预期的页面，
   文档仍会被建立索引并可以搜索，错误的只是链接目标。

权限
====

当 ``permission_sync=true`` （默认）时，项目的所有文档都会被授予以下角色:

- 项目每位成员的 ``mailAddress`` 对应的 ``{user}`` 角色，以及 ``userId`` 对应的 ``{user}`` 角色（空值除外）。
  成员可以使用其中任意一个登录 |Fess|
- ``default_permissions`` 的值
- 数据存储配置的“权限”字段的值

如果无法获取项目成员，或者没有任何成员拥有可用的 ``mailAddress`` 或 ``userId``，
则会跳过整个项目，并记录到「爬虫」→「失败URL」中。绝不会在没有成员角色的情况下为其建立索引。

当 ``permission_sync=false`` 时，只应用 ``default_permissions`` 和“权限”字段。

.. warning::

   请清空数据存储配置的“权限”字段。管理界面会在该字段中预先填入 ``{role}guest``，
   而包括匿名搜索用户在内的所有用户都拥有此角色。如果保留，它会被合并到每个文档的角色中，
   使Backlog的所有内容对所有人可搜索。
   当 ``permission_sync=true`` 时，对于角色中带有访客角色的每个项目，连接器会向日志输出一条警告。

在依赖成员角色之前，请注意以下几点:

- 成员的标识符被视为 |Fess| 的登录名。Backlog的 ``userId`` 为 ``tanaka`` 时，会向 |Fess| 登录名为 ``tanaka`` 的人授予访问权限，
  但这不一定是同一个人（例如LDAP或Active Directory的帐户名）。``mailAddress`` 角色没有这个问题。
  仅在 |Fess| 的登录名与Backlog的用户ID或邮件地址一致的环境中使用 ``permission_sync``。
- 标识符会对应到访客角色或其他登录名的成员会被忽略，并输出指明项目和成员ID的警告:
  ``userId`` 为 ``guest`` 的情况，以及包含反斜杠的标识符（|Fess| 会去掉用户名中反斜杠及其之前的部分）。
- 项目的所有成员都能搜索到项目中已建立索引的所有项目，包括附件和共享文件，
  即使Backlog本身不允许该成员下载（“仅查看”用户无法下载问题附件）也是如此。
  角色以项目为单位，而不是以功能为单位。

已删除的内容与已撤销的访问权限
==============================

默认情况下，|Fess| 会为每个文档设置有效期（常规设置中的“删除以前的文档”，默认3天），
并且在爬取结束时不会删除带有有效期的文档。已过期的文档由文档清除器（Doc Purger）删除。因此默认情况下:

- 在Backlog中删除的内容最多约3天内仍可搜索
- 成员离开项目后，该成员最多约3天内仍可访问项目中已建立索引的文档。
  下一次爬取会以新的文档ID重新为它们建立索引（ID中包含角色列表），而带有旧角色的旧副本会保留到有效期过期。
  在此期间，其余成员会看到重复的搜索结果

若要在爬取结束时就删除这类文档，请在数据存储配置的参数中添加 ``keep_expires_docs=false``。
|Fess| 会删除该配置下本次爬取未重新建立索引的所有文档，这也适用于爬取未能到达的所有内容（参见“错误处理”）。

使用示例
========

爬取特定项目
------------

参数:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    project_keys=PROJ,DOCS
    include_shared_files=false

仅问题和Wiki页面（不含附件）
----------------------------

参数:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    include_documents=false
    include_attachments=false
    include_shared_files=false

在爬取结束时删除Backlog中已删除的文档
-------------------------------------

参数:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    keep_expires_docs=false

错误处理
========

- 仅在HTTP ``401``、Backlog错误代码11（AuthenticationError）或12（RequiredMFAError）、
  ``api_key`` 或 ``space_url`` 缺失或格式错误，或获取项目列表失败时，爬取才会中止。
- 对于HTTP ``429``，会等待到 ``X-RateLimit-Reset`` 请求头指示的时间后重试（最多120秒；没有该请求头时为60秒）。
  对于HTTP ``5xx`` 和连接失败，会以指数退避（1秒、2秒、4秒，最多60秒）重试。
  用尽 ``max_retry_count`` 次重试后，该项目失败。
- 其他失败（``403``、``404``、重试用尽）只会针对该单个项目记录，爬取继续进行。
- 某个项目失败不会导致爬取作业失败。爬取后请检查「爬虫」→「失败URL」和爬虫日志。
- 指定 ``keep_expires_docs=false`` 时，失败部分的内容不会被重新建立索引，因此会在该次爬取结束时被删除:
  获取失败的列表、被跳过的项目以及因403被跳过的功能之下的所有内容，在之后不带该失败完成爬取之前，都会从索引中消失。
  爬取中止时同样如此。默认情况下，这类内容在有效期过期之前仍可搜索。

故障排除
========

爬取在开始时中止
----------------

1. 确认 ``api_key`` 正确，并且是为此空间的用户发放的
2. 确认 ``space_url`` 是只包含主机的 ``https`` URL（例如 ``https://example.backlog.com``）
3. 如果空间要求API访问使用两步验证，爬取会因RequiredMFAError而中止

项目没有被建立索引
------------------

1. 确认API用户是该项目的成员
2. 当 ``permission_sync=true`` 时，无法获取成员的项目，或没有任何成员拥有可用的邮件地址或用户ID的项目会被跳过。请查看「爬虫」→「失败URL」
3. 检查 ``project_keys`` 和 ``include_archived``

缺少附件或共享文件
------------------

请为API用户授予没有限制的角色。日志中，对于因HTTP 403被跳过的每个项目和功能，都有一条警告。

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-atlassian` - Atlassian连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../../admin/failureurl-guide` - 失败URL
- :doc:`../../admin/plugin-guide` - 插件管理指南
- `Backlog API Documentation <https://developer.nulab.com/docs/backlog/>`_
