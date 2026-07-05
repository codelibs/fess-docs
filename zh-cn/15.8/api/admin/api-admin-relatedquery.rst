==========================
RelatedQuery API
==========================

概述
====

RelatedQuery API是用于管理 |Fess| 相关查询的API。
您可以为用户输入的搜索关键词（``term``）注册并管理相关的搜索关键词候选
（``queries``）。注册的相关查询将在搜索界面中作为相关搜索候选显示。

有关认证方式、通用响应格式（``version`` 字段和 ``status`` 状态码）、
分页以及错误响应的详细信息，请参阅 :doc:`api-admin-overview`。

基础URL
=======

::

    /api/admin/relatedquery

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
     - 获取相关查询列表
   * - GET
     - /setting/{id}
     - 获取相关查询
   * - POST
     - /setting
     - 创建相关查询
   * - PUT
     - /setting
     - 更新相关查询
   * - DELETE
     - /setting/{id}
     - 删除相关查询

获取相关查询列表
================

请求
----

::

    GET /api/admin/relatedquery/settings

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
     - 每页记录数（默认：25。可通过 ``fess_config.properties`` 的 ``paging.page.size`` 更改）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始。默认：1）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   每条设置均包含 ``versionNo``（用于乐观锁的版本号）。``virtualHost``
   以及审计字段（``createdBy``、``createdTime``、``updatedBy``、``updatedTime``）
   仅在有值时才会包含在响应中。值为空的 ``virtualHost`` 不会包含在响应中。

获取相关查询
============

请求
----

::

    GET /api/admin/relatedquery/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

创建相关查询
============

请求
----

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 字段
     - 必需
     - 说明
   * - ``term``
     - 是
     - 搜索关键词（最多10000个字符）
   * - ``queries``
     - 是
     - 相关查询。每行一条，以换行符分隔的字符串（空行将被忽略。最多10000个字符）
   * - ``virtualHost``
     - 否
     - 虚拟主机（最多1000个字符）

.. note::

   ``crudMode`` 由API端自动设置，无需包含在请求体中。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

更新相关查询
============

请求
----

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
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
     - 待更新的相关查询ID（最多1000个字符）
   * - ``term``
     - 是
     - 搜索关键词（最多10000个字符）
   * - ``queries``
     - 是
     - 相关查询。每行一条，以换行符分隔的字符串（空行将被忽略。最多10000个字符）
   * - ``virtualHost``
     - 否
     - 虚拟主机（最多1000个字符）
   * - ``versionNo``
     - 是
     - 用于乐观锁的版本号。请指定获取时响应中包含的值

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

删除相关查询
============

请求
----

::

    DELETE /api/admin/relatedquery/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

错误响应
========

当请求失败时，``status`` 将被设置为非 0 的值，``message`` 中包含错误内容。
例如，缺少必填字段等验证错误时，``status`` 为 ``1``。
有关状态码的列表，请参阅 :doc:`api-admin-overview`。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "..."
      }
    }

使用示例
========

产品相关查询
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

帮助相关查询
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-relatedcontent` - 相关内容API
- :doc:`api-admin-suggest` - 建议管理API
- :doc:`../../admin/relatedquery-guide` - 相关查询管理指南
