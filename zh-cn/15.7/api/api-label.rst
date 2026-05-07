========
标签API
========

获取标签
=========

请求
--------

==================  ====================================================
HTTP方法             GET
端点                 ``/api/v1/labels``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v1/labels`` 请求，可以获取在 |Fess| 中注册的标签列表的JSON格式数据。

请求参数
-----------------

无可用的请求参数。


响应
--------

将返回以下响应：

::

    {
      "record_count": 9,
      "data": [
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

各元素说明如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - 标签注册数量。
   * - data
     - 搜索结果的父元素。
   * - label
     - 标签名称。
   * - value
     - 标签值。

表: 响应信息

使用示例
====

使用curl命令的请求示例：

::

    curl "http://localhost:8080/api/v1/labels"

使用JavaScript的请求示例：

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('标签列表:', data.data);
      });

错误响应
==============

当标签API失败时，将返回以下错误响应：

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 500 Internal Server Error
     - 服务器内部错误
