==========================
OpenAI Configuration
==========================

Overview
========

OpenAI is a cloud service that provides high-performance Large Language Models (LLM), including GPT-4.
|Fess| can use the OpenAI API to implement AI mode functionality.

Using OpenAI enables high-quality response generation powered by state-of-the-art AI models.

Key Features
------------

- **High-Quality Responses**: Highly accurate response generation using cutting-edge GPT models
- **Scalability**: Easy scaling as a cloud service
- **Continuous Improvement**: Performance improves with regular model updates
- **Rich Functionality**: Supports diverse tasks including text generation, summarization, and translation

Supported Models
----------------

Main models available with OpenAI:

- ``gpt-5`` - Latest high-performance model
- ``gpt-5-mini`` - Lightweight version of GPT-5 (cost-efficient)
- ``gpt-4o`` - High-performance multimodal model
- ``gpt-4o-mini`` - Lightweight version of GPT-4o
- ``o3-mini`` - Lightweight reasoning-focused model
- ``o4-mini`` - Next-generation lightweight reasoning model

.. note::
   For the latest information on available models, see `OpenAI Models <https://platform.openai.com/docs/models>`__.

.. note::
   When using o1/o3/o4 series or gpt-5 series models, |Fess| automatically uses the OpenAI API ``max_completion_tokens`` parameter. No configuration changes are required.

Prerequisites
=============

Before using OpenAI, prepare the following.

1. **OpenAI Account**: Create an account at `https://platform.openai.com/ <https://platform.openai.com/>`__
2. **API Key**: Generate an API key from the OpenAI dashboard
3. **Billing Setup**: Configure billing information as API usage incurs charges

Obtaining an API Key
--------------------

1. Log in to `OpenAI Platform <https://platform.openai.com/>`__
2. Navigate to the "API keys" section
3. Click "Create new secret key"
4. Enter a key name and create
5. Securely save the displayed key (it will only be shown once)

.. warning::
   API keys are confidential information. Please note the following:

   - Do not commit to version control systems
   - Do not output to logs
   - Manage using environment variables or secure configuration files

Plugin Installation
===================

In |Fess| 15.6, OpenAI integration is provided as a plugin. To use it, you must install the ``fess-llm-openai`` plugin.

1. Download `fess-llm-openai-15.6.0.jar`
2. Place the JAR file in the ``app/WEB-INF/plugin/`` directory of your |Fess| installation directory::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Restart |Fess|

.. note::
   The plugin version should match the version of |Fess|.

Basic Configuration
===================

In |Fess| 15.6, configuration items are divided into the following two files based on their purpose.

- ``app/WEB-INF/conf/fess_config.properties`` - |Fess| core settings and LLM provider-specific settings
- ``system.properties`` (Administration > System > General) - LLM provider selection (``rag.llm.name`` only)

Minimal Configuration
---------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # OpenAI API key
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model to use
    rag.llm.openai.model=gpt-5-mini

``system.properties`` (also configurable from Administration > System > General):

::

    # Set LLM provider to OpenAI
    rag.llm.name=openai

Recommended Configuration (Production)
---------------------------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # OpenAI API key
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model setting (use high-performance model)
    rag.llm.openai.model=gpt-4o

    # API endpoint (usually no change needed)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Timeout setting
    rag.llm.openai.timeout=120000

    # Concurrent request limit
    rag.llm.openai.max.concurrent.requests=5

``system.properties`` (also configurable from Administration > System > General):

::

    # LLM provider setting
    rag.llm.name=openai

Configuration Options
=====================

All configuration options available for the OpenAI client. All settings except ``rag.llm.name`` are configured in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - Property
     - Description
     - Default
     - Location
   * - ``rag.llm.name``
     - LLM provider name (specify ``openai``)
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - OpenAI API key
     - (Required)
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - Model name to use
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - API base URL
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - Request timeout (in milliseconds)
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - Availability check interval (in seconds)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - Maximum number of concurrent requests
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents during evaluation
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - Concurrent request wait timeout (ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - Max tokens multiplier for reasoning models
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - Max characters for conversation history
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - Max history messages for intent detection
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - Max history chars for intent detection
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - Max chars for assistant messages
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - Max chars for assistant summary
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - Max chars for doc description in evaluation
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - Enable AI mode functionality
     - ``false``
     - fess_config.properties

Per-Prompt-Type Settings
========================

In |Fess|, individual parameters can be configured per prompt type. Configure in ``fess_config.properties``.

Configuration Pattern
---------------------

Per-prompt-type settings are specified using the following pattern:

- ``rag.llm.openai.{promptType}.temperature`` - Generation randomness (0.0 to 2.0). Ignored for reasoning models (o1/o3/o4/gpt-5 series)
- ``rag.llm.openai.{promptType}.max.tokens`` - Maximum number of tokens
- ``rag.llm.openai.{promptType}.context.max.chars`` - Maximum number of context characters (default: ``16000`` for answer/summary, ``10000`` for others)

Prompt Types
------------

Available prompt types:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Prompt Type
     - Description
   * - ``intent``
     - Prompt for determining user intent
   * - ``evaluation``
     - Prompt for evaluating search result relevance
   * - ``unclear``
     - Response prompt for unclear queries
   * - ``noresults``
     - Response prompt when no search results are found
   * - ``docnotfound``
     - Response prompt when documents are not found
   * - ``answer``
     - Prompt for generating answers
   * - ``summary``
     - Prompt for generating summaries
   * - ``faq``
     - Prompt for generating FAQs
   * - ``direct``
     - Prompt for direct responses
   * - ``queryregeneration``
     - Query regeneration prompt

Default Values
--------------

Default values for each prompt type. Temperature settings are ignored for reasoning models (o1/o3/o4/gpt-5 series).

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Prompt Type
     - Temperature
     - Max Tokens
     - Notes
   * - ``intent``
     - 0.1
     - 256
     - Deterministic intent detection
   * - ``evaluation``
     - 0.1
     - 256
     - Deterministic relevance evaluation
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
     - Main answer generation
   * - ``summary``
     - 0.3
     - 2048
     - Summary generation
   * - ``queryregeneration``
     - 0.3
     - 256
     - Query regeneration

Configuration Examples
----------------------

::

    # Temperature setting for answer prompt
    rag.llm.openai.answer.temperature=0.7

    # Maximum tokens for answer prompt
    rag.llm.openai.answer.max.tokens=2048

    # Temperature setting for summary prompt (set lower for summaries)
    rag.llm.openai.summary.temperature=0.3

    # Temperature setting for intent prompt (set lower for intent analysis)
    rag.llm.openai.intent.temperature=0.1

Reasoning Model Support
=======================

When using reasoning models such as o1/o3/o4 series or gpt-5 series, |Fess| automatically uses the OpenAI API ``max_completion_tokens`` parameter instead of ``max_tokens``. No additional configuration changes are required.

.. note::
   Reasoning models (o1/o3/o4/gpt-5 series) ignore the ``temperature`` setting and use a fixed value (1). Also, when using reasoning models, the default ``max_tokens`` is multiplied by ``reasoning.token.multiplier`` (default: 4).

Additional Parameters for Reasoning Models
-------------------------------------------

When using reasoning models, the following additional parameters can be configured in ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - Reasoning effort setting for o-series models (``low``, ``medium``, ``high``)
     - ``low`` (intent/evaluation/docnotfound/unclear/noresults/queryregeneration), not set (others)
   * - ``rag.llm.openai.{promptType}.top.p``
     - Token selection probability threshold (0.0 to 1.0)
     - (Not set)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - Frequency penalty (-2.0 to 2.0)
     - (Not set)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - Presence penalty (-2.0 to 2.0)
     - (Not set)

``{promptType}`` can be ``intent``, ``evaluation``, ``answer``, ``summary``, etc.

Configuration Examples
----------------------

::

    # Set reasoning effort to high for o3-mini
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # Set top_p and penalties for gpt-5
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

Configuration via JVM Options
=============================

For security reasons, it is recommended to configure API keys via the runtime
environment (JVM options) rather than checked-in files.

Docker Environment
------------------

The official `docker-fess <https://github.com/codelibs/docker-fess>`__ repository
ships an OpenAI overlay (``compose-openai.yaml``). The minimum steps are:

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

The contents of ``compose-openai.yaml`` (use as a reference if you build your own equivalent):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Notes:

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` makes the container's ``run.sh`` download and install the plugin into ``app/WEB-INF/plugin/`` automatically
- ``-Dfess.config.rag.chat.enabled=true`` enables AI mode
- ``-Dfess.config.rag.llm.openai.api.key=...`` sets the API key, ``-Dfess.config.rag.llm.openai.model=...`` selects the model
- ``-Dfess.system.rag.llm.name=openai`` only acts as the initial default before a value is persisted in OpenSearch. After startup you can also change it from Administration > System > General (RAG section)

If outbound Internet access goes through a proxy, append
``-Dhttps.proxyHost=... -Dhttps.proxyPort=...`` to ``FESS_JAVA_OPTS``.

systemd Environment
-------------------

Append to ``FESS_JAVA_OPTS`` in ``/etc/sysconfig/fess`` (or ``/etc/default/fess``):

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

Using Azure OpenAI
==================

When using OpenAI models via Microsoft Azure, change the API endpoint.

::

    # Azure OpenAI endpoint
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Azure API key
    rag.llm.openai.api.key=your-azure-api-key

    # Deployment name (specified as model name)
    rag.llm.openai.model=your-deployment-name

.. note::
   When using Azure OpenAI, the API request format may differ slightly.
   Please refer to Azure OpenAI documentation for details.

Model Selection Guide
=====================

Guidelines for selecting models based on intended use.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Model
     - Cost
     - Quality
     - Use Case
   * - ``gpt-5-mini``
     - Medium
     - High
     - Balanced use cases (recommended)
   * - ``gpt-4o-mini``
     - Low-Medium
     - High
     - Cost-focused use cases
   * - ``gpt-5``
     - High
     - Highest
     - Complex reasoning, when high quality is needed
   * - ``gpt-4o``
     - Medium-High
     - Highest
     - When multimodal support is needed
   * - ``o3-mini`` / ``o4-mini``
     - Medium
     - Highest
     - Reasoning tasks such as math and coding

Cost Reference
--------------

OpenAI API is billed based on usage.

.. note::
   For the latest pricing, see `OpenAI Pricing <https://openai.com/pricing>`__.

Concurrency Control
===================

In |Fess|, the number of concurrent requests to the OpenAI API can be controlled with ``rag.llm.openai.max.concurrent.requests`` in ``fess_config.properties``. The default value is ``5``.

::

    # Set maximum concurrent requests
    rag.llm.openai.max.concurrent.requests=5

This setting prevents excessive requests to the OpenAI API and helps avoid rate limit errors.

OpenAI Tier-based Limits
------------------------

Limits vary based on your OpenAI account tier:

- **Free**: 3 RPM (requests/minute)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: Higher limits

Adjust ``rag.llm.openai.max.concurrent.requests`` appropriately based on your OpenAI account tier.

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: "401 Unauthorized" error occurs

**Check the following**:

1. Verify API key is correctly configured
2. Verify API key is valid (check in OpenAI dashboard)
3. Verify API key has necessary permissions

Rate Limit Errors
-----------------

**Symptom**: "429 Too Many Requests" error occurs

**Solutions**:

1. Reduce the value of ``rag.llm.openai.max.concurrent.requests``::

    rag.llm.openai.max.concurrent.requests=3

2. Upgrade your OpenAI account tier

Quota Exceeded
--------------

**Symptom**: "You exceeded your current quota" error

**Solutions**:

1. Check usage in OpenAI dashboard
2. Review billing settings and increase limits if necessary

Timeout
-------

**Symptom**: Requests time out

**Solutions**:

1. Extend timeout duration::

    rag.llm.openai.timeout=180000

2. Consider using a faster model (e.g., gpt-5-mini)

Debug Settings
--------------

When investigating issues, adjust |Fess| log levels to output detailed OpenAI-related logs.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

Security Notes
==============

When using OpenAI API, please note the following security considerations.

1. **Data Privacy**: Search result contents are sent to OpenAI servers
2. **API Key Management**: Key leakage can lead to unauthorized use
3. **Compliance**: If handling confidential data, verify your organization's policies
4. **Usage Policy**: Comply with OpenAI's terms of service

References
==========

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - LLM Integration Overview
- :doc:`rag-chat` - AI Mode Details
