==================================
Atlassian Connector
==================================

Overview
========

The Atlassian Connector provides functionality to retrieve data from Atlassian products (Jira, Confluence)
and register it in the |Fess| index.

This feature requires the ``fess-ds-atlassian`` plugin.

Supported Products
==================

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

Prerequisites
=============

1. Plugin installation is required
2. Appropriate authentication credentials for Atlassian products are required
3. For Cloud versions, OAuth 2.0 is available; for Server versions, OAuth 1.0a or Basic authentication is available

Installing the Plugin
---------------------

Install from the admin console under "System" -> "Plugins":

1. Download ``fess-ds-atlassian-X.X.X.jar`` from Maven Central
2. Upload and install from the plugin management screen
3. Restart |Fess|

Configuration
=============

Configure in the admin console under "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - Company Jira/Confluence
   * - Handler Name
     - JiraDataStore or ConfluenceDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

Cloud version (OAuth 2.0) example:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Server version (Basic authentication) example:

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Server version (OAuth 1.0a) example:

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``home``
     - Yes
     - Atlassian instance URL
   * - ``is_cloud``
     - Yes
     - ``true`` for Cloud version, ``false`` for Server version
   * - ``auth_type``
     - Yes
     - Authentication type: ``oauth``, ``oauth2``, ``basic``
   * - ``oauth.consumer_key``
     - For OAuth 1.0a
     - Consumer key (usually ``OauthKey``)
   * - ``oauth.private_key``
     - For OAuth 1.0a
     - RSA private key (PEM format)
   * - ``oauth.secret``
     - For OAuth 1.0a
     - Verification code
   * - ``oauth.access_token``
     - For OAuth 1.0a
     - Access token
   * - ``oauth2.client_id``
     - For OAuth 2.0
     - Client ID
   * - ``oauth2.client_secret``
     - For OAuth 2.0
     - Client secret
   * - ``oauth2.access_token``
     - For OAuth 2.0
     - Access token
   * - ``oauth2.refresh_token``
     - No
     - Refresh token (OAuth 2.0)
   * - ``oauth2.token_url``
     - No
     - Token URL (OAuth 2.0, has default value)
   * - ``basic.username``
     - For Basic auth
     - Username
   * - ``basic.password``
     - For Basic auth
     - Password
   * - ``issue.jql``
     - No
     - JQL (Jira only, advanced search conditions)

Script Configuration
--------------------

For Jira
~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

Available fields:

- ``issue.view_url`` - Issue URL
- ``issue.summary`` - Issue summary
- ``issue.description`` - Issue description
- ``issue.comments`` - Issue comments
- ``issue.last_modified`` - Last modified date

For Confluence
~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

Available fields:

- ``content.view_url`` - Page URL
- ``content.title`` - Page title
- ``content.body`` - Page body
- ``content.comments`` - Page comments
- ``content.last_modified`` - Last modified date

OAuth 2.0 Authentication Setup
==============================

For Cloud Version (Recommended)
-------------------------------

1. Create an application in Atlassian Developer Console
2. Obtain OAuth 2.0 credentials
3. Configure required scopes:

   - Jira: ``read:jira-work``, ``read:jira-user``
   - Confluence: ``read:confluence-content.all``, ``read:confluence-user``

4. Obtain access token and refresh token

OAuth 1.0a Authentication Setup
===============================

For Server Version
------------------

1. Create an Application Link in Jira or Confluence
2. Generate RSA key pair:

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. Register the public key in the Application Link
4. Set the private key in the parameters

Basic Authentication Setup
==========================

Simple Setup for Server Version
-------------------------------

.. warning::
   Basic authentication is not recommended for security reasons. Use OAuth authentication whenever possible.

When using Basic authentication:

1. Prepare a user account with administrator privileges
2. Set the username and password in the parameters
3. Use HTTPS to ensure secure connections

Advanced JQL Search
===================

Filtering Jira Issues with JQL
------------------------------

Crawl only issues matching specific conditions:

::

    # Specific project only
    issue.jql=project = "MYPROJECT"

    # Exclude specific statuses
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # Specify time period
    issue.jql=updated >= -30d

    # Combination of multiple conditions
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

For JQL details, refer to `Atlassian JQL Documentation <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Usage Examples
==============

Crawling Jira Cloud
-------------------

Parameters:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

Script:

::

    url=issue.view_url
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\n\nComments:\n" + issue.comments
    last_modified=issue.last_modified

Crawling Confluence Server
--------------------------

Parameters:

::

    home=https://wiki.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

Script:

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\nComments:\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: ``401 Unauthorized`` or ``403 Forbidden``

**Check**:

1. Verify authentication credentials are correct
2. For Cloud version, verify appropriate scopes are configured
3. For Server version, verify user has appropriate permissions
4. For OAuth 2.0, check token expiration

Connection Errors
-----------------

**Symptom**: ``Connection refused`` or connection timeout

**Check**:

1. Verify ``home`` URL is correct
2. Check firewall settings
3. Verify Atlassian instance is running
4. Verify ``is_cloud`` parameter is correctly set

Cannot Retrieve Data
--------------------

**Symptom**: Crawl succeeds but 0 documents

**Check**:

1. Verify JQL is not too restrictive
2. Verify user has read permission for projects/spaces
3. Verify script settings are correct
4. Check logs for errors

OAuth 2.0 Token Refresh
-----------------------

**Symptom**: Authentication errors occur after some time

**Resolution**:

OAuth 2.0 access tokens have an expiration time. Setting a refresh token enables automatic refresh:

::

    oauth2.refresh_token=your_refresh_token

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Atlassian Developer <https://developer.atlassian.com/>`_
