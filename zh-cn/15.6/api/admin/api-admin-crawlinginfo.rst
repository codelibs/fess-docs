==========================
CrawlingInfo API
==========================

概述
====

CrawlingInfo API是用于获取 |Fess| 爬虫信息的API。
您可以查看爬虫会话的状态、进度和统计信息。

基础URL
=======

::

    /api/admin/crawlinginfo

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
     - 获取爬虫信息列表
   * - GET
     - /{sessionId}
     - 获取爬虫会话详情
   * - DELETE
     - /{sessionId}
     - 删除爬虫会话

获取爬虫信息列表
================

请求
----

::

    GET /api/admin/crawlinginfo

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

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``sessionId``
     - 会话ID
   * - ``name``
     - 爬虫名称
   * - ``status``
     - 状态（running/completed/failed）
   * - ``startTime``
     - 开始时间
   * - ``endTime``
     - 结束时间
   * - ``crawlingInfoCount``
     - 爬虫信息数
   * - ``createdDocCount``
     - 创建文档数
   * - ``updatedDocCount``
     - 更新文档数
   * - ``deletedDocCount``
     - 删除文档数

获取爬虫会话详情
================

请求
----

::

    GET /api/admin/crawlinginfo/{sessionId}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

删除爬虫会话
============

请求
----

::

    DELETE /api/admin/crawlinginfo/{sessionId}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

使用示例
========

获取爬虫信息列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取正在运行的爬虫会话
----------------------

.. code-block:: bash

    # 获取所有会话并过滤running状态
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

获取特定会话详情
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除旧会话
----------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

监控进度
--------

.. code-block:: bash

    # 定期检查正在运行会话的进度
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-failureurl` - 失败URL API
- :doc:`api-admin-joblog` - 任务日志API
- :doc:`../../admin/crawlinginfo-guide` - 爬虫信息指南

