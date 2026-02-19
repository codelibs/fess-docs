==================================
Rate Limiting Configuration
==================================

Overview
========

|Fess| includes rate limiting features to maintain system stability and performance.
These features protect the system from excessive requests and enable fair resource allocation.

Rate limiting is applied in the following scenarios:

- All HTTP requests including search API and AI mode API (via ``RateLimitFilter``)
- Crawler requests (via crawl configuration)

HTTP Request Rate Limiting
==========================

You can limit the number of HTTP requests to |Fess| per IP address.
This applies to all HTTP requests including search API, AI mode API, admin pages, etc.

Configuration
-------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # Enable rate limiting (default: false)
    rate.limit.enabled=true

    # Maximum requests per window (default: 100)
    rate.limit.requests.per.window=100

    # Window size (milliseconds) (default: 60000)
    rate.limit.window.ms=60000

Behavior
--------

- Requests exceeding the rate limit return HTTP 429 (Too Many Requests)
- Requests from IPs on the blocked IP list return HTTP 403 (Forbidden)
- Limits are applied per IP address
- For each IP, the counting window starts from the first request and resets after the window period expires (fixed window algorithm)
- When the limit is exceeded, the IP is blocked for the duration specified by ``rate.limit.block.duration.ms``

AI Mode Rate Limiting
=====================

AI mode functionality has rate limiting to control LLM API costs and resource consumption.
In addition to the HTTP request rate limiting above, AI mode has its own specific rate limit settings.

For AI mode specific rate limiting settings, see :doc:`rag-chat`.

.. note::
   AI mode rate limiting is applied separately from the LLM provider's rate limiting.
   Configure both limits accordingly.

Crawler Rate Limiting
=====================

You can configure request intervals to prevent the crawler from overloading target sites.

Web Crawl Configuration
-----------------------

Configure the following in Admin Panel under "Crawler" -> "Web":

- **Request Interval**: Wait time between requests (milliseconds)
- **Thread Count**: Number of parallel crawling threads

Recommended settings:

::

    # General sites
    intervalTime=1000
    numOfThread=1

    # Large sites (with permission)
    intervalTime=500
    numOfThread=3

Respecting robots.txt
---------------------

|Fess| respects the Crawl-delay directive in robots.txt by default.

::

    # robots.txt example
    User-agent: *
    Crawl-delay: 10

All Rate Limiting Properties
============================

All properties configurable in ``app/WEB-INF/conf/fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``rate.limit.enabled``
     - Enable rate limiting
     - ``false``
   * - ``rate.limit.requests.per.window``
     - Maximum requests per window
     - ``100``
   * - ``rate.limit.window.ms``
     - Window size (milliseconds)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - IP block duration when limit is exceeded (milliseconds)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Retry-After header value (seconds)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - IP addresses excluded from rate limiting (comma-separated)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - IP addresses to block (comma-separated)
     - (empty)
   * - ``rate.limit.trusted.proxies``
     - Trusted proxy IPs (for X-Forwarded-For/X-Real-IP resolution)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Cleanup interval to prevent memory leaks (number of requests)
     - ``1000``

Advanced Rate Limiting Configuration
=====================================

Custom Rate Limiting
--------------------

To apply different rate limiting logic based on specific conditions,
custom component implementation is required.

::

    // Custom RateLimitHelper example
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // Custom logic
        }
    }

Exclusion Settings
==================

You can exclude specific IP addresses from rate limiting or block them.

::

    # Whitelist IPs (excluded from rate limiting, comma-separated)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # Blocked IP list (always blocked, comma-separated)
    rate.limit.blocked.ips=203.0.113.50

    # Trusted proxy IPs (comma-separated)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   When using a reverse proxy, set the proxy's IP address in ``rate.limit.trusted.proxies``.
   Client IPs are resolved from X-Forwarded-For and X-Real-IP headers only for requests
   coming from trusted proxies.

Monitoring and Alerts
=====================

Configuration for monitoring rate limiting status:

Log Output
----------

When rate limiting is applied, it is recorded in the logs:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Troubleshooting
===============

Legitimate Requests Being Blocked
---------------------------------

**Cause**: Limit values are too strict

**Solutions**:

1. Increase ``rate.limit.requests.per.window``
2. Add specific IPs to the whitelist (``rate.limit.whitelist.ips``)
3. Adjust the window size (``rate.limit.window.ms``)

Rate Limiting Not Working
-------------------------

**Cause**: Configuration is not properly applied

**Check**:

1. Is ``rate.limit.enabled=true`` configured?
2. Is the configuration file being read correctly?
3. Has |Fess| been restarted?

Performance Impact
------------------

If rate limiting checks themselves impact performance:

1. Use the whitelist to skip checks for trusted IPs
2. Disable rate limiting (``rate.limit.enabled=false``)

Reference Information
=====================

- :doc:`rag-chat` - AI Mode Configuration
- :doc:`../admin/webconfig-guide` - Web Crawl Configuration Guide
- :doc:`../api/api-overview` - API Overview
