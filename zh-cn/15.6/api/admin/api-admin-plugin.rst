==========================
Plugin API
==========================

概述
====

Plugin API是用于管理 |Fess| 插件的API。
您可以安装、启用、禁用、删除插件等。

基础URL
=======

::

    /api/admin/plugin

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
     - 获取插件列表
   * - POST
     - /install
     - 安装插件
   * - DELETE
     - /{id}
     - 删除插件

获取插件列表
============

请求
----

::

    GET /api/admin/plugin

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "id": "analysis-kuromoji",
            "name": "Japanese (kuromoji) Analysis Plugin",
            "version": "2.11.0",
            "description": "Japanese language analysis plugin",
            "enabled": true,
            "installed": true
          },
          {
            "id": "analysis-icu",
            "name": "ICU Analysis Plugin",
            "version": "2.11.0",
            "description": "Unicode normalization and collation",
            "enabled": true,
            "installed": true
          }
        ],
        "total": 2
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
     - 插件ID
   * - ``name``
     - 插件名称
   * - ``version``
     - 插件版本
   * - ``description``
     - 插件描述
   * - ``enabled``
     - 启用状态
   * - ``installed``
     - 安装状态

安装插件
========

请求
----

::

    POST /api/admin/plugin/install
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "url": "https://example.com/plugins/my-plugin-1.0.0.zip"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``url``
     - 是
     - 插件下载URL

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully. Restart required.",
        "pluginId": "my-plugin"
      }
    }

删除插件
========

请求
----

::

    DELETE /api/admin/plugin/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin deleted successfully. Restart required."
      }
    }

使用示例
========

获取插件列表
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

安装插件
--------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url": "https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.11.0/analysis-icu-2.11.0.zip"
         }'

删除插件
--------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin/analysis-icu" \
         -H "Authorization: Bearer YOUR_TOKEN"

注意事项
========

- 安装或删除插件后需要重启Fess
- 安装不兼容的插件可能导致Fess无法启动
- 删除插件时请谨慎操作。如果存在依赖关系，可能会影响系统

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-systeminfo` - 系统信息API
- :doc:`../../admin/plugin-guide` - 插件管理指南

