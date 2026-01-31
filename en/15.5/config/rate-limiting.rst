==================================
Rate Limiting Configuration
==================================

Overview
========

|Fess| includes rate limiting features to maintain system stability and performance.
These features protect the system from excessive requests and enable fair resource allocation.

Rate limiting is applied in the following scenarios:

- Search API
- AI Mode API
- Crawler requests

Search API Rate Limiting
========================

You can limit the number of requests to the search API.

Configuration
-------------

``app/WEB-INF/conf/system.properties``:

::

    # Enable rate limiting
    api.rate.limit.enabled=true

    # Maximum requests per minute per IP address
    api.rate.limit.requests.per.minute=60

    # Rate limit window size (seconds)
    api.rate.limit.window.seconds=60

Behavior
--------

- Requests exceeding the rate limit return HTTP 429 (Too Many Requests)
- Limits are applied per IP address
- Limit values are counted using a sliding window approach

AI Mode Rate Limiting
=====================

AI mode functionality has rate limiting to control LLM API costs and resource consumption.

Configuration
-------------

``app/WEB-INF/conf/system.properties``:

::

    # Enable chat rate limiting
    rag.chat.rate.limit.enabled=true

    # Maximum requests per minute
    rag.chat.rate.limit.requests.per.minute=10

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

Advanced Rate Limiting Configuration
====================================

Custom Rate Limiting
--------------------

To apply different limits for specific users or roles,
custom component implementation is required.

::

    // Custom RateLimitHelper example
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // Custom logic
        }
    }

Burst Limiting
--------------

Configuration that allows short bursts while preventing sustained high load:

::

    # Burst allowance
    api.rate.limit.burst.size=20

    # Sustained limit
    api.rate.limit.sustained.requests.per.second=1

Exclusion Settings
==================

You can exclude specific IP addresses or users from rate limiting.

::

    # Excluded IP addresses (comma-separated)
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # Excluded roles
    api.rate.limit.excluded.roles=admin

Monitoring and Alerts
=====================

Configuration for monitoring rate limiting status:

Log Output
----------

When rate limiting is applied, it is recorded in the logs:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Metrics
-------

Rate limiting metrics can be retrieved via the system statistics API:

::

    GET /api/admin/stats

Troubleshooting
===============

Legitimate Requests Being Blocked
---------------------------------

**Cause**: Limit values are too strict

**Solutions**:

1. Increase ``requests.per.minute``
2. Add specific IPs to the exclusion list
3. Adjust the window size

Rate Limiting Not Working
-------------------------

**Cause**: Configuration is not properly applied

**Check**:

1. Is ``api.rate.limit.enabled=true`` configured?
2. Is the configuration file being read correctly?
3. Has |Fess| been restarted?

Performance Impact
------------------

If rate limiting checks themselves impact performance:

1. Change rate limiting storage to Redis or similar
2. Adjust check frequency

Reference Information
=====================

- :doc:`rag-chat` - AI Mode Configuration
- :doc:`../admin/webconfig-guide` - Web Crawl Configuration Guide
- :doc:`../api/api-overview` - API Overview
