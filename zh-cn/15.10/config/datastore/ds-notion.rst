==================================
Notion连接器
==================================

概述
====

Notion连接器提供从Notion获取页面和数据库行并注册到
|Fess| 索引的功能。
它以Notion内部集成（internal integration）的身份进行认证，并为该集成已共享的所有内容建立索引。

此功能需要 ``fess-ds-notion`` 插件。

支持的内容
==========

- 页面（其块中的文本）
- 数据库行（包含属性值）
- Notion托管的文件块和PDF块的附件（各自作为独立文档建立索引）
- 页面中未解决的评论（并入页面的文档）

以下内容不在支持范围内:

- 仅在Notion中以链接形式存在的文件（外部文件）。只会下载Notion托管的 ``file`` 块和 ``pdf`` 块
- Notion回收站中的页面和数据库行
- 以页面为单位的访问控制（参见下文的“权限”）

前提条件
========

1. 需要安装插件
2. 需要创建Notion内部集成
3. 需要将要爬取的页面和数据库共享给该集成

插件安装
--------

从管理界面的「系统」→「插件」进行安装，或执行 ``bin/fess-setup install plugin fess-ds-notion`` 后
重启 |Fess|。
详情请参阅 :doc:`../../admin/plugin-guide`。

Notion集成设置
--------------

1. 在Notion中创建内部集成，并复制其“Internal Integration Secret”。
2. 在集成的设置页面（Configuration）中启用以下功能（capability）:

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - 功能
        - 是否必需
        - 用途
      * - Read content
        - 始终必需
        - 读取页面、块、数据库和数据库行。未启用时，所有请求都会以 ``401 unauthorized`` 失败，爬取会立即中止
      * - Read comments
        - 仅当 ``include_comments=true`` （默认）时
        - 获取页面评论。未启用时，会向日志输出一次警告，并在该次爬取的剩余过程中禁用评论爬取。爬取本身不会失败
      * - Read user information
        - 可选
        - 将用户ID（``created_by``、``last_edited_by``、``people`` 属性）解析为显示名称。未启用时，会对用户ID而不是名称建立索引

3. 在Notion中将所有要爬取的页面或数据库共享给该集成。
   仅添加功能并不会授予对任何内容的访问权限。

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
     - Company Notion
   * - 处理器名称
     - NotionDataStore
   * - 启用
     - 开

参数设置
--------

::

    token=secret_************************************

参数列表
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``token``
     - 是
     - 内部集成密钥（Internal Integration Secret）。不会传递给脚本，也不会输出到日志
   * - ``root_page_ids``
     - 否
     - 作为爬取起点的页面ID，以逗号分隔。当此参数与 ``database_ids`` 都为空时，通过Notion的搜索发现已共享给集成的所有页面和数据库
   * - ``database_ids``
     - 否
     - 作为爬取起点的数据库ID，以逗号分隔。会对每个数据库的所有行建立索引
   * - ``include_comments``
     - 否
     - 获取每个页面中未解决的评论，并将其文本包含到 ``notion.content`` 和 ``notion.comments`` 中（默认: ``true``）
   * - ``include_files``
     - 否
     - 下载Notion托管的 ``file`` 块和 ``pdf`` 块的附件并提取文本，各自作为独立文档建立索引（默认: ``true``）
   * - ``max_file_size``
     - 否
     - 超过此字节数的附件会被完全跳过，即使以空内容也不会建立索引（默认: ``10485760``）
   * - ``include_pattern``
     - 否
     - 文档的 ``notion.url`` 必须匹配的正则表达式（参见“爬取范围”）
   * - ``exclude_pattern``
     - 否
     - 文档的 ``notion.url`` 不得匹配的正则表达式（参见“爬取范围”）
   * - ``request_interval``
     - 否
     - 为避免超过Notion的速率限制（每秒约3次请求），在每次API请求之前等待的毫秒数（默认: ``350``）
   * - ``max_retry_count``
     - 否
     - 对返回 ``429``、``5xx``、``529`` 响应，或发生超时等通信错误的请求，最多重试的次数（默认: ``5``）
   * - ``connection_timeout``
     - 否
     - 每次API请求的连接超时（毫秒，默认: ``10000``）
   * - ``read_timeout``
     - 否
     - 每次API请求的读取超时（毫秒，默认: ``30000``）
   * - ``ignore_error``
     - 否
     - 已下载附件的文本提取失败时，不将文档视为失败，而是以空内容建立索引（默认: ``true``）。无论此设置如何，下载失败始终会使文档失败

.. note::

   对数字参数指定空值或非数字值时，会向日志输出警告并使用默认值。
   对 ``request_interval`` 和 ``max_retry_count`` 指定负值时（两者都允许 ``0``），
   以及对 ``true`` / ``false`` 参数指定其他值时，也是同样的处理。

脚本设置
--------

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time
    created=notion.created_time

可用字段
~~~~~~~~

页面、数据库行和附件等所有文档，都可以在脚本中通过 ``notion`` 对象引用。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``notion.type``
     - 页面或数据库行为 ``page``，附件为 ``file``
   * - ``notion.id``
     - 页面ID。附件为块ID
   * - ``notion.title``
     - 页面标题（无论名称如何，类型为 ``title`` 的属性）。附件为文件名
   * - ``notion.content``
     - 页面: 标题以外的属性值（仅数据库行）、块的文本和评论文本连接而成的内容。附件: 提取的文本
   * - ``notion.url``
     - 页面的Notion URL。附件为所属页面的URL末尾加上 ``#<块ID>``
   * - ``notion.mimetype``
     - 页面为 ``text/html``，附件为检测到的MIME类型
   * - ``notion.created_time``
     - 页面的创建时间。附件不可用
   * - ``notion.last_edited_time``
     - 页面（或附件块）的最后编辑时间
   * - ``notion.created_by``
     - 页面的创建者。Notion返回了名称时为名称，否则为用户ID。附件不可用
   * - ``notion.last_edited_by``
     - 最后编辑者（格式相同）。附件不可用
   * - ``notion.parent_id``
     - 父页面、数据库、数据源或块的ID。直接位于工作区下的页面为空。附件不可用
   * - ``notion.properties``
     - 数据库行的列名到格式化文本的映射。普通页面为空。附件不可用
   * - ``notion.comments``
     - 页面评论文本连接而成的内容。``include_comments=false`` 或没有评论时为空。附件不可用
   * - ``notion.page_url``
     - 所属页面的URL。仅附件可用
   * - ``notion.page_title``
     - 所属页面的标题。仅附件可用
   * - ``notion.size``
     - 附件的字节数（Notion返回时）。仅附件可用

爬取范围
========

- 未指定 ``root_page_ids`` 和 ``database_ids`` 时，通过Notion的搜索发现已共享给集成的所有页面和数据库。
  Notion不保证搜索结果完整无遗。如果索引中缺少某些内容，请显式指定 ``root_page_ids`` 或 ``database_ids``。
- 从每个起点可到达的子页面和子数据库也会全部爬取，因此通常指定一个根页面就能覆盖工作区的整个部分。
- ``include_pattern`` 和 ``exclude_pattern`` 只决定是否为该页面（或附件）自身的文档建立索引。
  它们不会阻止发现其下级内容。页面的块总是在用页面自身的URL判断模式之前先被遍历，
  因此被排除页面的子页面仍会被爬取，并以各自的URL建立索引。
  要排除整个子树，模式必须匹配其下的所有URL，而不仅仅是根。
- Notion回收站中的页面和数据库行会被跳过。

权限
====

Notion API不提供页面的共享设置，因此此连接器无法同步以页面为单位的访问控制。
所有文档仅使用数据存储配置的“权限”字段中设置的权限建立索引。

.. warning::

   无论在Notion中谁可以查看，共享给集成的所有内容都将可被此字段中允许的角色搜索到。
   请只将允许这些角色搜索的页面和数据库共享给集成。

错误处理
========

- 仅在HTTP ``401`` （令牌无法认证），或者返回表示 ``public_api_request_blocked`` 的 ``429`` 响应
  （Notion的速率限制屏蔽了该集成）时，爬取才会中止。
  未指定 ``root_page_ids`` 和 ``database_ids`` 时，如果Notion的搜索失败，由于没有起点，爬取也会中止。
- 其他失败按文档处理。对某个页面、数据库、评论线程或块的 ``404`` 或 ``403``，
  以及某个请求用尽 ``max_retry_count`` 的情况，会记录到日志并跳过，爬取继续进行。
- 按文档的失败会以该文档的URL（页面为Notion URL，附件为 ``<页面URL>#<块ID>``）
  记录到「爬虫」→「失败URL」中。
  附件的已签名下载URL既不会被记录，也不会输出到日志。
- 在参数中指定 ``keep_expires_docs=false`` 时，本次爬取中未重新建立索引的数据存储文档会在爬取结束时被删除。
  爬取中止时同样如此。
  默认情况下，文档带有有效期，在有效期过去之前会保留在索引中。

使用示例
========

爬取特定的页面树
----------------

参数:

::

    token=secret_************************************
    root_page_ids=0123456789abcdef0123456789abcdef
    include_comments=false

脚本:

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time

爬取数据库
----------

参数:

::

    token=secret_************************************
    database_ids=fedcba9876543210fedcba9876543210
    include_files=false

脚本:

::

    title=notion.title
    content=notion.content
    url=notion.url
    created=notion.created_time
    last_modified=notion.last_edited_time

爬取共享给集成的所有内容
------------------------

参数:

::

    token=secret_************************************
    request_interval=500

故障排除
========

爬取因 ``401`` 立即中止
-----------------------

请确认令牌是集成的“Internal Integration Secret”，并且已启用“Read content”功能。

索引中缺少页面
--------------

1. 确认页面或数据库已共享给集成
2. 如果依赖自动发现，请显式指定 ``root_page_ids`` 或 ``database_ids``，因为Notion的搜索不保证完整
3. 检查 ``include_pattern`` 和 ``exclude_pattern``
4. 在「爬虫」→「失败URL」中查看单独失败的文档

评论没有被建立索引
------------------

请启用集成的“Read comments”功能。未启用时，会向日志输出一次警告，并在该次爬取中跳过评论。
只有未解决的评论会被建立索引。

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-slack` - Slack连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../../admin/failureurl-guide` - 失败URL
- :doc:`../../admin/plugin-guide` - 插件管理指南
- `Notion API Documentation <https://developers.notion.com/>`_
