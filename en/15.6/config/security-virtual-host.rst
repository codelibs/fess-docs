============
Virtual Host
============

About Virtual Host
==================

|Fess| can provide different search results based on the hostname (host part of URL) used to access it.
Since search results are displayed in their respective JSPs, designs can also be changed.

System Configuration
--------------------

Configure "Virtual Host" in :doc:`Administrator Guide > General Settings <../admin/general-guide>`. Specify the virtual host name configured here in crawl configuration.

**Format**

::

   Host:hostname[:port number]=virtual host name

.. list-table::

   * - *Hostname*
     - Hostname or IP address that can be name-resolved (DNS) on the system
   * - *Port Number*
     - Optional. Default is 80.
   * - *Virtual Host Name*
     - Virtual host name to specify in crawl configuration

**Example**

::

   Host:abc.example.com:8080=host1
   Host:192.168.1.123:8080=host2

After configuration, search page JSPs are generated in ``WEB-INF/view/virtual host name``.
By editing these, you can also change page designs for each virtual host.


Crawl Configuration
-------------------

Specify "Virtual Host" in web crawl configuration, file crawl configuration, or data store crawl configuration.
"Virtual Host" should be one of the virtual host names configured in system settings.

**Example**

.. list-table::

   * - *Virtual Host*
     - ``host1``
