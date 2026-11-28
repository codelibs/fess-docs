=======================================
用 AI 搜索模式（RAG）让内部文档回答问题
=======================================

前言
====

与其逐个打开搜索结果对比阅读，很多人更希望直接问一句“报销的截止日是哪天？”，然后得到基于内部文档的回答。
Fess 的 AI 搜索模式（RAG 聊天）会由 Fess 自己搜索与问题相关的文档，把其内容交给 LLM（大语言模型）生成回答，并附上作为依据的文档链接一并返回。

本文介绍在 Fess 15.9 中运行 AI 搜索模式、限定可以使用的人和参考的文档，并通过界面和 API 确认其运行情况。
完成本文的步骤后，您将能够：

- 从 4 种 LLM 提供商中选择一个，安装对应的插件并完成设置
- 使用 docker-fess 提供的叠加用 Compose 文件，为 Docker 上的 Fess 连接 LLM
- 限定可以使用聊天的用户，以及作为回答依据的文档范围
- 通过搜索界面、\ ``/api/v2/chat``\ 和搜索日志确认其正常运行

前提是 Fess 已经启动，并且已经爬取了文档。
如果尚未完成，请按照 :doc:`guide-02` 的步骤进行准备。
查找意思相近文档的语义搜索在 :doc:`guide-18` 中介绍，让 AI 代理搜索 Fess 的 MCP 在 :doc:`guide-20` 中介绍。

AI 搜索模式的工作原理
=====================

AI 搜索模式不使用专用的向量索引。
它用与普通搜索相同的搜索处理（默认是关键词搜索）查找文档，因此无需准备嵌入模型或分块即可开始使用。
如果启用了语义搜索，它也会自动加入 AI 搜索模式的搜索中。

处理流程因调用的端点而异。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 端点
     - 处理流程
   * - ``POST /api/v2/chat/stream``\ （搜索界面的 AI 搜索使用）
     - 意图判定 → 搜索 → 由 LLM 评估相关度 → 获取正文 → 生成回答。各阶段的进度和回答片段以 Server-Sent Events 依次返回
   * - ``POST /api/v2/chat``
     - 意图判定 → 搜索 → 生成回答。不进行相关度评估，结果以一个 JSON 返回

无论哪种方式，当搜索结果为 0 件时，LLM 都会重新生成搜索词并再次搜索（默认最多 2 次，\ ``rag.chat.query.regeneration.max.count``\ ）。
由于一个问题会多次调用 LLM，响应时间比普通搜索更长，使用云端 LLM 时每次调用都会产生费用。

发送给 LLM 的是用户的问题，以及搜索找到的文档正文或其摘录。
选择提供商时，请确认这些数据的发送目的地。

会话通过 ``session_id`` 识别，保存在 Fess 的内存中。
默认情况下，30 分钟没有操作就会被清除（\ ``rag.chat.session.timeout.minutes``\ ），一个会话最多保留 30 条消息（\ ``rag.chat.history.max.messages``\ ）。
重启 Fess 也会清除会话。

选择 LLM 提供商
===============

在 Fess 15.9 中，与 LLM 的连接由各提供商对应的 ``fess-llm-*`` 插件提供。
使用哪个提供商由 ``rag.llm.name`` 指定。

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - 提供商
     - ``rag.llm.name``
     - 插件
     - 默认模型
     - 连接所需的设置，以及问题和文档的发送目的地
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url``\ （默认 ``http://localhost:11434``\ ）。发送目的地是您自己运行的 Ollama 服务器
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``\ 。发送目的地是 OpenAI
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``\ 。发送目的地是 Google
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region``\ （默认 ``us-east-1``\ ），以及 ``rag.llm.bedrock.api.key`` 或 AWS 凭证。发送目的地是指定区域的 Amazon Bedrock

模型可以通过 ``rag.llm.<提供商>.model`` 更改。

OpenAI 和 Gemini 只需准备 API 密钥即可开始使用，但问题和文档会发送到各自的服务。
Ollama 不会把问题和文档发送到自己的服务器之外，但需要一台运行模型的服务器。
docker-fess 的 Ollama 用 Compose 文件以 NVIDIA GPU 为前提。
Bedrock 需要 AWS 凭证和区域设置。
设置方法请参阅 `Amazon Bedrock配置 <https://fess.codelibs.org/zh-cn/stable/config/llm-bedrock.html>`__\ 。

需要的三项设置
==============

要运行 AI 搜索模式，以下三项必须全部具备。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 设置
     - 设置位置
     - 在 Docker 中的传递方式
   * - ``rag.chat.enabled=true``\ （默认为 ``false``\ ）
     - ``fess_config.properties``\ 。管理界面中没有对应的项目
     - 在 ``FESS_JAVA_OPTS`` 中加入 ``-Dfess.config.rag.chat.enabled=true``
   * - ``fess-llm-*`` 插件
     - [系统] > [插件]，或 ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0`` 等
   * - ``rag.llm.name`` 以及各提供商的连接设置
     - ``rag.llm.name`` 在 [系统] > [通用] 中设置，连接设置（\ ``rag.llm.<提供商>.*``\ ）在 ``fess_config.properties`` 中设置
     - ``-Dfess.system.rag.llm.name=openai``\ 、\ ``-Dfess.config.rag.llm.openai.api.key=...`` 等

``rag.llm.name`` 的默认值是 ``ollama``\ 。
如果只安装了 OpenAI 插件而不修改 ``rag.llm.name``\ ，Fess 会一直寻找并不存在的 Ollama 客户端，AI 搜索模式将无法使用。
此时日志中会出现 ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` 警告。

``-Dfess.system.rag.llm.name`` 是仅在 ``system.properties`` 中没有值时才使用的初始值。
在 [通用] 中保存的值写入 ``system.properties`` 后，以该值为准。

在 Docker 中运行（OpenAI、Gemini）
==================================

docker-fess 提供了用于连接 LLM 的叠加用 Compose 文件。
在 :doc:`guide-02` 中放置 Compose 文件的目录下，下载 v15.9.0 的文件。

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

将 API 密钥放入 shell 的环境变量，指定三个文件启动。

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` 会为 ``fess01`` 添加以下环境变量。
API 密钥和模型名取自 shell 的 ``OPENAI_API_KEY`` 和 ``OPENAI_MODEL``\ （未设置时为 ``gpt-5-mini``\ ），因此无需在文件中写入密钥。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

``FESS_PLUGINS`` 中的插件会在容器启动时先于 Fess 安装，因此无需另行重启。
如果 ``fess01`` 已在运行，此命令会重新创建 ``fess01``\ ，在 [通用] 中更改过的设置会随容器一起丢失。
之后的 ``ps``\ 、\ ``logs``\ 、\ ``down`` 等命令也请指定同样的三个文件。

使用 Gemini 时，下载 ``compose-gemini.yaml``\ ，设置 ``GEMINI_API_KEY``\ ，并以同样的方式将其指定为第三个文件。
该文件从 ``GEMINI_MODEL``\ （未设置时为 ``gemini-2.5-flash``\ ）设置模型，因此使用的是 ``gemini-2.5-flash``\ ，而不是插件的默认模型。

.. note::

   如果指定了两个以上设置 ``FESS_JAVA_OPTS`` 的叠加用文件，则只使用最后一个文件的值（与 OCR 用的设置等组合时）。
   这种情况下，请自行准备一个 Compose 文件，把所需的 ``-D`` 选项全部合并到一个 ``FESS_JAVA_OPTS`` 中。
   ``FESS_JAVA_OPTS`` 以空白分隔，因此无法写入值中含有空格的选项。

像 ``-Dfess.config.rag.llm.openai.api.key`` 这样传递的 API 密钥，在 [系统信息] > [配置信息] 中会以掩码形式显示。
如果需要通过公司内部代理访问外部，请添加 ``-Dfess.config.http.proxy.host=...`` 和 ``-Dfess.config.http.proxy.port=...``\ 。
LLM 插件使用 Fess 通用的代理设置。

在 Docker 中运行（Ollama）
==========================

``compose-ollama.yaml`` 会添加 Ollama 容器 ``ollama01``\ ，并将 ``fess01`` 连接到它。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 对象
     - 设置的内容
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``\ 、\ ``-Dfess.config.rag.chat.enabled=true``\ 、\ ``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - 镜像 ``ollama/ollama:latest``\ 、网络 ``search_net``\ 、端口 11434、卷 ``ollama-data``\ 、分配 1 块 NVIDIA GPU

由于没有设置 ``rag.llm.name`` 和模型，将使用默认值 ``ollama`` 和 ``gemma4:e4b``\ 。
之所以把 URL 指向 ``ollama01``\ ，是因为默认的 ``http://localhost:11434`` 会指向 ``fess01`` 容器自身。

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

使用该文件需要安装了 NVIDIA Container Toolkit 的环境。
在没有 GPU 的环境中试用时，请从下载的文件中删除 ``ollama01`` 的 ``deploy:`` 及其以下部分。
此时在 CPU 上运行，回答需要较长时间。

只有当设置的模型出现在 Ollama 的模型列表（\ ``/api/tags``\ ）中时，Fess 才判定 Ollama 可用，默认每 60 秒进行一次该检查。
因此，拉取模型后大约 1 分钟，AI 搜索模式即可使用。
文件开头的注释中写有另一个文件名和拉取 ``gpt-oss:20b`` 的步骤，但请按照上述步骤操作。
要使用其他模型，请先 ``ollama pull`` 该模型，再在 ``FESS_JAVA_OPTS`` 中添加 ``-Dfess.config.rag.llm.ollama.model=<模型名>``\ 。

在 Docker 以外（ZIP、RPM、DEB）进行设置
=======================================

1. 安装插件。在 [系统] > [插件] > [安装] 中选择，或用命令安装

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. 在 ``fess_config.properties`` 中添加设置。ZIP 版为 ``app/WEB-INF/classes/fess_config.properties``\ ，RPM/DEB 版为 ``/etc/fess/fess_config.properties``

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. 重启 Fess。插件和 ``fess_config.properties`` 的更改都会在重启时加载
4. 打开 [系统] > [通用]，在「AI搜索」栏的「LLM提供商」中选择 ``openai``\ ，然后点击 [更新]

「AI搜索」栏只有在 ``rag.chat.enabled=true`` 且至少加载了一个 LLM 插件时才会显示。
「LLM提供商」的选项只有已安装插件对应的提供商。
如果找不到该栏，请重新检查步骤 1～3。

确认运行情况
============

在搜索界面中确认
----------------

1. 打开 ``http://localhost:8080/``\ 。顶部导航栏中会显示带有机器人图标的 [AI搜索]
2. 点击 [AI搜索]，打开聊天界面（\ ``/chat``\ ）
3. 输入一个已爬取文档中可能有答案的问题。如果在 :doc:`guide-02` 中爬取了搜索指南，可以试试“请告诉我通配符搜索中可以使用哪些符号”等问题

生成回答期间，会依次显示分析、搜索、评估、获取、回答各个阶段。
回答下方会在「来源」中按编号列出作为依据的文档，与正文中 ``[1]`` 这样的编号相对应。
需要切换话题时，点击 [新对话] 即可清除会话历史。

如果没有显示 [AI搜索]，请参阅后面的“常见问题”。

通过 API 确认
-------------

如果不使用界面进行确认，请调用 ``/api/v2/ui/config``\ 。
如果 ``response.features.rag_chat_enabled`` 为 ``true``\ ，则该用户可以使用 AI 搜索模式。

对于 ``/api/v2/chat`` 等会改变状态的请求，需要通过 ``X-Fess-CSRF-Token`` 请求头发送与会话绑定的 CSRF 令牌。
``/api/v2/ui/config`` 的响应中包含令牌，因此请一边保存 Cookie 一边获取，再用同一 Cookie 调用（示例中使用 ``jq``\ ）。

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"请告诉我通配符搜索中可以使用哪些符号"}' | jq '.response'

响应中的 ``content`` 是回答，\ ``sources`` 是作为依据的文档（\ ``rank``\ 、\ ``title``\ 、\ ``url`` 等），\ ``session_id`` 是会话 ID。
继续提问时，请像 ``{"message":"...","session_id":"<上次的 session_id>"}`` 这样把 ``session_id`` 发回。

该示例以未登录的匿名用户身份调用，因此只有带有 ``{role}guest`` 的文档才是搜索对象。
以已登录用户身份调用的方法、流式版本 ``/api/v2/chat/stream`` 的事件以及错误代码，请参阅 `Chat API <https://fess.codelibs.org/zh-cn/stable/api/api-chat.html>`__ 和 `API 概述 <https://fess.codelibs.org/zh-cn/stable/api/api-overview.html>`__\ 。
``/api/v1/chat`` 是仅在安装了 ``fess-webapp-v1-api`` 插件时才能使用的旧格式 API。
新建的集成请使用 ``/api/v2/chat``\ 。

在管理界面和日志中确认
----------------------

[系统信息] > [搜索日志] 的 [AI 聊天] 标签页中，会显示请求数、用户数、总令牌数、平均响应时间、错误率，以及按用户、按意图、按模型统计的件数。
该记录由 ``rag.chat.log.enabled``\ （默认 ``true``\ ）启用，问题和回答的正文不会被记录。
令牌数仅在 LLM 插件报告时才会记录。

在 Docker 中，可以通过容器日志确认插件是否已安装。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

如果有 ``Installing fess-llm-openai-15.9.0.jar``\ ，说明已安装。
如果持续出现 ``[LLM] LlmClient not found``\ ，说明 ``rag.llm.name`` 与已安装的插件不一致。

限定用户和参考的文档
====================

AI 搜索模式的搜索与普通搜索一样，会按角色进行过滤。
用户在搜索结果中看不到的文档，既不会用作回答的依据，也不会作为来源。
每个文档对谁可见，由爬取配置的「权限」决定。
设计思路请参阅 :doc:`guide-05`\ 。

在此基础上，还可以在 [系统] > [通用] 的「AI搜索」栏中限定聊天本身的使用范围。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 内容
   * - 「聊天权限」（\ ``rag.chat.permissions``\ ）
     - 以逗号分隔指定可以使用聊天的用户，例如 ``{role}rag_user,{group}sales,{user}taro``\ 。为空时所有人都可以使用。如果也要让未登录的用户使用，请包含 ``{role}guest``
   * - 「聊天标签」（\ ``rag.chat.labels``\ ）
     - 将作为回答依据的文档限定为带有任一指定标签值的文档。以逗号分隔指定，例如 ``faq,policy``\ ，为空时以用户可见的所有文档为对象

不在「聊天权限」范围内的用户看不到 [AI搜索]，API 在未登录时返回 401，已登录时返回 403。
已登录的用户不带有 ``{role}guest``\ ，因此如果只指定 ``{role}guest``\ ，已登录的用户将无法使用聊天。
如果保存了没有任何有效项目的值（例如只有 ``{role}``\ ），则任何人都无法使用。

「聊天标签」适用于这样的场景：例如给公司规章和 FAQ 等可信赖的回答依据文档预先加上标签，只让聊天基于这些文档回答。
标签的创建和添加方法请参阅 :doc:`guide-04`\ 。

常见问题
========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 症状
     - 需要确认的内容
   * - 不显示 [AI搜索]
     - 按以下顺序确认。(1) 是否传递了 ``rag.chat.enabled=true``\ 。(2) 是否安装了插件（日志中的 ``Installing``\ ）。(3) ``rag.llm.name`` 是否与安装的插件一致（\ ``LlmClient not found`` 警告）。(4) API 密钥是否为空，使用 Ollama 时是否已拉取模型。(5) 自己是否不在「聊天权限」范围内
   * - [通用] 中没有「AI搜索」栏
     - ``rag.chat.enabled`` 仍为 ``false``\ ，或者没有加载 LLM 插件。请确认在完成设置和安装插件后是否重启了 Fess
   * - 执行 ``down`` 和 ``up -d`` 后「LLM提供商」恢复了原值
     - [通用] 中的值保存在 ``fess01`` 容器内的 ``system.properties`` 中，因此重新创建容器后会丢失。请通过 ``FESS_JAVA_OPTS`` 中的 ``-Dfess.system.rag.llm.name`` 指定
   * - API 返回 ``403``
     - 确认是否通过 ``X-Fess-CSRF-Token`` 发送了 CSRF 令牌，以及是否发送了获取令牌时的 Cookie。已登录用户不在「聊天权限」范围内时也会返回 403
   * - API 返回 ``429``
     - 每个用户每分钟最多 30 次（\ ``api.chat.rate.limit.per.user.per.minute``\ ）
   * - 无法连接云端 LLM
     - 确认容器能否访问外部；如果需要代理，请设置 ``http.proxy.host`` 和 ``http.proxy.port``

想提高回答质量时，首先要确认搜索的质量。
AI 搜索模式以普通搜索中排名靠前的文档（默认 5 件，\ ``rag.chat.context.max.documents``\ ）为依据，因此如果用问题中的词语搜索时排在前面的是无关文档，回答也会受其影响。
搜索的改进在 :doc:`guide-08` 中介绍。
各提示类型的温度和最大令牌数，以及提示的替换，请参阅 `AI 搜索（RAG）与 LLM 集成概述 <https://fess.codelibs.org/zh-cn/stable/config/llm-overview.html>`__\ 。

延伸阅读
========

- 即使关键词不一致，也想把意思相近的文档加入搜索结果：\ :doc:`guide-18`
- 想让 Claude 等 AI 代理搜索 Fess：\ :doc:`guide-20`
- 想按部门或角色区分可搜索的文档：\ :doc:`guide-05`
- 想通过查看搜索日志来改进搜索质量：\ :doc:`guide-08`
- 想让用户通过 SSO 登录，并按用户区分可见内容：\ :doc:`guide-15`

参考资料
========

- `AI搜索模式功能配置 <https://fess.codelibs.org/zh-cn/stable/config/rag-chat.html>`__
- `AI 搜索（RAG）与 LLM 集成概述 <https://fess.codelibs.org/zh-cn/stable/config/llm-overview.html>`__
- `Ollama配置 <https://fess.codelibs.org/zh-cn/stable/config/llm-ollama.html>`__
- `OpenAI配置 <https://fess.codelibs.org/zh-cn/stable/config/llm-openai.html>`__
- `Google Gemini配置 <https://fess.codelibs.org/zh-cn/stable/config/llm-gemini.html>`__
- `Amazon Bedrock配置 <https://fess.codelibs.org/zh-cn/stable/config/llm-bedrock.html>`__
- `Chat API <https://fess.codelibs.org/zh-cn/stable/api/api-chat.html>`__
- `AI搜索模式（面向用户） <https://fess.codelibs.org/zh-cn/stable/user/chat-search.html>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `docker-fess 的 compose 目录（v15.9.0） <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
