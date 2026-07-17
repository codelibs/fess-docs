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

认证
====

与其他Admin API相同，需要通过访问令牌进行认证。访问令牌需要具备 ``Radmin-api`` 权限（通过 ``api.admin.access.permissions`` 设置，默认值为 ``Radmin-api``）。
在请求头中指定访问令牌。

::

    Authorization: Bearer <访问令牌>

有关认证及访问令牌获取方式的详细信息，请参阅 :doc:`api-admin-overview`。

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
文件按文件名升序排列后返回。

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

.. note::

   ``version`` 中设置的是当前运行的 |Fess| 的产品版本。\ ``files`` 的内容及数量会根据服务器上的日志文件而变化，上述内容为示例。

下载日志文件
============

下载指定日志文件的内容。
``{id}`` 中直接指定列表获取时返回的 ``id``\ （对文件名进行 Base64 URL 编码后的值）。
响应以 ``application/octet-stream`` 流的形式返回。
出于安全考虑，仅接受以 ``.log`` 或 ``.log.gz`` 结尾的文件名，包含 ``..`` 等路径操作的名称将不被接受。
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
