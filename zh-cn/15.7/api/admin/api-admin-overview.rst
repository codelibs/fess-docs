==========================
Admin API 概述
==========================

概述
==========

|Fess| Admin API是用于通过程序访问管理功能的RESTful API。
您可以通过API执行几乎所有可在管理界面中进行的操作，包括爬虫设置、用户管理、调度器控制等。

通过使用此API，您可以自动化 |Fess| 的配置，或与外部系统集成。

基础URL
==========

Admin API的基础URL格式如下：

::

    http://<Server Name>/api/admin/

例如，在本地环境中：

::

    http://localhost:8080/api/admin/

认证
==========

访问Admin API需要通过访问令牌进行认证。

获取访问令牌
--------------------

1. 登录管理界面
2. 导航到"系统"→"访问令牌"
3. 点击"新建"
4. 输入令牌名称，并在"权限"栏中设置要授予令牌的权限（使用Admin API时，请输入 ``{role}admin-api``）
5. 点击"创建"获取令牌

使用令牌
--------------------

在请求头中包含访问令牌：

::

    Authorization: Bearer <访问令牌>

也可以省略 ``Bearer``，仅指定令牌：

::

    Authorization: <访问令牌>

也可以通过查询参数指定，但默认情况下该方式被禁用。在 ``fess_config.properties`` 的
``api.access.token.request.parameter`` 中设置参数名后，即可使用该名称传递
令牌（默认值为空，因此仅请求头指定方式有效）。
例如，设置 ``api.access.token.request.parameter=token`` 时：

::

    ?token=<访问令牌>

cURL示例
~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

所需权限
--------------------

Admin API的访问不是按功能控制的，而是由单一的权限集控制。要使用Admin API的
任意端点，访问令牌必须被授予 ``fess_config.properties`` 的
``api.admin.access.permissions`` 中所设置的权限之一。

默认值为 ``Radmin-api``，这是角色 ``admin-api`` 的编码形式
（开头的 ``R`` 是 ``role.search.role.prefix`` 的值）。在创建访问令牌时，
若在权限栏中输入 ``{role}admin-api``，则内部会保存为 ``Radmin-api``。

.. note::

   不存在按各个资源区分的不同权限（如 ``admin-scheduler`` 或 ``admin-user`` 等），
   也不存在通配符（``admin-*``）。具有所设置权限的令牌可以访问
   所有Admin API端点。如需更改允许访问的权限，
   请修改 ``api.admin.access.permissions`` 的值。

通用模式
==========

具有设置的资源（如 webconfig、user、role 等）遵循以下通用的CRUD模式。
但是，部分资源（systeminfo、stats、storage、plugin、log、backup、documents、suggest、dict 根等）
具有与该通用模式不同的独立端点结构，请参阅各资源的页面。

获取列表（GET /settings）
----------------------------------

获取设置列表。

请求
~~~~~~~~

::

    GET /api/admin/<resource>/settings

参数（分页）：

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 参数
     - 类型
     - 说明
   * - ``size``
     - Integer
     - 每页记录数（默认：25。可通过 ``fess_config.properties`` 的 ``paging.page.size`` 更改）
   * - ``page``
     - Integer
     - 页码（从1开始。默认：1。指定0以下的值时按1处理）

响应
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   所有响应的 ``response`` 对象中始终包含表示产品版本的 ``version``
   （例如： ``"15.7.0"``）。为简洁起见，后续示例中可能省略该字段。

获取单个设置（GET /setting/{id}）
----------------------------------------

通过指定ID获取单个设置。

请求
~~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

响应
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

新建（POST /setting）
----------------------------

创建新设置。

请求
~~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

响应
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

更新（PUT /setting）
----------------------------

更新现有设置。

请求
~~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

响应
~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

删除（DELETE /setting/{id}）
------------------------------------

删除设置。

请求
~~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

响应
~~~~~~~~

删除响应的格式因资源（操作）而异。多数资源仅返回
``status``。

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

部分资源会将删除结果作为 ``ApiUpdateResponse`` 返回，并附带已删除设置的
``id`` 和 ``created``（删除时为 ``false``）。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

此外，返回 ``ApiDeleteResponse`` 的资源还可能附带表示删除数量的 ``count``
（默认值 ``1``）。实际格式请参阅各资源的页面。

响应格式
==========

所有响应均由 ``response`` 对象包装，并始终包含表示产品版本的
``version`` 和表示处理结果的 ``status``。

``status`` 的取值如下。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 值
     - 说明
   * - ``0``
     - OK（成功）
   * - ``1``
     - BAD_REQUEST（请求无效）
   * - ``2``
     - SYSTEM_ERROR（系统错误）
   * - ``3``
     - UNAUTHORIZED（认证错误）
   * - ``9``
     - FAILED（处理失败）

成功响应
--------------------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` 表示成功。

错误响应
--------------------

发生错误时， ``status`` 会被设置为 0 以外的值， ``message`` 中包含错误消息。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

HTTP状态码
--------------------

Admin API在大多数情况下返回 HTTP 状态 ``200``，处理结果通过响应正文的
``status`` 字段表示。因此，成功与失败的判定请不要依据 HTTP 状态码，
而应依据正文中 ``status`` 的值。

实际返回的 HTTP 状态码如下。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 状态码
     - 说明
   * - 200
     - 通常的响应。除成功时（``status: 0``）外，大多数错误也以此状态码
       返回。例如，访问令牌未指定或无效，或权限不足时，会以
       ``status: 3``，系统错误会以 ``status: 2``，均以 HTTP ``200`` 返回。
   * - 400
     - 请求参数的验证错误。响应正文的 ``status`` 为 ``1``。
       尝试获取不存在的资源时也以此状态码返回。
   * - 401
     - 发生登录认证相关的异常时。响应正文的 ``status`` 为 ``3``。
       需要注意的是，访问令牌未指定或无效时，并非返回此状态码，而是以 HTTP ``200`` 返回
       ``status: 3``。

.. note::

   Admin API不会返回 ``403``、``404``、``500`` 等 HTTP 状态码。
   权限不足或资源不存在，也通过 HTTP ``200`` 或 ``400`` 响应正文中所包含的
   ``status`` 来表示。

可用API
==========

|Fess| 提供以下Admin API。

爬虫设置
--------------------

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

.. note::

   此外，以下与认证信息和爬取控制相关的资源也作为API提供
   （目前尚未提供独立页面）： ``webauth``（Web认证）、 ``fileauth``（文件认证）、
   ``reqheader``（请求头）、 ``pathmap``（路径映射）、
   ``duplicatehost``（重复主机）、 ``searchlist``（搜索/文档列表操作）。

索引管理
--------------------

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
--------------------

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
--------------------

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
--------------------

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
--------------------

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
   * - :doc:`api-admin-searchlist`
     - 文档搜索与管理
   * - :doc:`api-admin-storage`
     - 存储管理
   * - :doc:`api-admin-plugin`
     - 插件管理

词典
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 端点
     - 说明
   * - :doc:`api-admin-dict`
     - 词典管理（同义词、停用词等）

使用示例
==========

创建Web爬虫设置
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "userAgent": "Mozilla/5.0 (compatible; Fess)",
           "numOfThread": 1,
           "intervalTime": 1000,
           "boost": 1.0,
           "maxAccessCount": 1000,
           "depth": 3,
           "sortOrder": 1,
           "available": "true"
         }'

.. note::

   创建Web爬虫设置时，``name``、``urls``、``userAgent``、``numOfThread``、
   ``intervalTime``、``boost``、``available``、``sortOrder`` 为必填项。如果省略
   这些字段，将产生验证错误（``status: 1``）。``available`` 以字符串指定，
   设置为 ``"true"`` 或 ``"false"``。

启动计划任务
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

获取用户列表
--------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
==========

- :doc:`../api-overview` - API概述
- :doc:`../../admin/accesstoken-guide` - 访问令牌管理指南
