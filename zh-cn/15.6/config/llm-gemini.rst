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

- ``gemini-3-flash-preview`` - 最新高速模型（推荐）
- ``gemini-3.1-pro-preview`` - 最新高推理模型
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
    rag.llm.gemini.model=gemini-3-flash-preview

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
    rag.llm.gemini.model=gemini-3-flash-preview

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
     - ``gemini-3-flash-preview``
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
     - ``256``
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
     - ``256``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``4096``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``2048``
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

可按提示词类型在 ``fess_config.properties`` 中设置思考预算。

::

    # 回答生成时的思考预算设置
    rag.llm.gemini.answer.thinking.budget=1024

    # 摘要生成时的思考预算设置
    rag.llm.gemini.summary.thinking.budget=1024

.. note::
   设置思考预算后，响应时间可能会变长。
   请根据用途设置适当的值。

环境变量配置
================

出于安全考虑，建议使用环境变量设置API密钥。

Docker环境
----------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.6.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-3-flash-preview

systemd环境
-----------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

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
   * - ``gemini-3-flash-preview``
     - 高速
     - 最高
     - 一般用途（推荐）
   * - ``gemini-3.1-pro-preview``
     - 中速
     - 最高
     - 复杂推理
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
