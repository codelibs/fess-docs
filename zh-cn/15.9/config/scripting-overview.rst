============================
脚本概述
============================

概述
====

在 |Fess| 中，可以使用脚本在各种场景中实现自定义逻辑。
通过活用脚本，可以灵活控制爬取时的数据处理、URL 转换、
计划任务执行等。

支持的脚本语言
==============

|Fess| 支持以下脚本语言：

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 语言
     - 标识符
     - 说明
   * - JavaScript
     - ``javascript`` （别名： ``js`` 、 ``sai`` ）
     - |Fess| 默认内置的脚本语言，也是默认脚本语言（ ``Constants.DEFAULT_SCRIPT`` ）。
       运行于 Sai（CodeLibs 开发的 Nashorn 分支， |Fess| 已将其用于 DI XML 表达式的
       解析）之上，脚本以 ECMAScript 6 执行。
   * - Groovy
     - ``groovy``
     - 以 ``fess-script-groovy`` 插件形式提供。15.9 中随发行包一同分发，因此无需
       额外操作即可使用，但 **自 15.10 起将不再随发行包分发**，需从管理界面安装。

.. note::
   未记录脚本类型的脚本配置将被视为 Groovy。这并非临时的过渡措施，而是永久性行为：
   15.9 之前创建的配置保留其 Groovy 语法脚本、且未记录脚本类型，正是这一默认行为
   使其在升级后仍能保持原样运行。自 15.9 起新建的配置会显式记录脚本类型为
   ``javascript`` 。

   除非另有说明，本文档中的脚本示例均使用 JavaScript 语法编写。关于 Groovy 语法，
   请参阅 :doc:`scripting-groovy` 。

脚本使用场景
============

数据存储设置
------------

在数据存储连接器中，使用脚本将获取的数据映射到索引字段。
配置格式为 ``字段名=表达式``，每行单独记述，
每行作为一个独立的脚本表达式进行求值（默认使用 JavaScript）。

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

数据存储脚本中可引用的变量名因连接器类型而异。
例如，CSV 数据存储和 JSON 数据存储中，各列名、字段名可直接作为变量使用
（不带 ``data`` 之类的公共前缀）。
文件类连接器（Box、Google Drive、OneDrive 等）使用 ``file.*``，
Slack 使用 ``message.*``，不同连接器的前缀各不相同。
可用变量的详细信息，请参阅各数据存储连接器的文档。

.. note::
   数据存储的每行作为一个表达式求值，因此不能使用跨多行的
   ``if`` 块，也不能使用 ``let`` / ``const`` 变量声明语句。
   需要根据条件改变值时，请针对每个字段使用三元运算符
   （例： ``title=enabled === "true" ? name : null`` ）。引用类时
   请以内联方式写出完全限定名（FQCN）。

路径映射
--------

路径映射是用于对爬取目标 URL 进行规范化和转换的功能。
默认情况下，以"正则表达式"与"替换字符串"的组合进行配置，并非脚本。
例如，将正则表达式设为 ``http://``、替换字符串设为 ``https://``，
即可替换 URL 的协议部分。

当替换字符串以 ``（引擎名）:`` 的形式开头时，冒号之前的部分会被解释为要执行的
脚本引擎名称；若与已注册的引擎名匹配，则冒号之后的字符串将由该引擎作为脚本求值。
例如， ``groovy:`` 会选择 Groovy 引擎（需要 ``fess-script-groovy`` 插件），
``javascript:`` （别名 ``js:`` 、 ``sai:`` ）会选择 JavaScript 引擎。若冒号之前
的部分与任何已注册的引擎名都不匹配（例如普通替换字符串中冒号前是 ``https`` 这样
的 URL 协议名），则整个字符串不会被当作脚本处理，而是原样用作普通的正则表达式
替换字符串。当字符串作为脚本求值时，脚本中可使用表示转换目标 URL 字符串的
``url``，以及表示正则表达式 ``java.util.regex.Matcher`` 的 ``matcher`` 。

::

    javascript:url.replace(/http:\/\//g, "https://")

计划任务
--------

在计划任务中，可以使用脚本编写自定义处理逻辑。
整个脚本作为一个脚本求值，因此可以使用多行记述，包括（对于 JavaScript 而言）
``let`` / ``const`` 变量声明和控制结构。

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

在纯 JavaScript 中，顶层的 ``return`` 语句通常会导致语法错误。 |Fess| 的脚本引擎
会先尝试将脚本编译为表达式，只有在失败时才会重新解释为语句块。上例无法编译为
表达式，因此会被编译为语句块并按原样执行。详情请参阅 :doc:`scripting-javascript` 。

``logLevel("info")`` 等方法是任务类（ ``ExecJob`` 及其子类）的
方法，可以链式调用。关于 ``executor`` 变量，
请参阅"执行上下文与可用对象"。

基本语法
========

以下是 JavaScript 的基本语法示例。注释使用 ``//`` （行注释）或
``/* */`` （块注释）。请注意，以 ``#`` 开头的注释在 JavaScript 中
同样不可使用。

变量访问
--------

::

    // 访问数据存储字段（CSV/JSON 中以列名、字段名访问）
    title

    // 从 DI 容器获取组件
    container.getComponent("systemHelper")

字符串操作
----------

::

    // 连接
    title + " - " + category

    // 替换（使用正则表达式；ECMAScript 6 没有 String#replaceAll）
    content.replace(/old/g, "new")

    // 分割
    tags.split(",")

条件分支
--------

::

    // 三元运算符
    status === "active" ? "有效" : "无效"

    // null/空时的默认值（逻辑 OR 运算符；JavaScript 没有 Elvis 运算符）
    description || "无说明"

日期操作
--------

::

    // 当前日期时间
    new Date()

    // 格式化（Java 互操作与 Groovy 使用相同的写法）
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(updated_at)

执行上下文与可用对象
====================

脚本中可使用的对象因执行脚本的上下文而异。
仅 ``container`` 在所有上下文中均可使用。

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 执行上下文
     - 可用对象
     - 说明
   * - 所有上下文
     - ``container``
     - DI 容器。可通过 ``container.getComponent("systemHelper")`` 或
       ``container.getComponent("fessConfig")`` 访问各组件
   * - 数据存储脚本
     - 连接器特有的字段变量
     - 从数据存储获取的各字段可作为变量使用
       （变量名、前缀因连接器而异。CSV/JSON 中字段名直接成为变量名）
   * - 路径映射
     - ``url`` ``matcher``
     - 转换目标 URL 字符串及正则表达式 ``Matcher`` （仅在替换字符串带有 ``（引擎名）:``
       前缀时可用；所带的引擎名，如 ``groovy`` 或 ``javascript``，决定实际执行的语言）
   * - 计划任务
     - ``executor``
     - 任务执行实例（ ``JobExecutor`` ）。用于控制任务的关闭

.. note::
   ``container`` 以外的对象仅在特定上下文中注入。
   例如， ``executor`` 仅在计划任务中可用，在数据存储脚本和
   路径映射中不可使用。

安全性
======

.. warning::
   脚本具有强大功能，请仅使用来自可信来源的脚本。

- 脚本在服务器上执行
- 可访问文件系统和网络
- 请确保只有具有管理员权限的用户才能编辑脚本
- 脚本执行会记录在审计日志（ ``audit.log`` ）中。
  是否记录由 ``script.audit.log.enabled`` 控制，默认值为 ``true`` 。
  记录的脚本字符串的最大长度由 ``script.audit.log.max.length`` 控制，
  默认值为 ``100`` 个字符。

性能
====

优化脚本性能的建议：

1. **避免复杂处理**：数据存储脚本会针对每个文档执行
2. **最小化外部资源访问**：网络调用会导致延迟
3. **利用缓存**：考虑对重复使用的值进行缓存

调试
====

计划任务的脚本会作为一个完整的脚本求值，
因此可以利用日志输出进行调试。
（数据存储脚本中每行作为一个表达式求值，因此不能使用
多行处理。）

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("fess.script");
    logger.info("executor = {}", executor);

上述示例使用名为 ``fess.script`` 的日志记录器。
要输出该日志，需在 ``app/WEB-INF/classes/log4j2.xml`` 中
添加相应的日志记录器配置。

::

    <Logger name="fess.script" level="DEBUG"/>

此外，要启用脚本引擎本身的调试日志，需将 ``org.codelibs.fess.script``
包的日志级别设为 ``DEBUG`` 。

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

参考信息
========

- :doc:`scripting-javascript` - JavaScript 脚本指南
- :doc:`scripting-groovy` - Groovy 脚本指南（插件）
- :doc:`../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../admin/scheduler-guide` - 调度器配置指南
