==========================
General API
==========================

Overview
========

General API is an API for managing |Fess| general settings.
You can retrieve and update system-wide configuration settings.

Base URL
========

::

    /api/admin/general

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - Get general settings
   * - PUT
     - /
     - Update general settings

Get General Settings
====================

Request
-------

::

    GET /api/admin/general

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   The above shows only representative fields as an example. The actual ``setting``
   object in the response contains all general-settings fields (crawling, search,
   notification, LDAP, SSO, storage, etc.). See ``EditForm.java`` for the full list.

.. note::

   For security reasons, fields that contain credentials are not returned with their
   actual values.

   - ``ldapAdminSecurityCredentials`` (LDAP admin password) is always replaced with
     ``null``.
   - Other secrets (``storageAccessKey``, ``storageSecretKey``, ``oicClientId``,
     ``oicClientSecret``, ``spnegoPreauthPassword``, ``entraidClientId``,
     ``entraidClientSecret``) are returned masked as ``"**********"`` when they are
     set.

Update General Settings
=======================

Request
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

Updates are processed as a partial merge — request values are merged onto the
current settings, and fields not included in the request (null fields) are ignored
so existing values are kept.

.. warning::

   The following four fields have a ``@Required`` constraint and MUST be included in
   EVERY PUT request. Omitting them results in a validation error (HTTP 400).

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   They cannot be omitted even during a partial update. Because the value you send
   overwrites the existing setting, if you do not want to change a value, first
   retrieve the current value with ``GET`` and send it as-is. All other fields are
   optional; omitted fields keep their existing values.

.. note::

   Numeric fields have type and range validation. Sending a value that cannot be
   parsed as an integer, or a value outside the allowed range, results in a
   validation error (HTTP 400).

   - ``dayForCleanup``: ``-1`` to ``1000``
   - ``crawlingThreadCount``: ``0`` to ``100``
   - ``failureCountThreshold``: ``-1`` to ``10000``
   - ``purgeSearchLogDay`` / ``purgeJobLogDay`` / ``purgeUserInfoDay``: ``-1`` to ``100000``
   - ``purgeSuggestSearchLogDay``: ``0`` to ``100000``

.. note::

   For on/off (``available``-type) fields, only ``"true"`` or ``"on"`` (both
   case-insensitive) mean enabled. Any other value (such as ``"false"`` or an empty
   string) is treated as disabled (``false``). The existing value is kept only when
   the field is omitted (not sent). Note that in the GET response, these fields are
   returned as the strings ``"true"`` / ``"false"``.

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

Main Fields
~~~~~~~~~~~

There are a wide variety of setting items. The representative fields are shown
below (refer to ``EditForm.java`` for all fields). The API request/response body
type is ``EditBody``, which extends ``EditForm``, but the field definitions live in
``EditForm``. On/off settings of the ``available`` type are expressed as the strings
``"true"`` / ``"false"``.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Field
     - Required
     - Description
   * - ``incrementalCrawling``
     - No
     - Enable/disable incremental crawling
   * - ``dayForCleanup``
     - Yes
     - Number of days to retain crawled documents (-1 = cleanup disabled)
   * - ``crawlingThreadCount``
     - Yes
     - Number of threads used for crawling
   * - ``failureCountThreshold``
     - Yes
     - Failure count threshold to stop crawling a URL (-1 = disabled)
   * - ``csvFileEncoding``
     - Yes
     - Encoding for CSV export
   * - ``searchLog``
     - No
     - Enable/disable search query logging
   * - ``userInfo``
     - No
     - Enable/disable recording of user information
   * - ``userFavorite``
     - No
     - Enable/disable the favorite feature
   * - ``webApiJson``
     - No
     - Enable/disable the JSON Web API
   * - ``appValue``
     - No
     - Application-specific additional configuration value
   * - ``virtualHostValue``
     - No
     - Virtual host configuration (for multi-tenant setups)
   * - ``popularWord``
     - No
     - Enable/disable aggregation and display of popular words
   * - ``defaultLabelValue``
     - No
     - Default label value
   * - ``defaultSortValue``
     - No
     - Default sort order
   * - ``appendQueryParameter``
     - No
     - Append query parameters to search result URLs
   * - ``loginRequired``
     - No
     - Whether login is required for search
   * - ``loginLink``
     - No
     - Enable or disable display of the login link on the search screen
   * - ``thumbnail``
     - No
     - Enable/disable thumbnail generation
   * - ``resultCollapsed``
     - No
     - Enable or disable collapsing of similar documents in search results
   * - ``ignoreFailureType``
     - No
     - Crawl failure types to ignore
   * - ``crawlingUserAgent``
     - No
     - User-Agent string sent during crawling
   * - ``purgeSearchLogDay``
     - No
     - Number of days to retain search logs (-1 = disabled)
   * - ``purgeJobLogDay``
     - No
     - Number of days to retain job logs (-1 = disabled)
   * - ``purgeUserInfoDay``
     - No
     - Number of days to retain user information (-1 = disabled)
   * - ``purgeSuggestSearchLogDay``
     - No
     - Number of days to retain suggest search logs (0 = disabled)
   * - ``purgeByBots``
     - No
     - Bot User-Agents whose search logs are discarded
   * - ``notificationTo``
     - No
     - Email address to which system notifications are sent
   * - ``notificationLogin``
     - No
     - Notification message displayed on the login page
   * - ``notificationSearchTop``
     - No
     - Notification message displayed on the search top page
   * - ``notificationAdvanceSearch``
     - No
     - Notification message displayed on the advanced search page
   * - ``suggestSearchLog``
     - No
     - Enable/disable suggest from search logs
   * - ``suggestDocuments``
     - No
     - Enable/disable suggest from documents
   * - ``logLevel``
     - No
     - Log level for system logs
   * - ``logNotificationEnabled``
     - No
     - Enable/disable notifications for ERROR/WARN logs
   * - ``logNotificationLevel``
     - No
     - Log notification level
   * - ``slackWebhookUrls``
     - No
     - Slack Webhook URL for notifications
   * - ``googleChatWebhookUrls``
     - No
     - Google Chat Webhook URL for notifications
   * - ``searchUseBrowserLocale``
     - No
     - Whether to use the browser locale for search
   * - ``ragLlmName``
     - No
     - LLM provider name used for RAG
   * - ``llmLogLevel``
     - No
     - Log level for LLM-related packages

Authentication-Related Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Settings related to LDAP and SSO (OpenID Connect, SAML, SPNEGO, Entra ID) are
also managed by this API. The representative fields are shown below (refer to
``EditForm.java`` for all fields).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Field
     - Description
   * - ``ldapProviderUrl``
     - LDAP connection URL
   * - ``ldapBaseDn``
     - LDAP base DN
   * - ``ldapSecurityPrincipal``
     - Security principal for LDAP binding
   * - ``ldapAdminSecurityPrincipal``
     - Security principal for LDAP administrative operations
   * - ``ldapAdminSecurityCredentials``
     - LDAP administrator password (replaced with ``null`` in the response)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - User/group search filters
   * - ``ldapMemberofAttribute``
     - LDAP attribute name indicating group membership
   * - ``ssoType``
     - SSO type (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` etc.
     - OpenID Connect settings
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` etc.
     - SAML settings
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` etc.
     - SPNEGO settings
   * - ``entraidClientId`` / ``entraidTenant`` etc.
     - Microsoft Entra ID settings

Storage-Related Fields
~~~~~~~~~~~~~~~~~~~~~~~

Cloud storage (S3 / GCS) integration settings can also be managed.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Field
     - Description
   * - ``storageType``
     - Storage type (``s3`` / ``gcs`` / ``auto``)
   * - ``storageEndpoint``
     - Storage endpoint URL
   * - ``storageAccessKey`` / ``storageSecretKey``
     - Access key / secret key for authentication
   * - ``storageBucket``
     - Bucket name
   * - ``storageRegion``
     - S3 region
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - GCS project ID / credentials file path

.. note::

   Secret fields such as ``ldapAdminSecurityCredentials``,
   ``storageAccessKey`` / ``storageSecretKey``, ``oicClientId`` / ``oicClientSecret``,
   ``entraidClientId`` / ``entraidClientSecret``, and ``spnegoPreauthPassword`` keep
   their stored value (are not updated) when the mask value ``"**********"`` is sent
   as-is. Send the actual value only when you want to change it.

   Because this check is based on whether the string is blank after removing
   asterisks, sending an empty string (``""``) or a value consisting only of
   asterisks also leaves the value unchanged. Therefore, these secret fields cannot
   be cleared to an empty value via the API.

Response
--------

On a successful update, only ``status`` is returned (``id`` and ``created`` are not included).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Usage Examples
==============

.. note::

   Because the four fields ``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold``, and ``csvFileEncoding`` are required in PUT requests,
   all examples below include them. Since the values you send overwrite the existing
   settings, in real usage you should send the current values retrieved with ``GET``
   (the examples below use default values).

Update Crawl Settings
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

Update Log Retention Period
---------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

Update Suggest Settings
-----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

See Also
========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`../../admin/general-guide` - General Settings Guide
