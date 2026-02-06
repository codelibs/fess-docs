======================================
Fess vs Other Search Solutions
======================================

Introduction
============

When selecting a full-text search system, there are various options available.
This page compares Fess with major search solutions, explaining the characteristics and appropriate use cases for each.

.. note::

   This comparison is based on information as of January 2026.
   For the latest features and changes, please refer to each project's official documentation.

----

Fess vs OpenSearch/Elasticsearch Standalone
===========================================

Overview
--------

OpenSearch and Elasticsearch are powerful search engines, but using them standalone requires additional development to create a complete "search system."
Fess uses OpenSearch/Elasticsearch as its backend while providing a complete search system out of the box.

Comparison
----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Fess
     - OpenSearch/Elasticsearch Standalone
   * - Search UI
     - ✅ Built-in
     - ❌ Requires development
   * - Admin UI
     - ✅ Web-based admin panel
     - ❌ Requires development or separate tools
   * - Crawler
     - ✅ Built-in (Web/File/DB)
     - ❌ Requires development or separate tools
   * - Deployment time
     - Minutes (Docker)
     - Weeks to months (including development)
   * - Customizability
     - Medium (JSP/CSS customization)
     - High (fully custom development possible)
   * - Initial cost
     - Low
     - High (development costs)
   * - Operational cost
     - Low to Medium
     - Medium to High
   * - Scalability
     - High
     - High
   * - Required skills
     - Basic IT knowledge
     - Programming & search engine expertise

When to Choose Fess
-------------------

- **When you need to build a search system quickly**
- **When development resources are limited**
- **When standard search features are sufficient**
- **When web crawling and file search are the main use cases**

When to Choose OpenSearch/Elasticsearch Standalone
--------------------------------------------------

- **When you need a completely custom search experience**
- **When integrating search into an existing application**
- **When special search logic is required**
- **When your team has search engine expertise**

.. tip::

   After deploying Fess, you can also build a custom search UI using the API.
   Consider starting with Fess and customizing as needed.

----

Fess vs Apache Solr
===================

Overview
--------

Apache Solr is a Lucene-based open source search platform.
It offers high customizability, but requires more expertise for deployment and operation compared to Fess.

Comparison
----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Fess
     - Apache Solr
   * - Search UI
     - ✅ Built-in
     - ❌ Requires development
   * - Admin UI
     - ✅ Intuitive Web UI
     - △ Technical Admin UI
   * - Crawler
     - ✅ Built-in
     - ❌ Requires separate tool (Nutch, etc.)
   * - Setup difficulty
     - Low
     - Medium to High
   * - Documentation
     - ✅ Comprehensive
     - ✅ Comprehensive
   * - Cloud support
     - ✅ Docker/Kubernetes
     - ✅ SolrCloud
   * - Community
     - Japan-focused
     - Global

When to Choose Fess
-------------------

- **When Web/File crawling is the main use case**
- **When GUI management is important**
- **When ease of deployment is a priority**

When to Choose Solr
-------------------

- **When you already have Solr expertise**
- **When SolrCloud distributed search is needed**
- **When specific Solr plugins are required**

----

Fess vs Google Site Search / Custom Search
==========================================

Overview
--------

Google Site Search (GSS) was discontinued in 2018.
The successor, Google Custom Search (Programmable Search Engine), has limitations.
Fess is an ideal migration target from GSS.

Comparison
----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Fess
     - Google Custom Search
   * - Ad display
     - ✅ None
     - ❌ Displayed (free tier)
   * - Data location
     - ✅ Self-managed
     - ❌ Google servers
   * - Index control
     - ✅ Full control
     - △ Limited
   * - Customization
     - ✅ Freely customizable
     - △ Limited
   * - Internal content search
     - ✅ Supported
     - ❌ Not supported
   * - Monthly cost
     - Server costs only
     - Free (with ads) to paid
   * - Search relevance tuning
     - ✅ Detailed tuning possible
     - △ Limited

When to Choose Fess
-------------------

- **When you don't want to display ads**
- **When internal content should be searchable**
- **When you want control over search results**
- **When you want to manage data yourself**

.. tip::

   With Fess Site Search (FSS), you can implement site search
   by simply embedding JavaScript, just like Google Site Search.

----

Fess vs Commercial Search Products
==================================

Overview
--------

Compared to commercial products like Microsoft SharePoint Search, Autonomy, and Google Cloud Search.

Comparison
----------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Fess
     - Commercial Products (General)
   * - License cost
     - ✅ Free (OSS)
     - ❌ Expensive
   * - Vendor lock-in
     - ✅ None
     - ❌ Yes
   * - Customization
     - ✅ Source code available
     - △ Limited
   * - Feature richness
     - ○ Basic to intermediate
     - ✅ Advanced features
   * - Support
     - △ Community + Commercial
     - ✅ Vendor support
   * - AI/ML features
     - △ Basic suggest
     - ✅ Advanced AI features
   * - Enterprise integration
     - ○ Major systems supported
     - ✅ Broad integration

When to Choose Fess
-------------------

- **When you want to minimize costs**
- **When you want to avoid vendor lock-in**
- **When basic search features are sufficient**
- **When you want to leverage open source**

When to Choose Commercial Products
----------------------------------

- **When advanced AI/ML features are needed**
- **When comprehensive vendor support is required**
- **When integration with existing commercial ecosystems is needed**

.. note::

   The commercial version of Fess, `N2 Search <https://www.n2sm.net/products/n2search.html>`__,
   provides additional enterprise features and support.

----

Selection Guidelines
====================

Use the following flowchart to select the optimal solution:

::

    Do you have sufficient development resources?
          │
    ┌─────┴─────┐
    │           │
   Yes         No
    │           │
    ▼           ▼
  Are requirements  →  Consider Fess
  specialized?
    │
    ├── Yes → OpenSearch/Elasticsearch standalone
    │         or commercial products
    │
    └── No → Is Fess sufficient?
              │
              ├── Yes → Fess
              │
              └── No → Re-evaluate requirements

Summary
=======

Fess is an optimal choice as a "ready-to-use search system" for many cases.

**Fess Strengths**:

- Deploy in minutes
- Build search system without development
- Open source and free

**Next Steps**:

1. Try Fess with the `Quick Start <../quick-start.html>`__
2. Evaluate against your requirements
3. Consult `Commercial Support <../support-services.html>`__ if needed

