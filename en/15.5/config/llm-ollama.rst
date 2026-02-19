==========================
Ollama Configuration
==========================

Overview
========

Ollama is an open-source platform for running Large Language Models (LLM) in local environments.
It is configured as the default LLM provider for |Fess| and is suitable for use in private environments.

Using Ollama allows you to use AI chat functionality without sending data externally.

Key Features
------------

- **Local Execution**: Data is not sent externally, ensuring privacy
- **Various Models**: Supports multiple models including Llama, Mistral, Gemma, and CodeLlama
- **Cost Efficiency**: No API costs (only hardware costs)
- **Customization**: Can use custom fine-tuned models

Supported Models
----------------

Main models available with Ollama:

- ``llama3.3:70b`` - Meta's Llama 3.3 (70B parameters)
- ``gemma3:4b`` - Google's Gemma 3 (4B parameters, default)
- ``mistral:7b`` - Mistral AI's Mistral (7B parameters)
- ``codellama:13b`` - Meta's Code Llama (13B parameters)
- ``phi3:3.8b`` - Microsoft's Phi-3 (3.8B parameters)

.. note::
   For the latest list of available models, see `Ollama Library <https://ollama.com/library>`__.

Prerequisites
=============

Before using Ollama, verify the following.

1. **Ollama Installation**: Download and install from `https://ollama.com/ <https://ollama.com/>`__
2. **Model Download**: Download the model you want to use to Ollama
3. **Ollama Server Running**: Verify Ollama is running

Installing Ollama
-----------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

Download and run the installer from the official website.

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Downloading Models
------------------

::

    # Download default model (Gemma 3 4B)
    ollama pull gemma3:4b

    # Download Llama 3.3
    ollama pull llama3.3:70b

    # Verify model works
    ollama run gemma3:4b "Hello, how are you?"

Basic Configuration
===================

Add the following settings to ``app/WEB-INF/conf/fess_config.properties``.

Minimal Configuration
---------------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Set LLM provider to Ollama
    rag.llm.type=ollama

    # Ollama URL (for local environment)
    rag.llm.ollama.api.url=http://localhost:11434

    # Model to use
    rag.llm.ollama.model=gemma3:4b

Recommended Configuration (Production)
--------------------------------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # LLM provider setting
    rag.llm.type=ollama

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # Model setting (use large model)
    rag.llm.ollama.model=llama3.3:70b

    # Timeout setting (increased for large models)
    rag.llm.ollama.timeout=120000

Configuration Options
=====================

All configuration options available for the Ollama client.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.ollama.api.url``
     - Ollama server base URL
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - Model name to use (must be downloaded to Ollama)
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - Request timeout (in milliseconds)
     - ``60000``

Network Configuration
=====================

Docker Configuration
--------------------

Example configuration when running both |Fess| and Ollama in Docker.

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
        # ... other settings

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   In Docker Compose environments, use ``ollama`` as the hostname (not ``localhost``).

Remote Ollama Server
--------------------

When running Ollama on a separate server from Fess:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama does not have authentication by default, so when making it externally accessible,
   consider network-level security measures (firewall, VPN, etc.).

Model Selection Guide
=====================

Guidelines for selecting models based on intended use.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Model
     - Size
     - Required VRAM
     - Use Case
   * - ``phi3:3.8b``
     - Small
     - 4GB+
     - Lightweight environments, simple Q&A
   * - ``gemma3:4b``
     - Small-Medium
     - 6GB+
     - Well-balanced general use (default)
   * - ``mistral:7b``
     - Medium
     - 8GB+
     - When high-quality responses are needed
   * - ``llama3.3:70b``
     - Large
     - 48GB+
     - Highest quality responses, complex reasoning

GPU Support
-----------

Ollama supports GPU acceleration. Using an NVIDIA GPU significantly improves
inference speed.

::

    # Check GPU support
    ollama run gemma3:4b --verbose

Troubleshooting
===============

Connection Errors
-----------------

**Symptom**: Chat functionality shows errors, LLM displays as unavailable

**Check the following**:

1. Verify Ollama is running::

    curl http://localhost:11434/api/tags

2. Verify the model is downloaded::

    ollama list

3. Check firewall settings

Model Not Found
---------------

**Symptom**: "Configured model not found in Ollama" appears in logs

**Solutions**:

1. Verify the model name is correct (may need to include ``:latest`` tag)::

    # Check model list
    ollama list

2. Download the required model::

    ollama pull gemma3:4b

Timeout
-------

**Symptom**: Requests time out

**Solutions**:

1. Extend timeout duration::

    rag.llm.ollama.timeout=120000

2. Consider using a smaller model or GPU environment

Debug Settings
--------------

When investigating issues, adjust |Fess| log levels to output detailed Ollama-related logs.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

References
==========

- `Ollama Official Website <https://ollama.com/>`__
- `Ollama Model Library <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - LLM Integration Overview
- :doc:`rag-chat` - AI Mode Details
