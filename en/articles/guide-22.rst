============================================================
Part 22: Drawing an Organizational Knowledge Map from Search Data -- Understanding Information Utilization through the Analytics Dashboard
============================================================

Introduction
============

A search system is a tool for "finding" information, but the search logs themselves are also a valuable source of information.
"What is being searched?", "What cannot be found?", "What information is frequently viewed?" -- these data points serve as a mirror reflecting the organization's information needs and knowledge gaps.

In this article, we combine Fess search logs with OpenSearch Dashboards to build an analytics dashboard that visualizes the organization's knowledge utilization status.

Target Audience
===============

- Those who want to quantitatively understand how their search system is being used
- Those who want to collect data for information utilization strategies
- Those who want to learn the basic operations of OpenSearch Dashboards

The Value of Search Data
========================

What Search Logs Can Tell Us
-----------------------------

Search logs are a rare type of data that allows quantitative understanding of an organization's information needs.

.. list-table:: Insights Gained from Search Data
   :header-rows: 1
   :widths: 30 70

   * - Data
     - Insight
   * - Search Keywords
     - What employees are looking for (information needs)
   * - Zero-Hit Queries
     - Information missing from the organization (knowledge gaps)
   * - Click Logs
     - Which search results were useful (content value)
   * - Search Frequency Over Time
     - Changes in information needs (trends)
   * - Popular Words
     - Topics of interest across the organization

Data Collected by Fess
=======================

Fess automatically collects and stores the following data.

Search Logs (``fess_log.search_log``)
--------------------------------------

These can be viewed in the admin console under [System Info] > [Search Log].
They are stored in the OpenSearch index ``fess_log.search_log``.

Key fields:

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field Name
     - Type
     - Description
   * - ``searchWord``
     - keyword
     - Search keyword
   * - ``requestedAt``
     - date
     - Search date and time
   * - ``hitCount``
     - long
     - Number of search results (0 indicates a zero-hit query)
   * - ``queryTime``
     - long
     - Query execution time (milliseconds)
   * - ``responseTime``
     - long
     - Total response time (milliseconds)
   * - ``userAgent``
     - keyword
     - User agent
   * - ``clientIp``
     - keyword
     - Client IP address
   * - ``accessType``
     - keyword
     - Access type (web, json, gsa, admin, etc.)
   * - ``queryId``
     - keyword
     - Query ID (used for linking with click logs)

Click Logs (``fess_log.click_log``)
------------------------------------

These are records of when search result links are clicked.
They are stored in the OpenSearch index ``fess_log.click_log``.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field Name
     - Type
     - Description
   * - ``url``
     - keyword
     - Clicked URL
   * - ``queryId``
     - keyword
     - queryId from the search log (identifies which search led to the click)
   * - ``order``
     - integer
     - Display position in search results
   * - ``requestedAt``
     - date
     - Click date and time
   * - ``docId``
     - keyword
     - Document ID

Popular Words
--------------

The popular words displayed on the search screen are aggregated from search logs into the Fess suggest index.
Queries that exceed a certain number of search hits are ranked based on the number of searches.

Visualization with OpenSearch Dashboards
=========================================

Since Fess search logs are stored in OpenSearch, advanced visualization is possible using OpenSearch Dashboards.

Setting Up OpenSearch Dashboards
---------------------------------

Add OpenSearch Dashboards to your Docker Compose configuration.

.. code-block:: yaml

    services:
      opensearch-dashboards:
        image: opensearchproject/opensearch-dashboards:3.6.0
        ports:
          - "5601:5601"
        environment:
          OPENSEARCH_HOSTS: '["http://opensearch:9200"]'
          DISABLE_SECURITY_DASHBOARDS_PLUGIN: "true"

Access ``http://localhost:5601`` to use the Dashboards UI.

Creating Index Patterns
------------------------

To visualize Fess log data in OpenSearch Dashboards, you first need to create index patterns.

1. Access Dashboards and select [Stack Management] > [Index Patterns] from the left menu
2. Click [Create index pattern]
3. Create the following index patterns

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Index Pattern
     - Time Field
     - Purpose
   * - ``fess_log.search_log``
     - ``requestedAt``
     - Search log analysis
   * - ``fess_log.click_log``
     - ``requestedAt``
     - Click log analysis

Dashboard Design
=================

Design the dashboard with the following analytical perspectives.
Create each visualization from [Visualize] in the left menu, and combine them in a [Dashboard].

Search Usage Overview
----------------------

**Daily Search Count Trends**

Understand how search usage is changing over time.

- Index Pattern: ``fess_log.search_log``
- Visualization: Line (line chart)
- X-axis: Date Histogram (field: ``requestedAt``, interval: 1d)
- Y-axis: Count

If usage is increasing, it is evidence that the search system has become established; if decreasing, improvements are needed.

**Search Count by Time of Day**

Understand which times of day have the most searches.

- Visualization: Vertical Bar (bar chart)
- X-axis: Date Histogram (field: ``requestedAt``, interval: 1h)
- Y-axis: Count

If searches are frequent at the start of the workday or after lunch, it indicates that information gathering has become an established part of daily work.

Search Quality Analysis
------------------------

**Zero-Hit Rate Trends**

The zero-hit rate is an important indicator of search quality.
Records where the ``hitCount`` field in the search log is ``0`` correspond to zero-hit queries.

- Index Pattern: ``fess_log.search_log``
- Filter: Add ``hitCount: 0`` to extract zero-hit queries
- Visualization: Line (line chart)
- X-axis: Date Histogram (field: ``requestedAt``, interval: 1d)
- Y-axis: Count

If the zero-hit rate is high, adding synonyms or expanding the crawl scope is necessary (see Part 8).

Note that you can also view a list of zero-hit queries in the admin console under [System Info] > [Search Log].

**Zero-Hit Query Word Cloud**

Displaying zero-hit queries as a word cloud provides an at-a-glance view of what information is missing.

- Filter: ``hitCount: 0``
- Visualization: Tag Cloud
- Field: Terms Aggregation (field: ``searchWord``, size: 50)

Content Value Analysis
-----------------------

**Most Clicked Search Results**

Frequently clicked search results represent high-value content for the organization.

- Index Pattern: ``fess_log.click_log``
- Visualization: Data Table
- Field: Terms Aggregation (field: ``url``, size: 20, sort: Count descending)

Prioritize the maintenance and updating of these content items.

**Click Position Distribution**

Review the distribution of which position in search results is being clicked.

- Index Pattern: ``fess_log.click_log``
- Visualization: Vertical Bar (bar chart)
- X-axis: Histogram (field: ``order``, interval: 1)
- Y-axis: Count

If positions 1-3 receive the most clicks, search quality is good; if positions 10 and beyond receive many clicks, ranking improvements are needed.

Information Needs Trend Analysis
---------------------------------

**Popular Keyword Rankings**

Understand what the organization as a whole is interested in.

- Index Pattern: ``fess_log.search_log``
- Visualization: Data Table
- Field: Terms Aggregation (field: ``searchWord``, size: 20, sort: Count descending)

Changes in popular keywords reflect changes in the organization's challenges and interests.

Leveraging Analysis Results
============================

Search data analysis results can be applied to the following initiatives.

Content Strategy
-----------------

- **Zero-Hit Queries**: Identify missing content and request its creation
- **Popular Keywords**: Enrich information on frequently searched topics
- **Low Click-Rate Results**: Consider improving or removing content

Improving Search Quality
-------------------------

- **Adding Synonyms**: Discover synonym candidates from zero-hit queries
- **Key Match Configuration**: Set optimal results for popular queries
- **Boost Adjustment**: Improve rankings based on click-through rates

IT Investment Decisions
------------------------

- **Increasing Usage**: Plan for server resource expansion
- **New Information Needs**: Consider connecting additional data sources
- **AI Feature Needs**: Decide on introducing AI search mode (see Part 19)

Creating Regular Reports
=========================

Summarize analysis results into periodic reports and share them with stakeholders.

Example Monthly Report Items
------------------------------

1. Search usage summary (total search count, month-over-month comparison)
2. Zero-hit rate trends and improvement status
3. Top 10 popular keywords
4. Newly discovered knowledge gaps
5. Improvement measures implemented and their effects
6. Improvement plans for the next month

Conclusion
==========

In this article, we explained how to visualize organizational knowledge utilization using search logs.

- Insights gained from search logs (information needs, knowledge gaps, content value)
- Building visualization dashboards with OpenSearch Dashboards
- Applying analysis results to content strategy, search quality improvement, and IT investment
- Continuous improvement through regular reports

Search data is a valuable asset for drawing an "organizational knowledge map."
This concludes the AI and next-generation search section. In the next and final installment, we will provide an overall summary of the series.

References
==========

- `Fess Search Log <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/>`__
