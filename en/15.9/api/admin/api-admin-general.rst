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
        "version": "15.9",
        "status": 0,
        "setting": {
          "incremental_crawling": "true",
          "day_for_cleanup": -1,
          "crawling_thread_count": 5,
          "search_log": "true",
          "user_info": "true",
          "user_favorite": "false",
          "web_api_json": "true",
          "default_label_value": "",
          "default_sort_value": "",
          "append_query_parameter": "false",
          "login_required": "false",
          "thumbnail": "true",
          "failure_count_threshold": -1,
          "popular_word": "true",
          "csv_file_encoding": "UTF-8",
          "purge_search_log_day": 30,
          "purge_job_log_day": 30,
          "purge_user_info_day": 30,
          "purge_suggest_search_log_day": 30,
          "notification_to": "",
          "suggest_search_log": "true",
          "suggest_documents": "true",
          "ldap_provider_url": "ldap://localhost:389/",
          "ldap_base_dn": "dc=example,dc=com",
          "ldap_admin_security_principal": "cn=admin,dc=example,dc=com",
          "log_level": "",
          "sso_type": "none",
          "storage_type": "",
          "notification_login": "",
          "notification_search_top": ""
        }
      }
    }

.. note::

   The above shows only representative fields. The actual ``setting`` object in the
   response contains all general-settings fields (crawling, search, notification,
   LDAP, SSO, storage, etc.). See the admin "General" settings page for the full
   list.

.. note::

   For security reasons, fields that contain credentials are not returned with their
   actual values.

   - ``ldap_admin_security_credentials`` (LDAP admin password) is never included in
     the response.
   - Other secrets (``storage_access_key``, ``storage_secret_key``, ``oic_client_id``,
     ``oic_client_secret``, ``spnego_preauth_password``, ``entraid_client_id``,
     ``entraid_client_secret``) are returned masked as ``"**********"`` when they are
     set, or as an empty string (``""``) when they are not set.

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

.. warning::

   The following four fields are required and MUST be included in EVERY PUT request,
   even for a partial update:

   - ``day_for_cleanup``
   - ``crawling_thread_count``
   - ``failure_count_threshold``
   - ``csv_file_encoding``

   If any of them is missing, the request fails validation and the API returns
   HTTP 400 with ``status: 1`` and an error ``message``. Because the value you send
   overwrites the existing setting, to keep a value unchanged first retrieve it with
   ``GET`` and send it back as-is. All other fields are optional; omitted fields keep
   their existing values.

.. note::

   Numeric fields are type- and range-validated. Sending a value that cannot be
   parsed as an integer, or a value outside the allowed range, fails validation
   (HTTP 400 with ``status: 1``). The valid range for each numeric field is listed
   in the field table below.

.. note::

   For on/off (``available``-type) fields, only ``"true"`` or ``"on"`` (both
   case-insensitive) mean enabled. Any other value (such as ``"false"`` or an empty
   string) is treated as disabled (``false``). The existing value is kept only when
   the field is omitted (not sent). In the GET response, these fields are returned
   as the strings ``"true"`` / ``"false"``.

.. code-block:: json

    {
      "incremental_crawling": "true",
      "day_for_cleanup": -1,
      "crawling_thread_count": 10,
      "failure_count_threshold": 100,
      "csv_file_encoding": "UTF-8",
      "popular_word": "true"
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
   * - ``incremental_crawling``
     - No
     - Enable/disable incremental crawling
   * - ``day_for_cleanup``
     - Yes
     - Number of days to retain crawled documents (-1 = cleanup disabled; range: -1 to 1000)
   * - ``crawling_thread_count``
     - Yes
     - Number of threads used for crawling (range: 0 to 100)
   * - ``failure_count_threshold``
     - Yes
     - Failure count threshold to stop crawling a URL (-1 = disabled; range: -1 to 10000)
   * - ``csv_file_encoding``
     - Yes
     - Encoding for CSV export
   * - ``search_log``
     - No
     - Enable/disable search query logging
   * - ``user_info``
     - No
     - Enable/disable recording of user information
   * - ``user_favorite``
     - No
     - Enable/disable the favorite feature
   * - ``web_api_json``
     - No
     - Enable/disable the JSON Web API
   * - ``app_value``
     - No
     - Application-specific additional configuration value
   * - ``virtual_host_value``
     - No
     - Virtual host configuration (for multi-tenant setups)
   * - ``popular_word``
     - No
     - Enable/disable aggregation and display of popular words
   * - ``default_label_value``
     - No
     - Default label value
   * - ``default_sort_value``
     - No
     - Default sort order
   * - ``append_query_parameter``
     - No
     - Append query parameters to search result URLs
   * - ``login_required``
     - No
     - Whether login is required for search
   * - ``login_link``
     - No
     - Enable or disable display of the login link on the search screen
   * - ``thumbnail``
     - No
     - Enable/disable thumbnail generation
   * - ``result_collapsed``
     - No
     - Enable or disable collapsing of similar documents in search results
   * - ``ignore_failure_type``
     - No
     - Crawl failure types to ignore
   * - ``crawling_user_agent``
     - No
     - User-Agent string sent during crawling
   * - ``purge_search_log_day``
     - No
     - Number of days to retain search logs (-1 = disabled; range: -1 to 100000)
   * - ``purge_job_log_day``
     - No
     - Number of days to retain job logs (-1 = disabled; range: -1 to 100000)
   * - ``purge_user_info_day``
     - No
     - Number of days to retain user information (-1 = disabled; range: -1 to 100000)
   * - ``purge_suggest_search_log_day``
     - No
     - Number of days to retain suggest search logs (0 = disabled; range: 0 to 100000)
   * - ``purge_by_bots``
     - No
     - Bot User-Agents whose search logs are discarded
   * - ``notification_to``
     - No
     - Email address to which system notifications are sent
   * - ``notification_login``
     - No
     - Notification message displayed on the login page
   * - ``notification_search_top``
     - No
     - Notification message displayed on the search top page
   * - ``notification_advance_search``
     - No
     - Notification message displayed on the advanced search page
   * - ``suggest_search_log``
     - No
     - Enable/disable suggest from search logs
   * - ``suggest_documents``
     - No
     - Enable/disable suggest from documents
   * - ``log_level``
     - No
     - Log level for system logs
   * - ``log_notification_enabled``
     - No
     - Enable/disable notifications for ERROR/WARN logs
   * - ``log_notification_level``
     - No
     - Log notification level
   * - ``slack_webhook_urls``
     - No
     - Slack Webhook URL for notifications
   * - ``google_chat_webhook_urls``
     - No
     - Google Chat Webhook URL for notifications
   * - ``search_use_browser_locale``
     - No
     - Whether to use the browser locale for search
   * - ``rag_llm_name``
     - No
     - LLM provider name used for RAG
   * - ``llm_log_level``
     - No
     - Log level for LLM-related packages

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
   * - ``ldap_provider_url``
     - LDAP connection URL
   * - ``ldap_base_dn``
     - LDAP base DN
   * - ``ldap_security_principal``
     - Security principal for LDAP binding
   * - ``ldap_admin_security_principal``
     - Security principal for LDAP administrative operations
   * - ``ldap_admin_security_credentials``
     - LDAP administrator password (never included in the response)
   * - ``ldap_account_filter`` / ``ldap_group_filter``
     - User/group search filters
   * - ``ldap_memberof_attribute``
     - LDAP attribute name indicating group membership
   * - ``sso_type``
     - SSO type (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oic_client_id`` / ``oic_client_secret`` / ``oic_auth_server_url`` etc.
     - OpenID Connect settings
   * - ``saml_idp_entityid`` / ``saml_sp_entityid`` etc.
     - SAML settings
   * - ``spnego_krb5_conf`` / ``spnego_login_conf`` etc.
     - SPNEGO settings
   * - ``entraid_client_id`` / ``entraid_tenant`` etc.
     - Microsoft Entra ID settings

Storage-Related Fields
~~~~~~~~~~~~~~~~~~~~~~~

Cloud storage (S3 / GCS) integration settings can also be managed.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Field
     - Description
   * - ``storage_type``
     - Storage type (``auto`` / ``s3`` / ``gcs``)
   * - ``storage_endpoint``
     - Storage endpoint URL
   * - ``storage_access_key`` / ``storage_secret_key``
     - Access key / secret key for authentication
   * - ``storage_bucket``
     - Bucket name
   * - ``storage_region``
     - S3 region
   * - ``storage_project_id`` / ``storage_credentials_path``
     - GCS project ID / credentials file path

.. note::

   Secret fields such as ``ldap_admin_security_credentials``,
   ``storage_access_key`` / ``storage_secret_key``, ``oic_client_id`` / ``oic_client_secret``,
   ``entraid_client_id`` / ``entraid_client_secret``, and ``spnego_preauth_password`` keep
   their stored value (are not updated) when the mask value ``"**********"`` is sent
   as-is. Send the actual value only when you want to change it.

   Because this check is based on whether the string is blank after removing
   asterisks, sending an empty string (``""``) or a value consisting only of
   asterisks also leaves the value unchanged. Therefore, these secret fields cannot
   be cleared to an empty value via the API.

Response
--------

On a successful update, only ``version`` and ``status`` are returned (``id`` and
``created`` are not included).

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0
      }
    }

If the update fails (for example, due to a validation error), the API returns
HTTP 400 and the response ``status`` is set to a non-zero value (``1`` for a
validation error), with ``message`` containing the error details. See
:doc:`api-admin-overview` for the list of ``status`` values.

Usage Examples
==============

.. note::

   The examples below include the required fields (``day_for_cleanup``,
   ``crawling_thread_count``, ``failure_count_threshold``, ``csv_file_encoding``). Because
   these must always be sent regardless of what you are changing, retrieve the
   current values with ``GET`` and include them in actual operation (the examples
   below use default values).

Update Crawl Settings
---------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incremental_crawling": "true",
           "crawling_thread_count": 10,
           "failure_count_threshold": 100,
           "day_for_cleanup": -1,
           "csv_file_encoding": "UTF-8"
         }'

Update Log Retention Period
---------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "purge_search_log_day": 90,
           "purge_job_log_day": 90,
           "purge_user_info_day": 90
         }'

Update Suggest Settings
-----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "suggest_search_log": "true",
           "suggest_documents": "true"
         }'

See Also
========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`../../admin/general-guide` - General Settings Guide
