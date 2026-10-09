==============
UI Config API
==============

Overview
========

The UI Config API returns initial configuration needed by a single-page application (SPA): theme, feature flags, pagination limits, and — when CSRF is required — a fresh CSRF token.
This endpoint is called anonymously before login.

For the common response envelope and error model, see :doc:`api-overview`.

Fetching UI Configuration
==========================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/ui/config``
==================  ====================================================

Returns the initial configuration needed by the SPA.

Response
--------

On success (HTTP 200, UiConfigResponse), the following response is returned in the common envelope format (excerpt).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "ui_locale": "ja",
        "default_label_values": [],
        "default_sort": "",
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "search_history": true,
          "search_export": false,
          "user_tag": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.9/install/",
          "login_link": true,
          "sso_enabled": false,
          "osdd_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.search_result_sort_score_desc"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.searchoptions_all_langs"},
          {"value": "ja", "label_key": "labels.lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

Each element of ``response`` is as follows. All fields are required.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Response Information
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``site_name``
     - string
     - Site name. When the active theme includes a manifest, this is its display name (``display_name``); otherwise ``Fess``.
   * - ``login_required``
     - boolean
     - Whether login is required.
   * - ``locales``
     - string[]
     - Array of available locales.
   * - ``ui_locale``
     - string
     - The display language of the search screen as a BCP 47 tag (for example ``ja`` or ``pt-BR``). It is determined from the request parameter ``browser_lang`` (remembered in the session once given), then the session, then the ``Accept-Language`` header. Empty when it cannot be determined. Not the same as ``locales``, which lists the search languages.
   * - ``default_label_values``
     - string[]
     - Label values that the search screen pre-selects. For the current user, they are taken from "Default Label Value" on the "General Settings" page of the admin UI, including values set per role or group. An empty array when ``label_options`` is empty. ``/api/v2/search`` does not apply them.
   * - ``default_sort``
     - string
     - Sort value that the search screen pre-selects. For the current user, it is taken from "Default Sort Value" on the same page. Empty when none applies. ``/api/v2/search`` does not apply it.
   * - ``theme``
     - object
     - Active theme descriptor. See the table below for details.
   * - ``features``
     - object
     - Feature flags. See the table below for details.
   * - ``page_size_default``
     - integer
     - Default page size.
   * - ``page_size_max``
     - integer
     - Maximum page size.
   * - ``sort_options``
     - object[]
     - Sort options for the search UI. See the table below for details.
   * - ``num_options``
     - integer[]
     - Array of selectable page sizes. Values exceeding ``page_size_max`` are excluded.
   * - ``lang_options``
     - object[]
     - Language filter options. See the table below for details.
   * - ``label_options``
     - object[]
     - Configured label options. See the table below for details.
   * - ``notifications``
     - object
     - HTML notification snippets displayed at the top of specific views. See the table below for details.
   * - ``facet_views``
     - object[]
     - Configured facet query view groups. See the table below for details.
   * - ``filetype_options``
     - object[]
     - File type facet options for the advanced search form. See the table below for details.
   * - ``csrf_required``
     - boolean
     - Whether a CSRF token is required.
   * - ``csrf_token``
     - string
     - An empty string when ``csrf_required`` is ``false``; otherwise, a fresh token associated with the current session.

theme
~~~~~

``theme`` is always present but becomes an empty object when no custom theme is associated with the request.
Manifest-derived keys (``display_name`` / ``version`` / ``supported_locales``) are only present when the active theme includes a manifest.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``name``
     - string
     - Theme name.
   * - ``display_name``
     - string
     - Display name of the theme.
   * - ``version``
     - string
     - Theme version.
   * - ``supported_locales``
     - string[]
     - Array of locales supported by the theme.

features
~~~~~~~~

All fields are required.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``user_favorite``
     - boolean
     - Whether the user favorites feature is enabled.
   * - ``search_history``
     - boolean
     - Whether search history (``GET /api/v2/search-history``) is available (``true`` when both ``search.history.enabled`` and the search log are enabled).
   * - ``search_export``
     - boolean
     - Whether search result export (``GET /api/v2/documents/export``) is enabled (``api.search.export``).
   * - ``user_tag``
     - boolean
     - Whether per-user tags are enabled (``user.tag.enabled``): the tag endpoints (``/api/v2/tags``, ``/api/v2/documents/{docId}/tags``) answer and search hits carry ``tags``.
   * - ``popular_word``
     - boolean
     - Whether the popular word feature is enabled.
   * - ``suggest_search_log``
     - boolean
     - Whether suggestion by search log is enabled.
   * - ``suggest_documents``
     - boolean
     - Whether suggestion by documents is enabled.
   * - ``login_required``
     - boolean
     - Whether login is required.
   * - ``eoled``
     - boolean
     - Whether this |Fess| build has reached EOL.
   * - ``development_mode``
     - boolean
     - Always ``false``. It reported that the embedded (development) search engine was in use, a configuration removed in 15.9.
   * - ``search_log_enabled``
     - boolean
     - Whether search logging is enabled.
   * - ``thumbnail_enabled``
     - boolean
     - Whether thumbnails are enabled.
   * - ``display_label_type``
     - boolean
     - ``true`` when one or more labels are configured.
   * - ``clipboard_copy_icon``
     - boolean
     - Whether to display the clipboard copy icon.
   * - ``eol_link``
     - string
     - Resolved EOL information URL. Empty string when not EOL or when the URL cannot be resolved.
   * - ``installation_link``
     - string
     - Resolved installation guide URL. Empty string when it cannot be resolved.
   * - ``login_link``
     - boolean or string
     - Whether to show the login link ("Display Login Link" on the "General Settings" page of the admin UI). When the link is enabled and login goes through SSO (``sso_enabled`` below is ``true``), the string ``"sso/"``, a URL relative to the base URL of the page, is returned instead of a boolean.
   * - ``sso_enabled``
     - boolean
     - ``true`` when ``sso.type`` is set and the ``fess-sso-*`` plugin that serves it is installed.
   * - ``osdd_link``
     - boolean
     - ``true`` when the OpenSearch description document (``osdd``) is served (``osdd.link.enabled``; with ``auto`` it is not served under SSO).
   * - ``rag_chat_enabled``
     - boolean
     - Whether the RAG chat feature is available.

sort_options
~~~~~~~~~~~~

Array of sort options for the search UI.
Each element has ``value`` and ``label_key``.
``click_count.*`` items are present only when search logging is enabled; ``favorite_count.*`` items are present only when user favorites are enabled.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elements of sort_options
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``value``
     - string
     - Sort value.
   * - ``label_key``
     - string
     - Label key.

num_options
~~~~~~~~~~~

Array of selectable page sizes (integers). Values exceeding ``page_size_max`` are excluded.

lang_options
~~~~~~~~~~~~

Array of language filter options.
Each element has ``value`` and ``label_key``.
The first element is the ``all`` sentinel, followed by one entry per supported language code.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elements of lang_options
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``value``
     - string
     - Language value.
   * - ``label_key``
     - string
     - Label key.

label_options
~~~~~~~~~~~~~

Array of configured label options. Returns an empty array when no labels are defined.
Each element has ``value`` and ``name``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elements of label_options
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``value``
     - string
     - Label value.
   * - ``name``
     - string
     - Label name.

notifications
~~~~~~~~~~~~~

HTML notification snippets displayed at the top of specific views. An empty string means no notification for that view.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``search_top``
     - string
     - Notification displayed on the search top page.
   * - ``advance_search``
     - string
     - Notification displayed on the advanced search page.
   * - ``login``
     - string
     - Notification displayed on the login page.

facet_views
~~~~~~~~~~~

Array of configured facet query view groups. Returns an empty array when not defined.
Each element has ``group_name`` and ``queries``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elements of facet_views
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``group_name``
     - string
     - Group name.
   * - ``queries``
     - object[]
     - Array of facet queries for the group. Each element has ``label_key`` (string) and ``value`` (string).

filetype_options
~~~~~~~~~~~~~~~~

Array of file type facet options for the advanced search form.
Each element has ``value`` and ``label_key``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Elements of filetype_options
   :header-rows: 1
   :widths: 28 15 57

   * - Field
     - Type
     - Description
   * - ``value``
     - string
     - File type value.
   * - ``label_key``
     - string
     - Label key.

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response
   :header-rows: 1
   :widths: 25 75

   * - Status Code
     - Description
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 500 Internal Server Error
     - An internal server error occurred.
