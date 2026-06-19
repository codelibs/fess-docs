==========================
Ollama Configuration
==========================

Overview
========

Ollama is an open-source platform for running Large Language Models (LLMs) in local environments.
|Fess| Ollama integration is provided as the ``fess-llm-ollama`` plugin and is suitable for use in private environments.

Using Ollama allows you to use the AI search mode functionality without sending data externally.

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

Ollama integration is provided as a plugin.
To use Ollama, you must install the ``fess-llm-ollama`` plugin.

1. Download `fess-llm-ollama-15.7.0.jar`.
2. Place it in the ``app/WEB-INF/plugin/`` directory of your |Fess| installation directory.

::

    cp fess-llm-ollama-15.7.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Restart |Fess|.

.. note::
   The plugin version should match the version of |Fess|.

Basic Configuration
===================

LLM-related configuration is split across multiple configuration files.

Minimal Configuration
---------------------

``system.properties`` (also configurable from Administration > System > General):

::

    # Set LLM provider to Ollama
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI search mode functionality
    rag.chat.enabled=true

    # Ollama URL (for local environment)
    rag.llm.ollama.api.url=http://localhost:11434

    # Model to use
    rag.llm.ollama.model=gemma4:e4b

.. note::
   The LLM provider setting can also be configured by setting ``rag.llm.name`` from the administration screen (Administration > System > General).

Recommended Configuration (Production)
---------------------------------------

``system.properties`` (also configurable from Administration > System > General):

::

    # LLM provider setting
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI search mode functionality
    rag.chat.enabled=true

    # Ollama URL
    rag.llm.ollama.api.url=http://localhost:11434

    # Model setting (use large model)
    rag.llm.ollama.model=llama3.3:70b

    # Timeout setting (increased for large models)
    rag.llm.ollama.timeout=120000

    # Concurrent request control
    rag.llm.ollama.max.concurrent.requests=5

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
     - Model name to use (must be already downloaded to Ollama)
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - Request timeout (in milliseconds)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - Availability check interval (in seconds). Setting a value of ``0`` or lower disables periodic availability checks
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Maximum number of concurrent requests
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents for evaluation
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - Permit acquisition wait timeout for concurrency control (in milliseconds)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - TCP connect timeout (in milliseconds). Configurable separately from ``rag.llm.ollama.timeout``
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - Maximum number of HTTP retry attempts (on ``429`` and ``5xx`` errors)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - Base delay for exponential backoff (in milliseconds)
     - ``2000``

Advanced Configuration
----------------------

Advanced configuration options for history and context size.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - Maximum number of characters for descriptions during evaluation
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - Maximum number of characters in conversation history
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - Maximum number of history messages for intent determination
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - Maximum number of history characters for intent determination
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - Maximum number of characters for assistant responses in history
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - Maximum number of characters for assistant summaries in history
     - ``500``

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
- ``rag.llm.ollama.{promptType}.max.tokens`` - Maximum number of tokens (mapped to ``num_predict`` in the Ollama API)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Maximum number of context characters
- ``rag.llm.ollama.{promptType}.thinking.budget`` - Thinking budget (boolean-style thinking control; see "Thinking Model Support" for details)
- ``rag.llm.ollama.{promptType}.thinking.level`` - Thinking level (string form: ``high`` / ``medium`` / ``low``; see "Thinking Model Support" for details)
- ``rag.llm.ollama.{promptType}.top.p`` - Top-P sampling value
- ``rag.llm.ollama.{promptType}.top.k`` - Top-K sampling value
- ``rag.llm.ollama.{promptType}.num.ctx`` - Context window size

Each parameter is resolved in the following order: ``rag.llm.ollama.{promptType}.<param>`` (per-prompt-type setting) → ``rag.llm.ollama.default.<param>`` (fallback common to all prompt types) → hardcoded default for each prompt type. Values explicitly specified in a request always take precedence.

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
     - Prompt for when no search results are found
   * - ``docnotfound``
     - Prompt for when a document is not found
   * - ``answer``
     - Answer generation prompt
   * - ``summary``
     - Summary generation prompt
   * - ``faq``
     - FAQ generation prompt
   * - ``direct``
     - Direct response prompt
   * - ``queryregeneration``
     - Query regeneration prompt

Each prompt type has hardcoded defaults that are applied when a setting is omitted.

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Prompt Type
     - temperature
     - max.tokens
     - thinking.budget
     - context.max.chars
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
     - ``6000``
   * - ``evaluation``
     - ``0.1``
     - ``512``
     - ``0``
     - ``6000``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - (not set)
     - ``10000``
   * - ``summary``
     - ``0.3``
     - ``8192``
     - (not set)
     - ``10000``
   * - ``faq``
     - ``0.7``
     - ``4096``
     - (not set)
     - ``6000``
   * - ``direct``
     - ``0.7``
     - ``4096``
     - (not set)
     - ``6000``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``
     - ``6000``

Configuration Examples::

    # Set temperature for answer generation
    rag.llm.ollama.answer.temperature=0.7

    # Set maximum tokens for summary generation
    rag.llm.ollama.summary.max.tokens=2048

    # Set maximum context characters for intent determination
    rag.llm.ollama.intent.context.max.chars=4000

Ollama Model Options
====================

Ollama model parameters can be configured in ``fess_config.properties``.
Specifying them in the form ``rag.llm.ollama.default.<param>`` sets them as fallback values common to all prompt types.
The ``default`` fallback applies not only to ``top.p`` / ``top.k`` / ``num.ctx`` but also to ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.ollama.default.top.p``
     - Top-P sampling value (0.0 to 1.0). Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.top.p``
     - (not set)
   * - ``rag.llm.ollama.default.top.k``
     - Top-K sampling value. Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.top.k``
     - (not set)
   * - ``rag.llm.ollama.default.num.ctx``
     - Context window size. Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.num.ctx``
     - (not set)
   * - ``rag.llm.ollama.default.temperature``
     - Fallback temperature value for generation. Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.temperature``
     - (not set)
   * - ``rag.llm.ollama.default.max.tokens``
     - Fallback maximum token count. Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.max.tokens``
     - (not set)
   * - ``rag.llm.ollama.default.thinking.budget``
     - Fallback thinking budget value. Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.thinking.budget``
     - (not set)
   * - ``rag.llm.ollama.default.thinking.level``
     - Fallback thinking level (``high`` / ``medium`` / ``low``). Can be overridden per prompt type with ``rag.llm.ollama.{promptType}.thinking.level``
     - (not set)
   * - ``rag.llm.ollama.options.*``
     - Global options passed directly to the Ollama API. The suffix is used as the option name (e.g. ``rag.llm.ollama.options.repeat_penalty=1.1``). Values are automatically converted to Integer, Double, Boolean, or String
     - (not set)

Configuration Examples::

    # Default Top-P sampling (common to all prompt types)
    rag.llm.ollama.default.top.p=0.9

    # Default Top-K sampling
    rag.llm.ollama.default.top.k=40

    # Default context window size
    rag.llm.ollama.default.num.ctx=4096

    # Override Top-P for answer generation only
    rag.llm.ollama.answer.top.p=0.95

    # Global option (passed directly to the Ollama API)
    rag.llm.ollama.options.repeat_penalty=1.1

Thinking Model Support
======================

When using thinking models such as gemma4 or qwen3, |Fess| supports configuring a thinking budget.

Set the thinking budget per prompt type in ``fess_config.properties``:

::

    # Thinking budget configuration for answer generation
    rag.llm.ollama.answer.thinking.budget=1024

    # Thinking budget configuration for summary generation
    rag.llm.ollama.summary.thinking.budget=1024

By setting the thinking budget, you can control the number of tokens allocated to the "thinking" step that the model performs before generating a response.

.. note::
   In Ollama, the thinking budget is converted to a boolean flag (``think: true`` when the value is greater than 0, ``think: false`` when the value is 0). Fine-grained control by token count is not available due to Ollama API constraints.

Thinking Level
--------------

Some models, such as gpt-oss, ignore the boolean ``think`` flag and require thinking level to be specified as a string value of ``high`` / ``medium`` / ``low``.
For such models, use ``rag.llm.ollama.{promptType}.thinking.level``.

::

    # Thinking level configuration for answer generation
    rag.llm.ollama.answer.thinking.level=high

    # Thinking level configuration for summary generation
    rag.llm.ollama.summary.thinking.level=medium

Valid values for ``thinking.level`` are ``high``, ``medium``, or ``low`` (case-insensitive). An invalid value is ignored and a warning is logged.

.. note::
   When both ``thinking.level`` (string form) and ``thinking.budget`` (boolean form) are set, ``thinking.level`` takes precedence. Use ``thinking.level`` for GPT-OSS-type models, and ``thinking.budget`` for other thinking models.

Network Configuration
=====================

Docker Configuration
--------------------

The official |Fess| `docker-fess <https://github.com/codelibs/docker-fess>`__ ships an Ollama overlay ``compose-ollama.yaml``. The minimum steps are:

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` is configured to use an NVIDIA GPU (NVIDIA Container Toolkit is required). Its contents are as follows:

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.7.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        container_name: ollama01
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama
        networks:
          - search_net
        restart: unless-stopped
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

    volumes:
      ollama-data:
        driver: local

Notes:

- ``FESS_PLUGINS=fess-llm-ollama:15.7.0`` causes the startup script to automatically download the plugin JAR and place it in ``app/WEB-INF/plugin/`` (adjust the version to match your |Fess| version)
- ``-Dfess.config.rag.chat.enabled=true`` enables AI search mode
- ``-Dfess.config.rag.llm.ollama.api.url=...`` sets the Ollama server URL (within the Docker Compose network, resolve it by the service name such as ``ollama01``)
- The default LLM provider (``rag.llm.name``) is ``ollama``, so no explicit setting is needed when using only Ollama. When switching from another provider, add ``-Dfess.system.rag.llm.name=ollama`` to ``FESS_JAVA_OPTS``, or configure it after startup from Administration > System > General in the RAG section
- The ``deploy.resources.reservations.devices`` block enables GPU usage. Remove this block if you do not use a GPU (CPU-only execution)

.. note::
   Uppercase snake-case environment variables such as ``RAG_CHAT_ENABLED`` and ``RAG_LLM_NAME`` are not recognized directly by |Fess|. All values must be passed inside ``FESS_JAVA_OPTS`` as ``-Dfess.config.<key>`` (for ``fess_config.properties`` keys) or ``-Dfess.system.<key>`` (for ``system.properties`` keys).

Remote Ollama Server
--------------------

When running Ollama on a separate server from Fess:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama does not have authentication by default, so when making it externally accessible,
   consider network-level security measures (firewall, VPN, etc.).

Using HTTP Proxy
================

The Ollama client shares the |Fess|-wide HTTP proxy configuration. If reaching the Ollama server requires going through a proxy (for example, when using a remote Ollama server), configure the following properties in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``http.proxy.host``
     - Proxy hostname (an empty string disables the proxy)
     - ``""``
   * - ``http.proxy.port``
     - Proxy port number
     - ``8080``
   * - ``http.proxy.username``
     - Username for proxy authentication (optional; enables Basic auth when set)
     - ``""``
   * - ``http.proxy.password``
     - Password for proxy authentication
     - ``""``

.. note::
   Because Ollama typically runs locally or on an internal network, proxy configuration is only required in limited cases (for example, when reaching a remote Ollama server that is only accessible through a corporate proxy).
   This configuration also affects |Fess|-wide HTTP access such as the crawler.

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
     - Well-balanced general use, thinking mode support (default)
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

**Symptom**: "Configured model not found" appears in logs

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

2. Consider using a smaller model or a GPU environment

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
- :doc:`rag-chat` - AI Search Mode Details
