==========================
FileConfig API
==========================

概述
====

FileConfig API是用于管理 |Fess| 文件爬虫设置的API。
您可以操作文件系统和SMB/CIFS共享文件夹等的爬虫设置。

基础URL
=======

::

    /api/admin/fileconfig

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET/PUT
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
    PUT /api/admin/fileconfig/settings

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
            "paths": "file://///server/share/documents",
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
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

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
          "paths": "file://///server/share/documents",
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
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

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
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 2,
      "intervalTime": 500,
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
     - 设置名称
   * - ``paths``
     - 是
     - 爬虫起始路径（多个路径用换行符分隔）
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
     - 附加配置参数
   * - ``depth``
     - 否
     - 爬虫深度（默认：-1=无限制）
   * - ``maxAccessCount``
     - 否
     - 最大访问数（默认：100）
   * - ``numOfThread``
     - 否
     - 并行线程数（默认：1）
   * - ``intervalTime``
     - 否
     - 访问间隔（毫秒，默认：0）
   * - ``boost``
     - 否
     - 搜索结果提升值（默认：1.0）
   * - ``available``
     - 否
     - 启用/禁用（默认：true）
   * - ``sortOrder``
     - 否
     - 显示顺序
   * - ``permissions``
     - 否
     - 访问权限角色
   * - ``virtualHosts``
     - 否
     - 虚拟主机
   * - ``labelTypeIds``
     - 否
     - 标签类型ID

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
      "available": true,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_fileconfig_id",
        "created": false
      }
    }

路径格式
========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 协议
     - 路径格式
   * - 本地文件
     - ``file:///path/to/directory``
   * - Windows共享 (SMB)
     - ``file://///server/share/path``
   * - SMB带认证
     - ``smb://username:password@server/share/path``
   * - NFS
     - ``file://///nfs-server/export/path``

使用示例
========

SMB共享爬虫设置
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/fileconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "SMB Share",
           "paths": "smb://user:pass@server/documents",
           "includedPaths": ".*\\.(pdf|doc|docx)$",
           "excludedPaths": ".*/(temp|private)/.*",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 3,
           "intervalTime": 200,
           "available": true,
           "permissions": ["guest"]
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-webconfig` - Web爬虫设置API
- :doc:`api-admin-dataconfig` - 数据存储设置API
- :doc:`../../admin/fileconfig-guide` - 文件爬虫设置指南

