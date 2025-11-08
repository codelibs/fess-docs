============
内存配置
============

概述
====

Java 应用程序需要为每个进程设置使用的最大堆内存。
|Fess| 需要分别为以下3个组件进行内存配置。

- Fess Web 应用程序
- 爬虫进程
- OpenSearch

通过适当的内存配置,可以实现性能提升和稳定运行。

Fess Web 应用程序的内存配置
======================================

需要配置的情况
----------------

在以下情况下,请考虑调整内存大小。

- ``fess.log`` 中记录了 OutOfMemory 错误
- 需要处理大量并发访问
- 管理页面操作缓慢或超时

默认内存大小对于一般使用已经足够,但在高负载环境下需要增加。

环境变量配置
------------------

设置环境变量 ``FESS_HEAP_SIZE``。

::

    export FESS_HEAP_SIZE=2g

单位:

- ``m``: 兆字节
- ``g``: 吉字节

RPM/DEB 软件包配置
------------------------

使用 RPM 软件包安装时,请编辑 ``/etc/sysconfig/fess``。

::

    FESS_HEAP_SIZE=2g

使用 DEB 软件包时,请编辑 ``/etc/default/fess``。

::

    FESS_HEAP_SIZE=2g

.. warning::
   变更内存大小后,需要重启 |Fess| 服务。

推荐内存大小
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 环境
     - 推荐堆大小
     - 备注
   * - 开发/测试环境
     - 512m〜1g
     - 小规模索引
   * - 小规模生产环境
     - 1g〜2g
     - 数万〜数十万文档
   * - 中规模生产环境
     - 2g〜4g
     - 数十万〜数百万文档
   * - 大规模生产环境
     - 4g〜8g
     - 数百万以上文档

爬虫的内存配置
======================

需要配置的情况
----------------

在以下情况下,需要增加爬虫的内存大小。

- 增加并行爬取数量时
- 爬取大型文件时
- 爬取执行中发生 OutOfMemory 错误时

配置方法
--------

编辑 ``app/WEB-INF/classes/fess_config.properties`` 或 ``/etc/fess/fess_config.properties``。

::

    jvm.crawler.options=-Xmx512m

例如,要变更为 1GB:

::

    jvm.crawler.options=-Xmx1g

.. note::
   此配置按爬虫进程单位(调度器的任务单位)应用。
   同时执行多个爬取任务时,每个任务都会使用指定的内存。

推荐配置
--------

- **常规Web爬取**: 512m〜1g
- **大量并行爬取**: 1g〜2g
- **大型文件爬取**: 2g〜4g

详细 JVM 选项
------------------

爬虫的详细 JVM 选项可以通过 ``jvm.crawler.options`` 配置。
默认配置包含以下优化。

**主要选项:**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 选项
     - 说明
   * - ``-Xms128m -Xmx512m``
     - 初始堆大小和最大堆大小
   * - ``-XX:MaxMetaspaceSize=128m``
     - Metaspace 的最大大小
   * - ``-XX:+UseG1GC``
     - 使用 G1 垃圾收集器
   * - ``-XX:MaxGCPauseMillis=60000``
     - GC 停止时间目标值(60秒)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - 禁用 OutOfMemory 时的堆转储

OpenSearch 的内存配置
=======================

重要注意事项
--------------

OpenSearch 配置内存时需要考虑以下两点。

1. **Java堆内存**: OpenSearch 进程使用
2. **OS文件系统缓存**: 对搜索性能很重要

.. warning::
   Java堆内存过大会导致 OS 文件系统缓存
   可用内存减少,从而降低搜索性能。

配置方法
--------

Linux 环境
~~~~~~~~~

OpenSearch 的堆内存通过环境变量或 OpenSearch 配置文件指定。

通过环境变量配置:

::

    export OPENSEARCH_HEAP_SIZE=2g

或者,编辑 ``config/jvm.options``:

::

    -Xms2g
    -Xmx2g

.. note::
   推荐将最小堆大小(``-Xms``)和最大堆大小(``-Xmx``)设置为相同的值。

Windows 环境
~~~~~~~~~~~

编辑 ``config\jvm.options`` 文件。

::

    -Xms2g
    -Xmx2g

推荐内存大小
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 索引大小
     - 推荐堆大小
     - 推荐总内存
   * - 〜10GB
     - 2g
     - 4GB以上
   * - 10GB〜50GB
     - 4g
     - 8GB以上
   * - 50GB〜100GB
     - 8g
     - 16GB以上
   * - 100GB以上
     - 16g〜31g
     - 32GB以上

.. warning::
   OpenSearch 的堆内存请不要超过 32GB。
   超过 32GB 会禁用 Compressed OOP,导致内存效率降低。

最佳实践
------------------

1. **将物理内存的50%分配给堆**

   将服务器物理内存的约50%分配给 OpenSearch 的堆。
   其余用于 OS 和文件系统缓存。

2. **最大31GB**

   堆大小最大设为 31GB,如需更多内存请增加节点数。

3. **生产环境确认**

   请参考 OpenSearch 官方文档,根据环境进行最优配置。

建议/缩略图处理的内存配置
======================================

建议生成进程
----------------------

建议生成处理的内存配置通过 ``jvm.suggest.options`` 设置。

::

    jvm.suggest.options=-Xmx256m

默认使用以下配置:

- 初始堆: 128MB
- 最大堆: 256MB
- Metaspace最大: 128MB

缩略图生成进程
----------------------

缩略图生成处理的内存配置通过 ``jvm.thumbnail.options`` 设置。

::

    jvm.thumbnail.options=-Xmx256m

默认使用以下配置:

- 初始堆: 128MB
- 最大堆: 256MB
- Metaspace最大: 128MB

.. note::
   处理大型图片的缩略图生成时,需要增加内存。

内存监控与调优
========================

内存使用情况确认
--------------------

Fess 的内存使用情况
~~~~~~~~~~~~~~~~~~~~~

可以在管理页面的"系统信息"中确认。

或者,使用 JVM 监控工具:

::

    jps -l  # 确认Fess进程
    jstat -gcutil <PID> 1000  # 每秒显示GC统计

OpenSearch 的内存使用情况
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X GET "localhost:9201/_nodes/stats/jvm?pretty"
    curl -X GET "localhost:9201/_cat/nodes?v&h=heap.percent,ram.percent"

内存不足的征兆
----------------

出现以下症状时,可能存在内存不足。

**Fess Web 应用程序:**

- 响应缓慢
- 日志中记录了 ``OutOfMemoryError``
- 进程意外终止

**爬虫:**

- 爬取中途停止
- ``fess_crawler.log`` 中记录了 ``OutOfMemoryError``
- 大型文件爬取失败

**OpenSearch:**

- 搜索缓慢
- 索引创建缓慢
- 发生 ``circuit_breaker_exception`` 错误

调优步骤
----------------

1. **确认当前内存使用情况**

   监控各组件的内存使用情况。

2. **识别瓶颈**

   确定哪个组件内存不足。

3. **逐步增加**

   不要一次大幅增加,而是每次增加25-50%并确认效果。

4. **考虑系统整体平衡**

   确保各组件的总内存不超过物理内存。

5. **持续监控**

   持续监控内存使用情况,根据需要进行调整。

内存泄漏对策
----------------

怀疑内存泄漏时:

1. **获取堆转储**

::

    jmap -dump:format=b,file=heap.bin <PID>

2. **堆转储分析**

   使用 Eclipse Memory Analyzer (MAT) 等工具进行分析。

3. **问题报告**

   发现内存泄漏时,请在 GitHub Issues 中报告。

故障排除
======================

发生 OutOfMemoryError
---------------------------

**Fess Web 应用程序:**

1. 增加 ``FESS_HEAP_SIZE``。
2. 限制并发访问数。
3. 降低日志级别,减少日志输出的内存使用。

**爬虫:**

1. 增加 ``jvm.crawler.options`` 中的 ``-Xmx``。
2. 减少并行爬取数量。
3. 调整爬取配置以排除大型文件。

**OpenSearch:**

1. 增加堆大小(最大31GB)。
2. 重新评估索引的分片数。
3. 检查查询的复杂度。

GC 停止时间过长
----------------------

1. 调整 G1GC 配置。
2. 适当设置堆大小(过大或过小都会导致GC频繁)。
3. 考虑更新到更新的 Java 版本。

配置内存后性能仍未改善
------------------------------

1. 检查 CPU、磁盘 I/O、网络等其他资源。
2. 优化索引。
3. 重新评估查询和爬取配置。

参考信息
========

- :doc:`setup-port-network` - 端口与网络配置
- :doc:`crawler-advanced` - 爬虫高级配置
- :doc:`admin-logging` - 日志配置
- `OpenSearch Memory Settings <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/#important-settings>`_
- `Java GC Tuning <https://docs.oracle.com/en/java/javase/11/gctuning/>`_
