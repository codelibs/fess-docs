==========================
BoostDoc API
==========================

概述
====

BoostDoc API是用于管理 |Fess| 文档提升设置的API。
通过配置文档提升，可以提高符合特定条件的文档的评分，
使其更容易出现在搜索结果的靠前位置。

提升在索引创建时（爬取时）应用于每个文档。
条件（``urlExpr``）和提升值（``boostExpr``）均作为Groovy表达式进行求值。
多个规则按 ``sortOrder`` 升序依次求值，仅应用第一个条件匹配规则的提升值
（找到匹配规则后，后续规则将不再求值）。

.. note::

   在管理界面中，``urlExpr`` 显示为"条件"，``boostExpr`` 显示为"提升值表达式"。
   有关配置项的详细信息，请参阅 :doc:`../../admin/boostdoc-guide`。

基础URL
=======

::

    /api/admin/boostdoc

认证
====

使用此API需要持有 ``Radmin-api`` 权限的访问令牌。
有关访问令牌的获取方法和指定方式，请参阅 :doc:`api-admin-overview`。

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

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``size``
     - Integer
     - 否
     - 每页记录数（默认：25）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始。默认：1）
   * - ``urlExpr``
     - String
     - 否
     - 按条件表达式筛选（部分匹配）
   * - ``boostExpr``
     - String
     - 否
     - 按提升值表达式筛选（部分匹配）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
            "boostExpr": "3.0",
            "sortOrder": 1,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   除上述字段外，响应中每条设置对象还包含创建/更新元数据（``createdBy``、``createdTime``、``updatedBy``、``updatedTime``）。
   ``versionNo`` 在更新（PUT）时为必填项，请在更新前通过获取单条或列表API取得当前值。

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
          "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
          "boostExpr": "3.0",
          "sortOrder": 1,
          "versionNo": 1
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
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - 字段
     - 必需
     - 说明
   * - ``urlExpr``
     - 是
     - 条件表达式。用于判断提升目标文档的Groovy表达式，返回 ``Boolean`` 值。对应管理界面的"条件"（最多10000个字符）。
   * - ``boostExpr``
     - 是
     - 提升值表达式。返回提升值（数值）的Groovy表达式。也可指定如 ``3.0`` 这样的固定值。对应管理界面的"提升值表达式"（最多10000个字符）。
   * - ``sortOrder``
     - 是
     - 应用顺序。规则按升序依次求值，应用第一个条件匹配规则的提升值（表单初始值：0，须为0以上的整数）。

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
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

更新时，除创建时的字段外，还需提供 ``id``（目标规则的ID，最多1000个字符）和 ``versionNo``（用于乐观锁的版本号）。
``versionNo`` 请通过获取单条或列表API的响应取得当前值后再指定。
若版本号不匹配，更新将会失败。

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
        "status": 0
      }
    }

关于条件表达式与提升值表达式
============================

``urlExpr``（条件）和 ``boostExpr``（提升值表达式）均作为Groovy表达式进行求值。
在表达式中，可以通过字段名变量引用索引目标文档的字段值。

- ``urlExpr`` 必须返回 ``Boolean`` 值（例：``url.startsWith("https://docs.example.com/")``）。单纯的正则表达式字符串（例：``.*docs\.example\.com.*``）作为Groovy表达式不返回 ``Boolean``，因此无法作为条件使用。若需使用正则表达式，请使用Groovy的 ``String#matches`` 方法。
- ``boostExpr`` 必须返回数值。结果将被转换为 ``float``，仅当大于0时才会应用提升。

.. note::

   表达式中可引用的主要字段变量：``url``、``title``、``content``、``content_length``、``last_modified`` 等。
   ``click_count`` 和 ``favorite_count`` 分别在 ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled``（均默认启用）的情况下可引用。
   OpenSearch的日期计算语法（如 ``now - 7d``）无法在Groovy中使用。

条件表达式（``urlExpr``）示例
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 条件表达式
     - 说明
   * - ``url.startsWith("https://docs.example.com/")``
     - 以指定URL开头的文档为目标
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - 使用正则表达式（Groovy的 ``String#matches``）判断URL
   * - ``title.contains("发布说明")``
     - 以标题中包含特定词语的文档为目标

提升值表达式（``boostExpr``）示例
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 提升值表达式
     - 说明
   * - ``3.0``
     - 以固定值提升
   * - ``click_count * 0.1 + 1``
     - 根据点击次数提升
   * - ``Math.log(click_count + 1)``
     - 基于点击次数的对数缩放提升

使用示例
========

文档站点提升
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

点击量高的内容提升
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://www.example.com/\")",
           "boostExpr": "click_count * 0.1 + 1",
           "sortOrder": 10
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/boostdoc-guide` - 文档提升管理指南
