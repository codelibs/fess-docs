==========================
Ollama配置
==========================

概述
====

Ollama是用于在本地环境运行大型语言模型（LLM）的开源平台。
它是 |Fess| 的默认LLM提供商，适合在私有环境中使用。

使用Ollama，可以在不将数据发送到外部的情况下使用AI聊天功能。

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
- ``gemma3:4b`` - Google公司的Gemma 3（40亿参数，默认）
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

    # 下载默认模型（Gemma 3 4B）
    ollama pull gemma3:4b

    # 下载Llama 3.3
    ollama pull llama3.3:70b

    # 验证模型
    ollama run gemma3:4b "Hello, how are you?"

基本配置
========

在 ``app/WEB-INF/conf/system.properties`` 中添加以下配置。

最小配置
--------

::

    # 启用AI模式功能
    rag.chat.enabled=true

    # 设置LLM提供商为Ollama
    rag.llm.type=ollama

    # Ollama URL（本地环境）
    rag.llm.ollama.api.url=http://localhost:11434

    # 使用的模型
    rag.llm.ollama.model=gemma3:4b

推荐配置（生产环境）
--------------------

::

    # 启用AI模式功能
    rag.chat.enabled=true

    # LLM提供商设置
    rag.llm.type=ollama

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # 模型设置（使用大型模型）
    rag.llm.ollama.model=llama3.3:70b

    # 超时设置（为大型模型增加）
    rag.llm.ollama.timeout=120000

配置项
======

Ollama客户端可用的所有配置项。

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
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - 请求超时时间（毫秒）
     - ``60000``

网络配置
========

Docker配置
----------

|Fess| 和Ollama都在Docker中运行时的配置示例。

``docker-compose.yml``:

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma3:4b
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
----------------

在与Fess不同的服务器上运行Ollama时:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama默认没有认证功能，如果要从外部访问，
   请考虑网络级别的安全措施（防火墙、VPN等）。

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
   * - ``gemma3:4b``
     - 小~中
     - 6GB以上
     - 平衡的通用用途（默认）
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
    ollama run gemma3:4b --verbose

故障排除
========

连接错误
--------

**症状**: 聊天功能出错、显示LLM不可用

**检查事项**:

1. 确认Ollama正在运行::

    curl http://localhost:11434/api/tags

2. 确认模型已下载::

    ollama list

3. 检查防火墙设置

模型未找到
----------

**症状**: 日志输出"Configured model not found in Ollama"

**解决方法**:

1. 确认模型名称正确（可能需要包含 ``:latest`` 标签）::

    # 确认模型列表
    ollama list

2. 下载所需模型::

    ollama pull gemma3:4b

超时
----

**症状**: 请求超时

**解决方法**:

1. 延长超时时间::

    rag.llm.ollama.timeout=120000

2. 考虑使用更小的模型或GPU环境

调试设置
--------

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
- :doc:`rag-chat` - AI模式功能详情

