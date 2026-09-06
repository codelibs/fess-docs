==================================
JavaScript脚本指南
==================================

概述
====

JavaScript 是 |Fess| 自 15.9 版本起的默认脚本语言。
它运行于 Sai（CodeLibs 开发的 Nashorn 分支， |Fess| 已将其用于 DI XML 表达式的
解析）之上，脚本以 ECMAScript 6 执行。其标识符为 ``javascript`` ，也可使用别名
``js`` 和 ``sai`` 指定。

.. _javascript-statement-null:

脚本的求值方式
==============

|Fess| 的脚本引擎会先尝试将脚本文本编译为单个"表达式"。只有在解析失败时，
才会将该文本重新编译为"语句"块。

因此，仅返回一个值的简单表达式：

::

    content.length()

以及在顶层包含 ``return`` 语句的脚本：

::

    return container.getComponent("crawlJob").execute();

两者都能正常运行。后者在纯 JavaScript 中通常会导致语法错误，因为顶层不允许使用
``return`` 。但由于它无法编译为表达式，因此会被重新解释为语句块，作为有效脚本
执行。

在每行都被视为单个表达式的场景（如数据存储脚本）中，不能使用由多条语句组成的
脚本。而在整个脚本被求值的场景（如计划任务）中，则可以自由使用多行语句、
``let`` / ``const`` 变量声明以及控制结构。

.. warning::

   作为语句块编译的脚本，只有在包含显式 ``return`` 时才会返回值。当脚本文本无法解析为表达式
   时，它会被包装进函数并作为语句块执行，而没有 ``return`` 的块其求值结果为 ``null`` 。
   仅仅在末尾加一个分号就足以越过这条界线：

   .. list-table::
      :header-rows: 1
      :widths: 40 15 45

      * - 脚本
        - 结果
        - 原因
      * - ``content.length()``
        - ``11``
        - 解析为表达式，表达式的值即为结果
      * - ``content.length();``
        - ``null``
        - 只能解析为语句块，而其中没有 ``return``
      * - ``var x = 1; x + 2``
        - ``null``
        - 只能解析为语句块，而其中没有 ``return``

   在 Groovy 中这三者都会返回值，因为最后求值的语句的值就是脚本的返回值。JavaScript 没有
   这条规则。

   这是迁移中唯一一处不产生任何错误、任何日志行，除了字段悄然变空之外没有其他症状的差异：
   脚本返回 ``null`` 的数据存储映射，只是不设置该字段而已。数据存储的 ``字段名=表达式``
   每一行请写成不带末尾分号的表达式，并为每个计划任务脚本写上显式的 ``return`` 。

基本语法
========

下文中末尾不带分号的行是**表达式**，可在任何位置使用，包括数据存储的 ``字段名=表达式`` 行。
``let`` / ``const`` 声明、 ``if`` 块和循环是**语句**，只能用于整个脚本被求值的场景（如计划
任务），并且脚本必须包含显式的 ``return`` 才会产生值。请参阅上文"脚本的求值方式"。

变量声明
--------

::

    // let（可重新赋值的变量）
    let name = "Fess";
    let count = 100;

    // const（不可重新赋值的常量）
    const title = "Document Title";
    const pageNum = 1;

字符串操作
----------

::

    // 模板字符串（ES6）
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // 多行字符串（模板字符串）
    const content = `
    This is a
    multi-line string
    `;

    // 替换（使用正则表达式；ECMAScript 6 没有 String#replaceAll）
    title.replace(/old/g, "new")
    title.replace(/\s+/g, " ")  // 将连续空白合并为一个

    // 分割与连接
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // 大小写转换
    title.toUpperCase()
    title.toLowerCase()

集合操作
--------

::

    // 数组
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // 对象
    const map = { name: "Fess", version: "15.9" };
    map.name
    map["version"]

条件分支
--------

::

    // if-else
    if (data.status === "active") {
        return "有效";
    } else {
        return "无效";
    }

    // 三元运算符
    data.count > 0 ? "有" : "无"

    // 默认值（逻辑 OR 运算符；JavaScript 没有 Elvis 运算符）
    data.title || "无标题"

    // 可选链（?.）是 ES2020 语法，ES6 中不可用。
    // 请改为显式检查 null。
    (data.content != null) ? data.content.length() : 0

循环处理
--------

::

    // for...of（ES6）
    for (const item of items) {
        // 对每个元素进行处理
    }

    // forEach（箭头函数）
    items.forEach(item => {
        // 对每个元素进行处理
    });

    // 处理范围时可生成数组或使用 for 循环
    // （JavaScript 没有 Groovy 那样的范围表达式）
    for (let i = 1; i <= 10; i++) {
        // ...
    }

数据存储脚本
============

数据存储设置中的脚本示例。

.. note::
   在数据存储脚本中，每行 ``字段名=表达式`` 均作为独立的单一表达式求值。
   因此，不能使用 ``let`` / ``const`` 变量声明语句，也不能使用一次性设置多个字段的多行控制结构（如 ``if`` 块）。
   使用Java类时，请以完全限定类名（FQCN）写成单一表达式，条件分支则在各字段中使用三元运算符（例如： ``url=data.published ? data.url : null`` ）。
   此外，这里使用的变量名 ``data`` 仅为示例，实际变量名取决于所使用的数据存储连接器。详情请参阅 :doc:`../admin/dataconfig-guide` 。
   表达式请写成不带末尾分号的形式：只能解析为语句块的行其求值结果为 ``null`` ，该字段将不会被设置。请参阅 :ref:`javascript-statement-null` 。

基本映射
--------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL生成
-------

::

    // 基于ID的URL生成
    url="https://example.com/article/" + data.id

    // 组合多个字段
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // 条件URL
    url=data.external_url || "https://example.com/default/" + data.id

内容加工
--------

::

    // 移除HTML标签
    content=data.html_content.replace(/<[^>]+>/g, "")

    // 合并多个字段
    content=data.title + "\n" + data.description + "\n" + data.body

    // 限制长度
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

日期处理
--------

::

    // 解析日期（使用FQCN的单一表达式；Java 互操作与 Groovy 使用相同的写法）
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // 从epoch秒转换（无需 long 类型的 L 后缀）
    lastModified=new Date(data.timestamp * 1000)

可用对象
========

脚本中可用的对象因执行上下文而异。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 上下文
     - 对象
     - 说明
   * - 所有上下文
     - ``container``
     - DI容器。通过 ``container.getComponent("...")`` 访问组件
   * - 计划任务
     - ``executor``
     - 任务执行控制（ ``JobExecutor`` ）。任务停止支持所必需
   * - 数据存储
     - （连接器特定）
     - 各数据存储提供的数据记录变量。变量名取决于连接器
   * - 路径映射
     - ``url`` , ``matcher``
     - 待转换的URL字符串及正则表达式匹配结果（ ``Matcher`` ）。可在替换字符串带有已注册引擎名前缀（如 ``javascript:`` ，别名 ``js:`` 、 ``sai:`` ）时使用
   * - 文档权重
     - （文档字段）
     - 目标文档的各字段均可作为变量使用（用于条件表达式和权重值表达式）

计划任务脚本
============

计划任务中使用的JavaScript脚本示例。
在计划任务中，``container`` 和 ``executor`` 可用。
将 ``executor`` 传递给任务的 ``execute()`` 方法可启用任务停止控制。

.. note::
   计划任务脚本作为一个完整的脚本整体求值。
   脚本引擎会先尝试将其编译为表达式，仅在失败时才重新解释为语句块，因此可以使用多行语句、 ``let`` / ``const`` 声明、控制结构以及顶层的 ``return`` 语句（详见上文"脚本的求值方式"）。
   以下「使用Java类」「访问Fess组件」「错误处理」「调试与日志输出」的示例均基于此完整脚本的上下文。

执行爬取任务
------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

条件爬取
--------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // 仅在非工作时间爬取
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

顺序执行多个任务
----------------

::

    const results = [];

    // 更新建议词
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // 执行爬取
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

使用Java类
==========

在JavaScript脚本中，借助 Sai（Nashorn）的 Java 互操作机制，可以直接使用 Java
标准库和 |Fess| 的类。JavaScript 没有 ``import`` 语句，因此类名始终以完全限定名
（FQCN）书写。

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

日期与时间
----------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

文件操作
--------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/path/to/file.txt")));

HTTP通信
--------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   访问外部资源会影响性能，
   请将其控制在最小限度。

访问Fess组件
============

可以使用 ``container`` 访问Fess的组件。

系统帮助器
----------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

获取配置值
----------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

执行搜索
--------

::

    const searchHelper = container.getComponent("searchHelper");
    // 设置搜索参数并执行搜索

错误处理
========

JavaScript 没有 ``import`` 语句，因此不存在 Groovy 那样的位置限制。
可以使用 ``try-catch`` 捕获异常，控制任务的错误行为。

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

调试与日志输出
==============

日志输出
--------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

调试输出
--------

如需快速查看变量内容，可以使用 ``JSON.stringify`` 将其转换为字符串后输出到日志。

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

从Groovy迁移
============

将现有 Groovy 脚本移植到 JavaScript 时，请注意以下差异。

算术运算的精度
--------------

JavaScript 的数值运算始终以双精度浮点数处理。例如，以下表达式在 Groovy 中返回
整数 ``34`` ，而在 JavaScript 中返回浮点数 ``34.0`` 。

::

    10 * boost1 + boost2

另一方面，通过 Java 互操作调用的方法，其返回值会保留 Java 一侧的类型，因此
``content.length()`` 仍然返回整数。

需要改写的Groovy专用语法
------------------------

以下 Groovy 专用语法在 JavaScript 中需要改写。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - 说明
   * - ``1000L``
     - ``1000``
     - long 类型字面量的 ``L`` 后缀不再需要，直接书写数字字面量即可
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - JavaScript 数组在传递给接受 ``String[]`` 的方法时会自动转换为 Java 数组，
       因此无需强制转换

Java互操作
----------

Java 互操作的写法与 Nashorn 相同，与 Groovy 几乎没有差别。 ``new java.io.File(...)``、
``java.lang.System.getProperty(...)``、 ``new org.codelibs.fess.job.IndexExportJob()``
等完全限定构造函数调用均可直接解析。

ES6语法
-------

由于 |Fess| 的 JavaScript 引擎以 ECMAScript 6 运行，可以使用 ``let`` / ``const``、
箭头函数、模板字符串、解构赋值、``for...of``、``class`` 等 ES6 语法。但可选链
（ ``?.`` ）和空值合并运算符（ ``??`` ）属于 ES2020 及以后的语法，无法使用。

最佳实践
========

1. **保持简单**: 避免复杂逻辑，编写易读的代码
2. **默认值**: 使用逻辑 OR 运算符（ ``||`` ）代替 Elvis 运算符
3. **异常处理**: 使用适当的try-catch处理意外错误
4. **日志输出**: 输出日志以便于调试
5. **性能**: 最小化外部资源访问
6. **数值运算**: 需要整数的场合，直接使用 Java 互操作方法调用的结果，或按需显式转换

参考信息
========

- `MDN JavaScript 参考 <https://developer.mozilla.org/zh-CN/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - 脚本概述
- :doc:`scripting-groovy` - Groovy 脚本指南（插件）
- :doc:`../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../admin/scheduler-guide` - 调度器配置指南
