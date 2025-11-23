====================================
Fess Architecture and Key Features
====================================

Overview
========

This page describes Fess's key features and architecture from a component perspective.
Fess employs a modularized design to facilitate the construction of search systems.

Overall Architecture
====================

Fess consists of the following main components:

.. figure:: ../resources/images/en/architecture-overview.png
   :scale: 100%
   :alt: Fess Architecture Overview
   :align: center

   Fess Architecture Overview

Main Components
===============

1. Crawler Subsystem
--------------------

The crawler subsystem is responsible for collecting documents from various data sources.

**Main Classes and Features:**

Crawler
~~~~~~~

- **Role**: Central class for crawl processing
- **Key Features**:

  - Document collection from websites, file systems, and data stores
  - Target selection based on crawl configuration
  - Crawl job execution management
  - Session management for crawl results

- **Execution Modes**:

  - Scheduled periodic execution
  - Manual execution from admin interface
  - Command-line execution

WebCrawler
~~~~~~~~~~

- **Role**: Website crawling
- **Key Features**:

  - Fetching and parsing HTML pages
  - Link extraction and traversal
  - Support for JavaScript-based websites
  - Support for authenticated websites (BASIC/DIGEST/NTLM/FORM)
  - robots.txt compliance

FileCrawler
~~~~~~~~~~~

- **Role**: File system crawling
- **Key Features**:

  - Traversing local file systems
  - Network drive access (SMB/CIFS)
  - File format detection and parser selection
  - Permission-based access control

DataStoreCrawler
~~~~~~~~~~~~~~~~

- **Role**: External data store crawling
- **Key Features**:

  - Data retrieval from databases
  - Cloud storage integration (Google Drive, Dropbox, Box, etc.)
  - Groupware integration (Office 365, Slack, Confluence, etc.)
  - Plugin-based extensibility

CrawlConfig
~~~~~~~~~~~

- **Role**: Crawl configuration management
- **Key Features**:

  - Definition of target URLs or paths for crawling
  - Crawl depth limitation
  - Crawl interval configuration
  - Exclusion pattern specification
  - Label assignment

2. Indexing Subsystem
---------------------

The indexing subsystem converts collected documents into searchable format.

DocumentParser
~~~~~~~~~~~~~~

- **Role**: Document parsing and text extraction
- **Key Features**:

  - Support for various file formats using Apache Tika
  - Metadata extraction
  - Automatic character encoding detection
  - Automatic language detection

Indexer
~~~~~~~

- **Role**: Index registration in OpenSearch/Elasticsearch
- **Key Features**:

  - Document index creation
  - Bulk indexing for improved performance
  - Index optimization
  - Deletion of old documents

FieldMapper
~~~~~~~~~~~

- **Role**: Field mapping definition
- **Key Features**:

  - Document field definition
  - Custom field addition
  - Field type specification (text, keyword, date, etc.)
  - Multilingual analyzer configuration

3. Search Subsystem
-------------------

The search subsystem processes search queries from users and returns results.

SearchService
~~~~~~~~~~~~~

- **Role**: Core of search processing
- **Key Features**:

  - Query parsing and optimization
  - Query execution against OpenSearch/Elasticsearch
  - Search result ranking
  - Faceted search support
  - Highlighting

QueryProcessor
~~~~~~~~~~~~~~

- **Role**: Search query preprocessing
- **Key Features**:

  - Query normalization
  - Synonym expansion
  - Stop word processing
  - Query correction

SuggestService
~~~~~~~~~~~~~~

- **Role**: Suggestion feature provision
- **Key Features**:

  - Input completion candidate generation
  - Popular search keyword provision
  - Custom dictionary utilization

RankingService
~~~~~~~~~~~~~~

- **Role**: Search result ranking adjustment
- **Key Features**:

  - Document boosting
  - Field boosting
  - Custom scoring
  - Relevance adjustment

4. Administration Subsystem
----------------------------

The administration subsystem manages Fess configuration and operation.

AdminConsole
~~~~~~~~~~~~

- **Role**: Web-based administration interface
- **Key Features**:

  - Crawl configuration management
  - Scheduler settings
  - User and role management
  - System settings
  - Log viewing

Scheduler
~~~~~~~~~

- **Role**: Job schedule management
- **Key Features**:

  - Periodic execution of crawl jobs
  - Periodic execution of index optimization
  - Log rotation
  - Schedule configuration with Cron expressions

BackupManager
~~~~~~~~~~~~~

- **Role**: Backup and restore
- **Key Features**:

  - Configuration data backup
  - Index snapshots
  - Restore functionality
  - Automatic backup scheduling

5. Authentication and Authorization Subsystem
----------------------------------------------

The authentication and authorization subsystem manages security and access control.

AuthenticationManager
~~~~~~~~~~~~~~~~~~~~~

- **Role**: User authentication management
- **Key Features**:

  - Local authentication
  - LDAP/Active Directory integration
  - SAML integration
  - OpenID Connect integration
  - Role-based access control (RBAC)

RoleManager
~~~~~~~~~~~

- **Role**: Role and access permission management
- **Key Features**:

  - Role definition
  - Role assignment to users
  - Document-level access control
  - Search result filtering

6. API Layer
------------

The API layer provides integration with external systems.

SearchAPI
~~~~~~~~~

- **Role**: Search API provision
- **Key Features**:

  - REST API-based search
  - JSON-formatted responses
  - OpenSearch compatibility
  - GSA (Google Search Appliance) compatible API

AdminAPI
~~~~~~~~

- **Role**: Administration API provision
- **Key Features**:

  - CRUD operations for crawl configuration
  - Index management
  - Scheduler control
  - System information retrieval

7. Data Storage
---------------

Data storage handles data persistence for Fess.

ConfigStore
~~~~~~~~~~~

- **Role**: Configuration data storage
- **Key Features**:

  - Crawl configuration persistence
  - System configuration storage
  - User and role information management
  - H2 database or external DB usage

SearchEngine
~~~~~~~~~~~~

- **Role**: Search engine integration
- **Key Features**:

  - Communication with OpenSearch/Elasticsearch
  - Index management
  - Query execution
  - Clustering support

Plugin Architecture
===================

Fess can be extended through plugins.

DataStore Plugins
-----------------

- **Role**: Connection to external data sources
- **Available Plugins**:

  - Atlassian (Confluence/Jira)
  - Box
  - CSV
  - Database
  - Dropbox
  - Git/GitBucket
  - Google Drive
  - Office 365
  - S3
  - Slack
  - Others

Theme Plugins
-------------

- **Role**: Search interface customization
- **Available Plugins**:

  - Simple Theme
  - Classic Theme

Ingester Plugins
----------------

- **Role**: Pre- and post-processing of index data
- **Available Plugins**:

  - Logger
  - NDJSON

Script Plugins
--------------

- **Role**: Script-based customization
- **Available Plugins**:

  - Groovy
  - OGNL

Configuration Management
========================

FessConfig
----------

- **Role**: Centralized system configuration management
- **Main Configuration Items**:

  - General system settings
  - Crawl settings
  - Search settings
  - Authentication settings
  - Notification settings
  - Performance settings

DynamicProperties
-----------------

- **Role**: Dynamic configuration management
- **Key Features**:

  - Runtime configuration changes
  - Environment variable usage
  - Profile-specific configuration

Summary
=======

Fess realizes a powerful full-text search system through the collaboration of these components.
Each component is designed with loose coupling and can be customized or extended as needed.

For more detailed developer information, see:

- `JavaDoc <https://fess.codelibs.org/apidocs/index.html>`__
- `XRef <https://fess.codelibs.org/xref/index.html>`__
- `Developer Guide <dev/index.html>`__
- `GitHub Repository <https://github.com/codelibs/fess>`__
