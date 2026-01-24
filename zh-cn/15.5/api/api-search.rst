======
搜索API
======

获取搜索结果
===========

请求
--------

==================  ====================================================
HTTP方法             GET
端点                 ``/api/v1/documents``
==================  ====================================================

向 |Fess| 发送
``http://<Server Name>/api/v1/documents?q=搜索词``
形式的请求，
可以获取 |Fess| 的搜索结果的JSON格式数据。
要使用搜索API，需要在管理界面的"系统 > 常规设置"中启用JSON响应。

请求参数
-----------------

通过指定
``http://<Server Name>/api/v1/documents?q=搜索词&num=50&fields.label=fess``
等请求参数，可以执行更高级的搜索。
可用的请求参数如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - 搜索词。需要进行URL编码。
   * - start
     - 起始位置。从0开始。
   * - num
     - 显示数量。默认为20条。最多可显示100条。
   * - sort
     - 排序。用于对搜索结果进行排序。
   * - fields.label
     - 标签值。用于指定标签。
   * - facet.field
     - 分面字段指定。 (示例) ``facet.field=label``
   * - facet.query
     - 分面查询指定。     (示例) ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - 获取分面的最大数量。当指定了facet.field时有效。
   * - facet.minDocCount
     - 获取数量大于等于此值的分面。当指定了facet.field时有效。
   * - geo.location.point
     - 经纬度指定。 (示例) ``geo.location.point=35.0,139.0``
   * - geo.location.distance
     - 从中心点的距离指定。 (示例) ``geo.location.distance=10km``
   * - lang
     - 搜索语言指定。 (示例) ``lang=en``
   * - preference
     - 搜索时指定分片的字符串。 (示例) ``preference=abc``
   * - callback
     - 使用JSONP时的回调名称。不使用JSONP时无需指定。

表: 请求参数


响应
--------

| 将返回以下响应。
| （已格式化）

::

    {
      "q": "Fess",
      "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
      "exec_time": 0.21,
      "query_time": 0,
      "page_size": 20,
      "page_number": 1,
      "record_count": 31625,
      "page_count": 1,
      "highlight_params": "&hq=n2sm&hq=Fess",
      "next_page": true,
      "prev_page": false,
      "start_record_number": 1,
      "end_record_number": 20,
      "page_numbers": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "partial": false,
      "search_query": "(Fess OR n2sm)",
      "requested_time": 1507822131845,
      "related_query": [
        "aaa"
      ],
      "related_contents": [],
      "data": [
        {
          "filetype": "html",
          "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
          "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
          "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess ? Fess is very powerful and easily deployable Enterprise Search Server. ...",
          "host": "fess.codelibs.org",
          "last_modified": "2017-10-09T22:28:56.000Z",
          "content_length": "29624",
          "timestamp": "2017-10-09T22:28:56.000Z",
          "url_link": "https://fess.codelibs.org/",
          "created": "2017-10-10T15.50:48.609Z",
          "site_path": "fess.codelibs.org/",
          "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
          "url": "https://fess.codelibs.org/",
          "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is OpenSearch-based search",
          "site": "fess.codelibs.org/",
          "boost": "10.0",
          "mimetype": "text/html"
        }
      ]
    }

各元素说明如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 响应信息

   * - q
     - 搜索词
   * - exec_time
     - 响应时间（单位：秒）
   * - query_time
     - 查询处理时间（单位：毫秒）
   * - page_size
     - 显示数量
   * - page_number
     - 页码
   * - record_count
     - 搜索词匹配的总数量
   * - page_count
     - 搜索词匹配的总页数
   * - highlight_params
     - 高亮参数
   * - next_page
     - true: 存在下一页。false: 不存在下一页。
   * - prev_page
     - true: 存在上一页。false: 不存在上一页。
   * - start_record_number
     - 记录编号的起始位置
   * - end_record_number
     - 记录编号的结束位置
   * - page_numbers
     - 页码数组
   * - partial
     - 搜索超时等导致搜索结果被截断时为true。
   * - search_query
     - 搜索查询
   * - requested_time
     - 请求时间（单位：epoch毫秒）
   * - related_query
     - 相关查询
   * - related_contents
     - 相关内容查询
   * - facet_field
     - 匹配给定分面字段的文档信息（仅当请求参数中提供了 ``facet.field`` 时）
   * - facet_query
     - 匹配给定分面查询的文档数量（仅当请求参数中提供了 ``facet.query`` 时）
   * - result
     - 搜索结果的父元素
   * - filetype
     - 文件类型
   * - created
     - 文档创建日期时间
   * - title
     - 文档标题
   * - doc_id
     - 文档ID
   * - url
     - 文档URL
   * - site
     - 站点名称
   * - content_description
     - 内容描述
   * - host
     - 主机名
   * - digest
     - 文档摘要字符串
   * - boost
     - 文档权重值
   * - mimetype
     - MIME类型
   * - last_modified
     - 最后修改日期时间
   * - content_length
     - 文档大小
   * - url_link
     - 搜索结果的URL
   * - timestamp
     - 文档更新日期时间


搜索所有文档
==================

要搜索所有目标文档，请发送以下请求：
``http://<Server Name>/api/v1/documents/all?q=搜索词``

要使用此功能，需要在fess_config.properties中将api.search.scroll设置为true。

请求参数
-----------------

可用的请求参数如下：

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - 搜索词。需要进行URL编码。
   * - num
     - 显示数量。默认为20条。最多可显示100条。
   * - sort
     - 排序。用于对搜索结果进行排序。

表: 请求参数

错误响应
==============

当搜索API失败时，将返回以下错误响应：

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求参数无效
   * - 500 Internal Server Error
     - 服务器内部错误

错误响应示例：

::

    {
      "message": "Invalid request parameter",
      "status": 400
    }
