==========================
ElevateWord API
==========================

概述
====

ElevateWord API是用于管理 |Fess| 提升词（特定关键词的搜索排名操作）的API。
您可以针对特定搜索查询，将特定文档置于搜索结果的顶部或底部。

基础URL
=======

::

    /api/admin/elevateword

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
     - 获取提升词列表
   * - GET
     - /setting/{id}
     - 获取提升词
   * - POST
     - /setting
     - 创建提升词
   * - PUT
     - /setting
     - 更新提升词
   * - DELETE
     - /setting/{id}
     - 删除提升词

获取提升词列表
==============

请求
----

::

    GET /api/admin/elevateword/settings
    PUT /api/admin/elevateword/settings

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "",
            "permissions": [],
            "boost": 10.0,
            "targetRole": "",
            "targetLabel": ""
          }
        ],
        "total": 5
      }
    }

获取提升词
==========

请求
----

::

    GET /api/admin/elevateword/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "",
          "permissions": [],
          "boost": 10.0,
          "targetRole": "",
          "targetLabel": ""
        }
      }
    }

创建提升词
==========

请求
----

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "",
      "permissions": ["guest"],
      "boost": 15.0,
      "targetRole": "user",
      "targetLabel": "docs"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``suggestWord``
     - 是
     - 提升目标的关键词
   * - ``reading``
     - 否
     - 读音（日语假名）
   * - ``permissions``
     - 否
     - 访问权限角色
   * - ``boost``
     - 否
     - 提升值（默认：1.0）
   * - ``targetRole``
     - 否
     - 目标角色
   * - ``targetLabel``
     - 否
     - 目标标签

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

更新提升词
==========

请求
----

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "",
      "permissions": ["guest", "user"],
      "boost": 20.0,
      "targetRole": "user",
      "targetLabel": "docs",
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

删除提升词
==========

请求
----

::

    DELETE /api/admin/elevateword/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

使用示例
========

产品名称提升
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 20.0,
           "permissions": ["guest"]
         }'

针对特定标签提升
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 10.0,
           "targetLabel": "technical_docs",
           "permissions": ["guest"]
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-keymatch` - 关键词匹配API
- :doc:`api-admin-boostdoc` - 文档提升API
- :doc:`../../admin/elevateword-guide` - 提升词管理指南

