==================================
Groovy脚本指南
==================================

概述
====

Groovy是 |Fess| 的默认脚本语言。
它运行在Java虚拟机（JVM）上，与Java高度兼容，
同时可以使用更简洁的语法编写脚本。

基本语法
========

变量声明
--------

::

    // 类型推断（def）
    def name = "Fess"
    def count = 100

    // 显式类型指定
    String title = "Document Title"
    int pageNum = 1

字符串操作
----------

::

    // 字符串插值（GString）
    def id = 123
    def url = "https://example.com/doc/${id}"

    // 多行字符串
    def content = """
    This is a
    multi-line string
    """

    // 替换
    title.replace("old", "new")
    title.replaceAll(/\s+/, " ")  // 正则表达式

    // 分割与连接
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // 大小写转换
    title.toUpperCase()
    title.toLowerCase()

集合操作
----------------

::

    // 列表
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // 映射
    def map = [name: "Fess", version: "15.5"]
    println map.name
    println map["version"]

条件分支
--------

::

    // if-else
    if (data.status == "active") {
        return "有效"
    } else {
        return "无效"
    }

    // 三元运算符
    def result = data.count > 0 ? "有" : "无"

    // Elvis运算符（null合并运算符）
    def value = data.title ?: "无标题"

    // 安全导航运算符
    def length = data.content?.length() ?: 0

循环处理
----------

::

    // for-each
    for (item in items) {
        println item
    }

    // 闭包
    items.each { item ->
        println item
    }

    // 范围
    (1..10).each { println it }

数据存储脚本
======================

数据存储设置中的脚本示例。

基本映射
------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL生成
---------

::

    // 基于ID的URL生成
    url="https://example.com/article/" + data.id

    // 组合多个字段
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // 条件URL
    url=data.external_url ?: "https://example.com/default/" + data.id

内容加工
----------------

::

    // 移除HTML标签
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // 合并多个字段
    content=data.title + "\n" + data.description + "\n" + data.body

    // 限制长度
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

日期处理
----------

::

    // 解析日期
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // 从epoch秒转换
    lastModified=new Date(data.timestamp * 1000L)

计划任务脚本
============================

计划任务中使用的Groovy脚本示例。

执行爬取任务
--------------------

::

    return container.getComponent("crawlJob").execute();

条件爬取
----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // 仅在非工作时间爬取
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Skipped during business hours"

顺序执行多个任务
------------------------

::

    def results = []

    // 索引优化
    results << container.getComponent("optimizeJob").execute()

    // 执行爬取
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

使用Java类
================

在Groovy脚本中，可以使用Java标准库和Fess的类。

日期与时间
----------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

文件操作
------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/path/to/file.txt")))

HTTP通信
--------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   访问外部资源会影响性能，
   请将其控制在最小限度。

访问Fess组件
==============================

可以使用 ``container`` 访问Fess的组件。

系统帮助器
----------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

获取配置值
------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

执行搜索
----------

::

    def searchHelper = container.getComponent("searchHelper")
    // 设置搜索参数并执行搜索

错误处理
==================

::

    try {
        def result = processData(data)
        return result
    } catch (Exception e) {
        import org.apache.logging.log4j.LogManager
        def logger = LogManager.getLogger("script")
        logger.error("Error processing data: {}", e.message, e)
        return "Error: " + e.message
    }

调试与日志输出
==================

日志输出
--------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", data.id)
    logger.info("Processing document: {}", data.title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message)

调试输出
----------------

::

    // 控制台输出（仅限开发时）
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

最佳实践
==================

1. **保持简单**: 避免复杂逻辑，编写易读的代码
2. **null检查**: 活用 ``?.`` 运算符和 ``?:`` 运算符
3. **异常处理**: 使用适当的try-catch处理意外错误
4. **日志输出**: 输出日志以便于调试
5. **性能**: 最小化外部资源访问

参考信息
========

- `Groovy官方文档 <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - 脚本概述
- :doc:`../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../admin/scheduler-guide` - 调度器配置指南
