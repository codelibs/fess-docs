============================================================
Part 7: Search Strategy for the Cloud Storage Era -- Cross-Search Across Google Drive, SharePoint, and Box
============================================================

Introduction
============

For many organizations, using cloud storage has become the norm.
However, it is not uncommon for different departments or use cases to rely on different cloud storage services.
Time spent wondering "Was that file on Google Drive, SharePoint, or Box?" reduces productivity.

In this article, we integrate multiple cloud storage services with Fess and build an environment where all cloud-hosted files can be searched from a single search box.

Target Audience
===============

- Administrators of organizations that use multiple cloud storage services
- Those who find searching across cloud storage challenging
- Those who understand the basic concepts of OAuth authentication

Scenario
========

A company uses the following cloud storage services:

.. list-table:: Cloud Storage Usage
   :header-rows: 1
   :widths: 25 35 40

   * - Service
     - Department
     - Primary Use
   * - Google Drive
     - Sales & Marketing
     - Proposals, reports, spreadsheets
   * - SharePoint Online
     - Company-wide
     - Internal portal, shared documents
   * - Box
     - Legal & Accounting
     - Contracts, invoices, confidential documents

Preparing for Cloud Storage Integration
=========================================

Installing Data Store Plugins
------------------------------------

The following plugins are used for crawling cloud storage:

- ``fess-ds-gsuite``: Crawling Google Drive / Google Workspace
- ``fess-ds-microsoft365``: Crawling SharePoint Online / OneDrive
- ``fess-ds-box``: Crawling Box

Install them from [System] > [Plugins] in the admin console.

Setting Up OAuth Authentication
--------------------------------

To access cloud storage APIs, OAuth authentication must be configured.
Register an application in each service's management console and obtain the client ID and secret.

**Common Steps**

1. Register an application in each service's management console
2. Configure the required API scopes (permissions) (read-only access is sufficient)
3. Obtain the client ID and client secret
4. Enter these credentials in the Fess data store settings

Configuring Each Service
=========================

Google Drive Configuration
---------------------------

Add Google Drive files to the search targets.

**Preparation in Google Cloud Console**

1. Create a project in Google Cloud Console
2. Enable the Google Drive API
3. Create a service account and download the JSON key file
4. Share the target drives or folders with the service account

**Configuration in Fess**

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select handler: GoogleDriveDataStore
3. Configure parameters and scripts
4. Set label: ``google-drive``

**Parameter Configuration Example**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**Script Configuration Example**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

Set the ``private_key``, ``private_key_id``, and ``client_email`` values from the service account's JSON key file. Google-native formats such as Google Docs, Spreadsheets, and Slides can also be extracted and searched as text.

SharePoint Online Configuration
---------------------------------

Add SharePoint Online document libraries to the search targets.

**Preparation in Entra ID (Azure AD)**

1. Register an application in Entra ID
2. Configure Microsoft Graph API permissions (e.g., Sites.Read.All)
3. Create a client secret or certificate

**Configuration in Fess**

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select handler: SharePointDocLibDataStore (for document libraries; SharePointListDataStore, SharePointPageDataStore, and OneDriveDataStore are also available depending on the use case)
3. Configure parameters and scripts
4. Set label: ``sharepoint``

**Parameter Configuration Example**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**Script Configuration Example**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

Set ``tenant``, ``client_id``, and ``client_secret`` to the values obtained from the Entra ID application registration. Specifying ``site_id`` limits crawling to a specific site. If omitted, all accessible sites will be crawled.

Box Configuration
------------------

Add Box files to the search targets.

**Preparation in Box Developer Console**

1. Create a custom application in the Box Developer Console
2. Select "Server Authentication (with Client Credentials)" as the authentication method
3. Request application authorization from the administrator

**Configuration in Fess**

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select handler: BoxDataStore
3. Configure parameters and scripts
4. Set label: ``box``

**Parameter Configuration Example**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**Script Configuration Example**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

Set the authentication credentials from the custom application created in the Box Developer Console. Use ``supported_mimetypes`` to filter crawl targets by file type using a regular expression.

Optimizing Cross-Search
=========================

Leveraging Incremental Crawling
---------------------------------

When crawling cloud storage, incremental crawling -- fetching only files updated since the last crawl rather than retrieving all files every time -- is more efficient.

Check whether incremental crawling options are available in each plugin's settings.
Incremental crawling reduces the number of API calls and shortens crawl times.

Search Result URLs
-------------------

For documents crawled from cloud storage, clicking a link in the search results opens the file in the respective service's web UI.
This is a natural experience for users, and no special configuration is typically required.

Operational Considerations
===========================

OAuth Token Renewal
--------------------

When integrating with cloud storage, pay attention to OAuth token expiration.

- **Google Drive**: With service accounts, tokens are automatically refreshed
- **SharePoint Online**: Client secrets have an expiration date and must be renewed periodically
- **Box**: Application re-authorization may be required in some cases

Register token expiration dates in your calendar to prevent crawl interruptions caused by expired credentials.

Monitoring API Usage
---------------------

Cloud storage APIs have usage limits.
When crawling large numbers of files, monitor API usage and adjust crawl settings to avoid exceeding the limits.

Permissions and Security
-------------------------

Configure read-only access permissions for the Fess service account used with cloud storage.
Write permissions are unnecessary and should be avoided following the principle of minimizing security risk.

Additionally, by combining this with the role-based search covered in Part 5, you can also control search results in accordance with the cloud storage permission structure.

Summary
=======

In this article, we integrated three cloud storage services -- Google Drive, SharePoint Online, and Box -- with Fess to build a cross-search environment.

- Data store plugin and OAuth authentication configuration for each cloud storage service
- Distinguishing and filtering information sources using labels
- Optimizing the search experience with incremental crawling
- OAuth token management and API usage monitoring

This creates an environment where users can instantly find the files they need without having to think about which cloud service they are stored in.

In the next article, we will cover the tuning cycle for continuously improving search quality.

References
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin List <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
