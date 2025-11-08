====================
爬虫基本配置
====================

概述
====

|Fess| 的爬虫会从网站或文件系统等自动收集内容,并注册到搜索索引中。
本指南介绍爬虫的基本概念和配置方法。

爬虫的基本概念
====================

什么是爬虫
--------------

爬虫(Crawler)是以指定的URL或文件路径为起点,自动收集内容并追踪链接的程序。

|Fess| 的爬虫具有以下特点:

- **支持多种协议**: HTTP/HTTPS、文件系统、SMB、FTP等
- **计划执行**: 定期自动爬取
- **增量爬取**: 仅更新变更的内容
- **并行处理**: 同时爬取多个URL
- **遵守robots协议**: 遵守 robots.txt

爬虫类型
----------------

|Fess| 根据目标提供以下爬虫类型。

.. list-table:: 爬虫类型
   :header-rows: 1
   :widths: 20 40 40

   * - 类型
     - 目标
     - 用途
   * - **Web爬虫**
     - 网站(HTTP/HTTPS)
     - 公开网站、内网网站
   * - **文件爬虫**
     - 文件系统、SMB、FTP
     - 文件服务器、共享文件夹
   * - **数据存储爬虫**
     - 数据库
     - RDB、CSV、JSON等数据源

创建爬取配置
==================

添加基本爬取配置
--------------------------

1. **访问管理页面**

   在浏览器中访问 ``http://localhost:8080/admin`` 并以管理员身份登录。

2. **打开爬虫配置页面**

   从左侧菜单选择"爬虫"→"Web"或"文件系统"。

3. **创建新配置**

   点击"新建"按钮。

4. **输入基本信息**

   - **名称**: 爬取配置的标识名称(例: 公司Wiki)
   - **URL**: 爬取起始URL(例: ``https://wiki.example.com/``)
   - **爬取间隔**: 爬取执行频率(例: 每1小时)
   - **线程数**: 并行爬取数(例: 5)
   - **深度**: 追踪链接的层级深度(例: 3)

5. **保存**

   点击"创建"按钮保存配置。

Web爬虫配置示例
---------------------

公司内网网站爬取
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    名称: 公司门户
    URL: http://intranet.example.com/
    爬取间隔: 每天1次
    线程数: 10
    深度: 无限制(-1)
    最大访问数: 10000

公开网站爬取
~~~~~~~~~~~~~~~~~~~~~~~

::

    名称: 产品网站
    URL: https://www.example.com/products/
    爬取间隔: 每周1次
    线程数: 5
    深度: 5
    最大访问数: 1000

文件爬虫配置示例
--------------------------

本地文件系统
~~~~~~~~~~~~~~~~~~~~~~~~

::

    名称: 文档文件夹
    URL: file:///home/share/documents/
    爬取间隔: 每天1次
    线程数: 3
    深度: 无限制(-1)

SMB/CIFS(Windows文件共享)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    名称: 文件服务器
    URL: smb://fileserver.example.com/share/
    爬取间隔: 每天1次
    线程数: 5
    深度: 无限制(-1)

认证信息配置
--------------

访问需要认证的网站或文件服务器时,需要配置认证信息。

1. 在管理页面选择"爬虫"→"认证"
2. 点击"新建"
3. 输入认证信息:

   ::

       主机名: wiki.example.com
       端口: 443
       认证方式: Basic认证
       用户名: crawler_user
       密码: ********

4. 点击"创建"

执行爬取
==============

手动执行
--------

立即执行已配置的爬取:

1. 在爬取配置列表中选择目标配置
2. 点击"启动"按钮
3. 在"调度器"菜单中确认任务执行状态

计划执行
----------------

定期执行爬取:

1. 打开"调度器"菜单
2. 选择"Default Crawler"任务
3. 设置计划表达式(Cron格式)

   ::

       # 每天凌晨2点执行
       0 0 2 * * ?

       # 每小时0分执行
       0 0 * * * ?

       # 周一至周五下午6点执行
       0 0 18 ? * MON-FRI

4. 点击"更新"

确认爬取状态
------------------

确认正在执行的爬取状态:

1. 打开"调度器"菜单
2. 确认正在执行的任务
3. 在日志中确认详细信息:

   ::

       tail -f /var/log/fess/fess_crawler.log

基本配置项
================

爬取目标限制
------------------

URL模式限制
~~~~~~~~~~~~~~~~~~~~~

可以将特定的URL模式作为爬取目标,或将其排除。

**包含的URL模式(正则表达式):**

::

    # 仅爬取 /docs/ 下的内容
    https://example\.com/docs/.*

**排除的URL模式(正则表达式):**

::

    # 排除特定目录
    .*/admin/.*
    .*/private/.*

    # 排除特定文件扩展名
    .*\.(jpg|png|gif|css|js)$

深度限制
~~~~~~~~~~

限制追踪链接的层级深度:

- **0**: 仅起始URL
- **1**: 起始URL及其链接页面
- **-1**: 无限制(追踪所有链接)

最大访问数
~~~~~~~~~~~~~~

爬取页面数的上限:

::

    最大访问数: 1000

爬取到1000个页面后停止。

并行爬取数(线程数)
--------------------------

指定同时爬取的URL数量。

.. list-table:: 推荐线程数
   :header-rows: 1
   :widths: 40 30 30

   * - 环境
     - 推荐值
     - 说明
   * - 小规模网站(〜1万页)
     - 3〜5
     - 降低目标服务器负载
   * - 中规模网站(1万〜10万页)
     - 5〜10
     - 平衡配置
   * - 大规模网站(10万页以上)
     - 10〜20
     - 需要快速爬取
   * - 文件服务器
     - 3〜5
     - 考虑文件I/O负载

.. warning::
   线程数过多会对爬取目标服务器造成过大负载。
   请设置适当的值。

爬取间隔
------------

指定爬取执行频率。

::

    # 时间指定
    爬取间隔: 3600000  # 毫秒(1小时)

    # 或在调度器中设置
    0 0 2 * * ?  # 每天凌晨2点

文件大小配置
====================

可以设置爬取文件大小的上限。

获取文件大小上限
----------------------------

在爬虫配置的"配置参数"中添加:

::

    client.maxContentLength=10485760

获取最大10MB的文件。默认无限制。

.. note::
   爬取大型文件时,请同时调整内存配置。
   详情请参阅 :doc:`setup-memory`。

索引文件大小上限
------------------------------------

可以为每种文件类型设置索引大小上限。

**默认值:**

- HTML文件: 2.5MB
- 其他文件: 10MB

**配置文件:** ``app/WEB-INF/classes/crawler/contentlength.xml``

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
            "http://dbflute.org/meta/lastadi10.dtd">
    <components namespace="fessCrawler">
            <include path="crawler/container.xml" />

            <component name="contentLengthHelper"
                    class="org.codelibs.fess.crawler.helper.ContentLengthHelper" instance="singleton">
                    <property name="defaultMaxLength">10485760</property><!-- 10M -->
                    <postConstruct name="addMaxLength">
                            <arg>"text/html"</arg>
                            <arg>2621440</arg><!-- 2.5M -->
                    </postConstruct>
                    <postConstruct name="addMaxLength">
                            <arg>"application/pdf"</arg>
                            <arg>5242880</arg><!-- 5M -->
                    </postConstruct>
            </component>
    </components>

添加了处理PDF文件最大5MB的配置。

.. warning::
   增加处理文件大小时,也需要增加爬虫的内存配置。

单词长度限制
==============

概述
----

仅包含英数字的长字符串或连续符号会导致索引大小增加和性能下降。
因此,|Fess| 默认设置了以下限制:

- **连续英数字**: 最多20个字符
- **连续符号**: 最多10个字符

配置方法
--------

编辑 ``fess_config.properties``。

**默认配置:**

::

    crawler.document.max.alphanum.term.size=20
    crawler.document.max.symbol.term.size=10

**示例: 放宽限制**

::

    crawler.document.max.alphanum.term.size=50
    crawler.document.max.symbol.term.size=20

.. note::
   如需搜索长英数字符串(例: 序列号、令牌等),
   请增大此值。但索引大小会增加。

代理服务器配置
==============

概述
----

从内网爬取外部网站时,可能会被防火墙阻止。
这种情况下需要通过代理服务器进行爬取。

配置方法
--------

在管理页面的爬取配置中,在"配置参数"中添加以下内容。

**基本代理配置:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

**需要认证的代理:**

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

**从代理服务器排除特定主机:**

::

    client.nonProxyHosts=localhost|127.0.0.1|*.example.com

系统全局代理配置
--------------------------

所有爬取配置都使用相同代理时,可以通过环境变量配置。

::

    export http_proxy=http://proxy.example.com:8080
    export https_proxy=http://proxy.example.com:8080
    export no_proxy=localhost,127.0.0.1,.example.com

robots.txt 配置
=================

概述
----

robots.txt 是向爬虫指示是否允许爬取的文件。
|Fess| 默认遵守 robots.txt。

配置方法
--------

忽略 robots.txt 时,请编辑 ``fess_config.properties``。

::

    crawler.ignore.robots.txt=true

.. warning::
   爬取外部网站时,请遵守 robots.txt。
   忽略可能会对服务器造成过大负载或违反使用条款。

User-Agent 配置
=================

可以更改爬虫的User-Agent。

管理页面配置
----------------

在爬取配置的"配置参数"中添加:

::

    client.userAgent=MyCompanyCrawler/1.0

系统全局配置
------------------

在 ``fess_config.properties`` 中配置:

::

    crawler.user.agent=MyCompanyCrawler/1.0

编码配置
====================

爬取数据编码
--------------------------------

在 ``fess_config.properties`` 中配置:

::

    crawler.crawling.data.encoding=UTF-8

文件名编码
----------------------------

文件系统文件名的编码:

::

    crawler.document.file.name.encoding=UTF-8

爬取故障排除
================================

爬取未启动
----------------------

**确认事项:**

1. 确认调度器是否已启用

   - 在"调度器"菜单中确认"Default Crawler"任务是否已启用

2. 确认爬取配置是否已启用

   - 在爬取配置列表中确认目标配置是否已启用

3. 确认日志

   ::

       tail -f /var/log/fess/fess.log
       tail -f /var/log/fess/fess_crawler.log

爬取中途停止
------------------------

**可能的原因:**

1. **内存不足**

   - 确认 ``fess_crawler.log`` 中是否有 ``OutOfMemoryError``
   - 增加爬虫内存(详情参阅 :doc:`setup-memory`)

2. **网络错误**

   - 调整超时配置
   - 确认重试配置

3. **爬取目标错误**

   - 确认是否频繁出现404错误
   - 在日志中确认错误详情

特定页面未被爬取
------------------------------

**确认事项:**

1. **确认URL模式**

   - 确认是否匹配排除URL模式

2. **确认 robots.txt**

   - 确认目标网站的 ``/robots.txt``

3. **确认认证**

   - 如需认证的页面,请确认认证配置

4. **深度限制**

   - 确认链接层级是否超过深度限制

5. **最大访问数**

   - 确认是否达到最大访问数

爬取缓慢
--------------

**对策:**

1. **增加线程数**

   - 增加并行爬取数(但需注意目标服务器负载)

2. **排除不需要的URL**

   - 将图片或CSS文件等添加到排除URL模式

3. **调整超时配置**

   - 响应慢的网站,可缩短超时时间

4. **增加爬虫内存**

   - 详情参阅 :doc:`setup-memory`

最佳实践
==================

爬取配置推荐事项
----------------------

1. **设置适当的线程数**

   设置适当的线程数,避免对目标服务器造成过大负载。

2. **优化URL模式**

   通过排除不需要的文件(图片、CSS、JavaScript等),
   可缩短爬取时间并提高索引质量。

3. **设置深度限制**

   根据网站结构设置适当的深度。
   仅在需要爬取整个网站时使用无限制(-1)。

4. **设置最大访问数**

   设置上限,防止意外爬取大量页面。

5. **调整爬取间隔**

   根据更新频率设置适当的间隔。
   - 频繁更新的网站: 每1小时〜数小时
   - 不常更新的网站: 每1天〜1周

计划配置推荐事项
--------------------------

1. **夜间执行**

   在服务器负载较低的时段(例: 深夜2点)执行。

2. **避免重复执行**

   配置为在上次爬取完成后再启动下次爬取。

3. **错误通知**

   配置爬取失败时的邮件通知。

参考信息
========

- :doc:`crawler-advanced` - 爬虫高级配置
- :doc:`crawler-thumbnail` - 缩略图配置
- :doc:`setup-memory` - 内存配置
- :doc:`admin-logging` - 日志配置
