==============
收藏 API
==============

本文档介绍 |Fess| v2 收藏 API。
公共响应信封、错误模型及 CSRF 相关内容，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

.. note::

   要使用收藏功能，需要启用 ``user.favorite`` 配置（默认禁用）。

获取收藏文档列表
================

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/favorites``
==================  ====================================================

在由 ``query_id`` 标识的搜索结果中，返回调用用户过去收藏过的文档 ID。
``query_id`` 是搜索 API（\ ``/search``\ ）返回的不透明标识符（\ ``query_id`` 字段）。

匿名调用方（会话中无关联的用户代码）会返回 ``auth_required``\ （401）。
``user.favorite`` 功能未启用时，返回 ``invalid_request``\ （400）。
``query_id`` 与会话内缓存的结果集不匹配时，返回 ``200`` 和空的 ``data`` 数组。

请求参数
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``query_id``
     - 搜索 API（\ ``/search``\ ）返回的不透明 ``query_id``\ （query，必填，str）。

表: 请求参数

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "data": [
          { "doc_id": "a1b2c3d4e5f6" },
          { "doc_id": "f6e5d4c3b2a1" }
        ]
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``record_count``
     - ``data`` 中收藏文档的数量（int）。
   * - ``data``
     - 按搜索结果顺序返回查询目标结果集中收藏文档的数组。每个元素为 ``{doc_id}``\ 。

表: 响应字段

错误响应
--------

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求不合法时（包括 ``user.favorite`` 功能未启用的情形）。
   * - 401 Unauthorized
     - 需要认证时（匿名调用方）。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应

获取收藏状态
============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

获取指定文档的收藏状态。

匿名（未认证）的调用方同样可以使用本端点。此时，\ ``favorite`` 返回 ``false``\ ，但 ``count`` 仍会反映已保存的收藏数量（因此，本端点不会返回 ``401``\ ）。

收藏功能（\ ``user.favorite``\ ）未启用时，端点返回 ``invalid_request``\ （400）。

请求参数
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``docId``
     - 文档标识符（path，必填，格式 ``^[A-Za-z0-9_-]+$``\ ）。

表: 请求参数

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "favorite": true,
        "count": 5
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``doc_id``
     - 文档 ID（str）。
   * - ``favorite``
     - 是否为调用用户的收藏（bool）。
   * - ``count``
     - 该文档的收藏数量（int64）。

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
   * - 404 Not Found
     - 找不到资源时。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应

添加收藏
========

请求
----

==================  ====================================================
HTTP 方法            POST
端点                 ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

将指定文档添加至收藏。
由于是修改状态的请求，需要携带 ``X-Fess-CSRF-Token`` 头（参见 :doc:`api-overview`）。此外，调用用户必须已完成认证；匿名调用方会收到 ``auth_required``\ （401）。

``query_id`` 用于确认目标文档属于近期的某次搜索结果。当 ``query_id`` 与会话中缓存的结果集不匹配时，端点返回 ``invalid_request``\ （400）；当 ``docId`` 不包含在该结果集中时，返回 ``not_found``\ （404）。

请求参数
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``docId``
     - 文档标识符（path，必填，格式 ``^[A-Za-z0-9_-]+$``\ ）。

表: 请求参数

请求体
------

以 ``Content-Type: application/json``\ （字符集 UTF-8）发送包含以下字段的 JSON（FavoritePostRequest）。请求体的最大大小为 1 KiB（1024 字节），超过此限制将返回 ``payload_too_large``\ （413）。

::

    {
      "query_id": "f8b1c2d3e4a5"
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求体

   * - ``query_id``
     - 搜索 API（\ ``/search``\ ）返回的不透明 ``query_id``\ （str，必填）。

表: 请求体

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "ok": true,
        "favorite": true,
        "count": 6
      }
    }

各字段说明如下。上述示例为新注册时的响应；若收藏之前已存在（幂等的重复 POST），响应中还会附带 ``already_existed`` 字段（值为 ``true``\ ）。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``doc_id``
     - 文档 ID（str）。
   * - ``ok``
     - 始终为 ``true``\ （bool）。
   * - ``favorite``
     - 始终为 ``true``\ （bool）。无论是新添加还是已存在，文档均已成为调用用户的收藏。
   * - ``count``
     - 操作后当前的收藏数量（int64）。新添加时为操作前计数加 1（乐观计数），幂等的重复 POST 时反映已保存的计数。
   * - ``already_existed``
     - 收藏之前已存在时为 ``true``\ （bool，幂等的重复 POST）。第一次新添加收藏的 POST 中不存在此字段。

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
     - 需要认证时。
   * - 403 Forbidden
     - 因 CSRF 令牌缺失或过期等原因被拒绝时。
   * - 404 Not Found
     - 找不到资源时。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 413 Payload Too Large
     - 请求体超过大小限制时。
   * - 415 Unsupported Media Type
     - 不支持的 ``Content-Type`` 时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应
