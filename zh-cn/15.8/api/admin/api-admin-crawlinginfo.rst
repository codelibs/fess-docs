==========================
CrawlingInfo API
==========================

概述
====

CrawlingInfo API是用于查看和管理 |Fess| 爬虫信息（爬虫会话）的API。
可以执行爬虫会话的列表获取、单个获取、删除等操作。

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
     - /logs
     - 获取爬虫信息列表
   * - GET
     - /log/{id}
     - 获取爬虫信息
   * - DELETE
     - /log/{id}
     - 删除爬虫信息
   * - DELETE
     - /all
     - 批量删除爬虫会话（不含运行中）

获取爬虫信息列表
================

请求
----

::

    GET /api/admin/crawlinginfo/logs

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
   * - ``sessionId``
     - String
     - 否
     - 会话ID过滤（部分匹配）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
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
   * - ``id``
     - 爬虫信息ID
   * - ``sessionId``
     - 会话ID
   * - ``name``
     - 会话名称
   * - ``expiredTime``
     - 有效期限（epoch毫秒；以字符串形式返回）
   * - ``createdTime``
     - 创建时刻（epoch毫秒；以数值形式返回）

.. note::

   响应中每个日志对象还包含一个内部字段 ``crudMode``
   （表示CRUD操作模式的整数值，在读取操作时始终为 ``0``）。
   客户端可安全忽略此字段。

获取爬虫信息
============

请求
----

::

    GET /api/admin/crawlinginfo/log/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
        }
      }
    }

删除爬虫信息
============

请求
----

::

    DELETE /api/admin/crawlinginfo/log/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

批量删除爬虫会话
==================

删除所有爬虫会话（及其参数数据），正在运行的会话除外。不设置任何时间阈值，所有当前未在运行的会话均会被删除。

请求
----

::

    DELETE /api/admin/crawlinginfo/all

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

获取爬虫信息列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

按特定会话过滤
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取爬虫信息
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除爬虫信息
------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

批量删除会话
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-failureurl` - 失败URL API
- :doc:`api-admin-joblog` - 作业日志API
- :doc:`../../admin/crawlinginfo-guide` - 爬虫信息指南
