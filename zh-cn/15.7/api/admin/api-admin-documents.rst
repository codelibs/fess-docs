==========================
Documents API
==========================

概述
====

Documents API是用于将文档批量注册到 |Fess| 索引的API。
可以将多个文档一起添加到索引中。

基础URL
=======

::

    /api/admin/documents

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - PUT
     - /bulk
     - 文档批量注册

文档批量注册
============

将多个文档批量注册到索引中。

请求
----

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "サンプルページ1",
          "content": "ページ1の本文テキストです。"
        },
        {
          "url": "https://example.com/page2",
          "title": "サンプルページ2",
          "content": "ページ2の本文テキストです。"
        }
      ]
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``documents``
     - 是
     - 要注册的文档数组。每个文档以字段名与值的映射形式指定。不能指定空数组。

每个文档可以自由指定 ``url`` 、 ``title`` 、 ``content`` 等索引字段。
当省略 ``content_length`` 、 ``favorite_count`` 、 ``click_count`` 、 ``boost`` 、 ``role`` 、 ``last_modified`` 、 ``timestamp`` 等字段时，将自动补充默认值。
此外， ``doc_id`` 和 ID 会在注册时自动生成。

响应
----

响应以 ``items`` 数组返回所注册的各文档的处理结果。
成功的项目包含 ``result`` 和 ``id`` ，失败的项目包含 ``result`` 和 ``message`` 。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

当任一项目注册失败时， ``status`` 将变为 ``9`` （FAILED），相应项目中会包含 ``message`` 字段。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``items``
     - 各文档处理结果的数组
   * - ``items[].result``
     - 处理结果状态（例如： ``CREATED``）
   * - ``items[].id``
     - 已注册文档的ID（成功时）
   * - ``items[].message``
     - 失败原因的消息（失败时）

使用示例
========

文档批量注册
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "サンプルページ1",
               "content": "ページ1の本文テキストです。"
             }
           ]
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-searchlist` - 文档搜索与管理API
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/searchlist-guide` - 搜索列表管理指南
