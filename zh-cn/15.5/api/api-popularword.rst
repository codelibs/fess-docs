===========
热门词API
===========

获取热门词列表
===============

请求
--------

==================  ====================================================
HTTP方法             GET
端点                 ``/api/v1/popular-words``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v1/popular-words?seed=123`` 请求，可以获取在 |Fess| 中注册的热门词列表的JSON格式数据。
要使用热门词API，需要在管理界面的"系统 > 常规设置"中启用热门词响应。

请求参数
-----------------

可用的请求参数如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 请求参数

   * - seed
     - 获取热门词的种子（通过该值可以获取不同模式的词）
   * - label
     - 过滤的标签名称
   * - field
     - 生成热门词的字段名称


响应
--------

将返回以下响应：

::

    {
      "record_count": 3,
      "data": [
        "python",
        "java",
        "javascript"
      ]
    }

各元素说明如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 响应信息

   * - record_count
     - 热门词的注册数量
   * - data
     - 热门词数组

错误响应
==============

当热门词API失败时，将返回以下错误响应：

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求参数无效
   * - 500 Internal Server Error
     - 服务器内部错误
