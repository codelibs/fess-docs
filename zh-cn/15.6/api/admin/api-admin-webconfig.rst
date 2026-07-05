==========================
WebConfig API
==========================

概述
====

WebConfig API是用于管理 |Fess| Web爬虫设置的API。
您可以操作爬虫目标URL、爬虫深度、排除模式等设置。

基础URL
=======

::

    /api/admin/webconfig

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
     - 获取Web爬虫设置列表
   * - GET
     - /setting/{id}
     - 获取Web爬虫设置
   * - POST
     - /setting
     - 创建Web爬虫设置
   * - PUT
     - /setting
     - 更新Web爬虫设置
   * - DELETE
     - /setting/{id}
     - 删除Web爬虫设置

获取Web爬虫设置列表
==================

请求
----

::

    GET /api/admin/webconfig/settings
    PUT /api/admin/webconfig/settings

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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "",
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

获取Web爬虫设置
==============

请求
----

::

    GET /api/admin/webconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "",
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

创建Web爬虫设置
==============

请求
----

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 3,
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
   * - ``urls``
     - 是
     - 爬虫起始URL（多个URL用换行符分隔）
   * - ``includedUrls``
     - 否
     - 爬虫目标URL的正则表达式模式
   * - ``excludedUrls``
     - 否
     - 排除爬虫URL的正则表达式模式
   * - ``includedDocUrls``
     - 否
     - 索引目标URL的正则表达式模式
   * - ``excludedDocUrls``
     - 否
     - 排除索引URL的正则表达式模式
   * - ``configParameter``
     - 否
     - 附加配置参数
   * - ``depth``
     - 否
     - 爬虫深度（默认：-1=无限制）
   * - ``maxAccessCount``
     - 否
     - 最大访问数（默认：100）
   * - ``userAgent``
     - 否
     - 自定义User-Agent
   * - ``numOfThread``
     - 否
     - 并行线程数（默认：1）
   * - ``intervalTime``
     - 否
     - 请求间隔（毫秒，默认：0）
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
        "id": "new_webconfig_id",
        "created": true
      }
    }

更新Web爬虫设置
==============

请求
----

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
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
        "id": "existing_webconfig_id",
        "created": false
      }
    }

删除Web爬虫设置
==============

请求
----

::

    DELETE /api/admin/webconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_webconfig_id",
        "created": false
      }
    }

URL模式示例
===========

includedUrls / excludedUrls
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 模式
     - 说明
   * - ``.*example\\.com.*``
     - 包含example.com的所有URL
   * - ``https://example\\.com/docs/.*``
     - 仅/docs/目录下
   * - ``.*\\.(pdf|doc|docx)$``
     - PDF、DOC、DOCX文件
   * - ``.*\\?.*``
     - 带查询参数的URL
   * - ``.*/(login|logout|admin)/.*``
     - 包含特定路径的URL

使用示例
========

企业网站爬虫设置
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "available": true,
           "permissions": ["guest"]
         }'

文档网站爬虫设置
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": true,
           "labelTypeIds": ["documentation_label_id"]
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-fileconfig` - 文件爬虫设置API
- :doc:`api-admin-dataconfig` - 数据存储设置API
- :doc:`../../admin/webconfig-guide` - Web爬虫设置指南

