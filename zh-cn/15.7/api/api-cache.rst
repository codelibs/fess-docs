==========
缓存 API
==========

本文档介绍 |Fess| v2 缓存 API。
公共响应信封、错误模型及 CSRF 相关内容，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

获取缓存文档
============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/cache/{docId}``
==================  ====================================================

返回文档的缓存（已应用高亮）HTML。

当 ``app.login.required=true`` 且调用方为匿名时，返回 ``auth_required``\ （401）。

请求参数
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``docId``
     - 文档标识符（path，必填，格式 ``^[A-Za-z0-9_-]+$``\ ）。
   * - ``hq``
     - 高亮查询词（query）。可重复指定（数组）。

表: 请求参数

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``doc_id``
     - 文档 ID（str）。
   * - ``mimetype``
     - MIME 类型（枚举值：\ ``text/html``\ ）。
   * - ``content``
     - 缓存的 HTML 正文（str）。
   * - ``url``
     - 文档 URL（str）。若存在 ``url_link`` 字段则使用它，否则使用索引中的原始 URL。两者均不存在时省略。
   * - ``created``
     - 索引中文档的创建时间戳（str）。不存在时省略。
   * - ``charset``
     - 从文档 mimetype 解析的字符集（str）。不存在时默认为 ``UTF-8``\ 。

表: 响应字段

错误响应
--------

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求不合法时。
   * - 401 Unauthorized
     - 需要认证时（\ ``app.login.required=true`` 且调用方为匿名）。
   * - 404 Not Found
     - 找不到资源时。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应
