==========================
WebConfig API
==========================

概述
====

WebConfig API是用于管理 |Fess| Web爬虫设置的API。
可以操作爬虫目标URL、爬虫深度、排除模式等设置。

基础URL
=======

::

    /api/admin/webconfig

.. note::

   所有端点均需要管理员权限及有效的访问令牌。
   有关认证方式，请参阅 :doc:`api-admin-overview` 。

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
     - 获取Web爬虫设置列表
   * - GET
     - /setting/{id}
     - 获取Web爬虫设置
   * - POST
     - /setting
     - 创建Web爬虫设置
   * - PUT
     - /setting
     - 更新Web爬虫设置
   * - DELETE
     - /setting/{id}
     - 删除Web爬虫设置

获取Web爬虫设置列表
====================

请求
----

::

    GET /api/admin/webconfig/settings

.. note::

   列表获取端点除 ``GET`` 外，也可使用 ``PUT`` 访问。

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - 参数
     - 类型
     - 必需
     - 说明
   * - ``page``
     - Integer
     - 否
     - 页码（从1开始，默认：1）
   * - ``size``
     - Integer
     - 否
     - 每页记录数（默认：25。遵循 ``paging.page.size`` 设置）
   * - ``name``
     - String
     - 否
     - 按设置名称筛选
   * - ``urls``
     - String
     - 否
     - 按爬虫URL筛选
   * - ``description``
     - String
     - 否
     - 按说明筛选

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "示例站点",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
            "numOfThread": 1,
            "intervalTime": 1000,
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

``total`` 表示符合条件的设置总数。

获取Web爬虫设置
===============

请求
----

::

    GET /api/admin/webconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "示例站点",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   响应中包含在注册和更新时由服务器自动设置的 ``createdBy`` 、 ``createdTime`` 、
   ``updatedBy`` 、 ``updatedTime`` 、 ``versionNo`` 字段。
   ``versionNo`` 在更新时为必填项（请参阅后述的"更新Web爬虫设置"）。

创建Web爬虫设置
===============

请求
----

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 字段
     - 必需
     - 说明
   * - ``name``
     - 是
     - 设置名称（最多200个字符）
   * - ``description``
     - 否
     - 设置说明（最多1000个字符）
   * - ``urls``
     - 是
     - 爬虫起始URL（多个URL用换行符分隔）。使用 ``http:`` 或 ``https:`` 协议指定
   * - ``includedUrls``
     - 否
     - 爬虫目标URL的正则表达式模式
   * - ``excludedUrls``
     - 否
     - 排除爬虫URL的正则表达式模式
   * - ``includedDocUrls``
     - 否
     - 索引目标URL的正则表达式模式
   * - ``excludedDocUrls``
     - 否
     - 排除索引URL的正则表达式模式
   * - ``configParameter``
     - 否
     - 附加配置参数（ ``key=value`` 格式，每行一项）
   * - ``depth``
     - 否
     - 爬虫深度（0以上）
   * - ``maxAccessCount``
     - 否
     - 最大访问数（0以上）
   * - ``userAgent``
     - 是
     - User-Agent字符串（最多200个字符）
   * - ``numOfThread``
     - 是
     - 并行线程数（1以上）
   * - ``intervalTime``
     - 是
     - 访问间隔（毫秒，0以上）
   * - ``boost``
     - 是
     - 搜索结果提升值
   * - ``available``
     - 是
     - 启用/禁用（字符串 ``"true"`` / ``"false"``）
   * - ``sortOrder``
     - 是
     - 显示顺序（0以上）
   * - ``permissions``
     - 否
     - 访问权限角色（多个时用换行符分隔）
   * - ``virtualHosts``
     - 否
     - 虚拟主机（多个时用换行符分隔）

.. note::

   ``createdBy`` 、 ``createdTime`` 、 ``updatedBy`` 、 ``updatedTime`` 等审计字段
   由服务器自动设置，无需在请求体中指定。

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

更新Web爬虫设置
===============

请求
----

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

请求体
~~~~~~

更新时，除创建时的字段外，还需要指定用于确定更新目标的 ``id`` 和版本号 ``versionNo`` 。
``versionNo`` 需填写获取API（GET）响应中包含的当前值。

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

更新时的附加字段
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 字段
     - 必需
     - 说明
   * - ``id``
     - 是
     - 更新目标的设置ID（最多1000个字符）
   * - ``versionNo``
     - 是
     - 更新目标的当前版本号。填写获取API（GET）响应中包含的 ``versionNo`` 值

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_webconfig_id",
        "created": false
      }
    }

删除Web爬虫设置
===============

请求
----

::

    DELETE /api/admin/webconfig/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

URL模式示例
===========

``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` 中可使用正则表达式。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 模式
     - 说明
   * - ``.*example\\.com.*``
     - 包含example.com的所有URL
   * - ``https://example\\.com/docs/.*``
     - 仅/docs/目录下
   * - ``.*\\.(pdf|doc|docx)$``
     - PDF、DOC、DOCX文件
   * - ``.*\\?.*``
     - 带查询参数的URL
   * - ``.*/(login|logout|admin)/.*``
     - 包含特定路径的URL

使用示例
========

企业网站爬虫设置
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

文档网站爬虫设置
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`api-admin-fileconfig` - 文件爬虫设置API
- :doc:`api-admin-dataconfig` - 数据存储设置API
- :doc:`../../admin/webconfig-guide` - Web爬虫设置指南
