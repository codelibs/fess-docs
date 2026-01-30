==========================
Role API
==========================

概述
====

Role API是用于管理 |Fess| 角色的API。
您可以创建、更新、删除角色等。

基础URL
=======

::

    /api/admin/role

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
     - 获取角色列表
   * - GET
     - /setting/{id}
     - 获取角色
   * - POST
     - /setting
     - 创建角色
   * - PUT
     - /setting
     - 更新角色
   * - DELETE
     - /setting/{id}
     - 删除角色

获取角色列表
============

请求
----

::

    GET /api/admin/role/settings
    PUT /api/admin/role/settings

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
            "id": "role_id_1",
            "name": "admin"
          },
          {
            "id": "role_id_2",
            "name": "user"
          }
        ],
        "total": 5
      }
    }

获取角色
========

请求
----

::

    GET /api/admin/role/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin"
        }
      }
    }

创建角色
========

请求
----

::

    POST /api/admin/role/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "editor"
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
     - 角色名称

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

更新角色
========

请求
----

::

    PUT /api/admin/role/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

删除角色
========

请求
----

::

    DELETE /api/admin/role/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

使用示例
========

创建新角色
----------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

获取角色列表
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-user` - 用户管理API
- :doc:`api-admin-group` - 组管理API
- :doc:`../../admin/role-guide` - 角色管理指南

