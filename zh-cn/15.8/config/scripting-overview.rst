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
   * - Groovy
     - ``groovy``
     - 默认注册的脚本语言。与 Java 兼容，提供强大功能

.. note::
   |Fess| 默认注册的脚本引擎仅为 Groovy。
   默认脚本语言为 ``groovy`` （ ``Constants.DEFAULT_SCRIPT`` ）。
   本文档中的脚本示例均使用 Groovy 语法编写。

脚本使用场景
============

数据存储设置
------------

在数据存储连接器中，使用脚本将获取的数据映射到索引字段。
配置格式为 ``字段名=表达式``，每行单独记述，
每行作为一个独立的 Groovy 表达式进行求值。

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
   ``if`` 块、 ``import`` 语句或 ``def`` 变量声明。
   需要根据条件改变值时，请针对每个字段使用三元运算符
   （例： ``title=enabled == "true" ? name : null`` ）。引用类时
   请以内联方式写出完全限定名（FQCN）。

路径映射
--------

路径映射是用于对爬取目标 URL 进行规范化和转换的功能。
默认情况下，以"正则表达式"与"替换字符串"的组合进行配置，并非 Groovy 脚本。
例如，将正则表达式设为 ``http://``、替换字符串设为 ``https://``，
即可替换 URL 的协议部分。

仅当替换字符串以 ``groovy:`` 开头时，后续字符串才会作为 Groovy 脚本求值。
在该脚本中，可使用表示转换目标 URL 字符串的 ``url``，
以及表示正则表达式 ``java.util.regex.Matcher`` 的 ``matcher``\ 。

::

    groovy:url.replaceAll("http://", "https://")

计划任务
--------

在计划任务中，可以使用 Groovy 脚本编写自定义处理逻辑。
整个脚本作为一个 Groovy 脚本求值，因此可以使用多行记述、
``import`` 语句以及 ``def`` 变量声明。

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

``logLevel("info")`` 等方法是任务类（ ``ExecJob`` 及其子类）的
方法，可以链式调用。关于 ``executor`` 变量，
请参阅"执行上下文与可用对象"。

基本语法
========

以下是 Groovy 的基本语法示例。注释使用 ``//`` （行注释）或
``/* */`` （块注释）。请注意，以 ``#`` 开头的注释在 Groovy 中
不可使用。

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

    // 替换
    content.replaceAll("old", "new")

    // 分割
    tags.split(",")

条件分支
--------

::

    // 三元运算符
    status == "active" ? "有效" : "无效"

    // null/空时的默认值（Elvis 运算符）
    description ?: "无说明"

日期操作
--------

::

    // 当前日期时间
    new Date()

    // 格式化
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
     - 转换目标 URL 字符串及正则表达式 ``Matcher``\ （仅在带 ``groovy:`` 前缀的替换时）
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
  是否记录由 ``script.audit.log.enabled`` 控制，默认值为 ``true``\ 。
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

计划任务的脚本会作为一个完整的 Groovy 脚本求值，
因此可以利用日志输出进行调试。
（数据存储脚本中每行作为一个表达式求值，因此不能使用 ``import`` 语句或
多行处理。）

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("fess.script")
    logger.info("executor = {}", executor)

上述示例使用名为 ``fess.script`` 的日志记录器。
要输出该日志，需在 ``app/WEB-INF/classes/log4j2.xml`` 中
添加相应的日志记录器配置。

::

    <Logger name="fess.script" level="DEBUG"/>

此外，要启用脚本引擎本身的调试日志，需将 ``org.codelibs.fess.script``
包的日志级别设为 ``DEBUG``\ 。

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

参考信息
========

- :doc:`scripting-groovy` - Groovy 脚本指南
- :doc:`../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../admin/scheduler-guide` - 调度器配置指南
