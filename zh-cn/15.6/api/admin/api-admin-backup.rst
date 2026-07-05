==========================
Backup API
==========================

概述
====

Backup API是用于备份和恢复 |Fess| 配置数据的API。
您可以导出和导入爬虫设置、用户、角色、词典等配置。

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
     - /export
     - 导出配置数据
   * - POST
     - /import
     - 导入配置数据

导出配置数据
============

请求
----

::

    GET /api/admin/backup/export

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``types``
     - String
     - 否
     - 导出目标（逗号分隔，默认：all）

导出目标类型
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 类型
     - 说明
   * - ``webconfig``
     - Web爬虫设置
   * - ``fileconfig``
     - 文件爬虫设置
   * - ``dataconfig``
     - 数据存储设置
   * - ``scheduler``
     - 调度设置
   * - ``user``
     - 用户设置
   * - ``role``
     - 角色设置
   * - ``group``
     - 组设置
   * - ``labeltype``
     - 标签类型设置
   * - ``keymatch``
     - 关键词匹配设置
   * - ``dict``
     - 词典数据
   * - ``all``
     - 所有设置（默认）

响应
----

二进制数据（ZIP格式）

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

ZIP文件内容
~~~~~~~~~~~

::

    fess-backup-20250129-100000.zip
    ├── webconfig.json
    ├── fileconfig.json
    ├── dataconfig.json
    ├── scheduler.json
    ├── user.json
    ├── role.json
    ├── group.json
    ├── labeltype.json
    ├── keymatch.json
    ├── dict/
    │   ├── synonym.txt
    │   ├── mapping.txt
    │   └── protwords.txt
    └── metadata.json

导入配置数据
============

请求
----

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

请求体
~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [二进制数据]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``file``
     - 是
     - 备份ZIP文件
   * - ``overwrite``
     - 否
     - 覆盖现有设置（默认：false）
   * - ``types``
     - 否
     - 导入目标（逗号分隔，默认：all）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Backup imported successfully",
        "imported": {
          "webconfig": 5,
          "fileconfig": 3,
          "dataconfig": 2,
          "scheduler": 4,
          "user": 10,
          "role": 5,
          "group": 3,
          "labeltype": 8,
          "keymatch": 12,
          "dict": 3
        }
      }
    }

使用示例
========

导出所有设置
------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

导出特定设置
------------

.. code-block:: bash

    # 仅导出Web爬虫设置和用户设置
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

导入设置
--------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

覆盖现有设置导入
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

仅导入特定设置
--------------

.. code-block:: bash

    # 仅导入用户和角色
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

自动化备份
----------

.. code-block:: bash

    #!/bin/bash
    # 每天凌晨2点获取备份的脚本示例

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # 删除30天以前的备份
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

注意事项
========

- 备份包含密码信息，请安全保管
- 导入时指定 ``overwrite=true`` 会覆盖现有设置
- 大规模配置的导出/导入可能需要一些时间
- 不同版本Fess之间的导入可能存在兼容性问题

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../../admin/backup-guide` - 备份管理指南
- :doc:`../../admin/maintenance-guide` - 维护指南

