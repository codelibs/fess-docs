==========================
JobLog API
==========================

概述
====

JobLog API是用于获取 |Fess| 任务执行日志的API。
您可以查看计划任务和爬虫任务的执行历史、错误信息等。

基础URL
=======

::

    /api/admin/joblog

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
     - 获取任务日志列表
   * - GET
     - /{id}
     - 获取任务日志详情
   * - DELETE
     - /{id}
     - 删除任务日志
   * - DELETE
     - /delete-all
     - 删除所有任务日志

获取任务日志列表
================

请求
----

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - 否
     - 状态过滤（ok/fail/running）
   * - ``from``
     - String
     - 否
     - 开始日期时间（ISO 8601格式）
   * - ``to``
     - String
     - 否
     - 结束日期时间（ISO 8601格式）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
          }
        ],
        "total": 100
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
     - 任务日志ID
   * - ``jobName``
     - 任务名称
   * - ``jobStatus``
     - 任务状态（ok/fail/running）
   * - ``target``
     - 执行目标
   * - ``scriptType``
     - 脚本类型
   * - ``scriptData``
     - 执行脚本
   * - ``scriptResult``
     - 执行结果
   * - ``startTime``
     - 开始时间
   * - ``endTime``
     - 结束时间
   * - ``executionTime``
     - 执行时间（毫秒）

获取任务日志详情
================

请求
----

::

    GET /api/admin/joblog/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

删除任务日志
============

请求
----

::

    DELETE /api/admin/joblog/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

删除所有任务日志
================

请求
----

::

    DELETE /api/admin/joblog/delete-all

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
   * - ``status``
     - String
     - 否
     - 仅删除特定状态的日志

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

使用示例
========

获取任务日志列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

仅获取失败的任务
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取特定期间的任务日志
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取任务日志详情
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除旧任务日志
--------------

.. code-block:: bash

    # 删除30天之前的日志
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

仅删除失败的任务日志
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

检测执行时间长的任务
--------------------

.. code-block:: bash

    # 提取执行时间超过1小时的任务
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

计算任务成功率
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-scheduler` - 调度器API
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/joblog-guide` - 任务日志管理指南

