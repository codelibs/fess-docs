============
Virtual Host
============

About Virtual Host
==================

|Fess| can serve different search results depending on the hostname (the value of the HTTP ``Host`` header) used to access it.
A single |Fess| server can be published under multiple hostnames, providing a different set of crawl targets and page design for each hostname.
Search results are displayed using per-virtual-host JSPs, so the design can be customised for each host.

The virtual host feature is disabled (unconfigured) by default. Configure it using the steps below.

System Configuration
--------------------

In :doc:`Administrator Guide > General Settings <../admin/general-guide>`, set the mapping between the requesting hostname and the virtual host name under "Virtual Host". Specify the virtual host name configured here in the crawl configuration.

**Format**

Specify one virtual host per line using the following format.

::

   header_name:header_value=virtual_host_name

.. list-table::

   * - *header_name*
     - The name of the HTTP request header used for matching. Normally specify ``Host``. When accessing via a reverse proxy, you can also specify ``X-Forwarded-Host``.
   * - *header_value*
     - The hostname contained in the above header (in the form ``hostname:port`` if necessary). The virtual host is applied when this value exactly matches the value of the header sent by the client at access time (case-insensitive).
   * - *virtual_host_name*
     - The virtual host name to specify in the crawl configuration

**Example**

::

   Host:abc.example.com=host1
   Host:192.168.1.123:8080=host2

.. note::

   Matching is performed by string comparison against the request header value, not by hostname resolution (DNS).
   The ``Host`` header sent by the browser does not include the port number when accessing via a standard port (80 for HTTP, 443 for HTTPS), but does include it in the form ``hostname:port`` when accessing via any other port.
   Therefore, when publishing on a non-standard port, specify the port number explicitly, for example ``Host:abc.example.com:8080=host1``.

.. note::

   Only alphanumeric characters and underscores ( ``a-z`` , ``A-Z`` , ``0-9`` , ``_`` ) can be used in virtual host names.
   Other characters are automatically removed.

   The following names are reserved and cannot be used as virtual host names:
   ``admin`` , ``common`` , ``error`` , ``login`` , ``profile``

After saving the configuration, search page JSPs are generated under ``WEB-INF/view/virtual_host_name``.
By editing these files you can change the page design for each virtual host. The JSPs can also be edited from the :doc:`Administrator Guide > Design <../admin/design-guide>` screen.


Crawl Configuration
-------------------

Specify "Virtual Host" in web crawl configuration, file crawl configuration, or data store crawl configuration.
"Virtual Host" should be one of the virtual host names configured in the system settings. You can specify multiple virtual hosts for a single crawl configuration (one per line).

Searches made from a matched virtual host will only display documents belonging to crawl configurations that have that virtual host assigned.
Accesses that do not match any virtual host (normal access with no virtual host configured) are not filtered, and all search results are returned as usual.

**Example**

.. list-table::

   * - *Virtual Host*
     - ``host1``
