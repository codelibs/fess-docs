==========================
AI Chat Search
==========================

Overview
========

The AI chat search feature in |Fess| allows you to search for information through natural conversational interaction,
in addition to traditional keyword search. When you enter a question, the AI assistant analyzes
the search results and generates easy-to-understand answers.

Features of AI Chat Search
==========================

Conversational Search
---------------------

Instead of thinking of keywords, you can ask questions as you would in normal conversation.

Examples:

- "How do I install Fess?"
- "How can I crawl files?"
- "What should I do if search results don't appear?"

Context-Aware Answers
---------------------

The AI assistant understands the intent of your questions and compiles related information into answers.
It extracts and organizes necessary information from multiple search results.

Source Citation
---------------

AI responses clearly cite the sources (reference documents).
When you want to verify the accuracy of an answer, you can directly refer to the original documents.

Conversation Continuation
-------------------------

You're not limited to a single question; you can continue the conversation.
You can ask additional questions based on the context of previous questions and answers.

How to Use Chat Search
======================

Starting a Chat
---------------

1. Access the |Fess| search screen
2. Click the chat icon at the bottom right of the screen
3. The chat panel will be displayed

Entering a Question
-------------------

1. Enter your question in the text box
2. Click the send button or press Enter
3. The AI assistant will generate an answer

.. note::
   Generating an answer may take a few seconds.
   During processing, the current phase (searching, analyzing, etc.) is displayed.

Reviewing the Answer
--------------------

The AI assistant's answer will be displayed. Answers include the following information:

- **Answer Body**: Detailed answer to your question
- **Sources**: Links to the source documents (in the format [1], [2], etc.)

Click on source links to view the original documents.

Continuing the Conversation
---------------------------

If you have additional questions, you can continue to ask:

- "Please tell me more details"
- "Are there other methods?"
- "More about [topic]"

The AI assistant will respond considering the context of the previous conversation.

Starting a New Conversation
---------------------------

If you want to ask about a different topic, click the "New Chat" button.
This clears the conversation history and starts a new conversation.

Tips for Effective Questions
============================

Be Specific
-----------

Specific questions yield more appropriate answers than vague ones.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Vague Question
     - Specific Question
   * - How do I configure it?
     - How do I change memory settings in Fess?
   * - I'm getting an error
     - I'm getting an "index not found" error when searching
   * - About crawling
     - How do I set up exclusions when crawling websites?

Include Background Information
------------------------------

Including context and purpose helps get more appropriate answers.

Good examples:

- "I'm running Fess in a Docker environment. How do I change the log storage location?"
- "I'm using Fess for the first time. What should I do first?"

Ask Step by Step
----------------

Complex issues become easier to understand when asked step by step.

1. "Can Fess crawl file shares?"
2. "How do I connect using the SMB protocol?"
3. "What should I do for shared folders that require authentication?"

Frequently Asked Questions
==========================

Q: The chat feature doesn't appear
----------------------------------

A: The chat feature may not be enabled.
Please check with your system administrator whether the AI mode feature is enabled.

Q: It takes a long time for answers to appear
---------------------------------------------

A: Since the AI analyzes search results and generates answers, it may take a few to several seconds.
During processing, the current phase ("Searching", "Analyzing", "Generating response", etc.) is displayed.

Q: The answer sources seem incorrect
------------------------------------

A: Click the source link to check the original document.
While the AI generates answers based on search results, interpretations may sometimes be incorrect.
For important information, we recommend verifying with the original documents.

Q: It seems to have forgotten the previous conversation
-------------------------------------------------------

A: The session may have timed out.
After a certain period of inactivity, the conversation history is cleared.
Please start a new conversation.

Q: I can't get an answer for a specific question
------------------------------------------------

A: The following possibilities exist:

- There is no related information in the documents being searched
- The question is too vague to search properly
- Rate limits have been reached

Try rephrasing your question or wait a moment before trying again.

Q: Can I ask questions in languages other than English?
-------------------------------------------------------

A: Yes, depending on the configuration, you can often ask questions in other languages.
The AI recognizes the language of the question and attempts to respond in the same language.

Notes
=====

About AI Responses
------------------

- AI responses are generated based on search results
- Accuracy of responses is not guaranteed
- For important decisions, always verify with the original documents
- Check official documentation for the latest information

About Privacy
-------------

- Your questions are used for search and AI processing
- Conversation history is deleted after the session ends
- Logs may be recorded depending on system configuration

References
==========

- :doc:`search-and` - How to Use AND Search
- :doc:`search-not` - How to Use NOT Search
- :doc:`search-field` - How to Use Field Search
- :doc:`advanced-search` - Advanced Search Features
