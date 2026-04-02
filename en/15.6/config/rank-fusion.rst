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

Supported Algorithm
====================

|Fess| uses the RRF (Reciprocal Rank Fusion) algorithm for Rank Fusion.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calculates scores by summing the reciprocal of each result's rank.

Formula::

    score(d) = Σ 1 / (k + rank(d))

- ``k``: Rank constant parameter (default: 20)
- ``rank(d)``: Rank of document d in each search result

Settings
========

fess_config.properties
----------------------

Configuration properties::

    # Window size for rank fusion
    rank.fusion.window_size=200

    # Rank constant (k parameter for RRF)
    rank.fusion.rank_constant=20

    # Number of threads (-1 for auto)
    rank.fusion.threads=-1

    # Score field name in results
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Property
     - Default
     - Description
   * - ``rank.fusion.window_size``
     - ``200``
     - Number of results to consider from each search type for fusion
   * - ``rank.fusion.rank_constant``
     - ``20``
     - The k constant in the RRF formula; controls how much weight is given to lower-ranked results
   * - ``rank.fusion.threads``
     - ``-1``
     - Number of threads for parallel execution (-1 for automatic)
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Field name used to store the computed rank fusion score

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

Performance Considerations
===========================

- Adjust ``rank.fusion.window_size`` to balance quality and speed; larger values consider more candidates but use more memory
- Set ``rank.fusion.threads`` to control parallelism; ``-1`` automatically determines the thread count
- Memory usage increases with larger window sizes as more search results are retained

Troubleshooting
================

Search Results Differ from Expectations
-----------------------------------------

**Symptom**: Results after Rank Fusion differ from expectations

**Checks**:

1. Verify results from each search type individually
2. Adjust the ``rank.fusion.rank_constant`` value
3. Adjust ``rank.fusion.window_size`` to include more candidate results

Out of Memory
--------------

**Symptom**: OutOfMemoryError occurs

**Solutions**:

1. Reduce ``rank.fusion.window_size``
2. Increase JVM heap size
3. Disable unnecessary search types

Reference
=========

- :doc:`scripting-overview` - Scripting Overview
- :doc:`search-advanced` - Advanced Search Settings
- :doc:`llm-overview` - LLM Integration Guide (Semantic Search)
