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
当集群状态为 ``green`` / ``yellow`` 时，HTTP 状态码为 200；为 ``red`` 时，HTTP 状态码为 503。

本端点遵守信封不变量"``status >= 1`` ⇔ HTTP 状态码 ``>= 400``"。

- ``green`` / ``yellow`` 时：以成功信封（\ ``status: 0``\ ）返回 ``engine``\ 。
- ``red`` 时：以错误信封（\ ``status: 9``\ ，\ ``error.code: service_unavailable``\ ）返回，并将引擎快照嵌入 ``error.details.engine`` 中（以便监控工具解析集群元数据）。

``engine`` 各字段说明如下。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine 字段

   * - ``cluster_name``
     - 集群名称（str）。
   * - ``status``
     - 集群状态。为 ``green`` / ``yellow`` / ``red`` 之一。
   * - ``ping_status``
     - ping 的状态码（int）。集群为 ``red`` 时值为 ``1``\ ，其他情况（\ ``green`` / ``yellow``\ ）值为 ``0``\ 。

表: engine 字段

请求参数
--------

无可用的请求参数。

响应
----

集群为 ``green`` / ``yellow`` 时（200），以成功信封返回 ``engine``\ 。

::

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess-es",
          "status": "green",
          "ping_status": 0
        }
      }
    }

集群为 ``red`` 时（503），以错误信封返回，引擎快照嵌入在 ``error.details.engine`` 中。

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "cluster_name": "fess-es",
              "status": "red",
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
     - 集群为 ``green`` / ``yellow`` 且可达时。成功信封中包含 ``engine``\ 。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 503 Service Unavailable
     - 集群为 ``red`` 时。错误信封（\ ``error.code: service_unavailable``\ ）中，\ ``error.details.engine`` 包含引擎快照。

表: 响应一览
