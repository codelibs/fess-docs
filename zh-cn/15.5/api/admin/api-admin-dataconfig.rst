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
   * - GET/PUT
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
    PUT /api/admin/dataconfig/settings

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
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": true,
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
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
   * - ``handlerName``
     - 是
     - 数据存储处理器名称
   * - ``handlerParameter``
     - 否
     - 处理器参数（连接信息等）
   * - ``handlerScript``
     - 是
     - 数据转换脚本
   * - ``boost``
     - 否
     - 搜索结果提升值（默认：1.0）
   * - ``available``
     - 否
     - 启用/禁用（默认：true）
   * - ``sortOrder``
     - 否
     - 显示顺序
   * - ``permissions``
     - 否
     - 访问权限角色
   * - ``virtualHosts``
     - 否
     - 虚拟主机
   * - ``labelTypeIds``
     - 否
     - 标签类型ID

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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
      "available": true,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_dataconfig_id",
        "created": false
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
     - 从CSV文件读取数据
   * - ``JsonDataStore``
     - 从JSON文件或JSON API读取数据

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
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": true
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-webconfig` - Web爬虫设置API
- :doc:`api-admin-fileconfig` - 文件爬虫设置API
- :doc:`../../admin/dataconfig-guide` - 数据存储设置指南

