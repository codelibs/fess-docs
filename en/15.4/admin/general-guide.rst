================
General Settings
================

Overview
========

This administration page allows you to manage |Fess| configuration settings.
You can modify various |Fess| settings without restarting |Fess|.

|image0|

Configuration Options
=====================

System
------

JSON Response
:::::::::::::

Specify whether to enable the JSON API.

Login Required
::::::::::::::

Specify whether to require login for search functionality.

Display Login Link
::::::::::::::::::

Configures whether to display a link to the login page on the search screen.

Result Collapse
:::::::::::::::

Specifies whether to enable collapsing of duplicate results.

Thumbnail View
::::::::::::::

Specify whether to enable thumbnail display.

Default Label Value
:::::::::::::::::::

Specifies the label value to add to the search conditions by default.
To specify per role or group, add "role:" or "group:" prefix, such as "role:admin=label1".

Default Sort Value
::::::::::::::::::

Specifies the sort value to add to the search conditions by default.
To specify per role or group, add "role:" or "group:" prefix, such as "role:admin=content_length.desc".

Virtual Host
::::::::::::

Configures virtual hosts.
For details, see :doc:`Virtual Hosts in the Configuration Guide <../config/virtual-host>`.

Popular Word Response
:::::::::::::::::::::

Specify whether to enable the popular word API.

CSV File Encoding
:::::::::::::::::

Specifies the encoding for downloadable CSV files.

Append Search Parameters
::::::::::::::::::::::::

Enable when passing parameters to the search result display.

Notification Email
::::::::::::::::::

Specify the email address to notify when crawling is complete.
Multiple addresses can be specified separated by commas. A mail server is required to use this feature.

Crawler
-------

Check Last Modified
:::::::::::::::::::

Enable to perform differential crawling.

Concurrent Crawler Settings
:::::::::::::::::::::::::::

Specifies the number of crawl configurations to execute simultaneously.

Delete Documents Before
:::::::::::::::::::::::

Specifies the number of days for the retention period after indexing.

Excluded Failure Types
::::::::::::::::::::::

Failure URLs that exceed the threshold are excluded from crawl targets, but exception names specified here will be crawl targets even if they exceed the failure URL threshold.

Failure Count Threshold
:::::::::::::::::::::::

If a crawl target document is recorded in failure URLs more times than specified here, it will be excluded from the next crawl.

Logging
-------

Search Log
::::::::::

Specifies whether to enable recording of search logs.

User Log
::::::::

Specifies whether to enable recording of user logs.

Favorite Log
::::::::::::

Specifies whether to enable recording of favorite logs.

Purge Search Log Before
:::::::::::::::::::::::

Deletes search logs older than the specified number of days.

Purge Job Log Before
::::::::::::::::::::

Deletes job logs older than the specified number of days.

Purge User Log Before
:::::::::::::::::::::

Deletes user logs older than the specified number of days.

Purge Bot Name for Log
::::::::::::::::::::::

Specifies bot names to exclude from search logs.

Log Level
:::::::::

Specify the log level for fess.log.

Suggest
-------

Suggest from Search Words
:::::::::::::::::::::::::

Specifies whether to generate suggest candidates from search logs.

Suggest from Documents
::::::::::::::::::::::

Specifies whether to generate suggest candidates from indexed documents.

Purge Suggest Documents Before
::::::::::::::::::::::::::::::

Deletes suggest data older than the specified number of days.

LDAP
----

LDAP URL
::::::::

Specifies the URL of the LDAP server.

Base DN
:::::::

Specifies the base distinguished name for logging into the search screen.

Bind DN
:::::::

Specifies the Bind DN for administrators.

Password
::::::::

Specifies the password for the Bind DN.

User DN
:::::::

Specifies the distinguished name for users.

Account Filter
::::::::::::::

Specifies the user's Common Name, uid, etc.

Group Filter
::::::::::::

Specifies the filter conditions for the groups to retrieve.

memberOf Attribute
::::::::::::::::::

Specifies the memberOf attribute name available on the LDAP server.
For Active Directory, it is "memberOf".
For other LDAP servers, it may be "isMemberOf".


Notification Display
--------------------

Login Page
::::::::::

Enter the message to display on the login screen.

Search Top Page
:::::::::::::::

Enter the message to display on the search top screen.

Storage
-------

After configuring each item, a [System > Storage] menu will appear in the left menu.
For file management, see :doc:`Storage <../admin/storage-guide>`.

Type
::::

Specifies the storage type.
When "Auto" is selected, the storage type is automatically determined from the endpoint.

- **Auto**: Auto-detect from endpoint
- **S3**: Amazon S3
- **GCS**: Google Cloud Storage

Bucket
::::::

Specifies the bucket name to manage.

Endpoint
::::::::

Specifies the endpoint URL of the storage server.

- S3: Uses AWS default endpoint if left blank
- GCS: Uses Google Cloud default endpoint if left blank
- MinIO, etc.: The endpoint URL of the MinIO server

Access Key
::::::::::

Specifies the access key for S3 or S3-compatible storage.

Secret Key
::::::::::

Specifies the secret key for S3 or S3-compatible storage.

Region
::::::

Specifies the S3 region (e.g., ap-northeast-1).

Project ID
::::::::::

Specifies the Google Cloud project ID for GCS.

Credentials Path
::::::::::::::::

Specifies the path to the service account credentials JSON file for GCS.

Examples
========

LDAP Configuration Example
--------------------------

.. tabularcolumns:: |p{4cm}|p{4cm}|p{4cm}|
.. list-table:: LDAP/Active Directory Configuration
   :header-rows: 1

   * - Name
     - Value (LDAP)
     - Value (Active Directory)
   * - LDAP URL
     - ldap://SERVERNAME:389
     - ldap://SERVERNAME:389
   * - Base DN
     - cn=Directory Manager
     - dc=fess,dc=codelibs,dc=org
   * - Bind DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - manager@fess.codelibs.org
   * - User DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - %s@fess.codelibs.org
   * - Account Filter
     - cn=%s or uid=%s
     - (&(objectClass=user)(sAMAccountName=%s))
   * - Group Filter
     -
     - (member:1.2.840.113556.1.4.1941:=%s)
   * - memberOf
     - isMemberOf
     - memberOf

.. |image0| image:: ../../../resources/images/en/15.4/admin/general-1.png
.. pdf            :height: 940 px
