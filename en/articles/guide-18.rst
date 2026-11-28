=================================================
Finding Documents by Meaning with Semantic Search
=================================================

Introduction
============

When a user searches for "I want my pay sent to a different bank" but the internal policy is titled "Procedure for changing your payroll account", keyword search will not find it.
In Fess 15.9, "semantic search", which converts text into vectors that represent meaning and searches with them, is built into the core and works without a plugin (depending on where the embedding model runs, you add a plugin).

By following the steps in this article, you will be able to:

- Tell when semantic search helps and when keyword search is enough
- Run an environment with semantic search already configured, right away, using Docker
- Configure ``content_chunker.*`` on an existing Fess and generate vectors with the indexer job
- Check with the ``searcher`` field whether a search result was found by vector search

Configuring AI search mode (RAG) is covered in :doc:`guide-19`.

When Semantic Search Helps
==========================

Semantic search in Fess does not replace keyword search (BM25).
It works as a "hybrid search": it runs both keyword search and vector search, and merges the results into a single ranking with Rank Fusion (RRF).

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Semantic search helps
     - Keyword search is enough
   * - Users and documents use different words ("bank for my pay" vs. "payroll account", "working from home" vs. "telework")
     - Searching for the exact string in the document, such as product model numbers, error codes, or people's names
   * - Asking a question in a sentence ("How do I request a new PC")
     - There are few paraphrase combinations, and they all fit in a synonym dictionary
   * - Searching in English to find documents in another language, such as Japanese (requires a multilingual embedding model)
     - Using search syntax such as phrases or wildcards (in this case, vector search itself is not run)

If the paraphrase combinations are limited, trying a synonym dictionary first is simpler.
For how to register synonyms based on zero-hit terms in the search log, see :doc:`guide-08`.

How It Works Inside Fess
========================

#. The crawler registers documents in the index as usual. At this point there are no vectors.
#. The scheduler job ``Content Chunk Vector Indexer`` finds unprocessed documents, splits the body text into chunks (fragments), creates an embedding vector for each chunk, and stores them in the ``content_chunk_vector`` field. The result is recorded in the ``content_chunk_status`` field.
#. When ``content_chunker.search.enabled=true``, every search runs keyword search (searcher name ``default``) and vector search (searcher name ``semantic_chunk``), and fuses them with RRF.

This job is disabled by default and is not linked to crawling.
Note that adding the settings alone does not create vectors, and search results remain keyword search only.

Prerequisites
=============

**OpenSearch with the k-NN plugin**

The search index created by Fess 15.9 contains a field of type ``knn_vector``, whether or not you use semantic search.
The Docker image ``ghcr.io/codelibs/fess-opensearch`` and the standard OpenSearch distribution include the k-NN plugin.
With the minimal distribution, which does not include the k-NN plugin, the index cannot be created and Fess does not start.

**Embedding provider**

Select where the model that converts text into vectors runs with ``content_chunker.embedding.name``.

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - Value
     - Requirement
     - Description
   * - ``opensearch`` (default)
     - No additional plugin
     - Uses a model deployed to OpenSearch ML Commons
   * - ``ollama``
     - Plugin ``fess-llm-ollama``
     - Uses an Ollama embedding model (default model: ``embeddinggemma``)
   * - ``openai``
     - Plugin ``fess-llm-openai``
     - Uses the OpenAI embeddings API (default model: ``text-embedding-3-small``)
   * - ``gemini``
     - Plugin ``fess-llm-gemini``
     - Uses the Google Gemini embeddings API
   * - ``bedrock``
     - Plugin ``fess-llm-bedrock``
     - Uses an Amazon Bedrock embedding model

Install the plugin with the same minor version as Fess (15.9.x), and restart Fess after installing it.
OpenAI, Gemini, and Bedrock are pay-as-you-go, so the first job run incurs the charges for all existing documents at once.

The Quickest Way: Try It with docker-semanticsearch
===================================================

The docker-semanticsearch repository starts Fess 15.9 with semantic search already configured, using Docker Compose.
It automatically deploys a multilingual embedding model (``paraphrase-multilingual-MiniLM-L12-v2``, 384 dimensions) to OpenSearch ML Commons, and even enables the indexer job.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh`` fetches the search page theme ``semanticlens`` from the ``fess-themes`` repository.
The theme on ``main``, the default source in ``v15.9.0``, is for Fess 15.10 and later (``minFessVersion: 15.10``), so ``FESS_THEMES_REF`` specifies the ``15.9.x`` branch, which has the theme for 15.9.

The first startup takes a few minutes to download the model (about 490MB).
It is ready when ``docker compose ps -a`` shows ``fess01`` as healthy and ``init-semantic`` and ``init-fess-chunk`` as ``Exited (0)``.

After that, as with a regular Fess, create a crawl configuration in the admin console (``http://localhost:8080/admin``) and run the crawl.
In this setup, the indexer job runs every hour.
To create vectors right away, open ``Content Chunk Vector Indexer`` in [System] > [Scheduler] and click [Start Now].

In addition to the settings explained later in this article, this setup uses the following values:

- Fusion is performed on the OpenSearch side (``rank.fusion.engine.enabled=true``)
- The chunk length is 250 characters (because the model's input limit is 128 tokens)
- A similarity floor of ``content_chunker.search.min_score=0.5``
- The theme ``semanticlens``, which shows for each search result whether it was found by keyword search, semantic search, or both

For how to change these values, see the Configuration section of the repository README.

Enabling Semantic Search on an Existing Fess
============================================

Here, the steps are shown with Ollama's ``embeddinggemma`` (768 dimensions, multilingual) as an example.
To use the built-in ``opensearch`` provider, instead of Steps 1 and 2, deploy a model to ML Commons and set ``content_chunker.embedding.name=opensearch`` and ``content_chunker.embedding.opensearch.model.id``.
The procedure is in "Setup Procedure (opensearch Provider Example)" of `Semantic Search <https://fess.codelibs.org/stable/config/search-semantic.html>`__.

Step 1: Install the Plugin
--------------------------

In [System] > [Plugin] > [Install], select version 15.9.x of ``fess-llm-ollama``, install it, and restart Fess.
With Docker, specify ``FESS_PLUGINS=fess-llm-ollama:15.9.0`` for ``fess01`` in ``compose.yaml``.

Step 2: Prepare the Embedding Model
-----------------------------------

Pull the model on the server that runs Ollama.

::

    $ ollama pull embeddinggemma

Step 3: Write the Settings in system.properties
-----------------------------------------------

The ``content_chunker.*`` settings are read only from ``system.properties``.
They are ignored if written in ``fess_config.properties`` or with ``-Dfess.config.``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Installation type
     - Where to write
   * - ZIP
     - ``app/WEB-INF/conf/system.properties``
   * - RPM/DEB
     - ``/etc/fess/system.properties``
   * - Docker (docker-fess)
     - Specify each as ``-Dfess.system.<key>=<value>`` in ``FESS_JAVA_OPTS`` in ``compose.yaml``

``/opt/fess/system.properties`` inside the Docker container is also read, but ``fess01`` in docker-fess has no volume, so the file disappears with ``docker compose down``.

Write the following:

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url`` is the address of Ollama as seen from Fess.
If Fess runs in Docker, ``localhost`` refers to the container itself, so change it to an address reachable from the container.

``content_chunker.embedding.dimension`` must match the output dimension of the model.
This value is written into the mapping when the index is created and cannot be changed afterward.

Step 4: Restart Fess
--------------------

Changing ``content_chunker.search.enabled`` to ``true`` does not take effect until you restart (the other ``content_chunker.*`` settings are re-read while Fess is running).

Step 5: Rebuild the Existing Index
----------------------------------

In an environment where Fess has been started even once, the mapping with the new dimension has not been applied to the index.
In [System Info] > [Maintenance], under "Re-indexing", enable "Replace Aliases" and click [Start].
This is not needed in a new environment where you completed Step 3 before the first startup.

Re-indexing runs asynchronously in the background, and the screen does not show when it finishes.
Before going on to the next step, confirm that both the ``fess.search`` and ``fess.update`` aliases point to the new index (``fess.<timestamp>``).

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

The old index is not deleted automatically, so delete it manually once you have confirmed this.
You do not need to crawl again.
The indexer job creates vectors from the stored body text.

Step 6: Enable and Run the Indexer Job
--------------------------------------

#. Open ``Content Chunk Vector Indexer`` in [System] > [Scheduler] and click [Edit].
#. Check "Enabled" for "Status", change the schedule if needed, and click [Update]. The default schedule is ``0 13 * * *`` (every day at 13:00).
#. Back on the details screen, [Start Now] is displayed; click it to run the job once.

The job is not linked to crawling, so crawled documents can be found by keyword right away, but they become targets of vector search only after this job runs next.
Set the schedule to a time after your crawl jobs finish.

Checking That It Works
======================

Checking That Vectors Were Created
----------------------------------

Have OpenSearch aggregate the processing result of each document.

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Meaning
   * - ``pending``
     - Unprocessed (processed at the next job run). Recrawled documents also return to this state
   * - ``done``
     - Chunking and vector generation are complete
   * - ``chunked``
     - Chunking only. Documents are also in this state when the provider's plugin is not installed
   * - ``skipped``
     - The body text is empty, or the number of chunks exceeded the limit (default 1000)
   * - ``fail``
     - Failed. Check the cause in the log file ``fess-chunk.log``

If ``pending`` decreases and ``done`` increases each time the job runs, things are going well.

Checking Whether a Result Was Found by Vector Search
----------------------------------------------------

The ``searcher`` field of a search result contains the names of the searchers that found the document.
By default it is not included in the search API response, so add the following line to ``fess_config.properties`` and restart (with Docker, ``-Dfess.config.query.additional.api.response.fields=searcher``).

::

    query.additional.api.response.fields=searcher

Search with a paraphrase whose keywords do not match the document.
If you have a document that explains the "Procedure for changing your payroll account", search as follows:

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=I want my pay sent to a different bank" \
      | jq '.response.data[] | {title, searcher}'

A result whose ``searcher`` is ``["semantic_chunk"]`` was found only by vector search, and ``["default", "semantic_chunk"]`` means it was found by both.
If every result has only ``["default"]``, vector search is not returning results.
Check the next section.

Common Pitfalls
===============

**rank.fusion.searchers from the old plugin era is still set**

With the ``fess-webapp-semantic-search`` plugin for 15.7 and earlier, you specified ``-Drank.fusion.searchers=default,semantic``.
In 15.9 the searcher name is ``semantic_chunk``, so if this setting remains, semantic search is not run and only keyword search results are returned.
At startup, the WARN log ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'`` is output.
Check both the JVM options and the "System Property" field in [System] > [General], and remove this setting (if it is not specified, all searchers are used).
For how to migrate from the old plugin, see "Migrating from 15.7 or Earlier" in `Semantic Search <https://fess.codelibs.org/stable/config/search-semantic.html>`__.

**Vector search is not run for queries that contain search syntax**

The following queries are handled by keyword search only:

- Phrases (``"..."``), wildcards, fuzzy search, and ranges
- Sentences that end with an ASCII ``?`` (e.g. "What is ...?"). The full-width "？" used in Japanese and Chinese text does not count
- Exclusions (``-word``, ``NOT word``) and boosts (``word^2``)
- Searches that specify a sort order

Narrowing with ``label:``, ``site:``, or facets is fine, because it is also applied to vector search as a filter.

**The dimension does not match, or the index was created without setting it**

If the index is created without setting ``content_chunker.embedding.dimension``, the mapping becomes 768 dimensions, and the job marks documents as ``fail``.
If the model's dimension is not 768, set the correct value and redo the re-indexing in Step 5.
``fail`` and ``skipped`` documents are not reprocessed when the job is rerun.
After fixing the cause, temporarily set ``content_chunker.job.retry_failed=true`` and run the job.

**You changed the embedding model**

The stored vectors were created with the old model, so changing only the model breaks search accuracy (no error appears even if the dimension is the same).
The procedure for deleting ``content_chunk_vector`` and ``content_chunk_status`` and rerunning the job is in "Notes" of the reference.

**Loosely related documents rank high**

Vector search returns documents in order of closeness, even those with low similarity.
Setting a cosine similarity floor (0 to 1) in ``content_chunker.search.min_score`` excludes documents that do not reach it.
The right value depends on the model and the documents, so adjust it while searching with both terms that previously had zero hits and unrelated terms.

**Results change character in the latter part of page 2 and beyond**

In the default setup, where fusion is done on the Fess side, only the top 200 results of each searcher (``rank.fusion.window_size``) are fused, and results from the 101st onward are keyword search results only.
The hit count also increases by the number of documents found only by vector search.
For how fusion works and the tuning options (``rank.fusion.rank_constant``, fusion on the OpenSearch side), see `Hybrid Search and Rank Fusion <https://fess.codelibs.org/stable/config/rank-fusion.html>`__.

Relationship to AI Search Mode and Multimodal Search
====================================================

AI search mode (RAG) can be used without enabling semantic search.
For documents whose vectors have been created with ``content_chunker.enabled=true``, the body text used for the answer is narrowed down to the chunks closest to the question, so the relevant parts of even long documents can be passed to the LLM.
For configuring AI search mode, see :doc:`guide-19`.

Multimodal search (``fess-webapp-multimodal``), which searches images and text together, cannot be used at the same time as the text semantic search in this article on the same Fess.
For details, see :doc:`guide-21`.

What to Read Next
=================

- Improve zero-hit terms from the search log with synonyms and Key Match: :doc:`guide-08`
- Have generative AI answer from internal documents: :doc:`guide-19`
- Search including images: :doc:`guide-21`
- Search from business systems through the search API: :doc:`guide-11`

References
==========

- `Semantic Search (Content Chunking + Vector Search) <https://fess.codelibs.org/stable/config/search-semantic.html>`__
- `Hybrid Search and Rank Fusion (Semantic + Keyword) <https://fess.codelibs.org/stable/config/rank-fusion.html>`__
- `Ollama Configuration (Local LLM / RAG) <https://fess.codelibs.org/stable/config/llm-ollama.html>`__
- `Scheduler <https://fess.codelibs.org/stable/admin/scheduler-guide.html>`__
- `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__
- `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch (GitHub) <https://github.com/codelibs/docker-semanticsearch>`__
