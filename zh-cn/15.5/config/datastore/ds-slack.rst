==================================
Slack连接器
==================================

概述
====

Slack连接器提供从Slack工作区获取频道消息并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-slack`` 插件。

支持的内容
==============

- 公共频道消息
- 私有频道消息
- 文件附件（可选）

前提条件
========

1. 需要安装插件
2. 需要创建Slack App并设置权限
3. 需要获取OAuth Access Token

插件安装
------------------------

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
----------------

::

    token=xoxp-your-token-here
    channels=general,random
    file_crawl=false
    include_private=false

参数列表
~~~~~~~~~~~~~~~~

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
     - 是
     - 爬取目标频道（逗号分隔，或 ``*all``）
   * - ``file_crawl``
     - 否
     - 是否也爬取文件（默认: ``false``）
   * - ``include_private``
     - 否
     - 是否包含私有频道（默认: ``false``）

脚本设置
--------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

可用字段
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``message.text``
     - 消息的文本内容
   * - ``message.user``
     - 消息发送者的显示名称
   * - ``message.channel``
     - 消息发送的频道名
   * - ``message.timestamp``
     - 消息发送时间
   * - ``message.permalink``
     - 消息的永久链接
   * - ``message.attachments``
     - 附件文件的回退信息

Slack App设置
=============

1. 创建Slack App
------------------

访问 https://api.slack.com/apps:

1. 点击「Create New App」
2. 选择「From scratch」
3. 输入应用名称（例: Fess Crawler）
4. 选择工作区
5. 点击「Create App」

2. OAuth & Permissions设置
----------------------------

在「OAuth & Permissions」菜单中:

**在Bot Token Scopes中添加以下权限**:

仅公共频道时:

- ``channels:history`` - 读取公共频道消息
- ``channels:read`` - 读取公共频道信息

包含私有频道时（``include_private=true``）:

- ``channels:history``
- ``channels:read``
- ``groups:history`` - 读取私有频道消息
- ``groups:read`` - 读取私有频道信息

也爬取文件时（``file_crawl=true``）:

- ``files:read`` - 读取文件内容

3. 安装应用
-----------------------

在「Install App」菜单中:

1. 点击「Install to Workspace」
2. 确认权限并点击「允许」
3. 复制「Bot User OAuth Token」（以 ``xoxb-`` 开头）

.. note::
   通常使用以 ``xoxb-`` 开头的Bot User OAuth Token，
   但参数中也可以使用以 ``xoxp-`` 开头的User OAuth Token。

4. 添加到频道
---------------------

将App添加到爬取目标频道:

1. 在Slack中打开频道
2. 点击频道名
3. 选择「集成」选项卡
4. 点击「添加应用」
5. 添加创建的应用

使用示例
======

爬取特定频道
--------------------------

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
----------------------------

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
--------------------------------------

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
------------------------

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
----------------------------

脚本:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

故障排除
======================

认证错误
----------

**症状**: ``invalid_auth`` 或 ``not_authed``

**确认事项**:

1. 确认令牌是否正确复制
2. 确认令牌格式:

   - Bot User OAuth Token: 以 ``xoxb-`` 开头
   - User OAuth Token: 以 ``xoxp-`` 开头

3. 确认应用是否已安装到工作区
4. 确认是否授予了所需权限

找不到频道
------------------------

**症状**: ``channel_not_found``

**确认事项**:

1. 确认频道名是否正确（不需要#）
2. 确认应用是否已添加到频道
3. 私有频道时，设置 ``include_private=true``
4. 确认频道是否存在且未归档

无法获取消息
------------------------

**症状**: 爬取成功但消息数为0

**确认事项**:

1. 确认是否授予了所需权限范围:

   - ``channels:history``
   - ``channels:read``
   - 私有频道时: ``groups:history``、``groups:read``

2. 确认频道中是否存在消息
3. 确认应用是否已添加到频道
4. 确认Slack应用是否已启用

权限不足错误
--------------

**症状**: ``missing_scope``

**解决方法**:

1. 在Slack App设置中添加所需权限范围:

   **公共频道**:

   - ``channels:history``
   - ``channels:read``

   **私有频道**:

   - ``groups:history``
   - ``groups:read``

   **文件**:

   - ``files:read``

2. 重新安装应用
3. 重启 |Fess|

无法爬取文件
--------------------------

**症状**: ``file_crawl=true`` 时也无法获取文件

**确认事项**:

1. 确认是否授予了 ``files:read`` 权限范围
2. 确认频道中是否实际发布了文件
3. 确认文件的访问权限

API速率限制
-------------

**症状**: ``rate_limited``

**解决方法**:

1. 增加爬取间隔
2. 减少频道数
3. 分割成多个数据存储并分散计划

Slack API限制:

- Tier 3方法: 50+请求/分钟
- Tier 4方法: 100+请求/分钟

有大量消息的情况
--------------------------

**症状**: 爬取耗时长或超时

**解决方法**:

1. 分割频道设置多个数据存储
2. 分散爬取计划
3. 考虑设置排除旧消息

脚本的高级使用示例
========================

消息过滤
--------------------------

只索引特定用户的消息:

::

    if (message.user == "张三") {
        title=message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

只索引包含关键词的消息:

::

    if (message.text.contains("重要") || message.text.contains("故障")) {
        title="[重要] " + message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

消息加工
----------------

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
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
