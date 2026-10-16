================
搜索结果导出 API
================

本文档介绍将搜索结果下载为 CSV 或 JSON 文件的 |Fess| v2 导出 API。公共响应信封和错误模型相关内容，请参阅 :doc:`api-overview`\ 。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

.. note::

   导出默认禁用。要使用此功能，请在 ``fess_config.properties`` 中设置 ``api.search.export=true``\ 。启用后，内置的 ``bootstrap`` 主题会在搜索结果数量旁边显示导出菜单（CSV / JSON）。可以通过 ``/api/v2/ui/config`` 的 ``features.search_export`` 确认其状态。

下载搜索结果
============

请求
----

==================  ====================================================
HTTP 方法           GET
端点                ``/api/v2/documents/export``
==================  ====================================================

将与搜索匹配的文档作为文件下载（ ``Content-Disposition: attachment``\ ，文件名为 ``search_results.csv`` 或 ``search_results.json`` ）返回。

- 应用与 ``/api/v2/search`` 相同的角色筛选。即使在 ``login.required=true`` 时，也可以像 ``/api/v2/search`` 一样使用访问令牌。
- 最多导出 ``api.search.export.max.size`` （默认值： ``1000`` ）个文档。不使用分页参数（ ``start``\ 、\ ``num`` ）。
- 导出的字段为 ``api.search.export.fields`` （默认值： ``title,url_link,last_modified,content_length,filetype`` ）中可以包含在 API 响应中的字段。
- 请求被限制为每分钟 ``api.search.export.rate.limit.per.minute`` （默认值： ``10``\ ，\ ``0`` 表示不限制）次。已登录用户按用户计数，访客按客户端 IP 地址计数。超出时返回 ``429`` 和 ``Retry-After`` 头。
- 导出不会记录到搜索日志中。

请求参数
--------

可以指定 ``q``\ 、\ ``ex_q``\ 、\ ``fields.*``\ 、\ ``sort``\ 、\ ``lang`` 等与 ``/api/v2/documents/all`` 相同的搜索条件参数（请参阅 :doc:`api-search` ）。此外还有以下参数。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 请求参数

   * - ``format``
     - 文件格式。 ``csv`` （默认）或 ``json``\ 。其他值返回 ``invalid_request`` （400）。

表: 请求参数

响应
----

CSV 的第 1 行为字段名标题行，以 ``csv.file.encoding`` 的字符编码输出（UTF-8 时附加 BOM）。以 ``=``\ 、\ ``+``\ 、\ ``-``\ 、\ ``@``\ 、制表符或回车开头的值会在开头加上 ``'``\ ，以免在电子表格中被当作公式执行。具有多个值的字段以空格连接。

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

JSON 为 ``{"data":[{...},...]}`` 格式，具有多个值的字段保持为数组。

在文件开始输出之前失败时，返回通常的错误信封。输出开始后失败时，文件会中途结束（CSV 只输出到中途，JSON 会成为无法解析的内容）。

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 查询不正确、 ``format`` 不是 ``csv`` / ``json``\ ，或通过 ``api.search.export=false`` 禁用了导出时。
   * - 401 Unauthorized
     - 需要认证时（例如 ``login.required=true`` 下的匿名调用者）。
   * - 405 Method Not Allowed
     - HTTP 方法不被允许时。
   * - 429 Too Many Requests
     - 超过每分钟请求数上限时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应
