==========================
Suggest API
==========================

概述
====

Suggest API是用于管理 |Fess| 建议功能的API。
您可以添加、删除、更新建议词等。

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
   * - GET/PUT
     - /settings
     - 获取建议词列表
   * - GET
     - /setting/{id}
     - 获取建议词
   * - POST
     - /setting
     - 创建建议词
   * - PUT
     - /setting
     - 更新建议词
   * - DELETE
     - /setting/{id}
     - 删除建议词
   * - DELETE
     - /delete-all
     - 删除所有建议词

获取建议词列表
==============

请求
----

::

    GET /api/admin/suggest/settings
    PUT /api/admin/suggest/settings

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
            "id": "suggest_id_1",
            "text": "fess",
            "reading": "",
            "fields": ["title", "content"],
            "tags": ["product"],
            "roles": ["guest"],
            "lang": "ja",
            "score": 1.0
          }
        ],
        "total": 100
      }
    }

获取建议词
==========

请求
----

::

    GET /api/admin/suggest/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "suggest_id_1",
          "text": "fess",
          "reading": "",
          "fields": ["title", "content"],
          "tags": ["product"],
          "roles": ["guest"],
          "lang": "ja",
          "score": 1.0
        }
      }
    }

创建建议词
==========

请求
----

::

    POST /api/admin/suggest/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "text": "search engine",
      "reading": "",
      "fields": ["title"],
      "tags": ["feature"],
      "roles": ["guest"],
      "lang": "en",
      "score": 1.0
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``text``
     - 是
     - 建议文本
   * - ``reading``
     - 否
     - 读音（日语假名）
   * - ``fields``
     - 否
     - 目标字段
   * - ``tags``
     - 否
     - 标签
   * - ``roles``
     - 否
     - 访问权限角色
   * - ``lang``
     - 否
     - 语言代码
   * - ``score``
     - 否
     - 分数（默认：1.0）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_suggest_id",
        "created": true
      }
    }

更新建议词
==========

请求
----

::

    PUT /api/admin/suggest/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_suggest_id",
      "text": "search engine",
      "reading": "",
      "fields": ["title", "content"],
      "tags": ["feature", "popular"],
      "roles": ["guest"],
      "lang": "en",
      "score": 2.0,
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_suggest_id",
        "created": false
      }
    }

删除建议词
==========

请求
----

::

    DELETE /api/admin/suggest/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_suggest_id",
        "created": false
      }
    }

删除所有建议词
==============

请求
----

::

    DELETE /api/admin/suggest/delete-all

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "count": 250
      }
    }

使用示例
========

添加热门关键词
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/suggest/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "getting started",
           "fields": ["title"],
           "tags": ["tutorial"],
           "roles": ["guest"],
           "lang": "en",
           "score": 5.0
         }'

批量删除建议
------------

.. code-block:: bash

    # 删除所有建议
    curl -X DELETE "http://localhost:8080/api/admin/suggest/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-badword` - 屏蔽词API
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/suggest-guide` - 建议管理指南

