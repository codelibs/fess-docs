==========================
SearchLog API
==========================

概述
====

SearchLog API是用于获取和管理 |Fess| 搜索日志的API。
可用于分析用户搜索行为，改进搜索质量。

基础URL
=======

::

    /api/admin/searchlog

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
     - 获取搜索日志列表
   * - GET
     - /{id}
     - 获取搜索日志详情
   * - DELETE
     - /{id}
     - 删除搜索日志
   * - DELETE
     - /delete-all
     - 批量删除搜索日志
   * - GET
     - /stats
     - 获取搜索统计

获取搜索日志列表
================

请求
----

::

    GET /api/admin/searchlog

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
     - 按搜索查询过滤
   * - ``user``
     - String
     - 否
     - 按用户ID过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "searchlog_id_1",
            "searchWord": "Fess 安装",
            "requestedAt": "2025-01-29T10:00:00Z",
            "responseTime": 125,
            "hitCount": 234,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user001",
            "userSessionId": "session_abc123",
            "clientIp": "192.168.1.100",
            "referer": "https://example.com/",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user", "admin"],
            "languages": ["ja"]
          },
          {
            "id": "searchlog_id_2",
            "searchWord": "搜索 设置",
            "requestedAt": "2025-01-29T09:55:00Z",
            "responseTime": 98,
            "hitCount": 567,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user002",
            "userSessionId": "session_def456",
            "clientIp": "192.168.1.101",
            "referer": "",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user"],
            "languages": ["ja", "en"]
          }
        ],
        "total": 10000
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``id``
     - 搜索日志ID
   * - ``searchWord``
     - 搜索关键词
   * - ``requestedAt``
     - 搜索日期时间
   * - ``responseTime``
     - 响应时间（毫秒）
   * - ``hitCount``
     - 命中数量
   * - ``queryOffset``
     - 结果偏移量
   * - ``queryPageSize``
     - 页面大小
   * - ``user``
     - 用户ID
   * - ``userSessionId``
     - 会话ID
   * - ``clientIp``
     - 客户端IP地址
   * - ``referer``
     - 来源页面
   * - ``userAgent``
     - 用户代理
   * - ``roles``
     - 用户角色
   * - ``languages``
     - 搜索语言

获取搜索日志详情
================

请求
----

::

    GET /api/admin/searchlog/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "searchlog_id_1",
          "searchWord": "Fess 安装",
          "requestedAt": "2025-01-29T10:00:00Z",
          "responseTime": 125,
          "hitCount": 234,
          "queryOffset": 0,
          "queryPageSize": 10,
          "user": "user001",
          "userSessionId": "session_abc123",
          "clientIp": "192.168.1.100",
          "referer": "https://example.com/",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "roles": ["user", "admin"],
          "languages": ["ja"],
          "clickLogs": [
            {
              "url": "https://fess.codelibs.org/install.html",
              "docId": "doc_123",
              "order": 1,
              "clickedAt": "2025-01-29T10:00:15Z"
            }
          ]
        }
      }
    }

删除搜索日志
============

请求
----

::

    DELETE /api/admin/searchlog/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search log deleted successfully"
      }
    }

批量删除搜索日志
================

请求
----

::

    DELETE /api/admin/searchlog/delete-all

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
     - 否
     - 删除此日期时间之前的日志（ISO 8601格式）
   * - ``user``
     - String
     - 否
     - 仅删除特定用户的日志

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

获取搜索统计
============

请求
----

::

    GET /api/admin/searchlog/stats

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
   * - ``interval``
     - String
     - 否
     - 统计间隔（hour/day/week/month）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalSearches": 50000,
          "uniqueUsers": 1234,
          "averageResponseTime": 156,
          "averageHitCount": 345,
          "zeroHitRate": 0.05,
          "topSearchWords": [
            {"word": "Fess", "count": 1500},
            {"word": "安装", "count": 800},
            {"word": "设置", "count": 650}
          ],
          "searchesByDate": [
            {"date": "2025-01-29", "count": 2500},
            {"date": "2025-01-28", "count": 2300},
            {"date": "2025-01-27", "count": 2100}
          ]
        }
      }
    }

使用示例
========

获取搜索日志列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

指定期间获取
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?from=2025-01-01T00:00:00Z&to=2025-01-31T23:59:59Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取特定用户的搜索日志
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?user=user001" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取特定关键词的搜索日志
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?query=Fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取搜索统计
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31&interval=day" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除旧搜索日志
--------------

.. code-block:: bash

    # 删除30天之前的日志
    curl -X DELETE "http://localhost:8080/api/admin/searchlog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

提取热门搜索关键词
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.topSearchWords'

分析搜索质量
------------

.. code-block:: bash

    # 检查零命中率
    curl -X GET "http://localhost:8080/api/admin/searchlog/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '{zeroHitRate: .response.stats.zeroHitRate, averageHitCount: .response.stats.averageHitCount}'

日均搜索量趋势
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?interval=day&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.searchesByDate'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-stats` - 系统统计API
- :doc:`../../admin/searchlog-guide` - 搜索日志管理指南
- :doc:`../../config/admin-opensearch-dashboards` - 搜索分析配置指南

