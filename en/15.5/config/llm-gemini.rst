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

- ``gemini-2.5-flash`` - Fast and efficient model (recommended)
- ``gemini-2.5-pro`` - Model with higher reasoning capabilities
- ``gemini-1.5-flash`` - Stable Flash model
- ``gemini-1.5-pro`` - Stable Pro model

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

Basic Configuration
===================

Add the following settings to ``app/WEB-INF/conf/fess_config.properties``.

Minimal Configuration
---------------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # Set LLM provider to Gemini
    rag.llm.type=gemini

    # Gemini API key
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model to use
    rag.llm.gemini.model=gemini-2.5-flash

Recommended Configuration (Production)
--------------------------------------

::

    # Enable AI mode functionality
    rag.chat.enabled=true

    # LLM provider setting
    rag.llm.type=gemini

    # Gemini API key
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Model setting (use fast model)
    rag.llm.gemini.model=gemini-2.5-flash

    # API endpoint (usually no change needed)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Timeout setting
    rag.llm.gemini.timeout=60000

Configuration Options
=====================

All configuration options available for the Gemini client.

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
     - ``gemini-2.5-flash``
   * - ``rag.llm.gemini.api.url``
     - API base URL
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Request timeout (in milliseconds)
     - ``60000``

Environment Variable Configuration
==================================

For security reasons, it is recommended to configure API keys using environment variables.

Docker Environment
------------------

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
   * - ``gemini-2.5-flash``
     - Fast
     - High
     - General use, balanced approach (recommended)
   * - ``gemini-2.5-pro``
     - Medium
     - Highest
     - Complex reasoning, when high quality is needed
   * - ``gemini-1.5-flash``
     - Fast
     - Good
     - Cost-focused, stability-focused
   * - ``gemini-1.5-pro``
     - Medium
     - High
     - When long context is needed

Context Window
--------------

Gemini models support very long context windows:

- **Gemini 1.5/2.5 Flash**: Up to 1 million tokens
- **Gemini 1.5/2.5 Pro**: Up to 2 million tokens

You can leverage this feature to include more search results in the context.

::

    # Include more documents in context
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

Cost Reference
--------------

Google AI API is billed based on usage (free tier available).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Model
     - Input (per 1M characters)
     - Output (per 1M characters)
   * - Gemini 1.5 Flash
     - $0.075
     - $0.30
   * - Gemini 1.5 Pro
     - $1.25
     - $5.00
   * - Gemini 2.5 Flash
     - Prices may vary
     - Prices may vary

.. note::
   For the latest pricing and free tier information, see `Google AI Pricing <https://ai.google.dev/pricing>`__.

Rate Limiting
=============

Google AI API has rate limits. Configure appropriately in combination with |Fess| rate limiting functionality.

::

    # Fess rate limit settings
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Free Tier Limits
----------------

Google AI API has a free tier with the following limits:

- Requests/minute: 15 RPM
- Tokens/minute: 1 million TPM
- Requests/day: 1,500 RPD

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

1. Set stricter rate limits in |Fess|::

    rag.chat.rate.limit.requests.per.minute=5

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
