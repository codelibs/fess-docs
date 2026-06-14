==========================
Backup API
==========================

概述
====

Backup API是用于参照和下载 |Fess| 备份对象数据的API。
可以获取备份对象的列表，以及下载单个备份文件（系统属性、各索引的批量数据、日志的NDJSON数据）。

基础URL
=======

::

    /api/admin/backup

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /files
     - 获取备份对象列表
   * - GET
     - /file/{id}
     - 下载备份文件

获取备份对象列表
================

返回备份对象的列表。对象基于 ``index.backup.targets`` 和 ``index.backup.log.targets`` 的设置。

请求
----

::

    GET /api/admin/backup/files

响应
----

``files`` 中存放表示备份对象的对象数组，``total`` 中存放数量。
每个对象具有 ``id`` 和 ``name``，二者均设置为对象名（如 ``fess_config.bulk``、``system.properties``、``search_log.ndjson`` 等）。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "fess_config.bulk",
            "name": "fess_config.bulk"
          },
          {
            "id": "system.properties",
            "name": "system.properties"
          },
          {
            "id": "search_log.ndjson",
            "name": "search_log.ndjson"
          }
        ],
        "total": 3
      }
    }

下载备份文件
============

下载指定备份文件的内容。``{id}`` 中指定列表获取时得到的 ``id`` （对象名）。
根据 ``{id}`` 的种类，响应内容会按如下方式切换。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - 内容
   * - ``system.properties``
     - 系统属性的内容
   * - ``*.bulk`` 或不带 ``.bulk`` 扩展名的索引名
     - 对目标索引进行滚动（scroll）生成的批量数据
   * - ``*.ndjson`` （``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``）
     - 对应日志的NDJSON数据

如果指定了不存在于备份对象中的 ``{id}``，将会出错。

请求
----

::

    GET /api/admin/backup/file/{id}

响应
----

备份文件的流。NDJSON格式时以 ``Content-Type: application/x-ndjson`` 返回，其他情况以 ``application/octet-stream`` 返回。

使用示例
========

获取备份对象列表
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

下载配置索引
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

下载搜索日志
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-log` - 日志API
