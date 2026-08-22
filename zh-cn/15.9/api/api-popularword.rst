===========
热门词 API
===========

获取热门词列表
==============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/popular-words``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v2/popular-words?seed=123`` 等形式的请求，可以获取热门搜索词列表（JSON 格式）。

若 ``web.api.popularword=false``\ ，则此 API 返回 ``invalid_request``\ （HTTP 400）（相当于 v1 中"unsupported operation"的行为）。

有关公共响应信封及错误模型，请参阅 :doc:`api-overview`。

请求参数
--------

可用的请求参数如下。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 请求参数

   * - seed
     - 获取热门词的种子（字符串）。通过该值可以获取不同模式的词。（例）\ ``seed=123``
   * - label
     - 过滤的标签名。可重复指定，以数组形式处理。（例）\ ``label=java``
   * - field
     - 生成热门词的字段名。可重复指定，以数组形式处理。（例）\ ``field=label``

响应
----

成功时，返回如下公共信封格式的响应。

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应信息

   * - record_count
     - 热门词的数量（整数）。
   * - popular_words
     - 热门词的数组（字符串数组）。

.. note::

   在 v2 中，热门词以 ``popular_words``\ （字符串数组）返回（而非 v1 的 ``data``\ ）。

使用示例
========

使用 curl 命令的请求示例：

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

错误响应
========

热门词 API 失败时，将返回公共错误信封。错误模型详情请参阅 :doc:`api-overview`。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求不合法时（包括 ``web.api.popularword=false`` 导致功能禁用的情形）。\ ``error.code`` 为 ``invalid_request``\ 。
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。
