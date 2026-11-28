====================================================
Answers from Internal Documents with AI Search (RAG)
====================================================

Introduction
============

Instead of opening search results one by one and comparing them, people often want to ask a question such as "When is the deadline for expense reports?" and get an answer based on internal documents.
The AI search mode of Fess (RAG chat) has Fess itself search for documents related to the question, passes their content to an LLM (large language model) to generate an answer, and returns that answer together with links to the documents it was based on.

This article covers running AI search mode on Fess 15.9, restricting who can use it and which documents it refers to, and checking that it works on the search page and through the API.
After following the steps in this article, you will be able to:

- Choose one of four LLM providers and install the matching plugin and settings
- Connect an LLM to Fess on Docker using the overlay Compose files provided by docker-fess
- Restrict which users can use the chat and which documents answers are based on
- Confirm that it works on the search page, through ``/api/v2/chat``, and in the search log

As a prerequisite, Fess must be running and documents must already be crawled.
If not, prepare them by following the steps in :doc:`guide-02`.
Semantic search, which finds documents with similar meaning, is covered in :doc:`guide-18`, and MCP, which lets AI agents search Fess, is covered in :doc:`guide-20`.

How AI Search Mode Works
========================

AI search mode does not use a dedicated vector index.
It finds documents with the same search processing as ordinary search (keyword search by default), so you can start without preparing an embedding model or chunking.
If semantic search is enabled, it is automatically included in AI search mode's searches as well.

The processing flow depends on the endpoint being called.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Endpoint
     - Processing flow
   * - ``POST /api/v2/chat/stream`` (used by AI search on the search page)
     - Intent detection → search → relevance evaluation by the LLM → fetching document content → answer generation. The progress of each stage and the answer fragments are returned in order as Server-Sent Events
   * - ``POST /api/v2/chat``
     - Intent detection → search → answer generation. There is no relevance evaluation, and the result is returned as a single JSON

In both cases, when a search returns no results, the LLM rewrites the search terms and searches again (up to 2 times by default, ``rag.chat.query.regeneration.max.count``).
Because a single question calls the LLM several times, responses take longer than an ordinary search, and with a cloud LLM each call is billed.

The user's question and the content or excerpts of the documents found by the search are sent to the LLM.
When choosing a provider, check where this data is sent.

Conversations are identified by ``session_id`` and kept in Fess's memory.
By default, a conversation is discarded after 30 minutes of inactivity (``rag.chat.session.timeout.minutes``), and up to 30 messages are kept per conversation (``rag.chat.history.max.messages``).
Conversations are also lost when Fess restarts.

Choosing an LLM Provider
========================

In Fess 15.9, the connection to an LLM is provided by a ``fess-llm-*`` plugin for each provider.
The provider to use is specified with ``rag.llm.name``.

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - Provider
     - ``rag.llm.name``
     - Plugin
     - Default model
     - Settings required to connect, and where questions and documents are sent
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url`` (default ``http://localhost:11434``). Data is sent to the Ollama server you run yourself
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``. Data is sent to OpenAI
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``. Data is sent to Google
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region`` (default ``us-east-1``), plus ``rag.llm.bedrock.api.key`` or AWS credentials. Data is sent to Amazon Bedrock in the specified region

The model can be changed with ``rag.llm.<provider>.model``.

With OpenAI and Gemini, all you need to get started is an API key, but questions and documents are sent to the respective service.
Ollama keeps questions and documents within your own servers, but you need a server to run the model.
The docker-fess Compose file for Ollama assumes an NVIDIA GPU.
Bedrock requires AWS credentials and a region setting.
For how to configure it, see `Amazon Bedrock Configuration <https://fess.codelibs.org/stable/config/llm-bedrock.html>`__.

Three Things to Configure
=========================

AI search mode works only when the following three are all in place.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Setting
     - Where to set it
     - How to pass it on Docker
   * - ``rag.chat.enabled=true`` (default ``false``)
     - ``fess_config.properties``. There is no field for it in the admin console
     - ``-Dfess.config.rag.chat.enabled=true`` in ``FESS_JAVA_OPTS``
   * - A ``fess-llm-*`` plugin
     - [System] > [Plugin], or ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0`` and so on
   * - ``rag.llm.name`` and the connection settings for each provider
     - ``rag.llm.name`` in [System] > [General]; the connection settings (``rag.llm.<provider>.*``) in ``fess_config.properties``
     - ``-Dfess.system.rag.llm.name=openai``, ``-Dfess.config.rag.llm.openai.api.key=...`` and so on

The default value of ``rag.llm.name`` is ``ollama``.
If you install only the OpenAI plugin and leave ``rag.llm.name`` unchanged, Fess keeps looking for an Ollama client that does not exist, and AI search mode cannot be used.
In that case, the warning ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` appears in the log.

``-Dfess.system.rag.llm.name`` is an initial value used only when ``system.properties`` has no value.
Once a value saved under [General] is written to ``system.properties``, that value takes precedence.

Running on Docker (OpenAI and Gemini)
=====================================

docker-fess provides overlay Compose files for connecting an LLM.
In the directory where you placed the Compose files in :doc:`guide-02`, download the v15.9.0 file.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

Put the API key in a shell environment variable and start with the three files specified.

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` adds the following environment variables to ``fess01``.
The API key and model name are taken from the shell's ``OPENAI_API_KEY`` and ``OPENAI_MODEL`` (``gpt-5-mini`` if unset), so you do not need to write the key in the file.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Plugins in ``FESS_PLUGINS`` are installed when the container starts, before Fess itself, so no separate restart is needed.
If ``fess01`` is already running, this command recreates ``fess01``, and any settings you changed under [General] are lost along with the container.
Specify the same three files for subsequent commands such as ``ps``, ``logs`` and ``down`` as well.

For Gemini, download ``compose-gemini.yaml``, set ``GEMINI_API_KEY``, and specify it as the third file in the same way.
This file sets the model from ``GEMINI_MODEL`` (``gemini-2.5-flash`` if unset), so ``gemini-2.5-flash`` is used instead of the plugin's default model.

.. note::

   If you specify two or more overlay files that set ``FESS_JAVA_OPTS`` (for example, when combining with settings for OCR), only the value from the last file is used.
   In that case, prepare your own Compose file that combines all the required ``-D`` options into a single ``FESS_JAVA_OPTS``.
   ``FESS_JAVA_OPTS`` is split on whitespace, so options whose values contain spaces cannot be written there.

An API key passed as in ``-Dfess.config.rag.llm.openai.api.key`` is shown masked under [System Info] > [Config Info].
If you need to go out through an internal proxy, add ``-Dfess.config.http.proxy.host=...`` and ``-Dfess.config.http.proxy.port=...``.
LLM plugins use Fess's common proxy settings.

Running on Docker (Ollama)
==========================

``compose-ollama.yaml`` adds an Ollama container, ``ollama01``, and connects ``fess01`` to it.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Target
     - What is configured
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``, ``-Dfess.config.rag.chat.enabled=true``, ``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - Image ``ollama/ollama:latest``, network ``search_net``, port 11434, volume ``ollama-data``, and one NVIDIA GPU assigned

``rag.llm.name`` and the model are not set, so the default values ``ollama`` and ``gemma4:e4b`` are used.
The URL points to ``ollama01`` because the default ``http://localhost:11434`` would refer to the ``fess01`` container itself.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

This file requires an environment with the NVIDIA Container Toolkit installed.
To try it in an environment without a GPU, delete the ``deploy:`` section of ``ollama01`` from the downloaded file.
It then runs on the CPU, so answers take time.

Fess considers Ollama available only when the configured model is in Ollama's model list (``/api/tags``), and it performs this check every 60 seconds by default.
For this reason, AI search mode becomes available about a minute after you pull the model.
The comments at the top of the file mention a different file name and steps for pulling ``gpt-oss:20b``, but follow the steps above.
To use a different model, ``ollama pull`` that model and add ``-Dfess.config.rag.llm.ollama.model=<model-name>`` to ``FESS_JAVA_OPTS``.

Configuring Without Docker (ZIP, RPM and DEB)
=============================================

1. Install the plugin. Select it from [System] > [Plugin] > [Install], or install it with a command

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. Add the settings to ``fess_config.properties``. It is ``app/WEB-INF/classes/fess_config.properties`` for the ZIP package and ``/etc/fess/fess_config.properties`` for the RPM/DEB packages

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. Restart Fess. Both the plugin and the changes to ``fess_config.properties`` are loaded on restart
4. Open [System] > [General], select ``openai`` for "LLM Provider" in the "AI Search" section, and click [Update]

The "AI Search" section is shown only when ``rag.chat.enabled=true`` and at least one LLM plugin is loaded.
The choices for "LLM Provider" are limited to the providers of the installed plugins.
If you cannot find the section, review steps 1 to 3.

Checking That It Works
======================

Checking on the Search Page
---------------------------

1. Open ``http://localhost:8080/``. [AI Search] with a robot icon appears in the navigation bar at the top
2. Click [AI Search] to open the chat page (``/chat``)
3. Enter a question that the crawled documents are likely to answer. If you crawled the Search Guide in :doc:`guide-02`, you can try something like "What symbols can I use in wildcard searches?"

While the answer is being generated, the stages Intent, Search, Evaluate, Fetch and Answer are shown in turn.
Below the answer, the documents it was based on are listed with numbers under "Sources", corresponding to numbers such as ``[1]`` in the answer text.
When you change the topic, click [New chat] to clear the conversation history.

If [AI Search] is not shown, check "Common Pitfalls" below.

Checking Through the API
------------------------

To check without using the page, call ``/api/v2/ui/config``.
If ``response.features.rag_chat_enabled`` is ``true``, that user can use AI search mode.

State-changing requests such as ``/api/v2/chat`` must send a CSRF token bound to the session in the ``X-Fess-CSRF-Token`` header.
The response from ``/api/v2/ui/config`` contains the token, so obtain it while saving cookies, and make the call with the same cookies (the example uses ``jq``).

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"What symbols can I use in wildcard searches?"}' | jq '.response'

In the response, ``content`` is the answer, ``sources`` lists the documents it was based on (``rank``, ``title``, ``url`` and so on), and ``session_id`` is the conversation ID.
To ask a follow-up question, send the ``session_id`` back, as in ``{"message":"...","session_id":"<previous session_id>"}``.

This example calls the API as an anonymous user who is not logged in, so only documents with ``{role}guest`` are searched.
For how to call it as a logged-in user, the events of the streaming ``/api/v2/chat/stream``, and the error codes, see `Chat API <https://fess.codelibs.org/stable/api/api-chat.html>`__ and `API Overview <https://fess.codelibs.org/stable/api/api-overview.html>`__.
``/api/v1/chat`` is a legacy API that is available only when the ``fess-webapp-v1-api`` plugin is installed.
Use ``/api/v2/chat`` for new integrations.

Checking in the Admin Console and Logs
--------------------------------------

The [AI Chat] tab under [System Info] > [Search Log] shows the number of requests, number of users, total tokens, average response time and error rate, along with counts per user, per intent and per model.
This logging is enabled by ``rag.chat.log.enabled`` (default ``true``), and the text of questions and answers is not recorded.
Token counts are recorded only when the LLM plugin reports them.

On Docker, you can check whether the plugin was installed in the container log.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

If ``Installing fess-llm-openai-15.9.0.jar`` appears, the plugin is installed.
If ``[LLM] LlmClient not found`` keeps appearing, ``rag.llm.name`` does not match the installed plugin.

Restricting Users and Referenced Documents
==========================================

AI search mode's searches are filtered by role in the same way as ordinary search.
Documents a user cannot see in search results are used neither as the basis of answers nor as sources.
Which documents each user can see is determined by "Permissions" in the crawl configuration.
For the design approach, see :doc:`guide-05`.

On top of that, you can restrict the use of the chat itself in the "AI Search" section of [System] > [General].

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Description
   * - "Chat Permissions" (``rag.chat.permissions``)
     - Specifies the users who can use the chat as a comma-separated list such as ``{role}rag_user,{group}sales,{user}taro``. If empty, everyone can use it. To let users who are not logged in use it as well, include ``{role}guest``
   * - "Chat Labels" (``rag.chat.labels``)
     - Limits the documents answers are based on to those with any of the specified label values. Specify them as a comma-separated list such as ``faq,policy``; if empty, all documents the user can see are used

Users not covered by "Chat Permissions" do not see [AI Search], and the API returns 401 if they are not logged in, or 403 if they are logged in.
Logged-in users do not have ``{role}guest``, so if you specify only ``{role}guest``, logged-in users can no longer use the chat.
If you save a value with no valid entries (such as ``{role}`` alone), no one can use the chat.

"Chat Labels" is useful when you want answers to come only from documents you trust as a basis for answers, such as internal policies and FAQs, which you have labeled in advance.
For how to create and assign labels, see :doc:`guide-04`.

Common Pitfalls
===============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptom
     - What to check
   * - [AI Search] is not shown
     - Check in this order. (1) Is ``rag.chat.enabled=true`` being passed? (2) Is the plugin installed (``Installing`` in the log)? (3) Does ``rag.llm.name`` match the installed plugin (the ``LlmClient not found`` warning)? (4) Is the API key non-empty, and for Ollama, have you pulled the model? (5) Are you excluded by "Chat Permissions"?
   * - There is no "AI Search" section under [General]
     - Either ``rag.chat.enabled`` is still ``false`` or no LLM plugin is loaded. Check that you restarted Fess after configuring the setting and installing the plugin
   * - "LLM Provider" reverted after ``down`` and ``up -d``
     - The values under [General] are saved in ``system.properties`` inside the ``fess01`` container, so they are lost when the container is recreated. Specify it with ``-Dfess.system.rag.llm.name`` in ``FESS_JAVA_OPTS``
   * - The API returns ``403``
     - Check that you send the CSRF token in ``X-Fess-CSRF-Token`` and that you send the cookies from when you obtained the token. A logged-in user excluded by "Chat Permissions" also gets 403
   * - The API returns ``429``
     - Each user is limited to 30 requests per minute (``api.chat.rate.limit.per.user.per.minute``)
   * - Cannot connect to a cloud LLM
     - Check that the container can reach the outside network, and if a proxy is required, set ``http.proxy.host`` and ``http.proxy.port``

To improve the quality of answers, first check the quality of search.
AI search mode bases its answers on the top-ranked documents of an ordinary search (5 by default, ``rag.chat.context.max.documents``), so if searching with the words of the question brings unrelated documents to the top, the answer is pulled along by them as well.
Improving search is covered in :doc:`guide-08`.
For temperature and maximum tokens per prompt type, and for replacing prompts, see `AI Search (RAG) and LLM Integration Overview <https://fess.codelibs.org/stable/config/llm-overview.html>`__.

What to Read Next
=================

- Add documents with similar meaning to search results even when keywords do not match: :doc:`guide-18`
- Let AI agents such as Claude search Fess: :doc:`guide-20`
- Separate searchable documents by department or role: :doc:`guide-05`
- Improve search quality by looking at the search log: :doc:`guide-08`
- Have users log in with SSO and show different documents to each user: :doc:`guide-15`

References
==========

- `AI Mode Configuration <https://fess.codelibs.org/stable/config/rag-chat.html>`__
- `AI Search (RAG) and LLM Integration Overview <https://fess.codelibs.org/stable/config/llm-overview.html>`__
- `Ollama Configuration <https://fess.codelibs.org/stable/config/llm-ollama.html>`__
- `OpenAI Configuration <https://fess.codelibs.org/stable/config/llm-openai.html>`__
- `Google Gemini Configuration <https://fess.codelibs.org/stable/config/llm-gemini.html>`__
- `Amazon Bedrock Configuration <https://fess.codelibs.org/stable/config/llm-bedrock.html>`__
- `Chat API <https://fess.codelibs.org/stable/api/api-chat.html>`__
- `AI Search Mode (for users) <https://fess.codelibs.org/stable/user/chat-search.html>`__
- `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `compose directory of docker-fess (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
