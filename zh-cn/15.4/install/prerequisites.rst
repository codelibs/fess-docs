============
系统要求
============

本页面说明运行 |Fess| 所需的硬件和软件要求。

硬件要求
==============

最低要求
--------

以下是评估和开发环境的最低要求：

- CPU: 2核或以上
- 内存: 4GB或以上
- 磁盘空间: 10GB或以上的可用空间

推荐配置
--------

对于生产环境，推荐以下配置：

- CPU: 4核或以上
- 内存: 8GB或以上（根据索引大小进行扩展）
- 磁盘空间:

  - 系统空间: 20GB或以上
  - 数据空间: 索引大小的3倍或以上（包含副本）

- 网络: 1Gbps或以上

.. note::

   如果索引大小较大或需要进行高频率爬取，请适当增加内存和磁盘空间。

软件要求
==============

操作系统
--------------------

|Fess| 可在以下操作系统上运行：

**Linux**

- Red Hat Enterprise Linux 8 或更高版本
- CentOS 8 或更高版本
- Ubuntu 20.04 LTS 或更高版本
- Debian 11 或更高版本
- 其他 Linux 发行版（可运行 Java 21 的环境）

**Windows**

- Windows Server 2019 或更高版本
- Windows 10 或更高版本

**其他**

- macOS 11 (Big Sur) 或更高版本（仅推荐用于开发环境）
- 可运行 Docker 的环境

必需软件
--------------

根据安装方法的不同，需要以下软件：

TAR.GZ/ZIP/RPM/DEB 版
~~~~~~~~~~~~~~~~~~~~

- **Java 21**: 推荐使用 `Eclipse Temurin <https://adoptium.net/temurin>`__

  - OpenJDK 21 或更高版本
  - Eclipse Temurin 21 或更高版本

- **OpenSearch 3.3.2**: 生产环境必需（不推荐使用内嵌版本）

  - 支持版本: OpenSearch 3.3.2
  - 其他版本需要注意插件兼容性

Docker 版
~~~~~~~~~

- **Docker**: 20.10 或更高版本
- **Docker Compose**: 2.0 或更高版本

网络要求
==============

所需端口
----------

|Fess| 使用的主要端口如下：

.. list-table::
   :header-rows: 1
   :widths: 15 15 50

   * - 端口
     - 协议
     - 用途
   * - 8080
     - HTTP
     - |Fess| Web 界面（搜索页面・管理页面）
   * - 9200
     - HTTP
     - OpenSearch HTTP API（|Fess| 与 OpenSearch 的通信）
   * - 9300
     - TCP
     - OpenSearch 传输通信（集群配置时）

.. warning::

   在生产环境中，强烈建议限制外部对端口 9200 和 9300 的直接访问。
   这些端口应仅用于 |Fess| 与 OpenSearch 之间的内部通信。

防火墙设置
------------------

如果要从外部访问 |Fess|，需要开放端口 8080。

**Linux (使用 firewalld)**

::

    $ sudo firewall-cmd --permanent --add-port=8080/tcp
    $ sudo firewall-cmd --reload

**Linux (使用 iptables)**

::

    $ sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    $ sudo iptables-save

浏览器要求
============

对于 |Fess| 的管理页面和搜索页面，推荐使用以下浏览器：

- Google Chrome（最新版）
- Mozilla Firefox（最新版）
- Microsoft Edge（最新版）
- Safari（最新版）

.. note::

   不支持 Internet Explorer。

安装前检查清单
====================

安装前，请确认以下项目：

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 检查项目
     - 状态
   * - 是否满足硬件要求
     - □
   * - 是否已安装 Java 21（Docker 版除外）
     - □
   * - 是否已安装 Docker（Docker 版）
     - □
   * - 所需端口是否可用
     - □
   * - 防火墙设置是否合适
     - □
   * - 磁盘空间是否充足
     - □
   * - 网络连接是否正常（如需爬取外部网站）
     - □

下一步
==========

确认系统要求后，请根据您的环境进行相应的安装：

- :doc:`install-linux` - Linux (TAR.GZ/RPM/DEB) 安装
- :doc:`install-windows` - Windows (ZIP) 安装
- :doc:`install-docker` - Docker 安装
- :doc:`install` - 安装方法概述
