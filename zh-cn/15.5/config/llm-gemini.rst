==========================
Google Gemini配置
==========================

概述
====

Google Gemini是Google公司提供的最先进的大型语言模型（LLM）。
|Fess| 可以使用Google AI API（Generative Language API）通过Gemini模型实现RAG聊天功能。

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

- ``gemini-2.5-flash`` - 高速高效的模型（推荐）
- ``gemini-2.5-pro`` - 具有更高推理能力的模型
- ``gemini-1.5-flash`` - 稳定版Flash模型
- ``gemini-1.5-pro`` - 稳定版Pro模型

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

基本配置
========

在 ``app/WEB-INF/conf/system.properties`` 中添加以下配置。

最小配置
--------

::

    # 启用RAG聊天功能
    rag.chat.enabled=true

    # 设置LLM提供商为Gemini
    rag.llm.type=gemini

    # Gemini API密钥
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 使用的模型
    rag.llm.gemini.model=gemini-2.5-flash

推荐配置（生产环境）
--------------------

::

    # 启用RAG聊天功能
    rag.chat.enabled=true

    # LLM提供商设置
    rag.llm.type=gemini

    # Gemini API密钥
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # 模型设置（使用高速模型）
    rag.llm.gemini.model=gemini-2.5-flash

    # API端点（通常无需更改）
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # 超时设置
    rag.llm.gemini.timeout=60000

配置项
======

Gemini客户端可用的所有配置项。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.gemini.api.key``
     - Google AI API密钥
     - （必需）
   * - ``rag.llm.gemini.model``
     - 使用的模型名称
     - ``gemini-2.5-flash``
   * - ``rag.llm.gemini.api.url``
     - API的基础URL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - 请求超时时间（毫秒）
     - ``60000``

环境变量配置
============

出于安全考虑，建议使用环境变量设置API密钥。

Docker环境
----------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-2.5-flash

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
   * - ``gemini-2.5-flash``
     - 高速
     - 高
     - 一般用途、平衡优先（推荐）
   * - ``gemini-2.5-pro``
     - 中速
     - 最高
     - 复杂推理、需要高质量
   * - ``gemini-1.5-flash``
     - 高速
     - 良好
     - 成本优先、稳定性优先
   * - ``gemini-1.5-pro``
     - 中速
     - 高
     - 需要长上下文

上下文窗口
----------

Gemini模型支持非常长的上下文窗口:

- **Gemini 1.5/2.5 Flash**: 最大100万令牌
- **Gemini 1.5/2.5 Pro**: 最大200万令牌

利用此特性，可以在上下文中包含更多搜索结果。

::

    # 在上下文中包含更多文档
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

成本估算
--------

Google AI API按使用量计费（有免费额度）。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 模型
     - 输入（100万字符）
     - 输出（100万字符）
   * - Gemini 1.5 Flash
     - $0.075
     - $0.30
   * - Gemini 1.5 Pro
     - $1.25
     - $5.00
   * - Gemini 2.5 Flash
     - 价格可能变动
     - 价格可能变动

.. note::
   最新价格和免费额度信息请查阅 `Google AI Pricing <https://ai.google.dev/pricing>`__

速率限制
========

Google AI API有速率限制。请结合 |Fess| 的速率限制功能适当配置。

::

    # Fess速率限制设置
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

免费额度限制
------------

Google AI API有免费额度，但有以下限制:

- 请求/分钟: 15 RPM
- 令牌/分钟: 100万 TPM
- 请求/日: 1,500 RPD

故障排除
========

认证错误
--------

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

1. 加严 |Fess| 速率限制设置::

    rag.chat.rate.limit.requests.per.minute=5

2. 等待几分钟后重试
3. 必要时申请提高配额

区域限制
--------

**症状**: 服务不可用错误

**检查事项**:

Google AI API仅在部分地区可用。请查阅Google文档确认支持的地区。

超时
----

**症状**: 请求超时

**解决方法**:

1. 延长超时时间::

    rag.llm.gemini.timeout=120000

2. 考虑使用Flash模型（更快）

调试设置
--------

调查问题时，可调整 |Fess| 日志级别输出Gemini相关的详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

安全注意事项
============

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
- :doc:`rag-chat` - RAG聊天功能详情

