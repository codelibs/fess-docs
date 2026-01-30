==========================
Scheduler API
==========================

概述
====

Scheduler API是用于管理 |Fess| 计划任务的API。
您可以启动/停止爬虫任务、创建/更新/删除调度设置等。

基础URL
=======

::

    /api/admin/scheduler

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET/PUT
     - /settings
     - 获取计划任务列表
   * - GET
     - /setting/{id}
     - 获取计划任务
   * - POST
     - /setting
     - 创建计划任务
   * - PUT
     - /setting
     - 更新计划任务
   * - DELETE
     - /setting/{id}
     - 删除计划任务
   * - PUT
     - /{id}/start
     - 启动任务
   * - PUT
     - /{id}/stop
     - 停止任务

获取计划任务列表
================

请求
----

::

    GET /api/admin/scheduler/settings
    PUT /api/admin/scheduler/settings

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
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": true,
            "crawler": true,
            "available": true,
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

获取计划任务
============

请求
----

::

    GET /api/admin/scheduler/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cronExpression": "0 0 0 * * ?",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "jobLogging": true,
          "crawler": true,
          "available": true,
          "sortOrder": 0,
          "running": false
        }
      }
    }

创建计划任务
============

请求
----

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 任务名称
   * - ``target``
     - 是
     - 执行目标（"all"或特定目标）
   * - ``cronExpression``
     - 是
     - Cron表达式（秒 分 时 日 月 星期）
   * - ``scriptType``
     - 是
     - 脚本类型（"groovy"）
   * - ``scriptData``
     - 是
     - 执行脚本
   * - ``jobLogging``
     - 否
     - 启用日志记录（默认：true）
   * - ``crawler``
     - 否
     - 是否为爬虫任务（默认：false）
   * - ``available``
     - 否
     - 启用/禁用（默认：true）
   * - ``sortOrder``
     - 否
     - 显示顺序

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Cron表达式示例
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Cron表达式
     - 说明
   * - ``0 0 2 * * ?``
     - 每天凌晨2点执行
   * - ``0 0 0/6 * * ?``
     - 每6小时执行一次
   * - ``0 0 2 * * MON``
     - 每周一凌晨2点执行
   * - ``0 0 2 1 * ?``
     - 每月1日凌晨2点执行

更新计划任务
============

请求
----

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1,
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

删除计划任务
============

请求
----

::

    DELETE /api/admin/scheduler/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

启动任务
========

立即执行计划任务。

请求
----

::

    PUT /api/admin/scheduler/{id}/start

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

注意事项
--------

- 如果任务已在运行中，将返回错误
- 如果任务已禁用（``available: false``），将返回错误

停止任务
========

停止正在运行的任务。

请求
----

::

    PUT /api/admin/scheduler/{id}/stop

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用示例
========

创建并执行爬虫任务
------------------

.. code-block:: bash

    # 创建任务
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": true,
           "crawler": true,
           "available": true
         }'

    # 立即执行任务
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

检查任务状态
------------

.. code-block:: bash

    # 检查所有任务状态
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 可通过running字段查看执行状态

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-joblog` - 任务日志API
- :doc:`../../admin/scheduler-guide` - 调度器管理指南

