==========================
Storage API
==========================

概述
==========

Storage API是用于管理 |Fess| 对象存储的API。
您可以获取存储中文件和目录的列表，并执行文件的下载、删除和上传操作。

基础URL
==========

::

    /api/admin/storage

认证
==========

Storage API所属的Admin API全部端点均需要通过访问令牌进行认证。
请在请求的 ``Authorization`` 头中指定访问令牌。

::

    Authorization: Bearer <访问令牌>

有关访问令牌的获取方法及所需权限（默认为 ``admin-api`` 角色）的详细信息，
请参阅 :doc:`api-admin-overview`。

端点列表
==========

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
     - /upload
     - 上传文件

获取文件和目录列表
====================

返回指定目录下文件和目录的列表。
``{id}`` 中指定通过列表获取操作得到的目录 ``id``\ 。省略 ``{id}`` 时获取根目录的列表。

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
     - 经过编码的标识符。将对象路径以URL安全的Base64编码后的字符串，用于下载和删除时的 ``{id}``\ 。
   * - ``path``
     - 父目录的路径
   * - ``name``
     - 文件名或目录名
   * - ``hashCode``
     - 内部处理使用的哈希值（并非表示对象内容的稳定值）
   * - ``size``
     - 大小（字节）
   * - ``directory``
     - 是否为目录（boolean）
   * - ``lastModified``
     - 最后修改时间（ISO 8601格式，仅文件包含此字段）

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
==========

下载存储中的文件。\ ``{id}`` 中指定通过列表获取操作得到的 ``id``\ 。
响应以 ``application/octet-stream`` 流的形式返回。

请求
----

::

    GET /api/admin/storage/download/{id}

响应
----

文件的二进制流（``Content-Type: application/octet-stream``）。

.. note::

   此API的响应不附带 ``Content-Disposition`` 头。
   请由客户端侧指定保存时的文件名（使用cURL时请使用 ``-o`` 选项）。

删除文件
==========

删除存储中的文件。\ ``{id}`` 中指定通过列表获取操作得到的 ``id``\ 。

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
==========

将文件上传到存储。以 ``multipart/form-data`` 格式发送。
上传目标目录通过表单字段 ``path`` 指定，而非通过URL路径指定。

请求
----

::

    PUT /api/admin/storage/upload
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
     - 上传目标的目录路径（首尾无需加斜杠）。未指定时保存至根目录（存储桶直下）。
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

错误
==========

各端点在处理失败时，将返回 ``status`` 为非 0 值（验证错误时为 ``1``）的响应。
响应正文的 ``message`` 中包含错误详情。有关状态值和HTTP状态码的详细信息，请参阅 :doc:`api-admin-overview`。

主要错误情况如下所示。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 发生错误的主要情况
   * - 获取文件和目录列表
     - 获取数量超过上限时
   * - 下载文件
     - ``id`` 无效，或下载失败时
   * - 删除文件
     - ``id`` 无效，或删除失败时
   * - 上传文件
     - 未指定 ``file``，或上传失败时

使用示例
==========

获取根目录列表
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

下载文件
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

删除文件
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

上传文件
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

参考信息
==========

- :doc:`api-admin-overview` - Admin API概述
