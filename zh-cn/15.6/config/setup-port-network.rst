======================
端口与网络配置
======================

概述
====

本章节介绍 |Fess| 的网络相关配置。
包括端口号变更、代理服务器配置、HTTP通信配置等网络连接相关设置。

使用端口配置
================

默认端口
----------------

|Fess| 默认使用以下端口。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 服务
     - 端口号
   * - Fess Web 应用程序
     - 8080
   * - OpenSearch (HTTP)
     - 9201
   * - OpenSearch (Transport)
     - 9301

Fess Web 应用程序端口变更
--------------------------------------

Linux 环境配置
~~~~~~~~~~~~~~~~~

在 Linux 环境中变更端口号时,请编辑 ``bin/fess.in.sh`` 文件。

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=8080"

例如,要使用端口 80:

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.port=80"

.. note::
   使用 1024 以下的端口号时,需要 root 权限或适当的权限设置(CAP_NET_BIND_SERVICE)。

环境变量配置
~~~~~~~~~~~~~~~~~~

也可以通过环境变量指定端口号。

::

    export FESS_PORT=8080

RPM/DEB 软件包配置
~~~~~~~~~~~~~~~~~~~~~~~~

RPM 软件包请编辑 ``/etc/sysconfig/fess``,DEB 软件包请编辑 ``/etc/default/fess``。

::

    FESS_PORT=8080

Windows 环境配置
~~~~~~~~~~~~~~~~~~~

在 Windows 环境中,请编辑 ``bin\fess.in.bat`` 文件。

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=8080

注册为 Windows 服务时
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在 Windows 环境中作为服务注册使用时,请同时变更 ``bin\service.bat`` 中的端口配置。
详情请参阅 :doc:`setup-windows-service`。

上下文路径配置
----------------------

要在子目录中发布 |Fess|,可以配置上下文路径。

::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.context.path=/search"

此配置将使您可以通过 ``http://localhost:8080/search/`` 访问。

.. warning::
   变更上下文路径后,还需要正确配置静态文件的路径。

代理服务器配置
============

概述
----

当从内网爬取外部网站或访问外部 API 时,
通信可能会被防火墙阻止。
在这种环境中,需要配置通过代理服务器进行通信。

爬虫代理服务器配置
--------------------------

基本配置
~~~~~~~~

在管理页面的爬虫配置中,在配置参数中指定如下内容。

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080

需要认证的代理服务器配置
~~~~~~~~~~~~~~~~~~~~~~~~~~

如果代理服务器需要认证,请添加如下配置。

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.proxyUsername=proxyuser
    client.proxyPassword=proxypass

从代理服务器排除特定主机
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当需要直连特定主机(如内网服务器)而不通过代理服务器时:

::

    client.proxyHost=proxy.example.com
    client.proxyPort=8080
    client.nonProxyHosts=localhost|*.local|192.168.*

系统全局 HTTP 代理配置
------------------------------

如果 |Fess| 应用程序整体都使用 HTTP 代理,请在 ``fess_config.properties`` 中配置。

::

    http.proxy.host=proxy.example.com
    http.proxy.port=8080
    http.proxy.username=proxyuser
    http.proxy.password=proxypass

.. warning::
   密码将以未加密形式保存。请设置适当的文件权限。

通过环境变量配置代理
~~~~~~~~~~~~~~~~~~~~

当 Java 库(如 SSO 认证)需要使用代理时,必须通过环境变量进行配置。
这些环境变量会被转换为 Java 系统属性(``http.proxyHost``、``https.proxyHost`` 等)。

::

    FESS_PROXY_HOST=proxy.example.com
    FESS_PROXY_PORT=8080
    FESS_NON_PROXY_HOSTS=localhost|*.local|192.168.*

对于 RPM 包,在 ``/etc/sysconfig/fess`` 中配置。对于 DEB 包,在 ``/etc/default/fess`` 中配置。

.. note::
   ``fess_config.properties`` 中的 ``http.proxy.*`` 设置用于 Fess 内部的 HTTP 通信。
   如果外部 Java 库(如 SSO 认证)需要使用代理,还需要配置上述环境变量。

HTTP 通信配置
============

文件上传限制
--------------------------

可以限制从管理页面上传文件的大小。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 配置项
     - 说明
   * - ``http.fileupload.max.size``
     - 最大文件上传大小(默认: 262144000字节 = 250MB)
   * - ``http.fileupload.threshold.size``
     - 内存保留阈值大小(默认: 262144字节 = 256KB)
   * - ``http.fileupload.max.file.count``
     - 一次可上传的文件数(默认: 10)

``fess_config.properties`` 配置示例:

::

    http.fileupload.max.size=524288000
    http.fileupload.threshold.size=524288
    http.fileupload.max.file.count=20

连接超时配置
--------------------

可以配置到 OpenSearch 的连接超时时间。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 配置项
     - 说明
   * - ``search_engine.http.url``
     - OpenSearch的URL(默认: http://localhost:9201)
   * - ``search_engine.heartbeat_interval``
     - 健康检查间隔(毫秒,默认: 10000)

OpenSearch 连接目标变更
----------------------

连接到外部 OpenSearch 集群时:

::

    search_engine.http.url=http://opensearch-cluster.example.com:9200

连接多个节点
~~~~~~~~~~~~~~~~~~

连接多个 OpenSearch 节点时,请用逗号分隔指定。

::

    search_engine.http.url=http://node1:9200,http://node2:9200,http://node3:9200

SSL/TLS 连接配置
-----------------

通过 HTTPS 连接到 OpenSearch 时:

::

    search_engine.http.url=https://opensearch.example.com:9200
    search_engine.http.ssl.certificate_authorities=/path/to/ca.crt
    search_engine.username=admin
    search_engine.password=admin_password

.. note::
   进行证书验证时,请在 ``certificate_authorities`` 中指定 CA 证书的路径。

虚拟主机配置
==============

概述
----

可以根据访问 |Fess| 的主机名显示不同的搜索结果。
详情请参阅 :doc:`security-virtual-host`。

基本配置
--------

在 ``fess_config.properties`` 中配置虚拟主机头。

::

    virtual.host.headers=X-Forwarded-Host,Host

反向代理集成
========================

Nginx 配置示例
--------------

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

Apache 配置示例
---------------

::

    <VirtualHost *:80>
        ServerName search.example.com

        ProxyPreserveHost On
        ProxyPass / http://localhost:8080/
        ProxyPassReverse / http://localhost:8080/

        RequestHeader set X-Forwarded-Proto "http"
        RequestHeader set X-Forwarded-Host "search.example.com"
    </VirtualHost>

SSL/TLS 终止
-----------

在反向代理上进行 SSL/TLS 终止的配置示例(Nginx):

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

防火墙配置
====================

开放必要端口
------------------

要使 |Fess| 可从外部访问,请开放以下端口。

**iptables 配置示例:**

::

    # Fess Web 应用程序
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

    # 通过 HTTPS 访问时(经由反向代理)
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT

**firewalld 配置示例:**

::

    # Fess Web 应用程序
    firewall-cmd --permanent --add-port=8080/tcp
    firewall-cmd --reload

安全组配置(云环境)
------------------------------------------

在 AWS、GCP、Azure 等云环境中,请在安全组或网络 ACL 中
开放适当的端口。

推荐配置:
- 入站: 80/443端口(通过 HTTP 反向代理)
- 8080端口仅限从内部访问
- OpenSearch 的 9201/9301 端口仅限从内部访问

故障排除
======================

变更端口后无法访问
------------------------------

1. 请确认是否已重启 |Fess|。
2. 请确认防火墙是否已开放相应端口。
3. 请在日志文件(``fess.log``)中确认错误信息。

无法通过代理服务器爬取
------------------------------

1. 请确认代理服务器的主机名和端口是否正确。
2. 如代理服务器需要认证,请配置用户名和密码。
3. 请在代理服务器日志中确认是否记录了连接尝试。
4. 请确认 ``nonProxyHosts`` 的配置是否正确。

无法连接到 OpenSearch
-------------------------

1. 请确认 OpenSearch 是否已启动。
2. 请确认 ``search_engine.http.url`` 的配置是否正确。
3. 请确认网络连接: ``curl http://localhost:9201``
4. 请在 OpenSearch 日志中确认错误信息。

通过反向代理访问时无法正常工作
----------------------------------------------------

1. 请确认 ``X-Forwarded-Host`` 头是否配置正确。
2. 请确认 ``X-Forwarded-Proto`` 头是否配置正确。
3. 请确认上下文路径是否配置正确。
4. 请在反向代理日志中确认错误信息。

参考信息
========

- :doc:`setup-memory` - 内存配置
- :doc:`setup-windows-service` - Windows 服务配置
- :doc:`security-virtual-host` - 虚拟主机配置
- :doc:`crawler-advanced` - 爬虫高级配置
- `OpenSearch Configuration <https://opensearch.org/docs/latest/install-and-configure/configuration/>`_
