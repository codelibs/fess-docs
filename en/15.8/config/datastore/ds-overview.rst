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
     - Crawl Google Drive
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
2. Go to "System" -> "Plugin"
3. Click the "Install" button
4. Select the plugin from the "Remote" tab (or upload a JAR file from the "Local" tab)
5. Click "Install"
6. Restart |Fess|

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
     - Handler name for the connector (e.g., ``CsvDataStore``)
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
The left side of each line is a |Fess| index field; the right side is the field obtained from the connector.

The following example is for a CSV connector whose header columns are ``link``, ``subject``, and ``body``:

::

    url=link
    title=subject
    content=body

.. note::

   Field names referenced in scripts differ per connector.
   Box/Dropbox/Google Drive/OneDrive reference the fetched object with a prefix: ``file.*``; Slack uses ``message.*``; Jira uses ``issue.*``.
   CSV, JSON, and Database connectors do NOT use a prefix; fields are referenced directly:

   - CSV: header column names (when ``has_header_line=true``), or ``cell1``, ``cell2``, ... (1-based column index); plus ``csvfile`` and ``csvfilename``.
   - JSON: JSON object field names.
   - Database: column names (aliases) from the SELECT result.

   Refer to each connector's individual documentation for details.

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
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``readInterval``
     - ``0``
     - Delay in milliseconds between processing each record. Increase this value to
       reduce load on the external service.
   * - ``script_type``
     - ``groovy``
     - Type of script engine used for index field mapping. Only ``groovy`` is available by default.

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

When investigating issues, adjust the log level. Datastore crawling runs in the crawler process, so you must edit the crawler's log configuration file:

``app/WEB-INF/env/crawler/resources/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ds" level="DEBUG"/>

Reference Information
=====================

- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../../admin/plugin-guide` - Plugin Management Guide
- :doc:`../../api/admin/api-admin-dataconfig` - Data Store Configuration API
