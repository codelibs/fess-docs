==========================================
Search Log Visualization Configuration
==========================================

About Search Log Visualization
================================

|Fess| captures user search logs and click logs.
The captured search logs can be analyzed and visualized using `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__.

|Fess| includes a dashboard definition file ``extension/kibana/fess_log.ndjson`` for visualizing search logs.
By importing this file into OpenSearch Dashboards, you can immediately use the pre-built dashboards.

Information That Can Be Visualized
------------------------------------

Importing the bundled dashboard definition (``fess_log.ndjson``) registers the ``fess_log`` dashboard and the following six visualizations.

-  Average response time to display search results (``average-response-time``)
-  Number of search requests per unit time (``search-query-counts-per-sec``)
-  User Agent ranking of accessing users (``rank-of-UserAgent``)
-  Search keyword ranking (``search-term-rank``)
-  Search keyword ranking with zero search results (``search-term-rank-of-no-results``)
-  Average number of search result hits (``hit-counts``)

In addition to these, you can build custom monitoring dashboards by creating new graphs using the Visualize feature and adding them to the dashboard.

Data Visualization Configuration with OpenSearch Dashboards
=============================================================

Installing OpenSearch Dashboards
----------------------------------

OpenSearch Dashboards is a tool for visualizing data from the OpenSearch used by |Fess|.
Install OpenSearch Dashboards following the `OpenSearch official documentation <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Editing Configuration File
----------------------------

Edit the configuration file ``config/opensearch_dashboards.yml`` to make OpenSearch Dashboards recognize the OpenSearch used by |Fess|.

::

    opensearch.hosts: ["http://localhost:9201"]

Change ``localhost`` to an appropriate hostname or IP address for your environment.
In |Fess|'s default configuration, OpenSearch starts on port 9201.

.. note::
   If the OpenSearch port number is different, change it to the appropriate port number.

Starting OpenSearch Dashboards
--------------------------------

After editing the configuration file, start OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

After startup, access ``http://localhost:5601`` in your browser.

Index Pattern Configuration
-----------------------------

Create an index pattern for visualizing search logs.

1. Select "Management" from the left menu (or "Dashboards Management" depending on your version of OpenSearch Dashboards).
2. Select "Index Patterns".
3. Click the "Create index pattern" button.
4. Enter ``fess_log*`` in Index pattern name.
5. Click the "Next step" button.
6. Select ``requestedAt`` for Time field.
7. Click the "Create index pattern" button.

.. note::
   |Fess| search logs are recorded in multiple indices starting with ``fess_log``, such as ``fess_log.search_log`` for search logs and ``fess_log.click_log`` for click logs.
   By specifying the ``fess_log*`` index pattern, you can target all of these at once.

Importing Dashboard Definition
--------------------------------

By importing the dashboard definition bundled with |Fess|, you can use the pre-built visualizations and dashboard.

1. Select "Management" from the left menu (or "Dashboards Management" depending on your version of OpenSearch Dashboards).
2. Select "Saved Objects".
3. Click "Import".
4. Select ``extension/kibana/fess_log.ndjson`` from the |Fess| installation directory.
5. Click "Import" to execute the import.

Once the import is complete, six visualizations and the ``fess_log`` dashboard will be registered.

Displaying the Dashboard
--------------------------

1. Select "Dashboard" from the left menu.
2. Select the ``fess_log`` dashboard.
3. The visualization results of the search logs will be displayed.
4. You can specify the period to display with the time range selection in the upper right.

Creating Custom Visualizations
--------------------------------

In addition to the bundled dashboards, you can also create your own visualizations and dashboards.

Creating Visualizations
~~~~~~~~~~~~~~~~~~~~~~~~

1. Select "Visualize" from the left menu.
2. Click the "Create visualization" button.
3. Select a visualization type (line chart, pie chart, bar chart, etc.).
4. Select the created index pattern ``fess_log*``.
5. Configure necessary metrics and buckets (aggregation units).
6. Click the "Save" button to save the visualization.

Creating Dashboards
~~~~~~~~~~~~~~~~~~~~

1. Select "Dashboard" from the left menu.
2. Click the "Create dashboard" button.
3. Click the "Add" button to add the visualizations you created.
4. Adjust the layout and click the "Save" button to save.

Timezone Configuration
------------------------

If the time display is incorrect, configure the timezone.

1. Select "Management" from the left menu (or "Dashboards Management" depending on your version of OpenSearch Dashboards).
2. Select "Advanced Settings".
3. Search for ``dateFormat:tz``.
4. Set the timezone to an appropriate value (e.g., ``Asia/Tokyo`` or ``UTC``).
5. Click the "Save" button.

Checking Log Data
------------------

1. Select "Discover" from the left menu.
2. Select the index pattern ``fess_log*``.
3. Search log data will be displayed.
4. You can specify the period to display with the time range selection in the upper right.

Main Search Log Fields
-----------------------

|Fess| search logs (``fess_log.search_log``) contain the following information.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field Name
     - Description
   * - ``queryId``
     - Unique identifier for the search query
   * - ``searchWord``
     - Search keyword
   * - ``requestedAt``
     - Date and time when the search was executed
   * - ``responseTime``
     - Overall response time for search processing (milliseconds)
   * - ``queryTime``
     - Query execution time to the search engine (milliseconds)
   * - ``hitCount``
     - Number of search result hits
   * - ``hitCountRelation``
     - Relationship indicating whether the hit count is an exact value or a lower bound (``eq``: exact count, ``gte``: greater than or equal to the specified value)
   * - ``queryOffset``
     - Starting position for retrieving search results
   * - ``queryPageSize``
     - Number of items displayed per page
   * - ``userAgent``
     - User's browser information
   * - ``referer``
     - Referring URL of the page from which the search was executed
   * - ``clientIp``
     - Client IP address
   * - ``languages``
     - Language used in the request
   * - ``accessType``
     - Access type (``web``, ``json``, ``gsa``, ``admin``, ``other``)
   * - ``roles``
     - User role information
   * - ``user``
     - Username (when logged in)
   * - ``virtualHost``
     - Virtual host name (if configured)

You can analyze search logs from various perspectives using these fields.

Troubleshooting
----------------

If Data Is Not Displayed
~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that OpenSearch is started correctly.
- Verify that the ``opensearch.hosts`` setting in ``opensearch_dashboards.yml`` is correct.
- Verify that searches are being executed in |Fess| and logs are being recorded.
- Verify that the time range in the upper right is set to include the period when logs were recorded.
- If the time display is off, check the ``dateFormat:tz`` setting.

If Connection Errors Occur
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the OpenSearch port number is correct.
- Check firewall or security group settings.
- Check OpenSearch log files for errors.
