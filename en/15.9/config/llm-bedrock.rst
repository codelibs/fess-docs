==============================================
Amazon Bedrock Configuration (AI Search / RAG)
==============================================

Overview
========

This page explains how to configure the ``fess-llm-bedrock`` plugin so |Fess| can use Amazon Bedrock for its **AI search mode (RAG: Retrieval-Augmented Generation)** and as the embedding provider for content chunks.

Amazon Bedrock is the AWS service that provides foundation models from Amazon and other model providers through one API.
The plugin calls the Bedrock Runtime API in the AWS region you choose:

- **AI search mode**: the Converse API (``ConverseStream`` for streamed answers)
- **Content chunk embedding**: the InvokeModel API with Amazon Titan Text Embeddings V2 or Cohere Embed

Supported Models
----------------

AI search mode works with any model that supports the Converse API in your region.
The default is Amazon Nova 2 Lite through the US cross-region inference profile, ``us.amazon.nova-2-lite-v1:0``.
``rag.llm.bedrock.model`` accepts a model ID, an inference profile ID (for example with the ``us.``, ``eu.`` or ``global.`` prefix) or an ARN.

Content chunk embedding supports the following models.

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - Model
     - ``content_chunker.embedding.dimension``
     - Texts per request
   * - ``amazon.titan-embed-text-v2:0``
     - ``256``, ``512`` or ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - up to 96, each at most 2048 characters
   * - ``cohere.embed-v4:0`` (also through an inference profile)
     - ``256``, ``512``, ``1024`` or ``1536``
     - up to 96

The embedding model is recognized by the base model name inside the configured ID: a base model ID, a cross-region inference profile ID (``us.``, ``eu.``, ``global.`` ...), or an ARN that contains one of those.
Application inference profiles have opaque IDs and are not recognized.

.. note::
   For the models available in each region, see `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__.

Prerequisites
=============

1. **AWS account** with Amazon Bedrock available in the region you use
2. **Model access**: the models you configure must be usable from your account in that region
3. **Credentials**: either a Bedrock API key, or AWS credentials allowed to call the models (see :ref:`bedrock-authentication`)

Plugin Installation
===================

Bedrock integration is provided as the ``fess-llm-bedrock`` plugin.
Install it from "System" > "Plugins" in the administration screen, or place the JAR file manually and restart |Fess|.

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   The plugin version should match the version of |Fess|.

Basic Configuration
===================

The LLM provider (``rag.llm.name``) is selected from the administration screen (Administration > System > General) or in ``system.properties``.
Enabling AI search mode and the ``rag.llm.bedrock.*`` settings go in ``fess_config.properties``.

``system.properties`` (also configurable from Administration > System > General):

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` for package installations), with AWS credentials:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

With a Bedrock API key instead of AWS credentials:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

Configuration Options
=====================

All options of the AI search mode client. They are configured in ``fess_config.properties`` (or as ``-Dfess.config.<key>`` JVM options).

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``rag.llm.bedrock.api.key``
     - Bedrock API key. When empty, requests are signed with AWS credentials (SigV4)
     - ``""``
   * - ``rag.llm.bedrock.region``
     - AWS region of the Bedrock Runtime endpoint and of the SigV4 signature
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - Endpoint URL, for example a VPC interface endpoint. When empty, ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - Model ID, inference profile ID or ARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - Request timeout (in milliseconds)
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - Availability check interval (in seconds)
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - ``false`` stops ``temperature`` from being sent, for models or modes that reject it
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - JSON object sent as ``additionalModelRequestFields`` for model-specific parameters
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - Maximum number of concurrent requests
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - Concurrent request wait timeout (milliseconds)
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - Maximum characters of retrieved context for answer generation
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - Maximum characters of the document for summary generation
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - Maximum characters of retrieved context for FAQ generation
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - Maximum number of relevant documents during evaluation
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - Maximum characters for document description during evaluation
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - Maximum characters for chat history
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - Maximum history messages for intent determination
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - Maximum history characters for intent determination
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - Maximum characters for assistant history
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - Maximum characters for assistant summary history
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - Maximum number of HTTP attempts (on ``429``, ``500``, ``502``, ``503`` and ``504``)
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - Base delay for exponential backoff (in milliseconds)
     - ``2000``

.. _bedrock-authentication:

Authentication
==============

API key
-------

When ``rag.llm.bedrock.api.key`` is set, it is sent as ``Authorization: Bearer <key>``.
Short-term Bedrock API keys expire and are valid only in the region they were created in; long-term keys are tied to an IAM user.
The value is masked in Administration > System Info when it is set in ``fess_config.properties`` (or, for ``content_chunker.embedding.bedrock.api.key``, in ``system.properties``).
Environment variables and JVM system properties, ``-Dfess.config.*`` and ``-Dfess.system.*`` options included, are listed there unmasked, so do not pass the key that way.

AWS credentials (SigV4)
-----------------------

When no API key is set, every request is signed with AWS Signature Version 4.
Credentials are taken from the first of these sources that provides them:

1. the ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken`` JVM system properties
2. the ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN`` environment variables
3. web identity (``AWS_WEB_IDENTITY_TOKEN_FILE`` and ``AWS_ROLE_ARN``, as used on Amazon EKS)
4. the shared ``~/.aws/credentials`` and ``~/.aws/config`` files (``AWS_PROFILE`` selects the profile)
5. the container credentials endpoint (Amazon ECS)
6. the EC2 instance metadata service (instance profile)

The JVM system properties (source 1) reach only the |Fess| web process.
Content chunk (document) embedding runs in a separate child JVM, so for it use environment variables, a shared credentials profile or an IAM role, or repeat the ``-Daws.*`` options in ``jvm.chunk.options``.

The region always comes from ``rag.llm.bedrock.region``; ``AWS_REGION`` is not read.
Profiles that use IAM Identity Center (SSO) are not supported.

.. warning::
   Prefer an IAM role (EC2 instance profile, ECS task role, EKS web identity) or the shared credentials file of the user that runs |Fess|.
   Environment variables and JVM system properties are listed unmasked under Administration > System Info, so keep long-lived keys out of them.

The IAM principal needs ``bedrock:InvokeModel`` (Converse and InvokeModel) and ``bedrock:InvokeModelWithResponseStream`` (ConverseStream) on the models it uses.
When the model is an inference profile, allow both the inference profile and the foundation models it routes to.

Retry Behavior
==============

Requests are retried on ``429``, ``500``, ``502``, ``503`` and ``504``, and when the connection to Bedrock could not be established.
Retries wait with exponential backoff (base ``rag.llm.bedrock.retry.base.delay.ms``, +/-20% jitter, up to ``rag.llm.bedrock.retry.max`` attempts); a ``Retry-After`` header takes precedence.
For streaming requests, only the initial request is retried; an error after the answer has started streaming, including an exception event inside the stream, ends the request.

Per-Prompt-Type Settings
========================

``temperature`` and ``max.tokens`` can be set per prompt type, as for the other providers:

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` is one of ``intent``, ``evaluation``, ``unclear``, ``noresults``, ``docnotfound``, ``direct``, ``faq``, ``answer``, ``summary`` and ``queryregeneration``.
A per-prompt-type ``additional.model.request.fields`` replaces the global value for that prompt type.

Default values used when nothing is configured:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Prompt Type
     - temperature
     - max.tokens
   * - ``intent``, ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear``, ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct``, ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   ``rag.llm.bedrock.{promptType}.thinking.budget`` is not supported: reasoning settings differ per model on Bedrock.
   A configured value is not sent and a WARN is logged. Use ``additional.model.request.fields`` instead.

Model-Specific Parameters
=========================

``additional.model.request.fields`` passes a JSON object to the model as is.
A value that is not a JSON object is not sent, and a WARN naming the property is logged.

For example, to use extended thinking of an Anthropic Claude model only for answer generation:

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

Claude rejects ``temperature`` while thinking is enabled, and ``max.tokens`` must be larger than ``budget_tokens``.
Reasoning text is never shown to users; only the answer text is.

Content Chunk Embedding
=======================

To use Bedrock for content chunk embedding, set the following in ``app/WEB-INF/conf/system.properties`` (``/etc/fess/system.properties`` on the RPM/DEB packages, ``/opt/fess/system.properties`` on Docker), or as ``-Dfess.system.<key>`` options.
Unlike ``rag.llm.bedrock.*``, these keys are not read from ``fess_config.properties``.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Property
     - Description
     - Default
   * - ``content_chunker.embedding.bedrock.api.key``
     - Bedrock API key. When empty, AWS credentials are used
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - AWS region
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - Endpoint URL. When empty, derived from the region
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - Embedding model (see `Supported Models`_)
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - Titan only: whether vectors are normalized
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - Cohere only: ``truncate`` (``NONE``/``START``/``END`` for v3, ``NONE``/``LEFT``/``RIGHT`` for v4). Not sent when empty
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - Request timeout (in milliseconds)
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - Connection timeout (in milliseconds)
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - Availability check interval (in seconds)
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - Maximum number of HTTP attempts (on ``429``, ``500``, ``502``, ``503`` and ``504``)
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - Base delay for exponential backoff (in milliseconds)
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - Upper bound of one backoff wait, ``Retry-After`` included (in milliseconds)
     - ``60000``

``content_chunker.embedding.dimension`` must be a size the model produces (see `Supported Models`_); otherwise the embedding provider is reported as unavailable with an ERROR log.
Documents are embedded with Cohere's ``input_type=search_document`` and queries with ``search_query``.
Cohere Embed v3 accepts at most 2048 characters per text. Bedrock rejects a longer text with ``400 ValidationException`` whatever ``truncate`` says, and the plugin does not shorten or split texts.
``truncate`` (``END`` when not set) applies only to a text within 2048 characters that exceeds 512 tokens.

Using HTTP Proxy
================

Requests to Bedrock use the |Fess|-wide HTTP proxy configuration (``http.proxy.host``, ``http.proxy.port``, ``http.proxy.username`` and ``http.proxy.password`` in ``fess_config.properties``).
Credential lookups that call AWS endpoints (STS for web identity, the container credentials endpoint, the instance metadata service) do not use these settings.
To reach Bedrock through a VPC interface endpoint, set ``rag.llm.bedrock.endpoint`` (and ``content_chunker.embedding.bedrock.endpoint``) to its URL; the region setting still selects the signing region.

Troubleshooting
===============

AI search mode is not available
-------------------------------

The client reports itself available when the model and region are set, the endpoint is a valid URL, and either an API key is set or AWS credentials can be resolved.
An invalid region or endpoint is logged at ERROR. To see why credentials could not be resolved, enable DEBUG for ``org.codelibs.fess.llm.bedrock``.
A failed credential lookup is remembered for 60 seconds, so credentials made available later are picked up within a minute.

Access denied
-------------

A ``403`` with ``type=AccessDeniedException`` in the WARN log means the API key or the IAM principal is not allowed to invoke the model.
Check the IAM permissions above, and that the model can be used from your account in the configured region.

Validation errors
-----------------

A ``400`` with ``type=ValidationException`` usually means the model ID is not available in the region (for some models only an inference profile ID can be used) or that ``additional.model.request.fields`` contains parameters the model does not accept.

Debug Settings
--------------

Enable DEBUG for ``org.codelibs.fess.llm.bedrock`` to log the request and response bodies of AI search mode, and the reason AWS credentials could not be resolved.
DEBUG for ``org.codelibs.fess.embedding.bedrock`` logs how query text was normalized and the same credential reason; it does not log embedding requests.
API keys, AWS credentials and signatures are never written by these loggers.

.. warning::
   Two other loggers write credentials at DEBUG: Apache HttpClient's wire logging writes the ``Authorization`` header, and the AWS SDK's signer (``software.amazon.awssdk.http.auth.aws.internal.signer``) writes the canonical request, including the ``x-amz-security-token`` of temporary credentials.
   Starting |Fess| with the root log level at DEBUG enables both; keep ``org.apache.hc`` and ``software.amazon.awssdk`` at INFO or above.

References
==========

- :doc:`llm-overview` - LLM Integration Overview
- :doc:`rag-chat` - AI Search Mode Details
- :doc:`search-semantic` - Semantic Search and Content Chunk Embedding
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
