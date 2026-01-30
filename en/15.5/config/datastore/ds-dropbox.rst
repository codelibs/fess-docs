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

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
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
     - Set to ``true`` for Basic plan (default: ``false``)

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

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj

Basic Plan Settings
===================

Dropbox Basic Plan Limitations
------------------------------

For Dropbox Basic plan, API limits differ.
Set the ``basic_plan`` parameter to ``true``:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    basic_plan=true

This enables processing that accommodates API rate limits.

Usage Examples
==============

Crawling All Dropbox Files
--------------------------

Parameters:

::

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
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

    access_token=sl.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIj
    basic_plan=false

Script:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

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

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-box` - Box Connector
- :doc:`ds-gsuite` - Google Workspace Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
