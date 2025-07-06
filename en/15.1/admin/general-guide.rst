=====================
General Configuration
=====================

Overview
========
On this administration page, you can manage the settings of |Fess|.
You can change various settings of |Fess| without restarting it.

|image0|

Management Operations
=====================

System
------

JSON Response
:::::::::::::

Specify whether to enable the JSON API.

Login Required
::::::::::::::

Specify whether to require login for search functionality.

Login Link
::::::::::

Specify whether to display a link to the login page on the search screen.

Similar Result Collapsed
::::::::::::::::::::::::

Specify whether to enable collapsing of duplicate results.

Thumbnail View
::::::::::::::

Specify whether to enable thumbnail display.

Default Label Value
:::::::::::::::::::

Specify the default label value to add to search conditions.
If specified on a per-role or per-group basis, add role: or group: respectively, e.g., role:admin=label1.

Default Sort Value
::::::::::::::::::

Specify the default sort value to add to search conditions.
If specified on a per-role or per-group basis, add role: or group: respectively, e.g., role:admin=content_length.desc.

Virtual Host
::::::::::::

Specify the virtual host.
For details, see :doc:the virtual host section of the configuration guide <../config/virtual-host>.

Popular Word Response
:::::::::::::::::::::

Specify whether to enable the popular word API.

Encoding for CSV
::::::::::::::::

Specify the encoding of the CSV file to be downloaded.

Append Params to URL
::::::::::::::::::::

Enable to pass parameters to the search result display.

Notification Email
::::::::::::::::::

Specify the email address to notify when crawling is complete.
Multiple addresses can be specified separated by commas. A mail server is required to use this feature.

Crawler
-------

Check Last Modified
:::::::::::::::::::

Enable to perform a differential crawl.

Simultaneous Crawler Config
:::::::::::::::::::::::::::

Specify the number of crawl settings to execute simultaneously.

Remove Documents Before
:::::::::::::::::::::::

Specify the number of days after the index to keep documents.

Excluded Failure Type
:::::::::::::::::::::

Specify the exception names, etc., which are excluded from being crawled as URLs with failures exceeding the threshold.

Failure Count Threshold
:::::::::::::::::::::::

If the number of failures recorded as URLs exceeds the number specified here for documents targeted for crawling, they will be excluded from the next crawl.

Logging
-------

Search Logging
::::::::::::::

Specify whether to enable the recording of search logs.

User Logging
::::::::::::

Specify whether to enable the recording of user logs.

Favorite Logging
::::::::::::::::

Specify whether to enable the recording of favorite logs.

Purge Search Log Before
:::::::::::::::::::::::

Delete search logs older than the specified number of days.

Purge Job Log Before
::::::::::::::::::::

Delete job logs older than the specified number of days.

Purge User Before
:::::::::::::::::

Delete user logs older than the specified number of days.

Here's the translation:

Bots Name For Purge
:::::::::::::::::::

Specify bot names to exclude from search logs.

Log Level
:::::::::

Specify the log level for fess.log.

Suggest
-------

Suggest from Search Words
:::::::::::::::::::::::::

Specify whether to generate suggestion candidates from search logs.

Suggest from Documents
::::::::::::::::::::::

Specify whether to generate suggestion candidates from indexed documents.

Purge Suggest Documents Before
::::::::::::::::::::::::::::::

Delete suggest data from the specified number of days ago.

LDAP
----

LDAP URL
::::::::

Specify the URL of the LDAP server.

Base DN
:::::::

Specify the base distinguished name for logging in to the search page.

Bind DN
:::::::

Specify the administrator's bind DN.

Password
::::::::

Specify the password for the Bind DN.

User DN
:::::::

Specify the distinguished name of the user.

Account Filter
::::::::::::::

Specify the user's common name or uid.

Group Filter
::::::::::::

Specify the filter condition for the groups to be acquired.

memberOf Attribute
::::::::::::::::::

Specify the memberOf attribute name available on the LDAP server.
For Active Directory, it's "memberOf".
For other LDAP servers, it might be "isMemberOf".

Notification
------------

Login Page
::::::::::

Enter the message to be displayed on the login page.

Search Top Page
:::::::::::::::

Enter the message to be displayed on the search top page.

Example
=======

LDAP Configuration
------------------

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

.. |image0| image:: ../../../resources/images/en/15.1/admin/general-1.png
