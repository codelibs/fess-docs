==========================
KeyMatch API
==========================

概述
====

KeyMatch API是用于管理 |Fess| 关键词匹配（搜索关键词与结果的关联）的API。
您可以设置特定关键词对应的特定文档优先显示。

基础URL
=======

::

    /api/admin/keymatch

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
     - 获取关键词匹配列表
   * - GET
     - /setting/{id}
     - 获取关键词匹配
   * - POST
     - /setting
     - 创建关键词匹配
   * - PUT
     - /setting
     - 更新关键词匹配
   * - DELETE
     - /setting/{id}
     - 删除关键词匹配

获取关键词匹配列表
==================

请求
----

::

    GET /api/admin/keymatch/settings

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
     - 每页记录数（默认：25，取自 ``paging.page.size`` 的设置值）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认：1）
   * - ``term``
     - String
     - 否
     - 按搜索关键词筛选（通配符匹配）
   * - ``query``
     - String
     - 否
     - 按匹配条件查询筛选（通配符匹配）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``total`` 中设置的是符合筛选条件的总记录数（而非当前页的记录数）。
   各设置对象除上述字段外，若有值则还会包含 ``virtualHost`` 、
   ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、 ``updatedTime`` 。

获取关键词匹配
==============

请求
----

::

    GET /api/admin/keymatch/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "maxSize": 10,
          "boost": 10.0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   ``versionNo`` 是用于乐观锁的版本号。更新关键词匹配时，请在请求体中指定获取时得到的
   ``versionNo`` 。若指定的ID不存在，则返回错误。

创建关键词匹配
==============

请求
----

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "maxSize": 5,
      "boost": 20.0
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 字段
     - 类型
     - 必需
     - 说明
   * - ``term``
     - String
     - 是
     - 搜索关键词（最大100个字符）
   * - ``query``
     - String
     - 是
     - 匹配条件查询（最大长度取决于 ``form.admin.max.input.size`` 的设置值）
   * - ``maxSize``
     - Integer
     - 是
     - 最大显示数量（0以上的整数，管理界面初始值为10）
   * - ``boost``
     - Float
     - 是
     - 提升值（管理界面初始值为100.0）
   * - ``virtualHost``
     - String
     - 否
     - 虚拟主机名（最大1000个字符，用于按虚拟主机切换关键词匹配时指定）

.. note::

   ``maxSize`` 和 ``boost`` 在通过API调用时为必填项。初始值是管理界面表单中显示的值，
   不适用于API。若省略则会返回验证错误。
   另外，即使在请求中指定了 ``createdBy`` 和 ``createdTime`` ，服务器端也会将其覆盖。

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

更新关键词匹配
==============

请求
----

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

字段说明
~~~~~~~~

在创建时的字段（ ``term`` 、 ``query`` 、 ``maxSize`` 、 ``boost`` 、 ``virtualHost`` ）基础上，
还需指定以下字段。

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 字段
     - 类型
     - 必需
     - 说明
   * - ``id``
     - String
     - 是
     - 待更新的关键词匹配ID（最大1000个字符）
   * - ``versionNo``
     - Integer
     - 是
     - 乐观锁用版本号，请指定获取时得到的值

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

删除关键词匹配
==============

请求
----

::

    DELETE /api/admin/keymatch/setting/{id}

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

创建产品页面关键词匹配
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

创建支持页面关键词匹配
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "maxSize": 5,
           "boost": 20.0
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/keymatch-guide` - 关键词匹配管理指南
