==========================
SearchList API
==========================

概述
====

SearchList API是用于在 |Fess| 索引中搜索和管理文档的Admin API。
支持对文档进行搜索、获取、创建、更新和删除操作。

响应中所有字段名均使用 ``snake_case`` 格式。值为 ``null`` 的字段将从响应中省略。

基础URL
=======

::

    /api/admin/searchlist

认证
====

调用此API需要通过 :doc:`api-admin-overview` 中所述的访问令牌进行认证。
令牌必须具有Admin API的访问权限（默认为 ``Radmin-api`` ）。
此权限可通过配置键 ``api.admin.access.permissions`` 进行修改。

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET / PUT
     - /docs
     - 搜索文档
   * - GET
     - /doc/{id}
     - 获取文档
   * - POST
     - /doc
     - 创建文档
   * - PUT
     - /doc
     - 更新文档
   * - DELETE
     - /doc/{id}
     - 删除文档（按ID）
   * - DELETE
     - /query
     - 删除文档（按查询）

搜索文档
========

搜索符合检索条件的文档。

请求
----

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``q``
     - String
     - 否
     - 搜索查询（最多1000个字符）。未指定时，以全部文档为对象。
   * - ``sort``
     - String
     - 否
     - 排序字段与方向（例：``last_modified.desc``）。
   * - ``start``
     - Integer
     - 否
     - 从0开始的起始位置（默认值 ``0``）。
   * - ``offset``
     - Integer
     - 否
     - 相对于 ``start`` 的偏移量（默认值 ``0``）。
   * - ``pn``
     - Integer
     - 否
     - 页码。
   * - ``num``
     - Integer
     - 否
     - 获取条数（默认值 ``10``）。超过配置最大值（默认 ``100``）或值为 ``0`` 以下时，将被截断为最大值。
   * - ``size``
     - Integer
     - 否
     - 获取条数（``num`` 的别名，为与其他Admin API兼容而提供）。
   * - ``lang``
     - String[]
     - 否
     - 搜索语言。可重复指定（数组）。例：``en``。
   * - ``ex_q``
     - String[]
     - 否
     - 附加查询表达式。可重复指定（数组）。
   * - ``fields.<name>``
     - String[]
     - 否
     - 按字段值过滤。最常见的用例是 ``fields.label``（按标签名过滤）；任意 ``fields.<name>`` 均会将结果限定为文档字段 ``<name>`` 与指定值匹配的文档。可重复指定。
   * - ``as.<name>``
     - String[]
     - 否
     - 高级搜索条件。任意 ``as.<name>``（例：``as.q``）均会传递给高级搜索条件构建器。每个 name 可重复指定。
   * - ``sdh``
     - String
     - 否
     - 相似文档哈希（similar-document hash）。

.. note::

   此端点不支持分面、高亮或地理（geo）搜索。即使指定了相关参数，也将被忽略。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
            "content_description": "..."
          }
        ]
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``version``
     - 运行中的 |Fess| 版本（示例值仅供参考）。
   * - ``status``
     - 状态码（``0`` 表示成功，详见"状态码"）。
   * - ``query_id``
     - 搜索查询ID。
   * - ``docs``
     - 搜索结果文档数组。每个文档以字段名与值的映射形式表示，使用索引字段名（``doc_id``、``url``、``title``、``content_description`` 等）。
   * - ``exec_time``
     - 搜索执行时间（秒，字符串类型）。
   * - ``query_time``
     - 搜索引擎查询时间（毫秒）。
   * - ``page_size``
     - 每页条数。
   * - ``page_number``
     - 当前页码。
   * - ``record_count``
     - 命中条数。
   * - ``record_count_relation``
     - 命中数的关系。``eq`` 表示精确计数，``gte`` 表示仅知下限。
   * - ``page_count``
     - 总页数。
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
     - 请求时间（epoch毫秒）。
   * - ``highlight_params``
     - 高亮用的查询参数字符串（此Admin API通常为空）。

获取文档
========

通过指定文档ID获取单条文档。

请求
----

::

    GET /api/admin/searchlist/doc/{id}

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``id``
     - String
     - 是
     - 文档ID（``doc_id`` 的值，路径参数）。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

若指定ID对应的文档不存在，将返回错误响应（``status`` = ``1``）。

创建文档
========

在索引中创建新文档。

请求
----

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "Sample Page 1",
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``doc``
     - 是
     - 要注册的文档。以索引字段名与值的映射形式指定。

在 ``doc`` 中指定的字段里，``index.admin.required.fields`` 配置的必填字段（默认值 ``url,title,role,boost``）必须全部提供。
与批量注册用的 :doc:`Documents API <api-admin-documents>` 不同，此端点不会自动补全 ``role`` 或 ``boost`` 等默认值，因此必填字段需在请求中明确指定。
``doc_id`` 由服务器端自动生成，创建时无需指定。

各字段的值将按照字段类型配置进行验证。类型不匹配时将返回错误（``status`` = ``1``）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 配置键
     - 默认值
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - （空）
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - （空）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``id``
     - 已注册文档的 ``doc_id``。
   * - ``created``
     - 创建时为 ``true``。

更新文档
========

更新已有文档。

请求
----

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "Updated Title",
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``doc``
     - 是
     - 要更新的文档。以索引字段名与值的映射形式指定。

更新对象由 ``doc`` 内的 ``doc_id`` 确定。若未指定 ``doc_id``，或不存在对应文档，将返回错误（``status`` = ``1``）。
与创建时相同，``index.admin.required.fields`` 配置的必填字段（默认值 ``url,title,role,boost``）必须全部提供，且各字段值将按类型配置进行验证。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``id``
     - 已更新文档的 ``doc_id``。
   * - ``created``
     - 更新时为 ``false``。

按ID删除文档
============

通过指定文档ID删除文档。

请求
----

::

    DELETE /api/admin/searchlist/doc/{id}

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``id``
     - String
     - 是
     - 文档ID（``doc_id`` 的值，路径参数）。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

按查询删除文档
==============

批量删除符合搜索查询的文档。

请求
----

::

    DELETE /api/admin/searchlist/query

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``q``
     - String
     - 是
     - 用于指定删除对象的搜索查询。

删除对象使用与"搜索文档"相同的方式构建查询，因此可同时使用 ``fields.<name>`` 和 ``ex_q`` 等过滤参数。若未指定 ``q``，将返回错误（``status`` = ``1``）。

响应
----

在 ``count`` 中返回已删除的文档条数。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

状态码
======

响应中的 ``status`` 字段将被设置为以下值之一。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 值
     - 名称
     - 说明
   * - ``0``
     - OK
     - 成功。
   * - ``1``
     - BAD_REQUEST
     - 请求无效（必填字段缺失、类型不匹配、目标文档不存在、查询无效等）。
   * - ``2``
     - SYSTEM_ERROR
     - 系统错误。
   * - ``3``
     - UNAUTHORIZED
     - 认证错误。
   * - ``9``
     - FAILED
     - 处理失败。

使用示例
========

搜索文档
--------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取文档
--------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

创建文档
--------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

按查询删除文档
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-documents` - 文档批量注册API
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/searchlist-guide` - 搜索列表管理指南
