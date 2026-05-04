==========================
OpenAI配置
==========================

概述
====

OpenAI是提供GPT-4等高性能大型语言模型（LLM）的云服务。
|Fess| 可以使用OpenAI API实现AI搜索模式功能。

使用OpenAI，可以通过最先进的AI模型生成高质量的回答。

主要特点
--------

- **高质量回答**: 最先进的GPT模型提供高精度回答生成
- **可扩展性**: 云服务易于扩展
- **持续改进**: 模型定期更新提升性能
- **丰富功能**: 支持文本生成、摘要、翻译等多种任务

支持的模型
----------

OpenAI可用的主要模型:

- ``gpt-5`` - 最新高性能模型
- ``gpt-5-mini`` - GPT-5的轻量版（成本效益高）
- ``gpt-4o`` - 高性能多模态模型
- ``gpt-4o-mini`` - GPT-4o的轻量版
- ``o3-mini`` - 推理特化的轻量模型
- ``o4-mini`` - 下一代推理特化轻量模型

.. note::
   可用模型的最新信息请查阅 `OpenAI Models <https://platform.openai.com/docs/models>`__

.. note::
   使用o1/o3/o4系列或gpt-5系列模型时，|Fess| 会自动使用OpenAI API的 ``max_completion_tokens`` 参数。无需更改配置。

前提条件
========

使用OpenAI前，请准备以下内容。

1. **OpenAI账户**: 在 `https://platform.openai.com/ <https://platform.openai.com/>`__ 创建账户
2. **API密钥**: 在OpenAI仪表板生成API密钥
3. **计费设置**: API使用会产生费用，需设置计费信息

获取API密钥
-----------

1. 登录 `OpenAI Platform <https://platform.openai.com/>`__
2. 转到"API keys"部分
3. 点击"Create new secret key"
4. 输入密钥名称并创建
5. 安全保存显示的密钥（只显示一次）

.. warning::
   API密钥是机密信息。请注意以下几点:

   - 不要提交到版本管理系统
   - 不要在日志中输出
   - 使用环境变量或安全配置文件管理

插件安装
========================

|Fess| 15.6中，OpenAI集成功能以插件形式提供。使用前需要安装 ``fess-llm-openai`` 插件。

1. 下载 `fess-llm-openai-15.6.0.jar`
2. 将JAR文件放置到 |Fess| 安装目录下的 ``app/WEB-INF/plugin/`` 目录::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. 重启 |Fess|

.. note::
   插件版本请与 |Fess| 本体版本保持一致。

基本配置
========

|Fess| 15.6中，配置项根据用途分别存放在以下两个文件中。

- ``app/WEB-INF/conf/fess_config.properties`` - |Fess| 本体配置及LLM提供商专属配置
- ``system.properties`` - 在管理界面（管理界面 > 系统 > 通用）或文件中配置LLM提供商名称（ ``rag.llm.name`` ）

最小配置
--------

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # OpenAI API密钥
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用的模型
    rag.llm.openai.model=gpt-5-mini

``system.properties``（也可在管理界面 > 系统 > 通用中配置）:

::

    # 将LLM提供商设置为OpenAI
    rag.llm.name=openai

推荐配置（生产环境）
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # OpenAI API密钥
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 模型设置（使用高性能模型）
    rag.llm.openai.model=gpt-4o

    # API端点（通常无需更改）
    rag.llm.openai.api.url=https://api.openai.com/v1

    # 超时设置
    rag.llm.openai.timeout=120000

    # 并发请求数限制
    rag.llm.openai.max.concurrent.requests=5

``system.properties``（也可在管理界面 > 系统 > 通用中配置）:

::

    # LLM提供商设置
    rag.llm.name=openai

配置项
======

OpenAI客户端可用的所有配置项。 ``rag.llm.name`` 在 ``system.properties`` 或管理界面中进行设置，其他配置均在 ``fess_config.properties`` 中进行。

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - 属性
     - 说明
     - 默认值
     - 配置位置
   * - ``rag.llm.name``
     - LLM提供商名称（指定 ``openai``）
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - OpenAI API密钥
     - （必需）
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - 使用的模型名称
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - API的基础URL
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - 请求超时时间（毫秒）
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - 可用性检查间隔（秒）
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - 最大并发请求数
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - 评估时的最大相关文档数
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - 并发请求等待超时（毫秒）
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - 推理模型的max_tokens倍率
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - HTTP重试的最大尝试次数（``429`` 及 ``5xx`` 系错误时）
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - 指数退避的基准延迟时间（毫秒）
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - 流式输出时发送 ``stream_options.include_usage=true``，在最终分块中接收使用token信息
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - 会话历史的最大字符数
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - 意图判定时的最大历史消息数
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - 意图判定时的最大历史字符数
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - 助手消息的最大字符数
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - 助手摘要的最大字符数
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - 评估时文档描述的最大字符数
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - 启用AI搜索模式功能
     - ``false``
     - fess_config.properties

提示词类型别配置
======================

|Fess| 中可以按提示词类型分别设置参数。配置在 ``fess_config.properties`` 中进行。

配置模式
------------

按提示词类型的配置以如下模式指定:

- ``rag.llm.openai.{promptType}.temperature`` - 生成随机性（0.0〜2.0）。推理模型（o1/o3/o4/gpt-5系列）会忽略此设置
- ``rag.llm.openai.{promptType}.max.tokens`` - 最大token数
- ``rag.llm.openai.{promptType}.context.max.chars`` - 上下文最大字符数（默认值: answer/summary为 ``16000``，其他为 ``10000``）

提示词类型
----------------

可用的提示词类型:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 提示词类型
     - 说明
   * - ``intent``
     - 判定用户意图的提示词
   * - ``evaluation``
     - 评估搜索结果相关性的提示词
   * - ``unclear``
     - 针对不明确查询的响应提示词
   * - ``noresults``
     - 无搜索结果时的响应提示词
   * - ``docnotfound``
     - 文档未找到时的响应提示词
   * - ``answer``
     - 生成回答的提示词
   * - ``summary``
     - 生成摘要的提示词
   * - ``faq``
     - 生成FAQ的提示词
   * - ``direct``
     - 直接响应的提示词
   * - ``queryregeneration``
     - 搜索查询再生成的提示词

默认值
------

各提示词类型的默认值如下。推理模型（o1/o3/o4/gpt-5系列）会忽略temperature设置。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 提示词类型
     - Temperature
     - Max Tokens
     - 备注
   * - ``intent``
     - 0.1
     - 256
     - 确定性意图判定
   * - ``evaluation``
     - 0.1
     - 256
     - 确定性相关性评估
   * - ``unclear``
     - 0.7
     - 512
     -
   * - ``noresults``
     - 0.7
     - 512
     -
   * - ``docnotfound``
     - 0.7
     - 256
     -
   * - ``direct``
     - 0.7
     - 1024
     -
   * - ``faq``
     - 0.7
     - 1024
     -
   * - ``answer``
     - 0.5
     - 2048
     - 主要回答生成
   * - ``summary``
     - 0.3
     - 2048
     - 摘要生成
   * - ``queryregeneration``
     - 0.3
     - 256
     - 查询再生成

配置示例
------

::

    # answer提示词的temperature设置
    rag.llm.openai.answer.temperature=0.7

    # answer提示词的最大token数
    rag.llm.openai.answer.max.tokens=2048

    # summary提示词的temperature设置（摘要设置较低）
    rag.llm.openai.summary.temperature=0.3

    # intent提示词的temperature设置（意图判定设置较低）
    rag.llm.openai.intent.temperature=0.1

重试行为
========

对OpenAI API的请求会针对以下HTTP状态码自动重试:

- ``429`` Too Many Requests（速率限制）
- ``500`` Internal Server Error
- ``502`` Bad Gateway（OpenAI在上游过载时可能返回）
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

重试时采用指数退避（基准值 ``rag.llm.openai.retry.base.delay.ms`` 毫秒、最多 ``rag.llm.openai.retry.max`` 次、带±20%抖动）进行等待。
当服务器返回 ``Retry-After`` 头（整数秒，最大限制为 ``600`` 秒）时，该值优先于指数退避使用。这遵循OpenAI官方指南。

需要注意， ``IOException`` （连接超时、套接字重置、DNS失败）不会被重试。因为请求可能已到达服务器，重试可能导致重复计费。
对于流式请求，仅初次连接是重试对象，响应主体接收开始后发生的错误会立即向上传播。

.. note::
   在默认配置（最多10次、基准2秒）的最坏情况下，9次重试的退避总和为 ``2 + 4 + 8 + ... + 512 ≈ 1022秒（约17分钟）``。在每次都返回 ``Retry-After`` （最大600秒）的场景下，最坏情况会膨胀到 ``9 × 600秒 = 90分钟``。如需更严格地控制延迟，请将 ``rag.llm.openai.retry.max`` 设置得小一些。

流式输出和使用量信息
====================

默认情况下，请求中会附加 ``stream_options.include_usage=true``，在流式响应的最终SSE分块中接收 ``usage`` 对象（推理模型时包含 ``completion_tokens_details.reasoning_tokens``，使用提示词缓存时包含 ``prompt_tokens_details.cached_tokens``）。

对于vLLM或Azure OpenAI兼容网关等不接受 ``stream_options.include_usage`` 字段的后端，请按如下方式禁用::

    rag.llm.openai.stream.include.usage=false

日志输出和异常检测
==================

自 |Fess| 15.6.1 起，OpenAI客户端输出以下结构化日志。借此即使不启用 ``DEBUG`` 级别，也可监控token使用情况和响应异常。

- ``[LLM:OPENAI] Stream completed.`` （INFO） - 流式响应完成时输出分块数、首个分块的耗时、token使用信息等
- ``[LLM:OPENAI] Chat response received.`` （INFO） - 非流式响应完成时输出同等信息
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` （WARN） - 当 ``finish_reason`` 不是 ``stop`` 时输出（``length``：因max_tokens被截断、 ``content_filter``：内容审核、 ``tool_calls`` / ``function_call``：意外的工具调用配置等）
- ``[LLM:OPENAI] Stream refusal.`` （WARN） - 在结构化输出中返回 ``delta.refusal`` 时输出

这些WARN日志可用于调整 ``max_tokens``、审计内容过滤器以及检测 ``extra_params`` 的误配置。

URL日志中的认证信息屏蔽
-----------------------

输出到日志的URL中，包含认证信息的查询参数（ ``api_key`` 、 ``apikey`` 、 ``api-key`` 、 ``key`` 、 ``token`` 、 ``access_token`` 、 ``access-token``，不区分大小写）会自动用 ``***`` 进行屏蔽。

OpenAI官方端点（ ``https://api.openai.com`` ）通过 ``Authorization: Bearer`` 头进行认证，URL中不包含认证信息。但当将以查询参数接受认证信息的自定义代理（部分Azure部署、vLLM网关等）设置到 ``rag.llm.openai.api.url`` 时，该机制也能防止API密钥泄露到日志中。

推理模型支持
==============

使用o1/o3/o4系列或gpt-5系列推理模型时，|Fess| 会自动使用OpenAI API的 ``max_completion_tokens`` 参数代替 ``max_tokens``。无需额外更改配置。

.. note::
   推理模型（o1/o3/o4/gpt-5系列）会忽略 ``temperature`` 设置，使用固定值（1）。此外，使用推理模型时，默认的 ``max_tokens`` 会乘以 ``reasoning.token.multiplier``（默认值: 4）。

推理模型的附加参数
----------------------------

使用推理模型时，可在 ``fess_config.properties`` 中设置以下附加参数:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - o系列模型的推理effort设置（``low``、``medium``、``high``）
     - ``low``（intent/evaluation/docnotfound/unclear/noresults/queryregeneration），未设置（其他）
   * - ``rag.llm.openai.{promptType}.top.p``
     - token选择的概率阈值（0.0〜1.0）
     - （未设置）
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - 频率惩罚（-2.0〜2.0）
     - （未设置）
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - 存在惩罚（-2.0〜2.0）
     - （未设置）

``{promptType}`` 可以是 ``intent``、``evaluation``、``answer``、``summary`` 等提示词类型。

配置示例
------

::

    # 对o3-mini将推理effort设置为high
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # 对gpt-5设置top_p和惩罚
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

通过 JVM 选项配置
=================

出于安全考虑，建议通过运行时环境（JVM 选项）而非签入文件来配置 API 密钥。

Docker环境
----------

官方 `docker-fess <https://github.com/codelibs/docker-fess>`__ 仓库附带了 OpenAI 用的
overlay 文件 ``compose-openai.yaml``。最小步骤：

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` 的内容（自行编写等价配置时的参考）：

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

要点：

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` 让容器的 ``run.sh`` 自动下载并安装插件到 ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` 启用 AI 搜索模式
- ``-Dfess.config.rag.llm.openai.api.key=...`` 设置 API 密钥，``-Dfess.config.rag.llm.openai.model=...`` 选择模型
- ``-Dfess.system.rag.llm.name=openai`` 仅在 OpenSearch 尚未保存值的首次启动时作为默认值生效。启动后也可在管理界面"系统 > 全局设置"的 RAG 区段进行修改

如果通过代理访问互联网，请通过 ``FESS_JAVA_OPTS`` 指定 |Fess| 的 ``http.proxy.*`` 配置（参见后述"通过 HTTP 代理使用"一节）。

systemd环境
-----------

在 ``/etc/sysconfig/fess`` （或 ``/etc/default/fess`` ）的 ``FESS_JAVA_OPTS`` 中追加：

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

通过 HTTP 代理使用
==================

自 |Fess| 15.6.1 起，OpenAI客户端会共享 |Fess| 整体的HTTP代理配置。请在 ``fess_config.properties`` 中指定以下属性。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``http.proxy.host``
     - 代理主机名（空字符串时不使用代理）
     - ``""``
   * - ``http.proxy.port``
     - 代理端口号
     - ``8080``
   * - ``http.proxy.username``
     - 代理认证的用户名（可选。指定后启用Basic认证）
     - ``""``
   * - ``http.proxy.password``
     - 代理认证的密码
     - ``""``

在Docker环境中，按如下方式在 ``FESS_JAVA_OPTS`` 中指定::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   此配置同样会影响爬虫等 |Fess| 整体的HTTP访问。
   传统的Java系统属性（ ``-Dhttps.proxyHost`` 等）不会被OpenAI客户端引用。

使用Azure OpenAI
==================

通过Microsoft Azure使用OpenAI模型时，需更改API端点。

::

    # Azure OpenAI端点
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Azure API密钥
    rag.llm.openai.api.key=your-azure-api-key

    # 部署名称（作为模型名称指定）
    rag.llm.openai.model=your-deployment-name

.. note::
   使用Azure OpenAI时，API请求格式可能略有不同。
   详情请参阅Azure OpenAI文档。

模型选择指南
============

根据使用目的的模型选择指南。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 模型
     - 成本
     - 质量
     - 用途
   * - ``gpt-5-mini``
     - 中
     - 高
     - 均衡用途（推荐）
   * - ``gpt-4o-mini``
     - 低〜中
     - 高
     - 成本优先的用途
   * - ``gpt-5``
     - 高
     - 最高
     - 复杂推理、需要高质量
   * - ``gpt-4o``
     - 中〜高
     - 最高
     - 需要多模态支持
   * - ``o3-mini`` / ``o4-mini``
     - 中
     - 最高
     - 数学、编程等推理任务

成本估算
------------

OpenAI API按使用量计费。

.. note::
   最新价格请查阅 `OpenAI Pricing <https://openai.com/pricing>`__

并发请求控制
==================

|Fess| 中可通过 ``fess_config.properties`` 的 ``rag.llm.openai.max.concurrent.requests`` 控制对OpenAI API的并发请求数。默认值为 ``5``。

::

    # 设置最大并发请求数
    rag.llm.openai.max.concurrent.requests=5

通过此设置，可防止向OpenAI API发送过多请求，避免速率限制错误。

OpenAI Tier限制
------------------

OpenAI API端的限制因账户Tier而异:

- **Free**: 3 RPM（请求/分钟）
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: 更高限制

请根据OpenAI账户Tier适当调整 ``rag.llm.openai.max.concurrent.requests``。

故障排除
======================

认证错误
----------

**症状**: 发生"401 Unauthorized"错误

**检查事项**:

1. 确认API密钥配置正确
2. 确认API密钥有效（在OpenAI仪表板确认）
3. 确认API密钥具有所需权限

速率限制错误
------------

**症状**: 发生"429 Too Many Requests"错误

**解决方法**:

1. 减小 ``rag.llm.openai.max.concurrent.requests`` 的值::

    rag.llm.openai.max.concurrent.requests=3

2. 升级OpenAI账户Tier

配额超限
--------

**症状**: "You exceeded your current quota"错误

**解决方法**:

1. 在OpenAI仪表板确认使用量
2. 检查计费设置，必要时提高上限

超时
----

**症状**: 请求超时

**解决方法**:

1. 延长超时时间::

    rag.llm.openai.timeout=180000

2. 考虑使用更快的模型（如gpt-5-mini等）

调试设置
------------

调查问题时，可调整 |Fess| 日志级别输出OpenAI相关的详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

安全注意事项
========================

使用OpenAI API时，请注意以下安全事项。

1. **数据隐私**: 搜索结果内容会发送到OpenAI服务器
2. **API密钥管理**: 密钥泄露会导致未授权使用
3. **合规性**: 包含机密数据时，请确认组织政策
4. **使用政策**: 遵守OpenAI使用条款

参考信息
========

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - LLM集成概述
- :doc:`rag-chat` - AI搜索模式功能详情
