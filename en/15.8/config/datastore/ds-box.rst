==================================
Box Connector
==================================

Overview
========

The Box Connector provides functionality to retrieve files from Box.com cloud storage
and register them in the |Fess| index.

This connector authenticates to the enterprise using JWT (Server Authentication) and
recursively crawls the files accessible to each user in the enterprise by impersonating
(impersonation) each of them. The users to crawl can be narrowed down with the
``filter_term`` parameter.

This feature requires the ``fess-ds-box`` plugin.

Prerequisites
=============

1. Plugin installation is required
2. A Box developer account and application creation is required
3. JWT (JSON Web Token) authentication setup is required

Installing the Plugin
---------------------

Method 1: Direct JAR file placement

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Place the file
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Company Box Storage
   * - Handler Name
     - BoxDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

JWT authentication example:

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=<YOUR_PRIVATE_KEY>
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Parameter List
~~~~~~~~~~~~~~

Authentication Parameters (Required)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``client_id``
     - Yes
     - Box application client ID
   * - ``client_secret``
     - Yes
     - Box application client secret
   * - ``public_key_id``
     - Yes
     - Public key ID
   * - ``private_key``
     - Yes
     - Private key (PEM format, newlines represented as ``\n``)
   * - ``passphrase``
     - Yes
     - Private key passphrase
   * - ``enterprise_id``
     - Yes
     - Box enterprise ID

Crawl Parameters (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Default Value
     - Description
   * - ``max_size``
     - ``10000000``
     - Maximum file size (bytes) to crawl. Default is 10 MB.
   * - ``supported_mimetypes``
     - ``.*``
     - MIME types to crawl (regular expression). Multiple values can be specified separated by commas.
   * - ``include_pattern``
     - (none)
     - URL pattern to include in crawl targets
   * - ``exclude_pattern``
     - (none)
     - URL pattern to exclude from crawl targets
   * - ``number_of_threads``
     - ``1``
     - Number of threads for crawl processing
   * - ``ignore_folder``
     - ``true``
     - Whether to exclude folders from indexing. In the current implementation, folders themselves are not indexed (only files are targeted), so this parameter has no effect.
   * - ``ignore_error``
     - ``true``
     - Whether to continue processing when an error occurs
   * - ``filter_term``
     - (none)
     - Filter condition to narrow down the enterprise users to crawl. If not specified, all enterprise users are targeted.
   * - ``fields``
     - (all fields)
     - Specification of fields to retrieve from the Box API

Connection Parameters (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Parameter
     - Default Value
     - Description
   * - ``base_url``
     - ``https://app.box.com``
     - Base URL used to construct the URL for opening a file in a browser (``file.url``). It does not affect the API endpoints used by the Box SDK.
   * - ``max_retry_count``
     - ``10``
     - Maximum number of retries for API calls
   * - ``proxy_host``
     - (none)
     - HTTP proxy host name
   * - ``proxy_port``
     - (none)
     - HTTP proxy port number
   * - ``refresh_token_interval``
     - ``3540``
     - Token refresh interval (seconds). Default is 59 minutes.

Script Configuration
--------------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Available Fields
~~~~~~~~~~~~~~~~

Primary Fields
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``file.url``
     - Link to open the file in a browser
   * - ``file.contents``
     - Text content of the file
   * - ``file.mimetype``
     - File MIME type
   * - ``file.filetype``
     - File type
   * - ``file.name``
     - File name
   * - ``file.size``
     - File size (bytes)
   * - ``file.created_at``
     - Creation date and time
   * - ``file.modified_at``
     - Last modified date and time
   * - ``file.download_url``
     - Box direct download URL
   * - ``file.id``
     - Box item ID
   * - ``file.description``
     - File description
   * - ``file.extension``
     - File extension
   * - ``file.sha1``
     - SHA1 hash of the file
   * - ``file.path_collection``
     - List of folder paths

Metadata Fields
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``file.type``
     - Item type ("file" or "folder")
   * - ``file.file_version``
     - File version information
   * - ``file.sequence_id``
     - Sequence ID
   * - ``file.etag``
     - ETag hash
   * - ``file.trashed_at``
     - Date and time moved to trash
   * - ``file.purged_at``
     - Date and time permanently deleted
   * - ``file.content_created_at``
     - Content creation date and time
   * - ``file.content_modified_at``
     - Content modified date and time
   * - ``file.created_by``
     - Creator information
   * - ``file.modified_by``
     - Modifier information
   * - ``file.owned_by``
     - Owner information
   * - ``file.shared_link``
     - Shared link information
   * - ``file.parent``
     - Parent folder information
   * - ``file.item_status``
     - Item status
   * - ``file.version_number``
     - Version number
   * - ``file.comment_count``
     - Comment count
   * - ``file.permissions``
     - Permission information
   * - ``file.tags``
     - Tag information
   * - ``file.lock``
     - Lock information
   * - ``file.is_package``
     - Package flag
   * - ``file.is_watermark``
     - Watermark flag
   * - ``file.collections``
     - Collection information
   * - ``file.representations``
     - Representation format information
   * - ``file.api``
     - Box file API object (for retrieving collaboration and permission information)

For details, refer to `Box File Object <https://developer.box.com/reference#file-object>`_.

Box Authentication Setup
========================

JWT Authentication Setup Steps
-------------------------------

1. Create an Application in Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access https://app.box.com/developers/console:

1. Click "Create New App"
2. Select "Custom App"
3. Select "Server Authentication (with JWT)" for authentication method
4. Enter app name and create

2. Application Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the "Configuration" tab:

**Application Scopes**:

- Check "Read all files and folders stored in Box"

**Advanced Features**:

- Click "Generate a Public/Private Keypair"
- Download the generated JSON file (important!)

**App Access Level**:

- Select "App + Enterprise Access"

3. Authorize in Enterprise
~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Box admin console:

1. Open "Apps" -> "Custom Apps"
2. Authorize the created app

4. Obtain Authentication Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obtain the following information from the downloaded JSON file:

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

Private Key Format
~~~~~~~~~~~~~~~~~~

Replace newlines in ``private_key`` with ``\n`` to make it a single line:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

Usage Examples
==============

Crawling Entire Company Box Storage
------------------------------------

Parameters:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Crawling Only Specific Folders
--------------------------------

Filtering by folder path is possible using the ``include_pattern`` parameter.

Parameters:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    include_pattern=.*Documents/Projects/.*

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Crawling Only PDF Files
------------------------

Filtering by MIME type is possible using the ``supported_mimetypes`` parameter.

Parameters:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789
    supported_mimetypes=application/pdf

Script:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Troubleshooting
===============

Authentication Errors
---------------------

**Symptom**: ``Authentication failed`` or ``Invalid grant``

**Check**:

1. Verify ``client_id`` and ``client_secret`` are correct
2. Verify private key is correctly copied (newlines are ``\n``)
3. Verify passphrase is correct
4. Verify app is authorized in Box admin console
5. Verify ``enterprise_id`` is correct

Private Key Format Errors
--------------------------

**Symptom**: ``Invalid private key format``

**Resolution**:

Verify newlines are correctly converted to ``\n``:

::

    # Correct format
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # Incorrect format (contains actual newlines)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

Cannot Retrieve Files
---------------------

**Symptom**: Crawl succeeds but 0 files

**Check**:

1. Verify "Read all files and folders" is enabled in Application Scopes
2. Verify App Access Level is set to "App + Enterprise Access"
3. Verify files actually exist in Box storage
4. Verify service account has appropriate permissions

When There Are a Large Number of Files
---------------------------------------

**Symptom**: Crawling takes a long time or times out

**Resolution**:

Split processing in the data store settings:

1. Adjust crawl interval
2. Divide into multiple data stores (e.g., by folder)
3. Increase thread count with the ``number_of_threads`` parameter
4. Distribute load with schedule settings

Permissions and Access Control
================================

Reflecting Box Collaboration Permissions
-----------------------------------------

Through the ``BoxFileAPI`` object provided by the ``file.api`` field, you can map
Box collaboration information to |Fess| search roles.
``file.api.collaborationRoles`` returns a list of search roles corresponding to the
users and groups that can access the file.

Set permissions in the script:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.api.collaborationRoles
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

.. note::
   ``file.api.collaborationRoles`` retrieves collaboration information for each file,
   which increases the number of Box API calls and may slow down crawling.

To assign a fixed role to all files, specify it as follows:

::

    role="{role}box-users"

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-dropbox` - Dropbox Connector
- :doc:`ds-gsuite` - Google Workspace Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
