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
   * - GET
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
     - 每页记录数（默认：25）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认：1）
   * - ``id``
     - String
     - 否
     - 按指定的组ID进行完全匹配过滤

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
            "attributes": {
              "gidNumber": "1000"
            },
            "versionNo": 1
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "attributes": {
              "gidNumber": "1001"
            },
            "versionNo": 1
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
          "attributes": {
            "gidNumber": "1000"
          },
          "versionNo": 1
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
      "attributes": {
        "gidNumber": "1002"
      }
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
     - 组名称（最大100个字符）
   * - ``attributes``
     - 否
     - 属性的映射（包含 ``gidNumber`` 等LDAP属性）。值以字符串指定

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
      "attributes": {
        "gidNumber": "1002"
      },
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
     - 要更新的组ID
   * - ``name``
     - 是
     - 组名称（最大100个字符）
   * - ``attributes``
     - 否
     - 属性的映射（包含 ``gidNumber`` 等LDAP属性）。值以字符串指定
   * - ``versionNo``
     - 是
     - 乐观锁的版本号。指定从获取组获得的 ``versionNo`` 值

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
           "attributes": {
             "gidNumber": "2000"
           }
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

