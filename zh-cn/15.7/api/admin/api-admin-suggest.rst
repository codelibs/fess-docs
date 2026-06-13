==========================
Suggest API
==========================

概述
====

Suggest API是用于管理 |Fess| 建议功能的API。
可以获取建议词的统计信息，以及删除建议词。

基础URL
=======

::

    /api/admin/suggest

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /
     - 获取建议词统计信息
   * - DELETE
     - /all
     - 删除所有建议词
   * - DELETE
     - /document
     - 删除来源于文档的建议词
   * - DELETE
     - /query
     - 删除来源于搜索查询的建议词

获取建议词统计信息
==================

获取有关建议词数量的统计信息。

请求
----

::

    GET /api/admin/suggest

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 300
        }
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``setting.totalWordsNum``
     - 建议词总数
   * - ``setting.documentWordsNum``
     - 来源于文档的建议词数
   * - ``setting.queryWordsNum``
     - 来源于搜索查询的建议词数

删除所有建议词
==============

删除所有建议词。

请求
----

::

    DELETE /api/admin/suggest/all

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

删除来源于文档的建议词
======================

删除从文档生成的建议词。

请求
----

::

    DELETE /api/admin/suggest/document

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

删除来源于搜索查询的建议词
==========================

删除从搜索查询生成的建议词。

请求
----

::

    DELETE /api/admin/suggest/query

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

获取统计信息
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除所有建议词
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

删除来源于文档的建议词
----------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-badword` - 屏蔽词API
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/suggest-guide` - 建议管理指南
