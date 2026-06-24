==========================
General API
==========================

Overview
========

General API is an API for managing the |Fess| general settings (system-wide
configuration). You can retrieve and update settings for crawling, logging,
search result display, suggest, log retention periods, notifications,
authentication (LDAP / SSO), and cloud storage integration. These settings
correspond to the "General" settings in the admin UI
(:doc:`../../admin/general-guide`).

Base URL
========

::

    /api/admin/general

Accessing this API requires an access token with the ``Radmin-api`` permission.
See :doc:`api-admin-overview` for authentication details.

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

This endpoint does not accept query parameters.

Response
--------

``response.setting`` contains the current general settings. The response includes
all updatable setting fields; the example below shows only representative fields.
On/off settings are expressed as the strings ``"true"`` / ``"false"``, while
values such as retention days and thread counts are expressed as numbers.

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
          "storageAccessKey": "**********",
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   For security reasons, passwords and secret values are not returned as-is. The
   LDAP administrator password ``ldapAdminSecurityCredentials`` is always returned
   as ``null``. Other secret fields (``storageAccessKey``, ``storageSecretKey``,
   ``oicClientId``, ``oicClientSecret``, ``spnegoPreauthPassword``,
   ``entraidClientId``, ``entraidClientSecret``) are returned as the masked value
   ``"**********"`` when set, or as an empty string when not set.

Update General Settings
=======================

Request
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

Updates are processed as a partial update (merge). The server loads the current
settings and then overwrites only the non-``null`` fields included in the request.
Fields not included in the request, and fields set to ``null``, retain their
existing values.

.. important::

   The request body is validated before the overwrite is applied. Therefore, the
   required fields (``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold``, ``csvFileEncoding``) **must always be included in the
   request**, regardless of what you are changing. If any of them is missing, the
   request fails validation and ``status: 1`` is returned. To change only some
   fields, first retrieve the current settings with ``GET``, then ``PUT`` the
   request with the current values of the required fields included.

.. note::

   Password and secret fields (``ldapAdminSecurityCredentials``,
   ``storageAccessKey``, ``storageSecretKey``, ``oicClientId``, ``oicClientSecret``,
   ``spnegoPreauthPassword``, ``entraidClientId``, ``entraidClientSecret``) are
   ignored when an empty string or the masked value (``**********``) is sent, and
   the existing value is retained. These fields are updated only when an actual
   value is sent.

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
below (all fields correspond to the "General" settings in the admin UI). On/off
settings are specified as the strings ``"true"`` / ``"false"``.

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
     - Number of days to retain crawled documents (-1 = cleanup disabled; range: -1 to 1000)
   * - ``crawlingThreadCount``
     - Yes
     - Number of threads used for crawling (range: 0 to 100)
   * - ``failureCountThreshold``
     - Yes
     - Failure count threshold to stop crawling a URL (-1 = disabled; range: -1 to 10000)
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
   * - ``thumbnail``
     - No
     - Enable/disable thumbnail generation
   * - ``ignoreFailureType``
     - No
     - Crawl failure types to ignore
   * - ``purgeSearchLogDay``
     - No
     - Number of days to retain search logs (-1 = disabled; range: -1 to 100000)
   * - ``purgeJobLogDay``
     - No
     - Number of days to retain job logs (-1 = disabled; range: -1 to 100000)
   * - ``purgeUserInfoDay``
     - No
     - Number of days to retain user information (-1 = disabled; range: -1 to 100000)
   * - ``purgeSuggestSearchLogDay``
     - No
     - Number of days to retain suggest search logs (0 = disabled; range: 0 to 100000)
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

Authentication-Related Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Settings related to LDAP and SSO (OpenID Connect, SAML, SPNEGO, Entra ID) are
also managed by this API. The representative fields are shown below (all fields
correspond to the "General" settings in the admin UI).

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
     - Storage type (``auto`` / ``s3`` / ``gcs``)
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

Response
--------

On a successful update, only ``version`` and ``status`` are returned (``id`` and
``created`` are not included).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

If the update fails (for example, due to a validation error), ``status`` is set
to a non-zero value (``1`` for a validation error), and ``message`` contains the
error details. See :doc:`api-admin-overview` for the list of ``status`` values.

Usage Examples
==============

.. note::

   The examples below include the required fields (``dayForCleanup``,
   ``crawlingThreadCount``, ``failureCountThreshold``, ``csvFileEncoding``). Because
   these must always be specified regardless of what you are changing, use the
   current values retrieved via ``GET`` in actual operation.

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

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`../../admin/general-guide` - General Settings Guide
