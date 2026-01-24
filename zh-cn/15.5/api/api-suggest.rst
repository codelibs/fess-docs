===========
建议API
===========

获取建议词列表
====================

请求
--------

==================  ====================================================
HTTP方法             GET
端点                 ``/api/v1/suggest-words``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v1/suggest-words?q=建议词`` 请求，可以获取在 |Fess| 中注册的建议词列表的JSON格式数据。
要使用建议词API，需要在管理界面的"系统 > 常规设置"中启用"文档建议"或"搜索词建议"。

请求参数
-----------------

可用的请求参数如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 请求参数

   * - q
     - 建议关键词。 (示例) ``q=fess``
   * - num
     - 建议词的数量。默认为10。 (示例) ``num=20``
   * - label
     - 过滤的标签名称。 (示例) ``label=java``
   * - fields
     - 限定建议对象的字段名称。默认不限定。 (示例) ``fields=content,title``
   * - lang
     - 搜索语言指定。 (示例) ``lang=en``


响应
--------

将返回以下响应：

::

    {
      "query_time": 18,
      "record_count": 355,
      "page_size": 10,
      "data": [
        {
          "text": "fess",
          "labels": [
            "java",
            "python"
          ]
        }
      ]
    }

各元素说明如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 响应信息

   * - query_time
     - 查询处理时间（单位：毫秒）。
   * - record_count
     - 建议词的注册数量。
   * - page_size
     - 页面大小。
   * - data
     - 搜索结果的父元素。
   * - text
     - 建议词。
   * - labels
     - 标签值数组。

错误响应
==============

当建议API失败时，将返回以下错误响应：

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求参数无效
   * - 500 Internal Server Error
     - 服务器内部错误
