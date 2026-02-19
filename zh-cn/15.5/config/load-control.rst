==================================
负载控制配置
==================================

概述
====

|Fess| 具有两种基于CPU使用率保护系统稳定性的负载控制功能。

**HTTP请求负载控制** (``web.load.control`` / ``api.load.control``):

- 实时监控OpenSearch集群的CPU使用率
- 可为Web请求和API请求设置独立的阈值
- 超过阈值时返回HTTP 429 (Too Many Requests)
- 管理界面、登录和静态资源不受控制
- 默认禁用（阈值=100）

**自适应负载控制** (``adaptive.load.control``):

- 监控Fess服务器自身的系统CPU使用率
- 自动限制爬取、索引、建议更新、缩略图生成等后台任务
- 当CPU使用率达到或超过阈值时，处理线程暂停等待，低于阈值后自动恢复
- 默认启用（阈值=50）

HTTP请求负载控制配置
====================

在 ``fess_config.properties`` 中设置以下属性:

::

    # Web请求的CPU使用率阈值（%）
    # CPU使用率达到或超过此值时拒绝请求
    # 设置为100则禁用（默认: 100）
    web.load.control=100

    # API请求的CPU使用率阈值（%）
    # CPU使用率达到或超过此值时拒绝请求
    # 设置为100则禁用（默认: 100）
    api.load.control=100

    # CPU使用率监控间隔（秒）
    # 获取OpenSearch集群CPU使用率的间隔
    # 默认: 1
    load.control.monitor.interval=1

.. note::
   当 ``web.load.control`` 和 ``api.load.control`` 均设置为100（默认）时，
   负载控制功能完全禁用，监控也不会启动。

工作原理
========

监控机制
--------

当负载控制启用时（任一阈值低于100），LoadControlMonitorTarget会定期监控OpenSearch集群的CPU使用率。

- 从OpenSearch集群的所有节点获取OS统计信息
- 记录所有节点中最高的CPU使用率
- 按 ``load.control.monitor.interval`` 指定的间隔（默认1秒）进行监控
- 监控通过延迟初始化，在首次请求时启动

.. note::
   如果获取监控信息失败，CPU使用率将重置为0。
   连续3次失败后，日志级别从WARNING变更为DEBUG。

请求控制
--------

当请求到达时，LoadControlFilter按以下顺序处理:

1. 检查是否为排除路径（排除则直接通过）
2. 判断请求类型（Web / API）
3. 获取对应的阈值
4. 阈值为100或以上时不进行控制（直接通过）
5. 将当前CPU使用率与阈值进行比较
6. CPU使用率 >= 阈值时，返回HTTP 429

**排除的请求:**

- 以 ``/admin`` 开头的路径（管理界面）
- 以 ``/error`` 开头的路径（错误页面）
- 以 ``/login`` 开头的路径（登录页面）
- 静态资源（``.css``、``.js``、``.png``、``.jpg``、``.gif``、``.ico``、``.svg``、``.woff``、``.woff2``、``.ttf``、``.eot``）

**Web请求的情况:**

- 返回HTTP 429状态码
- 显示错误页面（``busy.jsp``）

**API请求的情况:**

- 返回HTTP 429状态码
- 返回JSON响应:

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

配置示例
========

仅限制Web请求
--------------

仅限制Web搜索请求，不限制API的配置:

::

    # Web: CPU使用率80%及以上时拒绝请求
    web.load.control=80

    # API: 不限制
    api.load.control=100

    # 监控间隔: 1秒
    load.control.monitor.interval=1

同时限制Web和API
-----------------

为Web和API设置不同阈值的示例:

::

    # Web: CPU使用率70%及以上时拒绝请求
    web.load.control=70

    # API: CPU使用率80%及以上时拒绝请求
    api.load.control=80

    # 监控间隔: 2秒
    load.control.monitor.interval=2

.. note::
   将API阈值设置高于Web阈值，可以实现分级控制：
   高负载时先限制Web请求，负载进一步升高时再限制API请求。

与速率限制的区别
================

|Fess| 除负载控制外，还有 :doc:`rate-limiting` 功能。
两者通过不同的方式保护系统。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 项目
     - 速率限制
     - 负载控制
   * - 控制依据
     - 请求数（每单位时间）
     - OpenSearch CPU使用率
   * - 目的
     - 防止过度请求
     - 保护搜索引擎免受高负载
   * - 限制单位
     - 每个IP地址
     - 整个系统
   * - 响应
     - HTTP 429
     - HTTP 429
   * - 适用范围
     - 全部HTTP请求
     - Web请求 / API请求（管理界面等除外）

结合两种功能可以实现更健壮的系统保护。

自适应负载控制
==============

自适应负载控制根据Fess服务器自身的系统CPU使用率，
自动调整后台任务的处理速度。

配置
----

``fess_config.properties``:

::

    # 自适应负载控制的CPU使用率阈值（%）
    # 系统CPU使用率达到或超过此值时，暂停后台任务
    # 设置为0或以下则禁用（默认: 50）
    adaptive.load.control=50

行为
----

- 监控Fess运行所在服务器的系统CPU使用率
- CPU使用率达到或超过阈值时，目标处理线程等待直到CPU使用率降至阈值以下
- CPU使用率降至阈值以下时，处理自动恢复

**目标后台任务:**

- 爬取（Web / 文件系统）
- 索引（文档注册）
- 数据存储处理
- 建议更新
- 缩略图生成
- 备份和恢复

.. note::
   自适应负载控制默认启用（阈值=50）。
   它与HTTP请求负载控制（``web.load.control`` / ``api.load.control``）独立运行。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 项目
     - HTTP请求负载控制
     - 自适应负载控制
   * - 监控目标
     - OpenSearch CPU使用率
     - Fess服务器系统CPU使用率
   * - 控制目标
     - HTTP请求（Web / API）
     - 后台任务
   * - 控制方法
     - 返回HTTP 429拒绝请求
     - 暂时暂停处理线程
   * - 默认
     - 禁用（阈值=100）
     - 启用（阈值=50）

故障排除
========

负载控制未生效
--------------

**原因**: 设置未正确生效

**确认事项**:

1. ``web.load.control`` 或 ``api.load.control`` 是否设置为低于100
2. 配置文件是否正确加载
3. 是否重启了 |Fess|

正常请求被拒绝
--------------

**原因**: 阈值设置过低

**解决方法**:

1. 提高 ``web.load.control`` 或 ``api.load.control`` 的值
2. 调整 ``load.control.monitor.interval`` 以更改监控频率
3. 增强OpenSearch集群的资源

.. warning::
   阈值设置过低可能导致正常负载下请求也被拒绝。
   请先确认OpenSearch集群平时的CPU使用率，再设置适当的阈值。

爬取速度慢
----------

**原因**: 由于自适应负载控制，线程处于等待状态

**确认事项**:

1. 日志中是否出现 ``Cpu Load XX% is greater than YY%``
2. ``adaptive.load.control`` 阈值是否过低

**解决方法**:

1. 提高 ``adaptive.load.control`` 的值（例: 70）
2. 增强Fess服务器的CPU资源
3. 设置为0以禁用自适应负载控制（不推荐）

参考信息
========

- :doc:`rate-limiting` - 速率限制配置
