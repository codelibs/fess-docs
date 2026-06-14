==========================
BadWord API
==========================

概述
====

BadWord API是用于管理 |Fess| 屏蔽词（不适当的建议词排除）的API。
您可以设置不希望在建议功能中显示的关键词。

基础URL
=======

::

    /api/admin/badword

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
     - 获取屏蔽词列表
   * - GET
     - /setting/{id}
     - 获取屏蔽词
   * - POST
     - /setting
     - 创建屏蔽词
   * - PUT
     - /setting
     - 更新屏蔽词
   * - DELETE
     - /setting/{id}
     - 删除屏蔽词
   * - PUT
     - /upload
     - 上传屏蔽词CSV
   * - GET
     - /download
     - 下载屏蔽词CSV

获取屏蔽词列表
==============

请求
----

::

    GET /api/admin/badword/settings

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
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

获取屏蔽词
==========

请求
----

::

    GET /api/admin/badword/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

创建屏蔽词
==========

请求
----

::

    POST /api/admin/badword/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
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
     - 要排除的关键词（不能包含空白字符）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

更新屏蔽词
==========

请求
----

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

删除屏蔽词
==========

请求
----

::

    DELETE /api/admin/badword/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

上传屏蔽词CSV
=============

从CSV文件批量注册屏蔽词。文件以 ``multipart/form-data`` 发送。导入在服务器端异步执行。

请求
----

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``badWordFile``
     - 是
     - 要上传的屏蔽词CSV文件

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

下载屏蔽词CSV
=============

将已注册的屏蔽词作为CSV文件（``badword.csv``）下载。响应为 ``application/octet-stream`` 流。

请求
----

::

    GET /api/admin/badword/download

使用示例
========

排除垃圾关键词
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

上传CSV文件
-----------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

下载CSV文件
-----------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-suggest` - 建议管理API
- :doc:`api-admin-elevateword` - 提升词API
- :doc:`../../admin/badword-guide` - 屏蔽词管理指南

