==========================
Documents API
==========================

概述
====

Documents API是用于将文档批量注册到 |Fess| 索引的Admin API。
不经过爬虫，即可将外部系统生成的文档直接添加到索引中。
一次请求可同时注册多个文档。

基础URL
=======

::

    /api/admin/documents

认证
====

调用此API需要通过 :doc:`api-admin-overview` 中所述的访问令牌进行认证。
令牌必须具有Admin API的访问权限（默认为 ``Radmin-api`` ）。
此权限可通过配置键 ``api.admin.access.permissions`` 进行修改。

端点列表
========

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 方法
     - 路径
     - 说明
   * - PUT
     - /bulk
     - 文档批量注册

.. note::

   此端点仅接受 ``PUT`` 方法。

文档批量注册
============

将多个文档批量注册到索引中。

请求
----

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "示例页面 1",
          "content": "这是页面 1 的正文文本。"
        },
        {
          "url": "https://example.com/page2",
          "title": "示例页面 2",
          "content": "这是页面 2 的正文文本。"
        }
      ]
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 必需
     - 说明
   * - ``documents``
     - 是
     - 要注册的文档数组。每个文档以字段名与值的映射形式指定。若为 ``null`` 或空数组，将返回错误（ ``status`` = ``1`` ）。

文档字段
~~~~~~~~

每个文档可以自由指定索引字段的名称与值的映射。
至少需要指定 ``url`` 和 ``title`` （遵循必填字段配置
``index.admin.required.fields`` ，默认值为 ``url,title,role,boost`` ；
``role`` 和 ``boost`` 会按后文所述自动补全，因此实际上 ``url`` 和 ``title`` 为必填项）。

以下字段省略时将自动补全默认值：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 省略时的默认值
   * - ``content_length``
     - ``title`` 与 ``content`` 的字符数之和
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - 搜索访客角色（为访客用户设置的搜索角色）
   * - ``last_modified``
     - 当前时间
   * - ``timestamp``
     - 当前时间

此外，以下字段将在注册时自动生成：

- ``id`` - 由文档的 ``url`` （以及 ``role`` 、 ``virtual_host`` ）确定性生成，
  用作OpenSearch上的文档ID（ ``_id`` ）。响应中的 ``items[].id`` 将返回此值。
- ``doc_id`` - 每次注册时生成随机UUID，作为文档字段存储。

.. note::

   由于 ``id`` 是由 ``url`` 确定性生成的，对相同 ``url`` 的文档再次注册时，
   将更新已有文档（ ``items[].result`` 为 ``OK`` ）。

补充说明
~~~~~~~~

- 若 ``lang`` 字段包含 ``"auto"`` ，将从正文自动检测语言。
- 指定 ``config_id`` 时，将应用对应爬取配置的摄取管道（ingest pipeline）。
- 若缩略图生成已启用（ ``thumbnail.crawler.enabled`` ），注册时将尝试生成缩略图。
- 各字段的值将按照字段类型配置（ ``index.admin.array.fields`` 、
  ``index.admin.date.fields`` 、 ``index.admin.long.fields`` 等）进行验证。
  类型不匹配时将返回错误（ ``status`` = ``1`` ）。

响应
----

响应以 ``items`` 数组返回所注册的各文档的处理结果。
成功的项目包含 ``result`` 和 ``id`` ，失败的项目包含 ``result`` 和 ``message`` 。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

``status`` 为 ``0`` 表示所有文档均注册成功。
``items[].result`` 在新建时为 ``CREATED`` ，更新已有文档时为 ``OK`` 。

若有任意项目注册失败，则 ``status`` 为 ``9`` （FAILED），
失败项目中将包含 ``message`` 字段（ ``result`` 将设置为 ``CONFLICT`` 或
``BAD_REQUEST`` 等错误状态名）。成功的项目仍会返回 ``id`` 。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

.. note::

   若请求本身无效（ ``documents`` 未指定或为空、必填字段缺失、
   字段类型不匹配等），则不会执行文档注册处理，
   将返回包含 ``status`` = ``1`` （BAD_REQUEST）和 ``message`` 的错误响应。
   此情况下不返回 ``items`` 数组。

响应字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 字段
     - 说明
   * - ``items``
     - 各文档处理结果的数组
   * - ``items[].result``
     - 处理结果状态名。新建时为 ``CREATED`` ，更新时为 ``OK`` ，失败时为 ``BAD_REQUEST`` 等错误状态名
   * - ``items[].id``
     - 已注册文档的ID（仅成功时）
   * - ``items[].message``
     - 失败原因的消息（仅失败时）

使用示例
========

文档批量注册
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "示例页面 1",
               "content": "这是页面 1 的正文文本。"
             }
           ]
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-searchlist` - 文档搜索与管理API
- :doc:`api-admin-crawlinginfo` - 爬虫信息API
- :doc:`../../admin/searchlist-guide` - 搜索列表管理指南
