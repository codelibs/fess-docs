==================
AI Search Mode
==================

Overview
==========

With the AI search mode feature (RAG chat) in |Fess|, you can look for information through natural
conversation, in addition to traditional keyword search. When you enter a question, the AI
assistant searches for relevant documents and generates an easy-to-understand answer based on
their content.

.. note::
   AI search mode is disabled by default. To use it, a system administrator must enable
   the feature and configure an LLM (Large Language Model) provider. For configuration
   instructions, see :doc:`../config/rag-chat` and :doc:`../config/llm-overview`.

Features of AI Search Mode
============================

Conversational Search
-----------------------

Instead of coming up with keywords, you can ask questions just as you would in everyday
conversation.

For example:

- "Tell me how to install Fess"
- "How do I crawl files?"
- "What should I do if no search results appear?"

Context-Aware Answers
-----------------------

The AI assistant analyzes the intent of your question, searches for relevant documents, and
extracts the necessary information from multiple search results to provide an organized answer.

Clearly Cited Sources
-----------------------

At the bottom of an answer, the documents that the answer was based on are listed as
"Sources". Each source is a numbered link, and clicking it lets you view the original
document directly. The answer body may also include citation numbers such as ``[1]``
and ``[2]``, which correspond to the numbers in the sources list.

Multi-Turn Conversations
--------------------------

You are not limited to a single question; you can keep the conversation going. The AI
assistant answers additional questions while taking the context of previous questions and
answers into account.

How to Use Chat Search
=========================

Opening AI Search Mode
------------------------

1. Open the |Fess| search screen
2. Click the "AI Search" link (robot icon) in the navigation bar at the top of the screen
3. The AI search mode screen is displayed

.. note::
   The "AI Search" link is displayed only when AI search mode is enabled and an LLM
   provider is available. If the link does not appear, see `Frequently Asked Questions`_.

Entering a Question
---------------------

1. Enter your question in the text box at the bottom of the screen (up to 4000 characters
   per question)
2. Click the "Send message" button (paper airplane icon), or press Enter
3. The AI assistant starts generating an answer

.. note::
   To insert a line break, press Shift+Enter instead of Enter, as indicated by the hint
   below the text box: "Press Enter to send, Shift+Enter for new line".

.. note::
   Generating an answer can take anywhere from a few seconds to over ten seconds. While
   processing, the current phase is shown in a progress indicator (Analyze → Search →
   Evaluate → Retrieve → Answer), along with messages such as "Thinking...",
   "Searching...", "Reviewing search results...", "Retrieving documents...", and
   "Generating answer...". Once the search is complete, the number of documents found is
   also displayed.

Reviewing the Answer
-----------------------

The AI assistant's answer is displayed. The answer includes the following information:

- **Answer body**: The answer to your question (formatted in Markdown)
- **Sources**: A numbered list of links to the documents the answer is based on (clicking a
  link opens the original document in a new tab)

The answer body may include citation numbers such as ``[1]`` and ``[2]``, which correspond
to the numbers in the sources list. Each answer has a copy button that lets you copy its
content to the clipboard.

.. note::
   The AI uses only the top documents it considers most relevant among the search results
   as the basis for its answer. As a result, the number of sources may be smaller than the
   number of documents that matched the search.

Narrowing Down Search Targets
-------------------------------

Depending on the topic, you can use the "Filter" button at the top of the screen to narrow
down the search target by criteria such as label, file type, last modified date, and size.
This is useful when you want to ask the AI about a specific set of documents only.

Continuing the Conversation
------------------------------

If you have additional questions, you can simply keep asking:

- "Could you explain in more detail?"
- "Are there other ways to do this?"
- "Tell me more about XX"

The AI assistant answers while taking the context of the previous conversation into account.

Starting a New Conversation
------------------------------

If you want to ask about a different topic, click the "New Chat" button (plus icon). This
clears the previous conversation history so you can start a new conversation.

Tips for Effective Questions
===============================

Be Specific
-------------

Specific questions get more appropriate answers than vague ones.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Vague Question
     - Specific Question
   * - How do I configure this?
     - How do I change the memory settings in Fess?
   * - I'm getting an error
     - I get an "index not found" error when searching
   * - About crawling
     - How do I configure exclusions when crawling a website?

Include Background Information
----------------------------------

Including your situation and purpose leads to more appropriate answers.

Good examples:

- "I'm running Fess in a Docker environment. I want to change where the logs are stored —
  how do I do that?"
- "This is my first time using Fess. What should I do first?"

Ask Questions Step by Step
------------------------------

Complex issues are easier to understand when you ask about them step by step.

1. "Can Fess crawl file shares?"
2. "How do I connect using the SMB protocol?"
3. "What should I do for shared folders that require authentication?"

Frequently Asked Questions
=============================

Q: AI Search Mode Doesn't Appear
-----------------------------------

A: AI search mode may not be enabled. The "AI Search" link is displayed only when the
feature is enabled (``rag.chat.enabled=true``) and an LLM provider (such as OpenAI, Gemini,
or Ollama) is configured and available. Ask your system administrator to check whether AI
search mode is enabled and whether the LLM provider is configured correctly (see
:doc:`../config/rag-chat` for details).

Q: It Takes a Long Time for the Answer to Appear
----------------------------------------------------

A: Since the AI analyzes your question, searches for and evaluates documents, and then
generates an answer, this can take anywhere from a few seconds to over ten seconds. While
processing, the current phase is displayed ("Thinking...", "Searching...", "Reviewing
search results...", "Retrieving documents...", "Generating answer...").

Q: The Sources Seem to Be Incorrect
---------------------------------------

A: Click the source links to check the original documents. The AI generates answers based
on search results, but its interpretation may occasionally be incorrect. We recommend
always verifying important information against the original documents.

Q: It Seems to Have Forgotten the Previous Conversation
-------------------------------------------------------------

A: The conversation session may have timed out. If there is no activity for a certain
period (30 minutes by default), the conversation history is cleared. In addition, since
the conversation history is temporarily kept in the server's memory, it is also lost if the
server restarts. If this happens, please start a new conversation.

.. note::
   The "session" mentioned here refers to the AI search mode's conversation session, which
   is separate from your |Fess| login session.

Q: I Can't Get an Answer to a Specific Question
-----------------------------------------------------

A: The following are possible causes:

- There is no relevant information in the documents being searched
- The question is too vague for the search to work properly
- A rate limit has been reached (the maximum number of requests per minute, or the maximum
  number of concurrent requests, has been exceeded)

Try rephrasing your question, or wait a while and try again.

Q: Is There a Limit on the Number of Characters I Can Enter?
--------------------------------------------------------------

A: You can enter up to 4000 characters per question. A character counter is displayed
below the text box, and it switches to a warning display as you approach the limit. If
your question is long, shorten it by focusing on the key points.

Q: Can I Ask Questions in Languages Other Than English?
---------------------------------------------------------

A: Yes, in most cases you can also ask questions in other languages. Based on your
browser's or the screen's display language, the AI tries to respond in the same language
whenever possible. However, this is a best-effort behavior, and in some cases the response
may not be in the language you intended.

Notes
=======

About AI Responses
--------------------

- AI responses are generated based on search results
- The accuracy of responses is not guaranteed
- For important decisions, always check the original documents (sources)
- For the latest information, refer to the official documentation

About Privacy
---------------

- The questions you enter are used for search and for AI processing by the configured LLM
  provider
- If the system is configured to use an external LLM service (such as OpenAI or Gemini),
  the content of your questions and the search results are sent to that service. If you
  want processing to stay entirely in-house, ask your administrator about using a locally
  running provider (such as Ollama)
- Conversation history is temporarily kept in the server's memory and is deleted when the
  session times out, when you click "New Chat", or when the server restarts
- As with regular search, role (permission) and label-based access control applies, so
  documents you are not permitted to view are not used as a basis for answers
- Depending on the system configuration, logs may be recorded

References
============

- :doc:`../config/rag-chat` - Configuring the AI search mode feature (for administrators)
- :doc:`../config/llm-overview` - Configuring LLM providers
- :doc:`../api/api-chat` - Chat API (for programmatic use)
- :doc:`search-and` - How to Use AND Search
- :doc:`search-not` - How to Use NOT Search
- :doc:`search-field` - How to Use Field Search
- :doc:`advanced-search` - Advanced Search Features
