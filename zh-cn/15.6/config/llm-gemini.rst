==========================
Google Gemini配置
==========================

概述
====

Google Gemini是Google公司提供的最先进的大型语言模型（LLM）。
|Fess| 可以使用Google AI API（Generative Language API）通过Gemini模型实现AI搜索模式功能。

使用Gemini，可以利用Google最新的AI技术生成高质量的回答。

主要特点
--------

- **多模态支持**: 不仅可处理文本，还可处理图像
- **长上下文**: 可一次处理大量文档的长上下文窗口
- **成本效益**: Flash模型快速且低成本
- **Google集成**: 易于与Google Cloud服务集成

支持的模型
----------

Gemini可用的主要模型:

- ``gemini-3.1-flash-lite-preview`` - 轻量、低成本的高速模型（默认）
- ``gemini-3-flash-preview`` - 标准的Flash模型
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - 高推理模型
- ``gemini-2.5-flash`` - 稳定版高速模型
- ``gemini-2.5-pro`` - 稳定版高推理模型

.. note::
   可用模型的最新信息请查阅 `Google AI for Developers <https://ai.google.dev/models/gemini>`__

前提条件
========

使用Gemini前，请准备以下内容。

1. **Google账户**: 需要Google账户
2. **Google AI Studio访问**: 访问 `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **API密钥**: 在Google AI Studio生成API密钥

获取API密钥
-----------

1. 访问 `Google AI Studio <https://aistudio.google.com/>`__
2. 点击"Get API key"
3. 选择"Create API key"
4. 选择或新建项目
5. 安全保存生成的API密钥

.. warning::
   API密钥是机密信息。请注意以下几点:

   - 不要提交到版本管理系统
   - 不要在日志中输出
   - 使用环境变量或安全配置文件管理

插件安装
========================

|Fess| 15.6中，Gemini集成功能以 ``fess-llm-gemini`` 插件的形式提供。
使用Gemini需要安装插件。

1. 下载 `fess-llm-gemini-15.6.0.jar`
2. 将其放置到 |Fess| 的 ``app/WEB-INF/plugin/`` 目录
3. 重启 |Fess|

::

    # 插件放置示例
    cp fess-llm-gemini-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   插件版本请与 |Fess| 版本保持一致。

基本配置
========

|Fess| 15.6中，AI搜索模式功能的启用及Gemini专属配置在 ``fess_config.properties`` 中进行，LLM提供商名称（ ``rag.llm.name`` ）的选择在管理界面或 ``system.properties`` 中进行。

fess_config.properties配置
----------------------------

在 ``app/WEB-INF/conf/fess_config.properties`` 中添加AI搜索模式功能的启用配置。

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

LLM提供商配置
---------------------

LLM提供商名称（ ``rag.llm.name`` ）可在管理界面（管理界面 > 系统 > 通用）中配置，或在 ``system.properties`` 中设置。Gemini专属配置在 ``fess_config.properties`` 中进行。

最小配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # Gemini API密钥
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用的模型
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

``system.properties``（也可在管理界面 > 系统 > 通用中配置）:

::

    # 将LLM提供商设置为Gemini
    rag.llm.name=gemini

推荐配置（生产环境）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # Gemini API密钥
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 模型设置（使用高速模型）
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

    # API端点（通常无需更改）
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # 超时设置
    rag.llm.gemini.timeout=60000

``system.properties``（也可在管理界面 > 系统 > 通用中配置）:

::

    # 将LLM提供商设置为Gemini
    rag.llm.name=gemini

配置项
======

Gemini客户端可用的所有配置项。 ``rag.llm.name`` 在 ``system.properties`` 或管理界面中进行设置，其他配置均在 ``fess_config.properties`` 中进行。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.gemini.api.key``
     - Google AI API密钥（使用Gemini API需要设置）
     - ``""``
   * - ``rag.llm.gemini.model``
     - 使用的模型名称
     - ``gemini-3.1-flash-lite-preview``
   * - ``rag.llm.gemini.api.url``
     - API的基础URL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - 请求超时时间（毫秒）
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - 可用性检查间隔（秒）
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - 最大并发请求数
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - 评估时的最大相关文档数
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - 评估时文档描述的最大字符数
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - 并发请求等待超时（毫秒）
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - 聊天历史的最大字符数
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - 意图判定时的历史最大消息数
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - 意图判定时的历史最大字符数
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - 助手历史的最大字符数
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - 助手摘要历史的最大字符数
     - ``1000``
   * - ``rag.llm.gemini.retry.max``
     - HTTP重试的最大尝试次数（``429`` 及 ``5xx`` 系错误时）
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - 指数退避的基准延迟时间（毫秒）
     - ``2000``

认证方式
========

自 |Fess| 15.6.1 起，API密钥通过 ``x-goog-api-key`` HTTP请求头发送（Google推荐方式）。
不再像以往那样以 ``?key=...`` 查询参数附加到URL，因此API密钥不会残留在访问日志中。

重试行为
========

对Gemini API的请求会针对以下HTTP状态码自动重试:

- ``429`` Resource Exhausted（配额超限、速率限制）
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

重试时采用指数退避（基准值 ``rag.llm.gemini.retry.base.delay.ms`` 毫秒、最多 ``rag.llm.gemini.retry.max`` 次、带±20%抖动）进行等待。
对于流式请求，仅初次连接是重试对象，响应主体接收开始后发生的错误会立即向上传播。

提示词类型别配置
======================

|Fess| 中可以按提示词类型精细设置LLM参数。
按提示词类型的配置在 ``fess_config.properties`` 中记述。

配置格式
----------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

可用的提示词类型
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 提示词类型
     - 说明
   * - ``intent``
     - 判定用户意图的提示词
   * - ``evaluation``
     - 评估文档相关性的提示词
   * - ``unclear``
     - 问题不明确时的提示词
   * - ``noresults``
     - 无搜索结果时的提示词
   * - ``docnotfound``
     - 文档未找到时的提示词
   * - ``answer``
     - 生成回答的提示词
   * - ``summary``
     - 生成摘要的提示词
   * - ``faq``
     - 生成FAQ的提示词
   * - ``direct``
     - 直接响应的提示词
   * - ``queryregeneration``
     - 查询再生成的提示词

提示词类型别默认值
------------------------------

各提示词类型的默认值如下。未设置时将使用这些值。

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - 提示词类型
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``512``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - ``0``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``0``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

配置示例
------

::

    # 生成回答的temperature设置
    rag.llm.gemini.answer.temperature=0.7

    # 生成摘要的最大token数
    rag.llm.gemini.summary.max.tokens=2048

    # 生成回答的上下文最大字符数
    rag.llm.gemini.answer.context.max.chars=16000

    # 生成摘要的上下文最大字符数
    rag.llm.gemini.summary.context.max.chars=16000

    # 生成FAQ的上下文最大字符数
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   ``context.max.chars`` 的默认值因提示词类型而异。
   ``answer`` 和 ``summary`` 为16000，``faq`` 为10000，其他提示词类型为10000。

思考模型支持
==============

Gemini支持思考模型（Thinking Model）。
使用思考模型时，模型在生成回答前会执行内部推理过程，从而生成精度更高的回答。

可按提示词类型在 ``fess_config.properties`` 中设置思考预算。 |Fess| 在请求时会将 ``rag.llm.gemini.{promptType}.thinking.budget`` 的整数值（token数）根据解析出的模型世代自动转换为相应的API字段。

::

    # 回答生成时的思考预算设置
    rag.llm.gemini.answer.thinking.budget=1024

    # 摘要生成时的思考预算设置
    rag.llm.gemini.summary.thinking.budget=1024

按模型世代的映射
----------------

- **Gemini 2.x** （例如 ``gemini-2.5-flash`` ）: 将设置的整数值原样作为 ``thinkingConfig.thinkingBudget`` 发送。指定 ``0`` 时完全禁用思考。
- **Gemini 3.x** （例如 ``gemini-3.1-flash-lite-preview`` ）: 将整数值分桶为 ``thinkingConfig.thinkingLevel`` 的枚举值（ ``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH`` ）后发送。

Gemini 3.x 的分桶映射如下:

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - 预算值
     - thinkingLevel
     - 备注
   * - ``<=0``
     - ``MINIMAL`` 或 ``LOW``
     - 在Flash / Flash-Lite模型上为 ``MINIMAL``，在不支持 ``MINIMAL`` 的Pro系模型（ ``gemini-3-pro`` / ``gemini-3.1-pro`` ）上为 ``LOW``
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x在任何分桶下都必定会消耗一定的思考token（即便 ``thinkingLevel=MINIMAL`` 也可能消耗数百token）。
   因此 |Fess| 在使用Gemini 3.x模型时会自动为默认的 ``maxOutputTokens`` 加上额外的余量（1024 token），以防止因 ``finishReason=MAX_TOKENS`` 导致回答被截断。
   Gemini 2.x通过 ``thinkingBudget=0`` 即可禁用思考本身，因此不会追加余量。

.. note::
   将思考预算设置得较大时，响应时间可能会变长。
   请根据用途设置适当的值。

通过 JVM 选项配置
=================

出于安全考虑，建议通过运行时环境（JVM 选项）而非签入文件来配置 API 密钥。

Docker环境
----------

官方 `docker-fess <https://github.com/codelibs/docker-fess>`__ 仓库附带了 Gemini 用的
overlay 文件 ``compose-gemini.yaml``。最小步骤：

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

``compose-gemini.yaml`` 的内容（自行编写等价配置时的参考）：

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

要点：

- ``FESS_PLUGINS=fess-llm-gemini:15.6.0`` 让容器的 ``run.sh`` 自动下载并安装插件到 ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` 启用 AI 搜索模式
- ``-Dfess.config.rag.llm.gemini.api.key=...`` 设置 API 密钥，``-Dfess.config.rag.llm.gemini.model=...`` 选择模型
- ``-Dfess.system.rag.llm.name=gemini`` 仅在 OpenSearch 尚未保存值的首次启动时作为默认值生效。启动后也可在管理界面"系统 > 全局设置"的 RAG 区段进行修改

如果通过代理访问互联网，请通过 ``FESS_JAVA_OPTS`` 指定 |Fess| 的 ``http.proxy.*`` 配置（参见后述"通过 HTTP 代理使用"一节）。

systemd环境
-----------

在 ``/etc/sysconfig/fess`` （或 ``/etc/default/fess`` ）的 ``FESS_JAVA_OPTS`` 中追加：

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

通过 HTTP 代理使用
==================

自 |Fess| 15.6.1 起，Gemini客户端会共享 |Fess| 整体的HTTP代理配置。请在 ``fess_config.properties`` 中指定以下属性。

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
   传统的Java系统属性（ ``-Dhttps.proxyHost`` 等）不会被Gemini客户端引用。

通过Vertex AI使用
=================

如果使用Google Cloud Platform，也可以通过Vertex AI使用Gemini。
使用Vertex AI时，API端点和认证方法不同。

.. note::
   当前 |Fess| 使用Google AI API（generativelanguage.googleapis.com）。
   如需通过Vertex AI使用，可能需要自定义实现。

模型选择指南
============

根据使用目的的模型选择指南。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 模型
     - 速度
     - 质量
     - 用途
   * - ``gemini-3.1-flash-lite-preview``
     - 高速
     - 高
     - 轻量、低成本（默认，支持 ``thinkingLevel=MINIMAL`` ）
   * - ``gemini-3-flash-preview``
     - 高速
     - 最高
     - 一般用途（支持 ``thinkingLevel=MINIMAL`` ）
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - 中速
     - 最高
     - 复杂推理（不支持 ``MINIMAL``，最低为 ``LOW`` ）
   * - ``gemini-2.5-flash``
     - 高速
     - 高
     - 稳定版、成本优先
   * - ``gemini-2.5-pro``
     - 中速
     - 高
     - 稳定版、长上下文

上下文窗口
----------

Gemini模型支持非常长的上下文窗口:

- **Gemini 3 Flash / 2.5 Flash**: 最大100万令牌
- **Gemini 3.1 Pro / 2.5 Pro**: 最大100万令牌（3.1 Pro）/ 200万令牌（2.5 Pro）

利用此特性，可以在上下文中包含更多搜索结果。

::

    # 在上下文中包含更多文档（在fess_config.properties中设置）
    rag.llm.gemini.answer.context.max.chars=20000

成本估算
--------

Google AI API按使用量计费（有免费额度）。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 模型
     - 输入（100万字符）
     - 输出（100万字符）
   * - Gemini 3 Flash Preview
     - $0.50
     - $3.00
   * - Gemini 3.1 Pro Preview
     - $2.00
     - $12.00
   * - Gemini 2.5 Flash
     - $0.075
     - $0.30
   * - Gemini 2.5 Pro
     - $1.25
     - $5.00

.. note::
   最新价格和免费额度信息请查阅 `Google AI Pricing <https://ai.google.dev/pricing>`__

并发请求控制
==================

|Fess| 中可以控制对Gemini的并发请求数。
请在 ``fess_config.properties`` 中设置以下属性。

::

    # 最大并发请求数（默认: 5）
    rag.llm.gemini.max.concurrent.requests=5

通过此设置，可防止向Google AI API发送过多请求，避免速率限制错误。

免费额度限制（参考）
--------------------

Google AI API有免费额度，但有以下限制:

- 请求/分钟: 15 RPM
- 令牌/分钟: 100万 TPM
- 请求/日: 1,500 RPD

使用免费额度时，建议将 ``rag.llm.gemini.max.concurrent.requests`` 设置得低一些。

故障排除
======================

认证错误
----------

**症状**: 发生API密钥相关错误

**检查事项**:

1. 确认API密钥配置正确
2. 确认API密钥在Google AI Studio上有效
3. 确认API密钥具有所需权限
4. 确认API在项目中已启用

速率限制错误
------------

**症状**: 发生"429 Resource has been exhausted"错误

**解决方法**:

1. 在 ``fess_config.properties`` 中减少并发请求数::

    rag.llm.gemini.max.concurrent.requests=3

2. 等待几分钟后重试
3. 必要时申请提高配额

区域限制
--------------

**症状**: 服务不可用错误

**检查事项**:

Google AI API仅在部分地区可用。请查阅Google文档确认支持的地区。

超时
------------

**症状**: 请求超时

**解决方法**:

1. 延长超时时间::

    rag.llm.gemini.timeout=120000

2. 考虑使用Flash模型（更快）

调试设置
------------

调查问题时，可调整 |Fess| 日志级别输出Gemini相关的详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

安全注意事项
========================

使用Google AI API时，请注意以下安全事项。

1. **数据隐私**: 搜索结果内容会发送到Google服务器
2. **API密钥管理**: 密钥泄露会导致未授权使用
3. **合规性**: 包含机密数据时，请确认组织政策
4. **使用条款**: 遵守Google使用条款和可接受使用政策

参考信息
========

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - LLM集成概述
- :doc:`rag-chat` - AI搜索模式功能详情
