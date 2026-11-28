========================================
Scaling Fess as Documents and Users Grow
========================================

Introduction
============

As the number of documents and users grows, problems start to appear: "the crawl no longer finishes by morning", "searches have become slow", "Fess stopped with an OutOfMemoryError".
Adding servers straight away does not necessarily solve them.
Fess runs as several JVM processes, and it is often just one of them that runs short.

This article targets Fess 15.9 and explains how to scale in the following order.

1. Find out which process is short of what
2. Tune memory and crawl parallelism on a single server
3. Move OpenSearch to a separate server
4. Turn OpenSearch into a three-node cluster
5. Run multiple Fess servers

Setting up monitoring (health checks, logs, notifications) and backups is covered in :doc:`guide-10`.

The Processes That Make Up Fess
===============================

Even when Fess runs on a single server, its memory settings are split as follows.

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Process
     - Role
     - Default heap
     - Where to set it
   * - Fess server
     - Search page, admin console, API, scheduler
     - ZIP package: minimum 256m, maximum 2g; RPM/DEB packages and the Docker image: 512m
     - Environment variable ``FESS_HEAP_SIZE``
   * - Crawler
     - A separate JVM started for each crawl job
     - Maximum 512m
     - ``jvm.crawler.options`` in ``fess_config.properties``
   * - Suggest generation, thumbnail generation
     - A separate JVM started for each job
     - Maximum 256m
     - ``jvm.suggest.options``, ``jvm.thumbnail.options``
   * - OpenSearch
     - Stores the index and executes searches
     - 1g in docker-fess's ``compose-opensearch3.yaml``
     - ``OPENSEARCH_JAVA_OPTS`` or ``config/jvm.options``

The chunk processing used by semantic search also has its own JVM (``jvm.chunk.options``, maximum 1g); it is covered in :doc:`guide-18`.

If ``fess-crawler.log`` shows an OutOfMemoryError, it is the crawler's JVM that is short of memory.
In that case, increasing ``FESS_HEAP_SIZE`` has no effect.

Finding Out What Is Short
=========================

Check the following places, depending on the symptom.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptom
     - Where to check
   * - Searches are slow
     - On the [Performance] tab of [System Info] > [Search Log], look at the p95 and p99 response times and the slow search terms. Distinguish whether only specific search terms are slow or everything is slow.
   * - Crawls do not finish
     - In [System Info] > [Job Log], look at how the start and end times of crawl jobs change over time. If ``fess-crawler.log`` keeps showing ``Cpu Load XX% is greater than 50%``, the crawl is being held back by the load control described later.
   * - The crawler stops
     - Look for ``OutOfMemoryError`` in ``fess-crawler.log``.
   * - The Fess server stops or the admin console is slow
     - Look for ``OutOfMemoryError`` in ``fess.log`` and check ``response.stats.jvm.memory.heap.percent`` in ``/api/admin/stats``.
   * - OpenSearch is slow
     - Check ``response.stats.engine.status`` in ``/api/admin/stats`` and the heap usage in OpenSearch's ``_cat/nodes``. A ``circuit_breaker_exception`` is a sign of insufficient heap.

``/api/admin/stats`` returns the state of the JVM and OS of the Fess server that received the request, and of the OpenSearch cluster.
It does not include the crawler's JVM or the heap of each OpenSearch node.
Calling it requires an access token with the ``admin-api`` permission.
See `Admin API Overview <https://fess.codelibs.org/stable/api/admin/api-admin-overview.html>`__ for how to create one, and `Stats API <https://fess.codelibs.org/stable/api/admin/api-admin-stats.html>`__ for the response fields.

Query OpenSearch directly for the heap of each OpenSearch node.

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

You can check the number of documents and the size of the index with the following command.
``fess.search`` is the alias of the index used for searching.

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

Tuning a Single Server
======================

Changing the Fess Server Heap
-----------------------------

With Docker, add ``FESS_HEAP_SIZE`` to ``environment`` of ``fess01`` in ``compose.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

If you change ``environment`` or ``volumes`` of ``fess01`` in ``compose.yaml`` and run ``docker compose ... up -d``, the ``fess01`` container is recreated.
Settings changed in [System] > [General] are stored in ``system.properties`` inside the container, so they are lost when it is recreated.
The same applies whenever another step in this article changes ``compose.yaml``.
Take a backup first, following the steps in :doc:`guide-10`.

For the RPM package, edit ``FESS_HEAP_SIZE=512m`` in ``/etc/sysconfig/fess``; for the DEB package, in ``/etc/default/fess``. Then restart Fess.
For the ZIP package, export ``FESS_HEAP_SIZE`` in the environment that starts Fess.

Confirm that the change took effect by looking at the arguments of the running processes.
With Docker, run the following.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

The line after ``-Xmx`` shows the type of the process.
``FessBoot`` is the Fess server, and ``exec.Crawler`` is the crawler.
For the RPM/DEB and ZIP packages, run the command inside ``sh -c`` and everything after it directly on the Fess server.

Changing the Crawler Heap
-------------------------

``jvm.crawler.options`` is a single value that lists JVM options separated by ``\n``.
Because the whole value is replaced, writing only ``-Xmx1g`` removes all default options, such as G1GC.
Keep the default value and rewrite only the ``-Xmx512m`` line.

::

    -Xms128m\n\
    -Xmx1g\n\

The configuration file is ``/etc/fess/fess_config.properties`` for the RPM/DEB packages and ``app/WEB-INF/classes/fess_config.properties`` for the ZIP package.
With Docker, copy ``fess_config.properties`` from the image to your machine, edit it, and mount it at ``/opt/fess/fess_config.properties`` in the container.
``/opt/fess`` is read in preference to ``/etc/fess``.
Because this value spans several lines, it is not suited to being set with ``-Dfess.config.`` in ``FESS_JAVA_OPTS``.
For the steps, see "How to Apply Configuration Files" in `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__.

After restarting Fess, confirm in "App Properties" of [System Info] > [Config Info] that ``jvm.crawler.options`` contains ``-Xmx1g``.
The change takes effect from the next crawler that starts.
If you run the command from the previous section while a crawl is running, ``-Xmx1g`` appears on the line before ``org.codelibs.fess.exec.Crawler``.

One crawler JVM starts per crawl job.
The "Default Crawler" job processes all crawl configurations in a single crawler.
If you create a job for each configuration with [Create New Job] on the details page of a crawl configuration, each one starts as a separate crawler, and each one uses memory up to its ``-Xmx``.
To limit the number of crawlers running at the same time, use ``job.max.crawler.processes`` in ``fess_config.properties`` (the default ``0`` means unlimited).
A crawl job started beyond that limit does not wait for its turn; it ends with an error.

For the suggest generation and thumbnail generation JVMs, rewrite the ``-Xmx256m`` line of ``jvm.suggest.options`` and ``jvm.thumbnail.options`` in the same way.

Changing the OpenSearch Heap
----------------------------

In docker-fess, ``search01`` in ``compose-opensearch3.yaml`` has the following line.

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

Change both values to the same new value.
For OpenSearch installed from ZIP or RPM, change ``-Xms`` and ``-Xmx`` in ``config/jvm.options`` and restart it.

As a rule of thumb, the upper limit is no more than half of physical memory, and less than 32GB.
The remaining memory serves as the OS file cache and contributes to search speed, so do not allocate too much to the heap.
At 32GB or more, the JVM's Compressed OOPs are disabled and efficiency actually drops.
At a scale that needs more than that, add nodes.

Guidelines that relate index size to heap size are in `Memory Configuration <https://fess.codelibs.org/stable/config/setup-memory.html>`__.
Start from those guidelines, and adjust while watching the heap usage in ``_cat/nodes`` mentioned earlier and the search response times.

When Fess and OpenSearch run on the same server, make sure that the total heap of the Fess server, the crawler and OpenSearch fits in physical memory.

Changing Crawl Parallelism
--------------------------

Crawl speed is determined by the following three settings.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Setting
     - Default
     - Location
   * - Number of Threads
     - Web 1, file system 5
     - Each crawl configuration ([Crawler] > [Web], [File System])
   * - Interval
     - Web 10000 ms, file system 1000 ms
     - Same as above. The time each thread waits every time it fetches a URL
   * - Concurrent Crawler Config
     - 5
     - [System] > [General]. The number of crawl configurations a single crawler processes at the same time

Increasing the number of threads makes fetching for that crawl configuration faster, but it also increases the crawler's memory usage and the load on the servers being crawled.
When crawling external sites or servers used for daily business, do not make the interval too short.

Something easily overlooked on a single server is ``adaptive.load.control`` in ``fess_config.properties`` (default ``50``).
While the CPU usage of the server running Fess is at or above this value, the crawl and indexing threads wait.
If OpenSearch on the same server is using CPU to write to the index or to run searches, the crawl can almost stop progressing.
In that case, ``fess-crawler.log`` shows ``Cpu Load XX% is greater than 50%``.
You can raise the value, but if the CPU is chronically short, the fundamental fix is to move OpenSearch to a separate server, as described in the next section.
For details, see `Load Control Configuration <https://fess.codelibs.org/stable/config/load-control.html>`__.

Moving OpenSearch to a Separate Server
======================================

Moving OpenSearch to a separate server means that crawling and searching no longer compete for CPU, memory and disk I/O.

What OpenSearch Needs
---------------------

The OpenSearch that Fess uses needs the following two things.

- The four plugins for Fess (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash``, ``opensearch-configsync``). Their versions must match OpenSearch (Fess 15.9 uses OpenSearch 3.9.0)
- ``configsync.config_path`` in ``opensearch.yml``. Specify, as an absolute path, a directory for dictionary files under the OpenSearch configuration directory

The installation commands are in `Linux Installation (Detailed Procedure) <https://fess.codelibs.org/stable/install/install-linux.html>`__.
docker-fess's ``ghcr.io/codelibs/fess-opensearch`` image includes all of these from the start.

When OpenSearch is placed on a separate server, port 9200 is exposed to the network.
Do not use it in production with the security plugin disabled.
For the settings, see :doc:`guide-15` and `Security Configuration <https://fess.codelibs.org/stable/install/security.html>`__.

What to Configure in Fess
-------------------------

In Fess, specify the connection target and the dictionary location with two environment variables.

- ``SEARCH_ENGINE_HTTP_URL`` : the URL of OpenSearch
- ``FESS_DICTIONARY_PATH`` : the same path as ``configsync.config_path`` on the OpenSearch side

``FESS_DICTIONARY_PATH`` is a path on the OpenSearch server.
Fess writes dictionary files through the ``configsync`` plugin, so the Fess server does not need to mount that directory.
If it is not set, Fess cannot create its indexes and does not start.

Set them in ``/etc/sysconfig/fess`` for the RPM package, ``/etc/default/fess`` for the DEB package, and ``bin/fess.in.sh`` for the ZIP package.
With Docker, do not use ``compose-opensearch3.yaml``; specify them in ``environment`` of ``fess01`` in ``compose.yaml``.
In v15.9.0, ``fess01`` in ``compose.yaml`` has a ``depends_on`` that waits for ``search01``, so a setup that does not define ``search01`` fails to start with the error ``service "fess01" depends on undefined service "search01"``.
Delete the three lines from ``depends_on`` through ``condition: service_healthy``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

In this case, run all subsequent ``docker compose`` commands with ``-f compose.yaml`` only.

With the ZIP package, before starting Fess you can use ``bin/fess-setup check`` to confirm the connection, the four plugins and the response from ``configsync``.

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

Changing the connection target does not move the existing indexes to the new OpenSearch.
To carry over existing documents, migrate them with snapshots ("Data Migration" in `Index Management <https://fess.codelibs.org/stable/config/admin-index-backup.html>`__).
If crawling again is enough, it is simpler to connect to an empty OpenSearch and recrawl.

Turning OpenSearch into a Three-Node Cluster
============================================

While OpenSearch runs on a single server, searching stops whenever that server stops.
When you need redundancy, turn OpenSearch into a cluster.

Node Layout
-----------

Electing the node that manages the cluster (the cluster manager) requires agreement from a majority.
With only one or two cluster-manager-eligible nodes, the loss of a single node makes election impossible.
For that reason, prepare three cluster-manager-eligible nodes.
The smallest setup is one in which all three also hold data.

The following is an example of the cluster-related settings in each node's ``opensearch.yml`` (change ``node.name`` for each node).
Add network settings such as ``network.host`` and security settings to suit your environment.

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Install the four plugins for Fess on all three nodes, at the same version.
Also use the same path for ``configsync.config_path`` on all three nodes.
This is because Fess writes a single value of ``FESS_DICTIONARY_PATH`` into the index settings, and every node reads the dictionaries at that path.

docker-fess's ``compose/snapshot/compose-cluster.yaml`` contains an example of building multiple nodes with Docker.
That file is meant to be combined with a development version of the Fess image, so use it as a reference for how to write the OpenSearch environment variables.

Connecting from Fess
--------------------

In ``SEARCH_ENGINE_HTTP_URL``, list the node URLs separated by commas.
Even if some nodes are down, Fess connects to the remaining ones.

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

Shards and Replicas
-------------------

Fess creates the index for documents using ``index.number_of_shards`` in ``fess_config.properties`` (default ``5``, the number of primary shards) and ``index.auto_expand_replicas`` (default ``0-1``, which automatically adjusts the replicas between 0 and 1 according to the number of data nodes).
Because of the default ``0-1``, once there are two or more data nodes, one replica is created for each shard without changing any Fess settings.
When the cluster status becomes ``green``, all replicas have been allocated.

The number of shards is fixed when the index is created; changing ``index.number_of_shards`` later does not affect the existing index.
To change it, use "Re-indexing" in [System Info] > [Maintenance].
If you specify "Number of Shards" and "Auto-expand Replicas", enable "Replace Aliases" and start it, Fess creates a new index, copies the documents, and moves the ``fess.search`` and ``fess.update`` aliases to the new index.

Keep the following in mind when re-indexing.

- Documents are copied from the index that ``fess.update`` points to at the moment you start. Run it at a time when no crawl is running
- The old index is not deleted automatically. The disk needs enough capacity to hold both the old and the new index

For the items on the screen, see `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__.

Checking the Cluster
--------------------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

If three nodes are listed and ``status`` is ``green``, the cluster is complete.
You can confirm the same thing in Fess's ``/api/admin/stats`` with ``response.stats.engine.number_of_nodes`` and ``response.stats.engine.status``.

Running Multiple Fess Servers
=============================

When search users increase and the Fess server runs short of CPU, or when you want Fess itself to be redundant, connect multiple Fess servers to the same OpenSearch.
Note that docker-fess's ``compose/multi-instance/`` is a setup that runs independent search services side by side, each Fess using its own indexes; it differs from the setup described here (to separate by organization, see :doc:`guide-13`).

Crawl configurations, users, jobs and job logs are stored in OpenSearch, so they look the same from every Fess.
On the other hand, the following exist separately on each Fess server, so they must be kept the same on all servers.

- The settings in [System] > [General] (``system.properties`` on each server). Changing them on the settings page changes only the value on that server
- ``fess_config.properties`` and environment variables such as ``FESS_HEAP_SIZE``
- Installed plugins
- ``app.cipher.key`` in ``fess_config.properties``. Among the parameters of crawl configurations and data store configurations, values whose names end in ``password``, ``key``, ``token``, ``secret`` and so on are encrypted with this key and stored in OpenSearch. If the key differs between servers, values saved on another server cannot be decrypted

Choosing the Server That Crawls
-------------------------------

The "Target" of every default job is ``all``.
``all`` matches on every Fess, so as things stand, "Default Crawler" runs on all servers at the same time.

To leave crawling to a single server, do both of the following.

1. On the crawling server only, write an identifier in ``fess_config.properties``, such as ``scheduler.target.name=crawler``, and restart. With Docker, you can specify ``-Dfess.config.scheduler.target.name=crawler`` in ``FESS_JAVA_OPTS``. Leave it empty on the other servers
2. In [System] > [Scheduler], open "Default Crawler", change "Target" from ``all`` to ``crawler`` and save. Change crawl jobs created with [Create New Job] in the same way

"Target" accepts multiple identifiers separated by commas.
With step 1 alone, jobs keep running on all servers as before.
With step 2 alone, no server has a matching identifier, so crawls run on none of them.
To confirm that step 1 took effect, check the value of ``scheduler.target.name`` in "App Properties" of [System Info] > [Config Info] on the crawling server.

Leave "Target" as ``all`` for jobs other than crawling (such as log aggregation and deleting old documents).

Once crawling is pinned, press [Start Now] from the admin console of the crawling server as well.
If you press it on another server, the screen says the job has started, but it does not run on that server; only ``Ignoring job`` is recorded in ``fess.log``.
If the servers are behind a load balancer, prepare a route that reaches the crawling server directly.

Load Balancer Settings
----------------------

In Fess 15.9, login sessions are stored in the memory of each Fess.
When a load balancer distributes the search page or admin console used with login, enable sticky sessions so that the same user keeps being sent to the same server.
Storing sessions in OpenSearch to share them across servers is available from 15.10 onward.

You can use ``/api/v2/health`` for the load balancer's health check.
It returns 503 when the OpenSearch cluster is ``RED`` and when it cannot connect to OpenSearch.

Exclusive Control of Maintenance Operations
-------------------------------------------

"Re-indexing", "Reload Document Index", "Delete Crawler Index" and "Rebuild Config Index" in [System Info] > [Maintenance] are locked so that multiple Fess servers do not run them at the same time.
If one is already running on another server, "The operation is already running on <host name>." is displayed.
This lock applies only to maintenance operations; it does not coordinate jobs or [General] settings between servers.

About Sizing Guidelines
=======================

The number of documents or users alone does not determine the setup you need.
The memory and CPU required vary greatly with the length of body text per document, the share of attachments, search term trends, and whether users log in.

Decide based on measured values, as follows.

- From the index's ``store.size``, determine the OpenSearch heap using the guideline table in `Memory Configuration <https://fess.codelibs.org/stable/config/setup-memory.html>`__
- If the p95 in the search log worsens and the heap usage or CPU in ``_cat/nodes`` stays high, increase the OpenSearch heap or add nodes
- If crawl times in the job log grow longer and ``Cpu Load`` log lines appear, move OpenSearch to a separate server
- If OpenSearch has headroom but the Fess server's CPU is high, run multiple Fess servers

Further Reading
===============

- Run Fess in production with monitoring, logs and backups in place: :doc:`guide-10`
- Protect access, including how far OpenSearch is exposed and how users log in: :doc:`guide-15`
- Manage the work of keeping settings consistent across servers as code: :doc:`guide-16`
- Use a single Fess separately for each organization: :doc:`guide-13`
- Organize what to check at each stage of a rollout: :doc:`guide-23`

References
==========

- `Memory Configuration <https://fess.codelibs.org/stable/config/setup-memory.html>`__
- `Port and Network Settings <https://fess.codelibs.org/stable/config/setup-port-network.html>`__
- `Load Control Configuration <https://fess.codelibs.org/stable/config/load-control.html>`__
- `Linux Installation (Detailed Procedure) <https://fess.codelibs.org/stable/install/install-linux.html>`__
- `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__
- `fess-setup Command <https://fess.codelibs.org/stable/install/fess-setup.html>`__
- `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__
- `Scheduler <https://fess.codelibs.org/stable/admin/scheduler-guide.html>`__
- `Search Log <https://fess.codelibs.org/stable/admin/searchlog-guide.html>`__
- `Stats API <https://fess.codelibs.org/stable/api/admin/api-admin-stats.html>`__
- `Index Management <https://fess.codelibs.org/stable/config/admin-index-backup.html>`__
