==========================
Backup API
==========================

概述
====

Backup API是用于参照和下载 |Fess| 备份对象数据的API。
可以获取备份对象的列表，以及下载单个备份文件（系统属性、各索引的批量数据、日志的NDJSON数据）。

此API仅供参照和下载（只读）使用。上传备份文件并进行恢复的还原功能不通过API提供，如需还原，请通过管理界面的系统信息 → 备份进行操作。

基础URL
=======

::

    /api/admin/backup

认证
====

与其他Admin API相同，需要通过访问令牌进行认证。访问令牌需要具备 ``Radmin-api`` 权限（通过 ``api.admin.access.permissions`` 设置，默认值为 ``Radmin-api``）。
在请求头中指定访问令牌。

::

    Authorization: Bearer <访问令牌>

有关认证及访问令牌获取方式的详细信息，请参阅 :doc:`api-admin-overview`。

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

返回备份对象的列表。对象基于 ``index.backup.targets`` 和 ``index.backup.log.targets`` 的设置，返回两者合并后的列表。

请求
----

::

    GET /api/admin/backup/files

响应
----

``files`` 中存放表示备份对象的对象数组，``total`` 中存放数量。
每个对象具有 ``id`` 和 ``name``，二者均设置为对象名（如 ``fess_config.bulk``、``system.properties``、``search_log.ndjson`` 等）。

以下是默认设置（``index.backup.targets`` 和 ``index.backup.log.targets`` 为默认值）时的示例。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          { "id": "fess_basic_config.bulk", "name": "fess_basic_config.bulk" },
          { "id": "fess_config.bulk", "name": "fess_config.bulk" },
          { "id": "fess_user.bulk", "name": "fess_user.bulk" },
          { "id": "system.properties", "name": "system.properties" },
          { "id": "fess.json", "name": "fess.json" },
          { "id": "doc.json", "name": "doc.json" },
          { "id": "click_log.ndjson", "name": "click_log.ndjson" },
          { "id": "favorite_log.ndjson", "name": "favorite_log.ndjson" },
          { "id": "search_log.ndjson", "name": "search_log.ndjson" },
          { "id": "user_info.ndjson", "name": "user_info.ndjson" }
        ],
        "total": 10
      }
    }

.. note::

   ``version`` 中设置的是当前运行的 |Fess| 的产品版本。\ ``files`` 的内容会根据
   ``index.backup.targets`` / ``index.backup.log.targets`` 的设置而变化，
   上述内容为默认值时的示例。

下载备份文件
============

下载指定备份文件的内容。\ ``{id}`` 中指定获取列表时得到的 ``id``\ （对象名）。
根据 ``{id}`` 的种类，响应内容会按如下方式切换。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - 内容
   * - ``system.properties``
     - 系统属性的内容（``application/octet-stream``）
   * - ``*.bulk`` 或不带扩展名的索引名
     - 对与对象名同名的索引进行滚动（scroll）生成的批量数据（``application/octet-stream``）。去除 ``.bulk`` 后的名称作为索引名处理。
   * - ``*.ndjson`` （``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``）
     - 对应日志的NDJSON数据（``application/x-ndjson``）

.. note::

   ``fess.json`` 和 ``doc.json`` 是索引的映射定义（Schema）文件。
   它们包含在对象列表（``/files``）中，但通过此API下载时，与 ``.bulk`` 相同，
   作为索引的滚动处理来处理。包含映射定义的备份和还原请使用管理界面的系统信息 → 备份。

如果指定了不存在于备份对象中的 ``{id}``，将返回 ``status`` 为非0值且包含错误消息（``Could not find any backup index.``）的错误响应。

请求
----

::

    GET /api/admin/backup/file/{id}

响应
----

备份文件的流。NDJSON格式时以 ``Content-Type: application/x-ndjson`` 返回，其他情况以 ``application/octet-stream`` 返回。

.. note::

   日志（``*.ndjson``）的导出受 ``index.backup.log.load.timeout``\ （默认值 ``60000`` 毫秒）的限制。
   如果输出耗时较长，日志数据可能会被中途截断。

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
