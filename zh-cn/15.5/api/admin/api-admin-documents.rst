==========================
Documents API
==========================

概述
====

Documents API是用于管理 |Fess| 索引中文档的API。
您可以执行文档的批量删除、更新、搜索等操作。

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
   * - DELETE
     - /
     - 删除文档（通过查询指定）
   * - DELETE
     - /{id}
     - 删除文档（通过ID指定）

通过查询删除文档
================

批量删除匹配搜索查询的文档。

请求
----

::

    DELETE /api/admin/documents

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``q``
     - String
     - 是
     - 删除目标的搜索查询

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

使用示例
~~~~~~~~

.. code-block:: bash

    # 删除特定网站的文档
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 删除旧文档
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 通过标签删除文档
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

通过ID删除文档
==============

指定文档ID进行删除。

请求
----

::

    DELETE /api/admin/documents/{id}

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``id``
     - String
     - 是
     - 文档ID（路径参数）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

使用示例
~~~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

查询语法
========

删除查询可以使用 |Fess| 的标准搜索语法。

基本查询
--------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 查询示例
     - 说明
   * - ``url:example.com``
     - URL包含"example.com"的文档
   * - ``url:https://example.com/*``
     - 具有特定前缀的URL
   * - ``host:example.com``
     - 特定主机的文档
   * - ``title:keyword``
     - 标题包含关键词的文档
   * - ``content:keyword``
     - 正文包含关键词的文档
   * - ``label:mylabel``
     - 具有特定标签的文档

日期范围查询
------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 查询示例
     - 说明
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - 在指定期间内更新的文档
   * - ``lastModified:[* TO 2023-01-01]``
     - 在指定日期之前更新的文档
   * - ``created:[2024-01-01 TO *]``
     - 在指定日期之后创建的文档

复合查询
--------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 查询示例
     - 说明
   * - ``url:example.com AND label:blog``
     - AND条件
   * - ``url:example.com OR url:sample.com``
     - OR条件
   * - ``NOT url:example.com``
     - NOT条件
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - 分组

注意事项
========

删除操作注意
------------

.. warning::
   删除操作无法撤销。在生产环境执行之前，请务必在测试环境中确认。

- 删除大量文档时，处理可能需要一些时间
- 删除过程中可能会影响索引性能
- 删除后，可能需要一些时间才能反映在搜索结果中

推荐做法
--------

1. **删除前确认**: 使用相同的查询调用搜索API，确认删除目标
2. **分阶段删除**: 大量删除时分多次执行
3. **备份**: 提前备份重要数据

使用示例
========

准备重新爬取整个网站
--------------------

.. code-block:: bash

    # 删除特定网站的旧文档
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 启动爬虫任务
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

清理旧文档
----------

.. code-block:: bash

    # 删除超过1年未更新的文档
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/searchlist-guide` - 搜索列表管理指南

