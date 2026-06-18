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
-------------------------------

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
   * - ``max_content_length``
     - No
     - Maximum size of content to retrieve (default: -1, unlimited)
   * - ``cache_size``
     - No
     - Cache size for user/group information (default: 10000)
   * - ``proxy_host``
     - No
     - HTTP proxy host
   * - ``proxy_port``
     - No
     - HTTP proxy port
   * - ``proxy_username``
     - No
     - Proxy authentication username
   * - ``proxy_password``
     - No
     - Proxy authentication password

Azure AD Application Registration
==================================

1. Register an Application in Azure Portal
------------------------------------------

Open Azure Active Directory at https://portal.azure.com:

1. Click "App registrations" -> "New registration"
2. Enter the application name
3. Select the supported account types
4. Click "Register"

2. Create Client Secret
-----------------------

In "Certificates & secrets":

1. Click "New client secret"
2. Set the description and expiration
3. Copy the secret value (it cannot be viewed later)

3. Add API Permissions
----------------------

In "API permissions":

1. Click "Add a permission"
2. Select "Microsoft Graph"
3. Select "Application permissions"
4. Add the required permissions (see below)
5. Click "Grant admin consent"

Required Permissions by Data Store
====================================

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

Or ``Sites.Selected`` (when site_id is specified, configuration is required per site)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Required permissions:

- ``Sites.Read.All``

Or ``Sites.Selected`` (when site_id is specified, configuration is required per site)

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
- ``file.created`` - Creation date and time
- ``file.last_modified`` - Last modified date and time
- ``file.size`` - File size
- ``file.web_url`` - URL to open in browser
- ``file.url`` - File URL
- ``file.id`` - Drive item ID
- ``file.ctag`` - Change tag (cTag)
- ``file.etag`` - Entity tag (eTag)
- ``file.webdav_url`` - WebDAV URL
- ``file.parent_id`` - Parent folder ID
- ``file.parent_name`` - Parent folder name
- ``file.parent_path`` - Parent folder path
- ``file.roles`` - Access permissions

.. note::

   In addition to the above, Microsoft Graph metadata fields such as ``file.createdby_user``,
   ``file.last_modifiedby_user``, ``file.image``, ``file.video``, and ``file.special_folder``
   are also available.

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

Available fields:

- ``notebook.name`` - Notebook name
- ``notebook.contents`` - Integrated content of sections and pages
- ``notebook.size`` - Content size (character count)
- ``notebook.created`` - Creation date and time
- ``notebook.last_modified`` - Last modified date and time
- ``notebook.web_url`` - URL to open in browser
- ``notebook.roles`` - Access permissions

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

Available fields:

- ``message.title`` - Message title
- ``message.content`` - Message content
- ``message.body`` - Message body (raw data including HTML)
- ``message.subject`` - Message subject
- ``message.summary`` - Message summary
- ``message.importance`` - Importance
- ``message.from`` - Sender information
- ``message.created_date_time`` - Creation date and time
- ``message.last_modified_date_time`` - Last modified date and time
- ``message.last_edited_date_time`` - Last edited date and time
- ``message.deleted_date_time`` - Deletion date and time
- ``message.web_url`` - URL to open in browser
- ``message.id`` - Message ID
- ``message.etag`` - Entity tag
- ``message.locale`` - Locale
- ``message.chat_id`` - Chat ID
- ``message.reply_to_id`` - Reply-to message ID
- ``message.channel_identity`` - Channel identity information (team ID and channel ID)
- ``message.mentions`` - Mention information
- ``message.attachments`` - Attachment information
- ``message.replies`` - Reply messages
- ``message.hosted_contents`` - Inline content (images, etc.)
- ``message.roles`` - Access permissions

Top-level fields (set only for channel messages):

- ``team`` - Team (Microsoft Graph ``Group`` object)
- ``channel`` - Channel (Microsoft Graph ``Channel`` object)
- ``parent`` - Parent message (set when the message is a reply)

SharePoint Document Libraries
------------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

Available fields:

- ``doclib.name`` - Document library name
- ``doclib.description`` - Library description
- ``doclib.content`` - Integrated content for search
- ``doclib.created`` - Creation date and time
- ``doclib.modified`` - Last modified date and time
- ``doclib.url`` - SharePoint URL
- ``doclib.web_url`` - URL to open in browser
- ``doclib.id`` - Document library ID
- ``doclib.type`` - Document type
- ``doclib.site_name`` - Site name
- ``doclib.site_url`` - Site URL
- ``doclib.roles`` - Access permissions

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Available fields:

- ``item.title`` - List item title
- ``item.content`` - Text content
- ``item.created`` - Creation date and time
- ``item.modified`` - Last modified date and time
- ``item.url`` - SharePoint URL
- ``item.web_url`` - URL to open in browser
- ``item.id`` - List item ID
- ``item.content_type`` - Content type
- ``item.fields`` - Map of all fields
- ``item.roles`` - Access permissions

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

Available fields:

- ``page.title`` - Page title
- ``page.content`` - Page content
- ``page.created`` - Creation date and time
- ``page.modified`` - Last modified date and time
- ``page.url`` - SharePoint URL
- ``page.web_url`` - URL to open in browser
- ``page.id`` - Page ID
- ``page.description`` - Page description
- ``page.author`` - Author
- ``page.type`` - Page type (news/article/page)
- ``page.site_name`` - Site name
- ``page.site_url`` - Site URL
- ``page.promotion_state`` - Promotion state
- ``page.roles`` - Access permissions

Additional Parameters by Data Store
=====================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=
    url_filter=
    default_permissions=
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    default_permissions=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
------------------------------

::

    site_id=
    exclude_site_id=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    include_pattern=
    exclude_pattern=
    default_permissions=
    ignore_error=false
    ignore_system_pages=true
    page_type_filter=

Usage Examples
==============

Crawling All OneDrive Drives
-----------------------------

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

Crawling Teams Messages from a Specific Team
---------------------------------------------

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

Crawling a SharePoint List
---------------------------

Parameters:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

Script:

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: ``Authentication failed`` or ``Insufficient privileges``

**Check**:

1. Verify that the tenant ID, client ID, and client secret are correct
2. Verify that the required API permissions are granted in Azure Portal
3. Verify that admin consent has been granted
4. Check the client secret expiration

API Rate Limit Errors
---------------------

**Symptom**: ``429 Too Many Requests``

**Resolution**:

1. Reduce ``number_of_threads`` (set to 1 or 2)
2. Increase the crawl interval
3. Set ``ignore_error=true`` to continue processing

Cannot Retrieve Data
--------------------

**Symptom**: Crawl succeeds but 0 documents

**Check**:

1. Verify that the target data exists
2. Verify that the API permissions are correctly configured
3. Check the user/group drive crawler settings
4. Check the logs for error messages

How to Find the SharePoint Site ID
------------------------------------

Using PowerShell:

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

Or using the Microsoft Graph API:

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

Crawling Large Volumes of Data
-------------------------------

**Resolution**:

1. Split into multiple data stores (per site, per drive, etc.)
2. Use scheduled settings to distribute the load
3. Adjust ``number_of_threads`` for parallel processing
4. Crawl only specific folders/sites

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-gsuite` - Google Workspace Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
