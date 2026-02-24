==================================
Rank Fusion Settings
==================================

Overview
========

The Rank Fusion feature of |Fess| integrates multiple search results to
provide more accurate search results.

What is Rank Fusion
====================

Rank Fusion is a technique that combines results from multiple search algorithms
or scoring methods to generate a single optimized ranking.

Key benefits:

- Combines the strengths of different algorithms
- Improves search accuracy
- Provides diverse search results

Supported Algorithms
=====================

|Fess| supports the following Rank Fusion algorithms:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Algorithm
     - Description
   * - RRF (Reciprocal Rank Fusion)
     - A fusion algorithm using reciprocal of ranks
   * - Score Fusion
     - Fusion through score normalization and weighted average
   * - Borda Count
     - Vote-based ranking fusion

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calculates scores by summing the reciprocal of each result's rank.

Formula::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Constant parameter (default: 60)
- ``rank(d)``: Rank of document d in each search result

Settings
========

fess_config.properties
----------------------

Basic settings::

    # Enable Rank Fusion
    rank.fusion.enabled=true

    # Algorithm to use
    rank.fusion.algorithm=rrf

    # RRF k parameter
    rank.fusion.rrf.k=60

    # Search types for fusion
    rank.fusion.search.types=keyword,semantic

Algorithm-Specific Settings
----------------------------

RRF settings::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Score Fusion settings::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Borda Count settings::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

Integration with Hybrid Search
================================

Rank Fusion is particularly effective in hybrid search that combines
keyword search and semantic search.

Configuration Example
----------------------

::

    # Enable hybrid search
    search.hybrid.enabled=true

    # Fuse keyword search and semantic search results
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # Weight for each search type
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

Usage Examples
==============

Basic Hybrid Search
--------------------

1. Calculate BM25 score with keyword search
2. Calculate vector similarity with semantic search
3. Fuse both results with RRF
4. Generate final ranking

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

Custom Scoring
--------------------

Example of combining multiple score factors::

    # Base search score + Date boost + Popularity
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

Performance Considerations
===========================

Memory Usage
------------

- Memory usage increases as multiple search results are retained
- Limit the maximum number of fusion targets with ``rank.fusion.max.results``

::

    # Maximum number of results for fusion
    rank.fusion.max.results=1000

Processing Time
----------------

- Response time increases as multiple searches are executed
- Consider optimization through parallel execution

::

    # Enable parallel execution
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

Cache
------

- Use caching for frequent queries

::

    # Cache for Rank Fusion results
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

Troubleshooting
================

Search Results Differ from Expectations
-----------------------------------------

**Symptom**: Results after Rank Fusion differ from expectations

**Checks**:

1. Verify results from each search type individually
2. Verify that weighting is appropriate
3. Adjust the k parameter value

Search is Slow
---------------

**Symptom**: Search becomes slow when Rank Fusion is enabled

**Solutions**:

1. Enable parallel execution::

       rank.fusion.parallel=true

2. Limit the number of fusion target results::

       rank.fusion.max.results=500

3. Enable caching::

       rank.fusion.cache.enabled=true

Out of Memory
--------------

**Symptom**: OutOfMemoryError occurs

**Solutions**:

1. Reduce the maximum number of fusion target results
2. Increase JVM heap size
3. Disable unnecessary search types

Reference
=========

- :doc:`scripting-overview` - Scripting Overview
- :doc:`../admin/search-settings` - Search Settings Guide
- :doc:`llm-overview` - LLM Integration Guide (Semantic Search)
