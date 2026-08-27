==================================
Slack连接器
==================================

概述
====

Slack连接器提供从Slack工作区获取频道消息并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-slack`` 插件。

支持的内容
==========

- 公共频道消息
- 私有频道消息
- 线程回复消息（通过 ``conversations.replies``\ 获取）
- 文件附件（可选）

以下内容不在支持范围内:

- 系统事件消息（``channel_join``、``channel_topic``、``pinned_item``\ 等）默认会从索引中
  排除（``ignore_system_events``）
- 私信（DM）及群组私信
- Huddle的转录内容和Clips（Slack未提供公开API，因此无法爬取）

前提条件
========

1. 需要安装插件
2. 需要创建Slack App并设置权限
3. 需要获取OAuth Access Token

插件安装
--------

从管理界面的「系统」→「插件」进行安装:

1. 从Maven Central下载 ``fess-ds-slack-X.X.X.jar``
2. 从插件管理界面上传并安装
3. 重启 |Fess|

或者，详情请参阅 :doc:`../../admin/plugin-guide`。

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
     - Company Slack
   * - 处理器名称
     - SlackDataStore
   * - 启用
     - 开

参数设置
--------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

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
     - Slack App的OAuth Access Token
   * - ``channels``
     - 否
     - 爬取目标频道（逗号分隔，或 ``*all``）。未指定时获取所有频道（与 ``*all`` 相同的行为）
   * - ``file_crawl``
     - 否
     - 是否也爬取文件（默认: ``false``）
   * - ``include_private``
     - 否
     - 是否包含私有频道（默认: ``false``）
   * - ``number_of_threads``
     - 否
     - 并行处理线程数（默认: ``1``）
   * - ``max_filesize``
     - 否
     - 爬取文件的最大大小（字节，默认: ``10000000``）
   * - ``ignore_error``
     - 否
     - 发生错误时继续处理（默认: ``true``）
   * - ``supported_mimetypes``
     - 否
     - 允许的MIME类型（正则表达式，默认: ``.*``）
   * - ``include_pattern``
     - 否
     - 包含URL的正则表达式模式
   * - ``exclude_pattern``
     - 否
     - 排除URL的正则表达式模式
   * - ``proxy_host``
     - 否
     - HTTP代理主机
   * - ``proxy_port``
     - 否
     - HTTP代理端口（指定 ``proxy_host`` 时必需）
   * - ``file_types``
     - 否
     - 爬取对象的文件类型（Slack API的文件类型筛选器，默认: ``all``）
   * - ``channel_count``
     - 否
     - 每页获取的频道数（默认: ``100``）
   * - ``message_count``
     - 否
     - 每页获取的消息数（默认: ``100``）
   * - ``file_count``
     - 否
     - 每页获取的文件数（默认: ``20``）
   * - ``user_count``
     - 否
     - 每页获取的用户数（默认: ``100``）
   * - ``user_cache_size``
     - 否
     - 用户信息缓存的最大条目数（默认: ``10000``）
   * - ``bot_cache_size``
     - 否
     - 机器人信息缓存的最大条目数（默认: ``10000``）
   * - ``channel_cache_size``
     - 否
     - 频道信息缓存的最大条目数（默认: ``10000``）

高级参数
~~~~~~~~

以下参数用于控制连接与重试行为、精细的爬取范围，以及权限同步:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数
     - 说明
   * - ``connection_timeout``
     - 每次Slack API请求的连接超时时间（毫秒，默认: ``20000``）
   * - ``read_timeout``
     - 每次Slack API请求的读取超时时间（毫秒，默认: ``20000``）
   * - ``max_retry_count``
     - 收到 ``429``\ （速率限制）或 ``5xx`` 响应时的最大重试次数（默认: ``3``）
   * - ``retry_interval``
     - 当响应中没有 ``Retry-After`` 头时，首次重试前的等待时间（毫秒，默认: ``3000``）。每次
       重试后翻倍，上限为 ``60000``\ 毫秒。若响应包含 ``Retry-After`` 头，则优先使用该值
       （单位: 秒）
   * - ``executor_timeout``
     - 爬取结束时，等待队列中剩余任务完成的秒数（默认: ``60``）。超过此时间将强制终止
   * - ``exclude_archived``
     - 是否从 ``conversations.list`` 的结果中排除已归档的频道（默认: ``false``）。设为
       ``true``\ 时，在 ``channels`` 中按频道名指定的已归档频道将无法解析（详情参见故障排除）
   * - ``ignore_system_events``
     - 是否将Slack自动生成的频道管理类消息（``channel_join``、``channel_topic``、
       ``pinned_item``\ 等）从索引中排除（默认: ``true``）
   * - ``read_interval``
     - 每处理一条消息或文件后的等待时间（毫秒，默认: ``0``\ ，即不等待）。可用于在速率限制
       严格的工作区中降低爬取速度
   * - ``max_content_length``
     - 内容提取（Tika）从单个文件中可提取的最大字符数（默认: 未设置，此时遵循 |Fess|
       按MIME类型划分的默认上限）。``max_filesize`` 是下载前按文件大小拦截的传输量上限，
       ``max_content_length`` 是下载后提取文本量的上限，两者各自独立生效。调小
       ``max_filesize`` 并不能替代 ``max_content_length``\ （例如，1MB的压缩文件解压后可能
       产生远大于此的文本量）
   * - ``permission_sync``
     - 是否将私有频道的成员关系转换为搜索用权限（角色）（默认: ``false``）。详情参见后文
       「权限同步（ACL）」
   * - ``default_permissions``
     - 无论频道成员关系如何，都授予所有已索引文档的附加权限（``{user}``/``{group}``/
       ``{role}``\ 格式，逗号分隔，默认: 空）。仅在启用 ``permission_sync`` 时生效

.. note::

   ``ignore_system_events`` 的默认值为 ``true``\ 。即使是未设置此参数的现有爬取配置，在升级
   |Fess| 后，也会不再索引 ``channel_join`` 等系统事件消息——索引的文档数量会在没有任何错误
   或警告的情况下减少。若希望像以前一样继续索引系统事件，请显式指定
   ``ignore_system_events=false``\ 。

脚本设置
--------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

可用字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``message.title``
     - 标题（消息时为空字符串，文件时为文件名和标题）
   * - ``message.text``
     - 消息的文本内容（文件条目时为文件名及提取的文件正文）
   * - ``message.user``
     - 消息发送者的显示名称（未设置时，按真实姓名、用户名、用户ID的顺序解析）
   * - ``message.channel``
     - 消息发送的频道名
   * - ``message.timestamp``
     - 消息发送时间
   * - ``message.permalink``
     - 消息的永久链接
   * - ``message.attachments``
     - 附件文件的回退信息
   * - ``message.roles``
     - 可查看此消息或文件的搜索权限（角色）列表。仅在 ``permission_sync=true`` 时存在此字段。
       除非脚本中指定了 ``role=message.roles``\ ，否则计算出的权限不会反映到已索引的文档中

Slack App设置
=============

1. 创建Slack App
----------------

访问 https://api.slack.com/apps:

1. 点击「Create New App」
2. 选择「From scratch」
3. 输入应用名称（例: Fess Crawler）
4. 选择工作区
5. 点击「Create App」

2. OAuth & Permissions设置
--------------------------

在「OAuth & Permissions」菜单中:

**在Bot Token Scopes中添加以下权限**:

基础权限（始终需要）:

- ``channels:history`` - 读取公共频道消息
- ``channels:read`` - 读取公共频道信息
- ``users:read`` - 读取用户信息（显示名称解析所需）
- ``team:read`` - 读取工作区信息。每次爬取都会调用 ``team.info``\ ，因此该权限是必需的；
  若缺少此权限，本连接器会针对每条消息回退到额外调用一次 ``chat.getPermalink``\ ，从而大幅
  增加API调用次数

包含私有频道时（``include_private=true``）额外添加:

- ``groups:history`` - 读取私有频道消息
- ``groups:read`` - 读取私有频道信息

也爬取文件时（``file_crawl=true``）额外添加:

- ``files:read`` - 读取文件内容

同步私有频道权限时（``permission_sync=true``）额外添加:

- ``users:read.email`` - 读取成员的邮箱地址（权限同步所必需）

3. 安装应用
-----------

在「Install App」菜单中:

1. 点击「Install to Workspace」
2. 确认权限并点击「允许」
3. 复制「Bot User OAuth Token」（以 ``xoxb-`` 开头）

.. note::
   通常使用以 ``xoxb-`` 开头的Bot User OAuth Token，
   但参数中也可以使用以 ``xoxp-`` 开头的User OAuth Token。

4. 添加到频道
-------------

将App添加到爬取目标频道:

1. 在Slack中打开频道
2. 点击频道名
3. 选择「集成」选项卡
4. 点击「添加应用」
5. 添加创建的应用

权限同步（ACL）
===============

Slack连接器可以将私有频道的成员关系转换为 |Fess| 的搜索权限（角色），使得只有该频道的成员
才能搜索其内容。默认情况下此功能处于禁用状态。

.. note::

   ``permission_sync`` 仅计算权限（角色），并不会自动应用它们。只有在脚本中添加
   ``role=message.roles`` 后，计算出的权限才会反映到已索引的文档中。若忘记添加此映射，
   ``permission_sync=true`` 所带来的API调用增加和私有频道跳过依然会发生，却完全不会产生
   任何访问控制效果。

启用方法
--------

1. 为Slack App添加 ``users:read.email`` 权限（解析成员邮箱地址所必需）
2. 在参数中设置 ``permission_sync=true``
3. 在脚本中添加 ``role=message.roles``

参数:

::

    include_private=true
    permission_sync=true

脚本:

::

    role=message.roles

失败关闭（Fail-Closed）行为
---------------------------

符合以下任一条件的私有频道，在该次爬取中将完全不会被索引（这是一种「失败关闭」行为：宁可
索引不足，也绝不会将内容意外公开给所有人）:

- 获取该频道成员列表失败
- 成员列表返回为空（当用于爬取的令牌所属的机器人用户本身未加入该私有频道时会发生此情况）
- 频道有成员，但无法解析其中任何一位的邮箱地址（通常是因为缺少 ``users:read.email`` 权限）

公共频道从不调用 ``conversations.members``\ ，始终被视为所有人可见。

主体名称匹配
------------

搜索时的权限判定使用 |Fess| 的登录名（即主体名称）。由于此功能计算出的权限来自Slack的邮箱
地址，因此 |Fess| 的登录名必须与Slack的邮箱地址一致。Slack会将邮箱地址统一转换为小写，因此
请同样将 |Fess| 一侧的登录名保持为小写。若两者不一致，并不会导致看到他人的内容，而是会使
相应用户的搜索结果始终为0条（由于原因不易察觉，请特别注意）。

其他注意事项
------------

- 不使用Slack的用户组（User Group）功能，权限直接根据每位成员的邮箱地址计算
- 可通过 ``default_permissions`` 指定无论频道成员关系如何都授予所有文档的附加权限（仅在
  ``permission_sync=true`` 时生效）
- 若保持 ``permission_sync=false`` 而将 ``include_private=true``\ ，则私有频道的内容仅根据
  数据存储设置中「权限」栏的设置进行索引；若该栏为空，则实际上对所有人公开
- 对已经建立索引的工作区，事后启用 ``permission_sync`` 并不会为此前已索引的文档追溯授予
  权限。如需应用权限，请设置 ``permission_sync=true`` 和 ``role=message.roles``\ 后重新爬取。
  同样，之后禁用 ``permission_sync`` 也不会自动移除已应用到先前已索引文档上的权限

使用示例
========

爬取特定频道
------------

参数:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

脚本:

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

爬取所有频道
------------

参数:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

脚本:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

包含私有频道爬取
----------------

参数:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

脚本:

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\n附件: " + message.attachments
    created=message.timestamp
    url=message.permalink

包含文件爬取
------------

参数:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

脚本:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

包含详细消息信息
----------------

脚本:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

同步权限进行爬取
----------------

限制私有频道的内容，使其只能被该频道的成员搜索到。请事先为Slack App添加
``users:read.email`` 权限。

参数:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

脚本:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::
   若忘记添加 ``role=message.roles``\ ，计算出的权限将不会反映到已索引的文档中。详情参见
   「权限同步（ACL）」。

故障排除
========

错误处理机制
------------

Slack连接器将Slack API的错误分为以下三类进行处理:

- **致命错误**\ （``invalid_auth``、``token_revoked``、``account_inactive``、
  ``missing_scope``、``not_authed``、``token_expired``）: 令牌本身已不可用，因此会使整个
  爬取任务失败
- **临时错误**\ （``ratelimited``、``internal_error``、``fatal_error``、
  ``service_unavailable``、``request_timeout``）: 若重试仍无法解决，会使整个爬取任务失败
  （重试行为详见后文「API速率限制」）
- **频道级错误**\ （``channel_not_found``、``not_in_channel``\ 等）: 仅跳过该频道并给出
  警告，其他频道的爬取继续进行

在早期版本中，即使发生致命错误，爬取仍可能被报告为「成功」，结果导致只索引了0条或部分
文档的「静默部分成功」。目前按照上述三种分类，致命错误和临时错误都必定会被报告为任务失败。

认证错误
--------

**症状**: ``invalid_auth`` 或 ``not_authed``

**确认事项**:

1. 确认令牌是否正确复制
2. 确认令牌格式:

   - Bot User OAuth Token: 以 ``xoxb-`` 开头
   - User OAuth Token: 以 ``xoxp-`` 开头

3. 确认应用是否已安装到工作区
4. 确认是否授予了所需权限

找不到频道
----------

**症状**: ``channel_not_found``

**确认事项**:

1. 确认频道名是否正确（不需要#）
2. 确认应用是否已添加到频道
3. 私有频道时，设置 ``include_private=true``
4. 请确认是否设置了 ``exclude_archived=true``\ 。默认情况下（``exclude_archived=false``），
   已归档的频道仍会被列出并爬取；只有设为 ``true``\ 时，在 ``channels`` 中按频道名指定的
   已归档频道才会无法解析

无法获取消息
------------

**症状**: 爬取成功，但索引的文档很少或为0条

**确认事项**:

1. ``ignore_system_events`` 的默认值为 ``true``\ 。若某频道内的消息全部为
   ``channel_join`` 等系统事件，则该频道会被索引0条文档（参见「高级参数」）
2. 确认频道中是否存在消息
3. 确认应用是否已添加到频道
4. 当 ``permission_sync=true`` 时，若私有频道的成员获取失败，该频道在本次爬取中将不会被
   索引（失败关闭；参见「权限同步（ACL）」）

.. note::

   在早期版本中，即使出现权限缺失（``missing_scope``），爬取仍可能以「成功」状态结束但消息
   数为0。现在，包括 ``missing_scope`` 在内的致命错误会导致整个爬取任务失败。若您的任务
   正在失败，请参阅后文的「权限不足错误」，而非本节。

权限不足错误
------------

**症状**: ``missing_scope``\ （将导致整个爬取任务失败）

**解决方法**:

1. 在Slack App设置中添加所需权限:

   **基础**\ （始终需要）:

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **私有频道**:

   - ``groups:history``
   - ``groups:read``

   **文件**:

   - ``files:read``

   **权限同步**\ （``permission_sync=true``）:

   - ``users:read.email``

2. 重新安装应用
3. 重启 |Fess|

无法爬取文件
------------

**症状**: ``file_crawl=true`` 时也无法获取文件

**确认事项**:

1. 确认是否授予了 ``files:read`` 权限
2. 确认频道中是否实际发布了文件
3. 确认文件的访问权限
4. 超过 ``max_filesize`` 的文件不会被下载（请查看日志中的警告）

API速率限制
-----------

**症状**: ``ratelimited``\ （将导致整个爬取任务失败）

**解决方法**:

1. 若默认的 ``max_retry_count``、``retry_interval`` 无法解决问题，请增大取值
2. 设置 ``read_interval`` 以降低爬取速度
3. 减少频道数量，或拆分为多个数据存储并分散计划

Slack API的 ``ratelimited`` 错误会自动重试：若响应中带有 ``Retry-After`` 头，则使用其
秒数；否则以 ``retry_interval`` 为起点按指数退避（最多重试 ``max_retry_count`` 次，上限
为60秒）。若用尽所有重试后速率限制仍未解除，则整个爬取任务失败。

Slack API的Tier（可调用次数上限）:

- Tier 1: 1+请求/分钟
- Tier 2: 20+请求/分钟 —— ``conversations.list``、``users.list``\ （在每次爬取开始时无条件
  全量获取，因此最容易耗尽此层级）
- Tier 3: 50+请求/分钟 —— ``conversations.history``、``conversations.replies``、
  ``files.list``
- Tier 4: 100+请求/分钟 —— ``conversations.members``\ （仅在 ``permission_sync=true``
  时），``files.info``\ （目前本连接器的爬取流程不会调用此接口）

.. note::

   Slack于2025年5月29日实施的速率限制强化措施（将 ``conversations.history`` 和
   ``conversations.replies`` 两个方法限制为50+请求/分钟）仅适用于分发到创建该应用的工作区
   之外的应用，例如通过Slack Marketplace分发的应用。它不适用于为 |Fess| 创建、仅安装在
   创建该应用的工作区内的内部应用。

有大量消息的情况
----------------

**症状**: 爬取耗时长或超时

**解决方法**:

1. 分割频道设置多个数据存储
2. 分散爬取计划

脚本应用示例
============

消息加工
--------

长消息的摘要:

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

频道名整形:

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-atlassian` - Atlassian连接器
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../security-role` - 基于角色的搜索配置指南
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
