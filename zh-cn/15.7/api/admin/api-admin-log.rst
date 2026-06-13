==========================
Log API
==========================

概述
====

Log API是用于参阅和下载 |Fess| 日志文件的API。
您可以获取服务器上输出的日志文件列表，并下载单个日志文件。

基础URL
=======

::

    /api/admin/log

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /files
     - 获取日志文件列表
   * - GET
     - /file/{id}
     - 下载日志文件

获取日志文件列表
================

返回服务器日志输出目录中存在的日志文件（``.log`` 和 ``.log.gz``）的列表。

请求
----

::

    GET /api/admin/log/files

响应
----

``files`` 中存放表示各日志文件信息的对象数组，``total`` 中存放数量。
每个对象具有以下字段。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``id``
     - 对文件名进行 Base64 URL 编码后的值（用于下载时的 ``{id}``）
   * - ``name``
     - 日志文件名
   * - ``lastModified``
     - 最后修改时间

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

下载日志文件
============

下载指定日志文件的内容。
``{id}`` 中指定列表获取时得到的 ``id`` （对文件名进行 Base64 编码后的值）。
响应以 ``application/octet-stream`` 流的形式返回。
如果指定了不存在的文件名或不允许作为日志文件的名称，则返回空响应。

请求
----

::

    GET /api/admin/log/file/{id}

响应
----

日志文件的二进制流（``Content-Type: application/octet-stream``）。

使用示例
========

获取日志文件列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

下载日志文件
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-backup` - 备份API
