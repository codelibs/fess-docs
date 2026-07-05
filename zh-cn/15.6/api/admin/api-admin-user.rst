==========================
User API
==========================

概述
====

User API是用于管理 |Fess| 用户账户的API。
您可以创建、更新、删除用户以及设置权限等。

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
   * - GET/PUT
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
    PUT /api/admin/user/settings

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
            "id": "user_id_1",
            "name": "admin",
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "roles": ["admin"],
            "groups": []
          }
        ],
        "total": 10
      }
    }

获取用户
========

请求
----

::

    GET /api/admin/user/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "user_id_1",
          "name": "admin",
          "surname": "Administrator",
          "givenName": "System",
          "mail": "admin@example.com",
          "telephoneNumber": "",
          "homePhone": "",
          "homePostalAddress": "",
          "labeledUri": "",
          "roomNumber": "",
          "description": "",
          "title": "",
          "pager": "",
          "street": "",
          "postalCode": "",
          "physicalDeliveryOfficeName": "",
          "destinationIndicator": "",
          "internationaliSDNNumber": "",
          "state": "",
          "employeeNumber": "",
          "facsimileTelephoneNumber": "",
          "postOfficeBox": "",
          "initials": "",
          "carLicense": "",
          "mobile": "",
          "postalAddress": "",
          "city": "",
          "teletexTerminalIdentifier": "",
          "x121Address": "",
          "businessCategory": "",
          "registeredAddress": "",
          "displayName": "",
          "preferredLanguage": "",
          "departmentNumber": "",
          "uidNumber": "",
          "gidNumber": "",
          "homeDirectory": "",
          "roles": ["admin"],
          "groups": []
        }
      }
    }

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
      "surname": "Test",
      "givenName": "User",
      "mail": "testuser@example.com",
      "roles": ["user"],
      "groups": ["group_id_1"]
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
     - 用户名（登录ID）
   * - ``password``
     - 是
     - 密码
   * - ``surname``
     - 否
     - 姓
   * - ``givenName``
     - 否
     - 名
   * - ``mail``
     - 否
     - 电子邮件地址
   * - ``telephoneNumber``
     - 否
     - 电话号码
   * - ``roles``
     - 否
     - 角色ID数组
   * - ``groups``
     - 否
     - 组ID数组

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

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
      "surname": "Test",
      "givenName": "User Updated",
      "mail": "testuser.updated@example.com",
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

删除用户
========

请求
----

::

    DELETE /api/admin/user/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

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
           "surname": "Doe",
           "givenName": "John",
           "mail": "john.doe@example.com",
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

