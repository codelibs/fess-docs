============================
通过 MCP 让 AI 代理搜索 Fess
============================

前言
====

想让 Claude Code 等 AI 代理查阅公司内部文档时，如果代理能够直接调用 Fess 的搜索，就可以把已索引的文档直接作为依据。
实现这一点的机制就是 MCP（Model Context Protocol）。
在 Fess 中，安装插件 ``fess-webapp-mcp`` 后，会在 ``/mcp`` 上添加 MCP 服务器的端点。

本文介绍如何在 Fess 15.9 中安装该插件、将认证设为必需，并从 AI 代理进行连接，直到确认其正常工作。

完成本文的步骤后，将达到以下状态。

- 可以用 ``curl`` 确认 ``/mcp`` 正在工作
- 不带访问令牌的调用会被拒绝
- 可以通过令牌的权限决定代理能够搜索的文档范围
- 可以从 Claude Code 调用 Fess 的 ``search`` 工具

.. note::

   与 :doc:`guide-19` 中的 AI 搜索模式相比，调用方向正好相反。
   在 AI 搜索模式下，由 Fess 调用 LLM（Ollama、OpenAI 等）来生成回答。Ollama 是为此运行 LLM 的环境，并不是 MCP 客户端。
   而在 MCP 中，由外部 AI 代理把 Fess 作为搜索工具来调用，回答由代理一侧的 LLM 生成。

``/mcp`` 提供的内容
===================

``/mcp`` 只接受 ``POST``，每个请求返回一个 JSON（不保持会话）。
搜索与搜索页面经过相同的处理，因此按角色过滤搜索结果的机制同样生效。

15.9.0 版插件提供的内容如下。
全部为只读，没有任何会修改 Fess 数据的操作。

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - 名称
     - 内容
     - 可用条件
   * - ``search`` （工具）
     - 全文搜索。每条结果都带有 ``doc_id``
     - 始终可用
   * - ``suggest`` （工具）
     - 针对正在输入的词语给出的建议候选
     - 始终可用
   * - ``get_document`` （工具）
     - 指定 ``doc_id`` 获取一篇文档的正文
     - 始终可用
   * - ``get_index_stats`` （工具）
     - 索引名称、文档数、JVM 内存使用量
     - 默认设置下不可用（见后文）
   * - ``fess://document/{doc_id}`` （资源）
     - 以资源的形式进行与 ``get_document`` 相同的获取
     - 始终可用
   * - ``fess://index/stats`` （资源）
     - 与 ``get_index_stats`` 内容相同
     - 与 ``get_index_stats`` 相同
   * - ``basic_search`` / ``advanced_search`` （提示词）
     - 用于搜索的提示词模板。``advanced_search`` 还接受 ``sort`` 和 ``num``
     - 始终可用

在 ``search`` 中省略 ``num`` 时，只返回 3 条结果（``mcp.default.page.size`` 的默认值）。
无论是 ``search`` 的摘录还是 ``get_document`` 的正文，都会被截断为最多 10000 个字符，``get_document`` 中的 ``truncated`` 会变为 ``true``\ （``mcp.content.max.length``）。

安装插件
========

插件版本应与 Fess 的次版本号保持一致。
Fess 15.9 请使用 ``fess-webapp-mcp`` 的 15.9.x。
通过以下任一方式安装，安装后重启 Fess。

- 管理界面：在 [系统] > [插件] 中点击 [安装]，在 [远程] 选项卡中选择 ``fess-webapp-mcp`` 并安装
- 命令行：``bin/fess-setup install plugin fess-webapp-mcp:15.9.0``
- Docker：在 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 里添加 ``FESS_PLUGINS``。Docker 镜像中不包含此插件

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"

在 Docker 版中，如果名称或版本写错，该插件会被跳过，容器仍会照常启动。
添加后，请在启动日志中确认插件已被获取。

.. warning::

   升级 Fess 时，请在启动之前把此插件也替换为新版本。
   如果旧版本（例如 15.8 用）插件的 jar 仍留在 ``WEB-INF/plugin`` 中，Fess 15.9 会在启动时初始化失败，不仅是 ``/mcp``，所有页面和 API 都会返回 404。
   在命令行中，可以用 ``bin/fess-setup upgrade plugins`` 进行替换。

重启后，如果日志文件 ``fess.log`` 中出现以下 WARN，说明端点已启用。

::

    [MCP] mcp.auth.mode=none - every /mcp caller is treated as anonymous. Set mcp.auth.mode=fess_token, ...

此消息表示端点正以下一节所述的“无认证”状态运行。

先在无认证状态下确认工作情况
============================

.. warning::

   刚安装完成的 ``/mcp`` 在无认证状态下工作（``mcp.auth.mode=none``）。
   任何能够访问 ``/mcp`` 的人，都能以未登录用户（访客）的相同权限进行搜索，甚至可以通过 ``get_document`` 获取文档正文。
   权限保持默认值 ``{role}guest`` 的爬取配置中的文档，都会被暴露。
   在此状态下的试用请仅限于本地环境，并按下一节的说明将认证设为必需。
   另外，如果在 [系统] > [通用] 中启用了「需要登录」，此状态下的 ``/mcp`` 会以 HTTP 403 拒绝所有调用。这种情况下请直接进入下一节。

假设 Fess 运行在 ``http://localhost:8080``，调用 ``server/discover``。

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: server/discover' \
        -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

如果响应的 ``result.supportedVersions`` 中包含 ``2026-07-28``，``result.capabilities`` 中包含 ``tools`` 等，就说明调用成功。

接着调用 ``search`` 工具。
请在 ``q`` 中指定已爬取文档中包含的词语。

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: tools/call' \
        -H 'Mcp-Name: search' \
        -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"q":"Fess","num":5},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

``result.structuredContent.hits`` 中是搜索结果，``total`` 中是命中数。
请求头的值必须与请求正文一致。
``MCP-Protocol-Version`` 应与 ``params._meta`` 中的版本相同，``Mcp-Method`` 应与 ``method`` 相同，``Mcp-Name`` 应与工具名称相同。
不一致时会返回 HTTP 400（错误代码 ``-32020``）。

将认证设为必需
==============

切换到使用 Fess 访问令牌进行认证的 ``fess_token`` 模式。
另外还有使用外部授权服务器签发的 JWT 进行认证的 ``oauth`` 模式。
其设置请参阅 README 中的“OAuth 2.1 reference”。

创建访问令牌
------------

1. 打开管理界面的 [系统] > [访问令牌]，点击 [新建]
2. 在「名称」中输入能看出用途的名称，例如 ``mcp-agent``
3. 在「权限」中，每行输入一个允许代理查看的文档的角色。如果只需要面向访客的文档，输入 ``{role}guest`` 即可（如何确定请参见“令牌的权限与搜索结果”）
4. 根据需要指定「过期」，然后点击 [创建]
5. 在列表中点击所创建令牌的名称，详细信息页面的「令牌」中会显示其值

设置 mcp.auth.mode
------------------

``mcp.*`` 的设置全部从 Fess 的系统属性（``system.properties``）中读取。
写在 ``fess_config.properties`` 或 ``-Dfess.config.*`` 中会被忽略，既不报错也不输出日志。

ZIP 版在 ``app/WEB-INF/conf/system.properties`` 中、RPM/DEB 版在 ``/etc/fess/system.properties`` 中添加以下一行。

::

    mcp.auth.mode=fess_token

该值会在运行期间重新读取，因此几秒内即可生效，无需重启。

Docker 版的 ``fess01`` 容器没有卷，写在容器内文件中的设置会在重新创建容器时丢失。
请在 ``compose.yaml`` 的 ``FESS_JAVA_OPTS`` 中加上 ``-Dfess.system.`` 前缀进行指定（不是 ``fess.config.``）。

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"
      - "FESS_JAVA_OPTS=-Dfess.system.mcp.auth.mode=fess_token"

``FESS_PLUGINS`` 和 ``FESS_JAVA_OPTS`` 会在重新创建容器时生效。
编辑 ``compose.yaml`` 后，执行以下命令。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

如果 ``system.properties`` 中有相同的键，则以其为准。

确认认证已生效
--------------

原样再次执行上一节的 ``server/discover``。
由于没有附带令牌，会返回 HTTP 401 和 ``WWW-Authenticate: Bearer realm="fess-mcp"`` 响应头（可用 ``curl -i`` 显示响应头）。
在 ``fess_token`` 模式下，``server/discover`` 也需要认证。

接着，在上一节 ``search`` 的 ``curl`` 中加上 ``-H 'Authorization: Bearer <令牌>'`` 后执行。
将 ``<令牌>`` 替换为详细信息页面中显示的值。
如果返回了搜索结果，设置就完成了。
使用不存在或已过期的令牌时，会返回 HTTP 401。

令牌的权限与搜索结果
====================

在 ``fess_token`` 模式下，令牌的权限会直接作为搜索时的角色。
不仅 ``search``，``get_document`` 也会按相同的角色进行过滤，因此即使知道 ``doc_id``，也无法获取没有权限的文档。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 令牌的权限
     - 可搜索的文档
   * - 空
     - 与访客相同（``{role}guest`` 的文档）
   * - ``{role}guest``
     - 与访客相同
   * - ``{role}sales``
     - 仅 ``{role}sales`` 的文档。不包括面向访客的文档
   * - ``{role}sales`` 和 ``{role}guest``
     - 两者的文档

只有权限为空的令牌才会自动补上访客角色。
如果希望代理同时搜索部门文档和面向全员的文档，请同时指定 ``{role}guest``。
关于角色和权限的思路，请参阅 :doc:`guide-05`。

要进行确认，可以用权限不同的两个令牌对同一个词执行 ``search``，比较 ``total``。

.. warning::

   请不要给代理用的令牌加上 ``{role}admin-api``。
   拥有 ``{role}admin-api`` 的令牌可以调用 Fess 的全部 Admin API。
   而且，用只有 ``{role}admin-api`` 的令牌执行 ``search`` 时，由于没有文档拥有此角色，结果为 0 条。

使 ``get_index_stats`` 可用
---------------------------

``get_index_stats`` 和 ``fess://index/stats`` 只会显示给拥有 ``mcp.tools.index_stats.permissions`` 中所列任一权限的调用方。
默认值为 ``Radmin-api``\ （``{role}admin-api`` 的内部表示），在 ``none`` 模式下任何调用方都不具备权限，因此不会显示给任何人。
对没有权限的调用方，会返回与不存在的工具相同的错误。

如果只是搜索，则不需要此工具。
如需使用，请不要授予 ``{role}admin-api``，而是另行确定一个专用角色，并把该角色加到令牌的权限中。
``system.properties`` 一侧要用内部表示书写（``{role}`` 写作 ``R``）。

::

    mcp.tools.index_stats.permissions=Rmcp-stats

在此示例中，在令牌的权限中添加 ``{role}mcp-stats``。

其他设置
========

以下设置都写在 ``system.properties`` 中（Docker 版为 ``-Dfess.system.<键>``）。
布尔值只有 ``true`` 会被视为真，``1`` 或 ``yes`` 会被视为假。

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - 键
     - 默认值
     - 内容
   * - ``mcp.allowed.origins``
     - （空）
     - 从浏览器调用时允许的 ``Origin``，以 ``https://app.example.com`` 的形式用逗号分隔指定。为空时，带有 ``Origin`` 请求头的请求全部以 HTTP 403 拒绝。``curl`` 和 CLI 代理不会发送 ``Origin``，因此不受影响
   * - ``mcp.rate.limit.per.minute``
     - ``60``
     - 每个调用方（令牌；没有令牌时为 IP 地址）每分钟 ``tools/call`` 等调用的上限。超过时返回 HTTP 429 和 ``Retry-After``。设为 ``0`` 则禁用
   * - ``mcp.content.max.length``
     - ``10000``
     - ``search`` 和 ``get_document`` 返回的正文的最大字符数
   * - ``mcp.default.page.size``
     - ``3``
     - 在 ``search`` 中省略 ``num`` 时的条数
   * - ``mcp.enabled``
     - ``true``
     - 设为 ``false`` 时，``/mcp`` 一律返回 HTTP 503
   * - ``mcp.legacy.protocol.enabled``
     - ``true``
     - 也接受通过 ``initialize`` 连接的旧版（``2025-11-25`` / ``2025-06-18``）客户端

以下两项与 ``mcp.*`` 不同，是 Fess 自身的 ``fess_config.properties`` 中的设置（Docker 版为 ``-Dfess.config.<键>``）。

- 经由其他主机上的反向代理时，请把代理的 IP 地址加入 ``rate.limit.trusted.proxies``\ （默认值 ``127.0.0.1,::1``）。不加入的话，经由代理的调用方会全部共享同一个上限
- 从浏览器以其他源（Origin）调用时，除了 ``mcp.allowed.origins`` 之外，还要在 ``api.cors.allow.headers`` 中添加 ``MCP-Protocol-Version``、``Mcp-Method``、``Mcp-Name``。详情请参阅 README 中的“Browser clients”

从 AI 代理连接
==============

Claude Code
-----------

Claude Code 可以用 ``2026-07-28`` 直接连接。
用 ``claude mcp add`` 将其注册为 HTTP 的 MCP 服务器，并用 ``--header`` 传递令牌。

::

    $ claude mcp add --transport http fess http://localhost:8080/mcp \
        --header "Authorization: Bearer <令牌>"

执行 ``claude mcp list`` 会显示已注册的 ``fess``，也可以确认连接状态。
如果向 Claude Code 提出“在 Fess 中搜索出差报销的流程”这样的请求，代理会用如下参数调用 ``search`` 工具，再用结果中的 ``doc_id`` 调用 ``get_document`` 读取正文。

.. code-block:: json

    {
      "name": "search",
      "arguments": {
        "q": "出差 报销",
        "num": 5,
        "fields": { "label": ["manual"] }
      }
    }

``fields`` 的 ``label`` 中指定 Fess 标签的值（不按标签筛选时省略）。
``search`` 的参数还有 ``start``\ （分页）、``sort``\ （``last_modified.desc`` 等）、``lang`` 等。

其他客户端
----------

OpenCode、Codex CLI、Gemini CLI 等通过旧版（``initialize``）连接的客户端，只要 ``mcp.legacy.protocol.enabled`` 为默认值 ``true`` 也可以使用。
只支持 ``2025-03-26`` 及更早版本的客户端无法连接。
只能通过 stdio 启动 MCP 服务器的桌面客户端，需要经由在 stdio 与 HTTP 之间中继的 ``mcp-remote``。
各客户端能否连接，汇总在 README 的“Client compatibility”中。

注意搜索结果会被发送到外部
--------------------------

如果代理使用的 LLM 是云服务，``search`` 的摘录和 ``get_document`` 的正文会被发送到该服务。
通过令牌的权限只选择可以发送的文档，并根据需要调小 ``mcp.content.max.length``，就能缩小发送的范围。

故障排除
========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 症状
     - 原因与处理
   * - HTTP 400，错误代码 ``-32020``
     - 缺少 ``MCP-Protocol-Version``、``Mcp-Method``、``Mcp-Name``，或与正文不一致
   * - HTTP 401
     - 在 ``fess_token`` 模式下令牌缺失、不存在或已过期
   * - 所有请求都返回 HTTP 403
     - ``Origin`` 请求头不在 ``mcp.allowed.origins`` 中。或者在 ``none`` 模式下启用了「需要登录」
   * - 首次调用返回 ``-32601`` 且提到 ``initialize``
     - 是旧版客户端，且 ``mcp.legacy.protocol.enabled`` 不是 ``true``
   * - ``search`` 结果为 0 条
     - 令牌的权限中没有文档的角色。如果结果中的 ``partial`` 为 ``true``，说明搜索未完成（超时或 OpenSearch 故障），不一定是没有匹配项
   * - ``Tool execution failed (error_code:...)``
     - 原因以 WARN 记录在 ``fess.log`` 中。用 ``error_code`` 的值搜索日志

延伸阅读
========

- 想按角色区分通过 MCP 公开的文档：:doc:`guide-05`
- 想让 Fess 自身用 LLM 回答：:doc:`guide-19`
- 想在关键词不一致时也能找到含义相近的文档：:doc:`guide-18`
- 想在业务系统中使用搜索 API，或想按用途分别使用访问令牌：:doc:`guide-11`
- 想统一设置 SSO 和访问保护：:doc:`guide-15`

参考资料
========

- `fess-webapp-mcp README（15.9.0） <https://github.com/codelibs/fess-webapp-mcp/blob/fess-webapp-mcp-15.9.0/README.md>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `访问令牌 <https://fess.codelibs.org/zh-cn/stable/admin/accesstoken-guide.html>`__
- `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__
- `Model Context Protocol <https://modelcontextprotocol.io/>`__
