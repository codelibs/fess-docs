===========
建议词 API
===========

获取建议词列表
==============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/suggest-words``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v2/suggest-words?q=fes`` 等形式的请求，可以获取与输入前缀匹配的建议词列表（JSON 格式）。
要使用建议词 API，需要在管理界面的"系统 > 常规设置"中启用"文档建议"或"搜索词建议"。

有关公共响应信封及错误模型，请参阅 :doc:`api-overview`。

请求参数
--------

可用的请求参数如下。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 请求参数

   * - q
     - 用于建议的搜索词（前缀）。（例）\ ``q=fes``
   * - num
     - 建议词的数量（0 以上的整数）。默认值 ``10``\ 。（例）\ ``num=20``
   * - fn
     - 限定建议范围的字段名。可重复指定，以数组形式处理。（例）\ ``fn=content&fn=title``
   * - lang
     - 搜索语言。可重复指定，以数组形式处理。（例）\ ``lang=en``
   * - label
     - 过滤的标签名。可重复指定，以数组形式处理。（例）\ ``label=java``

.. note::

   在 v2 中，指定字段名的参数为 ``fn``\ （而非 v1 的 ``fields``\ ）。
   另外，指定标签的参数为 ``label``\ （与 v1 的 ``labels`` 参数不同）。

响应
----

成功时，返回如下公共信封格式的响应。

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "document",
              "query"
            ]
          }
        ]
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应信息

   * - q
     - 请求的搜索词（字符串）。
   * - page_size
     - 每页条数（整数）。
   * - record_count
     - 建议词的匹配数量（64 位整数）。
   * - query_time
     - 查询处理时间，单位毫秒（64 位整数）。
   * - suggest_words
     - 建议词的数组。每个元素包含 ``text`` 和 ``types``\ 。
   * - text
     - 建议词（字符串）。
   * - types
     - 建议词类型的数组（字符串数组）。

.. note::

   在 v2 中，建议词条目的字段为 ``text`` 和 ``types``\ （而非 v1 的 ``labels``\ ）。

使用示例
========

使用 curl 命令的请求示例：

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

错误响应
========

建议词 API 失败时，将返回公共错误信封。错误模型详情请参阅 :doc:`api-overview`。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。
