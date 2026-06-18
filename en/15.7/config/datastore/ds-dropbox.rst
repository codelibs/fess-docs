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
   :widths: 25 15 60

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
     - Maximum content size to cache in memory in bytes. Content exceeding this size is written to a temporary file (default: ``1048576``)
   * - ``readInterval``
     - No
     - Wait time in milliseconds inserted between processing each record (default: ``0``)

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
     - Last modified date on the client side
   * - ``file.server_modified``
     - Last modified date on the server side
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
=============================

Account Type and Access Token
------------------------------

This connector switches between two operating modes via the ``basic_plan`` parameter.
The type of app and access token you need to create differs between modes, so confirm this first.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Mode
     - ``basic_plan``
     - Description
   * - Team account (default)
     - ``false``
     - For Dropbox Business (team) accounts. Requires an access token with team administrator privileges, and crawls files of team members and team folders across the organization.
   * - Individual account
     - ``true``
     - For personal (non-team) accounts. Uses a standard scoped access token and crawls files directly within that account.

.. note::
   In the default mode (``basic_plan=false``), team administration APIs (team member listing, per-member file access, team folders) are used,
   so a Dropbox Business account and a token with team administrator privileges are required. If you are using a personal account, make sure to set ``basic_plan=true``.

Access Token Acquisition Steps
-------------------------------

1. Create an App in Dropbox App Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access https://www.dropbox.com/developers/apps:

1. Click "Create app"
2. Select "Scoped access" for API type
3. Select the access type (for crawling across team accounts, "Full Dropbox" is recommended)
4. Enter app name and create

2. Configure Permissions
~~~~~~~~~~~~~~~~~~~~~~~~

In the "Permissions" tab, select the required permissions:

**Required permissions for crawling files and Paper**:

- ``files.metadata.read`` - Read file metadata
- ``files.content.read`` - Read content of files and Paper documents
- ``sharing.read`` - Read sharing information

**Additional permissions required for team accounts (``basic_plan=false``)**:

- ``members.read`` - Read team member listing
- Access permissions for team data / team spaces (required for crawling per-member files and team folders)

.. note::
   In team account mode, files are accessed as a team administrator on behalf of each member and team folder.
   Enable the team-related permissions above in the Permissions tab, and generate a token for a team administrator.

3. Generate Access Token
~~~~~~~~~~~~~~~~~~~~~~~~

In the "Settings" tab:

1. Scroll to the "Generated access token" section
2. Click the "Generate" button
3. Copy the generated token (this token is only displayed once)

.. warning::
   Keep your access token secure. Anyone with this token can
   access your Dropbox account.

4. Configure Token
~~~~~~~~~~~~~~~~~~

Set the obtained token in the parameters:

::

    access_token=sl.your-dropbox-token-here

Individual Account Settings
============================

Using Individual Accounts
--------------------------

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
---------------------------------

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

To index only specific MIME types, specify regex patterns for the allowed MIME types
in the ``supported_mimetypes`` parameter, separated by commas.

.. note::
   Each line of a data store script is evaluated as an independent expression in the form ``field=expression``.
   Therefore, it is not possible to assign multiple fields together inside a multi-line ``if`` block.
   Use the ``supported_mimetypes`` parameter — not the script — to filter by MIME type.

Parameters (PDF and Word files only):

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    supported_mimetypes=application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

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
   - "App folder": Can only access a specific folder

2. Verify required permissions are granted:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Verify files exist in the Dropbox account

API Rate Limit Errors
---------------------

**Symptom**: ``429 Too Many Requests`` error

**Resolution**:

1. Set ``readInterval`` to add a wait between processing each file
2. Reduce ``number_of_threads`` to lower the number of concurrent requests
3. Split the data store into multiple instances (e.g., by folder) and stagger the schedules

.. note::
   ``basic_plan`` is a parameter that switches the account type (team / individual) and does not affect
   rate limit adjustment. Set it correctly according to your account type.

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

1. Split data stores into multiple instances (e.g., by folder)
2. Distribute load with schedule settings
3. For the Basic plan, pay attention to API rate limits

Permissions and Access Control
===============================

Reflecting Dropbox Sharing Permissions
---------------------------------------

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
