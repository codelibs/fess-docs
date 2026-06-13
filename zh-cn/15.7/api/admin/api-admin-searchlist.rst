==========================
SearchList API
==========================

概述
====

SearchList API是用于搜索和管理 |Fess| 索引内文档的API。
可以执行文档的搜索、获取、创建、更新和删除操作。

基础URL
=======

::

    /api/admin/searchlist

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
     - 文档搜索
   * - GET
     - /doc/{id}
     - 文档获取
   * - POST
     - /doc
     - 文档创建
   * - PUT
     - /doc
     - 文档更新
   * - DELETE
     - /doc/{id}
     - 文档删除（指定ID）
   * - DELETE
     - /query
     - 文档删除（指定查询）

文档搜索
========

搜索与检索条件匹配的文档。

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
     - 搜索查询。未指定时以全部记录为对象。
   * - ``sort``
     - String
     - 否
     - 排序字段和方向
   * - ``start``
     - Integer
     - 否
     - 搜索结果的起始位置
   * - ``offset``
     - Integer
     - 否
     - 分页的偏移量
   * - ``num``
     - Integer
     - 否
     - 获取的记录数
   * - ``size``
     - Integer
     - 否
     - 获取的记录数（ ``num`` 的别名）
   * - ``lang``
     - String[]
     - 否
     - 语言

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "queryId": "...",
        "execTime": "0.05",
        "pageSize": 20,
        "pageNumber": 1,
        "recordCount": 234,
        "recordCountRelation": "EQUAL_TO",
        "pageCount": 12,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "サンプルページ1",
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
   * - ``queryId``
     - 搜索查询ID
   * - ``docs``
     - 搜索结果文档的数组
   * - ``execTime``
     - 搜索执行时间
   * - ``pageSize``
     - 每页的记录数
   * - ``pageNumber``
     - 当前页码
   * - ``recordCount``
     - 命中记录数
   * - ``recordCountRelation``
     - 命中记录数的关系（完全一致还是下限值）
   * - ``pageCount``
     - 总页数

文档获取
========

指定文档ID，获取单个文档。

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
     - 文档ID（ ``doc_id`` ，路径参数）

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
          "title": "サンプルページ1"
        }
      }
    }

文档创建
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
        "title": "サンプルページ1",
        "content": "本文テキストです。"
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
     - 要注册的文档。以字段名和值的映射指定。

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

文档更新
========

更新已有的文档。

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
        "title": "更新後のタイトル",
        "content": "更新後の本文テキストです。"
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
     - 要更新的文档。以字段名和值的映射指定。

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

文档删除（指定ID）
==================

指定文档ID进行删除。

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
     - 文档ID（ ``doc_id`` ，路径参数）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

文档删除（指定查询）
====================

批量删除与搜索查询匹配的文档。

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
     - 删除对象的搜索查询

响应
----

通过 ``count`` 返回已删除的文档数量。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

使用示例
========

文档搜索
--------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

文档获取
--------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

通过指定查询删除文档
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-documents` - 文档批量注册API
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/searchlist-guide` - 搜索列表管理指南
