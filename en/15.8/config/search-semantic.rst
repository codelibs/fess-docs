=====================================================
Semantic Search (Content Chunking + Vector Search)
=====================================================

Overview
========

In |Fess| 15.8, the **content chunking feature** — which splits document bodies into chunks and
generates and stores an embedding vector for each chunk — has been integrated into the core.
The generated vectors are used for two purposes:

- **Semantic search**: a hybrid search that combines keyword (BM25) search and vector search via
  Rank Fusion. Documents that are semantically close to the query can match even without exact
  keyword overlap.
- **AI search mode (RAG)**: when generating an answer, only the chunks that are semantically
  closest to the question are selected as the LLM's context, improving answer quality and token
  efficiency.

All of this is disabled by default. Unless you enable it, |Fess| continues to operate exactly as
before, using keyword search only. If you are upgrading |Fess| from 15.7 or earlier, or if you
were using the ``fess-webapp-semantic-search`` plugin, see :ref:`semantic-search-migration`.

Processing Flow
----------------

1. The crawler indexes documents as usual (no chunks exist at this point).
2. The scheduler job **Content Chunk Vector Indexer** finds unprocessed documents, splits their
   bodies (the ``content`` field) into chunks, generates embedding vectors, and stores them in the
   ``content_chunk_vector`` field. At this point the ``content`` field itself is also rewritten
   into an array of those chunks (``content_length`` keeps its original value).
3. The outcome of that processing is recorded in the ``content_chunk_status`` field (described
   below).
4. When ``content_chunker.search.enabled=true``, the semantic searcher participates in Rank
   Fusion at search time.

Prerequisites
=============

- **OpenSearch with the k-NN plugin**: In |Fess| 15.8, the mapping for the search index
  (``fess.search``) always includes the ``content_chunk_vector`` field (a ``nested`` field whose
  ``vector`` sub-field is the ``knn_vector`` type used for ANN), and the index settings always
  include ``index.knn: true``, regardless of whether the content chunking feature is enabled. As a
  result, if OpenSearch does not have the k-NN plugin installed, creating a new index fails
  outright and |Fess| cannot start.

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Configuration
       - k-NN Plugin Support
     * - Embedded OpenSearch (``bin/fess``, or the TAR.GZ/ZIP packages with
         ``SEARCH_ENGINE_HTTP_URL`` left unset — the default)
       - Ships with the k-NN plugin. It does not include the JNI native libraries, however, so
         the only supported ANN engine is ``lucene``. ``content_chunker.search.knn.engine`` also
         accepts ``faiss`` as a value, and setting it here still creates the mapping successfully
         — but **documents are then silently lost on every write, and searches return zero
         hits**. (|Fess| logs a warning at startup when it is started with this combination.)
     * - Docker (``ghcr.io/codelibs/fess-opensearch``), the RPM/DEB packages (which always connect
         to a separately installed external OpenSearch), or another external OpenSearch (standard
         distribution)
       - Fully supported, including ``faiss``.
     * - The **minimal distribution** of an external OpenSearch
       - **Not supported.** It does not include the k-NN plugin, so creating a new index fails.

  ``nmslib`` is never an accepted value for ``content_chunker.search.knn.engine``, on any of the
  configurations above: ``content_chunk_vector`` is a ``nested`` field, and the k-NN plugin only
  supports nested fields for the ``lucene``/``faiss`` engines (``nmslib`` is also deprecated and
  restricted starting with OpenSearch 3.0). Setting it falls back to ``lucene`` with a warning; see
  Configuration Reference below for the other ANN settings' accepted values.

- **OpenSearch version for an external cluster**: the shipped ``fess.search`` index settings always
  send ``index.knn`` and ``knn.derived_source.enabled`` (in ``fess_indices/fess.json`` and its
  AWS/cloud variants). The latter is a relatively recent k-NN plugin setting, and an older
  OpenSearch that does not recognize it fails to create the index regardless of whether the k-NN
  plugin itself is installed. See :doc:`../install/prerequisites` for the OpenSearch versions
  |Fess| 15.8 supports.

- **Embedding provider**: use one of the following.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Configuration Value
     - Provided By
     - Description
   * - ``opensearch``
     - |Fess| core (built in)
     - Uses an embedding model deployed to OpenSearch ML Commons. No additional plugin required.
       Default setting.
   * - ``ollama``
     - ``fess-llm-ollama`` plugin
     - Uses an Ollama embedding model (e.g. ``nomic-embed-text``).
   * - ``openai``
     - ``fess-llm-openai`` plugin
     - Uses the OpenAI embeddings API.
   * - ``gemini``
     - ``fess-llm-gemini`` plugin
     - Uses the Google Gemini embeddings API.
   * - ``none``
     - |Fess| core (built in)
     - Splits documents into chunks only; no vectors are generated (chunk-only mode).

Configuration Reference
========================

All ``content_chunker.*`` settings live in a single channel: **system properties**
(``system.properties``). Set them in ``app/WEB-INF/conf/system.properties``
(``/etc/fess/system.properties`` on the RPM/DEB packages, ``/opt/fess/system.properties`` on
Docker), or supply an initial value with the ``-Dfess.system.<key>`` startup option. Values are
reloaded at runtime, so most settings take effect immediately after you change them. The one
exception is enabling
``content_chunker.search.enabled`` (``false`` → ``true``): because the semantic searcher is only
registered at startup, **this change requires a restart to take effect**.

.. note::

   The ``content_chunker.*`` keys are also listed as comments in ``fess_config.properties``, but
   they are only read from the ``system.properties`` channel. Writing them in
   ``fess_config.properties`` or passing them as ``-Dfess.config.<key>`` has no effect, so always
   set them in ``system.properties``. Note also that the admin **System Info > Config Info** screen
   is a **read-only** view of the current values — you cannot set ``content_chunker.*`` from it.

system.properties Settings
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Property
     - Default
     - Description
   * - ``content_chunker.enabled``
     - ``false``
     - Master switch for the entire content chunking feature
   * - ``content_chunker.chunker.name``
     - ``length``
     - Chunking method
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - Target number of characters per chunk. With boundary-aware splitting enabled (the
       default) this is a target rather than a hard limit: a chunk may be up to
       ``boundary.lookback_percent`` of it shorter, and up to ``max(lookahead, 32)`` characters
       longer -- 640 to 840 characters at the defaults. Leave that margin against the embedding
       model's token limit
   * - ``content_chunker.length.overlap``
     - ``0``
     - Number of characters to overlap between chunks. The restart point is snapped to a
       boundary as well, and snapping can only move it earlier, so the effective overlap is
       between this value and twice this value
   * - ``content_chunker.length.boundary.enabled``
     - ``true``
     - Move each cut to a sensible text boundary instead of cutting at exactly
       ``chunk_size`` characters. Candidates are tiered and the nearest candidate of the highest
       tier present wins: a line break or sentence end, otherwise a clause separator or space,
       otherwise a writing-system change. Set to ``false`` for the previous fixed-length
       behaviour
   * - ``content_chunker.length.boundary.lookback_percent``
     - ``20``
     - How far before the ideal cut a boundary may be searched, as a percentage of
       ``chunk_size`` (0-50)
   * - ``content_chunker.length.boundary.lookahead_percent``
     - ``5``
     - How far after the ideal cut a sentence end or line break may be searched, as a
       percentage of ``chunk_size`` (0-25). Used only when nothing was found behind the cut
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - Maximum number of chunks per document. Documents that exceed this are marked ``skipped``
       and receive no embeddings. Because boundary-aware splitting makes chunks shorter, a
       document yields roughly 3% to 25% more chunks than a fixed-length split, so a corpus of
       very large documents may need a higher value here
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - Embedding provider (``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``)
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - Dimension of the embedding vector. This value is used when the mapping is created, so it
       **must** match the dimension of the embedding model you use. There are two distinct read
       paths for this value, and they behave differently. When the index mapping is created, an
       unset, non-numeric, non-positive, or above-``16000`` value (``16000`` is the k-NN plugin's
       own maximum) falls back to ``768`` with a warning. The embedding process itself, by
       contrast, has no fallback: an unset, non-numeric, or non-positive value is an error there.
       A value above ``16000`` is not rejected at runtime, so only the mapping ends up at ``768``
       and you get a dimension mismatch
   * - ``content_chunker.job.concurrency``
     - ``2``
     - Number of parallel workers for the indexer job
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - Number of documents fetched and written per batch
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ (unlimited)
     - Maximum number of documents processed per job run. Any value of ``0`` or less is treated
       as unlimited
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - When set to ``true``, documents that ended the previous run with
       ``content_chunk_status=fail`` are included in the next run's processing target as well.
       There is no automatic retry or attempt-count tracking; the intended workflow is to fix the
       underlying cause, then temporarily enable this to retry
   * - ``content_chunker.chat.top_k``
     - ``3``
     - Number of chunks selected when AI search mode generates an answer
   * - ``content_chunker.search.enabled``
     - ``false``
     - Rank Fusion integration for semantic search (**enabling this requires a restart**)
   * - ``content_chunker.search.min_score``
     - (unset)
     - Minimum cosine similarity (0-1) required for a result to be included. No cutoff when unset.
       In ``ann`` mode, if ``search.knn.space_type`` is anything other than ``cosinesimil``, a
       cosine-based cutoff cannot be defined, so the cutoff is skipped with a warning
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - ANN index method. ``hnsw`` is currently the only accepted value; any other value falls back
       to ``hnsw`` with a warning (reflected in the mapping; changing it requires recreating the
       index)
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - ANN engine. Only ``lucene`` or ``faiss`` are accepted (see Prerequisites above); any other
       value falls back to ``lucene`` with a warning (reflected in the mapping; changing it
       requires recreating the index)
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - Distance space. Only ``cosinesimil``, ``innerproduct``, or ``l2`` are accepted; any other
       value falls back to ``cosinesimil`` with a warning (reflected in the mapping; changing it
       requires recreating the index)
   * - ``content_chunker.search.knn.k``
     - ``100``
     - Number of neighbors retrieved per ANN query (automatically enlarged for deep paging)
   * - ``content_chunker.search.knn.param.ef_search``
     - (unset)
     - The ``ef_search`` parameter for ANN queries

.. note::
   Setting ``content_chunker.length.boundary.enabled`` to ``false``, or both percentages to
   ``0``, reproduces the previous fixed-length behaviour exactly. Changing any of these settings
   only affects documents chunked afterwards: a document already stored as a chunk array keeps
   its boundaries until it is re-crawled.

.. note::

   The HNSW ``m`` and ``ef_construction`` parameters are hard-coded in ``doc.json``
   (``m=16`` / ``ef_construction=100``) and cannot be changed through configuration.

Connection Settings for the opensearch Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connection settings for the built-in ``opensearch`` provider (OpenSearch ML Commons). These are
set in the same ``system.properties`` file as above.

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - Property
     - Default
     - Description
   * - ``content_chunker.embedding.opensearch.model.id``
     - (required)
     - ID of the model already deployed to ML Commons
   * - ``content_chunker.embedding.opensearch.api.url``
     - The search engine's address
     - ML Commons API endpoint. When unset, defaults to the search engine |Fess| is already using
       (e.g. ``http://localhost:9200``)
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - The search engine's credentials
     - When unset, falls back to the credentials used for the search engine connection — but
       only while ``api.url`` is left unconfigured (i.e. the target is the same cluster |Fess|
       already uses). Once ``api.url`` is set, there is no fallback.
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - Request timeout (ms)
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - Connection timeout (ms)
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - Number of retries for transient errors (429, 5xx, etc.)
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - Base retry backoff delay (ms)
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - Interval between provider availability checks (seconds)
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - (empty)
     - Prefix prepended to document/query text before embedding

.. warning::

   The contents of ``system.properties`` can be viewed on the admin **System Info > Config Info**
   screen, in the **App Properties** panel. ``content_chunker.embedding.opensearch.password`` is
   masked there as ``XXXXXXXX``, but ``username`` is shown as-is. Values supplied with
   ``-Dfess.system.<key>``, on the other hand, are shown **unmasked** in the **System Properties**
   panel of that same screen — so put credentials in ``system.properties`` rather than in startup
   options.

Other Providers (ollama / openai / gemini)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``ollama`` provider (``fess-llm-ollama`` plugin) uses the same style of settings under the
``content_chunker.embedding.ollama.`` prefix (``api.url`` defaults to ``http://localhost:11434``,
``model`` defaults to ``embeddinggemma``, and ``document.prefix`` / ``query.prefix`` default to
``title: none | text:`` / ``task: search result | query:`` respectively). If you use a model in
the ``nomic-embed-text`` family, set ``document.prefix`` / ``query.prefix`` explicitly to
``search_document:`` / ``search_query:``. These prefixes are concatenated with the text to be
embedded exactly as configured (surrounding whitespace is not trimmed), so the defaults above and
``search_document:`` / ``search_query:`` all **include one trailing space**. Remember the
separating space when you set a prefix yourself. The ``openai`` and ``gemini`` providers
are configured the same way, under the ``content_chunker.embedding.openai.`` and
``content_chunker.embedding.gemini.`` prefixes respectively. See each plugin's documentation for
the full list of settings.

Setup Procedure (opensearch Provider Example)
===============================================

This section walks through a configuration example using the built-in ``opensearch`` provider
(ML Commons).

1. Deploy the Embedding Model
-------------------------------

Register and deploy an embedding model to OpenSearch ML Commons. On a single-node cluster, you
must apply the following setting first.

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

Register and deploy the model (example: a 384-dimension sentence embedding model):

.. code-block:: bash

    # Register the model (get model_id from the response's task_id)
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # Check the task and obtain model_id (model_id is returned once state becomes COMPLETED)
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # Deploy
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # Check status: model_state should be DEPLOYED
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   A model that is still ``REGISTERED`` cannot be used. Be sure to deploy it and confirm that
   ``model_state`` becomes ``DEPLOYED``.

2. Configure |Fess|
----------------------

``app/WEB-INF/conf/system.properties`` (``/etc/fess/system.properties`` on the RPM/DEB packages,
``/opt/fess/system.properties`` on Docker; everything below goes in that same file)::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

If you also want to use semantic search, add the following as well::

    content_chunker.search.enabled=true

Restart |Fess| after making these changes.

3. Recreate the Index (When Enabling on an Existing Deployment)
-------------------------------------------------------------------

The mapping for the ``content_chunk_vector`` field — including the dimension and ANN method
settings you configured — is applied **at the moment the** ``fess.search`` **index is newly
created**.

- **New installations**: If you apply the settings above to ``system.properties`` before starting
  |Fess| for the first time, the correct mapping is applied automatically when the index is first
  created, so this step is unnecessary.
- **If an index already exists** (that is, if you have started |Fess| at least once before): the
  running index does not pick up the new mapping automatically, and an existing mapping cannot be
  amended after the fact. Recreate the index as follows:

  Open **System Info > Maintenance**, and under **Re-indexing** run it with **Replace Aliases**
  enabled.

  You can then confirm that the recreated index has ``index.knn: true`` in its index settings and a
  ``content_chunk_vector`` mapping carrying your configured dimension and ANN method settings
  (``index.knn`` is an index setting while the ANN method settings live in the mapping — they are
  applied in two different places).

.. warning::

   Re-indexing runs as an asynchronous background operation, and the admin UI shows no completion
   notification. ``_cat/indices`` only shows that the new index exists (health, doc count, and so
   on) — it does not show which index the aliases point to. Before moving on to the indexer job
   below, check ``_cat/aliases`` instead and confirm that both ``fess.search`` and ``fess.update``
   point to the new index; the |Fess| log only logs a warning on failure, so a quiet log is not
   proof of success, only the absence of a known failure. The old index (the physical index that
   the ``fess.search`` alias previously pointed to, named ``fess.<timestamp>``) is not deleted
   automatically; remove it manually once you no longer need it. While both indices exist, expect
   roughly double the usual index disk usage.

4. Enable the Indexer Job
----------------------------

Chunking and embedding generation are performed by the scheduler job **Content Chunk Vector
Indexer** (ID: ``content-chunk-vector-indexer``; disabled by default; scheduled ``0 13 * * *``).

Enable this job under **System > Scheduler**, then run it once with **Start Now**. After that,
unprocessed documents are picked up on the configured schedule (daily at 13:00 by default),
independently of when crawling finishes. This job is not chained to the crawler job, so if you want
documents processed right after a crawl, set its schedule to a time later than the crawler job is
expected to finish.

.. note::

   In a multi-node deployment, we recommend pinning this job to run on exactly one node. Running
   it on every node at once does not break correctness, but every node processes and embeds the
   same documents redundantly, multiplying the load and cost on your embedding provider by the
   number of nodes.

   Pinning it requires **both** of the following settings — either one alone does not pin the job.

   1. **On the node you want to run the job**: set ``scheduler.target.name=<some identifier>`` in
      ``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` on the
      RPM/DEB packages, or via ``-Dfess.config.scheduler.target.name=<some identifier>``), then
      restart that node. (The default is empty; leave every other node at the default.)
   2. In the admin UI, under **System > Scheduler**, open the Content Chunk Vector Indexer job and
      change its **Target** field from ``all`` to the same identifier you set in step 1, then
      save.

   See :doc:`../admin/scheduler-guide` for what the **Target** field means. Setting
   ``scheduler.target.name`` alone does not pin the job if the **Target** field is left at
   ``all``: **it will not be pinned**. ``all`` is treated as a special value that always matches,
   so step 1 alone or step 2 alone is not enough — you must do both.

.. warning::

   Once the job is pinned, run **Start Now** **from the admin UI of the node you gave the
   identifier to in step 1**. If you press **Start Now** on any other node, the screen still
   reports "Started a job: ...", but the job does not actually run because the **Target** does not
   match — the only trace is an ``Ignoring job`` line logged at INFO level on that node.

5. Check Processing Status
-----------------------------

You can check the outcome for each document in its ``content_chunk_status`` field.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Meaning
   * - (field absent)
     - Not yet processed (will be picked up by the next job run). Documents also return to this
       state after being re-crawled
   * - ``done``
     - Chunking and vector generation completed
   * - ``chunked``
     - Chunking completed only (chunk-only mode). This is the state when
       ``embedding.name=none``, and also when the plugin for the provider named in
       ``embedding.name`` is not installed
   * - ``skipped``
     - Processing skipped (e.g. exceeded ``max_chunks_per_document``)
   * - ``fail``
     - Processing failed (check the logs)

You can check the distribution of statuses by querying the search engine directly::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

Thanks to the ``missing`` option, documents that have no ``content_chunk_status`` (that is,
unprocessed documents) are aggregated into a bucket keyed ``pending``.

How Semantic Search Behaves
==============================

Setting ``content_chunker.search.enabled=true`` registers the semantic searcher with Rank Fusion,
which then merges keyword search results with vector search results. (See :doc:`rank-fusion` for
how Rank Fusion works.)
Note that ``content_chunker.enabled`` is also consulted at search time: when
``content_chunker.enabled=false`` or ``content_chunker.embedding.name=none``, semantic search does
not run even though the searcher is registered. (This is evaluated per request, so no restart is
needed.)

.. warning::

   Because the semantic searcher is registered at startup, **enabling this requires a restart**.
   Disabling it (changing the value back to ``false``) is evaluated per request, so it takes
   effect immediately.

exact Mode and ann Mode
--------------------------

The search method is chosen automatically based on the state of the index.

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - Mode
     - Condition
     - Characteristics
   * - ``ann``
     - An index that has ``index.knn`` and ANN method settings
     - Approximate nearest-neighbor search using HNSW. Suited to large indexes
   * - ``exact``
     - Anything else (an index missing either ``index.knn`` or the ANN method settings, including
       the case where the index state cannot be determined)
     - Exact cosine-similarity computation against every vector. Suited to small-to-medium
       indexes

Any ``fess.search`` index newly created under |Fess| 15.8 always has ``index.knn`` and ANN method
settings, regardless of the value of ``content_chunker.search.enabled`` — so ``ann`` mode is
normally always used. ``exact`` mode is a fallback for older indexes created before this mechanism
existed. Because k-NN settings cannot be added to an existing index after the fact, switching an
``exact``-mode index to ``ann`` mode requires recreating the index (see
:ref:`semantic-search-migration`). Note that the result of this determination is cached for 60
seconds, so it can take up to 60 seconds after recreating an index for the change to take effect.

Score Cutoff
--------------

Setting ``content_chunker.search.min_score`` to a cosine similarity (0-1) excludes from semantic
search results any document whose best-matching chunk still falls short of that value. (A
document's score is the score of its best chunk, so the cutoff operates per document, not per
chunk.) Use it to rein in hit counts when queries with no vocabulary overlap are matching too
broadly::

    content_chunker.search.min_score=0.4

The configured value is interpreted as a cosine similarity in both ``exact`` and ``ann`` mode; it is
converted internally to each mode's score scale.

.. note::

   This cutoff is applied only when ``content_chunker.search.knn.space_type`` is ``cosinesimil``
   (the default). On an ``ann``-mode index that uses ``innerproduct`` or ``l2``, a cosine
   similarity cannot be defined, so the cutoff is skipped after logging a warning once.

Limitations
-------------

- **Semantic search is skipped for queries that contain search syntax**, and only keyword search
  runs. The check is performed on the query string **after** it has been assembled, and it trips
  whenever that string contains any of ``"`` ``(`` ``)`` ``:`` ``[`` ``]`` ``{`` ``}`` ``^`` ``~``
  ``*`` ``?`` ``\``, ``&&``, ``||``, a ``+`` or ``-`` at the start or immediately after
  whitespace, or the uppercase words ``AND`` / ``OR`` / ``NOT`` / ``TO``. As a result, the
  following operations are skipped too, even when the user typed no search syntax at all.

  - Specifying a label (``label:"..."`` is appended internally)
  - Specifying a sort order (``sort:...`` is appended internally)
  - Drilling down with a facet (``filetype:...`` and the like are appended internally)
  - Advanced search: phrase search, excluded terms, file type, site, and date range
  - A search term that has related queries configured (expanded internally to ``("A" OR "B")``)

  The ASCII ``?`` is on that list, so a natural-language question ending in an ASCII question mark
  — "what is ...?" — is skipped as well. (The full-width ``？`` is not affected.)
- It is also skipped when combined with geolocation search (a geo filter) or similar-document
  search.
- On deep result pages, Rank Fusion itself is disabled and you get keyword-only results. The
  boundary is determined by ``rank.fusion.window_size`` (default ``200``), which by default means
  everything from result 101 onward.
- If the embedding provider is unreachable or a search error occurs, |Fess| automatically falls
  back to keyword-only results (the search itself never fails as a result).
- Role- and virtual-host-based access control applies to semantic search results as well.

Integration with AI Search Mode
==================================

When AI search mode (:doc:`rag-chat`, ``rag.chat.enabled=true``) is enabled, for documents whose
``content_chunk_status`` is ``done``, answer generation computes the similarity against each chunk
and uses only the top ``content_chunker.chat.top_k`` most relevant chunks (default: ``3``) as the
LLM's context.

What is embedded here is not the user's own utterance but **the search query the LLM generated in
the intent-detection phase** (if a re-search occurs, the regenerated query is used instead). When
no search query is generated at all — as when the user asks for a summary of a document — no chunk
selection takes place.

As a result, even for long documents only the relevant portions are passed to the LLM, which can
improve answer accuracy and reduce token usage. For documents whose ``content_chunk_status`` is
``chunked`` (chunks exist but vectors do not), chunk selection is performed by keyword (highlight)
matching instead of a similarity computation. Documents that are ``skipped`` or ``fail``, and
unprocessed documents, still use the full body (or a highlighted excerpt) as before.

This behavior is independent of ``content_chunker.search.enabled``, but it does require
``content_chunker.enabled`` to be on. Note that the text formed by joining the selected chunks is
still truncated at ``rag.chat.content.fulltext.max.length`` (default ``3000``), so raising
``content_chunker.chat.top_k`` or ``content_chunker.length.chunk_size`` never sends more characters
than that limit to the LLM.

.. _semantic-search-migration:

Migrating from 15.7 or Earlier
=================================

If you are upgrading |Fess| from 15.7 or earlier, your situation falls into one of the four
patterns below, depending on how you currently use these features. Follow the instructions for
the pattern that applies to you.

New Installations
--------------------

No extra work is needed. If you want to use vector search, simply configure
``system.properties`` according to the *Configuration Reference* section on this page before
starting |Fess| for the first time; the correct mapping is applied automatically when the index is
first created. (See *Setup Procedure* above for the concrete steps.)

.. note::

   If you have started |Fess| even once before (that is, the index already exists), follow one of
   the *existing users* patterns below instead of this one.

Existing Users Who Do Not Want Vector Search
------------------------------------------------

No work is needed. ``content_chunker.enabled`` and ``content_chunker.search.enabled`` are both
``false`` by default, so your search results and existing index behavior are unchanged after the
upgrade. The new scheduler job **Content Chunk Vector Indexer** is registered automatically at
startup, but since it is disabled by default it never runs, and the semantic searcher is never
registered with Rank Fusion. (The job is registered on every startup, so if you delete it from the
admin UI it is recreated — still disabled — the next time |Fess| starts.)

.. note::

   Even if you never use vector search, **creating a new index** under |Fess| 15.8 or later
   (including re-indexing) applies a mapping containing ``content_chunk_vector`` (a ``knn_vector``
   type) together with ``index.knn: true``. On a deployment whose OpenSearch does not have the
   k-NN plugin installed, index creation fails at that point. See *Prerequisites* on this page for
   details.

Existing Users Who Want to Enable Vector Search
----------------------------------------------------

The running index does not pick up the new mapping automatically, so the following steps are
required.

1. Apply the settings to ``system.properties`` as described in *Configuration Reference* on this
   page (see *Setup Procedure* above for the concrete steps when using the opensearch provider).
2. Restart |Fess|.
3. In the admin UI, run **Re-indexing** under **System Info > Maintenance** with **Replace
   Aliases** enabled. This runs in the background with no completion notification.
   ``_cat/indices`` only shows that the new index exists, not whether the aliases have switched —
   check ``_cat/aliases`` instead and confirm ``fess.search``/``fess.update`` point to the new
   index (the |Fess| log only warns on failure, so silence is not proof of success). The old index
   is not deleted automatically (remove it manually once you no longer need it), and index disk
   usage roughly doubles until you do.
4. Only after confirming that the alias swap above has finished, enable and run the Content Chunk
   Vector Indexer job under **System > Scheduler** (you do not need to re-crawl: the job reads
   ``content`` from the existing index's ``_source`` to chunk and embed it).

.. note::

   If you also apply ``content_chunker.search.enabled=true`` in step 1, then between the restart in
   step 2 and the completion of step 4 every search embeds the query without that embedding
   affecting the results at all. With a metered provider such as ``openai`` or ``gemini``, apply
   ``content_chunker.search.enabled=true`` and restart only after step 4 has completed.

If You Were Using the fess-webapp-semantic-search Plugin
--------------------------------------------------------------

The ``fess-webapp-semantic-search`` plugin, which provided semantic search in |Fess| 15.7 and
earlier, has been folded into the core in 15.8 and is now **unnecessary (deprecated)**. In
addition to the steps in *Existing Users Who Want to Enable Vector Search* above, you also need to
do the following.

1. **Remove the plugin**: delete ``fess-webapp-semantic-search-*.jar`` from
   ``app/WEB-INF/plugin/`` (on Docker, exclude it from ``FESS_PLUGINS``).

2. **Remove the old settings**: delete every ``-Dfess.semantic_search.*`` startup option. Also,
   if you had specified ``-Drank.fusion.searchers=default,semantic`` for the old plugin, remove
   it. Leaving it in place excludes the new semantic searcher (``semantic_chunk``) from Rank
   Fusion and logs a warning at startup.

3. **Detach the old ingest pipeline**: if you had configured ``-Dfess.semantic_search.pipeline``,
   the old plugin embedded ``default_pipeline`` (an ingest pipeline for neural search) into the
   index settings when the index was created. **Removing the plugin does not remove the
   pipeline** — it stays attached to the index and keeps running — so detach it **before** you run
   the re-indexing described in *Existing Users Who Want to Enable Vector Search*. The new index
   produced by that re-indexing never carries the setting, so running the command afterwards
   achieves nothing. Use ``_cat/aliases`` to find the ``fess.<timestamp>`` index that
   ``fess.search`` points to, and target that concrete index name rather than the alias::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   Detaching it from the index settings leaves the ingest pipeline itself in place in the search
   engine. If you will not be using it any more, delete it as well::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<pipeline_name>"

4. **Add the new settings**: configure ``content_chunker.*`` in ``system.properties`` as
   described in *Configuration Reference* on this page. If you continue to use your existing ML
   Commons model, set ``content_chunker.embedding.name=opensearch`` and put its existing
   ``model_id`` in ``content_chunker.embedding.opensearch.model.id``.

5. **Recreate the index and run the job**: the vector field the old plugin stored
   (``content_vector`` in the default configuration) and the ``content_chunk_vector`` field the new
   core feature uses are different fields, so the old vectors cannot be used by the new feature.
   Re-indexing copies ``_source`` verbatim, however, so those old vectors *are* duplicated into the
   new index, where dynamic mapping keeps them consuming disk space. We recommend purging them
   **before** re-indexing (adjust the field name if you had changed it)::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   Then run **Re-indexing** under **System Info > Maintenance**, and enable and run the Content
   Chunk Vector Indexer job to regenerate the vectors.

Notes
=======

Changing the Embedding Model (Dimension)
--------------------------------------------

To switch to an embedding model with a different dimension, follow this order.

1. Delete the existing, old vectors. If vectors at the old dimension are still present when you
   re-index, the new mapping cannot accept them, and the affected documents are left uncopied to
   the new index while processing carries on. |Fess| only checks the HTTP status of the re-index,
   so the admin UI shows no error even though documents go missing::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      You may equally well target ``fess.update`` (the update alias that re-indexing reads from).
      Also note that this operation leaves the ``content`` field as an array of chunks. The next
      job run joins it back together and re-splits it, so if you have set
      ``content_chunker.length.overlap`` to something other than 0, the overlapping portions end up
      included twice when it is re-split. Re-crawl the affected documents if that concerns you.

2. Change ``content_chunker.embedding.dimension`` and the model setting for your provider.
3. Recreate the index as described in *3. Recreate the Index (When Enabling on an Existing
   Deployment)* under *Setup Procedure*, then re-run the indexer job.

Disk Usage
------------

Chunk vectors are retained in ``_source`` in addition to the search index structures, so each
document consumes extra disk space proportional to its number of chunks times the vector
dimension. If disk space becomes a concern, adjust ``content_chunker.length.chunk_size`` or
``content_chunker.max_chunks_per_document``.

chunk-only Mode
------------------

Setting ``content_chunker.embedding.name=none`` performs chunking only, without generating
embedding vectors (``content_chunk_status`` becomes ``chunked``). This lets you run chunking
ahead of time, before your embedding provider is ready; once you configure a provider later and
re-run the job, vectors are generated for the chunks already stored, without re-chunking them.

Memory Settings for Large Corpora
--------------------------------------

The indexer job's child JVM is started with ``jvm.chunk.options`` in ``fess_config.properties``
(JVM options that default to include ``-Xms128m -Xmx1g``). Because
``content_chunker.job.max_documents_per_run`` defaults to unlimited, a single run holds every
pending document ID in memory. Document IDs are SHA-512 digests (128 characters) and occupy roughly
200 bytes each on the heap, and chunk processing itself uses another 200-250MB — so for **corpora
beyond 1 to 2 million documents**, either raise the ``-Xmx`` value in ``jvm.chunk.options`` or set
a finite ``content_chunker.job.max_documents_per_run`` to split the work across several runs.
Override ``jvm.chunk.options`` in ``app/WEB-INF/classes/fess_config.properties``
(``/etc/fess/fess_config.properties`` on the RPM/DEB packages); see :doc:`setup-memory` for how JVM
options work.

The same unlimited default has a cost consequence with a metered embedding provider (``openai``,
``gemini``): the first indexer run embeds the entire existing corpus in one pass and bills for it
all at once. Set a finite ``content_chunker.job.max_documents_per_run`` to spread that cost across
multiple runs instead.

References
============

- :doc:`rank-fusion` - Rank Fusion (hybrid search) configuration
- :doc:`rag-chat` - AI search mode configuration
- :doc:`llm-overview` - LLM integration overview
- :doc:`llm-ollama` - Ollama configuration
- :doc:`setup-memory` - JVM memory settings
- :doc:`../install/upgrade` - Upgrade procedure
