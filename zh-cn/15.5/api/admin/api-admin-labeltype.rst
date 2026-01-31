==========================
LabelType API
==========================

概述
====

LabelType API是用于管理 |Fess| 标签类型的API。
您可以操作用于搜索结果标签分类和过滤的标签类型。

基础URL
=======

::

    /api/admin/labeltype

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
     - 获取标签类型列表
   * - GET
     - /setting/{id}
     - 获取标签类型
   * - POST
     - /setting
     - 创建标签类型
   * - PUT
     - /setting
     - 更新标签类型
   * - DELETE
     - /setting/{id}
     - 删除标签类型

获取标签类型列表
================

请求
----

::

    GET /api/admin/labeltype/settings
    PUT /api/admin/labeltype/settings

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
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

获取标签类型
============

请求
----

::

    GET /api/admin/labeltype/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "sortOrder": 0,
          "permissions": [],
          "virtualHost": ""
        }
      }
    }

创建标签类型
============

请求
----

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": ["guest"]
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
     - 标签显示名称
   * - ``value``
     - 是
     - 标签值（搜索时使用）
   * - ``includedPaths``
     - 否
     - 标签目标路径的正则表达式（多个用换行符分隔）
   * - ``excludedPaths``
     - 否
     - 标签排除路径的正则表达式（多个用换行符分隔）
   * - ``sortOrder``
     - 否
     - 显示顺序
   * - ``permissions``
     - 否
     - 访问权限角色
   * - ``virtualHost``
     - 否
     - 虚拟主机

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

更新标签类型
============

请求
----

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": ["guest"],
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

删除标签类型
============

请求
----

::

    DELETE /api/admin/labeltype/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_label_id",
        "created": false
      }
    }

使用示例
========

创建文档标签
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": ["guest"]
         }'

使用标签搜索
------------

.. code-block:: bash

    # 使用标签过滤
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../search-api` - 搜索API
- :doc:`../../admin/labeltype-guide` - 标签类型管理指南

