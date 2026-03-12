==================================
脚本概述
==================================

概述
====

在 |Fess| 中，可以使用脚本在各种场景中实现自定义逻辑。
通过活用脚本，可以灵活控制爬取时的数据处理、搜索结果定制、
计划任务执行等。

支持的脚本语言
==================

|Fess| 支持以下脚本语言:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 语言
     - 标识符
     - 说明
   * - Groovy
     - ``groovy``
     - 默认脚本语言。与Java兼容，提供强大功能
   * - JavaScript
     - ``javascript``
     - Web开发者熟悉的语言

.. note::
   Groovy使用最广泛，本文档中的示例以Groovy编写。

脚本使用场景
====================

数据存储设置
----------------

在数据存储连接器中，使用脚本将获取的数据映射到索引字段。

::

    url="https://example.com/article/" + data.id
    title=data.name
    content=data.description
    lastModified=data.updated_at

路径映射
--------------

可以使用脚本进行URL规范化或路径转换。

::

    # 转换URL
    url.replaceAll("http://", "https://")

计划任务
------------------

在计划任务中，可以使用Groovy脚本编写自定义处理逻辑。

::

    return container.getComponent("crawlJob").execute();

基本语法
============

变量访问
------------

::

    # 访问数据存储的数据
    data.fieldName

    # 访问系统组件
    container.getComponent("componentName")

字符串操作
----------

::

    # 连接
    title + " - " + category

    # 替换
    content.replaceAll("old", "new")

    # 分割
    tags.split(",")

条件分支
--------

::

    # 三元运算符
    data.status == "active" ? "有效" : "无效"

    # null检查
    data.description ?: "无描述"

日期操作
--------

::

    # 当前日期时间
    new Date()

    # 格式化
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(data.date)

可用对象
======================

脚本中可使用的主要对象:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 对象
     - 说明
   * - ``data``
     - 从数据存储获取的数据
   * - ``container``
     - DI容器（访问组件）
   * - ``systemHelper``
     - 系统帮助器
   * - ``fessConfig``
     - |Fess| 的配置

安全性
============

.. warning::
   脚本具有强大功能，请仅使用来自可信来源的脚本。

- 脚本在服务器上执行
- 可以访问文件系统和网络
- 请确保只有具有管理员权限的用户才能编辑脚本

性能
==============

优化脚本性能的提示:

1. **避免复杂处理**: 脚本会为每个文档执行
2. **最小化外部资源访问**: 网络调用会导致延迟
3. **利用缓存**: 考虑缓存重复使用的值

调试
========

使用日志输出进行脚本调试:

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")
    logger.info("data.id = {}", data.id)

日志级别设置:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="script" level="DEBUG"/>

参考信息
========

- :doc:`scripting-groovy` - Groovy脚本指南
- :doc:`../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../admin/scheduler-guide` - 调度器配置指南
