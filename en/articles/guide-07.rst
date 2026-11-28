===================================================
Searching Files in Google Drive, SharePoint and Box
===================================================

Introduction
============

When different departments use Google Drive, SharePoint Online and Box, people spend more and more time trying to remember where a document was saved.
With Fess data store plugins, files from all three services can be found from a single search page.

Cloud storage, however, mixes files with different access rights.
A misconfiguration can expose confidential files such as contracts in the search results of users who are not even logged in.
This article explains, for each service, a minimal configuration that works as written, and how to carry the original permissions over into Fess.

Steps common to all data stores, such as installing plugins, handler names, parameters, writing scripts and creating jobs, are covered in :doc:`datastore-basics`.
Read that article first before continuing.
The settings in this article are based on Fess 15.9 and version 15.9.0 of each plugin.

What We Will Build
==================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Service
     - Plugin
     - Handler name
     - What to prepare on the service side
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - A JSON key for a service account, and domain-wide delegation
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - An app registration in Entra ID (client secret) and Microsoft Graph application permissions
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - A Box custom app with JWT authentication

If you run Fess on Docker, list the plugin names and versions, separated by spaces, in the ``FESS_PLUGINS`` environment variable to install them all at startup.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

If you install them from the admin UI or with ``fess-setup``, restart Fess after the installation (``FESS_PLUGINS`` installs plugins before Fess starts, so no restart is needed).

Decide First: Who May See the Search Results
============================================

When you create a new data store configuration, the "Permissions" field already contains ``{role}guest``.
If this value is left in place, the imported files can be found by users who are not logged in.
All three plugins put the roles derived from the original sharing settings into ``file.roles``.
The configuration is therefore the same for all three in these two respects:

- Delete ``{role}guest`` from the "Permissions" field and leave it empty
- Write ``role=file.roles`` in the script

Both are needed because the plugins treat the "Permissions" field differently.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Plugin
     - Value of the "Permissions" field
     - ``default_permissions`` parameter
   * - Google Drive
     - Not used if you write ``role=file.roles``. If you do not, the field value (initially ``{role}guest``) is attached as is to every file
     - Used only for files for which nothing could be obtained from the Drive ACL. If it is not set either, such files are not imported
   * - SharePoint (OneDriveDataStore)
     - Merged into ``file.roles``. Leaving ``{role}guest`` makes every file public
     - Added to every file
   * - Box
     - Merged into ``file.roles``. Leaving ``{role}guest`` makes every file public
     - Added to every file

``file.roles`` contains strings that represent the users and groups of each service.

- Google Drive: users and groups are email addresses, and file owners use the same format. Domain sharing becomes ``{group}<domain-name>`` (configurable with ``domain_permission_format``), and public sharing that can be found by search (``anyone``) becomes the ``guest`` role. Sharing with "anyone with the link" does not become a role.
- SharePoint: users are their object ID and UPN, and groups are their ID and display name. A sharing link for "people in your organization" becomes the group ``EVERYONE_IN_TENANT``.
- Box: users are their Box user ID and login (email address), and groups are their Box group ID. In addition to the file's own collaborations, the collaborations and owners of its parent folders are included.

At search time, these are matched against the user name and group names of the user logged in to Fess.
For example, for Google Drive user permissions to take effect, the Fess user name must match the email address.
See :doc:`guide-05` for how roles work and :doc:`guide-15` for login via SSO.

A data store configuration has no dedicated field for labels that let users narrow search results by service.
Either add a line such as ``label="box"`` to the script, or create a label that matches the URLs (for details, see :doc:`datastore-basics`).
Label values may contain only alphanumeric characters and ``_``, so a value with a hyphen such as ``google-drive`` cannot be created.

Google Drive: Importing Shared Drives
=====================================

Preparing Google
----------------

In 15.9, ``fess-ds-gsuite`` runs with ``crawl_target=shared_drives`` by default.
It reads every shared drive in the domain by impersonating a domain administrator.

1. Create a project in the Google Cloud console and enable the Google Drive API
2. Create a service account, then create and download a key in JSON format on the [Keys] tab
3. Enable domain-wide delegation for the service account and note its OAuth 2 client ID
4. In the Google Workspace Admin console, under [Security] > [Access and data control] > [API controls] > [Domain-wide delegation], authorize that client ID for the scope ``https://www.googleapis.com/auth/drive.readonly``

The account specified in ``impersonate_user`` must be a domain administrator of Google Workspace.
If ``crawl_target`` is anything other than ``legacy`` and ``impersonate_user`` is missing, the crawl stops with an error when it starts.

Parameters and Script
---------------------

Under [Crawler] > [Data Store] > [Create New], select ``GoogleDriveDataStore`` as the "Handler Name" and empty the "Permissions" field.
Copy the values of the same names from the JSON key into ``private_key``, ``private_key_id`` and ``client_email``.
Write ``private_key`` on a single line, keeping the line breaks as ``\n``.

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url`` is the file's ``webViewLink``.
Deletions are reflected on the assumption that the indexed URL contains the Drive file ID.
For that reason, use ``url`` as is, without rewriting it.

The other import scopes are as follows.

- ``crawl_target=users``: reads every user's My Drive. You need to enable the Admin SDK API and add the scope ``https://www.googleapis.com/auth/admin.directory.user.readonly`` (both in the delegation settings and in the ``scopes`` parameter).
- ``crawl_target=legacy``: reads only files shared directly with the service account's address. Neither delegation nor ``impersonate_user`` is needed.

Incremental Crawling
--------------------

If you add ``incremental=true``, the second and later crawls read only the Drive change feed.
In this mode, ``delete_old_docs`` is forced to ``false``, and files deleted from Drive may remain in the index.
Also, unchanged files are not re-registered, so as things stand they disappear from the search results once the number of days in "Delete old documents" (3 days by default) has passed (see the section on document expiration in :doc:`datastore-basics`).

If you use incremental crawling, combine it as follows.

- Also create a configuration for a full crawl without ``incremental``, and run it regularly, for example once a week
- Specify in both configurations a ``time_to_live`` slightly longer than the full crawl interval (for a weekly full crawl, ``time_to_live=11520``, 8 days)

Files deleted from Drive disappear from the search results when this period expires.
The plugin writes the change feed position back to the "Parameters" field, so do not edit the value it writes back.

SharePoint Online: Importing Files from Document Libraries
==========================================================

Which Handler to Use
--------------------

To search the content of files in SharePoint document libraries, use ``OneDriveDataStore`` from ``fess-ds-microsoft365``.

- ``SharePointDocLibDataStore`` only registers each library as a single document and does not import the files in it.
- ``fess-ds-sharepoint`` (``SharePointDataStore``) is for on-premises SharePoint Server. It does not support Microsoft Graph, and its documentation directs SharePoint Online users to ``fess-ds-microsoft365``.

Preparing Entra ID
------------------

1. Create a new registration under [App registrations] in the Azure Portal
2. Under [Certificates & secrets], create a new client secret and note its value (this is where you choose its expiration)
3. Under [API permissions] > [Microsoft Graph] > [Application permissions], add the four permissions below
4. Run [Grant admin consent]

Add the following application permissions.

- ``Files.Read.All``
- ``User.Read.All``, ``Group.Read.All``: needed for every import scope to look up the user and group names in ACLs
- ``Sites.Read.All``: needed to enumerate sites with ``shared_documents_drive_crawler=true``

Parameters and Script
---------------------

If nothing is specified, ``OneDriveDataStore`` reads every SharePoint site, and also every user's OneDrive and the drives of every Microsoft 365 group.
To target SharePoint only, set the three flags explicitly.

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

To limit the import to specific libraries, set all three flags to ``false`` and specify the drive ID in ``drive_id``.
You can look up the drive ID with ``GET /sites/{site-id}/drives`` in Microsoft Graph.
If you specify only ``drive_id`` and leave the flags as they are, that drive is merely "added" to the overall import.

Missing Permissions and Retries
-------------------------------

The ACL of each file is obtained with a separate Graph call per file.
What happens when this call fails is determined by ``permission_failure_policy``.
With the default ``skip``, the file is not registered and is recorded in [System Info] > [Failure URL] and in a WARN log.
If you change it to ``index_without_acl``, files are registered with incomplete ACLs, so for highly confidential libraries it is safer to keep the default.

Retries of Graph calls can be tuned with ``max_retry_count`` (default 3, maximum 10) and ``retry_interval`` (seconds, default 3, maximum 180).
``OneDriveDataStore`` has no incremental crawling option and reads everything every time.

Box: Importing a Contracts Folder with Permissions
==================================================

Preparing Box
-------------

``fess-ds-box`` supports only server authentication with JWT.

1. In the Box Developer Console, create a "Custom App" and select "Server Authentication (with JWT)" as the authentication method
2. On the [Configuration] tab, enable "Read all files and folders stored in Box" under Application Scopes
3. Select "App + Enterprise Access" as the App Access Level
4. Create a key pair with [Generate a Public/Private Keypair] and save the JSON file
5. Authorize the app in the Box Admin Console

``clientID``, ``clientSecret``, ``publicKeyID``, ``privateKey``, ``passphrase`` and ``enterpriseID`` in the JSON file correspond to ``client_id``, ``client_secret``, ``public_key_id``, ``private_key``, ``passphrase`` and ``enterprise_id``, respectively.
All six are required.

Limiting the Import to a Single Folder
--------------------------------------

When the target is fixed, such as the legal department's contracts, use ``root_folder_id`` to read just one folder.
In this mode, the plugin does not impersonate users; it reads the folder as the app's service account.
You therefore need to add the service account as a collaborator on the target folder.
The folder ID is the number at the end of the URL when you open the folder in the Box web interface.

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

Be sure to delete ``{role}guest`` from the "Permissions" field.
In Box, the field value is merged into ``file.roles``, so if you leave it, the contracts can be found by users who are not logged in.

Box groups become roles as group IDs, so as they are they do not match the group names in Fess.
In this example, ``default_permissions={group}legal`` makes every file visible to the Fess ``legal`` group.
Users with whom a file is shared individually in Box can also find it, provided their login (email address) matches their Fess user name.
To add a role to files that have a company-wide shared link, use ``company_shared_link_role``.

Reading Every User's Files
--------------------------

If you omit ``root_folder_id``, the plugin enumerates every user in the enterprise and reads their files by impersonating them one at a time.
You can narrow down the target users with ``filter_term``.
API calls through impersonation must be allowed in the app settings on the Box side, so check the settings in Box's developer documentation.

Handling Rate Limits
--------------------

The number of retries for ``429`` and ``5xx`` responses is ``max_retry_attempts`` (default 5).
``max_retry_count`` (default 10) is the number of times the connection is re-created on a ``401`` response and has nothing to do with rate limits.
To space out API calls, set a wait per item with ``readInterval`` (milliseconds).
``fess-ds-box`` has no incremental crawling option.

Operational Notes
=================

Credential Expiration
---------------------

- An Entra ID client secret has the expiration chosen when it was created. Once it expires, authentication fails and nothing is imported, so create a new secret before the expiration and replace ``client_secret`` in the parameters.
- Google access tokens are refreshed automatically by the library the plugin uses. In 15.9, ``refresh_token_interval`` is ignored and a warning is logged.
- Box access tokens are refreshed automatically every ``refresh_token_interval`` (default 3540 seconds).

When Not Everything Gets Imported
---------------------------------

At the end of a crawl, all three plugins wait 60 seconds by default for their worker threads to finish, and anything not finished by then is not imported.
If the document count falls short on a large tenant, extend the wait time.
The parameter is ``thread_pool_timeout_seconds`` for Google Drive, ``executor_shutdown_timeout`` for SharePoint and ``thread_pool_await_timeout`` for Box (all in seconds).

In Google Drive, 429, 500, 502, 503 and 504 responses and 403 responses caused by rate limits are retried with exponential backoff.
Retries can be tuned with ``max_retries`` (default 5), ``retry_initial_interval_ms`` (default 1000) and ``max_backoff_ms`` (default 32000).

Verifying the Results
=====================

How to read job results and logs is explained in :doc:`datastore-basics`.
A data store crawl may show the job as "OK" even when fetching files failed, so judge by the document count and the logs.
For the configuration in this article, also check the following three points.

1. While logged out, search for a word contained in an imported file and confirm that no results are returned (to make sure you did not forget to clear the "Permissions" field)
2. Log in as a user the file is shared with and confirm that the same file is returned
3. For the Google Drive configuration, check that ``fess-crawler.log`` does not contain ``Skipped ... because no permission could be resolved`` (these are files that were not imported because their ACL was empty)

If the file is not returned in step 2, check whether the user's user name and group names match the values in ``file.roles``.

Summary
=======

- Import the content of SharePoint files with ``OneDriveDataStore``, setting OneDrive and group drives to ``false`` if you do not need them.
- For all three services, delete ``{role}guest`` from the "Permissions" field and write ``role=file.roles`` in the script.
- ``default_permissions`` replaces an empty ACL in Google Drive, and is added to every file in SharePoint and Box.
- Only Google Drive offers incremental crawling (``incremental=true``). If you use it, combine it with a configuration for full crawls and specify ``time_to_live`` in both.

References
==========

- `Google Workspace Connector <https://fess.codelibs.org/stable/config/datastore/ds-gsuite.html>`__
- `Microsoft 365 Connector <https://fess.codelibs.org/stable/config/datastore/ds-microsoft365.html>`__
- `Box Connector <https://fess.codelibs.org/stable/config/datastore/ds-box.html>`__
- `Data Store Configuration <https://fess.codelibs.org/stable/admin/dataconfig-guide.html>`__
- `fess-ds-microsoft365 15.9.0 README (list of Graph permissions) <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `fess-ds-box 15.9.0 README (file.roles and root_folder_id) <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
