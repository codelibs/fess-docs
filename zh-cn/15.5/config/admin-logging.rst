============
日志配置
============

概述
====

|Fess| 输出多个日志文件以记录系统运行状况和错误信息。
通过适当的日志配置,可以简化故障排除和系统监控。

日志文件类型
==================

主要日志文件
------------------

|Fess| 输出的主要日志文件如下。

.. list-table:: 日志文件列表
   :header-rows: 1
   :widths: 25 75

   * - 文件名
     - 内容
   * - ``fess.log``
     - 管理页面和搜索页面的操作日志、应用程序错误、系统事件
   * - ``fess_crawler.log``
     - 爬取执行时的日志、爬取目标URL、获取的文档信息、错误
   * - ``fess_suggest.log``
     - 建议(搜索候选)生成时的日志、索引更新信息
   * - ``server_?.log``
     - Tomcat等应用服务器的系统日志
   * - ``audit.log``
     - 用户认证、登录/登出、重要操作的审计日志

日志文件位置
------------------

**Zip安装:**

::

    {FESS_HOME}/logs/

**RPM/DEB软件包:**

::

    /var/log/fess/

故障排除时的日志确认
----------------------------------

问题发生时,请按以下步骤确认日志。

1. **识别错误类型**

   - 应用程序错误 → ``fess.log``
   - 爬取错误 → ``fess_crawler.log``
   - 认证错误 → ``audit.log``
   - 服务器错误 → ``server_?.log``

2. **确认最新错误**

   ::

       tail -f /var/log/fess/fess.log

3. **搜索特定错误**

   ::

       grep -i "error" /var/log/fess/fess.log
       grep -i "exception" /var/log/fess/fess.log

4. **确认错误上下文**

   通过确认错误发生前后的日志可以识别原因。

   ::

       grep -B 10 -A 10 "OutOfMemoryError" /var/log/fess/fess.log

日志级别配置
================

什么是日志级别
--------------

日志级别控制输出日志的详细程度。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 级别
     - 说明
   * - ``FATAL``
     - 致命错误(应用程序无法继续)
   * - ``ERROR``
     - 错误(部分功能无法运行)
   * - ``WARN``
     - 警告(潜在问题)
   * - ``INFO``
     - 信息(重要事件)
   * - ``DEBUG``
     - 调试信息(详细的运行日志)
   * - ``TRACE``
     - 跟踪信息(最详细)

推荐日志级别
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 环境
     - 推荐级别
     - 理由
   * - 生产环境
     - ``WARN``
     - 重视性能和磁盘容量
   * - 演示环境
     - ``INFO``
     - 记录重要事件
   * - 开发环境
     - ``DEBUG``
     - 需要详细的调试信息
   * - 问题调查时
     - ``DEBUG`` 或 ``TRACE``
     - 临时启用详细日志

从管理页面变更
------------------

最简单的方法是从管理页面变更。

1. 登录管理页面。
2. 从"系统"菜单选择"常规"。
3. 在"日志级别"中选择所需级别。
4. 点击"更新"按钮。

.. note::
   管理页面的变更在 |Fess| 重启后也会保持。

通过配置文件变更
----------------------

要进行更详细的日志配置,请编辑 Log4j2 的配置文件。

配置文件位置
~~~~~~~~~~~~~~~~~~

- **Zip安装**: ``app/WEB-INF/classes/log4j2.xml``
- **RPM/DEB软件包**: ``/etc/fess/log4j2.xml``

基本配置示例
~~~~~~~~~~~~~~

**默认日志级别:**

::

    <Logger name="org.codelibs.fess" level="warn"/>

**示例: 更改为DEBUG级别**

::

    <Logger name="org.codelibs.fess" level="debug"/>

**示例: 更改特定包的日志级别**

::

    <Logger name="org.codelibs.fess.crawler" level="info"/>
    <Logger name="org.codelibs.fess.ds" level="debug"/>
    <Logger name="org.codelibs.fess.app.web" level="warn"/>

.. warning::
   ``DEBUG`` 或 ``TRACE`` 级别会输出大量日志,
   请勿在生产环境中使用。会影响磁盘容量和性能。

通过环境变量配置
~~~~~~~~~~~~~~~~~~

系统启动时也可以指定日志级别。

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dlog.level=debug"

爬虫日志配置
====================

爬虫日志默认以 ``INFO`` 级别输出。

管理页面配置
----------------

1. 从管理页面的"爬虫"菜单打开目标爬取配置。
2. 在"配置"选项卡中选择"脚本"。
3. 在脚本栏中添加以下内容。

::

    logLevel("DEBUG")

可配置的值:

- ``FATAL``
- ``ERROR``
- ``WARN``
- ``INFO``
- ``DEBUG``
- ``TRACE``

仅更改特定URL模式的日志级别
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    if (url.contains("example.com")) {
        logLevel("DEBUG")
    }

更改整个爬虫进程的日志级别
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 ``fess_config.properties`` 中配置:

::

    logging.level.org.codelibs.fess.crawler=DEBUG

日志轮转
==================

概述
----

日志文件会随时间增大,需要定期轮转(世代管理)。

Log4j2 自动轮转
-------------------------------

|Fess| 使用 Log4j2 的 RollingFileAppender 自动进行日志轮转。

默认配置
~~~~~~~~~~~~~~~~

- **文件大小**: 超过 10MB 时轮转
- **保留世代数**: 最多10个文件

配置文件示例(``log4j2.xml``):

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%i">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <SizeBasedTriggeringPolicy size="10MB"/>
        </Policies>
        <DefaultRolloverStrategy max="10"/>
    </RollingFile>

每日轮转配置
~~~~~~~~~~~~~~~~~~~~~~~~

按日而非大小进行轮转:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

压缩配置
~~~~~~~~

轮转时自动压缩:

::

    <RollingFile name="FessFile"
                 fileName="${log.dir}/fess.log"
                 filePattern="${log.dir}/fess.log.%d{yyyy-MM-dd}.gz">
        <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n"/>
        <Policies>
            <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
        </Policies>
        <DefaultRolloverStrategy max="30"/>
    </RollingFile>

logrotate 轮转
------------------------------

在 Linux 环境中,也可以使用 logrotate 管理日志轮转。

``/etc/logrotate.d/fess`` 示例:

::

    /var/log/fess/*.log {
        daily
        rotate 14
        compress
        delaycompress
        missingok
        notifempty
        create 0644 fess fess
        sharedscripts
        postrotate
            systemctl reload fess > /dev/null 2>&1 || true
        endscript
    }

配置说明:

- ``daily``: 每日轮转
- ``rotate 14``: 保留14代
- ``compress``: 压缩旧日志
- ``delaycompress``: 不压缩上一代日志(应用程序可能正在写入)
- ``missingok``: 日志文件不存在也不报错
- ``notifempty``: 空日志文件不轮转
- ``create 0644 fess fess``: 新日志文件的权限和所有者

日志监控
========

生产环境建议监控日志文件以尽早检测错误。

需要监控的日志模式
----------------------

重要错误模式
~~~~~~~~~~~~~~~~~~~~

- ``ERROR``、``FATAL`` 级别日志
- ``OutOfMemoryError``
- ``Connection refused``
- ``Timeout``
- ``Exception``
- ``circuit_breaker_exception``
- ``Too many open files``

应警告的模式
~~~~~~~~~~~~~~~~~~

- ``WARN`` 级别日志频发
- ``Retrying``
- ``Slow query``
- ``Queue full``

实时监控
----------------

使用 tail 命令实时监控:

::

    tail -f /var/log/fess/fess.log | grep -i "error\|exception"

同时监控多个日志文件:

::

    tail -f /var/log/fess/*.log

监控工具示例
--------------

**Logwatch**

定期分析和报告日志文件。

::

    # 安装(CentOS/RHEL)
    yum install logwatch

    # 每日报告发送
    logwatch --service fess --mailto admin@example.com

**Logstash + OpenSearch + OpenSearch Dashboards**

实时日志分析和可视化。

**Fluentd**

日志收集和转发。

::

    <source>
      @type tail
      path /var/log/fess/fess.log
      pos_file /var/log/fluentd/fess.log.pos
      tag fess.app
      <parse>
        @type multiline
        format_firstline /^\d{4}-\d{2}-\d{2}/
        format1 /^(?<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?<thread>.*?)\] (?<level>\w+)\s+(?<logger>.*?) - (?<message>.*)/
      </parse>
    </source>

**Prometheus + Grafana**

指标监控和告警。

告警配置
------------

错误检测时的通知示例:

::

    # 简单的邮件通知脚本
    tail -n 0 -f /var/log/fess/fess.log | while read line; do
        echo "$line" | grep -i "error\|fatal" && \
        echo "$line" | mail -s "Fess Error Alert" admin@example.com
    done

日志格式
================

默认格式
----------------------

|Fess| 的默认日志格式:

::

    %d{ISO8601} [%t] %-5p %c - %m%n

各元素说明:

- ``%d{ISO8601}``: 时间戳(ISO8601格式)
- ``[%t]``: 线程名
- ``%-5p``: 日志级别(5字符宽,左对齐)
- ``%c``: 记录器名(包名)
- ``%m``: 消息
- ``%n``: 换行

自定义格式示例
----------------------

JSON格式输出日志
~~~~~~~~~~~~~~~~~~

::

    <PatternLayout>
        <pattern>{"timestamp":"%d{ISO8601}","thread":"%t","level":"%-5p","logger":"%c","message":"%m"}%n</pattern>
    </PatternLayout>

包含更详细信息
~~~~~~~~~~~~~~~~~~~~~~

::

    <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c{1.} [%F:%L] - %m%n"/>

添加的信息:

- ``%c{1.}``: 缩短的包名
- ``%F``: 文件名
- ``%L``: 行号

性能影响
======================

日志输出会影响磁盘I/O和性能。

最佳实践
------------------

1. **生产环境使用WARN级别以上**

   不输出不必要的详细日志。

2. **定期清理日志文件**

   删除或压缩旧日志文件。

3. **使用异步日志输出**

   使用 Log4j2 的异步附加器减少日志输出开销。

   ::

       <Async name="AsyncFile">
           <AppenderRef ref="FessFile"/>
       </Async>

4. **确保适当的磁盘容量**

   为日志文件确保足够的磁盘容量。

5. **选择适当的日志级别**

   根据环境设置日志级别。

性能测量
------------------

测量日志输出影响:

::

    # 确认日志输出量
    du -sh /var/log/fess/

    # 每小时日志增长量
    watch -n 3600 'du -sh /var/log/fess/'

故障排除
======================

日志未输出
------------------

**原因和对策:**

1. **日志目录权限**

   ::

       ls -ld /var/log/fess/
       # 必要时更改权限
       sudo chown -R fess:fess /var/log/fess/
       sudo chmod 755 /var/log/fess/

2. **磁盘容量**

   ::

       df -h /var/log
       # 容量不足时,删除旧日志
       find /var/log/fess/ -name "*.log.*" -mtime +30 -delete

3. **Log4j2配置文件**

   ::

       # 配置文件语法检查
       xmllint --noout /etc/fess/log4j2.xml

4. **SELinux确认**

   ::

       # SELinux启用时
       getenforce
       # 必要时设置上下文
       restorecon -R /var/log/fess/

日志文件过大
------------------------------

1. **调整日志级别**

   请设置为 ``WARN`` 以上。

2. **确认日志轮转配置**

   ::

       # 确认log4j2.xml配置
       grep -A 5 "RollingFile" /etc/fess/log4j2.xml

3. **禁用不必要的日志输出**

   ::

       # 抑制特定包的日志
       <Logger name="org.apache.http" level="error"/>

4. **临时处理**

   ::

       # 压缩旧日志文件
       gzip /var/log/fess/fess.log.[1-9]

       # 删除旧日志文件
       find /var/log/fess/ -name "*.log.*" -mtime +7 -delete

找不到特定日志
------------------------

1. **确认日志级别**

   日志级别过低时不会输出。

   ::

       grep "org.codelibs.fess" /etc/fess/log4j2.xml

2. **确认日志文件路径**

   ::

       # 确认实际日志输出位置
       ps aux | grep fess
       lsof -p <PID> | grep log

3. **确认时间戳**

   请确认系统时间是否正确。

   ::

       date
       timedatectl status

4. **日志缓冲**

   日志可能不会立即写入。

   ::

       # 强制刷新日志
       systemctl reload fess

日志出现乱码
------------------------

1. **编码配置**

   在 ``log4j2.xml`` 中指定字符编码:

   ::

       <PatternLayout pattern="%d{ISO8601} [%t] %-5p %c - %m%n" charset="UTF-8"/>

2. **环境变量配置**

   ::

       export LANG=ja_JP.UTF-8
       export LC_ALL=ja_JP.UTF-8

参考信息
========

- :doc:`setup-memory` - 内存配置
- :doc:`crawler-advanced` - 爬虫高级配置
- :doc:`admin-index-backup` - 索引备份
- `Log4j2 Documentation <https://logging.apache.org/log4j/2.x/>`_
