==========================
ElevateWord API
==========================

概述
====

ElevateWord API是用于管理 |Fess| 提升词（特定关键词的搜索排名操作）的API。
您可以针对特定搜索查询，将特定文档置于搜索结果的顶部或底部。

基础URL
=======

::

    /api/admin/elevateword

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
     - 获取提升词列表
   * - GET
     - /setting/{id}
     - 获取提升词
   * - POST
     - /setting
     - 创建提升词
   * - PUT
     - /setting
     - 更新提升词
   * - DELETE
     - /setting/{id}
     - 删除提升词
   * - PUT
     - /upload
     - 上传提升词CSV
   * - GET
     - /download
     - 下载提升词CSV

获取提升词列表
==============

请求
----

::

    GET /api/admin/elevateword/settings

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
     - 页码（从1开始，默认：1）
   * - ``id``
     - String
     - 否
     - 按提升词ID进行精确匹配过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

获取提升词
==========

请求
----

::

    GET /api/admin/elevateword/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

创建提升词
==========

请求
----

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - 字段
     - 必需
     - 说明
   * - ``suggestWord``
     - 是
     - 提升目标的关键词
   * - ``reading``
     - 否
     - 读音（日语假名）
   * - ``permissions``
     - 否
     - 访问权限（每行一项的换行分隔字符串。表单初始值：搜索的默认显示权限）
   * - ``boost``
     - 是
     - 提升值（表单初始值：100.0）
   * - ``labelTypeIds``
     - 否
     - 目标标签ID（字符串数组）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

更新提升词
==========

请求
----

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   更新时，除创建时所需的字段外，还需要以下字段。

   - ``id`` - 要更新的提升词ID
   - ``versionNo`` - 用于乐观锁的版本号。请指定通过 ``GET /setting/{id}`` 获取的值。

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

删除提升词
==========

请求
----

::

    DELETE /api/admin/elevateword/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

上传提升词CSV
=============

从CSV文件批量注册提升词。文件以 ``multipart/form-data`` 发送。导入在服务器端异步执行。

请求
----

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``elevateWordFile``
     - 是
     - 要上传的提升词CSV文件

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

下载提升词CSV
=============

将已注册的提升词作为CSV文件（``elevate.csv``）下载。响应为 ``application/octet-stream`` 流。

请求
----

::

    GET /api/admin/elevateword/download

使用示例
========

产品名称提升
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

针对特定标签提升
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

上传CSV文件
-----------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

下载CSV文件
-----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-keymatch` - 关键词匹配API
- :doc:`api-admin-boostdoc` - 文档提升API
- :doc:`../../admin/elevateword-guide` - 提升词管理指南

