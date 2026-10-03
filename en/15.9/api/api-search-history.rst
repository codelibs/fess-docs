==================
Search History API
==================

This document describes the v2 Search History API of |Fess|.
For the common response envelope and error model, see :doc:`api-overview`.

The base URL is ``http://<Server Name>/api/v2/`` (local environment example: ``http://localhost:8080/api/v2``).

.. note::

   Search history is available while both ``search.history.enabled`` (default: ``true``) and the
   search log are enabled. ``features.search_history`` of ``/api/v2/ui/config`` reports the state.

Getting Recent Searches
=======================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/search-history``
==================  ====================================================

Returns the recent searches that the logged-in user made with ``/api/v2/search`` on the current
virtual host, newest first. A client can run one of them again with the returned conditions.

- Only first-page searches are listed. Searches with the same conditions are merged into the newest
  one, and searches without a query are left out.
- At most ``search.history.size`` (default: ``10``) searches are returned.
- Search logs are written by a job that runs every minute, so a search can take up to about a minute
  to appear.
- The history is keyed on the logged-in user of the session. Anonymous callers receive
  ``auth_required`` (401); an access token does not stand in for a login.
- When search history is disabled, the endpoint responds with ``invalid_request`` (400).

There are no request parameters.

Response
--------

On success (200), the following fields are returned directly under ``response`` of the common envelope.

::

    {
      "response": {
        "status": 0,
        "record_count": 1,
        "data": [
          {
            "q": "fess",
            "fields": { "label": ["docs"] },
            "sort": "last_modified.desc",
            "requested_at": "2026-10-01T09:00:00Z",
            "hit_count": 42
          }
        ]
      }
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Response Fields

   * - ``record_count``
     - Number of searches in ``data`` (int).
   * - ``data``
     - Recent searches, newest first. The condition keys use the request parameter names of
       ``/api/v2/search``; a key is omitted when the search did not use it.
   * - ``data[].q``
     - The query (str).
   * - ``data[].fields``
     - Field conditions given with ``fields.<name>``, keyed by field name, each with its values.
   * - ``data[].ex_q``
     - Extra queries (array of str).
   * - ``data[].sort``
     - Sort order (str).
   * - ``data[].lang``
     - Languages requested with ``lang`` (array of str).
   * - ``data[].requested_at``
     - When the search was made (UTC, ISO-8601).
   * - ``data[].hit_count``
     - Number of hits the search returned (int64).

Table: Response Fields

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response

   * - Status Code
     - Description
   * - 400 Bad Request
     - When search history is disabled.
   * - 401 Unauthorized
     - When the caller is not logged in.
   * - 405 Method Not Allowed
     - When the HTTP method is not allowed.
   * - 500 Internal Server Error
     - When an internal server error occurs.

Table: Error Response

In the Bundled Theme
====================

In the bundled ``bootstrap`` theme, a logged-in user sees the recent searches in the suggest
dropdown when they click the empty search box or press the down arrow key in it. Choosing an entry
runs the same search again, including conditions such as labels. Search logs recorded before
|Fess| 15.9 carry no conditions and are not listed.
