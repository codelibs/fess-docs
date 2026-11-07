============
相似文档 API
============

本文档介绍 |Fess| 的 v2 相似文档 API，用于列出与指定文档内容相同的文档。公共响应信封和错误模型相关内容，请参阅 :doc:`api-overview` 。

基础 URL 为 ``http://<Server Name>/api/v2/`` （本地环境示例： ``http://localhost:8080/api/v2`` ）。

.. note::

   此 API 查找的是副本和内容几乎相同的文档，无法找到仅仅主题相近的文档（参见下文“返回的文档”）。

获取相似文档
============

请求
----

==================  ====================================================
HTTP 方法           GET
端点                ``/api/v2/documents/{docId}/similar``
==================  ====================================================

返回与文档 ``docId`` 具有相同内容签名的文档。客户端可以据此在搜索结果旁提供“相似文档”链接。

- 指定的文档和返回的文档都适用与 ``/api/v2/search`` 相同的角色过滤、虚拟主机过滤和附加查询。不存在的文档和调用方不可见的文档都会返回 ``not_found`` (404)。指定的文档本身以及 URL 相同的其他文档不会被返回。
- 当 ``login.required=true`` 时，未登录的调用方会得到 ``auth_required`` (401)。访问令牌的使用方式与 ``/api/v2/search`` 相同。
- 请求限制为每分钟 ``api.search.similar.rate.limit.per.minute`` （默认： ``30`` ， ``0`` 表示不限制）次，按已登录用户统计，访客按客户端 IP 统计。超过限制时返回 ``429`` 和 ``Retry-After`` 头。
- 只返回一页，按 URL、文档 ID 的顺序排列。没有 ``start`` 或偏移量参数。
- 未确定虚拟主机的请求（默认主机）不会附加虚拟主机过滤器，因此具有虚拟主机值的文档也在对象之内（与 ``/api/v2/search`` 相同）。默认主机的用户不应看到的文档，请用角色加以限制。
- 文档内容发生变化并被重新爬取后，其 ``doc_id`` 会改变。保存下来的 ``doc_id`` 在重新爬取后可能变为 ``not_found`` (404)。

返回的文档
----------

|Fess| 在文档编入索引时计算内容签名（ ``content_minhash_bits`` ）。此 API 返回签名与指定文档相同的文档。分组方式与重复文档报告（ :doc:`../admin/docreport-guide` ）、搜索参数 ``sdh`` 和 ``similar_docs_*`` 字段相同，但无需启用搜索结果折叠即可使用。

- 返回的是副本或内容几乎相同的文档。编辑到签名发生变化的文档不会被返回，因此它并不是查找主题相近文档的功能。
- 当指定的文档没有内容或没有词语时，以及搜索引擎在没有 CodeLibs 插件的情况下运行时（ ``search_engine.type`` 为 ``vanilla`` 、 ``aws`` 或已弃用的 ``cloud`` ，参见 :doc:`../config/search-engine-type` ），不会报错，而是 ``data`` 为空数组。

请求参数
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数
   :widths: 27 73
   :header-rows: 1

   * - 参数
     - 说明
   * - ``docId``
     - 文档标识符（路径，必填，模式 ``[A-Za-z0-9_-]{1,512}`` ）。不匹配的值会产生 ``invalid_request`` (400)。
   * - ``num``
     - 返回的文档数（查询参数，默认 ``10`` ）。超过 ``20`` 与 ``paging.search.page.max.size`` 中较小者的值，会被缩小为该较小值，响应中的 ``page_size`` 会显示结果。 ``0`` 或更小的值会产生 ``invalid_request`` (400)。不是数字的值会被忽略，使用默认值。

表: 请求参数

响应
----

成功时（HTTP 200），在公共信封的 ``response`` 下直接返回以下字段。

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "exec_time": "0.01",
        "query_time": 5,
        "page_size": 10,
        "record_count": 1,
        "record_count_relation": "EQUAL_TO",
        "partial": false,
        "timed_out": false,
        "shard_failed": false,
        "data": [
          {
            "doc_id": "f6e5d4c3b2a1",
            "url": "https://example.com/copy/",
            "title": "Example",
            "content_description": "An example document about Fess."
          }
        ]
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段
   :widths: 27 73
   :header-rows: 1

   * - 字段
     - 说明
   * - ``doc_id``
     - 指定文档的 ID。
   * - ``exec_time``
     - 执行时间（秒），形如 ``"0.01"`` 的小数字符串。
   * - ``query_time``
     - 搜索引擎的查询时间（int64，毫秒）。
   * - ``page_size``
     - 应用上述上限之后所请求的文档数。
   * - ``record_count``
     - 签名相同的文档数量（包括未包含在 ``data`` 中的）。精确数量只统计到 ``query.track.total.hits`` （默认： ``10000`` ）。
   * - ``record_count_relation``
     - 为 ``EQUAL_TO`` 时数量精确；为 ``GREATER_THAN_OR_EQUAL_TO`` 时仅知道下限。
   * - ``partial``
     - 结果是否可能不完整（bool）。与搜索一样，适用查询超时（ ``query.timeout`` ）。
   * - ``timed_out``
     - 是否已达到查询超时（bool）。
   * - ``shard_failed``
     - 是否有一个或多个分片失败（bool）。
   * - ``data``
     - 文档数组（按 URL、文档 ID 的顺序）。每个元素的字段与 ``/api/v2/search`` 的命中项相同（参见 :doc:`api-search` ），也包含 ``tags`` （调用方可见的标签，参见 :doc:`api-tag` ）。由于没有需要高亮的查询，因此 ``content_description`` 是正文摘要，且没有 ``score`` 。

表: 响应字段

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应
   :widths: 25 75
   :header-rows: 1

   * - 状态码
     - 说明
   * - 400 Bad Request
     - ``docId`` 与模式不匹配，或 ``num`` 为 ``0`` 或更小。
   * - 401 Unauthorized
     - 需要认证时（启用了需要登录的设置但调用方未登录，或指定了未注册或已过期的访问令牌）。
   * - 404 Not Found
     - 指定的文档不存在，或调用方不可见（ ``not_found`` ）。
   * - 405 Method Not Allowed
     - 使用了不被允许的 HTTP 方法。
   * - 429 Too Many Requests
     - 超过每分钟的请求数上限。 ``Retry-After`` 头给出需要等待的秒数（ ``60`` ）。
   * - 500 Internal Server Error
     - 发生服务器内部错误。
   * - 503 Service Unavailable
     - 搜索引擎无法受理请求（无法连接，或因容量不足而拒绝）。 ``error.code`` 为 ``service_unavailable`` ， ``Retry-After`` 头给出需要等待的秒数（ ``5`` ）。请求本身没有问题，请稍等后重试。

表: 错误响应
