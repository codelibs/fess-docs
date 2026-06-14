==========================
FailureUrl API
==========================

概述
====

FailureUrl API是用于管理 |Fess| 爬虫失败URL的API。
可以执行爬虫过程中发生错误的URL的列表获取、单个获取、删除等操作。

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
     - /logs
     - 获取失败URL列表
   * - GET
     - /log/{id}
     - 获取失败URL
   * - DELETE
     - /log/{id}
     - 删除失败URL
   * - DELETE
     - /all
     - 删除所有失败URL

获取失败URL列表
===============

请求
----

::

    GET /api/admin/failureurl/logs

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
     - 每页记录数
   * - ``page``
     - Integer
     - 否
     - 页码
   * - ``url``
     - String
     - 否
     - URL过滤
   * - ``errorCountMin``
     - Integer
     - 否
     - 最小错误次数过滤
   * - ``errorCountMax``
     - Integer
     - 否
     - 最大错误次数过滤
   * - ``errorName``
     - String
     - 否
     - 错误名称过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "threadName": "Crawler-1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": 1738144800000,
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": 1738143000000,
            "configId": "webConfig_id_1"
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
   * - ``threadName``
     - 线程名称
   * - ``errorName``
     - 错误名称
   * - ``errorLog``
     - 错误日志
   * - ``errorCount``
     - 错误发生次数
   * - ``lastAccessTime``
     - 最后访问时刻（epoch毫秒）
   * - ``configId``
     - 爬虫配置ID

获取失败URL
===========

请求
----

::

    GET /api/admin/failureurl/log/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "threadName": "Crawler-1",
          "errorName": "ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": 3,
          "lastAccessTime": 1738144800000,
          "configId": "webConfig_id_1"
        }
      }
    }

删除失败URL
===========

请求
----

::

    DELETE /api/admin/failureurl/log/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

删除所有失败URL
===============

删除所有失败URL。没有参数。

请求
----

::

    DELETE /api/admin/failureurl/all

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
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

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

按错误次数过滤
--------------

.. code-block:: bash

    # 仅获取发生3次以上错误的URL
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

按错误名称过滤
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取失败URL
-----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除失败URL
-----------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除所有失败URL
---------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

按错误类型统计
--------------

.. code-block:: bash

    # 按错误类型计数
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`api-admin-joblog` - 作业日志API
- :doc:`../../admin/failureurl-guide` - 失败URL管理指南
