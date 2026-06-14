==========================
AccessToken API
==========================

概述
====

AccessToken API是用于管理 |Fess| API访问令牌的API。
您可以创建、更新、删除令牌等。

基础URL
=======

::

    /api/admin/accesstoken

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
     - 获取访问令牌列表
   * - GET
     - /setting/{id}
     - 获取访问令牌
   * - POST
     - /setting
     - 创建访问令牌
   * - PUT
     - /setting
     - 更新访问令牌
   * - DELETE
     - /setting/{id}
     - 删除访问令牌

获取访问令牌列表
================

请求
----

::

    GET /api/admin/accesstoken/settings

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expires": "2025-01-01T00:00:00",
            "permissions": "{role}admin"
          }
        ],
        "total": 5
      }
    }

获取访问令牌
============

请求
----

::

    GET /api/admin/accesstoken/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "token",
          "expires": "2025-01-01T00:00:00",
          "permissions": "{role}admin"
        }
      }
    }

创建访问令牌
============

请求
----

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "parameterName": "token",
      "expires": "2026-01-01T00:00:00",
      "permissions": "{role}user"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 令牌名称
   * - ``token``
     - 否
     - 令牌字符串（未指定时自动生成）
   * - ``parameterName``
     - 否
     - 参数名称（默认："token"）
   * - ``expires``
     - 否
     - 过期时间（ISO 8601格式的字符串。例如：``2026-01-01T00:00:00``）
   * - ``permissions``
     - 否
     - 允许的权限。使用换行分隔的字符串指定（例如：``{role}admin``）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "created": true
      }
    }

更新访问令牌
============

请求
----

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "parameterName": "token",
      "expires": "2026-01-01T00:00:00",
      "permissions": "{role}user\n{role}editor",
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

删除访问令牌
============

请求
----

::

    DELETE /api/admin/accesstoken/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用示例
========

创建API令牌
-----------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "External App Token",
           "parameterName": "token",
           "permissions": "{role}guest"
         }'

使用令牌调用API
---------------

.. code-block:: bash

    # 使用令牌作为参数
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # 使用令牌作为Authorization头
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../api-search` - 搜索API
- :doc:`../../admin/accesstoken-guide` - 访问令牌管理指南

