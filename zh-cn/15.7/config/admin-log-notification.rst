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
2. 捕获的事件存储在内存缓冲区中(最多1,000条)。
3. 定时器每隔30秒将缓冲区中的事件写入 OpenSearch 的索引(``fess_log.notification_queue``)。
4. 调度任务每隔5分钟从 OpenSearch 读取事件,按日志级别分组后发送通知。
5. 通知发送后,已处理的事件将从索引中删除。

.. note::
   通知功能自身的日志(``LogNotificationHelper``、``LogNotificationJob`` 等)
   为防止无限循环,不包含在通知对象中。

设置
====

启用
----

从管理页面启用
~~~~~~~~~~~~~~

1. 登录管理页面。
2. 从"系统"菜单选择"常规"。
3. 启用"日志通知"复选框。
4. 在"日志通知级别"中选择通知对象级别(``ERROR``、``WARN``、``INFO``、``DEBUG``、``TRACE``)。
5. 点击"更新"按钮。

.. note::
   默认情况下仅 ``ERROR`` 级别为通知对象。
   选择 ``WARN`` 时,``WARN`` 和 ``ERROR`` 都会被通知。

通过系统属性启用
~~~~~~~~~~~~~~~~

也可以直接设置在管理页面的"常规"设置中保存的系统属性。

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

通知目标设置
------------

邮件通知
~~~~~~~~

要使用邮件通知,需要进行以下设置。

1. 邮件服务器设置(``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. 在管理页面的"常规"设置中,在"通知目标"中输入邮件地址。多个地址用逗号分隔。

Slack 通知
~~~~~~~~~~

通过设置 Slack 的 Incoming Webhook URL,可以向 Slack 频道发送通知。

Google Chat 通知
~~~~~~~~~~~~~~~~

通过设置 Google Chat 的 Webhook URL,可以向 Google Chat 空间发送通知。

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
     - 通知任务的执行间隔(秒)
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
   这些属性的变更将在 |Fess| 重启后生效。

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
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR 和 WARN 的事件按级别分别作为独立的通知发送。

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

日志通知功能使用 ``fess_log.notification_queue`` 索引临时存储事件。
该索引在功能首次使用时自动创建。
由于通知发送后事件会被删除,通常索引大小不会变大。

故障排除
========

通知未发送
----------

1. **确认启用状态**

   在管理页面的"常规"设置中确认"日志通知"是否已启用。

2. **确认通知目标**

   邮件通知时,确认"通知目标"中是否已设置邮件地址。

3. **确认邮件服务器设置**

   确认 ``fess_env.properties`` 中邮件服务器是否正确配置。

4. **确认日志**

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
