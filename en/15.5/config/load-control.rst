==================================
Load Control Configuration
==================================

Overview
========

|Fess| includes a load control feature that controls requests based on OpenSearch CPU usage.
This feature automatically limits requests during high search engine load, protecting system stability.

Load control features:

- Real-time monitoring of OpenSearch cluster CPU usage
- Independent thresholds for web requests and API requests
- Returns HTTP 429 (Too Many Requests) when thresholds are exceeded
- Admin panel, login, and static resources are excluded from control
- Disabled by default (threshold=100)

Configuration
=============

Set the following properties in ``fess_config.properties``:

::

    # CPU usage threshold for web requests (%)
    # Requests are rejected when CPU usage is at or above this value
    # Set to 100 to disable (default: 100)
    web.load.control=100

    # CPU usage threshold for API requests (%)
    # Requests are rejected when CPU usage is at or above this value
    # Set to 100 to disable (default: 100)
    api.load.control=100

    # CPU usage monitoring interval (seconds)
    # Interval for retrieving OpenSearch cluster CPU usage
    # Default: 1
    load.control.monitor.interval=1

.. note::
   When both ``web.load.control`` and ``api.load.control`` are set to 100 (default),
   the load control feature is completely disabled and monitoring does not start.

How It Works
============

Monitoring Mechanism
--------------------

When load control is enabled (any threshold is below 100), LoadControlMonitorTarget periodically monitors the OpenSearch cluster CPU usage.

- Retrieves OS statistics from all nodes in the OpenSearch cluster
- Records the highest CPU usage among all nodes
- Monitors at the interval specified by ``load.control.monitor.interval`` (default: 1 second)
- Monitoring starts lazily on the first request

.. note::
   If monitoring information retrieval fails, CPU usage is reset to 0.
   After 3 consecutive failures, the log level changes from WARNING to DEBUG.

Request Control
---------------

When a request arrives, LoadControlFilter processes it in the following order:

1. Check if the path is excluded (if excluded, pass through)
2. Determine the request type (Web / API)
3. Get the corresponding threshold
4. If the threshold is 100 or above, do not control (pass through)
5. Compare current CPU usage with the threshold
6. If CPU usage >= threshold, return HTTP 429

**Excluded requests:**

- Paths starting with ``/admin`` (admin panel)
- Paths starting with ``/error`` (error pages)
- Paths starting with ``/login`` (login pages)
- Static resources (``.css``, ``.js``, ``.png``, ``.jpg``, ``.gif``, ``.ico``, ``.svg``, ``.woff``, ``.woff2``, ``.ttf``, ``.eot``)

**For web requests:**

- Returns HTTP 429 status code
- Displays the error page (``busy.jsp``)

**For API requests:**

- Returns HTTP 429 status code
- Returns a JSON response:

::

    {
        "response": {
            "status": 9,
            "message": "Server is busy. Please retry after 60 seconds.",
            "retry_after": 60
        }
    }

Configuration Examples
======================

Limit Web Requests Only
-----------------------

Configuration that limits only web search requests while leaving API unrestricted:

::

    # Web: Reject requests when CPU usage is 80% or above
    web.load.control=80

    # API: No restriction
    api.load.control=100

    # Monitoring interval: 1 second
    load.control.monitor.interval=1

Limit Both Web and API
----------------------

Example with different thresholds for web and API:

::

    # Web: Reject requests when CPU usage is 70% or above
    web.load.control=70

    # API: Reject requests when CPU usage is 80% or above
    api.load.control=80

    # Monitoring interval: 2 seconds
    load.control.monitor.interval=2

.. note::
   By setting the API threshold higher than the web threshold, you can achieve staged control
   where web requests are restricted first during high load, and API requests are also restricted
   when the load increases further.

Difference from Rate Limiting
=============================

|Fess| has a :doc:`rate-limiting` feature separate from load control.
These protect the system using different approaches.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Item
     - Rate Limiting
     - Load Control
   * - Control Basis
     - Number of requests (per time unit)
     - OpenSearch CPU usage
   * - Purpose
     - Prevent excessive requests
     - Protect search engine from high load
   * - Limit Unit
     - Per IP address
     - System-wide
   * - Response
     - HTTP 429
     - HTTP 429
   * - Scope
     - Search API / AI Mode API
     - Web requests / API requests

Combining both features enables more robust system protection.

Troubleshooting
===============

Load Control Not Taking Effect
------------------------------

**Cause**: Configuration is not properly applied

**Check**:

1. Is ``web.load.control`` or ``api.load.control`` set below 100?
2. Is the configuration file being read correctly?
3. Has |Fess| been restarted?

Legitimate Requests Being Rejected
-----------------------------------

**Cause**: Thresholds are too low

**Solutions**:

1. Increase the ``web.load.control`` or ``api.load.control`` values
2. Adjust ``load.control.monitor.interval`` to change the monitoring frequency
3. Scale up the OpenSearch cluster resources

.. warning::
   Setting thresholds too low may cause requests to be rejected even under normal load.
   Check the normal CPU usage of your OpenSearch cluster before setting appropriate thresholds.

Reference Information
=====================

- :doc:`rate-limiting` - Rate Limiting Configuration
