==========================
LabelType API
==========================

概述
====

LabelType API是用于管理 |Fess| 标签类型的API。
使用标签类型，可以根据爬取目标的路径或虚拟主机对搜索结果进行分类，
并在搜索界面中通过标签进行筛选（过滤）。

关于认证方式及响应的通用规范（``status`` 状态码、``version`` 字段、错误格式、
HTTP状态码等），请参阅 :doc:`api-admin-overview`。
访问本API需要使用具有管理API权限（``admin-api``）的访问令牌，
并通过 ``Authorization: Bearer <访问令牌>`` 请求头指定。

基础 URL
========

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
   * - GET
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

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必填
     - 说明
   * - ``size``
     - Integer
     - 否
     - 每页记录数。默认值为 ``paging.page.size`` 的设置值（标准为 ``25``）。
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始）。默认值为 ``1``。
   * - ``name``
     - String
     - 否
     - 按显示名称筛选（通配符搜索）。
   * - ``value``
     - String
     - 否
     - 按标签值筛选（通配符搜索）。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   每个设置对象中还包含用于审计的 ``createdBy`` / ``createdTime`` / ``updatedBy`` /
   ``updatedTime``，以及用于乐观锁的 ``versionNo``（值为 ``null`` 的
   字段将被省略）。``response`` 对象中始终包含表示产品版本的
   ``version``，但为简洁起见，后续示例中可能省略该字段。

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
          "permissions": "{role}admin",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
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
      "permissions": "{role}guest"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``name``
     - String
     - 是
     - 标签显示名称（最多100个字符）。
   * - ``value``
     - String
     - 是
     - 标签值（搜索时通过 ``label`` 参数使用）。只能使用半角英数字和下划线（``_``），且须符合正则表达式 ``^[a-zA-Z0-9_]+$``（最多100个字符）。
   * - ``includedPaths``
     - String
     - 否
     - 作为标签目标的路径正则表达式。指定多个时用换行符（``\n``）分隔。
   * - ``excludedPaths``
     - String
     - 否
     - 从标签目标中排除的路径正则表达式。指定多个时用换行符（``\n``）分隔。
   * - ``permissions``
     - String
     - 否
     - 允许访问的角色/组/用户（例如：``{role}admin``）。指定多个时用换行符（``\n``）分隔。
   * - ``sortOrder``
     - Integer
     - 否
     - 显示顺序（0以上的整数）。未指定时默认为 ``0``。
   * - ``virtualHost``
     - String
     - 否
     - 虚拟主机（最多1000个字符）。

.. note::

   ``createdBy`` / ``createdTime`` 等审计字段由服务器端自动设置，
   无需在请求中指定。

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

创建成功时，``created`` 的值为 ``true``。

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
      "permissions": "{role}guest",
      "versionNo": 1
    }

更新时，除创建时的字段外，还需要以下必填字段。

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``id``
     - String
     - 是
     - 要更新的标签类型ID。
   * - ``versionNo``
     - Integer
     - 是
     - 用于乐观锁的版本号。请指定获取时响应中包含的 ``versionNo``。若指定的版本与当前版本不一致，更新将失败。

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

更新时，``created`` 的值为 ``false``。

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
        "status": 0
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
           "permissions": "{role}guest"
         }'

获取标签类型列表
----------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

使用标签进行搜索
----------------

.. code-block:: bash

    # 使用标签过滤
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../api-search` - 搜索API
- :doc:`../../admin/labeltype-guide` - 标签类型管理指南
