==========================
RelatedContent API
==========================

概述
====

RelatedContent API是用于管理 |Fess| 相关内容的API。
您可以为特定关键词显示自定义的相关内容。

基础URL
=======

::

    /api/admin/relatedcontent

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
     - 获取相关内容列表
   * - GET
     - /setting/{id}
     - 获取相关内容
   * - POST
     - /setting
     - 创建相关内容
   * - PUT
     - /setting
     - 更新相关内容
   * - DELETE
     - /setting/{id}
     - 删除相关内容

获取相关内容列表
================

请求
----

::

    GET /api/admin/relatedcontent/settings

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
     - 页码（从1开始，默认：1。指定0以下的值时按1处理）
   * - ``term``
     - String
     - 否
     - 按搜索关键词筛选（通配符搜索）
   * - ``content``
     - String
     - 否
     - 按内容正文筛选（通配符搜索）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
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

   ``settings`` 的各元素以及单个获取端点返回的 ``setting`` 对象中，包含所存储实体的字段原始值。除
   ``term``、``content``、``sortOrder``、``virtualHost`` 之外，审计字段
   ``createdBy``、``createdTime``、``updatedBy``、``updatedTime`` 以及
   乐观锁字段 ``versionNo`` 也会一并返回。\ ``createdTime`` 和
   ``updatedTime`` 以自纪元以来的毫秒数（数值）表示。未设置（null）的字段
   将从响应中省略。此外，所有响应的 ``response`` 对象中始终包含表示
   产品版本的 ``version``\ （详情请参阅 :doc:`api-admin-overview`）。

获取相关内容
============

请求
----

::

    GET /api/admin/relatedcontent/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
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

.. note::

   更新（PUT）时所需的 ``versionNo``，请指定此获取响应中包含的值。

创建相关内容
============

请求
----

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``term``
     - 是
     - 搜索关键词（最多10000个字符）
   * - ``content``
     - 是
     - 要显示的HTML内容（最多10000个字符）
   * - ``sortOrder``
     - 否
     - 显示顺序（0到2147483647之间的整数）
   * - ``virtualHost``
     - 否
     - 虚拟主机（最多1000个字符）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

更新相关内容
============

请求
----

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
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
     - 要更新的相关内容ID（最多1000个字符）
   * - ``term``
     - 是
     - 搜索关键词（最多10000个字符）
   * - ``content``
     - 是
     - 要显示的HTML内容（最多10000个字符）
   * - ``sortOrder``
     - 否
     - 显示顺序（0到2147483647之间的整数）
   * - ``virtualHost``
     - 否
     - 虚拟主机（最多1000个字符）
   * - ``versionNo``
     - 是
     - 乐观锁用的版本号。请指定 ``setting/{id}`` 响应中包含的值。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   即使在请求体中包含 ``createdBy``、``createdTime``、``updatedBy``、
   ``updatedTime`` 等审计字段以及 ``crudMode``，由于这些字段在服务器端
   自动设置，因此会被忽略。创建或更新时无需指定这些字段。

删除相关内容
============

请求
----

::

    DELETE /api/admin/relatedcontent/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

使用示例
========

产品信息相关内容
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

支持信息相关内容
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-relatedquery` - 相关查询API
- :doc:`../../admin/relatedcontent-guide` - 相关内容管理指南
