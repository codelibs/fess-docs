===========================
通过搜索 API 与业务系统集成
===========================

前言
====

想在 CRM 的客户页面上列出相关资料，想在咨询登记页面上先显示相似的 FAQ，想让自家系统生成的报表也能被搜索。
这些需求都可以通过从业务系统的服务器调用 Fess 的搜索 API（\ ``/api/v2``\ ）来实现。

本文以 Fess 15.9 为对象，依次完成以下工作。

- 用 curl 调用搜索、标签、建议词和热门词 API，确认响应的结构
- 创建访问令牌，并通过令牌的角色控制返回哪些文档
- 编写从业务系统服务器端调用搜索 API 的函数
- 用 ``PUT /api/admin/documents/bulk`` 注册无法爬取的数据
- 为错误和速率限制做好准备

在现有网站中嵌入搜索框或搜索页面的方法（浏览器端嵌入、主题、Fess Site Search）请参见 :doc:`guide-03`。
如果尚未启动 Fess 并完成爬取，请先完成 :doc:`guide-02`。

本文构建的架构
==============

::

    [用户的浏览器] --> [业务系统的服务器] --(携带令牌)--> [Fess /api/v2]
                             令牌只放在这里

浏览器只访问业务系统，调用 Fess 的是业务系统的服务器。
访问令牌放在服务器的环境变量等位置，不要交给浏览器。
原因将在“创建访问令牌”中说明。

API 概览
========

Fess 15.9 本体提供的搜索类 API 位于 ``/api/v2`` 之下。
本文使用的 API 如下。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 端点
     - 用途
   * - ``GET /api/v2/search``
     - 全文搜索。结果位于 ``response.data`` 中
   * - ``GET /api/v2/labels``
     - 调用方可以使用的标签列表
   * - ``GET /api/v2/suggest-words``
     - 针对正在输入的词的建议候选
   * - ``GET /api/v2/popular-words``
     - 热门词
   * - ``GET /api/v2/health``
     - 搜索引擎的状态（在监控中的用法请参见 :doc:`guide-10`）
   * - ``PUT /api/admin/documents/bulk``
     - 批量注册文档（管理 API）

``/api/v2`` 的响应全部包装在 ``{"response": {...}}`` 中，``response.status`` 为 0 表示成功。
JSON 的键采用 ``snake_case``。

.. note::

   15.9 本体不提供 ``/api/v1``。
   如果要让调用 ``/api/v1`` 的现有客户端继续运行，需要插件 ``fess-webapp-v1-api``\ （Docker 镜像中未包含）。
   新建的集成请使用 ``/api/v2``。

先用 curl 试一试
================

如果处于可以匿名搜索的状态（[系统] > [通用] 中的「需要登录」为关闭，即默认状态），无需令牌即可调用。
中文等非 ASCII 字符或含空格的搜索词，用 ``-G --data-urlencode`` 进行 URL 编码后发送。
为了让输出更易读，这里使用了 ``jq``。

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=搜索 指南" \
        --data-urlencode "num=3" \
      | jq '.response | {status, record_count, page_size, data: [.data[] | {doc_id, title, url_link, content_description}]}'

响应的结构如下（\ ``data`` 只显示了第 1 条。值因环境而异）。

.. code-block:: json

    {
      "status": 0,
      "record_count": 12,
      "page_size": 3,
      "data": [
        {
          "doc_id": "5d4c0e0e5a7b4b5c9d2f6a1b3c8e7f90",
          "title": "搜索指南",
          "url_link": "https://fess.codelibs.org/zh-cn/stable/user/index.html",
          "content_description": "Fess 的<strong>搜索</strong><strong>指南</strong>。..."
        }
      ]
    }

``response`` 中还包含 ``page_count``、``next_page``、``exec_time``、``query_id`` 等。
``data`` 的各元素中只包含 ``title``、``url``、``url_link``、``content_description``、``last_modified``、``filetype``、``score`` 等允许用于 API 响应的字段。
正文全文（\ ``content``\ ）和标签（\ ``label``\ ）默认不返回。
如果要增加返回的字段，请添加到 ``fess_config.properties`` 的 ``query.additional.api.response.fields`` 中。
``content_description`` 是用 ``<strong>`` 标签包围搜索词的摘录，在页面上显示时，请将其作为 HTML 处理或去除标签。

常用参数如下。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 参数
     - 含义
   * - ``q``
     - 搜索词。可以使用与搜索页面相同的语法（AND、OR、排除、字段指定等）
   * - ``num`` / ``start``
     - 每页条数（默认 10，超过上限时会被调整为上限）和起始位置（从 0 开始）
   * - ``sort``
     - 排序方式。例如：``last_modified.desc``\ （按更新时间从新到旧）
   * - ``fields.label``
     - 按标签值筛选。可以重复指定

其他参数（分面、语言、地理位置等）请参见 `搜索 API <https://fess.codelibs.org/zh-cn/stable/api/api-search.html>`__。

标签、建议词和热门词也可以用同样的方式调用。

::

    $ curl -s "http://localhost:8080/api/v2/labels" | jq .response
    $ curl -s -G "http://localhost:8080/api/v2/suggest-words" --data-urlencode "q=fe" | jq .response
    $ curl -s "http://localhost:8080/api/v2/popular-words" | jq .response

结果分别位于 ``response.labels[]``\ （\ ``label`` 和 ``value``\ ）、``response.suggest_words[]``\ （\ ``text`` 和 ``types``\ ）、``response.popular_words``\ （字符串数组）中。
建议词和热门词为空的原因，将在“使用标签、建议词和热门词”中说明。

创建访问令牌
============

从业务系统调用时使用访问令牌。
令牌带有“权限”，搜索结果会按该权限进行筛选。

创建步骤
--------

1. 打开管理页面的 [系统] > [访问令牌]，点击 [新建]。
2. 在「名称」中输入能看出用途的名称（例如：``crm-search``）。
3. 在「权限」中，每行写一个允许此令牌显示的文档的角色。格式为 ``{role}角色名``、``{group}组名``、``{user}用户名``。
4. 按 ``2027-03-31T23:59:59`` 的格式输入「过期」。留空则没有期限。
5. 「参数名称」保持留空。
6. 点击 [创建]。返回列表后点击名称，记下详细页面中「令牌」显示的值（60 个字母数字字符）。

设置「参数名称」后，调用方就可以通过该请求参数追加权限。
除非能够完全掌控调用方，否则请不要使用。

令牌的发送方式
--------------

令牌通过 ``Authorization`` 请求头发送。
不带 ``Bearer`` 的 ``Authorization: <令牌>`` 也会被接受。

::

    $ export FESS_SEARCH_TOKEN=<记下的令牌>
    $ curl -s -G "http://localhost:8080/api/v2/search" \
        -H "Authorization: Bearer $FESS_SEARCH_TOKEN" \
        --data-urlencode "q=提案书" | jq '.response.record_count'

由于 ``api.access.token.request.parameter`` 默认为空，通过查询参数传递令牌的方式处于无效状态。
URL 会留在访问日志中，请使用请求头。

结果由令牌的角色决定
--------------------

在携带令牌的请求中，只有令牌的权限会被用作角色。
不带令牌的匿名调用所附带的访客角色（\ ``{role}guest``\ ），只要令牌的权限不为空，就不会被附加。

另一方面，新建爬取配置时权限栏中已填入 ``{role}guest``，因此普通的公开文档都带有 ``{role}guest``。
所以，权限只有 ``{group}sales`` 的令牌，会使公开文档从搜索结果中消失。
如果要同时返回公开文档和面向销售部的文档，请将令牌的权限设为如下 2 行。

::

    {role}guest
    {group}sales

设置完成后，请用相同的搜索词比较不带令牌和带令牌时的 ``record_count``，确认其增减符合预期。
文档端的权限设计请参见 :doc:`guide-05`。

不把令牌交给浏览器的原因
------------------------

- 写在浏览器 JavaScript 中的令牌，任何人都能用开发者工具读取。读取到的人可以绕过业务系统，搜索该令牌权限下可见的所有文档。
- 令牌不是按用户发放的，而是把发放时指定的权限打包在一起。分发给浏览器后，用户之间的权限差异就不复存在。
- 即使开启了「需要登录」，只要有有效的令牌，``/search``、``/documents/all``、``/documents/export``、``/suggest-words``、``/labels``、``/popular-words`` 无需登录也会响应。泄露的令牌可以被用来代替登录。

如果要根据业务系统的用户改变可见范围，请按范围分别创建令牌，并在服务器端根据用户选择使用。

从服务器端调用搜索 API
======================

下面是放在业务系统后端的 Python 函数示例。
它只使用标准库，并把搜索结果精简为页面所需的项目后返回。

.. code-block:: python

    import json
    import os
    import urllib.error
    import urllib.parse
    import urllib.request

    FESS_URL = os.environ.get("FESS_URL", "http://localhost:8080")
    FESS_SEARCH_TOKEN = os.environ["FESS_SEARCH_TOKEN"]


    class FessApiError(Exception):
        def __init__(self, http_status, code, retry_after=None):
            super().__init__(f"Fess API error: {http_status} {code}")
            self.http_status = http_status
            self.code = code
            self.retry_after = retry_after


    def search_documents(query, label=None, num=5):
        params = [("q", query), ("num", str(num))]
        if label:
            params.append(("fields.label", label))
        url = FESS_URL + "/api/v2/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + FESS_SEARCH_TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                body = json.load(res)
        except urllib.error.HTTPError as e:
            try:
                code = json.load(e)["response"]["error"]["code"]
            except (ValueError, KeyError, TypeError):
                code = "unknown"
            raise FessApiError(e.code, code, e.headers.get("Retry-After")) from e
        response = body["response"]
        return {
            "total": response["record_count"],
            "items": [
                {
                    "title": doc.get("title"),
                    "url": doc.get("url_link"),
                    "snippet": doc.get("content_description"),
                    "last_modified": doc.get("last_modified"),
                }
                for doc in response["data"]
            ],
        }

如果是 CRM 的客户页面，就像 ``search_documents("示例股份有限公司", label="sales_docs")`` 这样传入客户名称和标签，并将返回值直接渲染到页面上。

- 超时时间设置得比 Fess 端的搜索超时（\ ``query.timeout``\ ，默认 10000 毫秒）稍长一些。
- 根据 ``FessApiError`` 的 ``code`` 和 ``retry_after`` 决定显示给用户的消息以及是否重试（参见“错误处理”）。
- ``content_description`` 包含 ``<strong>`` 标签，因此在模板中以 HTML 输出时，请将允许的标签限定为 ``<strong>``。

注册外部系统的数据
==================

无法爬取的数据（业务系统生成的报表、工单摘要等）可以通过管理 API 的 ``PUT /api/admin/documents/bulk`` 直接注册到索引中。

为管理 API 单独准备令牌
-----------------------

管理 API 需要权限中带有 ``{role}admin-api`` 的令牌（\ ``api.admin.access.permissions=Radmin-api``\ ）。
该权限允许访问管理 API 的所有端点。
不存在仅限于注册文档的权限。
它还可以操作爬取配置、用户以及访问令牌本身，因此请像对待管理员密码一样妥善保管。

另外，如果用只有 ``{role}admin-api`` 的令牌进行搜索，角色只有 ``admin-api``，因此几乎不会返回任何文档。
请将搜索用和注册用的令牌分开。
在 [系统] > [访问令牌] 中再创建一个权限只有 ``{role}admin-api`` 一行的令牌（例如名称为 ``crm-indexer``），并记下它的值。

::

    $ export FESS_ADMIN_TOKEN=<记下的管理 API 用令牌>

注册
----

``url`` 和 ``title`` 为必填项。
``content`` 是正文，``label`` 是标签值的数组。

::

    $ curl -s -X PUT "http://localhost:8080/api/admin/documents/bulk" \
        -H "Authorization: Bearer $FESS_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "documents": [
            {
              "url": "https://crm.example.com/reports/2026-11",
              "title": "2026年11月 销售月报",
              "content": "11月的新商机比上月有所增加。",
              "label": ["sales_docs"]
            }
          ]
        }' | jq .response

成功后，每个文档的结果会返回在 ``items`` 中。
新建时为 ``CREATED``，更新现有文档时为 ``OK``。

.. code-block:: json

    {
      "version": "15.9",
      "status": 0,
      "items": [
        { "result": "CREATED", "id": "9c1e47b2...e04b" }
      ]
    }

``id`` 是根据 ``url`` 等计算出的哈希值（16 进制 128 位），上例中省略了中间部分。
用搜索用令牌搜索 ``q=销售月报`` 能找到所注册的文档，即表示注册完成。

注册时的注意事项
----------------

- 如果省略 ``role``，会附加访客角色，文档将可被任何人搜索到。如果要限制可见范围，请在 ``role`` 中以数组形式填入内部格式的值。内部格式中，``{role}x`` 为 ``Rx``，``{group}x`` 为 ``2x``，``{user}x`` 为 ``1x``\ （例如：``"role": ["2sales"]``）。
- 文档的 ID 由 ``url`` 和 ``role``\ （以及虚拟主机）生成。用相同的 ``url`` 重新发送会更新文档，但更改 ``role`` 后发送则会作为另一个文档添加，旧文档仍会保留。
- 响应中的 ``items[].id`` 是索引上的 ID，与文档的 ``doc_id`` 是不同的值。逐条删除的 ``DELETE /api/admin/searchlist/doc/{id}`` 需要传入搜索结果中的 ``doc_id``。按条件批量删除时使用 ``DELETE /api/admin/searchlist/query``\ （\ `SearchList API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-searchlist.html>`__\ ）。
- 只有部分文档失败时，``status`` 为 9，失败的元素中会包含 ``message``。缺少 ``url`` 或 ``title``、值的类型不匹配等请求本身无效的情况下，``status`` 为 1，不会注册任何内容。

使用标签、建议词和热门词
========================

用标签建立分类
--------------

用于 ``fields.label`` 筛选的标签，在 [爬虫] > [标签] 中创建。
「值」只能使用字母数字和下划线（不能使用 ``sales-docs`` 或中文等非 ASCII 字符）。
对于爬取的文档，当 URL 与标签的「包含的路径」匹配时会附加标签（\ :doc:`guide-04`\ ）。
对于批量注册的文档，请像上一节那样发送 ``label``。

``/api/v2/labels`` 只返回调用方的角色可以使用的标签。
标签也有权限，因此与令牌权限不匹配的标签不会出现在列表中。
门户的分类列表可以根据该响应中的 ``label``\ （显示名称）和 ``value``\ （传给 ``fields.label`` 的值）来生成。

建议词
------

``/api/v2/suggest-words`` 按 ``q`` 的前缀匹配返回候选。
条数由 ``num``\ （默认 10）指定，目标字段通过重复指定 ``fn`` 来设置。
候选的来源包括爬取文档中的词（[系统] > [通用] 中的「按文档建议」）、搜索词（同一页面的「按搜索词建议」）以及管理员注册的建议词。
文档中的词要等到调度器的“Suggest Indexer”作业（默认每天 1 次）运行之后才会出现在候选中。
候选也会按调用方的角色进行筛选。

热门词
------

``/api/v2/popular-words`` 返回从搜索日志中收集的搜索词里被频繁搜索的词。
如果返回空数组，请确认以下几点。

- 如果 [系统] > [通用] 中的「热门词响应」（\ ``web.api.popularword``\ ，默认开启）为关闭，会返回 ``invalid_request``\ （HTTP 400）。
- 「按搜索词建议」需要开启。只有在该设置开启时才会收集搜索词。
- 同一个词需要被搜索 10 次以上（\ ``suggest.popular.word.query.freq=10``\ ）。来自同一会话的重复搜索，在 1 分钟以内只计为 1 次。刚部署时为空是正常的。
- 统计对象仅为只以访客角色执行的搜索（\ ``suggest.search.log.permissions={user}guest,{role}guest``\ ）。带有 ``{group}sales`` 等权限的令牌或已登录用户的搜索不会被计入。
- 热门词也会按调用方的角色进行筛选。被统计的词只带有访客角色，因此权限中不含 ``{role}guest`` 的令牌总是得到空结果。
- 结果会被缓存，因此即使搜索增加也不会立即变化。

更改 ``seed`` 后，会从候选中返回不同的组合。

错误处理
========

``/api/v2`` 在出错时返回 HTTP 状态码和 ``response.error.code``。

::

    {"response": {"status": 1, "error": {"code": "invalid_request", "message": "..."}}}

集成方应预先确定处理方式的错误如下。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - HTTP
     - ``error.code``
     - 原因与处理
   * - 400
     - ``invalid_request``
     - ``num`` 小于等于 0、搜索词语法错误、``q`` 超过 ``api.param.max.length``\ （默认 1000 个字符）等。不要重试，请检查输入
   * - 401
     - ``auth_required``
     - 令牌未注册或已过期，或者在「需要登录」开启时未携带令牌。携带无效的令牌时，不会退回为匿名处理，而是返回 401。请重新创建令牌
   * - 503
     - ``service_unavailable``
     - 搜索引擎处理不过来而拒绝了搜索。响应中带有 ``Retry-After: 5``，可以等待 5 秒后重试
   * - 500
     - ``internal_error``
     - Fess 内部错误。请查看 [系统信息] > [日志文件] 中的 ``fess.log``

关于速率限制，登录、修改密码、聊天、导出的各端点分别有各自的上限，超过时返回 429 ``rate_limited`` 和 ``Retry-After``。
服务器整体的请求数限制（\ ``rate.limit.enabled``\ ）默认处于禁用状态。
启用后，超限时 429 的响应体为 ``{"error":"rate_limit_exceeded", ...}``，而不是上面的 ``response`` 结构。
从业务系统的服务器调用时，请注意所有搜索都来自同一个 IP 地址。
详情请参见 `速率限制配置 <https://fess.codelibs.org/zh-cn/stable/config/rate-limiting.html>`__。

管理 API（\ ``/api/admin/*``\ ）的错误结构有所不同。
没有令牌，或令牌不带有 ``{role}admin-api`` 时，返回 HTTP 401，``response.status`` 为 3，原因位于 ``response.message`` 中。

从浏览器直接调用的情况（CORS）
==============================

服务器之间的调用与 CORS 无关。
只有在浏览器的 JavaScript 直接调用其他源上的 Fess 时，``fess_config.properties`` 中的 ``api.cors.allow.origin``\ （默认 ``*``）、``api.cors.allow.methods``、``api.cors.allow.headers``\ （默认包含 ``Authorization``）、``api.cors.allow.credentials``\ （默认 ``true``）、``api.cors.max.age``\ （默认 ``3600`` 秒）才会生效。

当 ``api.cors.allow.origin`` 为 ``*`` 时，不允许携带 Cookie 等认证信息的请求。
如果要让浏览器以已登录用户的权限进行搜索，请像 ``https://portal.example.com`` 这样列出源（以逗号分隔）。
在 Docker 中，也可以在 ``FESS_JAVA_OPTS`` 中指定 ``-Dfess.config.api.cors.allow.origin=https://portal.example.com``。
修改后请重启 Fess。
浏览器端的嵌入方法请参见 :doc:`guide-03`。

延伸阅读
========

- 想在现有网站中嵌入搜索框或搜索页面：:doc:`guide-03`
- 想设计按令牌或按用户可见的文档：:doc:`guide-05`
- 想将 API 用于健康检查和监控：:doc:`guide-10`
- 想用管理 API 和 fessctl 以代码方式管理配置：:doc:`guide-16`
- 想在包括 SSO 和访问令牌运维在内的层面保护搜索平台：:doc:`guide-15`

参考资料
========

- `API 概述 <https://fess.codelibs.org/zh-cn/stable/api/api-overview.html>`__
- `搜索 API <https://fess.codelibs.org/zh-cn/stable/api/api-search.html>`__
- `标签 API <https://fess.codelibs.org/zh-cn/stable/api/api-label.html>`__
- `建议词 API <https://fess.codelibs.org/zh-cn/stable/api/api-suggest.html>`__
- `热门词 API <https://fess.codelibs.org/zh-cn/stable/api/api-popularword.html>`__
- `Documents API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-documents.html>`__
- `Admin API 概述 <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-overview.html>`__
- `访问令牌 <https://fess.codelibs.org/zh-cn/stable/admin/accesstoken-guide.html>`__
