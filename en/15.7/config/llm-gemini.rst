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

- ``gemini-3.1-flash-lite-preview`` - Lightweight, low-cost fast model (default)
- ``gemini-3-flash-preview`` - Standard Flash model
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - High reasoning models
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
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

Recommended Configuration (Production, fess_config.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Gemini API key
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model setting (use fast model)
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

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
     - Google AI API key (must be set to use the Gemini API)
     - ``""``
   * - ``rag.llm.gemini.model``
     - Model name to use
     - ``gemini-3.1-flash-lite-preview``
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
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - Maximum characters for document description during evaluation
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - Concurrent request wait timeout (milliseconds)
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - Maximum characters for chat history
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - Maximum history messages for intent determination
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - Maximum history characters for intent determination
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - Maximum characters for assistant history
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - Maximum characters for assistant summary history
     - ``1000``
   * - ``rag.llm.gemini.retry.max``
     - Maximum number of HTTP retries (on ``429`` and ``5xx`` errors)
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - Base delay for exponential backoff (in milliseconds)
     - ``2000``

Authentication
==============

Since |Fess| 15.6.1, the API key is sent in the ``x-goog-api-key`` HTTP request header (Google's recommended method).
It is no longer appended to the URL as a ``?key=...`` query parameter, so the API key will not appear in access logs.

Retry Behavior
==============

Requests to the Gemini API are automatically retried on the following HTTP status codes:

- ``429`` Resource Exhausted (quota exceeded / rate limit)
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Retries wait using exponential backoff (base ``rag.llm.gemini.retry.base.delay.ms`` milliseconds, up to ``rag.llm.gemini.retry.max`` attempts, with a jitter of +/-20%).
For streaming requests, only the initial connection is eligible for retry; any error that occurs after the response body has started streaming is propagated immediately.

Per-Prompt-Type Settings
========================

In |Fess|, LLM parameters can be configured in detail per prompt type.
Configure per-prompt-type settings in ``fess_config.properties``.

Configuration Format
--------------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
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
   * - ``queryregeneration``
     - Query regeneration prompt

Prompt Type Default Values
------------------------------

Default values for each prompt type. These values are used when not explicitly configured.

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - Prompt Type
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``512``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - ``0``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``0``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

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
   ``answer`` and ``summary`` are 16000, ``faq`` is 10000, and other prompt types are 10000.

Thinking Model Support
======================

Gemini supports thinking models. Using a thinking model, the model executes an internal reasoning process before generating a response, enabling more accurate answers.

The thinking budget is configured per prompt type in ``fess_config.properties``. At request time, |Fess| automatically converts the integer value (token count) of ``rag.llm.gemini.{promptType}.thinking.budget`` into the appropriate API field for the resolved model generation.

::

    # Thinking budget for answer generation
    rag.llm.gemini.answer.thinking.budget=1024

    # Thinking budget for summary generation
    rag.llm.gemini.summary.thinking.budget=1024

Mapping by Model Generation
---------------------------

- **Gemini 2.x** (e.g. ``gemini-2.5-flash``): the configured integer is sent as-is in ``thinkingConfig.thinkingBudget``. Setting ``0`` disables thinking entirely.
- **Gemini 3.x** (e.g. ``gemini-3.1-flash-lite-preview``): the integer is bucketed into one of the ``thinkingConfig.thinkingLevel`` enum values (``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH``).

The bucket mapping for Gemini 3.x is as follows:

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Budget value
     - thinkingLevel
     - Notes
   * - ``<=0``
     - ``MINIMAL`` or ``LOW``
     - ``MINIMAL`` on Flash / Flash-Lite models, ``LOW`` on Pro-class models that do not support ``MINIMAL`` (``gemini-3-pro`` / ``gemini-3.1-pro``)
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x always consumes some thinking tokens regardless of the bucket (``thinkingLevel=MINIMAL`` may still consume several hundred tokens).
   For this reason, |Fess| automatically adds extra headroom (1024 tokens) on top of the default ``maxOutputTokens`` when a Gemini 3.x model is in use, to prevent answer truncation due to ``finishReason=MAX_TOKENS``.
   With Gemini 2.x, ``thinkingBudget=0`` disables thinking entirely, so no headroom is added.

.. note::
   Setting a large thinking budget may increase response time.
   Set an appropriate value based on your use case.

Configuration via JVM Options
=============================

For security reasons, it is recommended to configure API keys via the runtime
environment (JVM options) rather than checked-in files.

Docker Environment
------------------

The official `docker-fess <https://github.com/codelibs/docker-fess>`__ repository
ships a Gemini overlay (``compose-gemini.yaml``). The minimum steps are:

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

The contents of ``compose-gemini.yaml`` (use as a reference if you build your own equivalent):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

Notes:

- ``FESS_PLUGINS=fess-llm-gemini:15.6.0`` makes the container's ``run.sh`` download and install the plugin into ``app/WEB-INF/plugin/`` automatically
- ``-Dfess.config.rag.chat.enabled=true`` enables AI mode
- ``-Dfess.config.rag.llm.gemini.api.key=...`` sets the API key, ``-Dfess.config.rag.llm.gemini.model=...`` selects the model
- ``-Dfess.system.rag.llm.name=gemini`` only acts as the initial default before a value is persisted in OpenSearch. After startup you can also change it from Administration > System > General (RAG section)

If outbound Internet access goes through a proxy, configure |Fess|'s ``http.proxy.*`` settings via ``FESS_JAVA_OPTS`` (see "Using HTTP Proxy" below).

systemd Environment
-------------------

Append to ``FESS_JAVA_OPTS`` in ``/etc/sysconfig/fess`` (or ``/etc/default/fess``):

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

Using HTTP Proxy
================

Since |Fess| 15.6.1, the Gemini client shares the |Fess|-wide HTTP proxy configuration. Configure the following properties in ``fess_config.properties``.

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

In Docker environments, specify them via ``FESS_JAVA_OPTS`` like so::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   This configuration also affects |Fess|-wide HTTP access (such as the crawler).
   The legacy Java system properties (``-Dhttps.proxyHost`` and friends) are no longer consulted by the Gemini client.

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
   * - ``gemini-3.1-flash-lite-preview``
     - Fast
     - High
     - Lightweight, low cost (default; supports ``thinkingLevel=MINIMAL``)
   * - ``gemini-3-flash-preview``
     - Fast
     - Highest
     - General use (supports ``thinkingLevel=MINIMAL``)
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - Medium
     - Highest
     - Complex reasoning (does not support ``MINIMAL``; minimum is ``LOW``)
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
