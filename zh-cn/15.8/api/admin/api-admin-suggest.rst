==========================
Suggest API
==========================

概述
====

Suggest API是用于管理 |Fess| 建议功能所使用的建议词的API。
可以获取有关建议词数量的统计信息，以及删除建议词。

建议词分为两类：从已爬取文档中生成的词（文档来源）和从用户搜索查询中生成的词（搜索查询来源）。
通过本API，可以按类别分别删除，也可以一次性全部删除。

认证
====

访问本API需要通过访问令牌进行认证。请在请求头中指定访问令牌。

::

    Authorization: Bearer <访问令牌>

访问令牌需要具有Admin API的权限（默认为 ``Radmin-api``）。
有关访问令牌的获取方式和权限的详细信息，请参阅 :doc:`api-admin-overview`。

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
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
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
     - 建议词总数（建议索引中已注册的建议词数量）
   * - ``setting.documentWordsNum``
     - 来源于文档的建议词数（文档频率在1以上的建议词数量）
   * - ``setting.queryWordsNum``
     - 来源于搜索查询的建议词数（查询频率在1以上的建议词数量）

.. note::

   ``documentWordsNum`` 与 ``queryWordsNum`` 并非互斥。若一个建议词同时来源于文档和搜索查询，
   则会同时计入两者的数量。因此，``documentWordsNum`` 与 ``queryWordsNum`` 的合计值不一定
   与 ``totalWordsNum`` 相等。

删除所有建议词
==============

删除所有建议词。无论来源于文档还是搜索查询，建议索引中的所有建议词均为删除对象。

请求
----

::

    DELETE /api/admin/suggest/all

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

删除来源于文档的建议词
======================

删除从文档生成的建议词（来源于文档的建议词）。

请求
----

::

    DELETE /api/admin/suggest/document

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

删除来源于搜索查询的建议词
==========================

删除从搜索查询生成的建议词（来源于搜索查询的建议词）。

请求
----

::

    DELETE /api/admin/suggest/query

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

删除处理失败时，将返回HTTP状态码 ``400``，响应体中的 ``status`` 将被设置为
``1``（BAD_REQUEST），``message`` 中包含错误消息。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

若访问令牌未指定或无效，或权限不足，响应体中的 ``status`` 将被设置为
``3``（UNAUTHORIZED）。有关 ``status`` 的值及HTTP状态码的列表，请参阅
:doc:`api-admin-overview`。

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

删除来源于搜索查询的建议词
--------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-badword` - 屏蔽词API
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/suggest-guide` - 建议管理指南
