========================
Port and Network Settings
========================

Overview
========

This section describes network-related configurations for |Fess|.
It covers settings for network connectivity, including port number changes, proxy configurations, and HTTP communication settings.

Port Configuration
==================

Default Ports
-------------

|Fess| uses the following ports by default:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Service
     - Port Number
   * - Fess Web Application
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Changing Fess Web Application Port
-----------------------------------

Configuration on Linux
~~~~~~~~~~~~~~~~~~~~~~

To change the port number on Linux, edit ``bin/fess.in.sh``.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

For example, to use port 80:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   Using port numbers below 1024 requires root privileges or appropriate permission settings (CAP_NET_BIND_SERVICE).

Configuration via Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also specify the port number using environment variables.

::

    export FESS_PORT=8080

For RPM/DEB Packages
~~~~~~~~~~~~~~~~~~~~~

For RPM packages, edit ``/etc/sysconfig/fess``; for DEB packages, edit ``/etc/default/fess``.

::

    FESS_PORT=8080

Configuration on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~

On Windows, edit ``bin\fess.in.bat``.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

Registering as a Windows Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using |Fess| as a Windows service, also modify the port settings in ``bin\service.bat``.
For details, see :doc:`setup-windows-service`.

Context Path Configuration
---------------------------

To publish |Fess| under a subdirectory, you can configure the context path.

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

This configuration makes |Fess| accessible at ``http://localhost:8080/search/``.

.. warning::
   When changing the context path, you must also configure static file paths appropriately.

Proxy Configuration
===================

Overview
--------

When crawling external sites from within an intranet or accessing external APIs,
communications may be blocked by a firewall.
In such environments, you need to configure communication via a proxy server.

Crawler Proxy Configuration
----------------------------

Basic Configuration
~~~~~~~~~~~~~~~~~~~

In the crawl configuration settings on the administration screen, specify the following parameters:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

Authenticated Proxy Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the proxy server requires authentication, add the following:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

Excluding Specific Hosts from Proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To connect to specific hosts (such as intranet servers) without using the proxy:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.nonProxyHosts=localhost|*.local|192.168.*

System-Wide HTTP Proxy Configuration
-------------------------------------

To use an HTTP proxy for the entire |Fess| application, configure it in ``fess_config.properties``.

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   Passwords are stored without encryption. Set appropriate file permissions.

Proxy Configuration via Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When Java libraries such as SSO authentication need to use a proxy, you must configure it via environment variables.
These environment variables are converted to Java system properties (``http.proxyHost``, ``https.proxyHost``, etc.).

::

    FESS_PROXY_HOST=proxy.example.com
    FESS_PROXY_PORT=8080
    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

For RPM packages, configure in ``/etc/sysconfig/fess``. For DEB packages, configure in ``/etc/default/fess``.

.. note::
   The ``http.proxy.*`` settings in ``fess_config.properties`` are used for HTTP communications within Fess.
   If external Java libraries such as SSO authentication need to use a proxy, also configure the environment variables above.

HTTP Communication Settings
===========================

File Upload Limits
------------------

You can limit file upload sizes from the administration screen.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Configuration Item
     - Description
   * - ``http.fileupload.max.size``
     - Maximum file upload size (Default: 262144000 bytes = 250MB)
   * - ``http.fileupload.threshold.size``
     - Threshold size to keep in memory (Default: 262144 bytes = 256KB)
   * - ``http.fileupload.max.file.count``
     - Maximum number of files that can be uploaded at once (Default: 10)

Configuration example in ``fess_config.properties``:

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

Connection Timeout Settings
----------------------------

You can configure connection timeouts to OpenSearch.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Configuration Item
     - Description
   * - ``search_engine.http.url``
     - OpenSearch URL (Default: http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - Health check interval in milliseconds (Default: 10000)

Changing OpenSearch Connection
-------------------------------

To connect to an external OpenSearch cluster:

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

Connecting to Multiple Nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To connect to multiple OpenSearch nodes, specify them separated by commas.

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

SSL/TLS Connection Configuration
---------------------------------

To connect to OpenSearch via HTTPS:

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   To verify certificates, specify the path to the CA certificate in ``certificate_authorities``.

Virtual Host Configuration
==========================

Overview
--------

|Fess| can provide different search results based on the hostname used to access it.
For details, see :doc:`security-virtual-host`.

Basic Configuration
-------------------

Configure virtual host headers in ``fess_config.properties``.

::

    virtual.host.headers=X-Forwarded-Host,Host

Reverse Proxy Integration
==========================

Nginx Configuration Example
----------------------------

::

    server {
        listen 80;
        server_name search.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Apache Configuration Example
-----------------------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

SSL/TLS Termination
-------------------

Configuration example for SSL/TLS termination at the reverse proxy (Nginx):

::

    server {
        listen 443 ssl http2;
        server_name search.example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }
    }

Firewall Configuration
======================

Opening Required Ports
-----------------------

To make |Fess| accessible from external networks, open the following ports:

**iptables configuration example:**

::

    # Fess web application
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # For HTTPS access (via reverse proxy)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**firewalld configuration example:**

::

    # Fess web application
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

Security Group Configuration (Cloud Environments)
--------------------------------------------------

In cloud environments such as AWS, GCP, and Azure, open the appropriate ports
using security groups or network ACLs.

Recommended settings:
- Inbound: Ports 80/443 (via HTTP reverse proxy)
- Restrict port 8080 to internal access only
- Restrict OpenSearch ports 9201/9301 to internal access only

Troubleshooting
===============

Cannot Access After Changing Port
----------------------------------

1. Verify that |Fess| has been restarted.
2. Confirm that the port is open in the firewall.
3. Check for errors in the log file (``fess.log``).

Cannot Crawl via Proxy
-----------------------

1. Verify that the proxy server hostname and port are correct.
2. If the proxy server requires authentication, configure the username and password.
3. Check the proxy server logs to see if connection attempts are recorded.
4. Verify that the ``nonProxyHosts`` setting is appropriate.

Cannot Connect to OpenSearch
-----------------------------

1. Verify that OpenSearch is running.
2. Confirm that the ``search_engine.http.url`` setting is correct.
3. Verify network connectivity: ``curl http://localhost:9201``
4. Check OpenSearch logs for errors.

Not Working Properly When Accessed via Reverse Proxy
-----------------------------------------------------

1. Verify that the ``X-Forwarded-Host`` header is configured correctly.
2. Verify that the ``X-Forwarded-Proto`` header is configured correctly.
3. Verify that the context path is configured correctly.
4. Check reverse proxy logs for errors.

References
==========

- :doc:`setup-memory` - Memory Configuration
- :doc:`setup-windows-service` - Windows Service Configuration
- :doc:`security-virtual-host` - Virtual Host Configuration
- :doc:`crawler-advanced` - Advanced Crawler Configuration
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
