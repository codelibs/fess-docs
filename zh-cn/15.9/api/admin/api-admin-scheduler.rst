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
   * - GET
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
     - 每页记录数（默认：25；可通过 ``fess_config.properties`` 中的 ``paging.page.size`` 修改）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始；默认：1）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cron_expression": "0 0 0 * * ?",
            "script_type": "javascript",
            "script_data": "...",
            "job_logging": "true",
            "crawler": "true",
            "available": "true",
            "sort_order": 0,
            "version_no": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   响应的 ``response`` 对象中始终包含表示产品版本的 ``version`` 和表示处理结果的 ``status``\ （公共规范请参阅 :doc:`api-admin-overview`）。后续示例中可能省略 ``version`` 以保持简洁。

.. note::

   响应中的 ``job_logging`` / ``crawler`` / ``available`` 以字符串（``"true"`` / ``"false"``）形式返回。\ ``running`` 为布尔值，是仅响应中包含的字段，表示任务当前是否正在运行（不可在请求中指定）。\ ``total`` 为符合查询条件的任务总数。

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
          "cron_expression": "0 0 0 * * ?",
          "script_type": "javascript",
          "script_data": "return container.getComponent(\"crawlJob\").execute();",
          "job_logging": "true",
          "crawler": "true",
          "available": "true",
          "sort_order": 0,
          "version_no": 1,
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
      "cron_expression": "0 0 2 * * ?",
      "script_type": "javascript",
      "script_data": "return container.getComponent(\"crawlJob\").execute();",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1
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
     - 任务名称（最大100字符）
   * - ``target``
     - 是
     - 执行目标（最大100字符）。指定 ``all`` 或特定目标名称
   * - ``cron_expression``
     - 否
     - Cron表达式（秒 分 时 日 月 星期）。最大100字符，将作为Cron表达式进行验证。若为空，则不进行定时执行，只能手动启动
   * - ``script_type``
     - 是
     - 脚本类型（最大100字符）。可指定 ``javascript`` （新建作业的默认值，由 ``job.default.script`` 属性决定）或 ``groovy`` （需要 ``fess-script-groovy`` 插件）
   * - ``script_data``
     - 否
     - 执行脚本。最大大小遵循 ``fess_config.properties`` 中的 ``form.admin.max.input.size``
   * - ``job_logging``
     - 否
     - 启用任务日志记录（字符串）
   * - ``crawler``
     - 否
     - 是否为爬虫任务（字符串）
   * - ``available``
     - 否
     - 启用/禁用（字符串）
   * - ``sort_order``
     - 是
     - 显示顺序（0～2147483647之间的整数）

.. note::

   ``job_logging`` / ``crawler`` / ``available`` 为字符串字段。在请求中，指定 ``"on"`` 或 ``"true"``\ （不区分大小写）时启用；其他值（``"false"``、空字符串或未指定）均视为禁用。在响应中以 ``"true"`` / ``"false"`` 形式返回。

.. note::

   ``crud_mode`` 由服务器端自动设置，无需在请求中指定。\ ``created_by`` / ``created_time`` 等审计字段也由服务器端设置。

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
      "cron_expression": "0 0 3 * * ?",
      "script_type": "javascript",
      "script_data": "...",
      "job_logging": "true",
      "crawler": "true",
      "available": "true",
      "sort_order": 1,
      "version_no": 1
    }

.. note::

   更新时，``id``\ （最大1000字符）和 ``version_no`` 为必填项。\ ``version_no`` 用于乐观锁，需指定获取响应中返回的值。若值不匹配，更新将失败。其他必填字段（``name`` / ``target`` / ``script_type`` / ``sort_order``）与创建时相同。

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
        "status": 0,
        "job_log_id": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``job_log_id``
     - 已启动任务的任务日志ID。在任务日志启用时发行。任务日志禁用时不包含在响应中。

注意事项
--------

- 如果任务已在运行中，启动将失败并返回错误（``status`` 非 ``0``）。
- 如果任务已禁用（``available`` 未启用），同样将启动失败并返回错误。
- ``job_log_id`` 仅在任务日志已启用（``job_logging`` 已启用）时才会发行。

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
           "cron_expression": "0 0 * * * ?",
           "script_type": "javascript",
           "script_data": "return container.getComponent(\"crawlJob\").execute();",
           "job_logging": "true",
           "crawler": "true",
           "available": "true",
           "sort_order": 1
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

