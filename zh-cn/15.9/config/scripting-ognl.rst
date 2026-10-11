============
OGNL脚本指南
============

概述
====

OGNL（Object-Graph Navigation Language）是 |Fess| 中可用的脚本引擎之一。
它以 ``fess-script-ognl`` 插件形式提供，标识符为 ``ognl`` 。

OGNL脚本是单个取值表达式，例如 ``title + " - " + siteName`` 或 ``content.length() > 0`` 。
它没有语句、控制结构和 ``return`` 。适用于字段映射、文档提升和路径映射等
只需简短表达式的场景。需要语句或循环的脚本，请使用 :doc:`scripting-javascript` 或 :doc:`scripting-groovy` 。

.. important::
   该插件 **不随发行包分发** 。请从管理界面的「系统 > 插件」页面安装，
   或执行 ``bin/fess-setup install plugin fess-script-ognl`` 。如需手动安装，请将
   JAR 文件（例如 ``fess-script-ognl-15.9.0.jar`` ）放置到 ``app/WEB-INF/plugin/``
   目录下，并重启 |Fess| 。

选择OGNL
========

只有在显式选择了脚本类型的地方才会使用OGNL。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 位置
     - 选择OGNL的方法
   * - 数据存储
     - 在数据存储配置的参数中添加 ``script_type=ognl``
   * - Web爬取、文件爬取
     - 在配置参数中添加 ``config.script.type=ognl`` ，并以 ``field.script.<字段名>=<表达式>``
       的形式编写字段脚本
   * - 文档提升规则
     - 将规则的脚本类型设置为 ``ognl`` （脚本类型按规则分别设置）
   * - 路径映射
     - 让替换字符串以 ``ognl:`` 开头。表达式的结果即为替换后的URL，原始URL和
       ``Matcher`` 可通过 ``url`` 和 ``matcher`` 引用
   * - 计划任务
     - 将任务的脚本类型设置为 ``ognl`` 。任务通常是一段处理流程，无法用单个表达式表达

编写表达式
==========

数据存储和字段脚本每行编写一个 ``字段名=表达式`` 。每个参数既可以用 ``name`` 引用，
也可以用 ``#name`` 引用。

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNL不是Groovy的子集。迁移脚本时请注意以下几点。

- 没有 ``return`` 、语句以及 ``if`` / ``for`` 。请使用三元运算符 ``cond ? a : b`` 。
- 不支持Elvis运算符 ``?:`` 和安全导航运算符 ``?.`` 。请写成 ``a != null ? a.b : null`` 。
- ``"x${id}"`` 不会报错，也不会被展开。它会作为字面字符串 ``x${id}`` 求值，
  因此字段会被索引为错误的文本。拼接请使用 ``+`` 。

设置
====

引擎从 ``system.properties`` 或JVM系统属性 ``-Dfess.system.<键>`` 读取以下键。
两者都有时， ``system.properties`` 优先。 ``system.properties`` 在ZIP版中是
``app/WEB-INF/conf/system.properties`` ，在RPM版和DEB版中是 ``/etc/fess/system.properties`` 。

.. important::
   这些键只在启动时引擎初始化时读取一次。
   修改后请重启 |Fess| ，正在运行的进程不会应用修改。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - 键
     - 默认值
     - 说明
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` 或 ``strict`` 。请参阅下一节。其他值会在日志中输出警告，并按 ``compat`` 处理
   * - ``script.ognl.allowed.classes``
     - 见下文
     - 允许使用的类的逗号分隔列表。仅在 ``strict`` 模式下使用
   * - ``script.ognl.denied.packages``
     - 见下文
     - 拒绝调用的声明类的逗号分隔列表。仅在 ``strict`` 模式下使用
   * - ``script.ognl.cache.size``
     - ``1000``
     - 缓存已解析表达式的最大数量。最小值为 ``1``
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - 表达式的最大字符数。更长的表达式不会被求值，而是失败。最小值为 ``1``
   * - ``script.ognl.max.log.length``
     - ``200``
     - 写入日志消息的表达式的最大字符数。最小值为 ``3``

不是整数的值会被忽略并输出警告，改用默认值。小于最小值的值会被提升到最小值，并输出警告。

compat模式和strict模式
======================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` （默认）
     - ``strict``
   * - DI容器
     - 可通过 ``container`` 引用
     - 不可引用（ ``container`` 求值为 ``null`` ）
   * - 类
     - 可通过 ``@任意类@方法(...)`` 访问任意类
     - 只能访问 ``script.ognl.allowed.classes`` 中的类
   * - 成员
     - 无限制
     - 无法调用由 ``script.ognl.denied.packages`` 中的类声明的成员。
       非public成员始终被拒绝

``compat`` 保持现有配置的行为。在 ``strict`` 模式下，
``@java.lang.System@getProperty("user.name")`` 或 ``new java.io.File("/etc/hosts")``
之类的表达式会被拒绝。被拒绝的表达式不会求值为 ``null`` ，而是在日志中输出警告，并且求值以错误失败。

引擎启动时会以 ``INFO`` 级别在日志中记录生效的模式
（ ``ognl script engine: mode=strict, ...`` ）。请通过这一行确认 ``strict`` 是否已生效。

允许列表
--------

``script.ognl.allowed.classes`` 按完整类名精确匹配，或按包名、类名后加 ``.`` 进行前缀匹配。
例如， ``java.time`` 允许 ``java.time.LocalDate`` 在内的该包下的所有类。默认值如下。

``java.lang.Math`` 、 ``java.lang.String`` 、 ``java.lang.Boolean`` 、 ``java.lang.Integer`` 、
``java.lang.Long`` 、 ``java.lang.Float`` 、 ``java.lang.Double`` 、 ``java.lang.Number`` 、
``java.util.Date`` 、 ``java.util.Arrays`` 、 ``java.util.List`` 、 ``java.util.Map`` 、
``java.util.Set`` 、 ``java.util.Collections`` 、 ``java.math.BigDecimal`` 、 ``java.time`` 、
``org.codelibs.core.lang.StringUtil`` 、 ``org.codelibs.fess.util.DocumentUtil`` 、
``org.codelibs.fess.taglib.FessFunctions``

嵌套类的名称包含 ``$`` （例如 ``java.util.Map$Entry`` ），不会因外部类的名称而被允许。
如有需要，请将包含 ``$`` 的名称添加到列表中。

拒绝列表
--------

当声明成员的类的名称以其中任一项开头时， ``script.ognl.denied.packages`` 会拒绝该成员。
默认值如下。

``java.io`` 、 ``java.nio`` 、 ``java.net`` 、 ``java.lang.reflect`` 、 ``java.lang.invoke`` 、
``java.lang.System`` 、 ``java.lang.Class`` 、 ``java.lang.Runtime`` 、 ``java.lang.ProcessBuilder`` 、
``java.lang.Process`` 、 ``java.lang.Thread`` 、 ``java.lang.ClassLoader`` 、 ``javax.script`` 、
``jdk.`` 、 ``sun.`` 、 ``org.lastaflute.di``

.. note::
   设置的值会替换默认列表，而不是追加到默认列表中。要向允许列表中添加一个类，请同时写出默认项和新增项。

.. warning::
   ``strict`` 模式限制的是表达式能够访问的类和成员，并不会把表达式与传给它的对象隔离开。
   如果将 |Fess| 的辅助对象或实体作为参数传入，则在两种模式下，表达式都可以调用其public方法。
