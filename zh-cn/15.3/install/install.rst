====================
选择安装方法
====================

本页面说明 |Fess| 安装方法的概述。
请根据您的环境选择适当的安装方法。

.. warning::

   **生产环境的重要注意事项**

   在生产环境或负载测试等场景中，不推荐使用内嵌 OpenSearch 运行。
   请务必构建外部的 OpenSearch 服务器。

确认前提条件
============

开始安装之前，请确认系统要求。

详情请参阅 :doc:`prerequisites`。

安装方法对比
====================

|Fess| 可以通过以下方法安装。请根据您的环境和用途进行选择。

.. list-table::
   :header-rows: 1
   :widths: 15 25 30 30

   * - 方法
     - 目标操作系统
     - 推荐用途
     - 详细文档
   * - Docker
     - Linux, Windows, macOS
     - 开发・评估环境、快速设置
     - :doc:`install-docker`
   * - TAR.GZ
     - Linux, macOS
     - 需要定制化的环境
     - :doc:`install-linux`
   * - RPM
     - RHEL, CentOS, Fedora
     - 生产环境（基于 RPM）
     - :doc:`install-linux`
   * - DEB
     - Debian, Ubuntu
     - 生产环境（基于 DEB）
     - :doc:`install-linux`
   * - ZIP
     - Windows
     - Windows 环境的开发・生产
     - :doc:`install-windows`

各安装方法的特点
======================

Docker 版
--------

**优点:**

- 设置最快速
- 无需管理依赖关系
- 最适合开发环境的构建
- 容器启动・停止简便

**缺点:**

- 需要 Docker 知识

**推荐环境:** 开发环境、评估环境、POC、生产环境

详情: :doc:`install-docker`

Linux 包版 (TAR.GZ/RPM/DEB)
---------------------------------

**优点:**

- 原生环境的高性能
- 可作为系统服务管理（RPM/DEB）
- 可进行细致的定制化

**缺点:**

- 需要手动安装 Java 和 OpenSearch
- 配置较为繁琐

**推荐环境:** 生产环境、需要定制化的环境

详情: :doc:`install-linux`

Windows 版 (ZIP)
---------------

**优点:**

- 在 Windows 原生环境中运行
- 无需安装程序

**缺点:**

- 需要手动安装 Java 和 OpenSearch
- 配置较为繁琐

**推荐环境:** Windows 环境的开发・评估、Windows Server 的生产运维

详情: :doc:`install-windows`

安装的基本流程
========================

所有安装方法的基本流程相同。

1. **确认系统要求**

   参阅 :doc:`prerequisites`，确认满足系统要求。

2. **下载软件**

   从 `下载站点 <https://fess.codelibs.org/ja/downloads.html>`__ 下载 |Fess|。

   Docker 版的情况下，获取 Docker Compose 文件。

3. **设置 OpenSearch**

   Docker 版以外的情况下，需要单独设置 OpenSearch。

   - 安装 OpenSearch 3.3.2
   - 安装必需插件
   - 编辑配置文件

4. **设置 Fess**

   - 安装 Fess
   - 编辑配置文件（OpenSearch 的连接信息等）

5. **启动和确认**

   - 启动服务
   - 在浏览器中访问并确认运行

   详情请参阅 :doc:`run`。

必需组件
==================

运行 |Fess| 需要以下组件。

Fess 本体
--------

全文搜索系统的主体。提供 Web 界面、爬虫、索引器等功能。

OpenSearch
----------

使用 OpenSearch 作为搜索引擎。

- **支持版本**: OpenSearch 3.3.2
- **必需插件**:

  - opensearch-analysis-fess
  - opensearch-analysis-extension
  - opensearch-minhash
  - opensearch-configsync

.. important::

   OpenSearch 的版本与插件的版本必须一致。
   版本不一致可能导致启动错误或意外行为。

Java (Docker 版除外)
-------------------

TAR.GZ/ZIP/RPM/DEB 版需要 Java 21 或更高版本。

- 推荐: `Eclipse Temurin <https://adoptium.net/temurin>`__
- 也可使用 OpenJDK 21 或更高版本

.. note::

   Docker 版的情况下，Java 已包含在 Docker 镜像中，无需单独安装。

下一步
==========

确认系统要求后，请选择适当的安装方法。

1. :doc:`prerequisites` - 确认系统要求
2. 选择安装方法:

   - :doc:`install-docker` - 使用 Docker 安装
   - :doc:`install-linux` - 在 Linux 上安装
   - :doc:`install-windows` - 在 Windows 上安装

3. :doc:`run` - |Fess| 的启动和初始设置
4. :doc:`security` - 安全配置（生产环境）

常见问题
==========

Q: OpenSearch 是必需的吗？
--------------------------

A: 是的，是必需的。|Fess| 使用 OpenSearch 作为搜索引擎。
Docker 版会自动设置，但其他方法需要手动安装。

Q: 可以从旧版本升级吗？
----------------------------------------------

A: 可以。详情请参阅 :doc:`upgrade`。

Q: 可以使用多个服务器构成吗？
---------------------------------

A: 可以。Fess 和 OpenSearch 可以在不同的服务器上运行。
此外，通过将 OpenSearch 配置为集群，可以提高可用性和性能。

下载
==========

|Fess| 及相关组件可从以下位置下载：

- **Fess**: `下载站点 <https://fess.codelibs.org/ja/downloads.html>`__
- **OpenSearch**: `Download OpenSearch <https://opensearch.org/downloads.html>`__
- **Java (Adoptium)**: `Adoptium <https://adoptium.net/>`__
- **Docker**: `Get Docker <https://docs.docker.com/get-docker/>`__

版本信息
============

本文档适用于以下版本：

- **Fess**: 15.3.2
- **OpenSearch**: 3.3.2
- **Java**: 21 或更高版本
- **Docker**: 20.10 或更高版本
- **Docker Compose**: 2.0 或更高版本

关于旧版本的文档，请参阅各版本的文档。
