==================================
Data Store Connector Overview
==================================

Overview
========

|Fess| Data Store Connectors provide functionality to retrieve and index content from data sources
other than websites and file systems.

Using Data Store Connectors, you can make data searchable from the following sources:

- Cloud storage (Box, Dropbox, Google Drive, OneDrive)
- Collaboration tools (Confluence, Jira, Slack)
- Databases (MySQL, PostgreSQL, Oracle, etc.)
- Other systems (Git, Salesforce, Elasticsearch, etc.)

Available Connectors
====================

|Fess| provides connectors for various data sources.
Many connectors are available as plugins and can be installed as needed.

Cloud Storage
-------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connector
     - Plugin
     - Description
   * - :doc:`ds-box`
     - fess-ds-box
     - Crawl files and folders from Box.com
   * - :doc:`ds-dropbox`
     - fess-ds-dropbox
     - Crawl files and folders from Dropbox
   * - :doc:`ds-gsuite`
     - fess-ds-gsuite
     - Crawl Google Drive, Gmail, etc.
   * - :doc:`ds-microsoft365`
     - fess-ds-microsoft365
     - Crawl OneDrive, SharePoint, etc.

Collaboration Tools
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connector
     - Plugin
     - Description
   * - :doc:`ds-atlassian`
     - fess-ds-atlassian
     - Crawl Confluence and Jira
   * - :doc:`ds-slack`
     - fess-ds-slack
     - Crawl Slack messages and files

Development & Operations Tools
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connector
     - Plugin
     - Description
   * - :doc:`ds-git`
     - fess-ds-git
     - Crawl source code from Git repositories
   * - :doc:`ds-elasticsearch`
     - fess-ds-elasticsearch
     - Retrieve data from Elasticsearch/OpenSearch
   * - :doc:`ds-salesforce`
     - fess-ds-salesforce
     - Crawl Salesforce objects

Databases & Files
-----------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Connector
     - Plugin
     - Description
   * - :doc:`ds-database`
     - fess-ds-db
     - Retrieve data from JDBC-compatible databases
   * - :doc:`ds-csv`
     - fess-ds-csv
     - Retrieve data from CSV files
   * - :doc:`ds-json`
     - fess-ds-json
     - Retrieve data from JSON files

Installing Connectors
=====================

Installing Plugins
------------------

Data Store Connector plugins can be installed from the admin UI.

1. Log in to the admin console
2. Navigate to "System" -> "Plugins"
3. Search for the target plugin in the "Available" tab
4. Click "Install"
5. Restart |Fess|

Data Store Configuration Basics
===============================

Data Store Connector configuration is done in the admin console under "Crawler" -> "Data Store".

Common Configuration Items
--------------------------

Configuration items common to all Data Store Connectors:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Description
   * - Name
     - Identifier name for the configuration
   * - Handler Name
     - Handler name for the connector (e.g., ``BoxDataStore``)
   * - Description
     - A free-text description of the configuration
   * - Parameters
     - Connector-specific configuration parameters (key=value format)
   * - Script
     - Index field mapping script
   * - Permissions
     - Access permissions for crawled documents (e.g., ``{role}guest``)
   * - Virtual Hosts
     - Virtual host keys to restrict which site this config applies to
   * - Sort Order
     - Display order in the configuration list
   * - Boost
     - Search result priority
   * - Enabled
     - Whether to enable this configuration

Parameter Configuration
-----------------------

Parameters are specified in ``key=value`` format, separated by newlines:

::

    api.key=xxxxxxxxxxxxx
    folder.id=0
    max.depth=3

Script Configuration
--------------------

Scripts map retrieved data to |Fess| index fields.
The example below uses the ``data.*`` prefix, which is used by CSV and JSON connectors.
Other connectors use their own prefix: ``file.*`` for Box/Dropbox/Google Drive/OneDrive,
``message.*`` for Slack, ``issue.*`` for Jira, etc.
See each connector's documentation for the available fields.

::

    url=data.url
    title=data.name
    content=data.content
    mimetype=data.mimetype
    filetype=data.filetype
    filename=data.filename
    created=data.created
    lastModified=data.lastModified
    contentLength=data.contentLength

Authentication Configuration
============================

Many Data Store Connectors require authentication (OAuth 2.0, API keys, service accounts, etc.).
The specific authentication parameters differ for each connector.
Refer to the individual connector documentation for the required settings.

Common Parameters
=================

The following parameter is inherited from ``AbstractDataStore`` and available in all connectors:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Default
     - Description
   * - ``readInterval``
     - ``0``
     - Delay in milliseconds between processing each record. Increase this value to
       reduce load on the external service.

Troubleshooting
===============

Connector Not Displayed
-----------------------

1. Verify that the plugin is correctly installed
2. Restart |Fess|
3. Check logs for errors

Authentication Errors
---------------------

1. Verify that authentication information is correct
2. Check token expiration
3. Verify that required permissions are granted
4. Verify that API access is allowed on the service side

Cannot Retrieve Data
--------------------

1. Verify that parameter format is correct
2. Check access permissions for target folders/files
3. Check filter settings
4. Check logs for detailed error messages

Debug Configuration
-------------------

When investigating issues, adjust the log level:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Reference Information
=====================

- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../../admin/plugin-guide` - Plugin Management Guide
- :doc:`../../api/admin/api-admin-dataconfig` - Data Store Configuration API
