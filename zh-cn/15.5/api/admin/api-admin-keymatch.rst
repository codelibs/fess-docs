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
   * - GET/PUT
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
    PUT /api/admin/keymatch/settings

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
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

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
          "boost": 10.0
        }
      }
    }

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
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``term``
     - 是
     - 搜索关键词
   * - ``query``
     - 是
     - 匹配条件查询
   * - ``maxSize``
     - 否
     - 最大显示数量（默认：10）
   * - ``boost``
     - 否
     - 提升值（默认：1.0）

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
        "status": 0,
        "id": "deleted_keymatch_id",
        "created": false
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

