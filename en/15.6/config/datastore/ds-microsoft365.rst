==================================
Microsoft 365 Connector
==================================

Overview
========

The Microsoft 365 Connector provides functionality to retrieve data from Microsoft 365 services
(OneDrive, OneNote, Teams, SharePoint) and register it in the |Fess| index.

This feature requires the ``fess-ds-microsoft365`` plugin.

Supported Services
==================

- **OneDrive**: User drives, group drives, shared documents
- **OneNote**: Notebooks (sites, users, groups)
- **Teams**: Channels, messages, chats
- **SharePoint Document Libraries**: Document library metadata
- **SharePoint Lists**: Lists and list items
- **SharePoint Pages**: Site pages, news articles

Prerequisites
=============

1. Plugin installation is required
2. Azure AD application registration is required
3. Microsoft Graph API permissions configuration and admin consent is required
4. Java 21 or higher, Fess 15.2.0 or higher

Installing the Plugin
---------------------

Method 1: Direct JAR file placement

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # Place the file
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Method 2: Build from source

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

Restart |Fess| after installation.

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
     - Microsoft 365 OneDrive
   * - Handler Name
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - Enabled
     - On

Common Parameter Configuration
------------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

Common Parameter List
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``tenant``
     - Yes
     - Azure AD tenant ID
   * - ``client_id``
     - Yes
     - App registration client ID
   * - ``client_secret``
     - Yes
     - App registration client secret
   * - ``number_of_threads``
     - No
     - Number of parallel processing threads (default: 1)
   * - ``ignore_error``
     - No
     - Continue processing on errors (default: false)
   * - ``include_pattern``
     - No
     - Regex pattern for content to include
   * - ``exclude_pattern``
     - No
     - Regex pattern for content to exclude
   * - ``default_permissions``
     - No
     - Default role assignment

Azure AD Application Registration
=================================

1. Register an Application in Azure Portal
------------------------------------------

Open Azure Active Directory at https://portal.azure.com:

1. Click "App registrations" -> "New registration"
2. Enter application name
3. Select supported account types
4. Click "Register"

2. Create Client Secret
-----------------------

In "Certificates & secrets":

1. Click "New client secret"
2. Set description and expiration
3. Copy the secret value (cannot be viewed later)

3. Add API Permissions
----------------------

In "API permissions":

1. Click "Add a permission"
2. Select "Microsoft Graph"
3. Select "Application permissions"
4. Add required permissions (see below)
5. Click "Grant admin consent"

Required Permissions by Data Store
==================================

OneDriveDataStore
-----------------

Required permissions:

- ``Files.Read.All``

Conditional permissions:

- ``User.Read.All`` - When user_drive_crawler=true
- ``Group.Read.All`` - When group_drive_crawler=true
- ``Sites.Read.All`` - When shared_documents_drive_crawler=true

OneNoteDataStore
----------------

Required permissions:

- ``Notes.Read.All``

Conditional permissions:

- ``User.Read.All`` - When user_note_crawler=true
- ``Group.Read.All`` - When group_note_crawler=true
- ``Sites.Read.All`` - When site_note_crawler=true

TeamsDataStore
--------------

Required permissions:

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

Conditional permissions:

- ``Chat.Read.All`` - When specifying chat_id
- ``Files.Read.All`` - When append_attachment=true

SharePointDocLibDataStore
-------------------------

Required permissions:

- ``Files.Read.All``
- ``Sites.Read.All``

Or ``Sites.Selected`` (when site_id specified, configuration needed per site)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Required permissions:

- ``Sites.Read.All``

Or ``Sites.Selected`` (when site_id specified, configuration needed per site)

Script Configuration
====================

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Available fields:

- ``file.name`` - File name
- ``file.description`` - File description
- ``file.contents`` - Text content
- ``file.mimetype`` - MIME type
- ``file.filetype`` - File type
- ``file.created`` - Creation date
- ``file.last_modified`` - Last modified date
- ``file.size`` - File size
- ``file.web_url`` - URL to open in browser
- ``file.roles`` - Access permissions

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

SharePoint Document Libraries
-----------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

Usage Examples
==============

Crawling All OneDrive Drives
----------------------------

Parameters:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

Script:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Crawling Teams Messages from Specific Team
------------------------------------------

Parameters:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+09:00

Script:

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: ``Authentication failed`` or ``Insufficient privileges``

**Check**:

1. Verify tenant ID, client ID, and client secret are correct
2. Verify required API permissions are granted in Azure Portal
3. Verify admin consent has been granted
4. Check client secret expiration

API Rate Limit Errors
---------------------

**Symptom**: ``429 Too Many Requests``

**Resolution**:

1. Reduce ``number_of_threads`` (set to 1 or 2)
2. Increase crawl interval
3. Set ``ignore_error=true`` for continued processing

Cannot Retrieve Data
--------------------

**Symptom**: Crawl succeeds but 0 documents

**Check**:

1. Verify target data exists
2. Verify API permissions are correctly configured
3. Check user/group drive crawler settings
4. Check logs for error messages

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-gsuite` - Google Workspace Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
