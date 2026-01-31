==========================
FailureUrl API
==========================

概述
====

FailureUrl API是用于管理 |Fess| 爬虫失败URL的API。
您可以查看和删除在爬虫过程中发生错误的URL。

基础URL
=======

::

    /api/admin/failureurl

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
     - 获取失败URL列表
   * - DELETE
     - /{id}
     - 删除失败URL
   * - DELETE
     - /delete-all
     - 删除所有失败URL

获取失败URL列表
===============

请求
----

::

    GET /api/admin/failureurl

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
   * - ``errorCountMin``
     - Integer
     - 否
     - 最小错误次数过滤
   * - ``configId``
     - String
     - 否
     - 配置ID过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
          }
        ],
        "total": 45
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
     - 失败URL ID
   * - ``url``
     - 失败的URL
   * - ``configId``
     - 爬虫配置ID
   * - ``errorName``
     - 错误名称
   * - ``errorLog``
     - 错误日志
   * - ``errorCount``
     - 错误发生次数
   * - ``lastAccessTime``
     - 最后访问时间
   * - ``threadName``
     - 线程名称

删除失败URL
===========

请求
----

::

    DELETE /api/admin/failureurl/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

删除所有失败URL
===============

请求
----

::

    DELETE /api/admin/failureurl/delete-all

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``configId``
     - String
     - 否
     - 仅删除特定配置ID的失败URL
   * - ``errorCountMin``
     - Integer
     - 否
     - 仅删除指定次数以上的错误

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
      }
    }

错误类型
========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 错误名称
     - 说明
   * - ``ConnectException``
     - 连接错误
   * - ``HttpStatusException``
     - HTTP状态错误（404、500等）
   * - ``SocketTimeoutException``
     - 超时错误
   * - ``UnknownHostException``
     - 主机名解析错误
   * - ``SSLException``
     - SSL证书错误
   * - ``IOException``
     - 输入输出错误

使用示例
========

获取失败URL列表
---------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

按错误次数过滤
--------------

.. code-block:: bash

    # 仅获取发生3次以上错误的URL
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取特定配置的失败URL
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除失败URL
-----------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除所有失败URL
---------------

.. code-block:: bash

    # 删除所有失败URL
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 仅删除特定配置的失败URL
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 仅删除发生3次以上错误的URL
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

按错误类型统计
--------------

.. code-block:: bash

    # 按错误类型计数
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`api-admin-joblog` - 任务日志API
- :doc:`../../admin/failureurl-guide` - 失败URL管理指南

