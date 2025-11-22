==================================
在 Linux 上安装（详细步骤）
==================================

本页面说明在 Linux 环境中安装 |Fess| 的步骤。
支持 TAR.GZ、RPM、DEB 各种包格式。

.. warning::

   在生产环境中，不推荐使用内嵌 OpenSearch 运行。
   请务必构建外部的 OpenSearch 服务器。

前提条件
========

- 满足 :doc:`prerequisites` 中描述的系统要求
- 已安装 Java 21
- OpenSearch 3.3.2 可用（或新安装）

选择安装方法
====================

在 Linux 环境中，可以从以下安装方法中选择：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 方式
     - 推荐环境
     - 特点
   * - TAR.GZ
     - 开发环境、需要定制化的环境
     - 可解压到任意目录
   * - RPM
     - RHEL、CentOS、Fedora 系
     - 可通过 systemd 进行服务管理
   * - DEB
     - Debian、Ubuntu 系
     - 可通过 systemd 进行服务管理

使用 TAR.GZ 版安装
========================

步骤 1: 安装 OpenSearch
----------------------------------

1. 下载 OpenSearch

   从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 TAR.GZ 版。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.tar.gz
       $ tar -xzf opensearch-3.3.2-linux-x64.tar.gz
       $ cd opensearch-3.3.2

   .. note::

      此示例使用 OpenSearch 3.3.2。
      请确认 |Fess| 支持的版本。

2. 安装 OpenSearch 插件

   安装 |Fess| 所需的插件。

   ::

       $ cd /path/to/opensearch-3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

   .. important::

      插件版本必须与 OpenSearch 版本一致。
      在上述示例中，所有版本都指定为 3.3.2。

3. 配置 OpenSearch

   在 ``config/opensearch.yml`` 中添加以下配置。

   ::

       # 配置同步路径（使用绝对路径指定）
       configsync.config_path: /path/to/opensearch-3.3.2/data/config/

       # 禁用安全插件（仅限开发环境）
       plugins.security.disabled: true

   .. warning::

      **关于安全的重要注意事项**

      ``plugins.security.disabled: true`` 仅应在开发环境或测试环境中使用。
      在生产环境中，应启用 OpenSearch 的安全插件并进行适当的认证和授权配置。
      详情请参阅 :doc:`security`。

   .. tip::

      请根据环境调整集群名称和网络设置等其他配置。
      配置示例::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

步骤 2: 安装 Fess
-----------------------------

1. 下载和解压 Fess

   从 `下载站点 <https://fess.codelibs.org/downloads.html>`__ 下载 TAR.GZ 版。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz
       $ cd fess-15.3.2

2. 配置 Fess

   编辑 ``bin/fess.in.sh``，设置到 OpenSearch 的连接信息。

   ::

       $ vi bin/fess.in.sh

   添加或更改以下配置::

       # OpenSearch 的 HTTP 端点
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200

       # 字典文件的放置路径（与 OpenSearch 的 configsync.config_path 相同）
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.3.2/data/config/

   .. note::

      如果 OpenSearch 在其他主机上运行，请将
      ``SEARCH_ENGINE_HTTP_URL`` 更改为适当的主机名或 IP 地址。
      例: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``

3. 确认安装

   确认配置文件已正确编辑::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

步骤 3: 启动
--------------

关于启动步骤，请参阅 :doc:`run`。

使用 RPM 版安装
====================

RPM 版用于 Red Hat Enterprise Linux、CentOS、Fedora 等基于 RPM 的 Linux 发行版。

步骤 1: 安装 OpenSearch
----------------------------------

1. 下载和安装 OpenSearch RPM

   从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 RPM 包并安装。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.3.2-linux-x64.rpm

   或者，也可以添加仓库后进行安装。
   详情请参阅 `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__。

2. 安装 OpenSearch 插件

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. 配置 OpenSearch

   在 ``/etc/opensearch/opensearch.yml`` 中添加以下配置。

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   要添加的配置::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      在生产环境中不要使用 ``plugins.security.disabled: true``。
      请参阅 :doc:`security` 进行适当的安全配置。

步骤 2: 安装 Fess
-----------------------------

1. 安装 Fess RPM

   从 `下载站点 <https://fess.codelibs.org/downloads.html>`__ 下载 RPM 包并安装。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.rpm
       $ sudo rpm -ivh fess-15.3.2.rpm

2. 配置 Fess

   编辑 ``/usr/share/fess/bin/fess.in.sh``。

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   添加或更改以下配置::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. 注册服务

   **使用 chkconfig 的情况**::

       $ sudo /sbin/chkconfig --add opensearch
       $ sudo /sbin/chkconfig --add fess

   **使用 systemd 的情况**（推荐）::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

步骤 3: 启动
--------------

关于启动步骤，请参阅 :doc:`run`。

使用 DEB 版安装
====================

DEB 版用于 Debian、Ubuntu 等基于 DEB 的 Linux 发行版。

步骤 1: 安装 OpenSearch
----------------------------------

1. 下载和安装 OpenSearch DEB

   从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 DEB 包并安装。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.3.2/opensearch-3.3.2-linux-x64.deb
       $ sudo dpkg -i opensearch-3.3.2-linux-x64.deb

   或者，也可以添加仓库后进行安装。
   详情请参阅 `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__。

2. 安装 OpenSearch 插件

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. 配置 OpenSearch

   在 ``/etc/opensearch/opensearch.yml`` 中添加以下配置。

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   要添加的配置::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      在生产环境中不要使用 ``plugins.security.disabled: true``。
      请参阅 :doc:`security` 进行适当的安全配置。

步骤 2: 安装 Fess
-----------------------------

1. 安装 Fess DEB

   从 `下载站点 <https://fess.codelibs.org/downloads.html>`__ 下载 DEB 包并安装。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.deb
       $ sudo dpkg -i fess-15.3.2.deb

2. 配置 Fess

   编辑 ``/usr/share/fess/bin/fess.in.sh``。

   ::

       $ sudo vi /usr/share/fess/bin/fess.in.sh

   添加或更改以下配置::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

3. 注册服务

   使用 systemd 启用服务::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

步骤 3: 启动
--------------

关于启动步骤，请参阅 :doc:`run`。

安装后的确认
==================

安装完成后，请确认以下内容：

1. **确认配置文件**

   - OpenSearch 的配置文件（opensearch.yml）
   - Fess 的配置文件（fess.in.sh）

2. **目录权限**

   确认配置中指定的目录存在且设置了适当的权限。

   TAR.GZ 版的情况::

       $ ls -ld /path/to/opensearch-3.3.2/data/config/

   RPM/DEB 版的情况::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **确认 Java 版本**

   ::

       $ java -version

   确认已安装 Java 21 或更高版本。

下一步
==========

安装完成后，请参阅以下文档：

- :doc:`run` - |Fess| 的启动和初始设置
- :doc:`security` - 生产环境的安全配置
- :doc:`troubleshooting` - 故障排除

常见问题
==========

Q: OpenSearch 的其他版本也能工作吗？
---------------------------------------------------------

A: |Fess| 依赖于特定版本的 OpenSearch。
为了确保插件兼容性，强烈建议使用推荐版本（3.3.2）。
如果使用其他版本，需要适当调整插件版本。

Q: 多个 Fess 实例可以共享同一个 OpenSearch 吗？
--------------------------------------------------------------

A: 可以，但不推荐。建议为每个 Fess 实例准备专用的 OpenSearch 集群。
如果多个 Fess 实例共享 OpenSearch，请注意索引名称的冲突。

Q: 如何将 OpenSearch 配置为集群？
------------------------------------------

A: 请参阅 OpenSearch 官方文档 `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__。
配置为集群时，需要删除 ``discovery.type: single-node`` 设置并添加适当的集群配置。
