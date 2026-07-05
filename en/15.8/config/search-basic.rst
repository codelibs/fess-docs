===============
Search Features
===============

Overview
========

|Fess| provides powerful full-text search capabilities.
This section explains detailed configuration and usage of search features.

Search Result Count Display
============================

Default Behavior
----------------

The default value of ``query.track.total.hits`` is ``10000``.
Therefore, when search results exceed 10,000 items, the search results screen displays "Approximately 10,000 or more results."
This is the default setting where OpenSearch limits the upper bound for counting exact total hits to the value of ``query.track.total.hits``, in order to reduce the performance impact of large-scale searches.

Search Example

|image0|

.. |image0| image:: ../../../resources/images/en/15.8/config/search-result.png

Displaying Accurate Hit Counts
-------------------------------

To display accurate hit counts beyond the default limit, change the value of ``query.track.total.hits`` in ``fess_config.properties``.

::

    query.track.total.hits=100000

In the above example, you can retrieve accurate hit counts up to 100,000 items.
The threshold at which the count is displayed as "Approximately N or more" also changes in line with this configured value.
However, setting a large value may impact performance.

.. warning::
   Setting the value too high may degrade search performance.
   Set an appropriate value based on actual usage.

Search Options
==============

Basic Search
------------

In |Fess|, simply entering keywords in the search box executes a full-text search.
Entering multiple keywords executes an AND search.

::

    search engine

The above example searches for documents containing both "search" and "engine".

OR Search
---------

To execute an OR search, insert ``OR`` between keywords.

::

    search OR engine

NOT Search
----------

To exclude specific keywords, prefix the keyword with ``-`` (minus sign).

::

    search -engine

Phrase Search
-------------

To search for an exact phrase, enclose it in double quotes.

::

    "search engine"

Field-Specific Search
---------------------

You can search by specifying specific fields.

::

    title:search engine
    url:https://fess.codelibs.org/

Main fields:

- ``title``: Document title
- ``content``: Document body
- ``url``: Document URL
- ``filetype``: File type (e.g., pdf, html, doc)
- ``label``: Label (classification)
- ``mimetype``: MIME type (e.g., text/html, application/pdf)
- ``filename``: File name
- ``host``: Host name
- ``site``: Site (combination of host name and path)
- ``lang``: Language

Additional fields to search can be added via ``query.additional.search.fields`` in ``fess_config.properties``.

Wildcard Search
---------------

Wildcard searches are available.

- ``*``: Any string of zero or more characters
- ``?``: Any single character

::

    search*
    se?rch

Fuzzy Search
------------

Fuzzy search for spelling mistakes and notation variations is available.
By default, for keywords of 4 or more characters, a fuzzy search query is additionally executed alongside the normal search.

::

    search~

You can specify edit distance by adding a number after ``~``.

Search Result Sorting
=====================

Search results are sorted by relevance by default.
You can specify the following sort orders via administration screen settings or API parameters:

- Relevance order (``score``, default)
- Last modified date order (``last_modified``)
- Creation date order (``created``)
- File size order (``content_length``)
- File name order (``filename``)
- Click count order (``click_count``)
- Favorite count order (``favorite_count``)

Additional sort fields can be added via ``query.additional.sort.fields`` in ``fess_config.properties``.

Faceted Search
==============

Faceted search allows you to narrow down search results by category.
By default, the label field is configured as a facet.

You can narrow down search results by clicking facets displayed on the left side of the search screen.

Search Result Highlighting
===========================

Search keywords are highlighted in the title and summary sections of search results.
Highlight settings can be customized in ``fess_config.properties``.

::

    query.highlight.tag.pre=<strong>
    query.highlight.tag.post=</strong>
    query.highlight.fragment.size=60
    query.highlight.number.of.fragments=2

- ``query.highlight.tag.pre`` / ``query.highlight.tag.post``: Tags surrounding highlighted text (default: ``<strong>`` / ``</strong>``)
- ``query.highlight.fragment.size``: Number of characters per highlight fragment (default: ``60``)
- ``query.highlight.number.of.fragments``: Maximum number of fragments to display (default: ``2``)

The fields used as highlight targets for the summary (snippet) are specified by ``query.highlight.content.description.fields`` (default: ``hl_content,digest``).

Suggest Feature
===============

When entering text in the search box, suggestions (autocomplete) are displayed.
Suggestions are generated based on past search keywords and popular search keywords.

The suggest feature can be enabled/disabled in the "General" settings on the administration screen.

Search Logs
===========

|Fess| records all search queries and click logs.
These logs can be used for:

- Analyzing and improving search quality
- Analyzing user behavior
- Understanding popular search keywords
- Identifying keywords with zero search results

Search logs and click logs are stored in OpenSearch indexes with the ``fess_log`` prefix
(search queries in the ``fess_log.search_log`` index, click logs in the ``fess_log.click_log`` index).
These logs can be visualized and analyzed using OpenSearch Dashboards.
|Fess| includes a bundled dashboard definition file for visualization. See :doc:`admin-opensearch-dashboards` for details.

Performance Tuning
==================

Search Timeout Configuration
-----------------------------

You can configure search timeout duration. The default is 10 seconds.

::

    query.timeout=10000

Maximum Query Length
--------------------

For security and performance, you can limit the maximum query length.

::

    query.max.length=1000

Cache Usage
-----------

|Fess| itself does not have a feature for caching search results (search responses).
However, the backend OpenSearch provides shard request cache and query cache at the engine level, which help reduce response time for repeated searches with the same conditions.
Since these are OpenSearch-level features, adjust them through OpenSearch configuration as needed.

Troubleshooting
===============

No Search Results Displayed
----------------------------

1. Verify that the index is created correctly.
2. Verify that crawling completed successfully.
3. Verify that the target documents are not being excluded for the current user (including guests) by role/permission-based search filtering.
4. Verify that OpenSearch is operating normally.

Slow Search Speed
-----------------

1. Check OpenSearch heap memory size.
2. Optimize index shard count and replica count.
3. Check search query complexity.
4. Check hardware resources (CPU, memory, disk I/O).

Irrelevant Results Displayed
-----------------------------

1. Adjust boost settings (``query.boost.title``, ``query.boost.content``, etc.).
2. Review fuzzy search settings.
3. Check Analyzer configuration.
4. If necessary, consult commercial support.
5. You can also improve search accuracy by utilizing Rank Fusion. See :doc:`rank-fusion` for details.
