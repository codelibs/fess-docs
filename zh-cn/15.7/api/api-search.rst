========
搜索 API
========

本文档介绍 |Fess| v2 搜索 API。
公共响应信封、错误模型及 CSRF 相关内容，请参阅 :doc:`api-overview`。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

搜索文档
========

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/search``
==================  ====================================================

搜索匹配查询的文档，并以公共信封格式返回结果。
载荷中的所有字段名均使用 ``snake_case``\ 。

请求参数
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``q``
     - 搜索词（URL 编码）。
   * - ``start``
     - 从 0 开始的起始位置（integer，\ ``>=0``\ ，默认值 ``0``\ ）。
   * - ``offset``
     - 相对于 ``start`` 的偏移量（integer，\ ``>=0``\ ，默认值 ``0``\ ）。
   * - ``num``
     - 每页条数（integer，\ ``>=1``\ ，默认值 ``20``\ ）。\ ``<= 0`` 会返回 ``invalid_request``\ 。超过配置最大值的数值会被静默截断。是否被截断可通过比较请求中的 ``num`` 与响应中的 ``page_size`` 来判断。
   * - ``sort``
     - 排序方式（例：\ ``score``\ ）。
   * - ``lang``
     - 搜索语言。可重复指定（数组）。例：\ ``en``\ 。
   * - ``ex_q``
     - 附加查询表达式。可重复指定。
   * - ``sdh``
     - 相似文档哈希（similar-document hash）。
   * - ``fields.label``
     - 按标签名过滤。可重复指定。这是通用 ``fields.<name>`` 系列参数中最常用的情形，任意 ``fields.<name>`` 查询参数都会将结果限定为文档字段 ``<name>`` 与指定值匹配的文档。
   * - ``as.*``
     - 高级搜索条件。任意 ``as.<name>``\ （例：\ ``as.q``\ 、\ ``as.filetype``\ ）均会传递给高级搜索条件构建器。每个 name 可重复指定。
   * - ``track_total_hits``
     - 转发给搜索引擎，用于控制精确命中数统计（例：\ ``true`` 或整数阈值）。影响 ``record_count_relation`` 是 ``eq`` 还是 ``gte``\ 。
   * - ``facet.field``
     - 分面字段。可重复指定（数组）。
   * - ``facet.query``
     - 分面查询。可重复指定（数组）。
   * - ``facet.size``
     - 返回的分面词最大数量（integer）。
   * - ``facet.minDocCount``
     - 分面词所包含的最小文档数（integer）。
   * - ``facet.sort``
     - 分面排序方式。
   * - ``facet.missing``
     - 对无值文档的分面处理方式。
   * - ``geo.location.point``
     - 地理坐标中心点（例：\ ``35.0,139.0``\ ）。
   * - ``geo.location.distance``
     - 距中心点的距离（例：\ ``10km``\ ）。

表: 请求参数

响应
----

成功时（200），以下字段会在公共信封的 ``response`` 下直接返回。

::

    {
      "response": {
        "status": 0,
        "q": "Fess",
        "query_id": "f8b1c2d3e4a5",
        "exec_time": 0.012,
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 42,
        "record_count_relation": "eq",
        "page_count": 3,
        "highlight_params": "&hq=Fess",
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "related_query": ["enterprise search"],
        "related_contents": [],
        "data": [
          {
            "doc_id": "a1b2c3d4e5f6",
            "url": "https://example.com/",
            "title": "Example",
            "content_description": "An example document about Fess.",
            "score": 1.2345
          }
        ],
        "facet_field": [
          {
            "name": "label",
            "result": [
              { "value": "news", "count": 12 }
            ]
          }
        ],
        "facet_query": [
          { "value": "filetype:html", "count": 30 }
        ]
      }
    }

各字段说明如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``q``
     - 搜索词（可为 null）。
   * - ``query_id``
     - 查询标识符。
   * - ``exec_time``
     - 执行时间（double，单位秒）。
   * - ``query_time``
     - 搜索引擎查询时间（int64，单位毫秒）。
   * - ``page_size``
     - 每页条数。
   * - ``page_number``
     - 当前页码。
   * - ``record_count``
     - 命中数量（int64）。
   * - ``record_count_relation``
     - ``eq`` 表示精确计数，\ ``gte`` 表示仅知下限。
   * - ``page_count``
     - 总页数。
   * - ``highlight_params``
     - 用于高亮的查询参数字符串。
   * - ``next_page``
     - 是否存在下一页（bool）。
   * - ``prev_page``
     - 是否存在上一页（bool）。
   * - ``start_record_number``
     - 本页起始记录编号。
   * - ``end_record_number``
     - 本页末尾记录编号。
   * - ``page_numbers``
     - 分页器中显示的页码数组（字符串）。
   * - ``partial``
     - 结果是否为部分结果（bool）。
   * - ``search_query``
     - 实际执行的搜索查询。
   * - ``requested_time``
     - 请求时间（int64，epoch 毫秒）。
   * - ``related_query``
     - 相关查询的数组（字符串）。
   * - ``related_contents``
     - 相关内容的数组（字符串）。
   * - ``data``
     - 搜索结果数组，每条文档对应一个元素。仅包含 ``QueryFieldConfig#isApiResponseField`` 允许的字段，null 及空键会被排除。
   * - ``facet_field``
     - 仅在请求了分面字段时存在的数组。每个元素为 ``{name, result:[{value, count}]}``\ 。
   * - ``facet_query``
     - 仅在请求了分面查询时存在的数组。每个元素为 ``{value, count}``\ 。

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
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应

全量文档获取（滚动搜索·NDJSON）
================================

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/documents/all``
==================  ====================================================

以 NDJSON（\ ``application/x-ndjson``\ ）流式传输所有匹配查询的文档。
每行为 ``{"data":{...}}`` 对象，包含 ``QueryFieldConfig#isApiResponseField`` 允许的字段。

当流中途失败时，最后一行会输出并刷新以下内容：

::

    {"error":{"code":"internal_error","message":"stream error"}}

因此，客户端必须检查最后一行的第一个键，以区分正常完成（\ ``data``\ ）还是服务器异常（\ ``error``\ ）。

查询使用与 ``GET /search`` 相同的参数集（\ ``q``\ 、\ ``sort``\ 、\ ``num``\ 、\ ``lang``\ 、\ ``ex_q``\ 、\ ``sdh``\ 、\ ``fields.*``\ 、\ ``as.*``\ 、\ ``track_total_hits``\ 、\ ``facet.*``\ 、\ ``geo.*``\ ）构建。
若 ``api.search.scroll=false`` 禁用了滚动搜索，则返回 ``invalid_request``\ （400）。

请求参数
--------

规范中明确列出的参数如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``q``
     - 搜索词。
   * - ``sort``
     - 排序方式。
   * - ``num``
     - 每页（滚动批次）条数（integer，\ ``>=1``\ ）。\ ``<= 0`` 会返回 ``invalid_request``\ 。
   * - ``lang``
     - 搜索语言。可重复指定（数组）。
   * - ``ex_q``
     - 附加查询表达式。可重复指定（数组）。
   * - ``fields.label``
     - 按标签名过滤。可重复指定（数组）。属于通用 ``fields.<name>`` 系列参数（参见 ``GET /search``\ ）。
   * - ``sdh``
     - 相似文档哈希（similar-document hash）。

表: 请求参数

响应
----

成功时（200），Content-Type 为 ``application/x-ndjson``\ ，每行返回一条文档，格式如下。

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

错误响应
--------

错误模型详情请参阅 :doc:`api-overview`。该端点返回的 HTTP 状态码如下。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 查询不合法、\ ``num <= 0``\ ，或 ``api.search.scroll=false`` 禁用了滚动搜索时。
   * - 405 Method Not Allowed
     - 不允许使用该 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应
