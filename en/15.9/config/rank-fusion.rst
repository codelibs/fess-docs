===================================================
Hybrid Search and Rank Fusion (Semantic + Keyword)
===================================================

Overview
========

**Hybrid search** in |Fess| combines traditional keyword search (BM25) with **semantic (vector) search** and merges the two result sets with **Rank Fusion** to produce more accurate, more relevant rankings. Rank Fusion integrates the results of multiple searchers into a single optimized ranking.

In |Fess| 15.9, semantic search (content chunking + vector search) is provided as a core
feature. Once you enable it, the semantic searcher is registered with Rank Fusion automatically.
See :doc:`search-semantic` for how to configure it.

The Rank Fusion feature of |Fess| integrates multiple search results to
provide more accurate search results.

What is Rank Fusion
===================

Rank Fusion is a technique that combines results from multiple search algorithms
or scoring methods (for example keyword/BM25 and semantic/vector search) to generate a single optimized ranking.

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

.. note::

   When |Fess| performs the fusion (the default), the algorithm is fixed to RRF and per-searcher
   weighting is not supported: every searcher contributes with the same weight when the scores are
   summed, and ``rank.fusion.rank_constant`` is the only setting that lets you adjust the ranking
   behavior. When the search engine performs the fusion, other combination techniques and
   per-searcher weights are available (see :ref:`rank-fusion-engine`).

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
    # (if 0 or less, availableProcessors × 3 / 2 + 1 is used)
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
     - Maximum number of results retrieved from each searcher for fusion. Must be >= ``paging.search.page.max.size × 2`` (``200`` by default); if a smaller value is set, it is automatically raised to this minimum (a WARN log is written at startup).
   * - ``rank.fusion.rank_constant``
     - ``20``
     - The constant ``k`` in the RRF formula. A larger value reduces the score difference between higher- and lower-ranked results.
   * - ``rank.fusion.threads``
     - ``-1``
     - Number of threads in the fixed thread pool used to run multiple searchers in parallel. If ``0`` or less is specified, ``availableProcessors × 3 / 2 + 1`` is used automatically (the calculation uses integer arithmetic, so the fractional part is truncated: for example, 4 cores → 7 and 5 cores → 8).
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Name of the result-document field used to store the fused score.

.. note::

   **When changes take effect**

   All four settings above require |Fess| to be restarted before a change takes effect. Values
   read from ``fess_config.properties`` are cached in the JVM, so editing the file while |Fess| is
   running has no effect.

   For reference, ``rank.fusion.window_size`` is read once at startup and ``rank.fusion.threads``
   is read when the thread pool is created. The thread pool is created when a searcher other than
   ``default`` (such as the semantic searcher) is registered, so if semantic search is disabled,
   no thread pool is created at all.

JVM System Properties
---------------------

The searchers to use are specified as a JVM system property. Add the following to
``fess.in.sh``::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Drank.fusion.searchers=default,semantic_chunk"

For ``fess.in.bat``, write it as follows::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Drank.fusion.searchers=default,semantic_chunk

This property behaves as follows:

- It is set as a JVM option, not in ``fess_config.properties``. Specify the key name
  ``rank.fusion.searchers`` exactly as-is. The prefixed forms that are common for other settings,
  ``-Dfess.config.`` and ``-Dfess.system.`` (for example ``-Dfess.config.rank.fusion.searchers``),
  are not recognized.
- Instead of a JVM option, you can also enter it on a single line, such as
  ``rank.fusion.searchers=default,semantic_chunk``, in the "System Property" field under
  System > General in the administration UI. Note that a value in that field is applied only when
  a system property of the same name is not already set. A ``-D`` option therefore takes
  precedence, and changing a value that has already been applied requires restarting |Fess|.
- ``default`` is the searcher that performs standard keyword search and is always available.
- A searcher's name is derived from its implementation class name by removing the trailing
  ``Searcher`` and decamelizing the remainder into lowercase snake_case
  (``SemanticChunkSearcher`` → ``semantic_chunk``). The core-integrated semantic searcher
  (:doc:`search-semantic`) is registered under the name ``semantic_chunk``.
- If this property is not specified, all registered searchers are used. If none of the specified names match a registered searcher, only the ``default`` searcher is used. If you use the core-integrated semantic searcher (:doc:`search-semantic`), you normally do not need to set this property at all.
- Result fusion is performed only when two or more searchers are available. When only one searcher is available, no fusion is performed and normal search results are returned.

.. warning::

   If you previously used the ``fess-webapp-semantic-search`` plugin from |Fess| 15.7 or earlier,
   you may have been told to set this property to
   ``-Drank.fusion.searchers=default,semantic``. That plugin registered its searcher under the
   name ``semantic``, which is a **different searcher** from the core-integrated searcher's name,
   ``semantic_chunk``, introduced in 15.9. If you carry that 15.7-era setting forward into 15.9
   as-is, the allowlist never includes ``semantic_chunk``, so the core-integrated semantic search
   (content chunking + vector search) **does not work at all** — |Fess| silently keeps returning
   ordinary keyword search results (a warning is logged at startup, but the per-request exclusion
   itself is only logged at DEBUG level). If your configuration specifies
   ``default,semantic``, either remove this setting or add ``semantic_chunk`` to it. See
   "Migrating from 15.7 or Earlier" in :doc:`search-semantic` for details.

.. _rank-fusion-engine:

Rank Fusion in the Search Engine
================================

Setting ``rank.fusion.engine.enabled=true`` has OpenSearch, rather than |Fess|, perform the fusion.
The searchers' queries are combined into a single search request (a ``hybrid`` query), and an
OpenSearch search pipeline normalizes and combines the scores. Because the fusion happens in one
request, the total hit count and the facet counts also describe the fused result set.

This requires the OpenSearch neural-search plugin. It is included in the standard OpenSearch
distribution and in the ``ghcr.io/codelibs/fess-opensearch`` image, but not in the minimal
distribution.

The settings go in ``fess_config.properties`` (a change requires a restart of |Fess|)::

    rank.fusion.engine.enabled=true
    rank.fusion.combination.technique=rrf
    rank.fusion.normalization.technique=min_max
    rank.fusion.combination.weights=
    rank.fusion.pagination_depth=200

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Property
     - Default
     - Description
   * - ``rank.fusion.engine.enabled``
     - ``false``
     - ``true`` has the search engine perform the fusion.
   * - ``rank.fusion.combination.technique``
     - ``rrf``
     - How the scores are combined: ``rrf``, ``arithmetic_mean``, ``geometric_mean`` or ``harmonic_mean``. For ``rrf``, ``rank.fusion.rank_constant`` is used as the constant ``k``, giving the same formula as when |Fess| performs the fusion.
   * - ``rank.fusion.normalization.technique``
     - ``min_max``
     - How the scores are normalized before they are combined: ``min_max``, ``l2`` or ``z_score``. Not used by ``rrf``.
   * - ``rank.fusion.combination.weights``
     - (empty)
     - Weight per searcher, as comma-separated ``name:weight`` pairs (for example ``default:0.7,semantic_chunk:0.3``). Each weight must be between ``0.0`` and ``1.0``, the weights must sum to ``1.0``, and every searcher taking part in the fusion must be named. Empty weights the searchers equally. A value that does not meet these rules is reported with an ERROR log, and that search is fused by |Fess|.
   * - ``rank.fusion.pagination_depth``
     - ``200``
     - How many results each searcher contributes to the fusion per shard. It bounds how deep a client can page and the set of documents that are fused.

.. note::

   ``z_score`` normalization can only be combined with ``arithmetic_mean``. This is a restriction of
   the neural-search plugin. If it is combined with ``geometric_mean`` or ``harmonic_mean``, |Fess|
   refuses the combination, writes an ERROR log naming both settings, and fuses that search itself.

In the following cases the search engine does not perform the fusion, and |Fess| fuses the results
instead.

- A search that includes advanced search parameters (``as.*``)
- A search that specifies a sort order, a geolocation search or a similar-document search. These
  skip semantic search altogether, so the results are keyword-only (see :doc:`search-semantic`).
- A page whose start position plus page size exceeds ``rank.fusion.pagination_depth`` (a DEBUG log
  is written for each such search). Fusion in |Fess| then applies the ``rank.fusion.window_size``
  boundary, so with the default settings the results are keyword-only.
- A ``rank.fusion.combination.weights`` value that does not meet the rules above
- ``z_score`` normalization combined with ``geometric_mean`` or ``harmonic_mean`` (an ERROR log
  names both settings)
- The search engine cannot run fused requests at all: it does not know the ``hybrid`` query or the
  search pipeline processor, for example because the neural-search plugin is missing or too old. A
  WARN log is written for each such search, and the next search asks the search engine again, so
  engine-side fusion resumes on its own once the plugin is installed or upgraded, without
  restarting |Fess|.

Any other failure of a fused request (an invalid query, a closed index, a shard failure, and so on)
is reported for that search only, as it would be without engine-side fusion, and the next search is
fused by the search engine again.

Keep the following in mind when the search engine performs the fusion.

- ``rank.fusion.timeout`` does not apply. The query embedding is computed synchronously before the
  search request is sent, so a slow or unresponsive embedding provider delays the search up to the
  provider's own timeout (for example ``content_chunker.embedding.ollama.timeout``).
- ``rank.fusion.window_size`` and ``rank.fusion.threads`` are used only when |Fess| performs the
  fusion.
- The ``k`` of the semantic searcher's knn query (the number of neighbors per shard) becomes the
  larger of ``content_chunker.search.knn.k`` and ``rank.fusion.pagination_depth``. A vector search
  returns neighbors even when their similarity is low, so without
  ``content_chunker.search.min_score`` the total hit count includes those vector hits, and on a
  small index it can cover most of the documents the user can see. Set
  ``content_chunker.search.min_score`` to narrow it (see :doc:`search-semantic`).
- The ``searcher`` field is added to the results as usual, but ``rf_score`` is not.

Integration with Hybrid Search
===============================

Rank Fusion is particularly effective for hybrid search, which combines keyword
search and semantic search. To use semantic search, configure the content chunking feature and
then set ``content_chunker.search.enabled=true``.

.. warning::

   The ``content_chunker.*`` settings, such as ``content_chunker.enabled`` and
   ``content_chunker.search.enabled``, are **system properties**, not ``fess_config.properties``
   settings. Write them in ``conf/system.properties``, or specify them as JVM options such as
   ``-Dfess.system.content_chunker.search.enabled=true``. Writing them in
   ``fess_config.properties`` has no effect. In addition, ``content_chunker.search.enabled`` is
   evaluated only at startup, so |Fess| must be restarted after you enable it.

See :doc:`search-semantic` for details.

Verifying Fusion Results
========================

You can check whether Rank Fusion is actually working by looking at the following two fields added
to the search results.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - ``searcher``
     - An array of the names of the searchers that retrieved the document (for example, ``["default", "semantic_chunk"]``). If both are present, the document was hit by both keyword search and semantic search.
   * - ``rf_score``
     - The fused score calculated by RRF. The field name can be changed with ``rank.fusion.score_field``.

Both values are added dynamically at search time and are not stored in the index.
They are also not included in the ``/api/v2/search`` response by default, so to see them, add the
following to ``fess_config.properties`` and restart |Fess|::

    query.additional.api.response.fields=rf_score,searcher

.. note::

   ``query.additional.api.response.fields`` adds entries to the allowlist of fields that may be
   included in the v2 search API response. Do not add access control fields such as ``role`` or
   ``virtual_host``, because doing so exposes access control information in search API responses.

Impact on Hit Counts
====================

When |Fess| performs Rank Fusion, the total hit count that is returned is not the count from the main
searcher (the ``default`` searcher registered first) as-is; it is adjusted as follows::

    total hits = total hits of the main searcher + adjustment

The adjustment is the number of documents among the top ``window_size ÷ 2`` fused results that
were not among the top ``window_size ÷ 2`` results of the main searcher. In other words, the count
increases by the number of documents that only semantic search found.
As a result, the same query can report a different hit count depending on whether hybrid search is
enabled.

Note that this adjustment is not applied when the total hit count of the main searcher is returned
as an approximate (lower-bound) value.
When the search engine performs the fusion, the total hit count is that of the fused result set
(see :ref:`rank-fusion-engine`).

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
- Use ``rank.fusion.window_size`` to limit the maximum number of results to fuse. The main searcher (the leading ``default`` searcher) retrieves up to ``window_size`` results, while each of the other searchers retrieves ``window_size ÷ number of searchers`` results (``number of searchers`` is the total including the main searcher, and the division is truncated).
- For example, with two searchers (``default`` and ``semantic_chunk``) and ``window_size=200``, the main searcher retrieves 200 results and the semantic searcher retrieves 100, so up to 300 documents are retained.

::

    # Window size for fusion
    rank.fusion.window_size=200

.. warning::

   ``rank.fusion.window_size`` cannot go below ``paging.search.page.max.size × 2``. When
   ``paging.search.page.max.size`` has its default value of ``100``, the lower bound is ``200``,
   which is exactly the default value of ``rank.fusion.window_size``. In other words, **in the
   default configuration you cannot set window_size to anything smaller than its default**. If you
   configure a smaller value, a WARN log is written at startup and the value is raised to ``200``.
   To lower it in practice, you must first lower ``paging.search.page.max.size``, but that also
   lowers the maximum number of results per page that clients can request.

Processing Time
---------------

- Response time increases because multiple searches are executed.
- Use ``rank.fusion.threads`` to set the number of threads for parallel execution.

::

    # Number of threads for parallel execution
    # (if 0 or less, availableProcessors × 3 / 2 + 1)
    rank.fusion.threads=-1

.. note::

   When |Fess| performs the fusion, searchers other than the main one are waited for up to
   ``rank.fusion.timeout`` milliseconds (default ``10000``). A searcher that has not answered by
   then is left out of that search, and the results are flagged as partial (timed out). The main
   searcher is always waited for. ``0`` or less waits without a limit. This setting does not apply
   when the search engine performs the fusion (see :ref:`rank-fusion-engine`).

Behavior When a Searcher Fails
==============================

If a searcher fails with an exception, its results are treated as empty, a WARN log is written,
and fusion continues with the results of the remaining searchers. The search request itself does
not fail.

Query syntax errors (``InvalidQueryException``) and paging limit violations
(``ResultOffsetExceededException``) are the exceptions to this rule: they are returned as errors
as-is. In addition, on deep pages where fusion is not performed (where ``start position × 2`` is
greater than or equal to ``rank.fusion.window_size``), an exception raised by the main searcher is
returned as a search request error as-is.

The semantic searcher returns empty results when it cannot connect to the embedding provider or
when embedding processing fails. This does not cause an error either; the response contains
keyword search results only.

Troubleshooting
===============

Search Results Differ from Expectations
----------------------------------------

**Symptom**: Results after Rank Fusion differ from expectations

**Checks**:

1. Check the ``searcher`` field (see "Verifying Fusion Results"). If every document has only
   ``["default"]``, the semantic searcher is not returning any results.
2. Check whether semantic search is being skipped. The semantic searcher returns no results, so
   only keyword search results are used, for queries that contain search syntax such as phrases or
   wildcards, as well as for sorted searches, geo searches, and similar-document searches. See
   :doc:`search-semantic` for details on the skip conditions.
3. Verify the results of each search type individually
4. Adjust the ``rank.fusion.rank_constant`` value
5. On deep pages (where ``start position × 2`` is greater than or equal to
   ``rank.fusion.window_size``, which by default means from the 101st result onward), fusion is
   not performed and only the main searcher is used. If you want fused results on more pages,
   increase ``rank.fusion.window_size``. When the search engine performs the fusion, a page whose
   start position plus page size exceeds ``rank.fusion.pagination_depth`` is fused by |Fess|
   instead, so increase ``rank.fusion.pagination_depth`` as well.

Slow Search
-----------

**Symptom**: Search becomes slow when Rank Fusion is enabled

**Solutions**:

1. Adjust ``rank.fusion.threads``::

       rank.fusion.threads=4

2. Reduce ``rank.fusion.window_size``. Because it cannot go below its lower bound
   (``paging.search.page.max.size × 2``), in the default configuration you have to set the
   following two properties together::

       paging.search.page.max.size=50
       rank.fusion.window_size=100

   Note that this also lowers the maximum number of results that can be requested per page. A
   restart is required after changing these settings.

Out of Memory
-------------

**Symptom**: OutOfMemoryError occurs

**Solutions**:

1. Reduce ``rank.fusion.window_size`` using the same procedure as in "Slow Search"
2. Increase the JVM heap size

Reference
=========

- :doc:`search-semantic` - Semantic Search (Content Chunking) Settings
- :doc:`scripting-overview` - Scripting Overview
- :doc:`search-advanced` - Advanced Search Settings
- :doc:`llm-overview` - LLM Integration Guide (Semantic Search)
