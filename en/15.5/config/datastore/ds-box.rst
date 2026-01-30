==================================
Box Connector
==================================

Overview
========

The Box Connector provides functionality to retrieve files from Box.com cloud storage
and register them in the |Fess| index.

This feature requires the ``fess-ds-box`` plugin.

Prerequisites
=============

1. Plugin installation is required
2. A Box developer account and application creation is required
3. JWT (JSON Web Token) authentication or OAuth 2.0 authentication setup is required

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

JWT authentication example (recommended):

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Parameter List
~~~~~~~~~~~~~~

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

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``file.url``
     - Link to open file in browser
   * - ``file.contents``
     - File text content
   * - ``file.mimetype``
     - File MIME type
   * - ``file.filetype``
     - File type
   * - ``file.name``
     - File name
   * - ``file.size``
     - File size (bytes)
   * - ``file.created_at``
     - Creation date
   * - ``file.modified_at``
     - Last modified date

For details, refer to `Box File Object <https://developer.box.com/reference#file-object>`_.

Box Authentication Setup
========================

JWT Authentication Setup Steps
------------------------------

1. Create an Application in Box Developer Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access https://app.box.com/developers/console:

1. Click "Create New App"
2. Select "Custom App"
3. Select "Server Authentication (with JWT)" for authentication method
4. Enter app name and create

2. Application Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
-----------------------------------

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
-------------------------

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

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-dropbox` - Dropbox Connector
- :doc:`ds-gsuite` - Google Workspace Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
