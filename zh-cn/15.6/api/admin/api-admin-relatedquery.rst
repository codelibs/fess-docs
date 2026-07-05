==========================
RelatedQuery API
==========================

概述
====

RelatedQuery API是用于管理 |Fess| 相关查询的API。
您可以为特定搜索查询推荐相关的搜索关键词。

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
   * - GET/PUT
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
    PUT /api/admin/relatedquery/settings

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
            "id": "query_id_1",
            "term": "fess",
            "queries": ["fess tutorial", "fess installation", "fess configuration"]
          }
        ],
        "total": 5
      }
    }

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
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": ["fess tutorial", "fess installation", "fess configuration"],
          "virtualHost": ""
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
      "queries": ["search tutorial", "search syntax", "advanced search"],
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
   * - ``queries``
     - 是
     - 相关查询数组
   * - ``virtualHost``
     - 否
     - 虚拟主机

响应
----

.. code-block:: json

    {
      "response": {
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
      "queries": ["search tutorial", "search syntax", "advanced search", "search tips"],
      "virtualHost": "",
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
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
        "status": 0,
        "id": "deleted_query_id",
        "created": false
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
           "queries": ["product features", "product pricing", "product comparison", "product reviews"]
         }'

帮助相关查询
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": ["help center", "help documentation", "help contact support"]
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-relatedcontent` - 相关内容API
- :doc:`api-admin-suggest` - 建议管理API
- :doc:`../../admin/relatedquery-guide` - 相关查询管理指南

