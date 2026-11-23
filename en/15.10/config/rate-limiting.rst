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

``app/WEB-INF/classes/fess_config.properties``:

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
- Requests from IPs blocked for exceeding the limit, and from IPs on the blocked IP list, return HTTP 403 (Forbidden)
- The response body is JSON (``{"error":"rate_limit_exceeded",...,"retry_after":60}`` for 429, ``{"error":"ip_blocked",...}`` for 403). A 429 response has a ``Retry-After`` header
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

robots.txt handling is controlled by ``crawler.ignore.robots.txt`` in
``app/WEB-INF/classes/fess_config.properties`` (default: ``false``).
Setting it to ``true`` disables robots.txt handling, including Crawl-delay.

::

    # Ignore robots.txt (default: false)
    crawler.ignore.robots.txt=false

Crawl-delay applies per origin and is capped at 60 seconds. It paces URLs, not requests, so in an
incremental crawl the HEAD and the GET of one URL are sent back to back. The interval of a crawl
configuration still works separately, as the wait before the next URL.

robots.txt is interpreted according to RFC 9309. Between ``Allow:`` and ``Disallow:``, the longest
matching rule wins, and the start URLs are checked against robots.txt too. A URL that robots.txt
disallows is logged at INFO in ``fess-crawler.log`` and is not recorded as a failure URL.

Request-rate
------------

From 15.10, |Fess| also honors the ``Request-rate`` and ``Visit-time`` lines of robots.txt (up to 15.9 they were ignored). Neither is part of RFC 9309: both come from the `extended robots exclusion proposal <https://www.conman.org/people/spc/robots2.html>`__, and SeznamBot also uses Request-rate (`Seznam documentation <https://www.napoveda.seznam.cz/en/crawling-control>`__). Like Crawl-delay, they apply only while robots.txt handling is on: ``crawler.ignore.robots.txt=true`` turns off all three, and there is no setting for one of them alone. They are not ``Allow:`` or ``Disallow:`` rules: they never end a ``User-agent`` group and never change which URLs are disallowed.

``Request-rate: <documents>/<time>[ unit]`` asks a crawler to fetch no more than that many documents in that time. The unit of the time is ``s`` (seconds, the default), ``m``, ``h`` or ``d``. For example:

- ``1/10``: one page per 10 seconds
- ``10/10m``: ten pages per 10 minutes
- ``20/1h``: twenty pages per hour
- ``100/15 m``: one hundred pages per 15 minutes

|Fess| converts the rate into the interval between two URLs (``1/10`` is 10 seconds, ``5/1m`` is 12 seconds) and, for each origin, waits for the longer of the Crawl-delay and the Request-rate interval before the next URL. The upper limit of 60 seconds applies to this wait as well, so a slower rate such as ``1/1h`` is clamped to 60 seconds. Request-rate paces URLs; it is not a burst budget. As with Crawl-delay, the first URL of an origin is not paced, because robots.txt is read while it is fetched, and in an incremental crawl the HEAD and the GET of one URL are sent back to back.

A time of day can follow the rate. The rate then applies only in that time of day; outside it, Request-rate sets no limit (Crawl-delay still applies):

::

    User-agent: *
    Request-rate: 1/10 s 1800-1900

Times are UT/GMT (UTC) from 00:00 to 23:59, written ``HHMM-HHMM`` or ``HH:MM-HH:MM``, and both ends are included. A range may cross midnight (``2300-0100``). When there are several Request-rate lines, all of them are honored, and the slowest one that is active at that moment applies. A malformed rate or time of day (for example an hour over 23 or a minute over 59) is ignored.

Visit-time
----------

``Visit-time: HH:MM-HH:MM`` (``HHMM-HHMM`` is accepted too) asks a crawler to visit the site only in that time of day, in UTC and with both ends included. Several lines are allowed, and the permitted time of day is the union of them.

::

    User-agent: *
    Visit-time: 02:00-06:00

|Fess| does not wait for the window to open, because that would hold a crawl thread for hours. A URL of the origin that is dequeued outside the window is skipped, like a URL that ``Disallow:`` forbids: it is logged at INFO once per origin, it is not put back into the queue (it is not retried later in the same crawl), and it is not counted as a failure. The crawl therefore has to start inside the window. A start URL that is dequeued before the window opens is lost for that crawl, even if the crawl is still running when the window opens. A malformed Visit-time line is ignored, which means no restriction.

If the crawl job of a site that declares Visit-time never runs inside the window, the site is not crawled and its indexed documents are not refreshed. With the default "Delete old documents" setting (``day.for.cleanup``, 3 days), they expire about 3 days after the last crawl that reached them, as they do when a site is down. Schedule the crawl job inside the window.

Backoff after 429/503 responses
-------------------------------

When a server answers ``429 Too Many Requests`` or ``503 Service Unavailable``, |Fess| pauses
requests to that origin and retries the URL up to three times. The wait is the ``Retry-After``
header when it is present, otherwise an exponential wait that starts at 10 seconds (up to 5
minutes). When the last retry fails too, a WARN is written to ``fess-crawler.log``.

When robots.txt cannot be fetched
---------------------------------

When fetching robots.txt fails with a 5xx, a 429 or a timeout, the URLs of that origin are put back
into the queue until the backoff ends. If three retries after the first failure also fail, no URL of
that origin is crawled for the rest of the crawl, and one WARN is written to ``fess-crawler.log``.
Up to 15.8, a robots.txt that could not be fetched meant "allow all". To restore that behavior,
set the following in the "Config Parameters" of the web crawl configuration:

::

    client.robotsTxtAllowOnUnavailable=true

To turn robots.txt handling off entirely, use ``client.robotsTxtEnabled=false`` (per crawl
configuration) or ``crawler.ignore.robots.txt=true``.

All Rate Limiting Properties
============================

All properties configurable in ``app/WEB-INF/classes/fess_config.properties``.

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
     - Trusted proxy IPs (for X-Forwarded-For/X-Real-IP resolution; also used for the client IP in the audit log and search log)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Cleanup interval (number of requests, reserved)
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` is a setting reserved for future use.
   In the current implementation, the request counters and blocked IP information
   are cleaned up automatically based on the internal cache expiration
   (``rate.limit.window.ms`` and ``rate.limit.block.duration.ms``),
   so this value is not used.

Login Rate Limit
================

Login has its own rate limit, separate from the one above, configured with ``theme.api.login.*``.
From 15.10, ``/api/v2/auth/login`` and the login form on the login screen (``/login/``) share the same limit and lockout.
Each attempt consumes one slot of the per-minute quota of the client IP (default ``10``), and the slot is returned when the login succeeds.
When attempts from the same IP address exceed the limit, that IP address is locked out for ``theme.api.login.lockout.seconds`` (default ``900``) seconds, and during that time even correct credentials cannot log in.
As a result, if more attempts than the limit (for example, simultaneous logins) come from the same IP address before one succeeds, that address is locked out.
The per-user limit (``theme.api.login.rate.limit.per.user.per.minute``) is counted for each pair of client IP address and user name. User names are compared without regard to case, so ``alice`` and ``Alice`` share one count. The user name used for authentication and written to the logs is the one that was typed.
See :doc:`../api/api-auth` for details.

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
   When X-Forwarded-For is split over several header lines (for example when a proxy adds
   a line of its own, as HAProxy's ``option forwardfor`` does), 15.10 and later join all the
   lines in the order received, read the chain from the right, and use the first address that
   is not a trusted proxy as the client IP. Up to 15.9 only the first line, which is the one
   the client sent, was read.

Monitoring and Alerts
=====================

Configuration for monitoring rate limiting status:

Log Output
----------

When rate limiting is applied, it is recorded in the logs:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

The message is logged at INFO, so it is not written at the default log level (``warn``). Add the ``Logger`` above to ``log4j2.xml`` (for its location, see :doc:`admin-logging`) or set ``FESS_LOG_LEVEL`` to ``info``.

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
