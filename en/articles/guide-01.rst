========================================
What Fess Can Do and How to Introduce It
========================================

Introduction
============

Internal documents are spread across websites, file servers, cloud storage, SaaS tools such as chat and ticket tracking, and databases.
Even if each tool has its own search function, you cannot search across all of these places at once.
Fess is a search server that collects documents from these places into a single index so that they can be searched from one search page or API.

This article is intended for IT staff and developers who are considering introducing Fess, and explains the following:

- What Fess is made of and how it works
- Which features are available out of the box and which require additional plugins
- Which articles to read next, depending on your goal

The setup steps for each feature are covered in the individual articles.

Fess Version Covered by This Practical Guide
============================================

Every article in this Practical Guide targets Fess 15.9.
Screen field names, configuration keys, and default values have been checked against 15.9.
When an article introduces a feature that is only available in 15.10 or later, it says so explicitly.

Links to the reference documentation start with ``https://fess.codelibs.org/stable/`` and point to the documentation of the current stable release.
If you are using a different version, replace ``stable`` in the URL with the version number (for example, ``15.9``) and check the field names and default values on that page.

What Is Fess?
=============

Fess is an open source full-text search server written in Java.
It is licensed under the Apache License 2.0 and can be used free of charge, including in commercial environments.

Fess uses OpenSearch to store and search documents.
At startup, Fess 15.9 checks the OpenSearch it connects to and aborts startup unless it is OpenSearch 3 or later.
It cannot connect to OpenSearch 2 or earlier, or to Elasticsearch.
In 15.9, the search engine that used to be embedded in Fess has been removed, so you always need to provide OpenSearch separately (in the Docker setup, an OpenSearch container is started together with Fess).

A single Fess instance includes all of the following:

- Crawlers that collect documents (web, file servers, and various services via plugins)
- An admin console for configuring crawl settings, users, permissions, dictionaries, schedules, and more
- A search page for end users
- APIs (``/api/v2/``) for calling search and suggest from external systems

The search page is rendered by a static theme that bundles HTML, CSS, and JavaScript.
Fess ships with the ``bootstrap`` theme, and you can add other themes as ZIP files under [System] > [Theme].

How Fess Is Structured
======================

The components involved in running Fess are as follows.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Component
     - Role
   * - Fess itself (web application)
     - Provides the search page, the admin console, and the APIs. The scheduler also runs here and launches jobs such as crawls at the configured times
   * - Crawler (separate process)
     - Crawl jobs are launched as Java processes separate from Fess itself. They fetch web pages and files, extract their text, and register them in OpenSearch. The jobs that build suggestions, generate thumbnails, and create vectors for semantic search also run as separate processes in the same way
   * - OpenSearch
     - Holds the index of the documents to be searched and executes searches. Much of the information registered in the admin console, such as crawl settings, users, job logs, and search logs, is also stored here

Because the crawler is a separate Java process, its memory is configured separately from Fess itself (covered in :doc:`guide-14`).

The flow until documents become searchable is as follows:

1. Register a crawl configuration in the admin console (the target URLs or paths, the permissions that decide who can see the results, and so on)
2. The scheduler launches the crawl job. You can also launch it manually from the admin console with [Start Now]
3. The crawler fetches the documents, extracts their text, and registers them in OpenSearch together with their permissions
4. When a user searches, Fess filters the results by the user's roles and groups before returning them

You can try the whole sequence, from starting Fess with Docker through crawling to searching, in :doc:`guide-02`.

Core Features and Plugins
=========================

In Fess 15.9, many features are provided as plugins separate from Fess itself.
Whether the plugins you need are already installed depends on how you install Fess.

- Fess installed from ZIP, RPM, or DEB comes with no plugins at all
- The standard Docker image (for example, ``ghcr.io/codelibs/fess:15.9.0``) comes with the following seven plugins preinstalled: ``fess-script-groovy``, ``fess-storage-s3``, ``fess-storage-gcs``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``, ``fess-sso-oidc``
- The slim Docker image (for example, ``15.9.0-slim``) comes with no plugins

The following table lists the main features and the plugins they require.

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Feature
     - Available with Fess alone
     - Requires a plugin
   * - Crawling
     - Web (http and https), file systems, file servers (SMB), FTP
     - Amazon S3 (``fess-storage-s3``), Google Cloud Storage (``fess-storage-gcs``), web crawling that runs JavaScript in a browser to fetch pages (``fess-crawler-playwright``)
   * - SaaS, databases, etc.
     - The data store configuration screen and the mechanism that runs it
     - A data store plugin (``fess-ds-*``) for each source to import. Slack, Confluence and Jira, Google Drive, Microsoft 365, Box, databases, CSV, Git, and more
   * - Login and permissions
     - Users, roles, and groups registered in Fess, and integration with LDAP / Active Directory
     - SSO (``fess-sso-oidc`` for OpenID Connect, ``fess-sso-saml`` for SAML, ``fess-sso-entraid`` for Entra ID, ``fess-sso-spnego`` for SPNEGO)
   * - Scripts
     - JavaScript
     - Groovy (``fess-script-groovy``), OGNL (``fess-script-ognl``)
   * - Search page
     - The bundled ``bootstrap`` theme
     - Add a theme ZIP file rather than a plugin
   * - APIs
     - ``/api/v2/`` (search, labels, suggest, popular words, health check, and more) and the admin API
     - ``/api/v1/`` (``fess-webapp-v1-api``), ``/json`` and ``/suggest`` (``fess-webapp-classic-api``). Fess Site Search uses ``/api/v1/``, so it requires ``fess-webapp-v1-api``
   * - AI-related
     - The mechanisms for semantic search and AI search mode (RAG). If you use an embedding model deployed in OpenSearch, semantic search requires no plugin
     - Connections to LLMs and external embedding models (``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``), MCP server (``fess-webapp-mcp``), image search (``fess-webapp-multimodal``)

Of the items in the "Requires a plugin" column, only S3 and GCS, the four SSO types, and Groovy are included in the standard Docker image.
Everything else requires an additional installation, whichever installation method you use.

Configurations whose script type is set to Groovy, and configurations carried over from earlier versions that have no script type recorded, are executed as Groovy.
To use them, you need ``fess-script-groovy``.
For newly created data store configurations, the script type defaults to JavaScript.

Install plugins in one of the following ways.
After installing or removing a plugin, restart Fess.
Match the plugin version to the Fess version (15.9.x for Fess 15.9).

- In the admin console, open [System] > [Plugin], click [Install], and choose from the list
- On the command line, run ``bin/fess-setup install plugin <plugin-name>:<version>``
- With Docker, set the environment variable ``FESS_PLUGINS`` to a space-separated list such as ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0``

How to use data store plugins is explained in :doc:`datastore-basics`, and how to write your own plugin in :doc:`guide-17`.

Searchable File Formats
=======================

Text is extracted from files with extraction processing such as Apache Tika.
You can search HTML, PDF, Microsoft Office documents, text, the contents of archive files, and more.
For the list of verified formats, see `Supported File Formats <https://fess.codelibs.org/supported-files.html>`__.

Text inside images and scanned PDFs is not searchable by default.
It becomes searchable when you install ``tesseract`` on the host where the crawler runs and enable OCR.
For the steps, see `OCR Configuration <https://fess.codelibs.org/stable/config/crawler-ocr.html>`__.

Choosing an Installation Method
===============================

Fess is distributed as Docker images and as ZIP, RPM, and DEB packages.
If you just want to try it, Docker is the quickest way because it starts Fess and OpenSearch together.
The steps are described in :doc:`guide-02`.

In production, you can also provide OpenSearch as a separate server or cluster.
For the required Java and OpenSearch versions and guidelines for CPU, memory, and disk, see `System Requirements <https://fess.codelibs.org/stable/install/prerequisites.html>`__.

Reading Paths by Goal
=====================

The articles are organized so that you can read them according to your goal.
Pick the row closest to your goal and read the articles from left to right.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Goal
     - Articles to read
   * - I want to try Fess first
     - :doc:`guide-02`
   * - I want to search file servers
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - I want to search cloud and SaaS data
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - I want to embed search in an existing site or system
     - :doc:`guide-03` → :doc:`guide-11`
   * - I want to show different information to each department or user
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - I want to enhance search with AI
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - I am starting production operation
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

The following articles are also available:

- Improving search quality: :doc:`guide-08`, :doc:`guide-09`, :doc:`guide-22`
- Searching images and text together: :doc:`guide-21`
- Writing your own plugins: :doc:`guide-17`
- Planning a company-wide rollout: :doc:`guide-23`
- Use cases and comparisons with other products: :doc:`use-cases`, :doc:`comparison`

The list of articles is also available on the :doc:`../guide` page.

References
==========

- `Fess Documentation (stable) <https://fess.codelibs.org/stable/>`__
- `System Requirements <https://fess.codelibs.org/stable/install/prerequisites.html>`__
- `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `Plugin Architecture <https://fess.codelibs.org/stable/dev/plugin-architecture.html>`__
- `Theme <https://fess.codelibs.org/stable/admin/theme-guide.html>`__
- `Supported File Formats <https://fess.codelibs.org/supported-files.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess (GitHub) <https://github.com/codelibs/fess>`__
