================
日志通知
================

概述
====

|Fess| 具有自动捕获 ERROR 和 WARN 级别日志事件并通知管理员的功能。
通过此功能,可以迅速检测系统异常,尽早开始故障处理。

主要特点:

- **支持的通知渠道**: 邮件、Slack、Google Chat
- **目标进程**: 主应用程序、爬虫、建议生成、缩略图生成
- **默认禁用**: 采用选择加入方式,需要明确启用

工作原理
========

日志通知按以下流程运行。

1. Log4j2 的 ``LogNotificationAppender`` 捕获达到或超过设定级别的日志事件。
2. 捕获的事件存储在内存缓冲区中(默认最多 1,000 条)。当缓冲区超过上限时,将从最旧的事件开始依次丢弃。
3. 定时器每隔 30 秒将缓冲区中的事件写入 OpenSearch 的索引(``fess_log.notification_queue``)。
4. "Log Notification"调度任务每隔 5 分钟从 OpenSearch 读取事件,按日志级别分组后,逐级发送通知。
5. 通知发送后,已处理的事件将从索引中删除。

.. note::
   每个节点仅以自身记录的日志为通知对象(事件按 ``hostname`` 进行筛选)。
   在集群配置中,会为每个节点分别发送独立的通知。

.. note::
   为防止无限循环,与通知功能自身相关的日志记录器
   (``LogNotificationAppender``、``LogNotificationHelper``、``LogNotificationTarget``、
   ``LogNotificationJob``、``NotificationHelper``,以及用于 HTTP 通信的
   ``org.codelibs.curl``)产生的日志将从通知对象中排除。

设置
====

启用
----

从管理页面启用
~~~~~~~~~~~~~~

1. 登录管理页面。
2. 从"系统"菜单选择"通用"。
3. 启用"Log Notification"复选框。
4. 在"Log Notification Level"中选择通知对象级别(``ERROR``、``WARN``、``INFO``、``DEBUG``、``TRACE``)。
5. 点击"更新"按钮。

.. note::
   默认情况下仅 ``ERROR`` 级别为通知对象。
   选择 ``WARN`` 时,``WARN`` 和 ``ERROR`` 都会被通知。

通过系统属性启用
~~~~~~~~~~~~~~~~

也可以直接设置在管理页面的"通用"设置中保存的系统属性(``system.properties``)。

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

通知目标设置
------------

通知目标(邮件收件地址、Slack / Google Chat 的 Webhook URL)均可在管理页面的
"系统"→"通用"设置中进行配置。请至少设置一个通知目标。
如果未设置任何通知目标,日志通知任务将不发送任何内容直接结束。

邮件通知
~~~~~~~~

要使用邮件通知,需要进行以下设置。

1. 邮件服务器设置(``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. 在管理页面的"通用"设置的"通知邮件"中输入邮件地址。
   多个地址可以用逗号分隔指定。

Slack 通知
~~~~~~~~~~

在管理页面的"通用"设置的"Slack Webhook URLs"中输入 Slack 的 Incoming Webhook URL。
多个 URL 可以用逗号或空格分隔指定。
此值将作为系统属性 ``slack.webhook.urls`` 保存。

Google Chat 通知
~~~~~~~~~~~~~~~~

在管理页面的"通用"设置的"Google Chat Webhook URLs"中输入 Google Chat 的 Webhook URL。
多个 URL 可以用逗号或空格分隔指定。
此值将作为系统属性 ``google.chat.webhook.urls`` 保存。

.. note::
   如果未设置"通知邮件"而仅设置了 Slack 或 Google Chat 的 Webhook URL,
   则不会发送邮件,仅向 Slack / Google Chat 发送通知。
   Slack / Google Chat 将收到与邮件通知相同的主题和正文作为消息。

配置属性
========

可以在 ``fess_config.properties`` 中设置以下属性。

.. list-table:: 日志通知配置属性
   :header-rows: 1
   :widths: 40 15 45

   * - 属性
     - 默认值
     - 说明
   * - ``log.notification.flush.interval``
     - ``30``
     - 从缓冲区到 OpenSearch 的刷新间隔(秒)
   * - ``log.notification.buffer.size``
     - ``1000``
     - 内存缓冲区中保持的最大事件数
   * - ``log.notification.interval``
     - ``300``
     - 通知消息中显示的统计周期(秒)。这是仅用于显示的值,并非实际的任务执行间隔(请参阅后述的注记)。
   * - ``log.notification.search.size``
     - ``1000``
     - 单次任务执行从 OpenSearch 获取的最大事件数
   * - ``log.notification.max.display.events``
     - ``50``
     - 单次通知消息中包含的最大事件数
   * - ``log.notification.max.message.length``
     - ``200``
     - 每条日志消息的最大字符数(超出部分将被截断)
   * - ``log.notification.max.details.length``
     - ``3000``
     - 通知消息详细部分的最大字符数

.. note::
   ``log.notification.flush.interval`` 的变更将在 |Fess| 重启后生效。
   其他属性将从下一个通知周期开始生效。

.. note::
   ``log.notification.interval`` 是用于通知消息内"过去 N 秒间"显示文本的值,
   并不会改变任务的执行频率。实际的执行间隔由"Log Notification"调度任务的
   cron 设置(默认每隔 5 分钟)决定。若要更改任务的执行间隔,请从
   "系统"→"调度器"更改此任务的 cron 表达式,并同时调整
   ``log.notification.interval`` 使显示与实际情况保持一致。

通知消息格式
============

邮件通知
--------

邮件通知以以下格式发送。

**主题:**

::

    [FESS] ERROR Log Alert: hostname

**正文:**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR 和 WARN 的事件按级别分别作为独立的通知发送。

.. note::
   当显示的事件数超过 ``log.notification.max.display.events`` 时,详细部分的开头将变为
   ``Total: N event(s) (showing M)``,并在末尾附加 ``... and X more``。
   每条日志消息超过 ``log.notification.max.message.length`` 时,末尾将以 ``...`` 截断;
   整个详细部分超过 ``log.notification.max.details.length`` 时,后续内容将被截断。

Slack / Google Chat 通知
------------------------

Slack 和 Google Chat 的通知也以相同的内容作为消息发送。

运维指南
========

推荐设置
--------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 环境
     - 推荐级别
     - 理由
   * - 生产环境
     - ``ERROR``
     - 仅通知重要错误,减少噪音
   * - 演示环境
     - ``WARN``
     - 包含潜在问题一并通知
   * - 开发环境
     - 禁用
     - 直接查看日志文件

OpenSearch 索引
---------------

日志通知功能使用 ``fess_log.notification_queue`` 索引临时存储事件
(索引名为 ``index.log`` 的值(默认 ``fess_log``)加上 ``.notification_queue`` 而成)。
该索引在功能首次使用时自动创建。
由于通知发送后事件会被删除,通常索引大小不会变大。

.. note::
   单次任务执行处理的事件数以 ``log.notification.search.size``(默认 1,000 条)为上限。
   超过此上限累积的事件,将在通知发送后被一并丢弃,不会延续到此后的执行中。
   在短时间内产生大量日志的环境中,请根据需要提高
   ``log.notification.search.size``。

故障排除
========

通知未发送
----------

1. **确认启用状态**

   在管理页面的"通用"设置中确认"Log Notification"是否已启用。

2. **确认通知目标**

   确认是否已设置至少一个通知目标("通知邮件"、"Slack Webhook URLs"、
   "Google Chat Webhook URLs"中的任意一个)。如果均未设置,任务将输出
   ``No notification targets configured.`` 而不发送任何内容。

3. **确认邮件服务器设置**

   使用邮件通知时,确认 ``fess_env.properties`` 中邮件服务器是否正确配置。

4. **确认调度任务**

   在"系统"→"调度器"中确认"Log Notification"任务是否已启用。
   如果此任务被禁用,将不会发送通知。

5. **确认日志**

   在 ``fess.log`` 中确认通知相关的错误消息。

   ::

       grep -i "notification" /var/log/fess/fess.log

通知过多
--------

1. **提高日志级别**

   将通知级别从 ``WARN`` 更改为 ``ERROR``。

2. **处理根本原因**

   如果频繁发生错误,请调查错误的根本原因。

通知内容被截断
--------------

请调整以下属性。

- ``log.notification.max.details.length``: 详细部分的最大字符数
- ``log.notification.max.display.events``: 显示事件的最大数量
- ``log.notification.max.message.length``: 每条消息的最大字符数

参考信息
========

- :doc:`admin-logging` - 日志配置
- :doc:`setup-memory` - 内存配置
