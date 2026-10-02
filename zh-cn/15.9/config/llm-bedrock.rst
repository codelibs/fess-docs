===================================
Amazon Bedrock配置（AI 搜索 / RAG）
===================================

概述
====

本页说明如何配置 ``fess-llm-bedrock`` 插件，以便 |Fess| 使用 Amazon Bedrock 实现其 **AI搜索模式（RAG：Retrieval-Augmented Generation）** ，并将其用作内容分块的嵌入提供商。

Amazon Bedrock 是 AWS 提供的服务，通过一个 API 提供 Amazon 及其他模型提供商的基础模型。
插件会调用您所选 AWS 区域中的 Bedrock Runtime API:

- **AI搜索模式**: Converse API（流式回答使用 ``ConverseStream`` ）
- **内容分块嵌入**: InvokeModel API，使用 Amazon Titan Text Embeddings V2 或 Cohere Embed

支持的模型
----------

AI搜索模式可使用在您所用区域中支持 Converse API 的任意模型。
默认值是通过美国跨区域推理配置文件使用的 Amazon Nova 2 Lite，即 ``us.amazon.nova-2-lite-v1:0`` 。
``rag.llm.bedrock.model`` 可接受模型ID、推理配置文件ID（例如带有 ``us.`` 、 ``eu.`` 或 ``global.`` 前缀的ID）或ARN。

内容分块嵌入支持以下模型。

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - 模型
     - ``content_chunker.embedding.dimension``
     - 每次请求的文本数
   * - ``amazon.titan-embed-text-v2:0``
     - ``256`` 、 ``512`` 或 ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - 最多96个，每个文本最多2048个字符
   * - ``cohere.embed-v4:0`` （也可通过推理配置文件使用）
     - ``256`` 、 ``512`` 、 ``1024`` 或 ``1536``
     - 最多96个

嵌入模型根据所配置ID中包含的基础模型名称进行识别: 基础模型ID、跨区域推理配置文件ID（ ``us.`` 、 ``eu.`` 、 ``global.`` 等）或包含上述ID之一的ARN。
应用程序推理配置文件的ID是不透明的，因此无法识别。

.. note::
   各区域可用的模型请参阅 `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__ 。

前提条件
========

1. **AWS账户**: 在您使用的区域中可使用 Amazon Bedrock
2. **模型访问权限**: 所配置的模型必须能在该区域中通过您的账户使用
3. **凭据**: Bedrock API密钥，或被允许调用这些模型的 AWS 凭据（参见 :ref:`bedrock-authentication` ）

插件安装
========

Bedrock集成功能以 ``fess-llm-bedrock`` 插件的形式提供。
请在管理界面的"系统" > "插件"中安装，或手动放置JAR文件并重启 |Fess| 。

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   插件版本请与 |Fess| 版本保持一致。

基本配置
========

LLM提供商（ ``rag.llm.name`` ）可在管理界面（管理界面 > 系统 > 通用）中选择，或在 ``system.properties`` 中设置。
AI搜索模式的启用及 ``rag.llm.bedrock.*`` 配置在 ``fess_config.properties`` 中进行。

``system.properties`` （也可在管理界面 > 系统 > 通用中配置）:

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties`` （软件包安装时为 ``/etc/fess/fess_config.properties`` ），使用AWS凭据:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

使用Bedrock API密钥代替AWS凭据:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

配置项
======

AI搜索模式客户端的所有配置项。它们在 ``fess_config.properties`` 中配置（也可作为 ``-Dfess.config.<key>`` JVM选项指定）。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.bedrock.api.key``
     - Bedrock API密钥。为空时，使用AWS凭据对请求进行签名（SigV4）
     - ``""``
   * - ``rag.llm.bedrock.region``
     - Bedrock Runtime 端点及SigV4签名所用的AWS区域
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - 端点URL，例如VPC接口端点。为空时为 ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - 模型ID、推理配置文件ID或ARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - 请求超时时间（毫秒）
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - 可用性检查间隔（秒）
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - 设为 ``false`` 时不再发送 ``temperature`` ，适用于拒绝该参数的模型或模式
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - 作为 ``additionalModelRequestFields`` 发送的JSON对象，用于设置模型专属参数
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - 最大并发请求数
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - 并发请求等待超时（毫秒）
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - 生成回答时检索上下文的最大字符数
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - 生成摘要时文档的最大字符数
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - 生成FAQ时检索上下文的最大字符数
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - 评估时的最大相关文档数
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - 评估时文档描述的最大字符数
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - 聊天历史的最大字符数
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - 意图判定时的历史最大消息数
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - 意图判定时的历史最大字符数
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - 助手历史的最大字符数
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - 助手摘要历史的最大字符数
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - HTTP重试的最大尝试次数（ ``429`` 、 ``500`` 、 ``502`` 、 ``503`` 及 ``504`` 时）
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - 指数退避的基准延迟时间（毫秒）
     - ``2000``

.. _bedrock-authentication:

认证方式
========

API密钥
-------

设置 ``rag.llm.bedrock.api.key`` 后，它会以 ``Authorization: Bearer <key>`` 的形式发送。
短期 Bedrock API 密钥会过期，且仅在其创建所在的区域有效；长期密钥则与 IAM 用户绑定。
当该值设置在 ``fess_config.properties`` 中（对于 ``content_chunker.embedding.bedrock.api.key`` 则是设置在 ``system.properties`` 中）时，会在管理界面 > 系统 > 系统信息中被掩码显示。
环境变量和JVM系统属性（包括 ``-Dfess.config.*`` 和 ``-Dfess.system.*`` 选项）会在该页面中不加掩码地列出，因此请勿以这种方式传递密钥。

AWS凭据（SigV4）
----------------

未设置API密钥时，每个请求都使用 AWS Signature Version 4 进行签名。
凭据按以下顺序，取自第一个能提供凭据的来源:

1. ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken`` JVM系统属性
2. ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN`` 环境变量
3. Web身份（ ``AWS_WEB_IDENTITY_TOKEN_FILE`` 和 ``AWS_ROLE_ARN`` ，用于 Amazon EKS）
4. 共享的 ``~/.aws/credentials`` 和 ``~/.aws/config`` 文件（由 ``AWS_PROFILE`` 选择配置文件）
5. 容器凭据端点（Amazon ECS）
6. EC2实例元数据服务（实例配置文件）

JVM系统属性（第1项）只会传递给 |Fess| 的Web进程。
内容分块（文档）的嵌入在单独的子JVM中运行，因此对它请使用环境变量、共享的凭据配置文件或IAM角色，或者在 ``jvm.chunk.options`` 中重复指定 ``-Daws.*`` 选项。

区域始终取自 ``rag.llm.bedrock.region`` ，不会读取 ``AWS_REGION`` 。
不支持使用 IAM Identity Center（SSO）的配置文件。

.. warning::
   建议使用IAM角色（EC2实例配置文件、ECS任务角色、EKS Web身份），或运行 |Fess| 的用户的共享凭据文件。
   环境变量和JVM系统属性会不加掩码地列在管理界面 > 系统 > 系统信息下，因此请勿在其中放置长期有效的密钥。

IAM主体需要对其所用模型拥有 ``bedrock:InvokeModel`` （Converse 和 InvokeModel）以及 ``bedrock:InvokeModelWithResponseStream`` （ConverseStream）权限。
当模型是推理配置文件时，需同时允许该推理配置文件及其路由到的基础模型。

重试行为
========

遇到 ``429`` 、 ``500`` 、 ``502`` 、 ``503`` 和 ``504`` ，以及无法建立到 Bedrock 的连接时，请求会被重试。
重试时采用指数退避进行等待（基准值 ``rag.llm.bedrock.retry.base.delay.ms`` 、±20%抖动、最多 ``rag.llm.bedrock.retry.max`` 次尝试）； ``Retry-After`` 头优先。
对于流式请求，仅初次请求会被重试；回答开始流式传输之后发生的错误（包括流内的异常事件）会终止该请求。

提示词类型别配置
================

与其他提供商一样， ``temperature`` 和 ``max.tokens`` 可按提示词类型设置:

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` 为 ``intent`` 、 ``evaluation`` 、 ``unclear`` 、 ``noresults`` 、 ``docnotfound`` 、 ``direct`` 、 ``faq`` 、 ``answer`` 、 ``summary`` 和 ``queryregeneration`` 之一。
按提示词类型设置的 ``additional.model.request.fields`` 会替换该提示词类型的全局值。

未配置时使用的默认值:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - 提示词类型
     - temperature
     - max.tokens
   * - ``intent`` 、 ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear`` 、 ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct`` 、 ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   不支持 ``rag.llm.bedrock.{promptType}.thinking.budget`` : 在 Bedrock 上，推理设置因模型而异。
   已配置的值不会被发送，并会记录一条 WARN 日志。请改用 ``additional.model.request.fields`` 。

模型专属参数
============

``additional.model.request.fields`` 会将一个JSON对象原样传递给模型。
不是JSON对象的值不会被发送，并会记录一条指明该属性的 WARN 日志。

例如，仅在生成回答时使用 Anthropic Claude 模型的扩展思考:

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

启用思考时 Claude 会拒绝 ``temperature`` ，并且 ``max.tokens`` 必须大于 ``budget_tokens`` 。
推理文本绝不会显示给用户，仅显示回答文本。

内容分块嵌入
============

要将Bedrock用于内容分块嵌入，请在 ``app/WEB-INF/conf/system.properties`` （RPM/DEB 软件包为 ``/etc/fess/system.properties`` ，Docker 为 ``/opt/fess/system.properties`` ）中进行以下设置，或将其作为 ``-Dfess.system.<key>`` 选项指定。
与 ``rag.llm.bedrock.*`` 不同，这些键不会从 ``fess_config.properties`` 中读取。

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``content_chunker.embedding.bedrock.api.key``
     - Bedrock API密钥。为空时使用AWS凭据
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - AWS区域
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - 端点URL。为空时根据区域推导
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - 嵌入模型（参见 `支持的模型`_ ）
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - 仅限 Titan: 是否对向量进行归一化
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - 仅限 Cohere: ``truncate`` （v3 为 ``NONE`` / ``START`` / ``END`` ，v4 为 ``NONE`` / ``LEFT`` / ``RIGHT`` ）。为空时不发送
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - 请求超时时间（毫秒）
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - 连接超时时间（毫秒）
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - 可用性检查间隔（秒）
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - HTTP重试的最大尝试次数（ ``429`` 、 ``500`` 、 ``502`` 、 ``503`` 及 ``504`` 时）
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - 指数退避的基准延迟时间（毫秒）
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - 单次退避等待的上限，包含 ``Retry-After`` （毫秒）
     - ``60000``

``content_chunker.embedding.dimension`` 必须是模型能够生成的大小（参见 `支持的模型`_ ）；否则嵌入提供商会被报告为不可用，并记录 ERROR 日志。
文档使用 Cohere 的 ``input_type=search_document`` 进行嵌入，查询使用 ``search_query`` 。
Cohere Embed v3 每个文本最多接受2048个字符。无论 ``truncate`` 如何设置，Bedrock 都会以 ``400 ValidationException`` 拒绝更长的文本，且插件不会缩短或拆分文本。
``truncate`` （未设置时为 ``END`` ）仅适用于不超过2048个字符但超过512个token的文本。

通过 HTTP 代理使用
==================

对 Bedrock 的请求使用 |Fess| 整体的HTTP代理配置（ ``fess_config.properties`` 中的 ``http.proxy.host`` 、 ``http.proxy.port`` 、 ``http.proxy.username`` 和 ``http.proxy.password`` ）。
调用AWS端点的凭据查询（用于Web身份的STS、容器凭据端点、实例元数据服务）不使用这些设置。
要通过VPC接口端点访问 Bedrock，请将 ``rag.llm.bedrock.endpoint`` （以及 ``content_chunker.embedding.bedrock.endpoint`` ）设置为其URL；区域设置仍用于选择签名区域。

故障排除
========

AI搜索模式不可用
----------------

当模型和区域已设置、端点是有效的URL，且已设置API密钥或能够解析出AWS凭据时，客户端会报告自身可用。
无效的区域或端点会以 ERROR 级别记录。要查看无法解析凭据的原因，请对 ``org.codelibs.fess.llm.bedrock`` 启用 DEBUG。
凭据查询失败的结果会被记住60秒，因此之后才可用的凭据会在一分钟内被获取。

访问被拒绝
----------

WARN 日志中出现带有 ``type=AccessDeniedException`` 的 ``403`` ，表示该API密钥或 IAM 主体无权调用该模型。
请检查上述IAM权限，并确认该模型可在所配置的区域中通过您的账户使用。

验证错误
--------

带有 ``type=ValidationException`` 的 ``400`` 通常意味着该模型ID在此区域不可用（某些模型只能使用推理配置文件ID），或者 ``additional.model.request.fields`` 中包含模型不接受的参数。

调试设置
--------

对 ``org.codelibs.fess.llm.bedrock`` 启用 DEBUG，可记录AI搜索模式的请求和响应主体，以及无法解析AWS凭据的原因。
对 ``org.codelibs.fess.embedding.bedrock`` 启用 DEBUG，可记录查询文本的规范化方式以及同样的凭据原因；它不会记录嵌入请求。
这些日志记录器绝不会写入API密钥、AWS凭据和签名。

.. warning::
   另有两个日志记录器在 DEBUG 级别会写入凭据: Apache HttpClient 的 wire 日志会写入 ``Authorization`` 头，而 AWS SDK 的签名器（ ``software.amazon.awssdk.http.auth.aws.internal.signer`` ）会写入规范请求，其中包含临时凭据的 ``x-amz-security-token`` 。
   以根日志级别 DEBUG 启动 |Fess| 会同时启用这两者；请将 ``org.apache.hc`` 和 ``software.amazon.awssdk`` 保持在 INFO 或更高级别。

参考信息
========

- :doc:`llm-overview` - LLM集成概述
- :doc:`rag-chat` - AI搜索模式功能详情
- :doc:`search-semantic` - 语义搜索与内容分块嵌入
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
