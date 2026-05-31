========
标签 API
========

本文档介绍 |Fess| v2 标签 API。
公共响应信封及错误模型，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

获取标签
========

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/labels``
==================  ====================================================

以公共信封格式获取 |Fess| 中已注册的标签列表。

请求参数
--------

无可用的请求参数。

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
          {
            "label": "AWS",
            "value": "aws"
          },
          {
            "label": "Azure",
            "value": "azure"
          }
        ]
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 响应字段

   * - ``record_count``
     - 标签的注册数量（integer）。
   * - ``labels``
     - 标签的数组。
   * - ``label``
     - 标签的名称。
   * - ``value``
     - 标签的值。

表: 响应字段

使用示例
========

使用 curl 命令的请求示例：

::

    curl "http://localhost:8080/api/v2/labels"

错误响应
========

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应
