==================================
Google Workspace Connector
==================================

Overview
========

The Google Workspace Connector provides functionality to retrieve files from Google Drive (formerly G Suite)
and register them in the |Fess| index.

This feature requires the ``fess-ds-gsuite`` plugin.

Supported Services
==================

- Google Drive (My Drive, Shared Drives)
- Google Docs, Spreadsheets, Slides, Forms, etc.

Prerequisites
=============

1. Plugin installation is required
2. A Google Cloud Platform project must be created
3. A service account must be created and credentials obtained
4. Domain-wide delegation must be configured for Google Workspace

Plugin Installation
-------------------

Method 1: Place JAR file directly

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Place the file
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Method 2: Install from admin console

1. Open "System" -> "Plugins"
2. Upload the JAR file
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
     - Company Google Drive
   * - Handler Name
     - GSuiteDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``private_key``
     - Yes
     - Service account private key (PEM format, newlines as ``\n``)
   * - ``private_key_id``
     - Yes
     - Private key ID
   * - ``client_email``
     - Yes
     - Service account email address

Script Configuration
--------------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

Available Fields
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``file.name``
     - File name
   * - ``file.description``
     - File description
   * - ``file.contents``
     - File text content
   * - ``file.mimetype``
     - File MIME type
   * - ``file.filetype``
     - File type
   * - ``file.created_time``
     - Creation date/time
   * - ``file.modified_time``
     - Last modified date/time
   * - ``file.web_view_link``
     - Link to open in browser
   * - ``file.url``
     - File URL
   * - ``file.thumbnail_link``
     - Thumbnail link (valid for short period)
   * - ``file.size``
     - File size (bytes)
   * - ``file.roles``
     - Access permissions

For details, see the `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Google Cloud Platform Configuration
===================================

1. Create a Project
-------------------

Access https://console.cloud.google.com/:

1. Create a new project
2. Enter a project name
3. Select organization and location

2. Enable Google Drive API
--------------------------

In "APIs & Services" -> "Library":

1. Search for "Google Drive API"
2. Click "Enable"

3. Create a Service Account
---------------------------

In "APIs & Services" -> "Credentials":

1. Select "Create credentials" -> "Service account"
2. Enter a service account name (e.g., fess-crawler)
3. Click "Create and continue"
4. Skip role assignment
5. Click "Done"

4. Create Service Account Key
-----------------------------

For the created service account:

1. Click on the service account
2. Open the "Keys" tab
3. Click "Add key" -> "Create new key"
4. Select JSON format
5. Save the downloaded JSON file

5. Enable Domain-wide Delegation
--------------------------------

In the service account settings:

1. Check "Enable domain-wide delegation"
2. Click "Save"
3. Copy the "OAuth 2 Client ID"

6. Authorize in Google Workspace Admin Console
----------------------------------------------

Access https://admin.google.com/:

1. Open "Security" -> "Access and data control" -> "API controls"
2. Select "Domain-wide delegation"
3. Click "Add new"
4. Enter the Client ID
5. Enter OAuth scope:

   ::

       https://www.googleapis.com/auth/drive.readonly

6. Click "Authorize"

Credential Configuration
========================

Retrieve Information from JSON File
-----------------------------------

The downloaded JSON file:

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

Set the following information in parameters:

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (keep newlines as ``\n``)
- ``client_email`` -> ``client_email``

Private Key Format
~~~~~~~~~~~~~~~~~~

``private_key`` preserves newlines as ``\n``:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Usage Examples
==============

Crawl Entire Google Drive
-------------------------

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com

Script:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    filename=file.name

Crawl with Permissions
----------------------

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

Script:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

Crawl Only Specific File Types
------------------------------

Google Docs only:

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

Troubleshooting
===============

Authentication Error
--------------------

**Symptom**: ``401 Unauthorized`` or ``403 Forbidden``

**Check**:

1. Verify service account credentials are correct:

   - Is ``private_key`` formatted with ``\n`` for newlines?
   - Is ``private_key_id`` correct?
   - Is ``client_email`` correct?

2. Verify Google Drive API is enabled
3. Verify domain-wide delegation is configured
4. Verify authorization in Google Workspace admin console
5. Verify OAuth scope is correct (``https://www.googleapis.com/auth/drive.readonly``)

Domain-wide Delegation Error
----------------------------

**Symptom**: ``Not Authorized to access this resource/api``

**Resolution**:

1. Verify authorization in Google Workspace admin console:

   - Is the Client ID registered correctly?
   - Is the OAuth scope correct? (``https://www.googleapis.com/auth/drive.readonly``)

2. Verify domain-wide delegation is enabled for the service account

Cannot Retrieve Files
---------------------

**Symptom**: Crawl succeeds but 0 files found

**Check**:

1. Verify files exist in Google Drive
2. Verify service account has read permissions
3. Verify domain-wide delegation is configured correctly
4. Verify access to target user's Drive is possible

API Quota Error
---------------

**Symptom**: ``403 Rate Limit Exceeded`` or ``429 Too Many Requests``

**Resolution**:

1. Check quota in Google Cloud Platform
2. Increase crawl interval
3. Request quota increase if needed

Private Key Format Error
------------------------

**Symptom**: ``Invalid private key format``

**Resolution**:

Verify newlines are correctly formatted as ``\n``:

::

    # Correct
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Incorrect (contains actual newlines)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Crawling Shared Drives
----------------------

.. note::
   To crawl shared drives with a service account,
   the service account must be added as a member of the shared drive.

1. Open the shared drive in Google Drive
2. Click "Manage members"
3. Add the service account email address
4. Set permission level to "Viewer"

Large Number of Files
---------------------

**Symptom**: Crawl takes too long or times out

**Resolution**:

1. Split into multiple data stores
2. Distribute load with scheduled crawling
3. Adjust crawl interval
4. Crawl only specific folders

Permissions and Access Control
==============================

Reflect Google Drive Sharing Permissions
----------------------------------------

Reflect Google Drive sharing settings in Fess permissions:

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

Script:

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles`` contains Google Drive sharing information.

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-microsoft365` - Microsoft 365 Connector
- :doc:`ds-box` - Box Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
