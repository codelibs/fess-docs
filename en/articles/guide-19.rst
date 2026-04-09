============================================================
Part 19: Building an Internal AI Assistant -- A Search-Based Q&A System Powered by RAG
============================================================

Introduction
============

In the previous article, we organized the concepts of semantic search.
In this article, as an evolution of that approach, we build an internal AI assistant using RAG (Retrieval-Augmented Generation).

RAG is a mechanism that "finds relevant documents through search, and then an LLM (Large Language Model) generates answers based on their content."
Because answers are generated based on internal documents, RAG can handle company-specific questions that a general-purpose chat AI cannot answer.

Target Audience
===============

- Those interested in building an internal AI assistant
- Those who want to learn how to implement RAG
- Those who want to understand the options for LLM integration

How RAG Works
=============

RAG Pipeline
------------

Fess's AI search mode operates through the following pipeline:

1. **Intent Analysis (Intent)**: Analyzes the user's question and classifies intent (search, summarization, FAQ, ambiguous)
2. **Search**: Retrieves relevant documents from Fess's index (automatically regenerates queries and re-searches on zero hits)
3. **Evaluate**: The LLM evaluates the relevance of retrieved documents
4. **Full-Text Fetch**: Retrieves the full text of highly relevant documents
5. **Answer Generation (Answer)**: The LLM generates a streaming response with citations based on document content

This pipeline mitigates "plausible but inaccurate responses (hallucinations)" from the LLM and provides answers backed by internal documents.

Fess's AI search mode does not require vector search (embedding models).
It leverages existing full-text search indexes as-is, with the LLM handling search result evaluation and answer generation.
This means you can introduce RAG-based AI search immediately, without additional infrastructure preparation such as selecting embedding models or building vector databases.

Choosing an LLM Provider
=========================

Fess supports three LLM backends.
Below is a summary of each provider's characteristics and selection criteria.

.. list-table:: LLM Provider Comparison
   :header-rows: 1
   :widths: 15 25 25 35

   * - Provider
     - Plugin
     - Cost
     - Characteristics
   * - OpenAI
     - fess-llm-openai
     - Pay-per-use API
     - High answer quality, GPT-4o support, easy to get started
   * - Google Gemini
     - fess-llm-gemini
     - Pay-per-use API
     - Extended thinking support, long context
   * - Ollama
     - fess-llm-ollama
     - Hardware costs
     - Local execution, data stays internal, privacy-focused

Selection Criteria
------------------

**When to choose a Cloud API (OpenAI / Gemini)**

- You want to minimize initial costs
- You cannot prepare a GPU server
- You prioritize answer quality above all
- Sending data externally is acceptable

**When to choose Local Execution (Ollama)**

- Sending internal data externally is not permitted
- Security and privacy requirements are strict
- You can prepare a GPU server
- You want to reduce running costs (for high-volume usage)

Setting Up AI Search Mode
=========================

Installing the Plugin
---------------------

Install the plugin corresponding to your chosen LLM provider.

1. Go to [System] > [Plugins] in the admin console
2. Install the corresponding plugin (e.g., ``fess-llm-openai``)

Enabling AI Search Mode
-----------------------

Enable AI search mode in Fess's settings.

Set ``rag.chat.enabled=true`` in the admin console settings or the configuration file.

LLM Connection Settings
-----------------------

Configure the connection information for your chosen LLM provider.

**For OpenAI**

- API key
- Model to use (gpt-4o, gpt-4o-mini, etc.)
- Maximum token count

**For Ollama**

- Ollama server URL
- Model name to use
- Adding a service via Docker Compose

.. code-block:: yaml

    services:
      ollama:
        image: ollama/ollama
        volumes:
          - ollama-data:/root/.ollama
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

The AI Chat Experience
======================

Chat UI
-------

When AI search mode is enabled, AI search mode is added to the Fess search screen.
Users can switch between keyword search and AI chat.

Question and Answer Example
---------------------------

**Question**: "How do I apply for paid leave?"

**AI Response**:

    To apply for paid leave, follow these steps:

    1. Access the "Attendance Management" page on the internal portal
    2. Select "Paid Leave" from the "Leave Request" menu
    3. Enter the dates, select your manager, and submit the request

    Please submit your request at least 3 business days before the leave date.

    Reference: [Employment Regulations, Article 15](https://portal/rules/chapter15.html)

The response includes source links, allowing users to verify the original documents.

Using the Chat API (SSE)
========================

To use AI search mode from a program, use the Chat API.
The Chat API returns streaming responses via Server-Sent Events (SSE).

For streaming responses (SSE):

::

    GET /api/v1/chat/stream?message=How to apply for paid leave

For non-streaming JSON responses:

::

    POST /api/v1/chat
    Content-Type: application/x-www-form-urlencoded

    message=How to apply for paid leave

With SSE, responses are sent to the client in real time as they are generated.
Users can start reading the progressively displayed response without waiting for the full answer to be generated.

Conversation History
--------------------

The Chat API supports session-based conversation history.
Follow-up questions based on the context of previous questions are possible.

Example:

- Q1: "How do I apply for paid leave?"
- A1: (Response as above)
- Q2: "What should I do if I miss the application deadline?"
- A2: (Response based on the context of Q1)

Tuning RAG
==========

Improving Answer Quality
------------------------

RAG answer quality is influenced by the following factors:

**Search Quality**

Since RAG generates answers based on search results, search quality directly affects answer quality.
Improving search quality through the tuning cycle described in Part 8 also leads to improved RAG quality.

**Document Quality**

If the documents being searched are outdated, inaccurate, or ambiguous, RAG answer quality will also decline.
Regular updates and quality management of documents are important.

**Prompt Settings**

Tuning the prompts (instruction text) sent to the LLM allows you to adjust the style and accuracy of responses.

Safety Considerations
=====================

Prompt Injection Countermeasures
--------------------------------

Fess's RAG feature has built-in prompt injection defenses.
It protects against attacks that attempt to manipulate LLM behavior through malicious inputs.

Preventing Information Leakage
------------------------------

Since RAG generates answers based on search results, combining it with role-based search (Part 5) ensures that only answers appropriate to the user's permissions are generated.
Content from documents the user is not authorized to access is not included in RAG responses.

Summary
=======

In this article, we explained how to build an internal AI assistant using Fess's AI search mode.

- How the RAG pipeline works (intent analysis -> search -> evaluation -> answer generation)
- Selection criteria for three LLM providers (OpenAI, Gemini, Ollama)
- Setting up and experiencing AI search mode
- Using the Chat API (SSE) from programs
- Tuning answer quality and safety considerations

With an AI assistant based on internal documents, knowledge utilization shifts from "searching" to "asking."

In the next article, we will cover how to integrate Fess as an MCP server into AI agents.

References
==========

- `Fess AI Search Mode Settings <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Fess Chat API <https://fess.codelibs.org/ja/15.5/api/api-chat.html>`__
