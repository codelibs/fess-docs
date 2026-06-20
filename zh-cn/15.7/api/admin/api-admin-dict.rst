==========================
Dict API
==========================

概述
====

Dict API是用于管理 |Fess| 词典的API。
可以通过根端点获取可用词典的列表。
单个词典项目的查看、创建、更新、删除，以及词典文件的上传、下载，
通过各词典类型的子端点（synonym、kuromoji、mapping、protwords、stopwords、stemmeroverride）进行操作。

基础URL
=======

::

    /api/admin/dict

端点列表
========

词典根
------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /
     - 获取词典列表

各词典类型的端点
----------------

``{type}`` 指定 ``synonym`` 、 ``kuromoji`` 、 ``mapping`` 、 ``protwords`` 、 ``stopwords`` 、 ``stemmeroverride`` 中的任意一个。
这些值与词典列表响应中所包含的 ``type`` 字段的值相对应。
``{dictId}`` 是通过获取词典列表得到的词典ID。

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - 方法
     - 路径
     - 说明
   * - GET
     - /{type}/settings/{dictId}
     - 获取词典项目列表
   * - GET
     - /{type}/setting/{dictId}/{id}
     - 获取词典项目
   * - POST
     - /{type}/setting/{dictId}
     - 创建词典项目
   * - PUT
     - /{type}/setting/{dictId}
     - 更新词典项目
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - 删除词典项目
   * - PUT
     - /{type}/upload/{dictId}
     - 上传词典文件
   * - GET
     - /{type}/download/{dictId}
     - 下载词典文件

获取词典列表
============

获取可用词典文件的列表。

请求
----

::

    GET /api/admin/dict

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
          }
        ],
        "total": 2
      }
    }

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``settings[].id``
     - 词典ID（在单个词典操作中作为 ``{dictId}`` 使用）
   * - ``settings[].type``
     - 词典类型
   * - ``settings[].path``
     - 词典文件的路径
   * - ``settings[].timestamp``
     - 词典文件的更新日期时间
   * - ``total``
     - 词典文件的总数

获取词典项目列表
================

获取指定词典内的项目列表。

请求
----

::

    GET /api/admin/dict/{type}/settings/{dictId}

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``dictId``
     - String
     - 是
     - 词典ID（路径参数）
   * - ``size``
     - Integer
     - 否
     - 每页记录数（默认值：25）
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认值：1）

响应
----

响应中 ``settings`` 数组各项目的字段因词典类型而异（请参阅后述的“各词典类型的项目字段”）。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "検索,サーチ",
            "outputs": "検索,サーチ,リサーチ"
          }
        ],
        "total": 1
      }
    }

以上为 ``synonym`` 词典的示例。

获取词典项目
============

获取词典内的特定项目。

请求
----

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``dictId``
     - String
     - 是
     - 词典ID（路径参数）
   * - ``id``
     - Long
     - 是
     - 项目ID（路径参数）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

创建词典项目
============

在词典中创建新的项目。

请求
----

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

请求体（synonym示例）
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

更新词典项目
============

更新词典内的现有项目。

请求
----

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

请求体（synonym示例）
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

删除词典项目
============

删除词典内的项目。

请求
----

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``dictId``
     - String
     - 是
     - 词典ID（路径参数）
   * - ``id``
     - Long
     - 是
     - 项目ID（路径参数）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

上传词典文件
============

上传整个词典文件并进行替换。

请求
----

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

文件字段的名称因词典类型而异（请参阅后述的“各词典类型的项目字段”）。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

下载词典文件
============

下载词典文件。

请求
----

::

    GET /api/admin/dict/{type}/download/{dictId}

响应为词典文件的二进制数据（ ``application/octet-stream`` ）。

各词典类型的项目字段
====================

词典项目的创建·更新请求体以及响应的字段因词典类型而异。
``id`` （项目ID）和 ``dictId`` （词典ID）在响应中是共通的。

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - 类型
     - 项目字段
     - 上传文件字段
   * - ``synonym``
     - ``inputs`` （必需）、 ``outputs`` （必需）
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` （必需）、 ``segmentation`` （必需）、 ``reading`` （必需）、 ``pos`` （必需）
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` （必需）、 ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` （必需）
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` （必需）
     - ``stopwordsFile``
   * - ``stemmeroverride``
     - ``input`` （必需）、 ``output`` （必需）
     - ``stemmerOverrideFile``

使用示例
========

获取词典列表
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取同义词词典的项目列表
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

向同义词词典添加项目
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

上传同义词词典文件
------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

下载同义词词典文件
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../../admin/dict-guide` - 词典管理指南
