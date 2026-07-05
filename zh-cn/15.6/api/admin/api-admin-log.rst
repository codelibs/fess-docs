==========================
Log API
==========================

概述
====

Log API是用于获取 |Fess| 日志信息的API。
您可以查看搜索日志、爬虫日志、系统日志等。

基础URL
=======

::

    /api/admin/log

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /search
     - 获取搜索日志
   * - GET
     - /click
     - 获取点击日志
   * - GET
     - /favorite
     - 获取收藏日志
   * - DELETE
     - /search/delete
     - 删除搜索日志

获取搜索日志
============

请求
----

::

    GET /api/admin/log/search

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``size``
     - Integer
     - 否
     - 每页记录数（默认：20）
   * - ``page``
     - Integer
     - 否
     - 页码（从0开始）
   * - ``from``
     - String
     - 否
     - 开始日期时间（ISO 8601格式）
   * - ``to``
     - String
     - 否
     - 结束日期时间（ISO 8601格式）
   * - ``query``
     - String
     - 否
     - 搜索查询过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "log_id_1",
            "queryId": "query_id_1",
            "query": "fess search",
            "requestedAt": "2025-01-29T10:30:00Z",
            "responseTime": 123,
            "hitCount": 567,
            "user": "guest",
            "roles": ["guest"],
            "languages": ["ja"],
            "clientIp": "192.168.1.100",
            "userAgent": "Mozilla/5.0..."
          }
        ],
        "total": 1234
      }
    }

获取点击日志
============

请求
----

::

    GET /api/admin/log/click

参数
~~~~

除了与搜索日志相同的参数外，还可指定以下参数：

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``url``
     - String
     - 否
     - 被点击的URL过滤
   * - ``queryId``
     - String
     - 否
     - 搜索查询ID过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "click_log_id_1",
            "queryId": "query_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "order": 1,
            "clickedAt": "2025-01-29T10:31:00Z",
            "user": "guest",
            "clientIp": "192.168.1.100"
          }
        ],
        "total": 567
      }
    }

获取收藏日志
============

请求
----

::

    GET /api/admin/log/favorite

参数
~~~~

与点击日志相同的参数

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "favorite_log_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "createdAt": "2025-01-29T10:32:00Z",
            "user": "user123"
          }
        ],
        "total": 123
      }
    }

删除搜索日志
============

请求
----

::

    DELETE /api/admin/log/search/delete

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``before``
     - String
     - 是
     - 删除此日期时间之前的日志（ISO 8601格式）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deletedCount": 5678
      }
    }

使用示例
========

获取最近的搜索日志
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取特定期间的搜索日志
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取特定查询的搜索日志
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?query=fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取点击日志
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/click?size=100" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除旧搜索日志
--------------

.. code-block:: bash

    # 删除30天之前的日志
    curl -X DELETE "http://localhost:8080/api/admin/log/search/delete?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-stats` - 统计API
- :doc:`../../admin/log-guide` - 日志管理指南

