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
   * - GET
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
     - 每页记录数（默认：25。可通过 ``fess_config.properties`` 的 ``paging.page.size`` 修改）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认：1。指定0或以下时视为1）
   * - ``id``
     - String
     - 否
     - 按指定的角色ID进行完全匹配过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "role_id_1",
            "name": "admin",
            "versionNo": 1
          },
          {
            "id": "role_id_2",
            "name": "user",
            "versionNo": 1
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
          "name": "admin",
          "versionNo": 1
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
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 角色名称（最大100个字符）
   * - ``attributes``
     - 否
     - 属性的映射。值以字符串指定

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

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``id``
     - 是
     - 要更新的角色ID
   * - ``name``
     - 是
     - 角色名称（最大100个字符）
   * - ``attributes``
     - 否
     - 属性的映射。值以字符串指定
   * - ``versionNo``
     - 是
     - 乐观锁的版本号。指定从获取角色获得的 ``versionNo`` 值

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

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-user` - 用户管理API
- :doc:`api-admin-group` - 组管理API
- :doc:`../../admin/role-guide` - 角色管理指南
