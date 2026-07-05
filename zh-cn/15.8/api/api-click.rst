==============
点击日志 API
==============

本文档介绍 |Fess| v2 点击日志 API。
公共响应信封、错误模型及 CSRF 相关内容，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

记录点击
========

请求
----

==================  ====================================================
HTTP 方法            POST
端点                 ``/api/v2/click``
==================  ====================================================

将搜索结果的点击记录到搜索日志。
对于匿名调用方，以及搜索日志功能已禁用的安装环境，会返回成功响应并附带 ``logged: false``\ （不报错）。

由于是修改状态的请求，需要携带 ``X-Fess-CSRF-Token`` 头（参见 :doc:`api-overview`）。

请求体
------

以 ``Content-Type: application/json`` 发送包含以下字段的 JSON（ClickRequest）。

::

    {
      "doc_id": "a1b2c3d4e5f6",
      "query_id": "f8b1c2d3e4a5",
      "rank": 1,
      "rt": 1717142400000
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求体

   * - ``doc_id``
     - 文档 ID（str，必填，格式 ``^[A-Za-z0-9_-]+$``\ ）。标识要记录点击的文档。
   * - ``query_id``
     - 搜索 API（\ ``/search``\ ）返回的 ``query_id``\ （str，可选）。将点击与来源搜索查询相关联。
   * - ``rank``
     - 结果列表中的位置（从 1 开始，int，可选）。
   * - ``rt``
     - 原始搜索请求的 epoch 毫秒（int64，可选）。未指定时，以服务器当前时间为默认值。

表: 请求体

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "ok": true,
        "logged": true
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``ok``
     - 始终为 ``true``\ （bool）。
   * - ``logged``
     - 当搜索日志持久化已禁用或调用方为匿名时为 ``false``\ （bool）。即使如此，也会返回 ``200`` 响应。

表: 响应字段

.. note::

   ``logged: true`` 表示点击已被接受进入搜索日志队列。持久化操作以异步方式执行。

错误响应
--------

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求体不是合法的 JSON，或 ``doc_id`` 缺失或不符合格式要求。
   * - 403 Forbidden
     - 因 CSRF 令牌缺失或过期等原因被拒绝时。
   * - 404 Not Found
     - 未找到与指定 ``doc_id`` 对应的文档。
   * - 405 Method Not Allowed
     - 使用了 ``POST`` 以外的 HTTP 方法（将返回 ``Allow: POST`` 头）。
   * - 413 Payload Too Large
     - 请求体超过大小限制（2 KiB）。
   * - 415 Unsupported Media Type
     - ``Content-Type`` 不是 ``application/json``\ （需使用 UTF-8）。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应
