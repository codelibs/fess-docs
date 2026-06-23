==========================
User API
==========================

概述
====

User API是用于管理 |Fess| 用户账户的REST API。
您可以创建、获取、更新、删除用户，以及分配角色和组。

这是一个管理用API，使用时需要通过管理员访问令牌进行认证。
有关认证方式和公共规格，请参阅 :doc:`api-admin-overview`。

所有响应均包装在 ``response`` 对象中，并包含以下公共字段：

- ``version`` ：|Fess| 产品版本字符串。
- ``status`` ：处理结果状态码（``0`` =成功，``1`` =请求错误，``2`` =系统错误，``3`` =未授权，``9`` =失败）。

基础URL
=======

::

    /api/admin/user

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
     - 获取用户列表
   * - GET
     - /setting/{id}
     - 获取用户
   * - POST
     - /setting
     - 创建用户
   * - PUT
     - /setting
     - 更新用户
   * - DELETE
     - /setting/{id}
     - 删除用户

获取用户列表
============

请求
----

::

    GET /api/admin/user/settings

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``size``
     - Integer
     - 否
     - 每页记录数。默认值为配置项 ``paging.page.size`` 的值（默认：25）。
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始）。默认值为1。

.. note::

   在当前实现中，获取用户列表端点不应用 ``size`` 和 ``page`` 参数。
   始终返回第一页，记录数由服务器设置 ``paging.page.size`` 决定（默认：25），并按用户名（``name``）升序排序。
   匹配用户的总数可通过 ``response.total`` 获取。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` ：当前页包含的用户数组。
- ``total`` ：匹配条件的用户总数。

获取用户
========

请求
----

::

    GET /api/admin/user/setting/{id}

在 ``{id}`` 中指定目标用户的文档ID。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["admin"],
          "groups": [],
          "versionNo": 1
        }
      }
    }

.. note::

   ``attributes`` 包含用户存储的所有属性，但不包含 ``name``、``password``、``roles`` 和 ``groups``。
   ``password`` 不包含在响应中。

创建用户
========

请求
----

::

    POST /api/admin/user/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
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
     - 用户名（登录ID）
   * - ``password``
     - 否
     - 密码
   * - ``confirmPassword``
     - 否
     - 确认密码
   * - ``attributes``
     - 否
     - 属性映射（见下文）
   * - ``roles``
     - 否
     - 角色ID数组
   * - ``groups``
     - 否
     - 组ID数组

.. note::

   REST API不执行密码必填检查、``password`` 与 ``confirmPassword`` 的一致性检查，以及密码策略验证（这些仅在管理界面中应用）。
   实际使用中，建议指定有效的 ``password`` 且其值与 ``confirmPassword`` 一致。

``attributes`` 的键为用户实体的属性名（源自LDAP的模式项目名）。
常用的键如下：

- ``surname``、``givenName``、``displayName``、``mail``
- ``telephoneNumber``、``mobile``、``homePhone``
- ``employeeNumber``、``title``、``description``、``homeDirectory``
- ``uidNumber``、``gidNumber``

``uidNumber`` 和 ``gidNumber`` 必须为数值（在更新时会进行类型验证）。
此外，还可以指定许多其他LDAP属性键。

.. note::

   创建时，用户ID（文档ID）会自动生成为用户名的Base64 URL编码值
   （例如，用户名 ``admin`` 对应 ``YWRtaW4=``）。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` ：创建的用户的文档ID。
- ``created`` ：创建成功时为 ``true``。

更新用户
========

请求
----

::

    PUT /api/admin/user/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 字段
     - 必需
     - 说明
   * - ``id``
     - 是
     - 要更新的用户的文档ID。
   * - ``name``
     - 是
     - 用户名（登录ID）
   * - ``versionNo``
     - 是
     - 版本号（用于乐观锁）
   * - ``password``
     - 否
     - 新密码（仅在指定时更新）
   * - ``confirmPassword``
     - 否
     - 确认密码
   * - ``attributes``
     - 否
     - 属性映射（参见"创建用户"）
   * - ``roles``
     - 否
     - 角色ID数组
   * - ``groups``
     - 否
     - 组ID数组

.. note::

   更新时，``id``、``name`` 和 ``versionNo`` 为必填项。
   ``versionNo`` 是获取目标用户（GET）时返回的值，对应OpenSearch文档的版本号。
   如果与当前版本不匹配，请求将被视为冲突并拒绝更新。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` ：更新时为 ``false``。

删除用户
========

请求
----

::

    DELETE /api/admin/user/setting/{id}

在 ``{id}`` 中指定要删除的用户的文档ID。

.. note::

   无法删除当前已登录的用户。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` ：已删除用户的文档ID。

使用示例
========

创建新用户
----------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["user"],
           "groups": []
         }'

更改用户角色
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-role` - 角色管理API
- :doc:`api-admin-group` - 组管理API
- :doc:`../../admin/user-guide` - 用户管理指南
