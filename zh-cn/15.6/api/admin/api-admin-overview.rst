==========================
Admin API 概述
==========================

概述
====

|Fess| Admin API是用于通过程序访问管理功能的RESTful API。
您可以通过API执行几乎所有可在管理界面中进行的操作，包括爬虫设置、用户管理、调度器控制等。

通过使用此API，您可以自动化 |Fess| 的配置，或与外部系统集成。

基础URL
=======

Admin API的基础URL格式如下：

::

    http://<Server Name>/api/admin/

例如，在本地环境中：

::

    http://localhost:8080/api/admin/

认证
====

访问Admin API需要通过访问令牌进行认证。

获取访问令牌
------------

1. 登录管理界面
2. 导航到"系统"→"访问令牌"
3. 点击"新建"
4. 输入令牌名称并选择所需权限
5. 点击"创建"获取令牌

使用令牌
--------

在请求头中包含访问令牌：

::

    Authorization: Bearer <访问令牌>

或者通过查询参数指定：

::

    ?token=<访问令牌>

cURL示例
~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

所需权限
--------

使用Admin API需要令牌具有以下权限：

- ``admin-*`` - 访问所有管理功能
- ``admin-scheduler`` - 仅限调度器管理
- ``admin-user`` - 仅限用户管理
- 其他功能特定的权限

通用模式
========

获取列表（GET/PUT /settings）
-----------------------------

获取设置列表。

请求
~~~~

::

    GET /api/admin/<resource>/settings
    PUT /api/admin/<resource>/settings

参数（分页）：

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 参数
     - 类型
     - 说明
   * - ``size``
     - Integer
     - 每页记录数（默认：20）
   * - ``page``
     - Integer
     - 页码（从0开始）

响应
~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

获取单个设置（GET /setting/{id}）
---------------------------------

通过指定ID获取单个设置。

请求
~~~~

::

    GET /api/admin/<resource>/setting/{id}

响应
~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

新建（POST /setting）
---------------------

创建新设置。

请求
~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

响应
~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

更新（PUT /setting）
--------------------

更新现有设置。

请求
~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

响应
~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

删除（DELETE /setting/{id}）
----------------------------

删除设置。

请求
~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

响应
~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

响应格式
========

成功响应
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        ...
      }
    }

``status: 0`` 表示成功。

错误响应
--------

.. code-block:: json

    {
      "response": {
        "status": 1,
        "errors": [
          {"code": "errors.failed_to_create", "args": ["...", "..."]}
        ]
      }
    }

HTTP状态码
----------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 状态码
     - 说明
   * - 200
     - 请求成功
   * - 400
     - 请求参数无效
   * - 401
     - 需要认证（无令牌或令牌无效）
   * - 403
     - 无访问权限
   * - 404
     - 资源未找到
   * - 500
     - 服务器内部错误

可用API
=======

|Fess| 提供以下Admin API。

爬虫设置
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-webconfig`
     - Web爬虫设置
   * - :doc:`api-admin-fileconfig`
     - 文件爬虫设置
   * - :doc:`api-admin-dataconfig`
     - 数据存储设置

索引管理
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-documents`
     - 文档批量操作
   * - :doc:`api-admin-crawlinginfo`
     - 爬虫信息
   * - :doc:`api-admin-failureurl`
     - 失败URL管理
   * - :doc:`api-admin-backup`
     - 备份/恢复

调度器
------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-scheduler`
     - 任务调度
   * - :doc:`api-admin-joblog`
     - 任务日志获取

用户和权限管理
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-user`
     - 用户管理
   * - :doc:`api-admin-role`
     - 角色管理
   * - :doc:`api-admin-group`
     - 组管理
   * - :doc:`api-admin-accesstoken`
     - API令牌管理

搜索调优
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-labeltype`
     - 标签类型
   * - :doc:`api-admin-keymatch`
     - 关键词匹配
   * - :doc:`api-admin-boostdoc`
     - 文档提升
   * - :doc:`api-admin-elevateword`
     - 提升词
   * - :doc:`api-admin-badword`
     - 屏蔽词
   * - :doc:`api-admin-relatedcontent`
     - 相关内容
   * - :doc:`api-admin-relatedquery`
     - 相关查询
   * - :doc:`api-admin-suggest`
     - 建议管理

系统
----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-general`
     - 常规设置
   * - :doc:`api-admin-systeminfo`
     - 系统信息
   * - :doc:`api-admin-stats`
     - 系统统计
   * - :doc:`api-admin-log`
     - 日志获取
   * - :doc:`api-admin-searchlog`
     - 搜索日志管理
   * - :doc:`api-admin-storage`
     - 存储管理
   * - :doc:`api-admin-plugin`
     - 插件管理

词典
----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-dict`
     - 词典管理（同义词、停用词等）

使用示例
========

创建Web爬虫设置
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

启动计划任务
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取用户列表
------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`../api-overview` - API概述
- :doc:`../../admin/accesstoken-guide` - 访问令牌管理指南

