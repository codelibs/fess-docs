==========================
Storage API
==========================

概述
====

Storage API是用于管理 |Fess| 对象存储的API。
您可以获取存储中文件和目录的列表，并执行文件的下载、删除和上传操作。

基础URL
=======

::

    /api/admin/storage

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /list/{id}
     - 获取文件和目录列表
   * - GET
     - /download/{id}
     - 下载文件
   * - DELETE
     - /delete/{id}
     - 删除文件
   * - PUT
     - /upload/{pathId}
     - 上传文件

获取文件和目录列表
==================

返回指定目录下文件和目录的列表。
``{id}`` 中指定经过编码的路径。省略 ``{id}`` 时获取根目录的列表。

请求
----

::

    GET /api/admin/storage/list/{id}

响应
----

``items`` 中存放表示文件和目录信息的对象数组（目录在前，文件在后的顺序）。
每个对象具有以下字段。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``id``
     - 经过编码的标识符（用于下载和删除时的 ``{id}``）
   * - ``path``
     - 父路径
   * - ``name``
     - 文件名或目录名
   * - ``hashCode``
     - 哈希码
   * - ``size``
     - 大小（字节）
   * - ``directory``
     - 是否为目录（boolean）
   * - ``lastModified``
     - 最后修改时间（仅文件）

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

下载文件
========

下载存储中的文件。``{id}`` 中指定列表获取时得到的 ``id``。
响应以 ``application/octet-stream`` 流的形式返回。

请求
----

::

    GET /api/admin/storage/download/{id}

响应
----

文件的二进制流（``Content-Type: application/octet-stream``）。

删除文件
========

删除存储中的文件。``{id}`` 中指定列表获取时得到的 ``id``。

请求
----

::

    DELETE /api/admin/storage/delete/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

上传文件
========

将文件上传到存储。以 ``multipart/form-data`` 格式发送。

请求
----

::

    PUT /api/admin/storage/upload/{pathId}
    Content-Type: multipart/form-data

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``path``
     - 否
     - 上传目标路径（未指定时为默认位置）
   * - ``file``
     - 是
     - 要上传的文件

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

使用示例
========

获取根目录列表
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

下载文件
--------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

删除文件
--------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

上传文件
--------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
