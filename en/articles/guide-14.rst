============================================================
Part 14: Scaling Strategies for Search Systems -- Gradual Expansion from Small to Large Scale
============================================================

Introduction
============

When you start with a small-scale Fess deployment, growing usage inevitably brings demands such as "more documents," "more users," and "faster search."

This article explains the strategies and decision criteria for gradually scaling from a small single-server configuration to a large-scale cluster configuration.

Target Audience
===============

- Those planning large-scale Fess operations
- Those facing performance issues
- Those who want to understand the basic concepts of OpenSearch clusters

Scaling Stages
===============

Scaling Fess typically proceeds through the following stages.

.. list-table:: Scaling Stages
   :header-rows: 1
   :widths: 15 20 25 20 20

   * - Stage
     - Configuration
     - Approx. Document Count
     - Approx. User Count
     - Cost
   * - S
     - Single Server
     - Up to 1 million
     - Up to 50
     - Low
   * - M
     - Separated Configuration
     - Up to 1 million
     - Up to 500
     - Medium
   * - L
     - Cluster Configuration
     - 1 million to 10 million
     - Up to several thousand
     - High
   * - XL
     - Multi-Instance
     - 10 million or more
     - Several thousand or more
     - Highest

Stage S: Single Server Configuration
======================================

This corresponds to the Docker Compose configuration built in Part 2.
Fess and OpenSearch run on the same server.

Use Cases
---------

- Initial deployment, PoC, small to medium-sized organizations
- Document count of 1 million or less
- Few concurrent search users

Tuning Points
--------------

**JVM Heap Adjustment**

Set the JVM heap size appropriately for both Fess and OpenSearch.

- Fess: Maximum 2 GB (default; initial heap is 256 MB)
- OpenSearch: 50% or less of physical memory, but no more than 32 GB

**Thread Pool**

Adjust the number of crawl threads according to the server's CPU core count.

Stage M: Separated Configuration
==================================

Physically separate the Fess server and the OpenSearch server.

Use Cases
---------

- When concurrent search users increase and search performance during crawling becomes an issue
- When memory or CPU becomes insufficient at Stage S

Configuration
--------------

::

    [Fess Server] <-> [OpenSearch Server]

Change the OpenSearch connection target in Fess settings to the external server.

Benefits
---------

- Eliminates resource contention between Fess (crawl processing) and OpenSearch (search processing)
- Allows optimal resource allocation (CPU, memory) for each server
- OpenSearch server disk I/O becomes independent

Stage L: Cluster Configuration
================================

Configure OpenSearch as a cluster to improve search redundancy and performance.

Use Cases
---------

- Document count of 1 million to 10 million
- When high availability is required
- When search response improvement is needed

Configuration Example
----------------------

::

    [Fess Server]
          |
    [OpenSearch Node 1] (Master/Data)
    [OpenSearch Node 2] (Data)
    [OpenSearch Node 3] (Data)

The OpenSearch cluster distributes and replicates data using the concepts of shards and replicas.

**Shards**: Split the index and distribute it across multiple nodes (faster processing through parallelization)

**Replicas**: Keep copies of shards on different nodes (redundancy in case of failure + search parallelization)

Configuration Tips
-------------------

- Number of shards: Set according to document count and search performance (target 10-50 GB per shard)
- Number of replicas: At least 1 (to ensure redundancy)
- Number of nodes: At least 3 (quorum for master election)

Stage XL: Multi-Instance Configuration
========================================

Configure multiple Fess instances to distribute crawl and search processing.

Use Cases
---------

- Document count exceeds 10 million
- Need to run large crawl jobs in parallel
- High-frequency search requests

Configuration Example
----------------------

::

    [Load Balancer]
      +-- [Fess Instance 1] (Search + Admin)
      +-- [Fess Instance 2] (Search)
      +-- [Fess Instance 3] (Crawl Only)
              |
    [OpenSearch Cluster]
      +-- [Node 1] (Master)
      +-- [Node 2] (Data)
      +-- [Node 3] (Data)
      +-- [Node 4] (Data)

Starting from Fess 15.6, the distributed coordinator feature enables exclusive control of maintenance operations (such as index rebuilding and clearing) across multiple Fess instances.

Scaling Decision Flowchart
===========================

When performance issues occur, identify the cause and consider countermeasures in the following order.

**1. When Search Is Slow**

- Check the OpenSearch cluster status
- Check JVM heap usage
- Check index size
- -> Consider Stage M (separation) or Stage L (clustering)

**2. When Crawling Is Slow or Does Not Complete**

- Check the number of documents to be crawled
- Adjust thread count and interval
- Check the impact on search during crawling
- -> Consider Stage M (separation) or Stage XL (dedicated crawl instance)

**3. When There Are Many Concurrent Accesses**

- Monitor search response time
- Check Fess server CPU usage
- -> Consider Stage XL (load balancer + multiple instances)

JVM Tuning
============

At any stage, JVM tuning has a significant impact on performance.

Key Parameters
---------------

.. list-table:: JVM Parameters
   :header-rows: 1
   :widths: 25 35 40

   * - Parameter
     - Description
     - Recommended Value
   * - ``-Xmx``
     - Maximum heap size
     - 50% or less of physical memory
   * - ``-Xms``
     - Initial heap size
     - Same value as ``-Xmx``
   * - GC settings
     - Garbage collection method
     - G1GC (default)

Heap Size Guidelines
---------------------

- 1 million or less: 2-4 GB
- 1 million to 5 million: 8 GB
- 5 million to 10 million: 16 GB
- 10 million or more: 32 GB or more (OpenSearch side)

Summary
========

This article explained the gradual scaling strategies for Fess.

- **Stage S**: Single server (up to 1 million documents)
- **Stage M**: Fess / OpenSearch separation (up to 1 million documents, multi-user support)
- **Stage L**: OpenSearch clustering (1 million to 10 million documents)
- **Stage XL**: Fess multi-instance (10 million documents or more)
- Scaling decision flowchart and JVM tuning

With the approach of "start small and grow as needed," you can scale according to requirements while keeping costs under control.

The next article will cover security architecture.

References
==========

- `Fess Installation Guide <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `OpenSearch Cluster Configuration <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
