==================================
Dropbox Connector
==================================

Overview
========

The Dropbox Connector provides functionality to retrieve files from Dropbox cloud storage
and register them in the |Fess| index.

This feature requires the ``fess-ds-dropbox`` plugin.

Supported Services
==================

- Dropbox (File Storage)
- Dropbox Paper (Documents)

Prerequisites
=============

1. Plugin installation is required
2. A Dropbox developer account and application creation is required
3. Access token acquisition is required

Installing the Plugin
---------------------

Install from the admin console under "System" -> "Plugins":

1. Download ``fess-ds-dropbox-X.X.X.jar`` from Maven Central
2. Upload and install from the plugin management screen
3. Restart |Fess|

Or refer to :doc:`../../admin/plugin-guide` for details.

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
     - Company Dropbox
   * - Handler Name
     - DropboxDataStore or DropboxPaperDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Parameter
     - Required
     - Description
   * - ``access_token``
     - Yes
     - Dropbox access token (generated in App Console)
   * - ``basic_plan``
     - No
     - Set to ``true`` for individual accounts, ``false`` for team accounts (default: ``false``)
   * - ``max_size``
     - No
     - Maximum file size for indexing in bytes (default: ``10000000``)
   * - ``number_of_threads``
     - No
     - Number of threads for crawling (default: ``1``)
   * - ``ignore_folder``
     - No
     - Whether to skip folder metadata (default: ``true``)
   * - ``ignore_error``
     - No
     - Whether to ignore errors during content extraction (default: ``true``)
   * - ``supported_mimetypes``
     - No
     - Regex patterns for allowed MIME types, comma-separated (default: ``.*``)
   * - ``include_pattern``
     - No
     - URL pattern to include in crawling
   * - ``exclude_pattern``
     - No
     - URL pattern to exclude from crawling
   * - ``default_permissions``
     - No
     - Default permissions for indexed documents, comma-separated
   * - ``max_cached_content_size``
     - No
     - Maximum content size cached in memory in bytes (default: ``1048576``)

Script Configuration
--------------------

For Dropbox Files
~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Available fields:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``file.url``
     - File preview link
   * - ``file.contents``
     - File text content
   * - ``file.mimetype``
     - File MIME type
   * - ``file.filetype``
     - File type
   * - ``file.name``
     - File name
   * - ``file.path_display``
     - File path
   * - ``file.size``
     - File size (bytes)
   * - ``file.client_modified``
     - Last modified date on client side
   * - ``file.server_modified``
     - Last modified date on server side
   * - ``file.roles``
     - File access permissions
   * - ``file.id``
     - Dropbox file ID
   * - ``file.path_lower``
     - Lower-cased file path
   * - ``file.parent_shared_folder_id``
     - Parent shared folder ID
   * - ``file.content_hash``
     - Content hash
   * - ``file.rev``
     - File revision

For Dropbox Paper
~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Available fields:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``paper.url``
     - Paper document preview link
   * - ``paper.contents``
     - Paper document text content
   * - ``paper.mimetype``
     - MIME type
   * - ``paper.filetype``
     - File type
   * - ``paper.title``
     - Paper document title
   * - ``paper.owner``
     - Paper document owner
   * - ``paper.roles``
     - Document access permissions
   * - ``paper.revision``
     - Paper document revision

Dropbox Authentication Setup
============================

Access Token Acquisition Steps
------------------------------

1. Create an App in Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access https://www.dropbox.com/developers/apps:

1. Click "Create app"
2. Select "Scoped access" for API type
3. Select "Full Dropbox" or "App folder" for access type
4. Enter app name and create

2. Configure Permissions
~~~~~~~~~~~~~~~~~~~~~~~~

In the "Permissions" tab, select required permissions:

**Required permissions for file crawling**:

- ``files.metadata.read`` - Read file metadata
- ``files.content.read`` - Read file content
- ``sharing.read`` - Read sharing information

**Additional permissions for Paper crawling**:

- ``files.content.read`` - Read Paper documents

3. Generate Access Token
~~~~~~~~~~~~~~~~~~~~~~~~

In the "Settings" tab:

1. Scroll to "Generated access token" section
2. Click "Generate" button
3. Copy the generated token (this token is only displayed once)

.. warning::
   Keep your access token secure. Anyone with this token can access
   your Dropbox account.

4. Configure Token
~~~~~~~~~~~~~~~~~~

Set the obtained token in the parameters:

::

    access_token=sl.your-dropbox-token-here

Individual Account Settings
===========================

Using Individual Accounts
-------------------------

For individual accounts (not team accounts),
set the ``basic_plan`` parameter to ``true``:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

When ``false`` (default), it operates as a team account and crawls files from team members and team folders.
When ``true``, it operates as an individual account and crawls files directly from the account.

Usage Examples
==============

Crawling All Dropbox Files
--------------------------

Parameters:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

Crawling Dropbox Paper Documents
--------------------------------

Parameters:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Script:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

Crawling with Permissions
-------------------------

Parameters:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    default_permissions={role}admin

Script (Dropbox Files):

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Script (Dropbox Paper):

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Crawling Specific File Types Only
----------------------------------

Filtering in script:

::

    # PDF and Word files only
    if (file.mimetype == "application/pdf" || file.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        last_modified=file.client_modified
    }

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: ``Invalid access token`` or ``401 Unauthorized``

**Check**:

1. Verify access token is correctly copied
2. Verify token has not expired (use long-lived tokens)
3. Verify required permissions are granted in Dropbox App Console
4. Verify app is not disabled

Cannot Retrieve Files
---------------------

**Symptom**: Crawl succeeds but 0 files

**Check**:

1. Verify app's "Access type" is appropriate:

   - "Full Dropbox": Can access entire Dropbox
   - "App folder": Can only access specific folder

2. Verify required permissions are granted:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Verify files exist in Dropbox account

API Rate Limit Errors
---------------------

**Symptom**: ``429 Too Many Requests`` error

**Resolution**:

1. For Basic plan, set ``basic_plan=true``
2. Increase crawl interval
3. Use multiple access tokens for load distribution

Paper Documents Cannot Be Retrieved
------------------------------------

**Symptom**: Paper documents are not crawled

**Check**:

1. Verify handler name is ``DropboxPaperDataStore``
2. Verify ``files.content.read`` permission is included
3. Verify Paper documents actually exist

When There Are Many Files
-------------------------

**Symptom**: Crawling takes a long time or times out

**Resolution**:

1. Split data stores into multiple (e.g., by folder)
2. Distribute load with schedule settings
3. For Basic plan, note API rate limits

Permissions and Access Control
==============================

Reflecting Dropbox Sharing Permissions
--------------------------------------

Dropbox sharing settings can be reflected in Fess permissions:

Parameters:

::

    access_token=sl.your-dropbox-token-here
    default_permissions={role}dropbox-users

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.roles
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

``file.roles`` or ``paper.roles`` contain Dropbox sharing information.

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-box` - Box Connector
- :doc:`ds-gsuite` - Google Workspace Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
