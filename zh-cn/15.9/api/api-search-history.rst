============
搜索历史 API
============

本文档介绍 |Fess| v2 搜索历史 API。公共响应信封和错误模型相关内容，请参阅 :doc:`api-overview`\ 。

基础 URL 为 ``http://<Server Name>/api/v2/``\ （本地环境示例：\ ``http://localhost:8080/api/v2``\ ）。

.. note::

   当 ``search.history.enabled`` （默认值： ``true`` ）和搜索日志记录都启用时，才能使用搜索历史。可以通过 ``/api/v2/ui/config`` 的 ``features.search_history`` 确认其状态。

获取最近的搜索
==============

请求
----

==================  ====================================================
HTTP 方法           GET
端点                ``/api/v2/search-history``
==================  ====================================================

按从新到旧的顺序返回已登录用户在当前虚拟主机上通过 ``/api/v2/search`` 进行的最近搜索。可以使用返回的条件再次执行同样的搜索。

- 只包含第 1 页的搜索。条件相同的搜索会合并为最新的 1 条。不包含没有搜索词的搜索。
- 最多返回 ``search.history.size`` （默认值： ``10`` ）条。
- 搜索日志由每分钟运行的作业写入，因此搜索最多需要大约 1 分钟才会出现在历史中。
- 历史与会话中的登录用户关联。匿名调用者会得到 ``auth_required`` （401），访问令牌不能代替登录。
- 搜索历史功能被禁用时，返回 ``invalid_request`` （400）。

没有请求参数。

响应
----

成功时（200），在公共信封的 ``response`` 下直接返回以下字段。

::

    {
      "response": {
        "status": 0,
        "record_count": 1,
        "data": [
          {
            "q": "fess",
            "fields": { "label": ["docs"] },
            "sort": "last_modified.desc",
            "requested_at": "2026-10-01T09:00:00Z",
            "hit_count": 42
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 响应字段

   * - ``record_count``
     - ``data`` 中的搜索条数（int）。
   * - ``data``
     - 最近搜索的数组（从新到旧）。条件的键使用 ``/api/v2/search`` 的请求参数名，该搜索未使用的键会被省略。
   * - ``data[].q``
     - 搜索词（str）。
   * - ``data[].fields``
     - 通过 ``fields.<name>`` 指定的字段条件（以字段名为键的值数组）。
   * - ``data[].ex_q``
     - 附加查询（str 数组）。
   * - ``data[].sort``
     - 排序顺序（str）。
   * - ``data[].lang``
     - 通过 ``lang`` 指定的语言（str 数组）。
   * - ``data[].requested_at``
     - 搜索的日期时间（UTC，ISO-8601）。
   * - ``data[].hit_count``
     - 该搜索的命中数（int64）。

表: 响应字段

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 搜索历史功能被禁用时。
   * - 401 Unauthorized
     - 未登录时。
   * - 405 Method Not Allowed
     - HTTP 方法不被允许时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

表: 错误响应

在内置主题中的显示
==================

在内置的 ``bootstrap`` 主题中，已登录的用户点击空的搜索框或在搜索框中按下方向键时，建议下拉列表中会显示最近的搜索。选择某一项后，会连同标签等条件一起再次执行同样的搜索。在 |Fess| 15.9 之前记录的搜索日志没有保存条件，因此不会显示在历史中。
