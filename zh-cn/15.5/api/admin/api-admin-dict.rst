==========================
Dict API
==========================

概述
====

Dict API是用于管理 |Fess| 词典文件的API。
您可以管理同义词词典、映射词典、保护词词典等。

基础URL
=======

::

    /api/admin/dict

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
     - 获取词典列表
   * - GET
     - /{id}
     - 获取词典内容
   * - PUT
     - /{id}
     - 更新词典内容
   * - POST
     - /upload
     - 上传词典文件

获取词典列表
============

请求
----

::

    GET /api/admin/dict

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dicts": [
          {
            "id": "synonym",
            "name": "同义词词典",
            "path": "/var/lib/fess/dict/synonym.txt",
            "type": "synonym",
            "updatedAt": "2025-01-29T10:00:00Z"
          },
          {
            "id": "mapping",
            "name": "映射词典",
            "path": "/var/lib/fess/dict/mapping.txt",
            "type": "mapping",
            "updatedAt": "2025-01-28T15:30:00Z"
          },
          {
            "id": "protwords",
            "name": "保护词词典",
            "path": "/var/lib/fess/dict/protwords.txt",
            "type": "protwords",
            "updatedAt": "2025-01-27T12:00:00Z"
          }
        ],
        "total": 3
      }
    }

获取词典内容
============

请求
----

::

    GET /api/admin/dict/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dict": {
          "id": "synonym",
          "name": "同义词词典",
          "path": "/var/lib/fess/dict/synonym.txt",
          "type": "synonym",
          "content": "检索,搜索,查找\nFess,フェス\n全文检索,全文搜索",
          "updatedAt": "2025-01-29T10:00:00Z"
        }
      }
    }

更新词典内容
============

请求
----

::

    PUT /api/admin/dict/{id}
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "content": "检索,搜索,查找,search\nFess,フェス\n全文检索,全文搜索,full-text search"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``content``
     - 是
     - 词典内容（换行符分隔）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary updated successfully"
      }
    }

上传词典文件
============

请求
----

::

    POST /api/admin/dict/upload
    Content-Type: multipart/form-data

请求体
~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="type"

    synonym
    --boundary
    Content-Disposition: form-data; name="file"; filename="synonym.txt"
    Content-Type: text/plain

    检索,搜索,查找
    Fess,フェス
    --boundary--

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``type``
     - 是
     - 词典类型（synonym/mapping/protwords/stopwords）
   * - ``file``
     - 是
     - 词典文件

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary uploaded successfully"
      }
    }

词典类型
========

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 类型
     - 说明
   * - ``synonym``
     - 同义词词典（搜索时展开同义词）
   * - ``mapping``
     - 映射词典（字符规范化）
   * - ``protwords``
     - 保护词词典（不进行词干提取的单词）
   * - ``stopwords``
     - 停用词词典（不建立索引的单词）
   * - ``kuromoji``
     - Kuromoji词典（日语形态素分析）

词典格式示例
============

同义词词典
----------

::

    # 用逗号分隔指定同义词
    检索,搜索,查找,search
    Fess,フェス,fess
    全文检索,全文搜索,full-text search

映射词典
--------

::

    # 转换前 => 转换后
    ０ => 0
    １ => 1
    ２ => 2

保护词词典
----------

::

    # 保护不进行词干提取处理的单词
    running
    searching
    indexing

使用示例
========

获取词典列表
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取同义词词典内容
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN"

更新同义词词典
--------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "content": "检索,搜索,search\nFess,フェス,fess\n文档,文件,document"
         }'

上传词典文件
------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "type=synonym" \
         -F "file=@synonym.txt"

注意事项
========

- 更新词典后，可能需要重建索引
- 大型词典文件可能会影响搜索性能
- 词典的字符编码请使用UTF-8

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../../admin/dict-guide` - 词典管理指南
- :doc:`../../config/dict-config` - 词典配置指南

