==========================
AccessToken API
==========================

概述
====

AccessToken API是用于管理 |Fess| API访问令牌的API。
可以执行令牌的创建、获取、更新和删除操作。

访问令牌用于通过程序调用 |Fess| 搜索API或Admin API时的认证。
有关包含此API在内的Admin API通用规范（认证方式、响应格式、 ``status`` 取值、错误响应、
HTTP状态码），请参阅 :doc:`api-admin-overview` 。

.. note::

   访问此API需要请求所使用的访问令牌具有与 ``api.admin.access.permissions``
   （默认值 ``{role}admin-api`` ）匹配的权限。

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
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``size``
     - Integer
     - 否
     - 每页记录数（默认：25。可通过 ``paging.page.size`` 修改）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始。默认：1）
   * - ``id``
     - String
     - 否
     - 仅获取指定ID的令牌的过滤条件

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   每个令牌对象中还包含 ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、
   ``updatedTime`` 、 ``versionNo`` 等审计信息和版本信息。
   ``createdTime`` 和 ``updatedTime`` 以自纪元起的毫秒数（数值）表示。
   值为 ``null`` 的字段将从响应中排除。
   ``permissions`` 以换行符（ ``\n`` ）分隔的字符串形式返回。

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
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
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
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
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
     - 令牌名称（最多1000个字符）
   * - ``permissions``
     - 否
     - 授予此令牌的权限。可使用换行符（ ``\n`` ）分隔指定多个权限（例如： ``{role}admin-api`` ）。调用Admin API的令牌需要具有与 ``api.admin.access.permissions`` （默认值 ``{role}admin-api`` ）匹配的权限。
   * - ``parameterName``
     - 否
     - 用于传递附加权限的请求参数名称。当使用此令牌认证的请求中包含此处指定名称的参数时，该参数值将被追加到 ``permissions`` 中。省略时不进行设置。
   * - ``expires``
     - 否
     - 有效期限。以 ``YYYY-MM-DDTHH:MM:SS`` 格式的字符串指定（例如： ``2026-01-01T00:00:00`` ）。省略时为永久有效。

.. note::

   令牌字符串（ ``token`` ）由服务器端自动生成。即使在请求体中指定 ``token``
   也会被忽略。由于创建响应中不包含令牌字符串，请通过"获取访问令牌"
   （ ``GET /setting/{id}`` ）来获取已生成的令牌字符串。

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
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

字段说明
~~~~~~~~

更新时，除创建时的字段外，还使用以下字段。

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``id``
     - 是
     - 待更新的令牌ID
   * - ``versionNo``
     - 是
     - 用于乐观锁的版本号。请指定预先获取的令牌的 ``versionNo`` 。

.. note::

   令牌字符串（ ``token`` ）无法更新。即使在请求体中指定 ``token`` 也会被忽略，
   现有值将被保留。

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
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

使用令牌调用API
---------------

创建的令牌可用于调用搜索API等时的认证。

.. code-block:: bash

    # 将令牌作为Authorization头使用
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # 将令牌作为查询参数使用（需要配置 api.access.token.request.parameter ）
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述（认证、响应格式、错误）
- :doc:`../api-search` - 搜索API
- :doc:`../../admin/accesstoken-guide` - 访问令牌管理指南
