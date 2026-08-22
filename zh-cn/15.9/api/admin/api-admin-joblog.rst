==========================
JobLog API
==========================

概述
====

JobLog API是用于查看和管理 |Fess| 作业执行日志的API。
可以获取和删除调度作业及爬虫作业的执行历史、执行结果和错误信息等。

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
     - /logs
     - 获取作业日志列表
   * - GET
     - /log/{id}
     - 获取作业日志
   * - DELETE
     - /log/{id}
     - 删除作业日志

获取作业日志列表
================

请求
----

::

    GET /api/admin/joblog/logs

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
     - 每页记录数（默认: 20）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认: 1）
   * - ``id``
     - String
     - 否
     - 按作业日志ID过滤（完全匹配）

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
            "startTime": "1738116000000",
            "endTime": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "1738029600000",
            "endTime": "1738030215000"
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
     - 作业日志ID
   * - ``jobName``
     - 作业名称
   * - ``jobStatus``
     - 作业状态（``ok``: 成功、``fail``: 失败、``running``: 执行中）
   * - ``target``
     - 执行目标（调度器的目标名称，默认值为 ``all``）
   * - ``scriptType``
     - 脚本类型（例: ``groovy``）
   * - ``scriptData``
     - 执行脚本
   * - ``scriptResult``
     - 执行结果
   * - ``startTime``
     - 开始时刻（epoch毫秒；以字符串形式返回）
   * - ``endTime``
     - 结束时刻（epoch毫秒；以字符串形式返回）。执行中的作业不返回此字段。

.. note::

   响应中每个日志对象还包含一个内部字段 ``crudMode``
   （表示CRUD操作模式的整数值，在读取操作时始终为 ``0``）。
   客户端可安全忽略此字段。

获取作业日志
============

请求
----

::

    GET /api/admin/joblog/log/{id}

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
          "startTime": "1738116000000",
          "endTime": "1738118723000"
        }
      }
    }

若指定ID的作业日志不存在，则返回 ``status`` 为非0值的错误响应。

删除作业日志
============

请求
----

::

    DELETE /api/admin/joblog/log/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

若指定ID的作业日志不存在，则返回 ``status`` 为非0值的错误响应。

使用示例
========

获取作业日志列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

仅提取失败的作业
----------------

.. code-block:: bash

    # 用jq过滤失败的作业
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

获取作业日志
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除作业日志
------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

计算作业成功率
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-scheduler` - 调度器API
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/joblog-guide` - 作业日志管理指南
