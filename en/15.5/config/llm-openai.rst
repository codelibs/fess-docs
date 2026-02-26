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

- ``gpt-4o`` - High-performance multimodal model
- ``gpt-4o-mini`` - Lightweight version of GPT-4o (cost-efficient)
- ``o3-mini`` - Lightweight reasoning-focused model
- ``o4-mini`` - Next-generation lightweight reasoning model
- ``gpt-4-turbo`` - High-speed version of GPT-4
- ``gpt-3.5-turbo`` - Model with excellent cost performance

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

Basic Configuration
===================

Add the following settings to ``app/WEB-INF/conf/fess_config.properties``.

Minimal Configuration
---------------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Set LLM provider to OpenAI
    rag.llm.type=openai

    # OpenAI API key
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model to use
    rag.llm.openai.model=gpt-4o-mini

Recommended Configuration (Production)
--------------------------------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # LLM provider setting
    rag.llm.type=openai

    # OpenAI API key
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model setting (use high-performance model)
    rag.llm.openai.model=gpt-4o

    # API endpoint (usually no change needed)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Timeout setting
    rag.llm.openai.timeout=60000

Configuration Options
=====================

All configuration options available for the OpenAI client.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.openai.api.key``
     - OpenAI API key
     - (Required)
   * - ``rag.llm.openai.model``
     - Model name to use
     - ``gpt-4o-mini``
   * - ``rag.llm.openai.api.url``
     - API base URL
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - Request timeout (in milliseconds)
     - ``60000``

Environment Variable Configuration
==================================

For security reasons, it is recommended to configure API keys using environment variables.

Docker Environment
------------------

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

systemd Environment
-------------------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

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
   * - ``gpt-3.5-turbo``
     - Low
     - Good
     - General Q&A, cost-focused
   * - ``gpt-4o-mini``
     - Medium
     - High
     - Balanced use cases (recommended)
   * - ``gpt-4o``
     - High
     - Highest
     - Complex reasoning, when high quality is needed
   * - ``o3-mini`` / ``o4-mini``
     - Medium
     - Highest
     - Reasoning tasks such as math and coding
   * - ``gpt-4-turbo``
     - High
     - Highest
     - When fast response is needed

Cost Reference
--------------

OpenAI API is billed based on usage. The following are reference prices as of 2024.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Model
     - Input (per 1K tokens)
     - Output (per 1K tokens)
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
   For the latest pricing, see `OpenAI Pricing <https://openai.com/pricing>`__.

Rate Limiting
=============

OpenAI API has rate limits. Configure appropriately in combination with |Fess| rate limiting functionality.

::

    # Fess rate limit settings
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

OpenAI Tier-based Limits
------------------------

Limits vary based on your OpenAI account tier:

- **Free**: 3 RPM (requests/minute)
- **Tier 1**: 500 RPM
- **Tier 2**: 5,000 RPM
- **Tier 3+**: Higher limits

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

1. Set stricter rate limits in |Fess|::

    rag.chat.rate.limit.requests.per.minute=5

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

    rag.llm.openai.timeout=120000

2. Consider using a faster model (e.g., gpt-3.5-turbo)

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
