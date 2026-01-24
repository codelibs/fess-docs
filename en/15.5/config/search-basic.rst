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

When search results exceed 10,000 items, the search results screen displays "Approximately 10,000 or more results."
This is the default setting considering OpenSearch performance.

Search Example

|image0|

.. |image0| image:: ../../../resources/images/en/15.5/config/search-result.png

Displaying Accurate Hit Counts
-------------------------------

To display accurate hit counts for more than 10,000 items, change the following setting in ``fess_config.properties``.

::

    query.track.total.hits=100000

This setting allows you to retrieve accurate hit counts up to 100,000 items.
However, setting too large a value may impact performance.

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
By default, fuzzy search is automatically applied to keywords of 4 or more characters.

::

    search~

You can specify edit distance by adding a number after ``~``.

Search Result Sorting
=====================

Search results are sorted by relevance by default.
You can specify the following sort orders via administration screen settings or API parameters:

- Relevance order (default)
- Last modified date order
- Creation date order
- File size order

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

Search logs are stored in OpenSearch's ``fess_log`` index and
can be visualized and analyzed in OpenSearch Dashboards.
See :doc:`admin-opensearch-dashboards` for details.

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

Using Cache
-----------

By enabling search result caching, you can reduce response time for the same search queries.
Adjust cache settings according to system requirements.

Troubleshooting
===============

No Search Results Displayed
----------------------------

1. Verify that the index is created correctly.
2. Verify that crawling completed successfully.
3. Verify that access permissions are not set on search target documents.
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
