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
     - 每页显示的记录数（默认：20）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认：1）
   * - ``url``
     - String
     - 否
     - URL过滤（支持通配符 ``*`` ``?``）
   * - ``errorCountMin``
     - Integer
     - 否
     - 错误次数的下限（大于等于指定值）
   * - ``errorCountMax``
     - Integer
     - 否
     - 错误次数的上限（小于等于指定值）
   * - ``errorName``
     - String
     - 否
     - 错误名称过滤（对存储的完全限定类名进行通配符匹配；支持 ``*`` ``?``）

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
            "errorName": "java.net.ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": "3",
            "lastAccessTime": "1738144800000",
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "org.codelibs.fess.exception.ContentNotFoundException",
            "errorLog": "Not found: https://example.com/not-found",
            "errorCount": "1",
            "lastAccessTime": "1738143000000",
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
     - 错误名称（发生的异常的完全限定类名；例如 ``java.net.ConnectException``）
   * - ``errorLog``
     - 错误日志（异常消息或堆栈跟踪）
   * - ``errorCount``
     - 错误发生次数（以字符串形式返回的数值）
   * - ``lastAccessTime``
     - 最后访问时刻（以字符串形式返回的epoch毫秒值）
   * - ``configId``
     - 爬虫配置ID

.. note::

   所有响应字段均以字符串形式返回（JSON string）。``errorCount`` 是以字符串表示的数值，``lastAccessTime`` 是以字符串表示的epoch毫秒值。

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
          "errorName": "java.net.ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": "3",
          "lastAccessTime": "1738144800000",
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

``errorName`` 存储爬虫过程中发生的异常的完全限定类名，与捕获时的内容完全一致。它不是固定的枚举值；根据实际抛出的异常，可能出现任意类名。以下是一些典型示例。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 错误名称（示例）
     - 说明
   * - ``java.net.ConnectException``
     - 连接被拒绝（无法连接到服务器）
   * - ``java.net.UnknownHostException``
     - 主机名无法解析（DNS错误）
   * - ``java.net.SocketTimeoutException``
     - 连接或读取超时
   * - ``javax.net.ssl.SSLException``
     - SSL/TLS握手或证书错误
   * - ``java.io.IOException``
     - I/O错误
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - URL返回的HTTP状态码在 ``crawler.failure.url.status.codes`` 中配置（默认：403、404、410）
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - 内容超过最大长度限制

使用示例
========

获取失败URL列表
---------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=1" \
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

    # errorName存储完全限定类名，请使用通配符指定
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=*ConnectException" \
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
