==========================
Stats API
==========================

概述
====

Stats API是用于获取 |Fess| 统计信息的API。
您可以查看搜索查询、点击、收藏等统计数据。

基础URL
=======

::

    /api/admin/stats

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /
     - 获取统计信息

获取统计信息
============

请求
----

::

    GET /api/admin/stats

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``from``
     - String
     - 否
     - 开始日期时间（ISO 8601格式）
   * - ``to``
     - String
     - 否
     - 结束日期时间（ISO 8601格式）
   * - ``type``
     - String
     - 否
     - 统计类型（query/click/favorite）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 12345,
          "uniqueQueries": 5678,
          "totalClicks": 9876,
          "totalFavorites": 543,
          "averageResponseTime": 123.45,
          "topQueries": [
            {
              "query": "fess",
              "count": 567
            },
            {
              "query": "search",
              "count": 432
            }
          ],
          "topClickedDocuments": [
            {
              "url": "https://example.com/doc1",
              "title": "Document 1",
              "count": 234
            }
          ],
          "queryTrends": [
            {
              "date": "2025-01-01",
              "count": 234
            },
            {
              "date": "2025-01-02",
              "count": 267
            }
          ]
        }
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``totalQueries``
     - 总搜索查询数
   * - ``uniqueQueries``
     - 唯一搜索查询数
   * - ``totalClicks``
     - 总点击数
   * - ``totalFavorites``
     - 总收藏数
   * - ``averageResponseTime``
     - 平均响应时间（毫秒）
   * - ``topQueries``
     - 热门搜索查询
   * - ``topClickedDocuments``
     - 热门文档
   * - ``queryTrends``
     - 查询趋势

使用示例
========

获取所有统计信息
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

指定期间的统计获取
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取搜索查询统计
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取热门查询TOP10
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.stats.topQueries[:10]'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-log` - 日志API
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`../../admin/stats-guide` - 统计管理指南

