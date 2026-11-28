===============================================
Searching Images and Text Together (Multimodal)
===============================================

Introduction
============

File servers and internal sites hold large numbers of images, such as product photos and on-site photos, that have no clue to their content other than their file names.
With keyword search, you can only find images by words contained in their file names or metadata.

With the multimodal search plugin ``fess-webapp-multimodal``, you can search with words such as "mountain sunset" or "dog" and find images whose content is close to them.
In this article, we do the following with Fess 15.9.

- Start the ``docker-multimodalsearch`` Docker environment for evaluation at its 15.9 version, crawl images, and search them
- Confirm from the search API response that images were found by vector search
- Go over the settings needed to add it to an existing Fess, and the points where people tend to stumble

What It Can and Cannot Do
=========================

First, let us sort out the scope of ``fess-webapp-multimodal`` in 15.9.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Behavior in 15.9
   * - Search direction
     - Only text-to-image search. There is no feature for uploading an image to find similar images
   * - Images that are vectorized
     - Only files whose MIME type is ``image/gif``, ``image/jpeg`` or ``image/png``. BMP and TIFF are not vectorized
   * - Images inside PDF or Office documents
     - Not vectorized. To search for text inside images, use OCR (a separate feature)
   * - Documents other than images
     - Searched by keyword search (BM25) as usual. Images and text documents appear mixed together in the search results
   * - Non-English queries (such as Japanese)
     - Use a multilingual CLIP model. The default model of ``docker-multimodalsearch`` is a multilingual model that its README describes as supporting Japanese queries
   * - Semantic search on text
     - Cannot be used in the same Fess (see below)

For OCR, see `OCR Configuration <https://fess.codelibs.org/stable/config/crawler-ocr.html>`__.

How It Works
============

CLIP is a model that converts text and images into the same vector space.
The vector of the text "dog" is placed near the vectors of images showing a dog, so images can be searched by how close the vectors are to each other.

Since Fess 15.8, storing and searching vectors is handled by Fess itself.
The plugin only adds the part that talks to the CLIP server.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Timing
     - Processing
   * - At crawl time
     - GIF/JPEG/PNG images are sent to the CLIP server, converted into vectors, and written to the core vector field ``content_chunk_vector``
   * - At search time
     - The query is converted into a vector by the CLIP server, and nearby images are searched for. This search runs in parallel with the keyword search, and the two are merged into one result by Rank Fusion
   * - Results
     - Documents found by vector search have ``multi_modal`` in the ``searcher`` field. Documents found by keyword search have ``default``

For how Rank Fusion works, see `Hybrid Search and Rank Fusion (Semantic + Keyword) <https://fess.codelibs.org/stable/config/rank-fusion.html>`__.

Trying It with docker-multimodalsearch
======================================

``docker-multimodalsearch`` is a Docker Compose environment that bundles the containers and settings needed so that you can try multimodal search right away.
At the ``v15.9.0`` tag, the following services start.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Service
     - Role
   * - ``fess01``
     - Fess itself. The image is ``ghcr.io/codelibs/fess:15.9.0-noble``, and it installs the plugin ``fess-webapp-multimodal:15.9.0`` at startup. The search page uses the image-gallery theme ``mosaic``
   * - ``search01``
     - OpenSearch 3.9.0. Port 9200 is published only on the host's loopback (127.0.0.1)
   * - ``clip_server``
     - The CLIP server. The default model is the multilingual ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k`` (512 dimensions), and it runs on the CPU
   * - ``content``
     - nginx serving sample images at ``http://content/``. It is reachable only from the network between the containers
   * - ``init-fess-verify``
     - Runs once at startup, checks that the vector field of the index matches the settings, and exits

Prerequisites
-------------

- Docker (the ``docker compose`` command), Git, bash
- An Internet connection (used to fetch the images and the CLIP model; according to the README, the model is about 1.6 GB)
- On Linux, raise ``vm.max_map_count`` for OpenSearch (the same as in the preparation steps of :doc:`guide-02`)

Getting the 15.9 Version
------------------------

The default branch of ``docker-multimodalsearch`` follows the next version under development, so check out the ``v15.9.0`` tag.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

Open ``.env`` and change the source of the themes to the branch for 15.9.

::

    FESS_THEMES_REF=15.9.x

In ``v15.9.0``, ``.env.example`` still says ``FESS_THEMES_REF=main``, but the ``mosaic`` theme on ``main`` of ``fess-themes`` is now for Fess 15.10 and later (``minFessVersion: 15.10``).
The ``mosaic`` theme for 15.9 is on the ``15.9.x`` branch.

Leave ``FESS_VERSION=15.9.0`` and ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0`` in ``.env`` as they are.
The plugin version must match the Fess version.

Setting Up and Starting
-----------------------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh`` creates the data directories, fetches the theme, and prepares the thumbnail generation script.
The first ``docker compose up -d`` builds the ``clip_server`` image and downloads the CLIP model.
``fess01`` waits for ``clip_server`` to be ready before starting, so the first startup takes a few minutes.

Check the status with the following commands.

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

If ``fess01`` becomes ``(healthy)``, ``init-fess-verify`` ends with ``Exited (0)``, and the log contains the following line, the vector field has been created as configured.

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

Crawling the Sample Images
--------------------------

Fetch the sample images (animals, vehicles, food, nature, buildings), HTML, and PDF.

::

    $ bash bin/fetch-sample-images.sh

Then crawl from the admin console.

1. Log in to ``http://localhost:8080/admin/`` as ``admin`` / ``admin``, and set a new password if prompted
2. In [Crawler] > [Web], click [Create New], enter ``content`` in "Name" and ``http://content/`` in "URLs", and click [Create]
3. In [System] > [Scheduler], open "Default Crawler" and click [Start Now]
4. In [System Info] > [Crawling Info], wait for the crawl to finish

The image vectors are written during this crawl.
According to the README, the bundled samples register 43 documents (37 images, 5 HTML, 1 PDF).
Treat the count as a rough guide.

Searching
---------

Open ``http://localhost:8080/`` and search for ``dog`` or ``mountain sunset``, or for the same words in Japanese, ``犬`` or ``山の夕日``.
The default model is multilingual, so images are returned for both English and Japanese queries.

The ``mosaic`` theme shows the results as a gallery of thumbnails and marks each result with a "Keyword", "Visual" or "Blend" badge.
"Visual" means image similarity, and "Blend" means the result was found by both keyword and image similarity.

Thumbnails are generated by a background job after the crawl.
If some of them are not shown right after the crawl, wait a moment and reload.

To stop, run ``docker compose down``.
The data stays under ``./data``.

Checking the Behavior
=====================

Looking at ``searcher`` in the Search API
-----------------------------------------

Whether vector search was used can be checked with ``searcher`` in the search API response.
If you have ``jq``, run the following.

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=dog' | jq -c '.response.data[] | {url, searcher}'

The values of ``searcher`` mean the following.

- ``["multi_modal"]``: found by image similarity
- ``["default"]``: found by keyword search
- Contains both: found by both

If every result has only ``["default"]``, vector search was not run.
Check whether the search falls under one of the cases in "Searches Where Vector Search Does Not Run" below.

``searcher`` is not included in API responses by default.
``docker-multimodalsearch`` sets ``query.additional.api.response.fields=searcher`` of ``fess_config.properties`` as a startup option (``-Dfess.config.query.additional.api.response.fields=searcher``), so it is included in the response.
For details of the search API, see `Search API <https://fess.codelibs.org/stable/api/api-search.html>`__.

Checking Whether Vectors Were Written
-------------------------------------

If searches return no images at all, count the documents that have vectors in OpenSearch (port 9200 of this environment is usable only from the host).

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

If ``count`` is 0, no vectors were created at crawl time.
Check ``docker compose logs fess01`` and the crawler logs for the warning ``Failed to convert an image to a vector.``.

Searches Where Vector Search Does Not Run
-----------------------------------------

In the following cases, vector search is not run, and the results come from keyword search only.
No error is raised, so this is easy to miss.

- Searches that specify a sort order (the ``sort`` parameter). If you set "Default Sort Value" in [System] > [General], the ``mosaic`` theme sends that value as ``sort``, so ordinary searches fall under this case too
- Searches that use search syntax in the query: phrases (``"mountain sunset"``), wildcards (``dog*``), boosts (``dog^2``), exclusions (``-dog``), ``allintitle:``, ``allinurl:``
- Searches without a query that only have filter conditions such as labels
- Pages from the 101st result onward (when the start position is half of ``rank.fusion.window_size`` (default 200) or more)
- When the CLIP server cannot be reached (``fess.log`` shows a WARN such as ``Embedding provider is unavailable``)

On the other hand, if you use a field query such as ``filetype:jpg`` or a label filter together with the query, vector search still runs and is narrowed by that condition.

Adding It to an Existing Fess
=============================

To add it to an existing Fess 15.9 without using ``docker-multimodalsearch``, follow these steps.

1. Install the Plugin
---------------------

Install ``fess-webapp-multimodal`` 15.9.x in one of the following ways, then restart Fess.

- [System] > [Plugin] > [Install] in the admin console
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- For Docker, add ``fess-webapp-multimodal:15.9.0`` to the environment variable ``FESS_PLUGINS``

For details, see `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__.

2. Prepare a CLIP Server
------------------------

The plugin connects to an HTTP API in the same format as Jina's CLIP server.
It uses ``POST /post`` for vectorization and ``GET /health`` for the connection check.
If ``/health`` does not return 2xx, it keeps running with vector search disabled.
The endpoint is set with ``content_chunker.embedding.clip.api.url``, and its default value is ``http://localhost:51000``.

- ``docker/compose.yaml`` in the plugin's repository starts ``jinaai/clip-server``. Its configuration ``docker/clip_config.yaml`` does not specify a model, so the default model (ViT-B/32 with 512 dimensions, according to the README) is used. This Compose file also requires a GPU
- To use non-English queries (such as Japanese), prepare a server that runs a multilingual model, like ``docker/clip-server`` of ``docker-multimodalsearch``

3. Configure system.properties
------------------------------

Multimodal search settings go in ``system.properties``.
It is located at ``app/WEB-INF/conf/system.properties`` for the ZIP package, ``/etc/fess/system.properties`` for the RPM/DEB packages, and ``/opt/fess/system.properties`` for Docker.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- Set ``content_chunker.embedding.dimension`` to the number of dimensions the CLIP model outputs (512 for the ViT-B/32 family)
- ``content_chunker.search.enabled`` is read only at startup, so restart Fess after setting it
- To pass the settings as startup options, use ``-Dfess.system.<key>``. Writing them in ``fess_config.properties`` or as ``-Dfess.config.<key>`` is ignored, without any warning
- Values in ``system.properties`` take precedence over ``-Dfess.system.*``. If you write a key in both, the value in the file is used
- In the docker-fess Compose files, ``fess01`` has no volume, so ``docker compose down`` loses ``system.properties``. With Docker, the reliable way is to list ``-Dfess.system.<key>=<value>`` in the environment variable ``FESS_JAVA_OPTS`` (the ``compose.yaml`` of ``docker-multimodalsearch`` also does this)

For the list of keys, see "Configuration Reference" in `Semantic Search (Content Chunking + Vector Search) <https://fess.codelibs.org/stable/config/search-semantic.html>`__.
Multimodal search uses the same ``content_chunker.*`` keys.

4. Recreate the Index
---------------------

The mapping of the vector field ``content_chunk_vector`` is created with the number of dimensions configured when the index is created.
If you started Fess even once before making the settings above, run "Re-indexing" in [System Info] > [Maintenance] with "Replace Aliases" enabled.
For details, see `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__.

5. Enable Thumbnails
--------------------

In image search, results cannot be told apart without thumbnails.
Thumbnails are disabled by default.

- In [System] > [General], enable "Show Thumbnail" and save
- Generating thumbnails for images, PDF and Office documents requires external tools such as ImageMagick. They are not included in the default (Alpine) Docker image, so use a ``-noble`` image (e.g. ``ghcr.io/codelibs/fess:15.9.0-noble``)

For the required tools, see `Thumbnail Configuration <https://fess.codelibs.org/stable/config/crawler-thumbnail.html>`__.

6. Crawl and Check
------------------

Crawl a site or folder that contains GIF/JPEG/PNG images.
The image vectors are written at crawl time.

To check ``searcher`` in the search API, set ``query.additional.api.response.fields=searcher`` in ``fess_config.properties`` (or ``-Dfess.config.query.additional.api.response.fields=searcher`` as a startup option).

Leave the "Content Chunk Vector Indexer" job in the scheduler disabled (it is disabled by default).
The crawler writes the image vectors, so this job is not needed.
If you enable it, text documents are also vectorized with the text side of CLIP, and the ``content`` field is split.

Operational Notes
=================

It Cannot Be Combined with Semantic Search on Text
--------------------------------------------------

The plugin replaces the core semantic search searcher (``semanticChunkSearcher``) with one for CLIP.
In addition, ``content_chunker.embedding.name`` can hold only one value.
For these reasons, the semantic search on text from :doc:`guide-18` and multimodal search cannot be used at the same time in one Fess.
If you need both, build separate Fess instances.

Note also that if you restrict the searchers used with ``rank.fusion.searchers``, vector search is excluded unless ``multi_modal`` is included.
Normally, leave this setting empty.

Re-crawl When Changing the Model
--------------------------------

Always change the model and the number of dimensions together.
The number of dimensions is fixed in the mapping when the index is created, so the following steps are required after the change.

1. In [System Info] > [Maintenance], run "Re-indexing" (with "Replace Aliases" enabled) to recreate the index with the new number of dimensions
2. Re-crawl

Re-indexing only copies documents; it does not recompute the vectors.
Even with the same number of dimensions, changing the model or the CLIP server changes the vector space, so delete the documents and then re-crawl.
In ``docker-multimodalsearch``, change ``CLIP_MODEL_NAME`` and ``MULTIMODAL_DIMENSION`` in ``.env``.
The procedure is in "Model swap" in the README.

CPU and GPU
-----------

The default model of ``docker-multimodalsearch`` (512 dimensions) is meant to run on the CPU, and ``CLIP_DEVICE=cpu`` is the default.
If you switch to the larger ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k`` (1024 dimensions), a GPU is recommended; with ``CLIP_DEVICE=auto``, a GPU is used if one is available.

Summary
=======

- ``fess-webapp-multimodal`` finds GIF/JPEG/PNG images from text. It cannot search by image or vectorize images embedded in documents
- To try it, use ``v15.9.0`` of ``docker-multimodalsearch`` and specify ``FESS_THEMES_REF=15.9.x``
- Write the ``content_chunker.*`` settings in ``system.properties`` (or as ``-Dfess.system.*``)
- Check whether vector search was used by looking for ``multi_modal`` in ``searcher`` of the search API
- Non-English queries (such as Japanese) need a multilingual model, and multimodal search cannot be combined with semantic search on text in the same Fess

Further Reading
===============

- :doc:`guide-18` — Searching text documents by vectors (a configuration separate from multimodal search)
- :doc:`guide-02` — The basics of running Fess with Docker
- :doc:`guide-11` — Integrating with business systems through the search API

References
==========

- `docker-multimodalsearch (v15.9.0) <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal (15.9.0) <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
