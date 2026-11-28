========================================
Fess Use Cases and Application Scenarios
========================================

Introduction
============

This page introduces the situations in which Fess is commonly used, organized by industry, by scale, and by technical goal.
For each scenario, it describes the problem to solve, the Fess features and plugins involved, and the articles that explain the steps.
The configuration steps themselves are in each article, so start from the scenario closest to your own situation and pick the articles to read.

The feature and plugin names in this page follow Fess 15.9.
In 15.9, importing from databases and SaaS, SSO, and crawling S3 and GCS are provided by plugins.
Use the same 15.9.x version for plugins as for Fess, and restart Fess after installing them.
For how to install them, see `Plugins <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__.

.. note::

   The following are general usage patterns. For actual deployment cases, please contact `Commercial Support <../support-services.html>`__.

Finding Features by Goal
========================

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - What you want to do
     - Features and plugins
     - Articles to read
   * - Try it out locally first
     - Docker Compose (docker-fess)
     - :doc:`guide-02`
   * - Search the intranet site and file servers together
     - Web crawling, file system crawling, File Authentication, labels
     - :doc:`guide-04`, :doc:`file-server-search`
   * - Show different documents by department or position
     - Permissions, roles and groups, LDAP (Active Directory)
     - :doc:`guide-05`
   * - Add a search box to an existing site
     - Search form, Fess Site Search (``fess-webapp-v1-api``), themes
     - :doc:`guide-03`
   * - Search Git, Confluence, Jira and Slack
     - ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack``
     - :doc:`datastore-basics`, :doc:`guide-06`
   * - Search Google Drive, SharePoint Online and Box
     - ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box``
     - :doc:`datastore-basics`, :doc:`guide-07`
   * - Search databases, CSV and Salesforce
     - ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce``
     - :doc:`datastore-basics`, :doc:`guide-12`
   * - Search from business systems
     - Search API (``/api/v2``), access tokens
     - :doc:`guide-11`
   * - Let users search with the company login
     - ``fess-sso-entraid``, ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``
     - :doc:`guide-15`
   * - Share one Fess among several organizations
     - Virtual hosts, roles, labels
     - :doc:`guide-13`
   * - Find terms that return nothing and how search is used, and improve
     - [System Info] > [Search Log]
     - :doc:`guide-08`
   * - Find documents with similar meaning, have AI answer questions
     - Semantic search, AI search mode, ``fess-webapp-mcp``
     - :doc:`guide-18`, :doc:`guide-19`, :doc:`guide-20`
   * - Prepare for more documents and users
     - Separating and clustering OpenSearch, running multiple Fess servers
     - :doc:`guide-14`
   * - Run reliably in production
     - ``/api/v2/health``, backups, logs
     - :doc:`guide-10`

Use Cases by Industry
=====================

Manufacturing: Finding Scattered Technical Documents
----------------------------------------------------

**Problem**: Design documents, specifications and quality records are split across each department's file server, and finding related material from a drawing number or model number takes time.

**Features used**:

- Crawl the file servers with ``smb://`` so that the body text of PDFs and Office documents becomes searchable. Windows access rights (ACLs) are imported as document permissions by default
- Create labels with display names such as "Design" and "Quality", classify documents by the paths they cover, and let users narrow results on the search page
- Scanned paper records become searchable by their text once OCR is enabled. OCR is disabled by default and requires ``tesseract`` on the host where the crawler runs (`OCR Configuration <https://fess.codelibs.org/stable/config/crawler-ocr.html>`__)

Files in formats from which Fess cannot extract text can only be found by file name or path.
Check the supported formats in `Supported Files <../supported-files.html>`__.

**Articles to read**: Build the setup with :doc:`guide-04`, check the ACL prerequisites in :doc:`file-server-search`, and configure per-department visibility with :doc:`guide-05`.

Finance and Insurance: Finding Regulations and Contracts with Permissions
-------------------------------------------------------------------------

**Problem**: There are large numbers of internal regulations, manuals and contracts, and finding them for every inquiry or audit takes effort. At the same time, who may read them must be strictly separated by department.

**Features used**:

- Use per-document permissions to limit who sees a document in search results. The permissions of a new crawl configuration contain ``{role}guest`` from the start, so remove it for documents that are not public
- To keep users who are not logged in from searching, enable "Login Required" under [General]
- Use SSO to log in through the company identity platform: ``fess-sso-saml`` for SAML, ``fess-sso-entraid`` for Entra ID (the Docker image bundles the four SSO plugins)
- To search from business systems, keep an access token on the server side and call the search API

**Articles to read**: Design permissions with :doc:`guide-05`, and configure SSO and HTTPS with :doc:`guide-15`. Integration with business systems is covered in :doc:`guide-11`.

Education: Searching Across Campus Sites and Shared Drives
----------------------------------------------------------

**Problem**: Each faculty's website, lecture materials and internal university documents are in separate places, and neither students nor staff can reach the information they need.

**Features used**:

- Import the campus websites with web crawling. Institutional repositories (such as DSpace) have no dedicated connector, so crawl their public pages as websites
- Import Google Drive shared drives with ``fess-ds-gsuite`` and SharePoint Online with ``fess-ds-microsoft365``
- To show students and staff different scopes, separate them with roles and permissions. To split the site itself, use virtual hosts

**Articles to read**: :doc:`guide-04`, :doc:`guide-07`, :doc:`guide-05`. To split the site, see :doc:`guide-13`.

IT and Software: Finding Development Information in One Place
-------------------------------------------------------------

**Problem**: Code lives in Git, designs in Confluence, issues in Jira, and discussions in Slack or Teams, which makes it hard to trace past decisions.

**Features used**:

- Import repository files with ``fess-ds-git``, Confluence and Jira with ``fess-ds-atlassian``, and Slack messages with ``fess-ds-slack``
- Teams channels and chats can be imported with the ``TeamsDataStore`` of ``fess-ds-microsoft365`` (`Microsoft 365 Connector <https://fess.codelibs.org/stable/config/datastore/ds-microsoft365.html>`__)
- `docker-codesearch <https://github.com/codelibs/docker-codesearch>`__ is published as a setup specialized for source code search
- To embed search in internal tools, use the search API; to let AI agents search, use ``fess-webapp-mcp``

**Articles to read**: :doc:`datastore-basics`, then :doc:`guide-06`. Integration with AI agents is covered in :doc:`guide-20`.

Use Cases by Scale
==================

The number of servers and the memory you need are not determined by the number of users or documents alone.
The load changes with the length of the body text, the share of attachments, and whether users log in, so start small, measure, and add what is lacking.
The steps for deciding are summarized in the section on sizing guidelines in :doc:`guide-14`.
For the recommended server requirements for production (4 or more CPU cores, 8 GB or more of memory, and so on), see `System Requirements <https://fess.codelibs.org/stable/install/prerequisites.html>`__.

Starting with One Server
------------------------

For a department-level deployment or a trial, run Fess and OpenSearch on a single server.
With Docker Compose, start it with two files: ``compose.yaml`` and ``compose-opensearch3.yaml``.
The steps are in :doc:`guide-02`.

Even with a single server, decide the following two points from the start.

- How to take backups. Settings can be downloaded from [System Info] > [Backup], but dictionaries are not included (:doc:`guide-10`)
- With Docker, settings changed under [System] > [General] are saved to ``system.properties`` inside the container and revert when the container is recreated (see the section on stopping and restarting in :doc:`guide-02`)

When More Departments Start Using It
------------------------------------

When search or crawling becomes slow, first determine whether the cause is Fess itself, the crawler, or OpenSearch.
In most cases, scale out in the following order.

1. On the single server, tune the heap of Fess, the crawler and OpenSearch, and the crawl parallelism
2. Move OpenSearch to a separate server
3. Make OpenSearch a three-node cluster
4. Run multiple Fess servers and distribute requests with a load balancer

When running multiple Fess servers, keep the [General] settings, ``app.cipher.key`` in ``fess_config.properties``, and the installed plugins the same on all servers.
In Fess 15.9, login sessions are stored in each server's memory, so when distributing screens that users log in to, enable sticky sessions on the load balancer.
Storing sessions in OpenSearch to share them across servers is available from 15.10 onward.

**Articles to read**: :doc:`guide-14`, :doc:`guide-10`.

Using It Company-Wide
---------------------

At company scale, consider the following in addition to the setup above.

- Assign crawling to one Fess server (``scheduler.target.name`` and the job's "Target"). This keeps the crawl load off the servers that handle searches
- Use ``/api/v2/health`` for the load balancer and monitoring. It returns 503 when the OpenSearch cluster is ``RED`` or cannot be reached
- To separate the search page or the search targets per organization, use virtual hosts or separate Fess instances (:doc:`guide-13`)
- Regularly check the search log for terms with zero results and terms whose results are not clicked (:doc:`guide-08`)

Fess can also run on Kubernetes, but no official Helm chart is provided.
Convert the Docker Compose files or write the manifests yourself (see the FAQ in `Docker Installation (Details) <https://fess.codelibs.org/stable/install/install-docker.html>`__).

For large-scale deployments, also consider using `Commercial Support <../support-services.html>`__.

Technical Use Cases
===================

Searching Across Internal Wikis and Knowledge Bases
---------------------------------------------------

How you import content depends on the type of wiki.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Target
     - How to import
     - Reference
   * - Confluence
     - ``fess-ds-atlassian`` (``ConfluenceDataStore``)
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Notion Connector <https://fess.codelibs.org/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Backlog Connector <https://fess.codelibs.org/stable/config/datastore/ds-backlog.html>`__
   * - Wikis viewable on the web, such as MediaWiki
     - Web crawling (also configure Web Authentication if login is required)
     - :doc:`guide-04`

Documents imported through a data store also have ``{role}guest`` in their permissions from the start.
When importing spaces that only a limited group may read, first read the section in :doc:`guide-06` on deciding who sees the search results.

Unified Search Across File Servers
----------------------------------

The protocols handled by file crawling in Fess 15.9 are as follows.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Path format
     - Target
   * - ``smb://``
     - Windows shared folders, or NAS devices shared over SMB
   * - ``smb1://``
     - Old servers that support only SMB1
   * - ``file:``
     - Directories visible from the Fess server. Mount NFS shares in the OS first, then specify them in this format
   * - ``ftp://``
     - FTP servers
   * - ``s3://`` / ``gcs://``
     - Amazon S3-compatible storage / Google Cloud Storage. Requires ``fess-storage-s3`` / ``fess-storage-gcs`` (bundled in the Docker image)

The protocols enabled by default are ``file``, ``smb``, ``smb1`` and ``ftp`` (``crawler.file.protocols``).
To reflect SMB ACLs in search results, you need to remove ``{role}guest`` from the permissions of the crawl configuration.
The reason and how to verify it are in :doc:`file-server-search`, and the concrete settings are in :doc:`guide-04`.

Site Search for Websites
------------------------

There are three ways to add search to a public site, and they can be combined.

- Place a search form that takes users to the Fess search page. No additional configuration is needed on the Fess side
- Show search results inside an existing page with Fess Site Search (FSS). FSS calls ``/api/v1``, so in 15.9 it requires the ``fess-webapp-v1-api`` plugin. The FSS JavaScript is not served by Fess, so generate it with the FSS JS Generator and host it on your own site
- Match the Fess search page to the look of the existing site with a theme

The steps are in :doc:`guide-03`.
To build your own search page, use ``/api/v2/search`` (:doc:`guide-11`).

Searching Databases
-------------------

Information stored in databases, such as product masters and FAQs, is imported with ``fess-ds-db``.
It works with JDBC-compatible databases (MySQL, PostgreSQL, Oracle, SQL Server and others), and you provide a JDBC driver that matches the target separately.
A script maps the columns retrieved by a SELECT statement to fields such as ``title`` and ``content``.

If you build the URL of the original business screen and store it in ``url``, users can open the original data directly from the search result link.
The steps are in :doc:`guide-12`.

Combining with Generative AI
----------------------------

- Find documents with similar meaning even when keywords do not match: semantic search (:doc:`guide-18`)
- Have AI answer based on internal documents: AI search mode. It works without vector search (:doc:`guide-19`)
- Let AI agents such as Claude Code search Fess: ``fess-webapp-mcp`` (:doc:`guide-20`)

With every method, the documents searched are filtered by the same permissions as a normal search (for AI search mode, those of the logged-in user; for MCP, those of the access token, or guest permissions when MCP is used without authentication).
These permissions also decide which documents reach the AI, so complete the permission design in :doc:`guide-05` first.

How to Proceed with Deployment
==============================

1. Start Fess with :doc:`guide-02`, crawl part of the targets, and try searching
2. From the table above, pick the articles that match your problem and configure accordingly
3. Decide on permissions (:doc:`guide-05`) and operations (:doc:`guide-10`) before opening it to users

References
==========

- `Quick Start <../quick-start.html>`__
- `Documentation <../documentation.html>`__
- `Plugins <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `Data Store Connector Guide <https://fess.codelibs.org/stable/config/datastore/index.html>`__
- `Discussion Forum <https://discuss.codelibs.org/c/FessEN/>`__
- `GitHub <https://github.com/codelibs/fess>`__
