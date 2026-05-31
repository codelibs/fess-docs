============================
相关查询与相关内容 API
============================

本页介绍用于获取查询相关信息的两个端点。

- ``GET /related-queries`` — 获取针对查询的相关查询候选。
- ``GET /related-content`` — 获取针对查询的相关 HTML 内容。

有关公共响应信封及错误模型，请参阅 :doc:`api-overview`。

获取相关查询
============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/related-queries``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v2/related-queries?q=fess`` 等形式的请求，可以获取针对指定查询的相关查询词列表（JSON 格式）。

即使 ``q`` 为空或未指定，也不会报错，而是返回空的 ``queries`` 数组。响应始终为成功信封。

请求参数
--------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 请求参数

   * - q
     - 用于获取相关查询的搜索词。（例）\ ``q=fess``

响应
----

成功时，返回如下公共信封格式的响应。

::

    {
      "response": {
        "status": 0,
        "queries": [
          "fess search",
          "fess install"
        ]
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应信息

   * - queries
     - 相关查询词的数组（字符串数组）。\ ``q`` 为空或未指定时，返回空数组。

错误响应
~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

获取相关内容
============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/related-content``
==================  ====================================================

向 |Fess| 发送 ``http://<Server Name>/api/v2/related-content?q=fess`` 等形式的请求，可以获取针对指定查询的相关 HTML 内容（JSON 格式）。

当多个内容项匹配时，将以换行符连接。
即使 ``q`` 为空或未指定，也不会报错，而是返回空字符串的 ``content``\ 。响应始终为成功信封。

请求参数
--------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 请求参数

   * - q
     - 用于获取相关内容的搜索词。（例）\ ``q=fess``

响应
----

成功时，返回如下公共信封格式的响应。

::

    {
      "response": {
        "status": 0,
        "content": "<div>...相关 HTML 内容...</div>",
        "content_type": "html"
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应信息

   * - content
     - 相关 HTML 内容（字符串）。多个项目匹配时以换行符连接。\ ``q`` 为空或未指定时，返回空字符串。
   * - content_type
     - 内容类型。值始终为 ``html``\ 。

错误响应
~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。
