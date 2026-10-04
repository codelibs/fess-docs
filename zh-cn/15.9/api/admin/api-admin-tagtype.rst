===========
TagType API
===========

概述
====

TagType API 是用于管理 |Fess| 用户标签（已登录的用户添加到文档上的、按用户管理的用户标签）的 API（请参阅 :doc:`../../admin/tagtype-guide` ）。无论 ``user.tag.enabled`` 的值如何，都可以管理所有用户的用户标签。

关于认证方式及响应的通用规范（``status`` 状态码、``version`` 字段、错误格式、
HTTP状态码等），请参阅 :doc:`api-admin-overview`。
访问本API需要使用具有管理API权限（``admin-api``）的访问令牌，
并通过 ``Authorization: Bearer <访问令牌>`` 请求头指定。

本 API 的 JSON 字段名为蛇形命名（ ``sort_order`` 、 ``virtual_host`` 、 ``seq_no`` 、 ``primary_term`` 等）。

基础 URL
========

::

    /api/admin/tagtype

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
     - 获取用户标签列表
   * - GET
     - /setting/{id}
     - 获取用户标签
   * - POST
     - /setting
     - 创建用户标签
   * - PUT
     - /setting
     - 更新用户标签
   * - DELETE
     - /setting/{id}
     - 删除用户标签

获取用户标签列表
================

请求
----

::

    GET /api/admin/tagtype/settings

参数
~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 参数
     - 类型
     - 必填
     - 说明
   * - ``size``
     - Integer
     - 否
     - 每页条数。默认为 ``paging.page.size`` 的设置值（默认 ``25`` ）。
   * - ``page``
     - Integer
     - 否
     - 页码（从 1 开始）。默认为 ``1`` 。
   * - ``name``
     - String
     - 否
     - 按名称筛选（通配符搜索，匹配包含所输入字符串的名称）。
   * - ``owner``
     - String
     - 否
     - 按所有者筛选（通配符搜索，匹配包含所输入字符串的所有者）。

用户标签按排序顺序、名称、所有者排序。

响应
----

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   列表不读取可能很长的用户标签路径，因此各元素没有 ``paths`` 。PUT 会整体替换用户标签，因此编辑前请先通过 ``GET /setting/{id}`` 获取，以保留其 ``paths`` 。

获取用户标签
============

请求
----

::

    GET /api/admin/tagtype/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` 和 ``primary_term`` 表示读取到的用户标签的版本。 ``paths`` 和 ``permissions`` 每行一个值。

创建用户标签
============

请求
----

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

字段说明
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``name``
     - String
     - 是
     - 用户标签名称。会经过 NFKC 规范化，连续的空白合并为一个空格，并去除首尾空白；规范化后的长度必须为 1 ～ ``user.tag.name.max.length`` （默认： ``50`` ）个字符，且不能包含控制字符或格式字符。
   * - ``owner``
     - String
     - 是
     - 拥有该用户标签的用户的登录用户 ID（最多 1000 个字符）。
   * - ``paths``
     - String
     - 否
     - 要添加用户标签的文档的 URL，多个时用换行符（ ``\n`` ）分隔。每个都必须与文档的 ``url`` 字段完全一致。最多 ``user.tag.max.paths`` （默认： ``10000`` ）个。
   * - ``permissions``
     - String
     - 否
     - 可以查看该用户标签的用户/组/角色（例如 ``{role}guest`` ），多个时用换行符（ ``\n`` ）分隔。为空时只有所有者可以查看。包含 ``{role}guest`` （ ``role.search.guest.permissions`` 的值）时，会与所有已登录的用户共享。
   * - ``virtual_host``
     - String
     - 否
     - 虚拟主机（最多 1000 个字符）。
   * - ``sort_order``
     - Integer
     - 否
     - 显示顺序（非负整数）。省略时为 ``0`` 。

用户标签的 ID 是由名称和所有者生成的用户标签值的 SHA-256，由服务器决定。所有者和名称的组合用于识别用户标签，因此所有者已有同名用户标签时，会返回验证错误（ ``status: 1`` ，“A tag with the same name and owner already exists.”）。

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

创建成功时， ``created`` 为 ``true`` 。

更新用户标签
============

请求
----

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

请求体
~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

除创建时的所有字段外，还需要以下字段。用户标签会被整体替换，因此请同时发送要保留的 ``paths`` 。

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``id``
     - String
     - 是
     - 要更新的用户标签的 ID。
   * - ``seq_no``
     - Integer
     - 是
     - ``GET /setting/{id}`` 返回的用户标签的 ``seq_no`` 。
   * - ``primary_term``
     - Integer
     - 是
     - ``GET /setting/{id}`` 返回的用户标签的 ``primary_term`` 。

- 如果读取后用户标签已被更改，即 ``seq_no`` 和 ``primary_term`` 不再一致，更新会返回验证错误（ ``status: 1`` ，“The tag was changed by someone else. Reload it and try again.”）。请重新获取用户标签后再试。
- 更改 ``name`` 或 ``owner`` 后，用户标签会获得新的 ID，响应中的 ``id`` 为新 ID。所有者已有新名称的用户标签时，更新会返回“A tag with the same name and owner already exists.”。
- 更改所有者后， ``permissions`` 中原所有者的用户权限会替换为新所有者的用户权限。

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

更新时， ``created`` 为 ``false`` 。

删除用户标签
============

请求
----

::

    DELETE /api/admin/tagtype/setting/{id}

响应
----

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

如果在删除过程中用户标签被更改，删除会返回“The tag was changed by someone else. Reload it and try again.”。

反映到文档
==========

通过本 API 创建、更新和删除用户标签时，会立即保存到用户标签信息中。在 ``user.tag.enabled`` 为 ``true`` 期间，对文档的更改（新增和移除的路径、重命名、删除）会放入队列，由每分钟运行一次的“Log Aggregator”（ ``log_aggregator`` ）作业反映。为 ``false`` 期间不会放入队列，请在启用用户标签功能后运行“Tag Updater”（ ``tag_updater`` ）作业。请参阅 :doc:`../../admin/tagtype-guide` 。

使用示例
========

与所有已登录的用户共享用户标签
------------------------------

.. code-block:: bash

    # 获取包含 paths、seq_no、primary_term 的用户标签
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 在权限中加上 {role}guest 后发回
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

获取某个用户的用户标签列表
--------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/tagtype/settings?owner=alice&size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考信息
========

- :doc:`api-admin-overview` - Admin API概述
- :doc:`../api-tag` - 用户标签 API
- :doc:`../../admin/tagtype-guide` - 用户标签管理指南
