==========================
Plugin API
==========================

概述
====

Plugin API是用于管理 |Fess| 插件（构件）的API。
可以获取已安装插件以及可安装插件的列表，并执行插件的安装与删除操作。

基础URL
=======

::

    /api/admin/plugin

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - GET
     - /installed
     - 获取已安装插件列表
   * - GET
     - /available
     - 获取可安装插件列表
   * - POST
     - /
     - 安装插件
   * - DELETE
     - /
     - 删除插件

获取已安装插件列表
==================

返回已安装插件的列表。

请求
----

::

    GET /api/admin/plugin/installed

响应
----

``plugins`` 中存放表示插件信息的对象数组。
每个对象是字符串键值的映射，包含 ``name`` （插件名）和 ``version`` （版本）等。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

获取可安装插件列表
==================

返回可安装插件的列表。

请求
----

::

    GET /api/admin/plugin/available

响应
----

``plugins`` 中存放表示可安装插件信息的对象数组。
每个对象与 ``installed`` 相同，是字符串键值的映射。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

安装插件
========

安装指定名称和版本的插件。

请求
----

::

    POST /api/admin/plugin
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 插件名（最多100个字符）
   * - ``version``
     - 是
     - 插件版本（最多100个字符）

响应
----

成功时仅返回 ``status``。
当 ``name`` 或 ``version`` 对应的构件不存在时，``status`` 为 ``1`` （BAD_REQUEST），并在 ``message`` 中设置 ``invalid name or version``。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

删除插件
========

删除指定名称和版本的插件。

请求
----

::

    DELETE /api/admin/plugin
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 插件名（最多100个字符）
   * - ``version``
     - 否
     - 插件版本（最多100个字符）

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

使用示例
========

获取已安装插件列表
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

安装插件
--------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

删除插件
--------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
