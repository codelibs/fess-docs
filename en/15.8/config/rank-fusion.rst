==================================
Rank Fusion Settings
==================================

Overview
========

The Rank Fusion feature of |Fess| integrates multiple search results to
provide more accurate search results.

What is Rank Fusion
===================

Rank Fusion is a technique that combines results from multiple search algorithms
or scoring methods to generate a single optimized ranking.

Key benefits:

- Combines the strengths of different algorithms
- Improves search accuracy
- Provides diverse search results

Supported Algorithm
===================

|Fess| supports the RRF (Reciprocal Rank Fusion) algorithm for Rank Fusion.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calculates a score by summing the reciprocal of each document's rank in each
search result. When a document is retrieved by multiple searchers, its scores are
added together.

Formula::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Constant parameter that controls the influence of rank (default: 20)
- ``rank(d)``: Rank of document d in each search result (0-based)
- ``Σ``: Sum over all searchers in which document d appears

Settings
========

fess_config.properties
----------------------

Basic configuration::

    # Window size (number of results to fuse)
    # Note: Must be >= paging.search.page.max.size × 2.
    # If the value is below this minimum, the minimum is used automatically.
    rank.fusion.window_size=200

    # Rank constant (k parameter for RRF)
    rank.fusion.rank_constant=20

    # Number of threads for parallel processing
    # (if 0 or less, availableProcessors × 1.5 + 1 is used)
    rank.fusion.threads=-1

    # Score field name (field that stores the fused score)
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Property
     - Default
     - Description
   * - ``rank.fusion.window_size``
     - ``200``
     - Maximum number of results retrieved from each searcher for fusion. Must be >= ``paging.search.page.max.size × 2`` (``200`` by default); if a smaller value is set, it is automatically raised to this minimum.
   * - ``rank.fusion.rank_constant``
     - ``20``
     - The constant ``k`` in the RRF formula. A larger value reduces the score difference between higher- and lower-ranked results.
   * - ``rank.fusion.threads``
     - ``-1``
     - Number of threads used when running multiple searchers in parallel. If ``0`` or less is specified, ``availableProcessors × 1.5 + 1`` is used automatically.
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Name of the result-document field used to store the fused score.

JVM System Properties
---------------------

The searchers to use are specified as a JVM system property. Add the following to
``fess.in.sh`` (or ``fess.in.bat``)::

    # Specify searchers (comma-separated)
    -Drank.fusion.searchers=default,semantic

This property behaves as follows:

- It is set as a JVM option, not in ``fess_config.properties``.
- ``default`` is the searcher that performs standard keyword search and is always available.
- ``semantic`` is the searcher that performs semantic (vector) search and is available when the Semantic Search plugin (``fess-webapp-semantic-search``) is installed.
- If this property is not specified, all registered searchers are used. If none of the specified names match a registered searcher, only the ``default`` searcher is used.
- Result fusion is performed only when two or more searchers are available. When only one searcher is available, no fusion is performed and normal search results are returned.

Integration with Hybrid Search
===============================

Rank Fusion is particularly effective for hybrid search, which combines keyword
search and semantic search. To use semantic search, install the Semantic Search
plugin (``fess-webapp-semantic-search``) and add ``semantic`` to
``-Drank.fusion.searchers``.

Usage Examples
==============

Basic Hybrid Search
-------------------

1. Calculate the BM25 score with keyword search
2. Calculate vector similarity with semantic search
3. Fuse both results with RRF
4. Generate the final ranking

Search Flow::

    User Query
        ↓
    ┌──────────────────┬──────────────────┐
    │  Keyword Search  │ Semantic Search  │
    │    (BM25)        │  (Vector)        │
    └────────┬─────────┴────────┬─────────┘
             ↓                  ↓
         Rank List 1        Rank List 2
             └────────┬─────────┘
                      ↓
              Rank Fusion (RRF)
                      ↓
              Final Ranking

Performance Considerations
==========================

Memory Usage
------------

- Memory usage increases because multiple search results are retained.
- Use ``rank.fusion.window_size`` to limit the maximum number of results to fuse. The main searcher (the leading ``default`` searcher) retrieves up to ``window_size`` results, while each of the other searchers retrieves ``window_size ÷ number of searchers`` results.

::

    # Window size for fusion
    rank.fusion.window_size=200

Processing Time
---------------

- Response time increases because multiple searches are executed.
- Use ``rank.fusion.threads`` to set the number of threads for parallel execution.

::

    # Number of threads for parallel execution
    # (if 0 or less, availableProcessors × 1.5 + 1)
    rank.fusion.threads=-1

Troubleshooting
===============

Search Results Differ from Expectations
----------------------------------------

**Symptom**: Results after Rank Fusion differ from expectations

**Checks**:

1. Verify the results of each search type individually
2. Adjust the ``rank.fusion.rank_constant`` value
3. Adjust the ``rank.fusion.window_size`` value
4. On deep pages (where ``start position × 2`` is greater than or equal to ``rank.fusion.window_size``), fusion is not performed and only the main searcher is used. If you want fused results on more pages, increase ``rank.fusion.window_size``.

Slow Search
-----------

**Symptom**: Search becomes slow when Rank Fusion is enabled

**Solutions**:

1. Reduce ``rank.fusion.window_size``::

       rank.fusion.window_size=100

2. Adjust ``rank.fusion.threads``::

       rank.fusion.threads=4

Out of Memory
-------------

**Symptom**: OutOfMemoryError occurs

**Solutions**:

1. Reduce ``rank.fusion.window_size``
2. Increase the JVM heap size

Reference
=========

- :doc:`scripting-overview` - Scripting Overview
- :doc:`search-advanced` - Advanced Search Settings
- :doc:`llm-overview` - LLM Integration Guide (Semantic Search)
