===================================================
Digging into Search Logs with OpenSearch Dashboards
===================================================

Introduction
============

In Fess 15.9, [System Info] > [Search Log] in the administration screen shows the zero-hit rate, the click-through rate, the distribution of click positions, response times, search counts by day of week and hour, and search counts by role and group.
Each table can be downloaded as CSV.
The workflow of finding problematic search terms and fixing them with synonyms or Key Match is described in :doc:`guide-08`.

On the other hand, this screen cannot produce aggregations like the following:

- Trends over periods longer than 366 days (the "Custom" period on the screen is limited to 366 days)
- Which terms return zero hits, broken down by role or by label
- Which URLs were actually opened for each search term
- A dashboard of charts sliced the way you choose

Search logs and click logs are stored in OpenSearch indices, so you can aggregate them directly in OpenSearch Dashboards.
This article starts OpenSearch Dashboards with the docker-fess Compose files, imports the dashboard bundled with Fess, checks the log fields, and then builds the four aggregations listed above.

Before You Start: Restricting Access
====================================

In docker-fess, OpenSearch Dashboards runs without the security plugin, just like OpenSearch itself.
Anyone who can reach port 5601 can read every field of the search logs (user IDs, IP addresses and so on) without logging in.
On top of that, from Dev Tools they can modify or delete any index, including the Fess indices for users and settings.

For this reason, make port 5601 (and 9200) reachable only from administrators' machines.
If you want to show search log statistics to people other than administrators, do not expose OpenSearch Dashboards; instead, create a role named ``admin-searchlog-view`` under [User] > [Role] in Fess and assign it to those people.
This role can view [System Info] > [Search Log] but cannot delete logs.

Starting OpenSearch Dashboards
==============================

Add the files for Dashboards to the directory where you placed ``compose.yaml`` and ``compose-opensearch3.yaml`` following :doc:`guide-02`.
``compose-dashboards3.yaml`` builds its image from the Dockerfile in the ``dashboards/`` directory, so three files are needed.

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

Start it by specifying the three Compose files.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

The first ``up`` builds an image from ``opensearch-dashboards:3.9.0`` with the ``securityDashboards`` plugin removed.
The container connects to ``OPENSEARCH_HOSTS='["http://search01:9200"]'`` on the ``search_net`` network and publishes port 5601.

Open ``http://localhost:5601`` in a browser; if the home page appears, it is running.
When stopping it or checking its status, also specify the three files with ``-f``.
Saved objects such as dashboards are stored in the ``.kibana`` index in OpenSearch, so removing the volumes with ``down -v`` deletes them too.

Importing the Bundled Dashboard
===============================

Fess ships with a dashboard definition for search logs, ``fess_log.ndjson``.
With Docker, copy it out of the container.
In the ZIP distribution, it is at ``extension/kibana/fess_log.ndjson`` in the extracted directory.

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

You can also get the same file from GitHub at ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson``.

1. Open [Dashboards Management] from the left menu and select [Saved objects]
2. Click [Import], select ``fess_log.ndjson`` and import it
3. Open the ``fess_log`` dashboard from [Dashboards] in the left menu

The import registers the index pattern ``fess_log*`` (time field ``requestedAt``), six visualizations and the ``fess_log`` dashboard.
Because the index pattern is included, you do not need to create ``fess_log*`` manually beforehand.
If you create it manually and then import, you end up with two patterns of the same name.

Watch How the Bundled Dashboard Counts
--------------------------------------

``fess_log*`` spans every index whose name starts with ``fess_log``, and the bundled visualizations do not filter by index.
In 15.9, click logs contain the search term (``searchWord``) and ``requestedAt``, so the count in "search-term-rank", for example, adds up searches and clicks.
If you use AI Search mode, chat logs (``fess_log.chat_log``) are also mixed into the counts and response times.

To count searches only, enter the following condition in the search bar at the top of the dashboard before reading it.

::

    _index : "fess_log.search_log"

Also, the field list saved in ``fess_log*`` comes from an older version and does not include newer fields such as ``rank``.
When building your own aggregations, use the index patterns from the next section.

Creating Index Patterns for Aggregation
=======================================

Keeping search logs and click logs in separate index patterns means they never get mixed, and every current field is available for selection.

1. In [Dashboards Management] > [Index patterns], click [Create index pattern]
2. Enter ``fess_log.search_log`` in "Index pattern name" and click [Next step]
3. Select ``requestedAt`` in "Time field" and click [Create index pattern]
4. Create ``fess_log.click_log`` (time field ``requestedAt``) the same way

If fields are added later (for example, when the first search filtered by a label is recorded), click [Refresh field list] on the index pattern page.

Handling Time
-------------

Fess stores dates and times in UTC.
By default, OpenSearch Dashboards displays them in the browser's time zone, and also splits days according to it.
To view them in a different time zone, change ``dateFormat:tz`` under [Dashboards Management] > [Advanced settings] to your time zone, for example ``Asia/Tokyo``.

The [Search Log] screen in Fess splits days by the server's time zone.
docker-fess containers use UTC by default, so when you compare daily figures between the two, they may differ by the offset between the day boundaries.

Log Fields
==========

The search log (``fess_log.search_log``) has one entry per search.
The fields most often used in aggregations are as follows.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``queryId``
     - keyword
     - ID of each search. Corresponds to ``queryId`` in the click log
   * - ``searchWord``
     - keyword
     - The search term. For a search filtered by a label, it also includes the condition, as in ``request label:"hr"``
   * - ``searchField.*``
     - keyword
     - The search term split by field. Ordinary terms go into ``searchField._default``, and label filters into ``searchField.label``
   * - ``requestedAt``
     - date
     - Date and time of the search (stored in UTC)
   * - ``hitCount``
     - long
     - Number of hits. ``0`` means a zero-hit search
   * - ``responseTime`` / ``queryTime``
     - long
     - Processing time of the whole search, and search time in OpenSearch (milliseconds)
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - Start position and page size. From the second page onward, ``queryOffset`` is greater than 0
   * - ``accessType``
     - keyword
     - One of ``json``, ``gsa``, ``admin``, ``other`` and ``web``. The search page of the default theme calls ``/api/v2/search``, so it is ``json``; searches from [System Info] > [Search] in the administration screen are ``admin``
   * - ``user`` / ``roles``
     - keyword
     - The ID of the logged-in user, and the list of roles used for the search. The first character of a ``roles`` value indicates its type: ``R`` is a role, ``2`` is a group and ``1`` is a user (example: ``Rguest``)
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - The cookie value that identifies the user, the IP address, the browser, the referrer and the virtual host

The click log (``fess_log.click_log``) is recorded when a link in the search results is opened via ``/go/``.
However, it is not recorded for requests where the browser has no Fess session (does not send a valid session cookie).

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``queryId``
     - keyword
     - ``queryId`` of the search the click came from
   * - ``url`` / ``docId``
     - keyword
     - URL and document ID of the opened document
   * - ``rank``
     - integer
     - Position across all search results (first place is 1). The first result on the second page is 11
   * - ``order``
     - integer
     - Position within the page (the first is 0). Use ``rank`` to aggregate positions
   * - ``searchWord`` / ``accessType``
     - keyword
     - Search term and access type copied from the originating search. You can aggregate by search term without joining with the search log
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - Date and time of the click, and of the originating search

``searchWord``, ``accessType`` and ``rank`` are included in click logs from 15.9 onward.
Clicks recorded before that do not have them.

Aggregation Recipes
===================

Here we build the four "aggregations the screen cannot do" listed at the beginning.
The first is built with Visualize, and the rest are run with the search API from [Dev Tools] in the left menu.

URLs Opened for Each Search Term
--------------------------------

This table shows, for each search term, which documents were opened at which positions.
It helps when choosing candidates for Key Match or Document Boost.

1. Click [Create visualization] in [Visualize] in the left menu and choose "Data Table"
2. Select ``fess_log.click_log`` as the source
3. Add a Metric with [Add] under Metrics, and choose "Average" for "Aggregation" and ``rank`` for "Field"
4. Under Buckets, choose [Add] > [Split rows], and set "Aggregation" to "Terms", "Field" to ``searchWord`` and "Size" to 20
5. Add another [Split rows] with "Terms", "Field" set to ``url`` and "Size" set to 5
6. Click [Update], choose the time range at the top right, and save

Combinations with a large average position are documents that users opened after going far down the results.

Zero-Hit Terms by Role
----------------------

If you assign roles per department, check what each department fails to find in its searches.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

``exclude`` removes values starting with ``1`` (individual users), so only roles and groups are listed.
A single search is counted under every role and group of that user.
Searches by users who are not logged in go into ``Rguest``.

Search Counts and Zero-Hit Counts by Label
------------------------------------------

For each label, count the searches made with that label selected on the search page, and how many of them returned zero hits.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

If no search filtered by a label has been recorded yet, the ``searchField.label`` field does not exist, so the ``labels`` buckets are empty.

Monthly Zero-Hit Rate (Two Years)
---------------------------------

Look at the long-term trend of the zero-hit rate (a ratio, not a count) beyond the period limit of the screen.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

Each monthly bucket returns the number of searches (``doc_count``), the number of zero-hit searches (``zero_hit.doc_count``) and the zero-hit rate (``zero_hit_rate.value``, between 0 and 1).
``time_zone`` makes months break at midnight in the given time zone (here ``Asia/Tokyo``; replace it with your own), and ``must_not`` excludes searches made from the administration screen.
Whether two years of logs are available depends on the retention settings described in the next section.

Retention and Personal Information
==================================

By default, search logs are kept forever.
This is because "Delete old search logs" under [System] > [General] defaults to ``-1`` (do not delete).
If you specify a number of days, the "Log Purger" job, which runs daily at midnight, deletes search logs older than that number of days.
Click logs, favorite logs and chat logs are deleted after the same number of days.
User records are controlled by a separate setting, "Delete old user logs", which also defaults to ``-1``.

Decide the number of days by weighing both how far back you want to see trends and your organization's rules for handling personal information.
Search logs contain the logged-in user's ID (``user`` and the ``roles`` values starting with ``1``), the IP address and the User-Agent.
In addition, by default the URLs and titles of the documents shown in the search results are recorded in the ``documents`` field (``logging.search.docs.enabled=true``).
All of these are visible in OpenSearch Dashboards, so follow the access restrictions described at the beginning.

Troubleshooting
===============

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptom
     - What to check
   * - No data appears in Discover or in visualizations
     - Whether the time range at the top right covers the dates of the logs. It can take about a minute after a search for the log to be written (the "Log Aggregator" job, which runs every minute, writes it)
   * - ``rank`` or ``searchField.label`` cannot be selected
     - Whether you are using ``fess_log*``. Create a dedicated index pattern, or click [Refresh field list]
   * - Counts are higher than on the [Search Log] screen
     - Whether ``fess_log*`` is also counting click or chat logs. Whether the access type filter and the time zone used for day boundaries are the same
   * - The number of clicks is low
     - Links do not go through ``/go/``, "Search Log" under [General] is disabled, or the browser opens ``/go/`` without a Fess session. Also check the prerequisites in :doc:`guide-08`

Further Reading
===============

- To improve the search terms you found with synonyms or Key Match: :doc:`guide-08`
- To review the design of roles and groups: :doc:`guide-05`
- To set up operations including monitoring and backup: :doc:`guide-10`
- To decide what to measure at each stage of a company-wide rollout: :doc:`guide-23`

References
==========

- `Search Log <https://fess.codelibs.org/stable/admin/searchlog-guide.html>`__
- `Search Log Visualization Configuration <https://fess.codelibs.org/stable/config/admin-opensearch-dashboards.html>`__
- `General Settings <https://fess.codelibs.org/stable/admin/general-guide.html>`__
- `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__
- `docker-fess Compose files (GitHub) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
