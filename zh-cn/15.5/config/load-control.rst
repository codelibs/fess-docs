==================================
负载控制配置
==================================

概述
====

|Fess| 具有基于OpenSearch CPU使用率控制请求的负载控制功能。
通过此功能，可以在搜索引擎高负载时自动限制请求，保护系统稳定性。

负载控制的特点:

- 实时监控OpenSearch集群的CPU使用率
- 可为Web请求和API请求设置独立的阈值
- 超过阈值时返回HTTP 429 (Too Many Requests)
- 管理界面、登录和静态资源不受控制
- 默认禁用（阈值=100）

配置
====

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
     - 搜索API / AI模式API
     - Web请求 / API请求

结合两种功能可以实现更健壮的系统保护。

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

参考信息
========

- :doc:`rate-limiting` - 速率限制配置
