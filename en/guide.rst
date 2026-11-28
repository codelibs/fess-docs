===============
Practical Guide
===============

Putting Knowledge to Work with Fess
===================================

This practical guide shows how to make your organization's information searchable with Fess and grow it into a search platform that people keep using.
Each article targets Fess 15.9 and explains in concrete terms the fields on the settings screens, the configuration keys, and how to confirm that things worked.
Features that are only available in 15.10 or later are explicitly marked as such in the articles.

Choose by Goal
==============

- **I want to try Fess first**: :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **I want to search file servers**: :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **I want to search cloud and SaaS data**: :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **I want to embed search in an existing site or system**: :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **I want to show different information to each department or user**: :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **I want to enhance search with AI**: :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **I am starting production operation**: :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

Getting Started
===============

- :doc:`articles/guide-01` - How Fess is structured, how work is divided between Fess and its plugins, and reading paths by goal
- :doc:`articles/guide-02` - Start Fess with Docker Compose and try everything from crawling to searching

Collecting Information
======================

- :doc:`articles/guide-04` - Crawl websites and file servers, and let users narrow results with labels
- :doc:`articles/datastore-basics` - Data store plugin settings, permissions, labels, schedules, and how to check the results
- :doc:`articles/guide-07` - Make files in Google Drive, SharePoint Online / OneDrive, and Box searchable
- :doc:`articles/guide-06` - Make Git repositories, Confluence, Jira, and Slack searchable
- :doc:`articles/guide-12` - Make data in databases, CSV files, and Salesforce searchable

Embedding Search and Changing Its Look
======================================

- :doc:`articles/guide-03` - Place a search box on an existing site and adjust the look of the search page with themes
- :doc:`articles/guide-11` - Search and register documents from business systems with the search API and access tokens

Controlling Access
==================

- :doc:`articles/guide-05` - Show different search results by role and group, and integrate with LDAP / Active Directory
- :doc:`articles/guide-15` - Introduce SSO (OIDC / SAML / Entra ID / SPNEGO) and protect access from outside
- :doc:`articles/guide-13` - Share a single Fess among multiple organizations with virtual hosts and roles

Improving Search Quality
========================

- :doc:`articles/guide-08` - Find problems in the search log analysis screens and fix them with synonyms and Key Match
- :doc:`articles/guide-09` - Understand how multilingual documents are indexed and searched, and tune each language
- :doc:`articles/guide-22` - Aggregate and visualize search logs your own way with OpenSearch Dashboards

Operations
==========

- :doc:`articles/guide-10` - Health checks, logs, notifications, backup and restore, and handling failure URLs
- :doc:`articles/guide-16` - Manage settings as code with fessctl and the admin API, and reproduce environments
- :doc:`articles/guide-14` - Memory settings, an external OpenSearch cluster, and running Fess on multiple servers
- :doc:`articles/guide-17` - Add features by writing your own data store plugins and ingesters

Enhancing Search with AI
========================

- :doc:`articles/guide-18` - Use vector search and rank fusion so that documents are found even when worded differently
- :doc:`articles/guide-19` - Connect an LLM and use AI search mode, which answers based on internal documents
- :doc:`articles/guide-20` - Let AI agents search Fess through the MCP server plugin
- :doc:`articles/guide-21` - Build multimodal search that searches images and text together

Planning a Company-Wide Rollout
===============================

- :doc:`articles/guide-23` - What to configure and check at each stage, from introduction to company-wide rollout

Use Cases and Comparisons
=========================

- :doc:`articles/use-cases` - Use cases by industry and scale, and the articles that help with each
- :doc:`articles/comparison` - How Fess compares with other search solutions (OpenSearch alone, Solr, commercial products, and others)
- :doc:`articles/file-server-search` - What to check before introducing full-text search for file servers

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
