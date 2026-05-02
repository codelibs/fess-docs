==========================
Ollama配置
==========================

概述
====

Ollama是用于在本地环境运行大型语言模型（LLM）的开源平台。
|Fess| 15.6中，Ollama集成功能以插件 ``fess-llm-ollama`` 的形式提供，适合在私有环境中使用。

使用Ollama，可以在不将数据发送到外部的情况下使用AI搜索模式功能。

主要特点
--------

- **本地执行**: 数据不发送到外部，确保隐私
- **多种模型**: 支持Llama、Mistral、Gemma、CodeLlama等多种模型
- **成本效益**: 无API成本（仅硬件成本）
- **可定制**: 可使用自行微调的模型

支持的模型
----------

Ollama可用的主要模型:

- ``llama3.3:70b`` - Meta公司的Llama 3.3（700亿参数）
- ``gemma4:e4b`` - Google公司的Gemma 4（E4B参数，默认）
- ``mistral:7b`` - Mistral AI公司的Mistral（70亿参数）
- ``codellama:13b`` - Meta公司的Code Llama（130亿参数）
- ``phi3:3.8b`` - Microsoft公司的Phi-3（38亿参数）

.. note::
   可用模型的最新列表请查阅 `Ollama Library <https://ollama.com/library>`__

前提条件
========

使用Ollama前，请确认以下内容。

1. **安装Ollama**: 从 `https://ollama.com/ <https://ollama.com/>`__ 下载安装
2. **下载模型**: 将要使用的模型下载到Ollama
3. **启动Ollama服务器**: 确认Ollama正在运行

安装Ollama
----------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

从官网下载安装程序并运行。

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

下载模型
--------

::

    # 下载默认模型（Gemma 4 E4B）
    ollama pull gemma4:e4b

    # 下载Llama 3.3
    ollama pull llama3.3:70b

    # 验证模型运行
    ollama run gemma4:e4b "Hello, how are you?"

插件安装
========================

|Fess| 15.6中，Ollama集成功能已作为插件分离提供。
使用Ollama需要安装 ``fess-llm-ollama`` 插件。

1. 下载 `fess-llm-ollama-15.6.0.jar`。
2. 将其放置到 |Fess| 安装目录下的 ``app/WEB-INF/plugin/`` 目录。

::

    cp fess-llm-ollama-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. 重启 |Fess|。

.. note::
   插件版本请与 |Fess| 版本保持一致。

基本配置
========

|Fess| 15.6中，LLM相关配置分布在多个配置文件中。

最小配置
--------

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # Ollama URL（本地环境时）
    rag.llm.ollama.api.url=http://localhost:11434

    # 使用的模型
    rag.llm.ollama.model=gemma4:e4b

``system.properties``（也可在管理界面 > 系统 > 通用中配置）:

::

    # 将LLM提供商设置为Ollama
    rag.llm.name=ollama

.. note::
   LLM提供商的配置也可以通过管理界面（管理界面 > 系统 > 通用）设置 ``rag.llm.name``。

推荐配置（生产环境）
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # 启用AI搜索模式功能
    rag.chat.enabled=true

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # 模型设置（使用大型模型）
    rag.llm.ollama.model=llama3.3:70b

    # 超时设置（为大型模型增加）
    rag.llm.ollama.timeout=120000

    # 并发请求数控制
    rag.llm.ollama.max.concurrent.requests=5

``system.properties``:

::

    # LLM提供商设置
    rag.llm.name=ollama

配置项
======

Ollama客户端可用的所有配置项。 ``rag.llm.name`` 在 ``system.properties`` 或管理界面中进行设置，其他配置均在 ``fess_config.properties`` 中进行。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.ollama.api.url``
     - Ollama服务器的基础URL
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - 使用的模型名称（已下载到Ollama的模型）
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - 请求超时时间（毫秒）
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - 可用性检查间隔（秒）
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - 最大并发请求数
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - 评估最大相关文档数
     - ``3``

并发控制
------------

使用 ``rag.llm.ollama.max.concurrent.requests`` 可以控制对Ollama的并发请求数。
默认值为5。请根据Ollama服务器的资源进行调整。
并发请求数过多时，会给Ollama服务器增加负担，导致响应速度下降。

提示词类型别配置
======================

|Fess| 中可以按提示词类型自定义LLM参数。
配置在 ``fess_config.properties`` 中记述。

按提示词类型可设置以下参数:

- ``rag.llm.ollama.{promptType}.temperature`` - 生成时的temperature
- ``rag.llm.ollama.{promptType}.max.tokens`` - 最大token数
- ``rag.llm.ollama.{promptType}.context.max.chars`` - 上下文最大字符数

可用的提示词类型:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 提示词类型
     - 说明
   * - ``intent``
     - 判定用户意图的提示词
   * - ``evaluation``
     - 评估搜索结果的提示词
   * - ``unclear``
     - 针对不明确查询的响应提示词
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

配置示例::

    # 设置生成回答时的temperature
    rag.llm.ollama.answer.temperature=0.7

    # 设置生成摘要时的最大token数
    rag.llm.ollama.summary.max.tokens=2048

    # 设置意图判定时的上下文最大字符数
    rag.llm.ollama.intent.context.max.chars=4000

Ollama模型选项
======================

可在 ``fess_config.properties`` 中设置Ollama的模型参数。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rag.llm.ollama.top.p``
     - Top-P采样的值（0.0〜1.0）
     - (未设置)
   * - ``rag.llm.ollama.top.k``
     - Top-K采样的值
     - (未设置)
   * - ``rag.llm.ollama.num.ctx``
     - 上下文窗口大小
     - (未设置)
   * - ``rag.llm.ollama.default.*``
     - 默认回退配置
     - (未设置)
   * - ``rag.llm.ollama.options.*``
     - 全局选项
     - (未设置)

配置示例::

    # Top-P采样
    rag.llm.ollama.top.p=0.9

    # Top-K采样
    rag.llm.ollama.top.k=40

    # 上下文窗口大小
    rag.llm.ollama.num.ctx=4096

思考模型支持
==============

使用gemma4或qwen3.5等思考模型（thinking model）时，|Fess| 支持设置思考预算（thinking budget）。

在 ``fess_config.properties`` 中进行如下设置:

::

    # 设置思考预算
    rag.llm.ollama.thinking.budget=1024

通过设置思考预算，可以控制模型在生成回答前用于"思考"步骤的token数。

网络配置
================

Docker配置
--------------

以下是 |Fess| 和Ollama均在Docker中运行时的配置示例。

``docker-compose.yml``:

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma4:e4b
        depends_on:
          - ollama
        # ... 其他设置

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   在Docker Compose环境中，使用 ``ollama`` 作为主机名（而不是 ``localhost``）。

远程Ollama服务器
----------------------

在与Fess不同的服务器上运行Ollama时:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama默认没有认证功能，如果要从外部访问，
   请考虑网络级别的安全措施（防火墙、VPN等）。

通过 HTTP 代理使用
==================

自 |Fess| 15.6.1 起，Ollama客户端会共享 |Fess| 整体的HTTP代理配置。当连接Ollama服务器需要经过代理时（例如使用远程Ollama服务器时），请在 ``fess_config.properties`` 中指定以下属性。

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

.. note::
   由于Ollama通常运行在本地或内部网络，需要代理配置的情况仅限于特定场景（例如使用仅能通过公司代理到达的远程Ollama服务器等）。
   此配置同样会影响爬虫等 |Fess| 整体的HTTP访问。

模型选择指南
============

根据使用目的的模型选择指南。

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - 模型
     - 大小
     - 所需VRAM
     - 用途
   * - ``phi3:3.8b``
     - 小
     - 4GB以上
     - 轻量环境、简单问答
   * - ``gemma4:e4b``
     - 小~中
     - 8GB以上
     - 平衡的通用用途、支持思考模式（默认）
   * - ``mistral:7b``
     - 中
     - 8GB以上
     - 需要高质量回答
   * - ``llama3.3:70b``
     - 大
     - 48GB以上
     - 最高质量回答、复杂推理

GPU支持
-------

Ollama支持GPU加速。使用NVIDIA GPU可显著提高推理速度。

::

    # 确认GPU支持
    ollama run gemma4:e4b --verbose

故障排除
======================

连接错误
--------

**症状**: 聊天功能出错、显示LLM不可用

**检查事项**:

1. 确认Ollama正在运行::

    curl http://localhost:11434/api/tags

2. 确认模型已下载::

    ollama list

3. 检查防火墙设置

4. 确认 ``fess-llm-ollama`` 插件已放置到 ``app/WEB-INF/plugin/``

模型未找到
--------------------

**症状**: 日志输出"Configured model not found in Ollama"

**解决方法**:

1. 确认模型名称正确（可能需要包含 ``:latest`` 标签）::

    # 确认模型列表
    ollama list

2. 下载所需模型::

    ollama pull gemma4:e4b

超时
------------

**症状**: 请求超时

**解决方法**:

1. 延长超时时间::

    rag.llm.ollama.timeout=120000

2. 考虑使用更小的模型或GPU环境

调试设置
------------

调查问题时，可调整 |Fess| 日志级别输出Ollama相关的详细日志。

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

参考信息
========

- `Ollama官网 <https://ollama.com/>`__
- `Ollama模型库 <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - LLM集成概述
- :doc:`rag-chat` - AI搜索模式功能详情
