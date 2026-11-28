==========================================
Comparing Fess with Other Search Solutions
==========================================

Introduction
============

When you set up search for internal documents or a website, the candidates include search systems such as Fess, in-house development on top of a search engine such as OpenSearch or Apache Solr, external web search services, and commercial enterprise search products.
This article first lays out what Fess 15.9 provides in a form that is easy to check, and then compares how its role differs from the other options.

.. note::

   Statements about Fess reflect version 15.9.
   For other products and services, this article covers only architectural differences that are unlikely to change. Features, pricing, and availability can change, so check the latest documentation of each product.

What Fess Provides
==================

Fess is a search system that uses OpenSearch as its search engine.
It provides the crawler, the admin console, the search UI, and the APIs as a single application, and stores the index and crawl settings in OpenSearch.
Elasticsearch and Solr cannot be used as the search engine.
It is licensed under the Apache License 2.0.

Many features are provided as plugins, and you install only the ones you need.
Items whose "Requires" column is empty in the following table work with Fess alone.

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - Item
     - What 15.9 provides
     - Requires
   * - Web crawling
     - Crawls HTTP/HTTPS sites. Web authentication, request headers, and path mappings can be configured
     -
   * - File crawling
     - Crawls ``file``, ``smb``, ``smb1``, and ``ftp`` paths
     -
   * - Cloud storage crawling
     - ``s3://`` (Amazon S3 and S3-compatible storage), ``gcs://`` (Google Cloud Storage)
     - ``fess-storage-s3``, ``fess-storage-gcs``
   * - Databases and SaaS
     - Ingested through data store connectors (listed in the next section)
     - ``fess-ds-*`` plugins
   * - Document formats
     - Office documents, PDF, HTML, text, archive files, and more. OCR for images and scanned PDFs is disabled by default
     - The ``tesseract`` command for OCR
   * - Access control
     - Shows different search results per role, group, and user. For SMB and file crawling, file permissions are imported as roles. Integration with LDAP (including Active Directory) is a core feature
     -
   * - Single sign-on
     - OpenID Connect, SAML, SPNEGO (Kerberos), Microsoft Entra ID
     - ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``
   * - Search UI
     - Rendered by a static theme (HTML, CSS, and JavaScript packaged as a ZIP). The bundled theme is ``bootstrap``
     -
   * - API
     - ``/api/v2`` for search, labels, suggestions, popular words, health checks, AI search mode, and more; ``/api/admin`` for administration
     -
   * - Legacy APIs
     - ``/api/v1``, ``/json`` and ``/suggest``
     - ``fess-webapp-v1-api``, ``fess-webapp-classic-api``
   * - Semantic search
     - Splits document content into chunks, vectorizes them, and merges the results with keyword search results using Rank Fusion. Disabled by default
     - An embedding model (OpenSearch ML Commons or a ``fess-llm-*`` plugin)
   * - AI search mode (RAG)
     - An LLM answers questions based on search results. Disabled by default
     - One of ``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``
   * - MCP server
     - Lets AI agents search Fess through ``/mcp``
     - ``fess-webapp-mcp``
   * - Image search
     - Multimodal search that finds images (GIF, JPEG, PNG) from a text description
     - ``fess-webapp-multimodal`` and a CLIP server

The Docker image bundles the four SSO plugins, ``fess-storage-s3``, ``fess-storage-gcs``, and ``fess-script-groovy``.
Install other plugins from [System] > [Plugin], and then restart Fess.
Choose the plugin version that matches the Fess minor version (15.9.x for 15.9).

Data Store Connectors
---------------------

The following data store plugins are published for 15.9.
Configuration details are in each connector's reference.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Category
     - Plugin (target)
   * - Cloud storage
     - ``fess-ds-box`` (Box), ``fess-ds-dropbox`` (Dropbox), ``fess-ds-gsuite`` (Google Drive), ``fess-ds-microsoft365`` (OneDrive, SharePoint Online, Teams, and more)
   * - Collaboration
     - ``fess-ds-atlassian`` (Confluence, Jira), ``fess-ds-slack`` (Slack), ``fess-ds-notion`` (Notion), ``fess-ds-backlog`` (Backlog), ``fess-ds-sharepoint`` (on-premises SharePoint Server)
   * - Development and business systems
     - ``fess-ds-git`` (Git repositories), ``fess-ds-salesforce`` (Salesforce)
   * - Data
     - ``fess-ds-db`` (databases reachable through JDBC), ``fess-ds-csv`` (CSV), ``fess-ds-json`` (JSON), ``fess-ds-wikipedia`` (Wikipedia dumps)

A data source not listed here can be made searchable by writing your own data store plugin (:doc:`guide-17`) or by registering documents through the admin API (:doc:`guide-11`).

Compared with In-House Development on a Search Engine (OpenSearch, Apache Solr)
===============================================================================

OpenSearch and Apache Solr are search engines.
They handle indexing and searching, but do not include a crawler to collect data, a search UI for end users, or per-document access control.
You either develop these yourself or combine other software.
For web crawling, for example, there are separate projects such as Apache Nutch.

Fess is an application that provides these parts on top of OpenSearch.
The differences are as follows.

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Aspect
     - Fess
     - In-house development on a search engine
   * - Data collection
     - Web, file, and data store crawls are configured in the admin console
     - Build crawlers and ingestion processes, or combine other software
   * - Search UI
     - Rendered by a theme. To change the look, create a theme or build your own UI on the API
     - Fully customizable, but everything must be developed
   * - Access control
     - Roles and file permissions are recorded on each document, and searches are filtered by the logged-in user
     - Design and implement both the import of document permissions and the filtering at search time
   * - Index design
     - Uses the index defined by Fess. Analyzers for many languages, including English, are preconfigured
     - Can be designed freely to fit the use case
   * - What you operate
     - Fess and OpenSearch
     - The search engine and every part developed in-house

If you want to design the search mechanism from scratch, or search your own data structures, using a search engine directly is a better fit.
On the other hand, if the goal is to collect documents and make them searchable within your organization, starting with Fess and filling the gaps with the API or plugins keeps the scope of development smaller.

Fess can also connect to an existing OpenSearch cluster.
For services where CodeLibs plugins cannot be installed, such as Amazon OpenSearch Service, set ``search_engine.type`` to ``aws`` or ``vanilla``.
In that case, some features such as dictionary management and duplicate document detection are not available (see `Search Engine Type <https://fess.codelibs.org/stable/config/search-engine-type.html>`__).

Compared with Site Search Using an External Web Search Service
==============================================================

Another way to provide site search is to use the index of a search service provider.
With this approach, only public pages fetched by the provider's crawler are searchable.
Pages that require login and internal file servers cannot be covered, and when pages are crawled and in what order they are shown also depend on the provider.

With Fess, you decide what to crawl and when, and the index stays in your own environment.
To tune search results, you can use Key Match (ranking specific documents higher for specific terms), Document Boost, Related Query, and more.
There are two ways to integrate Fess into an existing site.

- Place a search form that takes users to the Fess search UI (theme)
- Embed the Fess Site Search (FSS) JavaScript to show search results within the page

FSS calls ``/api/v1``, so the ``fess-webapp-v1-api`` plugin is required in 15.9.
See :doc:`guide-03` for the steps.

Compared with Commercial Enterprise Search Products
===================================================

When comparing with commercial products, coverage varies greatly from product to product, so no general verdict on which is better is possible.
We recommend checking candidate products and Fess under the same conditions against the following aspects.

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Aspect
     - For Fess
   * - Supported data sources
     - Check the table in the previous section and the list of data store connectors. If something is missing, you can write your own plugin
   * - Access control
     - Per role, group, and user, with support for LDAP and four SSO methods
   * - Generative AI
     - AI search mode (RAG), semantic search, and the MCP server. Choose the LLM from Ollama (self-hosted), OpenAI, Gemini, and Amazon Bedrock
   * - Data location
     - The index is stored in OpenSearch that you operate yourself. If you use external services for the LLM or embeddings, questions and document content are sent to those services
   * - Deployment model
     - Self-hosted software. It can be installed with Docker, on Linux (ZIP, RPM, DEB), and on Windows. It also runs on Kubernetes, but there is no official Helm chart
   * - Cost and support
     - There are no license fees. The costs are servers and operational effort. For commercial support, see `Commercial Support <https://fess.codelibs.org/support-services.html>`__
   * - Freedom to change
     - The source code is public, and Fess can be extended with themes, plugins, and the API

Commercial products are a good fit when the product already offers the connectors and management features you need and you want to leave operations to the vendor.
Fess is a good fit when you want to build a search platform by combining the features you need while keeping your data in your own environment.

How to Choose
=============

Answer the following questions in order to decide whether Fess is a candidate.

1. Is the data you want to search covered by Fess's crawl targets or data store connectors?

   - If not, estimate the development needed to write your own plugin (:doc:`guide-17`) or to register documents through the API (:doc:`guide-11`).

2. Do you need to show different documents to different users?

   - To use file server permissions, see :doc:`file-server-search`; for role design, see :doc:`guide-05`; for SSO, see :doc:`guide-15`.

3. Is the Fess theme sufficient for your search UI?

   - To build search into your own application, use ``/api/v2`` (:doc:`guide-11`).

4. Can you operate Fess and OpenSearch yourself?

   - If you cannot, or if you want to leave operations to a vendor, consider commercial support for Fess or a commercial product.

5. Do you need answers from generative AI or semantic search?

   - Decide which LLM to use, and check the required setup in :doc:`guide-19` and :doc:`guide-18`.

If the answers to 1 and 4 are "yes", the most reliable next step is to try Fess and check the search results with your actual documents.

Try It Out
==========

A comparison table alone cannot tell you how well your own documents can be searched.
Start Fess with Docker following the steps in :doc:`guide-02`, crawl part of what you want to search, and check the following.

- Whether the target documents have been indexed (check [System Info] > [Job Log] and [Failure URL] for URLs that ended in errors)
- Whether searching for frequently used terms brings the expected documents to the top
- Whether documents that should not be visible stay hidden when you switch the logged-in user (if you need access control)

What to Read Next
=================

- To understand how Fess is structured and how to read through the articles: :doc:`guide-01`
- To get it running locally first: :doc:`guide-02`
- To add search to an existing site: :doc:`guide-03`
- To search data in databases or SaaS: :doc:`datastore-basics`
- To reflect file server permissions in search results: :doc:`file-server-search`
- To have generative AI answer from internal documents: :doc:`guide-19`
- To prepare for growth in scale: :doc:`guide-14`
- To see examples of how Fess is used: :doc:`use-cases`

References
==========

- `Data Store Connector Overview <https://fess.codelibs.org/stable/config/datastore/ds-overview.html>`__
- `File Crawling (File Server Search) <https://fess.codelibs.org/stable/admin/fileconfig-guide.html>`__
- `Supported File Formats <https://fess.codelibs.org/supported-files.html>`__
- `OCR Configuration <https://fess.codelibs.org/stable/config/crawler-ocr.html>`__
- `Theme <https://fess.codelibs.org/stable/admin/theme-guide.html>`__
- `API Overview <https://fess.codelibs.org/stable/api/api-overview.html>`__
- `Semantic Search <https://fess.codelibs.org/stable/config/search-semantic.html>`__
- `AI Search (RAG) and LLM Integration Overview <https://fess.codelibs.org/stable/config/llm-overview.html>`__
- `Search Engine Type <https://fess.codelibs.org/stable/config/search-engine-type.html>`__
- `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
