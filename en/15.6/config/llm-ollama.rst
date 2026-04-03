==========================
Ollama Configuration
==========================

Overview
========

Ollama is an open-source platform for running Large Language Models (LLM) in local environments.
In |Fess| 15.6, Ollama integration is provided as the ``fess-llm-ollama`` plugin and is suitable for use in private environments.

Using Ollama allows you to use AI search mode functionality without sending data externally.

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
- ``gemma4:e4b`` - Google's Gemma 4 (E4B parameters, default)
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

    # Download default model (Gemma 4 E4B)
    ollama pull gemma4:e4b

    # Download Llama 3.3
    ollama pull llama3.3:70b

    # Verify model works
    ollama run gemma4:e4b "Hello, how are you?"

Plugin Installation
===================

In |Fess| 15.6, Ollama integration has been separated as a plugin.
To use Ollama, you must install the ``fess-llm-ollama`` plugin.

1. Download `fess-llm-ollama-15.6.0.jar`.
2. Place it in the ``app/WEB-INF/plugin/`` directory of your |Fess| installation directory.

::

    cp fess-llm-ollama-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Restart |Fess|.

.. note::
   The plugin version should match the version of |Fess|.

Basic Configuration
===================

In |Fess| 15.6, LLM-related configuration is split across multiple configuration files.

Minimal Configuration
---------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Ollama URL (for local environment)
    rag.llm.ollama.api.url=http://localhost:11434

    # Model to use
    rag.llm.ollama.model=gemma4:e4b

``system.properties`` (also configurable from Administration > System > General):

::

    # Set LLM provider to Ollama
    rag.llm.name=ollama

.. note::
   The LLM provider setting can also be configured by setting ``rag.llm.name`` from the administration screen (Administration > System > General).

Recommended Configuration (Production)
---------------------------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # Model setting (use large model)
    rag.llm.ollama.model=llama3.3:70b

    # Timeout setting (increased for large models)
    rag.llm.ollama.timeout=120000

    # Concurrent request control
    rag.llm.ollama.max.concurrent.requests=5

``system.properties``:

::

    # LLM provider setting
    rag.llm.name=ollama

Configuration Options
=====================

All configuration options available for the Ollama client. All settings except ``rag.llm.name`` are configured in ``fess_config.properties``.

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
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - Request timeout (in milliseconds)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - Availability check interval (in seconds)
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Maximum number of concurrent requests
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents during evaluation
     - ``3``

Concurrency Control
-------------------

Use ``rag.llm.ollama.max.concurrent.requests`` to control the number of concurrent requests to Ollama.
The default is 5. Adjust according to the resources of your Ollama server.
Too many concurrent requests may overload the Ollama server and degrade response speed.

Per-Prompt-Type Settings
========================

In |Fess|, LLM parameters can be customized per prompt type.
Configure in ``fess_config.properties``.

The following parameters can be set per prompt type:

- ``rag.llm.ollama.{promptType}.temperature`` - Temperature during generation
- ``rag.llm.ollama.{promptType}.max.tokens`` - Maximum number of tokens
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Maximum number of context characters

Available prompt types:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Prompt Type
     - Description
   * - ``intent``
     - Prompt for determining user intent
   * - ``evaluation``
     - Prompt for evaluating search results
   * - ``unclear``
     - Response prompt for unclear queries
   * - ``noresults``
     - Prompt for when no results are found
   * - ``docnotfound``
     - Prompt for when documents are not found
   * - ``answer``
     - Answer generation prompt
   * - ``summary``
     - Summary generation prompt
   * - ``faq``
     - FAQ generation prompt
   * - ``direct``
     - Direct response prompt

Configuration Examples::

    # Set temperature for answer generation
    rag.llm.ollama.answer.temperature=0.7

    # Set maximum tokens for summary generation
    rag.llm.ollama.summary.max.tokens=2048

    # Set maximum context characters for intent analysis
    rag.llm.ollama.intent.context.max.chars=4000

Ollama Model Options
====================

Ollama model parameters can be configured in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.ollama.top.p``
     - Top-P sampling value (0.0 to 1.0)
     - (Not set)
   * - ``rag.llm.ollama.top.k``
     - Top-K sampling value
     - (Not set)
   * - ``rag.llm.ollama.num.ctx``
     - Context window size
     - (Not set)
   * - ``rag.llm.ollama.default.*``
     - Default fallback settings
     - (Not set)
   * - ``rag.llm.ollama.options.*``
     - Global options
     - (Not set)

Configuration Examples::

    # Top-P sampling
    rag.llm.ollama.top.p=0.9

    # Top-K sampling
    rag.llm.ollama.top.k=40

    # Context window size
    rag.llm.ollama.num.ctx=4096

Thinking Model Support
======================

When using thinking models such as gemma4 or qwen3.5, |Fess| supports configuring a thinking budget.

Set the following in ``fess_config.properties``:

::

    # Thinking budget configuration
    rag.llm.ollama.thinking.budget=1024

By setting the thinking budget, you can control the number of tokens allocated to the "thinking" step that the model performs before generating a response.

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
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma4:e4b
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
   * - ``gemma4:e4b``
     - Small-Medium
     - 8GB+
     - Well-balanced general use, thinking support (default)
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
    ollama run gemma4:e4b --verbose

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

4. Verify the ``fess-llm-ollama`` plugin is placed in ``app/WEB-INF/plugin/``

Model Not Found
---------------

**Symptom**: "Configured model not found in Ollama" appears in logs

**Solutions**:

1. Verify the model name is correct (may need to include ``:latest`` tag)::

    # Check model list
    ollama list

2. Download the required model::

    ollama pull gemma4:e4b

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
