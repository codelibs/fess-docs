========================
爬虫高级配置
========================

概述
====

本指南介绍 |Fess| 爬虫的高级配置。
有关基本爬虫配置,请参阅 :doc:`crawler-basic`。

.. warning::
   本页的配置可能会影响整个系统。
   变更配置时,请在测试环境中充分测试后再应用到生产环境。

全局配置
========

配置文件位置
------------------

爬虫的详细配置在以下文件中进行。

- **主配置**: ``/etc/fess/fess_config.properties`` (或 ``app/WEB-INF/classes/fess_config.properties``)
- **内容长度配置**: ``app/WEB-INF/classes/crawler/contentlength.xml``
- **组件配置**: ``app/WEB-INF/classes/crawler/container.xml``

默认脚本
--------------------

设置爬虫的默认脚本语言。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.default.script``
     - 爬虫脚本语言
     - ``groovy``

::

    crawler.default.script=groovy

HTTP 线程池
------------------

HTTP 爬虫的线程池配置。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.http.thread_pool.size``
     - HTTP 线程池大小
     - ``0``

::

    # 0时为自动配置
    crawler.http.thread_pool.size=0

文档处理配置
====================

基本配置
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.max.site.length``
     - 文档站点的最大行数
     - ``100``
   * - ``crawler.document.site.encoding``
     - 文档站点编码
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - 未知主机名的替代值
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - 英文文档使用站点编码
     - ``false``
   * - ``crawler.document.append.data``
     - 向文档添加数据
     - ``true``
   * - ``crawler.document.append.filename``
     - 向文档添加文件名
     - ``false``

配置示例
~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

单词处理配置
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.max.alphanum.term.size``
     - 英数字单词最大长度
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - 符号单词最大长度
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - 删除重复单词
     - ``false``

配置示例
~~~~~~

::

    # 将英数字最大长度改为50个字符
    crawler.document.max.alphanum.term.size=50

    # 将符号最大长度改为20个字符
    crawler.document.max.symbol.term.size=20

    # 删除重复单词
    crawler.document.duplicate.term.removed=true

.. note::
   增大 ``max.alphanum.term.size`` 可以完整索引长ID、令牌、URL等,
   但会增加索引大小。

字符处理配置
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.space.chars``
     - 空白字符定义
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - 句点字符定义
     - ``\u002e\u06d4...``

配置示例
~~~~~~

::

    # 默认值(包含Unicode字符)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

协议配置
==============

支持的协议
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.web.protocols``
     - Web爬取协议
     - ``http,https``
   * - ``crawler.file.protocols``
     - 文件爬取协议
     - ``file,smb,smb1,ftp,storage,s3,gcs``

配置示例
~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage,s3,gcs

环境变量参数
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.data.env.param.key.pattern``
     - 环境变量参数键模式
     - ``^FESS_ENV_.*``

::

    # 可在爬取配置中使用以 FESS_ENV_ 开头的环境变量
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

robots.txt 配置
===============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.ignore.robots.txt``
     - 忽略 robots.txt
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - 忽略 robots 元标签
     - ``false``
   * - ``crawler.ignore.content.exception``
     - 忽略内容异常
     - ``true``

配置示例
~~~~~~

::

    # 忽略 robots.txt(不推荐)
    crawler.ignore.robots.txt=false

    # 忽略特定的 robots 标签
    crawler.ignore.robots.tags=

    # 忽略内容异常
    crawler.ignore.content.exception=true

.. warning::
   设置为 ``crawler.ignore.robots.txt=true`` 可能违反网站的使用条款。
   爬取外部网站时请注意。

错误处理配置
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.failure.url.status.codes``
     - 视为失败的 HTTP 状态码
     - ``404``

配置示例
~~~~~~

::

    # 除404外,也将403视为错误
    crawler.failure.url.status.codes=404,403

系统监控配置
================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.system.monitor.interval``
     - 系统监控间隔(秒)
     - ``60``

::

    # 每30秒监控系统
    crawler.system.monitor.interval=30

热线程配置
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.hotthread.ignore_idle_threads``
     - 忽略空闲线程
     - ``true``
   * - ``crawler.hotthread.interval``
     - 快照间隔
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - 快照数
     - ``10``
   * - ``crawler.hotthread.threads``
     - 监控线程数
     - ``3``
   * - ``crawler.hotthread.timeout``
     - 超时时间
     - ``30s``
   * - ``crawler.hotthread.type``
     - 监控类型
     - ``cpu``

配置示例
~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

元数据配置
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.metadata.content.excludes``
     - 排除的元数据
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - 元数据名称映射
     - ``title=title:string...``

配置示例
~~~~~~

::

    # 排除的元数据
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # 元数据名称映射
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

HTML 爬虫配置
===================

XPath 配置
----------

用于提取 HTML 元素的 XPath 配置。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.html.content.xpath``
     - 内容 XPath
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - 语言 XPath
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - 摘要 XPath
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - 规范 URL 的 XPath
     - ``//LINK[@rel='canonical'][1]/@href``

配置示例
~~~~~~

::

    # 默认配置
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

自定义 XPath 示例
~~~~~~~~~~~~~~~~~~~

::

    # 仅提取特定 div 元素作为内容
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # 摘要中也包含 meta keywords
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

HTML 标签处理
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.html.pruned.tags``
     - 删除的 HTML 标签
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - 摘要最大长度
     - ``120``
   * - ``crawler.document.html.default.lang``
     - 默认语言
     - (空)

配置示例
~~~~~~

::

    # 添加要删除的标签
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # 摘要长度设为200个字符
    crawler.document.html.max.digest.length=200

    # 默认语言设为日语
    crawler.document.html.default.lang=ja

URL 模式过滤器
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.html.default.include.index.patterns``
     - 包含在索引中的 URL 模式
     - (空)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - 从索引中排除的 URL 模式
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - 包含在搜索结果中的 URL 模式
     - (空)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - 从搜索结果中排除的 URL 模式
     - (空)

配置示例
~~~~~~

::

    # 默认排除模式
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # 仅索引特定路径
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

文件爬虫配置
======================

基本配置
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.file.name.encoding``
     - 文件名编码
     - (空)
   * - ``crawler.document.file.no.title.label``
     - 无标题文件的标签
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - 忽略空内容
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - 标题最大长度
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - 摘要最大长度
     - ``200``

配置示例
~~~~~~

::

    # 处理 Windows-31J 文件名
    crawler.document.file.name.encoding=Windows-31J

    # 无标题文件的标签
    crawler.document.file.no.title.label=无标题

    # 忽略空文件
    crawler.document.file.ignore.empty.content=true

    # 标题和摘要长度
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

内容处理
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.file.append.meta.content``
     - 向内容添加元数据
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - 向内容添加正文
     - ``true``
   * - ``crawler.document.file.default.lang``
     - 默认语言
     - (空)

配置示例
~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=ja

文件 URL 模式过滤器
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.file.default.include.index.patterns``
     - 包含在索引中的模式
     - (空)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - 从索引中排除的模式
     - (空)
   * - ``crawler.document.file.default.include.search.patterns``
     - 包含在搜索结果中的模式
     - (空)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - 从搜索结果中排除的模式
     - (空)

配置示例
~~~~~~

::

    # 仅索引特定扩展名
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # 排除 temp 文件夹
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

MIME 类型检测覆盖
--------------------

默认情况下，|Fess| 使用 Apache Tika 进行基于内容的 MIME 类型检测。
在某些情况下，基于内容的检测可能会产生错误的结果。
例如，以 ``REM`` 注释开头的 Oracle SQL 文件可能会被错误地检测为
批处理文件（``application/x-bat``），因为 ``REM`` 关键字
与批处理文件的魔术模式匹配。

``crawler.document.mimetype.extension.overrides`` 属性允许您
基于文件扩展名覆盖 MIME 类型检测，从而绕过特定文件类型的基于内容的检测。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.mimetype.extension.overrides``
     - 扩展名到 MIME 类型的覆盖映射（每行一个，格式：``.ext=mime/type``）
     - (空)

配置示例
~~~~~~~~~

::

    # 覆盖 SQL 文件的 MIME 类型检测
    crawler.document.mimetype.extension.overrides=\
    .sql=text/x-sql\n\
    .plsql=text/x-plsql\n\
    .pls=text/x-plsql

每行包含一个 ``.扩展名=MIME类型`` 格式的映射。
多个映射使用 ``\n``（换行符）分隔。
扩展名匹配不区分大小写（``.SQL`` 和 ``.sql`` 被视为相同）。

.. note::
   当文件扩展名与此映射中的条目匹配时，将立即返回配置的 MIME 类型，
   而不执行基于内容的检测。
   扩展名不在映射中的文件将继续使用正常的 Tika 检测。

缓存配置
==============

文档缓存
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``crawler.document.cache.enabled``
     - 启用文档缓存
     - ``true``
   * - ``crawler.document.cache.max.size``
     - 缓存最大大小(字节)
     - ``2621440`` (2.5MB)
   * - ``crawler.document.cache.supported.mimetypes``
     - 缓存目标 MIME 类型
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - 视为 HTML 的 MIME 类型
     - ``text/html``

配置示例
~~~~~~

::

    # 启用文档缓存
    crawler.document.cache.enabled=true

    # 缓存大小设为5MB
    crawler.document.cache.max.size=5242880

    # 缓存目标 MIME 类型
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # 视为 HTML 的 MIME 类型
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   启用缓存后,搜索结果中会显示缓存链接,
   用户可以查看爬取时的内容。

JVM 选项
==============

可以配置爬虫进程的 JVM 选项。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``jvm.crawler.options``
     - 爬虫的 JVM 选项
     - ``-Xms128m -Xmx512m...``

默认配置
--------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

主要选项说明
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 选项
     - 说明
   * - ``-Xms128m``
     - 初始堆大小(128MB)
   * - ``-Xmx512m``
     - 最大堆大小(512MB)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Metaspace 最大大小(128MB)
   * - ``-XX:+UseG1GC``
     - 使用 G1 垃圾收集器
   * - ``-XX:MaxGCPauseMillis=60000``
     - GC 停止时间目标值(60秒)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - 禁用 OutOfMemory 时的堆转储

自定义配置示例
--------------

**爬取大型文件时:**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**调试时:**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

详情请参阅 :doc:`setup-memory`。

性能调优
==========================

爬取速度优化
--------------------

**1. 调整线程数**

通过增加并行爬取数可以提高爬取速度。

::

    # 在管理页面的爬取配置中调整线程数
    线程数: 10

但需注意目标服务器的负载。

**2. 调整超时**

对于响应慢的网站,可调整超时时间。

::

    # 在爬取配置的"配置参数"中添加
    client.connectionTimeout=10000
    client.socketTimeout=30000

**3. 排除不需要的内容**

通过排除图片、CSS、JavaScript 文件等可以提高爬取速度。

::

    # 排除 URL 模式
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. 重试配置**

调整错误时的重试次数和间隔。

::

    # 在爬取配置的"配置参数"中添加
    client.maxRetry=3
    client.retryInterval=1000

内存使用量优化
--------------------

**1. 调整堆大小**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. 调整缓存大小**

::

    crawler.document.cache.max.size=1048576  # 1MB

**3. 排除大型文件**

::

    # 在爬取配置的"配置参数"中添加
    client.maxContentLength=10485760  # 10MB

详情请参阅 :doc:`setup-memory`。

索引质量提升
----------------------

**1. 优化 XPath**

排除不需要的元素(导航、广告等)。

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. 优化摘要**

::

    crawler.document.html.max.digest.length=200

**3. 元数据映射**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

故障排除
======================

内存不足
----------

**症状:**

- ``fess_crawler.log`` 中记录了 ``OutOfMemoryError``
- 爬取中途停止

**对策:**

1. 增加爬虫堆大小

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. 减少并行线程数

3. 排除大型文件

详情请参阅 :doc:`setup-memory`。

爬取缓慢
--------------

**症状:**

- 爬取耗时过长
- 频繁发生超时

**对策:**

1. 增加线程数(注意目标服务器负载)

2. 调整超时

   ::

       client.connectionTimeout=5000
       client.socketTimeout=10000

3. 排除不需要的 URL

无法提取特定内容
------------------------------

**症状:**

- 页面文本未正确提取
- 重要信息未包含在搜索结果中

**对策:**

1. 确认并调整 XPath

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. 确认删除标签

   ::

       crawler.document.html.pruned.tags=script,style

3. 对于由 JavaScript 动态生成的内容,请考虑其他方法(如 API 爬取)

发生乱码
------------------

**症状:**

- 搜索结果中出现乱码
- 特定语言未正确显示

**对策:**

1. 确认编码配置

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. 设置文件名编码

   ::

       crawler.document.file.name.encoding=Windows-31J

3. 在日志中确认编码错误

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

最佳实践
==================

1. **在测试环境中验证**

   应用到生产环境前,请在测试环境中充分验证。

2. **逐步调整**

   不要一次大幅变更配置,应逐步调整并确认效果。

3. **监控日志**

   变更配置后,请监控日志以确认没有错误或性能问题。

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **备份**

   变更配置文件前,请务必进行备份。

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **文档化**

   请记录变更的配置及其原因。

S3/GCS 爬虫配置
==================

S3 爬虫
-------

用于爬取 Amazon S3 和 S3 兼容存储（MinIO 等）的配置。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 参数
     - 说明
     - 默认值
   * - ``client.endpoint``
     - S3 端点 URL
     - (必须)
   * - ``client.accessKey``
     - 访问密钥
     - (必须)
   * - ``client.secretKey``
     - 私密密钥
     - (必须)
   * - ``client.region``
     - AWS 区域
     - ``us-east-1``
   * - ``client.connectTimeout``
     - 连接超时(ms)
     - ``10000``
   * - ``client.readTimeout``
     - 读取超时(ms)
     - ``10000``

配置示例
~~~~~~

在文件抓取配置的"配置参数"中添加以下内容。

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=AKIAIOSFODNN7EXAMPLE
    client.secretKey=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    client.region=ap-northeast-1

GCS 爬虫
--------

用于爬取 Google Cloud Storage 的配置。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 参数
     - 说明
     - 默认值
   * - ``client.projectId``
     - Google Cloud 项目 ID
     - (必须)
   * - ``client.credentialsFile``
     - 服务账户 JSON 文件路径
     - (可选)
   * - ``client.endpoint``
     - 自定义端点
     - (可选)
   * - ``client.connectTimeout``
     - 连接超时(ms)
     - ``10000``
   * - ``client.writeTimeout``
     - 写入超时(ms)
     - ``10000``
   * - ``client.readTimeout``
     - 读取超时(ms)
     - ``10000``

配置示例
~~~~~~

在文件抓取配置的"配置参数"中添加以下内容。

::

    client.projectId=my-gcp-project
    client.credentialsFile=/etc/fess/gcs-credentials.json

.. note::
   省略 ``credentialsFile`` 时，将使用环境变量 ``GOOGLE_APPLICATION_CREDENTIALS``。

参考信息
========

- :doc:`crawler-basic` - 爬虫基本配置
- :doc:`crawler-thumbnail` - 缩略图配置
- :doc:`setup-memory` - 内存配置
- :doc:`admin-logging` - 日志配置
- :doc:`search-advanced` - 高级搜索配置
