:canonical: security-virtual-host

============
Virtual Host
============

About Virtual Host
==================

You can differentiate search results based on the hostname (URL's host part) when accessing Fess. A static theme whose name matches the virtual host name is used for that host, so you can also customize the design.

System Configuration
--------------------

Configure the "Virtual Host" in the :doc:`Administrator's Guide > General Settings <../admin/general-guide>`. Specify the configured virtual host name in the crawl settings.

**Format**

::

   Host:hostname[:port]=virtual_host_name

.. list-table::

   * - *hostname*
     - A hostname or IP address that can be resolved (DNS) on the system.
   * - *port*
     - Optional. The default is 80.
   * - *virtual_host_name*
     - The virtual host name specified in the crawl settings.

**Example**

::  

   Host:abc.example.com:8080=host1
   Host:192.168.1.123:8080=host2

To customize the page design for a virtual host, install a static theme whose name is the virtual host name in lowercase. See :doc:`security-virtual-host` for details.


Crawl Configuration
-------------------

Specify the "Virtual Host" in the web crawl settings, file crawl settings, or data store crawl settings. The "Virtual Host" should match one of the virtual host names configured in the system settings.

**Example**

.. list-table::

   * - *Virtual Host*
     - ``host1``
