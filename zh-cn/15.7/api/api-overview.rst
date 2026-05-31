============
API 概述
============


|Fess| 提供的 API
==================

本文档介绍 |Fess| 提供的 Web API（v2）。
通过使用 API，您可以在现有的 Web 系统或单页应用程序（SPA）等中，将 |Fess| 作为搜索服务器使用。

.. note::

   |Fess| 15.7 中，API 已升级为 **v2** 版本。原有的 ``/api/v1`` JSON 搜索 API
   和聊天 API 已废弃，统一整合至 ``/api/v2``\ 。
   使用 ``/api/v1`` 的客户端请迁移至 ``/api/v2``\ 。

基础 URL
========

|Fess| v2 API 端点的基础 URL 如下：

::

    http://<Server Name>/api/v2/

例如，在本地环境中运行时，URL 如下：

::

    http://localhost:8080/api/v2/

响应信封
========

v2 的所有 JSON 响应均以公共信封结构返回。

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` 表示处理结果，沿用了 v1 的规约。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: status 的取值

   * - 0
     - 成功
   * - 1
     - 客户端错误
   * - 9
     - 系统错误

表: status 的取值

注意，\ ``response.status >= 1`` 与 HTTP 状态码 ``400`` 以上始终一致。

字段名
------

包括请求体、响应体及 SSE 事件数据在内，所有 JSON 的键均统一使用 ``snake_case``\ 。

错误响应
========

发生错误时，信封中会附加 ``error`` 对象。

::

    {
      "response": {
        "status": 1,
        "error": {
          "code": "invalid_request",
          "message": "..."
        }
      }
    }

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: error 的元素

   * - code
     - 稳定的错误码（\ ``snake_case``\ ）。建议客户端基于此值进行本地化处理。
   * - message
     - 人类可读的错误消息（英语）。显示时请由客户端根据 ``code`` 进行本地化。

表: error 的元素

错误码与 HTTP 状态码
--------------------

``error.code`` 对应的默认 HTTP 状态码如下。

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: 错误码一览

   * - error.code
     - HTTP 状态码
     - 说明
   * - ``invalid_request``
     - 400
     - 请求不合法。
   * - ``auth_required``
     - 401
     - 需要认证，或认证信息不正确。
   * - ``forbidden``
     - 403
     - 操作不被允许（如缺少或过期的 CSRF 令牌等）。
   * - ``not_found``
     - 404
     - 找不到资源。
   * - ``method_not_allowed``
     - 405
     - 不允许使用该 HTTP 方法。响应的 ``Allow`` 头中会列举支持的方法。
   * - ``not_acceptable``
     - 406
     - 无法接受的请求。
   * - ``conflict``
     - 409
     - 发生了资源冲突。
   * - ``payload_too_large``
     - 413
     - 请求体超过大小限制。
   * - ``unsupported_media_type``
     - 415
     - 不支持的 ``Content-Type``\ （大多数端点要求 ``application/json``\ ）。
   * - ``rate_limited``
     - 429
     - 超过速率限制。\ ``Retry-After`` 头中会指示需要等待的秒数。
   * - ``internal_error``
     - 500
     - 服务器内部发生了错误。
   * - ``service_unavailable``
     - 503
     - 服务暂时不可用。

表: 错误码一览

.. note::

   ``method_not_allowed`` 的响应中，会附带列举了支持 HTTP 方法的
   ``Allow`` 头。

认证与会话
==========

v2 API 采用基于会话的认证方式。
登录通过 ``POST /auth/login`` 完成，成功后将建立会话并颁发 CSRF 令牌。
当前认证状态可通过 ``GET /auth/me`` 查询。详情请参阅 :doc:`api-auth`。

无需登录的搜索等端点可以匿名使用（取决于 ``app.login.required`` 等配置）。

CSRF 令牌
---------

修改状态的请求（\ ``POST`` / ``PUT`` / ``DELETE``\ ）需要携带 ``X-Fess-CSRF-Token`` 头。
CSRF 令牌可通过以下方式获取：

- ``POST /auth/login`` 响应中的 ``csrf_token`` 字段
- ``GET /ui/config`` 响应（当 ``csrf_required=true`` 时的 ``csrf_token`` 字段）

令牌会在每次登录、注销或修改密码时轮换。

.. note::

   CSRF 验证在认证 **之前** 执行。因此，既没有有效会话也没有有效 CSRF 令牌
   的状态变更请求，会收到 ``403 forbidden``\ ，而非 ``401 auth_required``\ 。
   ``/auth/login`` 因为在登录前令牌不存在，所以不在 CSRF 验证范围之内。

流式响应格式
============

部分端点以流式格式（而非普通 JSON）返回响应。

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: 流式响应格式

   * - 端点
     - Content-Type
     - 说明
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events（SSE）。详情请参阅 :doc:`api-chat`。
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON（每行为 ``{"data":{...}}`` 格式的一条文档。仅当流中途失败时，最后一行为 ``{"error":{...}}``\ ）。详情请参阅 :doc:`api-search`。

表: 流式响应格式

API 种类
========

|Fess| 提供以下 v2 API。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - 用于搜索文档、获取标签列表及全量获取（滚动）的 API。
   * - suggest
     - 用于获取建议词的 API。
   * - popularword
     - 用于获取热门词的 API。
   * - related
     - 用于获取相关查询及相关内容的 API。
   * - monitor
     - 用于获取服务器（搜索引擎集群）状态的 API。
   * - auth
     - 用于认证与会话操作（登录、注销、获取认证状态、修改密码）的 API。
   * - ui
     - 用于获取 SPA 所需初始配置（UI 配置）的 API。
   * - favorite
     - 用于操作收藏文档的 API。
   * - click
     - 用于记录搜索结果点击的 API。
   * - cache
     - 用于获取缓存文档正文的 API。
   * - chat
     - 用于使用 AI 搜索模式（RAG 聊天）功能的 API。

表: API 种类
