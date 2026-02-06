=========================
Fess Use Cases & Examples
=========================

Introduction
============

Fess is utilized by organizations across various industries and scales.
This page introduces representative use cases and practical examples of Fess deployment.

.. note::

   The following examples illustrate common deployment patterns for Fess.
   For actual case studies, please contact `Commercial Support <../support-services.html>`__.

----

Industry-Specific Use Cases
===========================

Manufacturing
-------------

**Challenge**: Design drawings, technical documents, and quality management documents are scattered across multiple file servers, making it time-consuming to find needed information.

**Fess Solution**:

- Unified search across CAD drawings, PDF technical documents, and Office documents on file servers
- Cross-search by product model numbers, drawing numbers, and project names
- Display search results based on access permissions (role-based search)

**Architecture Example**:

.. code-block:: text

    [File Servers]  →  [Fess]  →  [Internal Portal]
         │               │
         ├─ Drawings     ├─ OpenSearch Cluster
         ├─ Tech Docs    └─ Active Directory Integration
         └─ QC Records

**Related Features**:

- `File Server Crawling <https://fess.codelibs.org/en/15.5/config/config-filecrawl.html>`__
- `Role-Based Search <https://fess.codelibs.org/en/15.5/config/config-role.html>`__
- `Thumbnail Display <https://fess.codelibs.org/en/15.5/admin/admin-general.html>`__

Financial Services & Insurance
------------------------------

**Challenge**: Compliance documents, contracts, and internal regulations are extensive, making audit responses and inquiry handling time-consuming.

**Fess Solution**:

- Cross-search of internal regulations, manuals, and FAQs
- Text search of contracts and application documents
- Knowledge search from past inquiry history

**Security Features**:

- Authentication via LDAP/Active Directory integration
- Single Sign-On via SAML
- API authentication via access tokens

**Related Features**:

- `LDAP Authentication <https://fess.codelibs.org/en/15.5/config/config-security.html>`__
- `SAML Authentication <https://fess.codelibs.org/en/15.5/config/config-saml.html>`__

Education
---------

**Challenge**: Research papers, lecture materials, and campus documents are distributed across departmental servers, making information sharing difficult.

**Fess Solution**:

- Unified search from campus portal
- Research paper repository search
- Lecture materials and syllabus search

**Architecture Examples**:

- Campus website crawling
- Integration with paper repositories (DSpace, etc.)
- Search of materials on Google Drive / SharePoint

**Related Features**:

- `Web Crawling <https://fess.codelibs.org/en/15.5/config/config-webcrawl.html>`__
- `Google Drive Crawling <https://fess.codelibs.org/en/15.5/config/config-crawl-gsuite.html>`__

IT & Software
-------------

**Challenge**: Source code, documentation, wikis, and ticket management system information are scattered, reducing development efficiency.

**Fess Solution**:

- Code search in GitHub/GitLab repositories
- Search of Confluence/Wiki pages
- Search of Slack/Teams messages

**Developer Features**:

- Integration with existing systems via Search API
- Code highlighting
- Filtering by file type

**Related Features**:

- `Git Repository Crawling <https://fess.codelibs.org/en/15.5/config/config-crawl-git.html>`__
- `Confluence Crawling <https://fess.codelibs.org/en/15.5/config/config-crawl-atlassian.html>`__
- `Slack Crawling <https://fess.codelibs.org/en/15.5/config/config-crawl-slack.html>`__

----

Scale-Based Use Cases
=====================

Small Business (up to 100 employees)
------------------------------------

**Characteristics**: Want easy deployment and operation with limited IT resources.

**Recommended Configuration**:

- Easy deployment via Docker Compose
- Single server configuration (Fess + OpenSearch)
- Required memory: 8GB or more

**Deployment Steps**:

.. code-block:: bash

    # Deploy in 5 minutes
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Cost**:

- Software: Free (Open Source)
- Server costs only (Cloud or On-premise)

Mid-size Enterprise (100-1000 employees)
----------------------------------------

**Characteristics**: Multi-department usage, requires reasonable availability.

**Recommended Configuration**:

- 2 Fess servers (redundancy)
- 3-node OpenSearch cluster
- Load balancer for traffic distribution
- Active Directory integration

**Capacity Guidelines**:

- Documents: up to 5 million
- Concurrent search users: up to 100

**Related Features**:

- `Cluster Configuration <https://fess.codelibs.org/en/15.5/install/clustering.html>`__
- `Backup & Restore <https://fess.codelibs.org/en/15.5/admin/admin-backup.html>`__

Large Enterprise (1000+ employees)
----------------------------------

**Characteristics**: Large-scale data, high availability, strict security requirements.

**Recommended Configuration**:

- Multiple Fess servers (running on Kubernetes)
- OpenSearch cluster (dedicated node configuration)
- Dedicated crawl servers
- Integration with monitoring and log collection infrastructure

**Scalability**:

- Documents: hundreds of millions possible
- Horizontal scaling via OpenSearch shard splitting

**Enterprise Features**:

- Department-specific label management
- Detailed access logging
- Integration with other systems via API

.. note::

   For large-scale deployments, we recommend using `Commercial Support <../support-services.html>`__.

----

Technical Use Cases
===================

Internal Wiki / Knowledge Base Search
-------------------------------------

**Overview**: Enable cross-search across Confluence, MediaWiki, and internal wikis.

**Benefits**:

- Unified search across multiple wiki systems
- Automatic crawling based on update frequency
- Wiki page attachments included in search scope

**Implementation**:

1. Install Confluence Data Store plugin
2. Configure connection settings from admin panel
3. Set crawl schedule (e.g., daily)

File Server Unified Search
--------------------------

**Overview**: Search documents on Windows file servers and NAS.

**Supported Protocols**:

- SMB/CIFS (Windows shared folders)
- NFS
- Local file system

**Security**:

- NTLM authentication-based access control
- File ACLs reflected in search results

**Configuration Points**:

- Create dedicated crawl account
- Phased crawling for large file volumes
- Consider network bandwidth

Website Search (Site Search)
----------------------------

**Overview**: Add search functionality to public websites.

**Deployment Methods**:

1. **JavaScript Embed**

   Use Fess Site Search (FSS) to add a search box with just a few lines of JavaScript

2. **API Integration**

   Build custom search UI using the Search API

**FSS Example**:

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

Database Search
---------------

**Overview**: Make data in RDBs searchable.

**Supported Databases**:

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**Use Cases**:

- Customer master search
- Product catalog search
- FAQ database search

**Implementation**:

1. Configure Database Data Store plugin
2. Specify crawl target with SQL query
3. Configure field mapping

----

Summary
=======

Fess, with its flexible design, can accommodate various industries, scales, and use cases.

**For Those Considering Deployment**:

1. First, try Fess with the `Quick Start <../quick-start.html>`__
2. Check required features in the `Documentation <../documentation.html>`__
3. For production deployment, consult `Commercial Support <../support-services.html>`__

**Related Resources**:

- `Article List <../articles.html>`__ - Detailed technical articles
- `Discussion Forum <https://discuss.codelibs.org/c/fessen/>`__ - Community support
- `GitHub <https://github.com/codelibs/fess>`__ - Source code and issue tracking

