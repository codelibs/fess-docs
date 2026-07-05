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
   * - GET/PUT
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
    PUT /api/admin/relatedcontent/settings

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
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

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
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "sortOrder": 0,
          "virtualHost": ""
        }
      }
    }

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
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``term``
     - 是
     - 搜索关键词
   * - ``content``
     - 是
     - 要显示的HTML内容
   * - ``sortOrder``
     - 否
     - 显示顺序
   * - ``virtualHost``
     - 否
     - 虚拟主机

响应
----

.. code-block:: json

    {
      "response": {
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

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

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
        "status": 0,
        "id": "deleted_content_id",
        "created": false
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

