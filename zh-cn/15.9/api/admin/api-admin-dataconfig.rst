==========================
DataConfig API
==========================

概述
====

DataConfig API是用于管理 |Fess| 数据存储设置的API。
您可以操作数据库、CSV、JSON等数据源的爬虫设置。

基础URL
=======

::

    /api/admin/dataconfig

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
     - 获取数据存储设置列表
   * - GET
     - /setting/{id}
     - 获取数据存储设置
   * - POST
     - /setting
     - 创建数据存储设置
   * - PUT
     - /setting
     - 更新数据存储设置
   * - DELETE
     - /setting/{id}
     - 删除数据存储设置

获取数据存储设置列表
====================

请求
----

::

    GET /api/admin/dataconfig/settings

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
     - 每页记录数（默认：25）
   * - ``page``
     - Integer
     - 否
     - 页码（从 1 开始，默认值：1）
   * - ``name``
     - String
     - 否
     - 按配置名称过滤
   * - ``handlerName``
     - String
     - 否
     - 按处理器名称过滤
   * - ``description``
     - String
     - 否
     - 按描述过滤

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "description": "数据库爬虫",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

获取数据存储设置
================

请求
----

::

    GET /api/admin/dataconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "description": "数据库爬虫",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
        }
      }
    }

创建数据存储设置
================

请求
----

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 设置名称
   * - ``description``
     - 否
     - 设置的说明
   * - ``handlerName``
     - 是
     - 数据存储处理器名称
   * - ``handlerParameter``
     - 否
     - 处理器参数（连接信息等）
   * - ``handlerScript``
     - 否
     - 数据转换脚本
   * - ``boost``
     - 是
     - 搜索结果提升值
   * - ``available``
     - 是
     - 启用/禁用（字符串 ``"true"`` / ``"false"``）
   * - ``sortOrder``
     - 是
     - 显示顺序
   * - ``permissions``
     - 否
     - 访问权限角色（多个时以换行分隔）
   * - ``virtualHosts``
     - 否
     - 虚拟主机（多个时以换行分隔）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

更新数据存储设置
================

请求
----

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

更新请求需要与创建时相同的必填字段（``name``、``handlerName``、``boost``、``available``、``sortOrder``），以及以下字段：

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``id``
     - 是
     - 要更新的配置 ID
   * - ``versionNo``
     - 是
     - 用于乐观锁的版本号（指定获取设置时返回的值）

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

删除数据存储设置
================

请求
----

::

    DELETE /api/admin/dataconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

处理器类型
==========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 处理器名称
     - 说明
   * - ``DatabaseDataStore``
     - 通过JDBC连接数据库
   * - ``CsvDataStore``
     - 从CSV文件读取数据（将每一行作为一个文档处理）
   * - ``CsvListDataStore``
     - 读取CSV文件并自动删除已处理的文件（支持基于时间戳过滤的 ``CsvDataStore`` 扩展）
   * - ``JsonDataStore``
     - 从JSON文件或JSON API读取数据

.. note::

   可用的处理器类型取决于已安装的数据存储插件。
   上述处理器为默认包含的类型。安装 SharePoint、Slack、Salesforce 等数据存储
   插件后，相应的处理器名称将变为可用。

使用示例
========

数据库爬虫设置
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-webconfig` - Web爬虫设置API
- :doc:`api-admin-fileconfig` - 文件爬虫设置API
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南
