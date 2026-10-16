==========
Health API
==========

本文档介绍 |Fess| v2 Health API。
公共响应信封及错误模型，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

获取状态
========

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/health``
==================  ====================================================

返回搜索引擎集群的状态快照（\ ``monitor`` 标签）。
当集群状态为 ``GREEN`` / ``YELLOW`` 时，HTTP 状态码为 200；为 ``RED`` 或无法连接搜索引擎时，HTTP 状态码为 503。

本端点遵守信封不变量"``status >= 1`` ⇔ HTTP 状态码 ``>= 400``"。

- ``GREEN`` / ``YELLOW`` 时：以成功信封（\ ``status: 0``\ ）返回 ``engine``\ 。
- ``RED`` 时：以错误信封（\ ``status: 9``\ ，\ ``error.code: service_unavailable``\ ）返回，并将引擎快照嵌入 ``error.details.engine`` 中（以便监控工具解析集群元数据）。
- 无法连接搜索引擎时：与 ``RED`` 一样以错误信封（\ ``error.code: service_unavailable``\ ，\ ``error.message: search engine is not reachable``\ ）返回，\ ``error.details.engine`` 中为 ``status: UNAVAILABLE``\ 、\ ``ping_status: 1``\ 。

``engine`` 各字段说明如下。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine 字段

   * - ``status``
     - 集群状态。为大写的 ``GREEN`` / ``YELLOW`` / ``RED`` 之一。无法连接搜索引擎时为 ``UNAVAILABLE``\ 。
   * - ``ping_status``
     - ping 的状态码（int）。集群为 ``RED`` 或无法连接搜索引擎时值为 ``1``\ ，其他情况（\ ``GREEN`` / ``YELLOW``\ ）值为 ``0``\ 。

表: engine 字段

由于该端点无需认证即可调用，因此不会返回集群名称（\ ``cluster_name``\ ）。

请求参数
--------

无可用的请求参数。

响应
----

集群为 ``GREEN`` / ``YELLOW`` 时（200），以成功信封返回 ``engine``\ 。

::

    {
      "response": {
        "status": 0,
        "engine": {
          "status": "GREEN",
          "ping_status": 0
        }
      }
    }

集群为 ``RED`` 时（503），以错误信封返回，引擎快照嵌入在 ``error.details.engine`` 中。

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "status": "RED",
              "ping_status": 1
            }
          }
        }
      }
    }

使用示例
========

使用 curl 命令的请求示例：

::

    curl "http://localhost:8080/api/v2/health"

响应与错误响应
==============

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应一览

   * - 状态码
     - 说明
   * - 200 OK
     - 集群为 ``GREEN`` / ``YELLOW`` 且可达时。成功信封中包含 ``engine``\ 。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 503 Service Unavailable
     - 集群为 ``RED`` 或无法连接搜索引擎时。错误信封（\ ``error.code: service_unavailable``\ ）中，\ ``error.details.engine`` 包含引擎快照。

表: 响应一览
