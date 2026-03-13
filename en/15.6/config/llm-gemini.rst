==========================
Google Gemini Configuration
==========================

Overview
========

Google Gemini is a state-of-the-art Large Language Model (LLM) provided by Google.
|Fess| can use the Google AI API (Generative Language API) to implement AI mode functionality with Gemini models.

Using Gemini enables high-quality response generation leveraging Google's latest AI technology.

Key Features
------------

- **Multimodal Support**: Can process not only text but also images
- **Long Context**: Long context window capable of processing large amounts of documents at once
- **Cost Efficiency**: Flash models are fast and low-cost
- **Google Integration**: Easy integration with Google Cloud services

Supported Models
----------------

Main models available with Gemini:

- ``gemini-3-flash-preview`` - Latest fast model (recommended)
- ``gemini-3.1-pro-preview`` - Latest high reasoning model
- ``gemini-2.5-flash`` - Stable fast model
- ``gemini-2.5-pro`` - Stable high reasoning model

.. note::
   For the latest information on available models, see `Google AI for Developers <https://ai.google.dev/models/gemini>`__.

Prerequisites
=============

Before using Gemini, prepare the following.

1. **Google Account**: A Google account is required
2. **Google AI Studio Access**: Access `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **API Key**: Generate an API key in Google AI Studio

Obtaining an API Key
--------------------

1. Access `Google AI Studio <https://aistudio.google.com/>`__
2. Click "Get API key"
3. Select "Create API key"
4. Select an existing project or create a new one
5. Securely save the generated API key

.. warning::
   API keys are confidential information. Please note the following:

   - Do not commit to version control systems
   - Do not output to logs
   - Manage using environment variables or secure configuration files

Plugin Installation
===================

In |Fess| 15.6, Gemini integration is provided as the ``fess-llm-gemini`` plugin.
To use Gemini, you must install the plugin.

1. Download `fess-llm-gemini-15.6.0.jar`
2. Place it in the ``app/WEB-INF/plugin/`` directory of |Fess|
3. Restart |Fess|

::

    # Example of placing the plugin
    cp fess-llm-gemini-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   The plugin version should match the version of |Fess|.

Basic Configuration
===================

In |Fess| 15.6, enabling AI mode functionality and Gemini-specific settings are done in ``fess_config.properties``, while selecting the LLM provider is done from the administration screen or in ``system.properties``.

fess_config.properties Settings
--------------------------------

Add the AI mode enable setting and Gemini-specific settings to ``app/WEB-INF/conf/fess_config.properties``.

Minimal Configuration (fess_config.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Gemini API key
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model to use
    rag.llm.gemini.model=gemini-3-flash-preview

Recommended Configuration (Production, fess_config.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Gemini API key
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model setting (use fast model)
    rag.llm.gemini.model=gemini-3-flash-preview

    # API endpoint (usually no change needed)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Timeout setting
    rag.llm.gemini.timeout=60000

LLM Provider Settings
---------------------

The LLM provider is configured from the administration screen (Administration > System > General) or in ``system.properties``.

::

    # Set LLM provider to Gemini
    rag.llm.name=gemini

Configuration Options
=====================

All configuration options available for the Gemini client. All settings except ``rag.llm.name`` are configured in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.gemini.api.key``
     - Google AI API key
     - (Required)
   * - ``rag.llm.gemini.model``
     - Model name to use
     - ``gemini-3-flash-preview``
   * - ``rag.llm.gemini.api.url``
     - API base URL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Request timeout (in milliseconds)
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - Availability check interval (in seconds)
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - Maximum number of concurrent requests
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents during evaluation
     - ``3``

Per-Prompt-Type Settings
========================

In |Fess|, LLM parameters can be configured in detail per prompt type.
Configure per-prompt-type settings in ``fess_config.properties``.

Configuration Format
--------------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.context.max.chars

Available Prompt Types
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Prompt Type
     - Description
   * - ``intent``
     - Prompt for determining user intent
   * - ``evaluation``
     - Prompt for evaluating document relevance
   * - ``unclear``
     - Prompt for when the question is unclear
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

Configuration Examples
----------------------

::

    # Temperature setting for answer generation
    rag.llm.gemini.answer.temperature=0.7

    # Maximum tokens for summary generation
    rag.llm.gemini.summary.max.tokens=2048

    # Maximum context characters for answer generation
    rag.llm.gemini.answer.context.max.chars=16000

    # Maximum context characters for summary generation
    rag.llm.gemini.summary.context.max.chars=16000

    # Maximum context characters for FAQ generation
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   The default value of ``context.max.chars`` varies by prompt type.
   ``answer`` and ``summary`` are 16000, and ``faq`` is 10000.

Thinking Model Support
======================

Gemini supports thinking models. Using a thinking model, the model executes an internal reasoning process before generating a response, enabling more accurate answers.

The thinking budget can be configured in ``fess_config.properties``.

::

    # Thinking budget configuration
    rag.llm.gemini.thinkingConfig.thinkingBudget=1024

.. note::
   Setting a thinking budget may increase response time.
   Set an appropriate value based on your use case.

Environment Variable Configuration
===================================

For security reasons, it is recommended to configure API keys using environment variables.

Docker Environment
------------------

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

systemd Environment
-------------------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

Using via Vertex AI
===================

If you are using Google Cloud Platform, you can also use Gemini via Vertex AI.
When using Vertex AI, the API endpoint and authentication method differ.

.. note::
   The current version of |Fess| uses the Google AI API (generativelanguage.googleapis.com).
   If you need to use Vertex AI, custom implementation may be required.

Model Selection Guide
=====================

Guidelines for selecting models based on intended use.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Model
     - Speed
     - Quality
     - Use Case
   * - ``gemini-3-flash-preview``
     - Fast
     - Highest
     - General use (recommended)
   * - ``gemini-3.1-pro-preview``
     - Medium
     - Highest
     - Complex reasoning
   * - ``gemini-2.5-flash``
     - Fast
     - High
     - Stable version, cost-focused
   * - ``gemini-2.5-pro``
     - Medium
     - High
     - Stable version, long context

Context Window
--------------

Gemini models support very long context windows:

- **Gemini 3 Flash / 2.5 Flash**: Up to 1 million tokens
- **Gemini 3.1 Pro / 2.5 Pro**: Up to 1 million tokens (3.1 Pro) / 2 million tokens (2.5 Pro)

You can leverage this feature to include more search results in the context.

::

    # Include more documents in context (configure in fess_config.properties)
    rag.llm.gemini.answer.context.max.chars=20000

Cost Reference
--------------

Google AI API is billed based on usage (free tier available).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Model
     - Input (per 1M characters)
     - Output (per 1M characters)
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
   For the latest pricing and free tier information, see `Google AI Pricing <https://ai.google.dev/pricing>`__.

Concurrency Control
===================

In |Fess|, the number of concurrent requests to Gemini can be controlled.
Configure the following property in ``fess_config.properties``.

::

    # Maximum concurrent requests (default: 5)
    rag.llm.gemini.max.concurrent.requests=5

This setting prevents excessive requests to the Google AI API and helps avoid rate limit errors.

Free Tier Limits (Reference)
-----------------------------

Google AI API has a free tier with the following limits:

- Requests/minute: 15 RPM
- Tokens/minute: 1 million TPM
- Requests/day: 1,500 RPD

When using the free tier, it is recommended to set ``rag.llm.gemini.max.concurrent.requests`` to a lower value.

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: API key-related errors occur

**Check the following**:

1. Verify API key is correctly configured
2. Verify API key is valid in Google AI Studio
3. Verify API key has necessary permissions
4. Verify the API is enabled for the project

Rate Limit Errors
-----------------

**Symptom**: "429 Resource has been exhausted" error occurs

**Solutions**:

1. Reduce the number of concurrent requests in ``fess_config.properties``::

    rag.llm.gemini.max.concurrent.requests=3

2. Wait a few minutes before retrying
3. Request quota increase if necessary

Region Restrictions
-------------------

**Symptom**: Service unavailable error

**Check the following**:

Google AI API is only available in certain regions. Please check
Google's documentation for supported regions.

Timeout
-------

**Symptom**: Requests time out

**Solutions**:

1. Extend timeout duration::

    rag.llm.gemini.timeout=120000

2. Consider using Flash models (faster)

Debug Settings
--------------

When investigating issues, adjust |Fess| log levels to output detailed Gemini-related logs.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

Security Notes
==============

When using Google AI API, please note the following security considerations.

1. **Data Privacy**: Search result contents are sent to Google servers
2. **API Key Management**: Key leakage can lead to unauthorized use
3. **Compliance**: If handling confidential data, verify your organization's policies
4. **Terms of Service**: Comply with Google's Terms of Service and Acceptable Use Policy

References
==========

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - LLM Integration Overview
- :doc:`rag-chat` - AI Mode Details
