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

插件信息字段
============

列表获取类端点（``/installed`` 和 ``/available``）返回的 ``plugins``
数组中，每个元素均为包含以下字段的对象。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 字段
     - 说明
   * - ``type``
     - 构件的种类ID。取值为 ``fess-ds`` （数据存储）、``fess-theme`` （主题）、
       ``fess-ingest`` （Ingest）、``fess-script`` （脚本）、``fess-webapp`` （Web应用）、
       ``fess-thumbnail`` （缩略图）、``fess-crawler`` （爬虫）、``fess-llm`` （LLM）、
       ``jar`` （上述以外的通用JAR）之一。
   * - ``id``
     - 格式为 ``{name}:{version}`` 的标识符。
   * - ``name``
     - 插件名。
   * - ``version``
     - 插件版本。
   * - ``url``
     - 下载来源的URL。仅包含于 ``/available`` 的响应中。\ ``/installed`` 中
       由于值不存在，该字段本身会被省略。

.. note::

   |Fess| 的API响应中，值为 ``null`` 的字段不会输出。因此，
   已安装插件的各元素中不包含 ``url``\ 。

获取已安装插件列表
==================

返回已安装插件的列表。扫描插件目录中的构件，
按种类分类后以名称顺序排序返回。

请求
----

::

    GET /api/admin/plugin/installed

响应
----

``plugins`` 中存放表示插件信息的对象数组。
各对象的字段请参阅 `插件信息字段`_\ 。
已安装插件中不输出 ``url``\ 。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.8.0",
            "name": "fess-ds-slack",
            "version": "15.8.0"
          }
        ]
      }
    }

获取可安装插件列表
==================

返回可安装插件的列表。从 ``fess_config.properties`` 的
``plugin.repositories`` 中配置的仓库获取所有种类的构件。
获取结果会缓存一定时间（默认5分钟）。

请求
----

::

    GET /api/admin/plugin/available

响应
----

``plugins`` 中存放表示可安装插件信息的对象数组。
各对象的字段请参阅 `插件信息字段`_\ 。
可安装插件中包含下载来源的 ``url``\ 。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.8.0",
            "name": "fess-ds-slack",
            "version": "15.8.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.8.0/fess-ds-slack-15.8.0.jar"
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
      "version": "15.8.0"
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

.. note::

   ``name`` 和 ``version`` 必须与通过 ``/available`` 获取的可安装插件中的某一项匹配。
   若不存在匹配的构件，则返回错误。

响应
----

请求被接受后，返回 ``status`` 为 ``0`` （OK）的响应。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

当 ``name`` 或 ``version`` 对应的构件不存在时，``status`` 为
``1`` （BAD_REQUEST），并在 ``message`` 中设置 ``invalid name or version``\ 。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   安装处理在后台异步执行。\ ``status: 0`` 的响应仅表示请求已被接受，
   并不保证安装已完成。安装完成后，若已安装同名不同版本的插件，
   这些插件将被自动删除。下载或安装失败时，
   错误信息会记录在服务器日志中，但不会反映在API响应中。

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
      "version": "15.8.0"
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
     - 插件版本（最多100个字符）。建议指定以唯一确定删除目标。

响应
----

请求被接受后，返回 ``status`` 为 ``0`` （OK）的响应。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

.. note::

   删除处理在后台异步执行。\ ``status: 0`` 的响应仅表示请求已被接受，
   不判断对应插件是否存在或删除是否成功。删除失败时（如目标文件不存在等），
   错误信息会记录在服务器日志中，但不会反映在API响应中。

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
           "version": "15.8.0"
         }'

删除插件
--------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.8.0"
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
