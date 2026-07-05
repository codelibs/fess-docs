==========================
Group API
==========================

概述
====

Group API是用于管理 |Fess| 组的API。
您可以创建、更新、删除组等。

基础URL
=======

::

    /api/admin/group

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
     - 获取组列表
   * - GET
     - /setting/{id}
     - 获取组
   * - POST
     - /setting
     - 创建组
   * - PUT
     - /setting
     - 更新组
   * - DELETE
     - /setting/{id}
     - 删除组

获取组列表
==========

请求
----

::

    GET /api/admin/group/settings
    PUT /api/admin/group/settings

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
            "id": "group_id_1",
            "name": "Engineering",
            "gidNumber": 1000
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "gidNumber": 1001
          }
        ],
        "total": 5
      }
    }

获取组
======

请求
----

::

    GET /api/admin/group/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "gidNumber": 1000
        }
      }
    }

创建组
======

请求
----

::

    POST /api/admin/group/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "gidNumber": 1002
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
     - 组名称
   * - ``gidNumber``
     - 否
     - 组ID编号

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

更新组
======

请求
----

::

    PUT /api/admin/group/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "gidNumber": 1002,
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

删除组
======

请求
----

::

    DELETE /api/admin/group/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

使用示例
========

创建新组
--------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "gidNumber": 2000
         }'

获取组列表
----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-user` - 用户管理API
- :doc:`api-admin-role` - 角色管理API
- :doc:`../../admin/group-guide` - 组管理指南

