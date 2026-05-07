================================
Search Log Visualization Configuration
================================

About Search Log Visualization
===============================

|Fess| captures user search logs and click logs.
The captured search logs can be analyzed and visualized using `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__.

Information That Can Be Visualized
-----------------------------------

With the default configuration, the following information can be visualized:

-  Average time to display search results
-  Search frequency per second
-  User Agent ranking
-  Search keyword ranking
-  Search keyword ranking with zero search results
-  Total number of search results
-  Search trends over time

You can build custom monitoring dashboards by creating new graphs using the Visualize feature and adding them to Dashboards.

Data Visualization Configuration with OpenSearch Dashboards
============================================================

Installing OpenSearch Dashboards
---------------------------------

OpenSearch Dashboards is a tool for visualizing data from the OpenSearch used by |Fess|.
Install OpenSearch Dashboards following the `OpenSearch official documentation <https://opensearch.org/docs/latest/install-and-configure/install-dashboards/index/>`__.

Editing Configuration File
---------------------------

Edit the configuration file ``config/opensearch_dashboards.yml`` to make OpenSearch Dashboards recognize the OpenSearch used by |Fess|.

::

    opensearch.hosts: ["http://localhost:9201"]

Change ``localhost`` to an appropriate hostname or IP address for your environment.
In |Fess|'s default configuration, OpenSearch starts on port 9201.

.. note::
   If the OpenSearch port number is different, change it to the appropriate port number.

Starting OpenSearch Dashboards
-------------------------------

After editing the configuration file, start OpenSearch Dashboards.

::

    $ cd /path/to/opensearch-dashboards
    $ ./bin/opensearch-dashboards

After startup, access ``http://localhost:5601`` in your browser.

Index Pattern Configuration
----------------------------

1. Select the "Management" menu from the OpenSearch Dashboards home screen.
2. Select "Index Patterns".
3. Click the "Create index pattern" button.
4. Enter ``fess_log*`` in Index pattern name.
5. Click the "Next step" button.
6. Select ``requestedAt`` for Time field.
7. Click the "Create index pattern" button.

This completes the preparation for visualizing |Fess| search logs.

Creating Visualizations and Dashboards
---------------------------------------

Creating Basic Visualizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Select "Visualize" from the left menu.
2. Click the "Create visualization" button.
3. Select a visualization type (line chart, pie chart, bar chart, etc.).
4. Select the created index pattern ``fess_log*``.
5. Configure necessary metrics and buckets (aggregation units).
6. Click the "Save" button to save the visualization.

Creating Dashboards
~~~~~~~~~~~~~~~~~~~

1. Select "Dashboard" from the left menu.
2. Click the "Create dashboard" button.
3. Click the "Add" button to add created visualizations.
4. Adjust the layout and click the "Save" button to save.

Timezone Configuration
----------------------

If the time display is incorrect, configure the timezone.

1. Select "Management" from the left menu.
2. Select "Advanced Settings".
3. Search for ``dateFormat:tz``.
4. Set the timezone to an appropriate value (e.g., ``Asia/Tokyo`` or ``UTC``).
5. Click the "Save" button.

Checking Log Data
-----------------

1. Select "Discover" from the left menu.
2. Select the index pattern ``fess_log*``.
3. Search log data will be displayed.
4. You can specify the period to display with the time range selection in the upper right.

Main Search Log Fields
----------------------

|Fess| search logs contain information such as:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field Name
     - Description
   * - ``queryId``
     - Unique identifier for search query
   * - ``searchWord``
     - Search keyword
   * - ``requestedAt``
     - Date and time when search was executed
   * - ``responseTime``
     - Search result response time (milliseconds)
   * - ``queryTime``
     - Query execution time (milliseconds)
   * - ``hitCount``
     - Number of search result hits
   * - ``userAgent``
     - User's browser information
   * - ``clientIp``
     - Client IP address
   * - ``languages``
     - Language used
   * - ``roles``
     - User role information
   * - ``user``
     - Username (when logged in)

You can analyze search logs from various perspectives using these fields.

Troubleshooting
---------------

If Data Is Not Displayed
~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that OpenSearch is started correctly.
- Verify that the ``opensearch.hosts`` setting in ``opensearch_dashboards.yml`` is correct.
- Verify that searches are being executed in |Fess| and logs are being recorded.
- Verify that the time range of the index pattern is set appropriately.

If Connection Errors Occur
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the OpenSearch port number is correct.
- Check firewall or security group settings.
- Check OpenSearch log files for errors.
