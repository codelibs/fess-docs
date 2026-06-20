==========================
FileConfig API
==========================

概述
====

FileConfig API是用于管理 |Fess| 文件爬虫设置的API。
可以操作本地文件系统、SMB/CIFS共享文件夹、FTP、各类对象存储等的爬虫设置。

基础URL
=======

::

    /api/admin/fileconfig

.. note::

   所有端点均需要管理员权限及有效的访问令牌。
   有关认证方式，请参阅 :doc:`api-admin-overview` 。

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
     - 获取文件爬虫设置列表
   * - GET
     - /setting/{id}
     - 获取文件爬虫设置
   * - POST
     - /setting
     - 创建文件爬虫设置
   * - PUT
     - /setting
     - 更新文件爬虫设置
   * - DELETE
     - /setting/{id}
     - 删除文件爬虫设置

获取文件爬虫设置列表
====================

请求
----

::

    GET /api/admin/fileconfig/settings

.. note::

   列表获取端点除 ``GET`` 外，也可使用 ``PUT`` 访问。

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认：1）
   * - ``size``
     - Integer
     - 否
     - 每页记录数（默认：25。遵循 ``paging.page.size`` 设置）
   * - ``name``
     - String
     - 否
     - 按设置名称筛选
   * - ``paths``
     - String
     - 否
     - 按爬虫路径筛选
   * - ``description``
     - String
     - 否
     - 按说明筛选

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "fileconfig_id_1",
            "name": "Shared Documents",
            "description": "共享文档",
            "paths": "smb://server/share/documents",
            "includedPaths": ".*\\.pdf$",
            "excludedPaths": ".*/(temp|cache)/.*",
            "includedDocPaths": "",
            "excludedDocPaths": "",
            "configParameter": "",
            "depth": 10,
            "maxAccessCount": 1000,
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

``total`` 表示符合条件的设置总数。

获取文件爬虫设置
================

请求
----

::

    GET /api/admin/fileconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "fileconfig_id_1",
          "name": "Shared Documents",
          "description": "共享文档",
          "paths": "smb://server/share/documents",
          "includedPaths": ".*\\.pdf$",
          "excludedPaths": ".*/(temp|cache)/.*",
          "includedDocPaths": "",
          "excludedDocPaths": "",
          "configParameter": "",
          "depth": 10,
          "maxAccessCount": 1000,
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   响应中包含在注册和更新时由服务器自动设置的 ``createdBy`` 、 ``createdTime`` 、
   ``updatedBy`` 、 ``updatedTime`` 、 ``versionNo`` 字段。
   ``versionNo`` 在更新时为必填项（请参阅后述的"更新文件爬虫设置"）。

创建文件爬虫设置
================

请求
----

::

    POST /api/admin/fileconfig/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx)$",
      "excludedPaths": ".*/(temp|backup)/.*",
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 设置名称（最多200个字符）
   * - ``description``
     - 否
     - 设置说明（最多1000个字符）
   * - ``paths``
     - 是
     - 爬虫起始路径（多个路径用换行符分隔）。使用 ``file:`` 、 ``smb:`` 、 ``smb1:`` 、 ``ftp:`` 、 ``storage:`` 、 ``s3:`` 、 ``gcs:`` 中的一种协议指定
   * - ``includedPaths``
     - 否
     - 爬虫目标路径的正则表达式模式
   * - ``excludedPaths``
     - 否
     - 排除爬虫路径的正则表达式模式
   * - ``includedDocPaths``
     - 否
     - 索引目标路径的正则表达式模式
   * - ``excludedDocPaths``
     - 否
     - 排除索引路径的正则表达式模式
   * - ``configParameter``
     - 否
     - 附加配置参数（ ``key=value`` 格式，每行一项）
   * - ``depth``
     - 否
     - 爬虫深度（0以上）
   * - ``maxAccessCount``
     - 否
     - 最大访问数（0以上）
   * - ``numOfThread``
     - 是
     - 并行线程数（1以上）
   * - ``intervalTime``
     - 是
     - 访问间隔（毫秒，0以上）
   * - ``boost``
     - 是
     - 搜索结果提升值
   * - ``available``
     - 是
     - 启用/禁用（字符串 ``"true"`` / ``"false"``）
   * - ``sortOrder``
     - 是
     - 显示顺序（0以上）
   * - ``permissions``
     - 否
     - 访问权限角色（多个时用换行符分隔）
   * - ``virtualHosts``
     - 否
     - 虚拟主机（多个时用换行符分隔）

.. note::

   ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、 ``updatedTime`` 等审计字段
   由服务器自动设置，无需在请求体中指定。

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_fileconfig_id",
        "created": true
      }
    }

更新文件爬虫设置
================

请求
----

::

    PUT /api/admin/fileconfig/setting
    Content-Type: application/json

请求体
~~~~~~

更新时，除创建时的字段外，还需要指定用于确定更新目标的 ``id`` 和版本号 ``versionNo`` 。
``versionNo`` 需填写获取API（GET）响应中包含的当前值。

.. code-block:: json

    {
      "id": "existing_fileconfig_id",
      "name": "Updated Local Files",
      "paths": "file:///data/documents",
      "includedPaths": ".*\\.(pdf|doc|docx|xls|xlsx|ppt|pptx)$",
      "excludedPaths": ".*/(temp|backup|archive)/.*",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 3,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

更新时的附加字段
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 字段
     - 必需
     - 说明
   * - ``id``
     - 是
     - 更新目标的设置ID（最多1000个字符）
   * - ``versionNo``
     - 是
     - 更新目标的当前版本号。填写获取API（GET）响应中包含的 ``versionNo`` 值

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_fileconfig_id",
        "created": false
      }
    }

删除文件爬虫设置
================

请求
----

::

    DELETE /api/admin/fileconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

路径格式
========

``paths`` 可使用以下协议（支持的协议可通过 ``crawler.file.protocols`` 设置更改）。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 协议
     - 路径格式
   * - 本地文件
     - ``file:///path/to/directory``
   * - SMB/CIFS共享
     - ``smb://server/share/path``
   * - SMB/CIFS共享（SMB1）
     - ``smb1://server/share/path``
   * - FTP
     - ``ftp://server/path``
   * - S3兼容对象存储（MinIO等）
     - ``storage://bucket/path``
   * - Amazon S3
     - ``s3://bucket/path``
   * - Google Cloud Storage
     - ``gcs://bucket/path``

.. note::

   SMB/CIFS及FTP的认证信息（用户名和密码）请勿嵌入路径中，
   应通过"文件认证"设置进行配置。详情请参阅 :doc:`../../admin/fileauth-guide` 。

使用示例
========

本地文件爬虫设置
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Local Files",
           "paths": "file:///data/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|backup)/.*",
           "numOfThread": 2,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

SMB共享爬虫设置
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

.. note::

   如果访问SMB共享需要认证，请事先在"文件认证"设置中注册目标主机的认证信息。

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-webconfig` - Web爬虫设置API
- :doc:`api-admin-dataconfig` - 数据存储设置API
- :doc:`../../admin/fileconfig-guide` - 文件爬虫设置指南
- :doc:`../../admin/fileauth-guide` - 文件认证设置指南
