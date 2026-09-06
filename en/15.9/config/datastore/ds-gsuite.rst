==================================
Google Workspace Connector
==================================

Overview
========

The Google Workspace Connector provides functionality to retrieve files from Google Drive (formerly G Suite)
and register them in the |Fess| index.

This feature requires the ``fess-ds-gsuite`` plugin.

Changes in 15.9
===============

The connector was substantially reworked in |Fess| 15.9. Read this section before
upgrading an existing data store configuration.

.. warning::

   ``crawl_target`` now defaults to ``shared_drives``, and every value other than
   ``legacy`` requires ``impersonate_user``. An existing configuration that is
   upgraded unchanged therefore **fails at startup** with a ``DataStoreException``
   instead of running.

   This is deliberate: the previous behaviour only ever reached the files that were
   explicitly shared with the service account, so the alternative would be a crawl
   that silently indexes nothing. Either set ``impersonate_user`` to a domain
   administrator account, or set ``crawl_target=legacy`` to keep the previous
   behaviour.

Behaviour Changes
-----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Change
     - What you have to do
   * - ``crawl_target`` defaults to ``shared_drives`` and requires ``impersonate_user``
     - Set ``impersonate_user``, or set ``crawl_target=legacy``. Otherwise the crawl fails at startup.
   * - The default OAuth scope narrowed from ``https://www.googleapis.com/auth/drive`` to ``https://www.googleapis.com/auth/drive.readonly``
     - Update the domain-wide delegation entry in the Google Workspace admin console, which lists the scopes explicitly.
   * - ``crawl_target=users`` and ``crawl_target=both`` additionally require ``https://www.googleapis.com/auth/admin.directory.user.readonly``
     - Add the scope both to the ``scopes`` parameter and to the delegation entry. This is validated at startup.
   * - The indexed URL is now ``webViewLink`` (the browser-openable link) instead of the download link
     - Run a full re-crawl to pick up the new URLs.
   * - ``default_permissions`` is now a fallback, not an addition
     - A document with a resolvable ACL indexes that ACL only, no longer the union of the ACL and ``default_permissions``. The result is strictly less permissive.
   * - Link-only sharing no longer grants a search role
     - A ``domain`` or ``anyone`` permission with ``allowFileDiscovery=false`` means "anyone with the link", which Drive itself does not make discoverable by search.
   * - A document whose ACL resolves to nothing is skipped instead of being indexed with no roles
     - Set ``default_permissions`` to keep indexing such documents. Previously they were visible to every user, because an empty role list disables the permission filter.
   * - ``fields`` no longer defaults to ``*`` but to an explicit field list
     - A crawl script that references an unusual field now reads null. Set ``fields=*`` to restore the previous projection.
   * - Google Docs are exported as Markdown instead of plain text, and Google Sheets as TSV instead of CSV
     - The indexed text of every Google Doc now contains Markdown syntax characters. Run a full re-crawl.
   * - ``refresh_token_interval`` is ignored
     - Token refresh is handled by the authentication library. An existing configuration keeps working, and a warning is logged.
   * - Google Forms and Google Sites are indexed as metadata only
     - They have no export format in the Drive API. Previously every one of them produced a crawl error.

New Capabilities
----------------

- ``crawl_target`` selects what is crawled: the service account's own view (``legacy``),
  every shared drive in the domain (``shared_drives``), every directory user's My Drive
  (``users``), or both (``both``). See `Crawl Target`_.
- Shared drive items now get the correct ACL. See `Permissions and Access Control`_.
- Incremental crawling through the Drive change feed. See `Incremental Crawling`_.
- Rate limiting with an exponential back-off that honours ``Retry-After``, and a failing
  shared drive or user that no longer aborts the whole crawl. See `Rate Limiting and Retries`_.
- ``proxy_username`` and ``proxy_password`` for an authenticating proxy.

Supported Services
==================

- Google Drive (My Drive, Shared Drives)
- Google Docs, Spreadsheets, Slides, Drawings, Apps Script
- Google Forms and Google Sites (metadata only; they have no export format)

Prerequisites
=============

1. Plugin installation is required
2. A Google Cloud Platform project must be created
3. A service account must be created and credentials obtained
4. Domain-wide delegation must be configured for Google Workspace
5. Unless ``crawl_target=legacy`` is used, a Google Workspace administrator account to
   impersonate is required

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
     - GoogleDriveDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com

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
   * - ``impersonate_user``
     - Conditional
     - The Google Workspace account impersonated through domain-wide delegation. Required unless ``crawl_target=legacy``; the crawl fails at startup without it. ``shared_drives`` and ``both`` enumerate the shared drives with domain administrator access, so this account must be a domain administrator.
   * - ``crawl_target``
     - No
     - What to crawl: ``legacy``, ``shared_drives``, ``users`` or ``both``. Default: ``shared_drives``. See `Crawl Target`_.
   * - ``scopes``
     - No
     - OAuth scopes, comma-separated. Default: ``https://www.googleapis.com/auth/drive.readonly``. ``crawl_target=users`` and ``crawl_target=both`` additionally require ``https://www.googleapis.com/auth/admin.directory.user.readonly``.
   * - ``user_query``
     - No
     - Admin SDK ``query`` used to narrow down the users enumerated by ``crawl_target=users`` and ``crawl_target=both``. Default: unset (every user of the customer).
   * - ``query``
     - No
     - Google Drive API search query string. Not applied to the change feed used by incremental crawling.
   * - ``corpora``
     - No
     - Corpora to search. Default: ``allDrives``. Only consumed by ``crawl_target=legacy``, so it has no effect under the default target: ``shared_drives`` lists each drive with ``drive`` and ``users`` lists each My Drive with ``user``, both fixed.
   * - ``spaces``
     - No
     - Spaces to search (Google Drive API ``spaces`` parameter, e.g. ``drive``, ``appDataFolder``). Default: unset (API default). Used by ``crawl_target=legacy`` and ``users``; ignored for ``shared_drives``.
   * - ``fields``
     - No
     - File fields to request from the Google Drive API. Default: an explicit field list, **not** ``*``. It covers every field the script context, the ACL resolution, the index URL and the incremental crawl need; a field outside the list reads as null in the crawl script. Set ``fields=*`` to request every field, as in previous versions.
   * - ``default_permissions``
     - No
     - Permissions used when the Drive ACL of a document resolves to nothing (comma-separated, e.g. ``{role}drive-users``). This is a fallback, not an addition: a document with a resolvable ACL indexes that ACL only.
   * - ``max_size``
     - No
     - Maximum file size to index (bytes). Default: ``10000000`` (approx. 10MB)
   * - ``number_of_threads``
     - No
     - Number of parallel processing threads. Default: ``1``
   * - ``incremental``
     - No
     - Whether to crawl through the Drive change feed instead of listing everything. Default: ``false``. It is read straight from the parameter field of the data store configuration, before the crawl starts. See `Incremental Crawling`_.

Advanced Parameters
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``domain_permission_format``
     - Role format applied to a ``type=domain`` Drive permission. ``{domain}`` is replaced with the domain name. Default: ``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - How long to wait for the worker threads to drain at the end of a crawl (seconds). Default: ``60``
   * - ``page_size``
     - Page size for ``files.list`` and ``changes.list``. Default: ``1000``; values above ``1000`` are clamped.
   * - ``permission_page_size``
     - Page size for ``permissions.list`` and ``drives.list``. Default: ``100``; values above ``100`` are clamped.
   * - ``max_cached_content_size``
     - Maximum size (in bytes) of content kept in memory; content larger than this is spooled to a temporary file. Default: ``1048576`` (1MB).
   * - ``max_retries``
     - Maximum number of retries for a throttled or transient Drive API failure. Default: ``5``
   * - ``retry_initial_interval_ms``
     - Initial back-off interval before the first retry (milliseconds). Default: ``1000``
   * - ``max_backoff_ms``
     - Upper bound of a single back-off wait (milliseconds). Default: ``32000``
   * - ``read_timeout``
     - HTTP read timeout (milliseconds). Default: ``20000``
   * - ``connect_timeout``
     - HTTP connection timeout (milliseconds). Default: ``20000``
   * - ``proxy_host``
     - Proxy server hostname. The proxy is used only when both ``proxy_host`` and ``proxy_port`` are set; either one alone has no effect.
   * - ``proxy_port``
     - Proxy server port number. See ``proxy_host``.
   * - ``proxy_username``
     - User name for an authenticating proxy. When set, a ``Proxy-Authorization`` header is added to every request. See `Limitations`_ for what this does and does not authenticate.
   * - ``proxy_password``
     - Password for an authenticating proxy
   * - ``ignore_folder``
     - Whether to skip folders. Default: ``true``
   * - ``ignore_error``
     - Whether to continue processing on errors. Default: ``true``
   * - ``supported_mimetypes``
     - MIME types to index (regex, comma-separated). Default: ``.*`` (all types)
   * - ``include_pattern``
     - Regex pattern for URLs to include in the index
   * - ``exclude_pattern``
     - Regex pattern for URLs to exclude
   * - ``refresh_token_interval``
     - Ignored since 15.9. Access tokens are refreshed by the authentication library. An existing setting keeps working and a warning is logged.

.. note::

   ``private_key``, ``private_key_id``, ``client_email``, ``proxy_username`` and
   ``proxy_password`` are removed from the script evaluation context, so a crawl script
   cannot index them and no search result can disclose them.

.. note::

   When incremental crawling is enabled, the connector writes ``start_page_tokens`` and
   ``crawl_signature`` back into the parameter field of the data store configuration. They
   are managed by the connector and appear alongside the parameters you set; leave them
   alone. Editing or deleting them makes the next run crawl every scope in full.

Crawl Target
------------

A service account has no Drive of its own and belongs to no Google group, so a crawl
that authenticates as the service account itself only ever reaches the files that were
explicitly shared with the service account's address. ``crawl_target`` therefore selects
whose view of Drive is crawled.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Description
   * - ``legacy``
     - The service account's own view, as in previous versions. ``impersonate_user`` is not required. Only the files explicitly shared with the service account are found.
   * - ``shared_drives``
     - Default. Every shared drive in the domain is enumerated, and each one is listed separately.
   * - ``users``
     - Every user in the directory is enumerated through the Admin SDK, and the My Drive of each one is listed by impersonating that user.
   * - ``both``
     - ``shared_drives`` followed by ``users``. A file that appears in several scopes is indexed once.

The following is validated when the crawl starts, and an invalid combination raises a
``DataStoreException`` instead of running:

1. ``crawl_target`` must be one of ``legacy``, ``shared_drives``, ``users`` or ``both``.
2. ``impersonate_user`` must be set unless ``crawl_target=legacy``.
3. ``scopes`` must contain ``https://www.googleapis.com/auth/admin.directory.user.readonly``
   when ``crawl_target`` is ``users`` or ``both``.

.. note::

   ``shared_drives`` and ``both`` enumerate the shared drives with domain administrator
   access, so the account named by ``impersonate_user`` must be a Google Workspace domain
   administrator. This listing decides the whole scope of the crawl, so a permanent
   failure aborts the crawl rather than being reported and skipped -- a crawl that
   enumerated no drive must not be able to report success while indexing nothing.

Incremental Crawling
--------------------

Setting ``incremental=true`` makes each scope -- one shared drive, or the view of one
impersonated user -- read the Drive change feed instead of listing everything. A scope
with no stored token is listed in full and its change feed is anchored for the next run.

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   ``delete_old_docs`` is forced to ``false`` for every incremental run, and an explicit
   ``delete_old_docs=true`` is overridden rather than honoured (a warning is logged).
   The stale document sweep deletes every document of the configuration that the current
   crawl did not touch, which assumes a full crawl; an incremental run only touches the
   documents that changed, so the sweep would delete the rest of the index.

   To drop documents that vanished from Drive, schedule a separate data store
   configuration with ``incremental=false``.

The start page tokens are persisted only when the crawl finished and the worker threads
drained. A crawl that was stopped leaves the tokens untouched and the next run reads the
same changes again.

The tokens are also discarded, and every scope crawled in full, when the configuration
that decides what a scope yields changed -- that is, any of ``crawl_target``,
``impersonate_user``, ``user_query``, ``query``, ``corpora`` or ``spaces``. A stored token
only describes the population it was taken over, and resuming it after such a change would
leave a permanent hole in the index.

Rate Limiting and Retries
-------------------------

A throttled or transient Drive API failure is retried with an exponential back-off,
bounded by ``max_retries``, ``retry_initial_interval_ms`` and ``max_backoff_ms``. A
``Retry-After`` header wins over the exponential wait, but is clamped by ``max_backoff_ms``
so that a mistaken header cannot stall the crawl for hours. Only the delta-seconds form of
``Retry-After`` is honoured; an HTTP-date falls back to the exponential wait.

``429``, ``500``, ``502``, ``503`` and ``504`` are always retried. A ``403`` is retried
only when it is a rate limit error; any other ``403`` is an authorization failure, which
retrying cannot fix, and is reported immediately.

A file listing that could not be finished no longer aborts the whole crawl: the remaining
shared drives and users are still crawled, and the failure is written to the crawler log
and to the failure URL list in the admin console.

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
     - File URL. This is ``webViewLink``; when a file has none, ``https://drive.google.com/open?id=<file id>`` is used instead.
   * - ``file.thumbnail_link``
     - Thumbnail link (valid for short period)
   * - ``file.size``
     - File size (bytes)
   * - ``file.roles``
     - Access permissions

.. note::

   Only the fields listed in the ``fields`` parameter are populated. A field that is not
   requested reads null in the script. Set ``fields=*`` to request every field, as in
   previous versions.

For details, see the `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Text Extraction of Native Google Types
--------------------------------------

A native Google type cannot be downloaded and has to be exported. The export target is
chosen from the export formats that the Drive API actually reports, not from a fixed
table, and an export is bounded at 10MB.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type
     - Exported as
   * - Google Docs
     - Markdown (``text/markdown``), falling back to plain text and then HTML
   * - Google Sheets
     - TSV (``text/tab-separated-values``), falling back to CSV
   * - Google Slides
     - Plain text
   * - Google Drawings
     - PNG. There is no text to index, so the metadata is indexed on its own.
   * - Apps Script
     - The exported JSON bundle, from which the script sources are indexed
   * - Google Forms, Google Sites
     - Not exportable. The metadata is indexed and no error is reported.

.. note::

   Because Google Docs are now exported as Markdown, the indexed text of every Google Doc
   contains Markdown syntax characters. A full re-crawl is required for the change to
   reach documents that were already indexed.

.. note::

   The export targets are read from the Drive API once per crawl. If that call fails, the
   connector falls back to the conversions Drive has always supported -- plain text for
   Google Docs and CSV for Google Sheets -- and logs a warning.

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
3. When ``crawl_target`` is ``users`` or ``both``, also enable "Admin SDK API"

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

   When ``crawl_target`` is ``users`` or ``both``, enter both scopes:

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. Click "Authorize"

.. warning::

   The delegation entry lists the scopes explicitly, so upgrading from an earlier version
   requires updating it. The default scope narrowed from
   ``https://www.googleapis.com/auth/drive`` to
   ``https://www.googleapis.com/auth/drive.readonly`` in 15.9, and the scopes granted here
   must match the ``scopes`` parameter of the data store configuration.

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

Crawl Every Shared Drive
------------------------

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com

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
    role=file.roles
    filename=file.name

Crawl Every User's My Drive
---------------------------

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=users
    impersonate_user=admin@example.com
    scopes=https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

To narrow the users down, add an Admin SDK query:

::

    user_query=orgUnitPath=/Sales

Keep the Previous Behaviour
---------------------------

``crawl_target=legacy`` keeps the pre-15.9 traversal, in which only the files explicitly
shared with the service account are found. ``impersonate_user`` is not required.

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=legacy

Crawl with Permissions
----------------------

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

``default_permissions`` is only used for a document whose Drive ACL resolves to nothing.

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

The Crawl Fails to Start
------------------------

**Symptom**: The crawl ends immediately with a ``DataStoreException``

**Resolution**:

1. ``parameter 'crawl_target' must be one of ...``: the value of ``crawl_target`` is not
   ``legacy``, ``shared_drives``, ``users`` or ``both``.
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'``: set
   ``impersonate_user`` to a domain administrator account, or set ``crawl_target=legacy``.
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'``:
   add that scope to ``scopes`` and to the domain-wide delegation entry.

This is the expected outcome of upgrading an existing configuration unchanged. See
`Changes in 15.9`_.

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
5. Verify OAuth scope is correct (``https://www.googleapis.com/auth/drive.readonly``,
   plus ``https://www.googleapis.com/auth/admin.directory.user.readonly`` for
   ``crawl_target=users`` or ``both``)

Domain-wide Delegation Error
----------------------------

**Symptom**: ``Not Authorized to access this resource/api``

**Resolution**:

1. Verify authorization in Google Workspace admin console:

   - Is the Client ID registered correctly?
   - Are the OAuth scopes correct? The delegation entry lists them explicitly, so the
     scope narrowing introduced in 15.9 requires updating it.

2. Verify domain-wide delegation is enabled for the service account
3. Verify that the account named by ``impersonate_user`` is a domain administrator when
   ``crawl_target`` is ``shared_drives`` or ``both``

Cannot Retrieve Files
---------------------

**Symptom**: Crawl succeeds but 0 files found

**Check**:

1. Verify ``crawl_target`` is what you intend. With ``legacy``, only the files explicitly
   shared with the service account are found, because a service account has no Drive of
   its own and belongs to no group.
2. Verify files exist in Google Drive
3. Verify service account has read permissions
4. Verify domain-wide delegation is configured correctly
5. Verify access to target user's Drive is possible

Documents Are Skipped
---------------------

**Symptom**: ``Skipped ... because no permission could be resolved`` in the crawler log

**Resolution**:

The Drive ACL of the document resolved to no search role at all, so it was skipped rather
than indexed. Indexing a document with no role disables the |Fess| permission filter for
it and makes it visible to every user, which is why it is skipped instead. A skipped
document is not a crawl failure, so it appears only in the crawler log and not in the
failure URL list.

1. Set ``default_permissions`` to index such documents under a fallback permission
2. Verify that the account named by ``impersonate_user`` is a domain administrator, so
   that the shared drive ACLs can be read
3. Check whether the document is shared by link only. A ``domain`` or ``anyone``
   permission with ``allowFileDiscovery=false`` grants no search role, because Drive
   itself does not make such a document discoverable by search.

API Quota Error
---------------

**Symptom**: ``403 Rate Limit Exceeded`` or ``429 Too Many Requests``

**Resolution**:

1. Such a failure is retried automatically with an exponential back-off. Raise
   ``max_retries`` or ``max_backoff_ms`` if the crawl still fails.
2. Lower ``number_of_threads`` to reduce the request rate
3. Check quota in Google Cloud Platform
4. Increase crawl interval
5. Request quota increase if needed

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
   With ``crawl_target=shared_drives`` (the default) the shared drives are enumerated with
   domain administrator access, so the service account does not have to be a member of
   each shared drive. Instead, ``impersonate_user`` must name a domain administrator.

With ``crawl_target=legacy`` the service account has to be added to each shared drive:

1. Open the shared drive in Google Drive
2. Click "Manage members"
3. Add the service account email address
4. Set permission level to "Viewer"

Large Number of Files
---------------------

**Symptom**: Crawl takes too long or times out

**Resolution**:

1. Enable ``incremental=true`` so that only the changes since the previous run are crawled
2. Split shared drives and users into separate data store configurations rather than using
   ``crawl_target=both``
3. Narrow the scope with ``query``, ``user_query`` or ``supported_mimetypes``
4. Distribute load with scheduled crawling
5. Adjust crawl interval

Permissions and Access Control
==============================

How Drive Permissions Become Fess Roles
---------------------------------------

The ACL of a document is resolved in three steps, so that the number of extra API calls
stays proportional to the number of shared drives rather than to the number of files:

1. the inline permissions returned by the file listing, which cost nothing extra;
2. for an item of a shared drive, whose inline permissions the Drive API does not populate,
   the ACL of the shared drive itself. It is fetched once per drive with domain
   administrator access and cached;
3. for an item that carries its own additional permissions, those permissions.

Each Drive permission becomes a |Fess| search role:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Drive permission
     - Search role
   * - ``user``
     - The search role of that user's email address. The file owners are always added this way.
   * - ``group``
     - The search role of that group's email address. Google group membership is never expanded; |Fess| is expected to resolve it on the user side through SSO or LDAP.
   * - ``domain``
     - ``domain_permission_format`` with ``{domain}`` replaced by the domain name. Default: ``{group}{domain}``
   * - ``anyone``
     - The ``guest`` role
   * - Any of the above with ``allowFileDiscovery=false``, or a deleted permission
     - No role. Link-only sharing is not discoverable by search in Drive itself either.

When the result is empty, ``default_permissions`` is used instead -- as a fallback, not as
an addition. When ``default_permissions`` is unset too, the document is skipped.

Reflect Google Drive Sharing Permissions
----------------------------------------

Reflect Google Drive sharing settings in Fess permissions:

Parameters:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

Limitations
===========

- Drive's "removed" change signal covers a loss of access as well as a deletion. With
  ``crawl_target=users`` or ``both``, revoking one user's access to a document drops it
  from the index even though another user can still read it. It comes back on the next
  change to that file, or on the next full crawl.
- When a scope falls back to a full crawl during an incremental run, the stale document
  sweep stays suppressed, so documents that were deleted from Drive while a scope was
  unanchored remain in the index. The remedy is a separate ``incremental=false``
  configuration whose full crawl sweeps them.
- Propagating a deletion assumes the indexed URL contains the Drive file ID, which holds
  for ``webViewLink`` and for the fallback URL. A crawl script that rewrites ``url`` to a
  value the file ID does not appear in will not have deletions propagated to it.
- The change feed is not filtered by ``query``. With ``query`` set and ``incremental=true``,
  a changed file that does not match the query is still indexed.
- ``crawl_target=both`` on a large domain issues roughly
  ``2 + (number of shared drives) + (number of users)`` listing sequences. Splitting shared
  drives and users into separate data store configurations is the practical mitigation.
- ``proxy_username`` and ``proxy_password`` are sent as a ``Proxy-Authorization`` request
  header, which only authenticates a plain HTTP request. All Google API traffic is HTTPS,
  and an HTTPS connection through an authenticating proxy is established by a ``CONNECT``
  exchange that the JDK drives through ``java.net.Authenticator`` rather than through a
  request header. Such an environment needs the JVM option
  ``-Djdk.http.auth.tunneling.disabledSchemes=`` and an ``Authenticator`` instead.

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-microsoft365` - Microsoft 365 Connector
- :doc:`ds-box` - Box Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
