===================================
Open Source Full-Text Search Server Fess
===================================

Overview
====

Fess is a **full-text search server that can be easily built in 5 minutes**.

.. figure:: ../resources/images/en/demo-1.png
   :scale: 100%
   :alt: Standard Demo
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   Standard Demo

.. figure:: ../resources/images/en/demo-3.png
   :scale: 100%
   :alt: Site Search Demo
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   Site Search Demo

.. figure:: ../resources/images/en/demo-2.png
   :scale: 100%
   :alt: Code Search
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   Source Code Search

.. figure:: ../resources/images/en/demo-4.png
   :scale: 100%
   :alt: Document Search
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   Document Search

It can run on any OS with Java or Docker execution environment.
Fess is provided under the Apache License and is free software available at no cost.


Downloads
============

- :doc:`Fess 15.4.0 <downloads>` (zip/rpm/deb packages)

Features
====

-  Provided under Apache License (free software, free to use)

-  Crawls Web, file systems, Windows shared folders, and databases

-  Supports many file formats including MS Office (Word/Excel/PowerPoint), PDF, and more

-  OS-independent (Java-based)

-  JavaScript library for embedding into existing sites

-  Uses OpenSearch or Elasticsearch as search engine

-  Supports sites with BASIC/DIGEST/NTLM/FORM authentication

-  Search result filtering based on login status

-  Single Sign-On (SSO) with Active Directory and SAML

-  Location-based search with map integration

-  Configuration of crawl targets and search screen editing in browser

-  Search result classification with labels

-  Request header modification, duplicate domain configuration, search result path conversion

-  Integration with external systems via JSON format search results

-  Aggregation of search logs and click logs

-  Facet and drilldown support

-  Auto-complete and suggest features

-  User dictionary and synonym dictionary editing

-  Search result cache and thumbnail display

-  Search result proxy function

-  Mobile support (Responsive Web Design)

-  External system integration with access tokens

-  External text extraction support including OCR

-  Flexible design for various use cases

News
========

2025-12-25
    `Fess 15.4.0 Released <https://github.com/codelibs/fess/releases/tag/fess-15.4.0>`__

2025-10-25
    `Fess 15.3.0 Released <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Fess 15.2.0 Released <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Fess 15.1.0 Released <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

2025-06-22
    `Fess 15.0.0 Released <https://github.com/codelibs/fess/releases/tag/fess-15.0.0>`__

For past news, please see :doc:`here <news>`.

Forum
==========

If you have questions, please use the `forum <https://discuss.codelibs.org/c/FessJA/>`__.

Commercial Support
============

Fess is an open source product provided under the Apache License and is free for personal and commercial use.

If you need customization, implementation, or support services for Fess, please see `commercial support (paid) <https://www.n2sm.net/products/n2search.html>`__.
Commercial support also handles performance tuning such as improving search quality and crawl speed.

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (Optimized commercial package of Fess)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (Google Site Search alternative service)

- :doc:`Various support services <support-services>`


Fess Site Search
================

CodeLibs Project provides `Fess Site Search (FSS) <https://fss-generator.codelibs.org/ja/>`__.
You can embed Fess search pages into existing sites simply by placing JavaScript.
FSS makes it easy to migrate from Google Site Search and Yahoo! Search Custom Search.
If you need an affordable Fess server, please see `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__.

Data Store Plugins
====================

- `Confluence/Jira <https://github.com/codelibs/fess-ds-atlassian>`__
- `Box <https://github.com/codelibs/fess-ds-box>`__
- `CSV <https://github.com/codelibs/fess-ds-csv>`__
- `Database <https://github.com/codelibs/fess-ds-db>`__
- `Dropbox <https://github.com/codelibs/fess-ds-dropbox>`__
- `Elasticsearch <https://github.com/codelibs/fess-ds-elasticsearch>`__
- `Git <https://github.com/codelibs/fess-ds-git>`__
- `Gitbucket <https://github.com/codelibs/fess-ds-gitbucket>`__
- `G Suite <https://github.com/codelibs/fess-ds-gsuite>`__
- `JSON <https://github.com/codelibs/fess-ds-json>`__
- `Office 365 <https://github.com/codelibs/fess-ds-office365>`__
- `S3 <https://github.com/codelibs/fess-ds-s3>`__
- `Salesforce <https://github.com/codelibs/fess-ds-salesforce>`__
- `SharePoint <https://github.com/codelibs/fess-ds-sharepoint>`__
- `Slack <https://github.com/codelibs/fess-ds-slack>`__

Theme Plugins
===============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Ingester Plugins
==================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Script Plugins
==================

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

Related Projects
================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__

Media Coverage
============

- `Part 48: Single Sign-On with SAML <https://news.mynavi.jp/techplus/article/_ossfess-48/>`__

- `Part 47: Storage Management and Crawling with MinIO <https://news.mynavi.jp/techplus/article/_ossfess-47/>`__

- `Part 46: Crawling Amazon S3 <https://news.mynavi.jp/techplus/article/_ossfess-46/>`__

- `Part 45: How to Start with Compose V2 <https://news.mynavi.jp/techplus/article/_ossfess-45/>`__

- `Part 44: Using OpenSearch with Fess <https://news.mynavi.jp/techplus/article/_ossfess-44/>`__

- `Part 43: How to Use Elasticsearch 8 <https://news.mynavi.jp/techplus/article/_ossfess-43/>`__

- `Part 42: How to Use Search API with Access Tokens <https://news.mynavi.jp/techplus/article/_ossfess-42/>`__

- `Part 41: Crawling Microsoft Teams <https://news.mynavi.jp/itsearch/article/bizapp/5880>`__

- `Part 40: Configuring Various Features (Document Boost, Related Content, Related Queries) <https://news.mynavi.jp/itsearch/article/bizapp/5804>`__

- `Part 39: Configuring Various Features (Path Mapping, Request Headers, Duplicate Hosts) <https://news.mynavi.jp/itsearch/article/bizapp/5686>`__

- `Part 38: Configuring Various Features (Labels, Key Match) <https://news.mynavi.jp/itsearch/article/bizapp/5646>`__

- `Part 37: How to Use AWS Elasticsearch Service <https://news.mynavi.jp/itsearch/article/devsoft/5557>`__

- `Part 36: How to Use Elastic Cloud <https://news.mynavi.jp/itsearch/article/devsoft/5507>`__

- `Part 35: Crawling SharePoint Server <https://news.mynavi.jp/itsearch/article/devsoft/5457>`__

- `Part 34: Authentication with OpenID Connect <https://news.mynavi.jp/itsearch/article/devsoft/5338>`__

- `Part 33: Building an Input Assistance Environment <https://news.mynavi.jp/itsearch/article/devsoft/5292>`__

- `Part 32: Index Management <https://news.mynavi.jp/itsearch/article/devsoft/5233>`__

- `Part 31: Crawling Office 365 <https://news.mynavi.jp/itsearch/article/bizapp/5180>`__

- `Part 30: Authentication with Azure AD <https://news.mynavi.jp/itsearch/article/bizapp/5136>`__

- `Part 29: How to Use Docker <https://news.mynavi.jp/itsearch/article/devsoft/5058>`__

- `Part 28: How to View Log Files <https://news.mynavi.jp/itsearch/article/devsoft/5032>`__

- `Part 27: Clustering Fess <https://news.mynavi.jp/itsearch/article/devsoft/4994>`__

- `Part 26: Location-Based Search <https://news.mynavi.jp/itsearch/article/devsoft/4963>`__

- `Part 25: Using Tesseract OCR <https://news.mynavi.jp/itsearch/article/devsoft/4928>`__

- `Part 24: Crawling GitBucket <https://news.mynavi.jp/itsearch/article/devsoft/4924>`__

- `Part 23: How to Use the Suggest Feature <https://news.mynavi.jp/itsearch/article/bizapp/4890>`__

- `Part 22: Crawling Dropbox <https://news.mynavi.jp/itsearch/article/bizapp/4844>`__

- `Part 21: Crawling Slack Messages <https://news.mynavi.jp/itsearch/article/bizapp/4808>`__

- `Part 20: Visualizing Search Logs <https://news.mynavi.jp/itsearch/article/devsoft/4781>`__

- `Part 19: Crawling CSV Files <https://news.mynavi.jp/itsearch/article/devsoft/4761>`__

- `Part 18: Crawling Google Drive <https://news.mynavi.jp/itsearch/article/devsoft/4732>`__

- `Part 17: Crawling Databases <https://news.mynavi.jp/itsearch/article/devsoft/4659>`__

- `Part 16: How to Use the Search API <https://news.mynavi.jp/itsearch/article/devsoft/4613>`__

- `Part 15: Crawling File Servers That Require Authentication <https://news.mynavi.jp/itsearch/article/devsoft/4569>`__

- `Part 14: How to Use the Management API <https://news.mynavi.jp/itsearch/article/devsoft/4514>`__

- `Part 13: How to Display Thumbnail Images in Search Results <https://news.mynavi.jp/itsearch/article/devsoft/4456>`__

- `Part 12: How to Use the Virtual Host Feature <https://news.mynavi.jp/itsearch/article/devsoft/4394>`__

- `Part 11: Single Sign-On with Fess <https://news.mynavi.jp/itsearch/article/devsoft/4357>`__

- `Part 10: Building in a Windows Environment <https://news.mynavi.jp/itsearch/article/bizapp/4320>`__

- `Part 9: Fess and Active Directory Integration <https://news.mynavi.jp/itsearch/article/bizapp/4283>`__

- `Part 8: Role-Based Search <https://news.mynavi.jp/itsearch/article/hardware/4201>`__

- `Part 7: Crawling Sites with Authentication <https://news.mynavi.jp/itsearch/article/hardware/4158>`__

- `Part 6: Analyzer for Japanese Full-Text Search <https://news.mynavi.jp/itsearch/article/devsoft/3671>`__

- `Part 5: Tokenization for Full-Text Search <https://news.mynavi.jp/itsearch/article/devsoft/3539>`__

- `Part 4: Natural Language Processing with Fess <https://news.mynavi.jp/itsearch/article/bizapp/3445>`__

- `Part 3: Web Scraping with Configuration Only <https://news.mynavi.jp/itsearch/article/bizapp/3341>`__

- `Part 2: Easy Migration from Google Site Search <https://news.mynavi.jp/itsearch/article/bizapp/3260>`__

- `Part 1: Introducing the Full-Text Search Server Fess <https://news.mynavi.jp/itsearch/article/bizapp/3154>`__

.. |image0| image:: ../resources/images/en/demo-1.png
.. |image1| image:: ../resources/images/en/demo-2.png
.. |image2| image:: ../resources/images/en/demo-3.png
.. |image3| image:: ../resources/images/en/n2search_225x50.png
   :target: https://www.n2sm.net/products/n2search.html
.. |image4| image:: ../resources/images/en/n2search_b.png


.. toctree::
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives


