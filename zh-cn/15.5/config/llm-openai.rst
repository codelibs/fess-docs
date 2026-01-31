==========================
OpenAI配置
==========================

概述
====

OpenAI是提供GPT-4等高性能大型语言模型（LLM）的云服务。
|Fess| 可以使用OpenAI API实现RAG聊天功能。

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

- ``gpt-4o`` - 最新的高性能模型
- ``gpt-4o-mini`` - GPT-4o的轻量版（成本效益高）
- ``gpt-4-turbo`` - GPT-4的高速版
- ``gpt-3.5-turbo`` - 性价比优秀的模型

.. note::
   可用模型的最新信息请查阅 `OpenAI Models <https://platform.openai.com/docs/models>`__

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

基本配置
========

在 ``app/WEB-INF/conf/system.properties`` 中添加以下配置。

最小配置
--------

::

    # 启用RAG聊天功能
    rag.chat.enabled=true

    # 设置LLM提供商为OpenAI
    rag.llm.type=openai

    # OpenAI API密钥
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用的模型
    rag.llm.openai.model=gpt-4o-mini

推荐配置（生产环境）
--------------------

::

    # 启用RAG聊天功能
    rag.chat.enabled=true

    # LLM提供商设置
    rag.llm.type=openai

    # OpenAI API密钥
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # 模型设置（使用高性能模型）
    rag.llm.openai.model=gpt-4o

    # API端点（通常无需更改）
    rag.llm.openai.api.url=https://api.openai.com/v1

    # 超时设置
    rag.llm.openai.timeout=60000

配置项
======

OpenAI客户端可用的所有配置项。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.openai.api.key``
     - OpenAI API密钥
     - （必需）
   * - ``rag.llm.openai.model``
     - 使用的模型名称
     - ``gpt-5-mini``
   * - ``rag.llm.openai.api.url``
     - API的基础URL
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - 请求超时时间（毫秒）
     - ``60000``

环境变量配置
============

出于安全考虑，建议使用环境变量设置API密钥。

Docker环境
----------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-4o-mini

systemd环境
-----------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

使用Azure OpenAI
================

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
   * - ``gpt-3.5-turbo``
     - 低
     - 良好
     - 一般问答、成本优先
   * - ``gpt-4o-mini``
     - 中
     - 高
     - 平衡用途（推荐）
   * - ``gpt-4o``
     - 高
     - 最高
     - 复杂推理、需要高质量
   * - ``gpt-4-turbo``
     - 高
     - 最高
     - 需要快速响应

成本估算
--------

OpenAI API按使用量计费。以下是2024年的参考价格。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 模型
     - 输入（1K令牌）
     - 输出（1K令牌）
   * - gpt-3.5-turbo
     - $0.0005
     - $0.0015
   * - gpt-4o-mini
     - $0.00015
     - $0.0006
   * - gpt-4o
     - $0.005
     - $0.015

.. note::
   最新价格请查阅 `OpenAI Pricing <https://openai.com/pricing>`__

速率限制
========

OpenAI API有速率限制。请结合 |Fess| 的速率限制功能适当配置。

::

    # Fess速率限制设置
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

OpenAI Tier限制
---------------

限制因OpenAI账户Tier而异:

- **Free**: 3 RPM（请求/分钟）
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: 更高限制

故障排除
========

认证错误
--------

**症状**: 发生"401 Unauthorized"错误

**检查事项**:

1. 确认API密钥配置正确
2. 确认API密钥有效（在OpenAI仪表板确认）
3. 确认API密钥具有所需权限

速率限制错误
------------

**症状**: 发生"429 Too Many Requests"错误

**解决方法**:

1. 加严 |Fess| 速率限制设置::

    rag.chat.rate.limit.requests.per.minute=5

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

    rag.llm.openai.timeout=120000

2. 考虑使用更快的模型（如gpt-3.5-turbo）

调试设置
--------

调查问题时，可调整 |Fess| 日志级别输出OpenAI相关的详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

安全注意事项
============

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
- :doc:`rag-chat` - RAG聊天功能详情

