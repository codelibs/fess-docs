============================================================
Part 20: Connecting AI Agents with Search -- Integrating Fess into External AI Tools via MCP Server
============================================================

Introduction
============

In the previous article, we built an AI assistant using Fess's built-in AI search mode.
However, that is not the only way to leverage AI.
There is a method to use Fess as a "search tool" from Claude Desktop and other AI agents.

In this article, we will set up Fess as an MCP (Model Context Protocol) server and build an environment where external AI tools can seamlessly search internal documents.

Target Audience
===============

- Those interested in integrating AI agents with search systems
- Those who want to understand the concept of MCP
- Those using AI tools such as Claude Desktop in their business operations

What is MCP?
============

MCP (Model Context Protocol) is a protocol that enables AI applications to access external data sources and tools.
It allows AI models to perform operations such as "search," "read a file," and "call an API" in a standardized way.

By exposing Fess as an MCP server, AI agents can execute operations like "search internal documents" in a natural context.

A Paradigm Shift
-----------------

Traditional search followed the model of "a human enters keywords and reads the results."
With MCP, a new model is realized: "an AI agent autonomously searches, interprets the results, and incorporates them into its answers."

This is a shift from "humans search" to "AI searches on behalf of humans."

Building the Fess MCP Server
==============================

Installing the Plugin
------------------------

The MCP server functionality for Fess is provided as a webapp plugin.

1. In the admin panel, go to [System] > [Plugins]
2. Install ``fess-webapp-mcp``
3. Restart Fess

Features Provided by the MCP Server
-------------------------------------

The Fess MCP server provides the following features to AI agents.

**Tools**

- **search**: Full-text search of internal documents
- **get_index_stats**: Retrieval of index document count and JVM memory information

AI agents can call these tools to search the Fess index or check system status.

**Resources**

- **fess://index/stats**: Index statistics (document count, configuration information, JVM memory)

**Prompts**

- **basic_search**: Generation of basic search queries
- **advanced_search**: Generation of detailed search queries including sort order and result count

Integration with Claude Desktop
=================================

Configuring Claude Desktop
----------------------------

To connect the Fess MCP server to Claude Desktop, add the MCP server information to the Claude Desktop configuration file.

Add the following configuration to the configuration file (claude_desktop_config.json).

.. code-block:: json

    {
      "mcpServers": {
        "fess": {
          "url": "http://localhost:8080/mcp"
        }
      }
    }

Usage Examples
--------------

Once Fess is connected as an MCP server in Claude Desktop, interactions like the following become possible.

**Example 1: Searching Internal Documents**

    User: "Please tell me about the business trip expense reimbursement procedure."

    Claude: (Calls Fess's search tool)
    I searched the internal documents regarding business trip expense reimbursement.
    The procedure for expense reimbursement is as follows:
    1. Create a business trip report...
    [From the Travel Expense Reimbursement Manual (portal/manual/travel-expense.html)]

**Example 2: Cross-Document Research**

    User: "Please summarize the password-related provisions in our security policy."

    Claude: (Searches Fess for "password security policy" and integrates multiple results)
    Password-related provisions are documented in the following documents:
    - Information Security Basic Policy: Passwords must be at least 12 characters...
    - Account Management Regulations: Must be changed every 90 days...
    - Remote Access Regulations: Multi-factor authentication is mandatory...

AI agents interpret the search results and generate answers that integrate information from multiple documents.

Integration with Other AI Tools
=================================

Since MCP is a standard protocol, Fess can be used from MCP-compatible AI tools other than Claude Desktop.

Using from Custom AI Agents
-----------------------------

It is also possible to connect to Fess via the MCP protocol from internally developed AI agents.
You can call Fess's search functionality programmatically using MCP client libraries.

Security Considerations
========================

Here are security considerations when exposing the MCP server.

Access Control
--------------

- Restrict access to the MCP server to trusted clients only
- Network-level restrictions (firewall, VPN)
- Authentication via API tokens

Search Result Permission Control
----------------------------------

Role-based search in Fess (covered in Part 5) also applies to searches via MCP.
By associating roles with API tokens, you can control the scope of documents that AI agents can retrieve.

Data Handling
----------------

When integrating with cloud-based AI services, be aware that search result text is sent externally.
If highly confidential documents are included, consider combining with a local LLM (Ollama) or filtering search results.

Summary
========

In this article, we explained how to expose Fess as an MCP server and integrate it with AI agents.

- The concept of the MCP protocol and the "AI searches" paradigm
- Installation and configuration of the fess-webapp-mcp plugin
- Examples of integration with Claude Desktop
- Security considerations (access control, permissions, data handling)

By enabling AI agents to directly access internal knowledge, the possibilities for knowledge utilization expand significantly.

In the next article, we will cover multimodal search.

References
==========

- `Fess MCP Server <https://github.com/codelibs/fess-webapp-mcp>`__

- `Model Context Protocol <https://modelcontextprotocol.io/>`__
