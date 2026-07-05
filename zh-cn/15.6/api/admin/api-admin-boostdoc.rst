==========================
BoostDoc API
==========================

概述
====

BoostDoc API是用于管理 |Fess| 文档提升设置的API。
您可以调整符合特定条件的文档的搜索排名。

基础URL
=======

::

    /api/admin/boostdoc

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
     - 获取文档提升列表
   * - GET
     - /setting/{id}
     - 获取文档提升
   * - POST
     - /setting
     - 创建文档提升
   * - PUT
     - /setting
     - 更新文档提升
   * - DELETE
     - /setting/{id}
     - 删除文档提升

获取文档提升列表
================

请求
----

::

    GET /api/admin/boostdoc/settings
    PUT /api/admin/boostdoc/settings

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
            "id": "boostdoc_id_1",
            "urlExpr": ".*docs\\.example\\.com.*",
            "boostExpr": "3.0",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

获取文档提升
============

请求
----

::

    GET /api/admin/boostdoc/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": ".*docs\\.example\\.com.*",
          "boostExpr": "3.0",
          "sortOrder": 0
        }
      }
    }

创建文档提升
============

请求
----

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``urlExpr``
     - 是
     - URL正则表达式模式
   * - ``boostExpr``
     - 是
     - 提升表达式（数值或表达式）
   * - ``sortOrder``
     - 否
     - 应用顺序

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

更新文档提升
============

请求
----

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

删除文档提升
============

请求
----

::

    DELETE /api/admin/boostdoc/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_boostdoc_id",
        "created": false
      }
    }

提升表达式示例
==============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 提升表达式
     - 说明
   * - ``2.0``
     - 固定值提升
   * - ``doc['boost'].value * 2``
     - 文档boost值的2倍
   * - ``Math.log(doc['click_count'].value + 1)``
     - 基于点击数的对数比例提升
   * - ``doc['last_modified'].value > now - 7d ? 3.0 : 1.0``
     - 最后更新日期在1周内则提升3倍

使用示例
========

文档网站提升
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*docs\\.example\\.com.*",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

新内容提升
----------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*",
           "boostExpr": "doc[\"last_modified\"].value > now - 30d ? 2.0 : 1.0",
           "sortOrder": 10
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/boostdoc-guide` - 文档提升管理指南

