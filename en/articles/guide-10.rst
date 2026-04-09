===========================================================================
Part 10: Stable Operation of a Search System -- Monitoring, Backup, and Failure Recovery in Practice
===========================================================================

Introduction
============

Once you have built a search system and made it available to users, it becomes a system that "cannot be stopped."
When users come to rely on search in their daily work, any downtime directly leads to business disruption.

This article provides a practical playbook for monitoring, backup, and failure recovery to keep Fess running reliably.

Target Audience
===============

- Administrators operating Fess in a production environment
- Those who want to ensure stable operation of a search system
- Those with basic knowledge of system operations

Operational Overview
=====================

Stable operation of Fess is built on the following three pillars:

1. **Monitoring**: Detect problems early
2. **Backup**: Protect your data
3. **Failure Recovery**: Restore service quickly when problems occur

Monitoring
==========

Health Check
--------------

Fess provides a health check endpoint via REST API.

::

    GET http://localhost:8080/api/v1/health

When operating normally, it returns HTTP 200.
By periodically calling this endpoint from an external monitoring tool (such as Nagios, Zabbix, or Datadog), you can monitor the operational status of Fess.

Checking System Information
---------------------------

From [System Info] in the administration console, you can check the following information.

**Crawl Info**

You can review the results of the last crawl execution (number of processed documents, number of errors, etc.).
Use this to verify that crawls are completing successfully.

**System Info**

You can check the versions of Fess and OpenSearch, JVM memory usage, number of documents in the index, and more.

Metrics to Monitor
-------------------

.. list-table:: Monitoring Metrics and Threshold Guidelines
   :header-rows: 1
   :widths: 25 35 40

   * - Metric
     - How to Check
     - Warning Condition
   * - Fess Process
     - Health API
     - No response or HTTP 500
   * - OpenSearch Cluster
     - Cluster Health API
     - Status is yellow / red
   * - JVM Heap Usage
     - System Info
     - Sustained above 80%
   * - Disk Usage
     - OS Commands
     - Above 85%
   * - Crawl Results
     - Crawl Info
     - Sudden increase in errors, drastic decrease in processed count
   * - Search Response
     - Search Log
     - Significant increase in response time

Crawl Completion Notification
------------------------------

Fess has a feature that sends notifications when error logs or search engine failures are detected.
By configuring a Webhook for Slack or Google Chat, you can be immediately informed of any anomalies.

Backup
=======

Backup Targets
----------------

The backup targets for a Fess environment fall into two main categories.

**1. Configuration Data**

This includes crawl settings, user information, dictionary data, and other information configured through the administration console.
You can obtain a backup of the configuration data from [System Info] > [Backup] in the Fess administration console.

**2. Index Data**

This is the index of documents collected by crawling.
Use the OpenSearch snapshot feature to back up the index.

Backup Strategy
-----------------

.. list-table:: Backup Strategy
   :header-rows: 1
   :widths: 20 25 25 30

   * - Target
     - Frequency
     - Retention Period
     - Method
   * - Configuration Data
     - Daily
     - 30 generations
     - Fess Backup Feature
   * - Index
     - Daily
     - 7 generations
     - OpenSearch Snapshot
   * - Docker Configuration
     - On change
     - Git managed
     - Version control of compose.yaml

Automating Configuration Data Backup
--------------------------------------

You can automate configuration data backup using the Fess administration API.
Set it up as a scheduler job or run it as an external cron job.

Restore Procedure
-------------------

It is important to verify the restore procedure in advance for when a failure occurs.

1. Stop Fess
2. Restore configuration data (via administration console or API)
3. Restore from OpenSearch snapshot if needed
4. Start Fess
5. Verify operation

Rehearse the restore procedure regularly to confirm its accuracy and to understand the time required.

Failure Recovery
================

Common Failures and Solutions
------------------------------

**Fess Does Not Start**

- Check the log file (logs/fess.log)
- JVM out of memory: Adjust the ``-Xmx`` parameter
- Port conflict: Check whether port 8080 is being used by another process
- Failed to connect to OpenSearch: Verify that OpenSearch is running

**Crawl Fails**

- Check the job log ([System Info] > [Job Log])
- Network connectivity: Verify connectivity to the crawl target
- Authentication error: Check the validity of credentials (password, token)
- Failure URLs: Check details at [System Info] > [Failure URL]

**Search Is Slow**

- Check the OpenSearch cluster status (action is needed if it is yellow/red)
- Check the index size (whether it has grown excessively)
- Check JVM heap (whether garbage collection is occurring frequently)
- If crawling is in progress, check whether performance improves after the crawl completes

**Search Results Are Outdated**

- Check the crawl schedule (whether it is running normally)
- Check whether the maximum access count in crawl settings is insufficient
- Check whether the target site is blocking crawls (robots.txt)

Managing Failure URLs
----------------------

URLs that could not be accessed during crawling are recorded as "Failure URLs."
You can review them at [System Info] > [Failure URL] in the administration console.

If there are many failure URLs, check the following:

- Whether the target server is down
- Whether there are issues with the network route
- Whether credentials are still valid
- Whether the crawl interval is too short, placing excessive load on the target server

Log Management
--------------

Fess log files are output to the following locations:

- **Fess Log**: ``logs/fess.log`` (Application log)
- **Crawl Info**: [System Info] > [Crawl Info] in the administration console
- **Job Log**: [System Info] > [Job Log] in the administration console
- **Search Log**: [System Info] > [Search Log] in the administration console

Make sure log rotation is configured to prevent log files from growing excessively.

Operations Checklist
=====================

Here is a checklist of items to verify during routine operations.

**Daily Checks**

- Did the crawl complete successfully?
- Is the health check returning normal results?
- Is disk usage below the threshold?

**Weekly Checks**

- Zero-hit rate in search logs (see Part 8)
- Review and address failure URLs
- Are backups being taken successfully?

**Monthly Checks**

- Trends in index size
- Trends in JVM memory usage
- Dictionary updates (see Part 9)
- Review of security patches

Summary
========

This article covered monitoring, backup, and failure recovery for the stable operation of Fess.

- Monitoring with the Health API and administration console
- Backup strategy for configuration data and index data
- Common failure patterns and solutions
- Daily, weekly, and monthly operations checklists

To maintain the expectation that "search just works," establish a proactive operational framework.

The next article will cover patterns for integrating with existing systems using the Search API.

References
==========

- `Fess System Administration <https://fess.codelibs.org/ja/15.5/admin/systeminfo.html>`__

- `Fess Backup <https://fess.codelibs.org/ja/15.5/admin/backup.html>`__
