==================================
在 Linux 上安装（详细步骤）
==================================

本页面说明在 Linux 环境中安装 |Fess| 的步骤。
支持 TAR.GZ、RPM、DEB 各种包格式。

.. warning::

   在生产环境中，不推荐使用内嵌 OpenSearch 运行。
   请务必构建外部的 OpenSearch 服务器。

前提条件
============

- 满足 :doc:`prerequisites` 中描述的系统要求
- 已安装 Java 21
- OpenSearch 3.7.0 可用（或新安装）

选择安装方法
================

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

运行 OpenSearch 所需的系统设置
==================================

为了让 OpenSearch 在 Linux 上稳定运行，需要设置以下内核参数和资源限制。
这些设置主要在 TAR.GZ 版（手动安装 OpenSearch 的情况）中是必需的。
在 RPM / DEB 版中，OpenSearch 和 |Fess| 的软件包会通过 systemd 设置文件描述符数量等参数，但由于 ``vm.max_map_count`` 属于主机侧的内核设置，因此无论采用哪种方式都请进行确认。

虚拟内存最大映射数量
------------------------

由于 OpenSearch 会使用大量内存映射，需要将 ``vm.max_map_count`` 设置为 ``262144`` 以上。

临时设置的情况::

    $ sudo sysctl -w vm.max_map_count=262144

永久设置的情况::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

文件描述符数量
------------------

手动运行 OpenSearch 时（TAR.GZ 版），需要将运行 OpenSearch 的用户的文件描述符数量上限设置为 ``65535`` 以上。

在 ``/etc/security/limits.conf`` 中添加以下内容（请将 ``opensearch`` 替换为运行 OpenSearch 的用户名）::

    opensearch  -  nofile  65535

.. note::

   在 RPM / DEB 版中，由于 systemd 的服务定义中已设置文件描述符数量上限，因此不需要进行此设置。

使用 TAR.GZ 版安装
======================

步骤 1: 安装 OpenSearch
---------------------------

1. 下载 OpenSearch

   从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 TAR.GZ 版。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.tar.gz
       $ tar -xzf opensearch-3.7.0-linux-x64.tar.gz
       $ cd opensearch-3.7.0

   .. note::

      此示例使用 OpenSearch 3.7.0。
      |Fess| 15.7 支持 OpenSearch 3.7.0。

2. 安装 OpenSearch 插件

   安装 |Fess| 所需的插件。

   ::

       $ cd /path/to/opensearch-3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ ./bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

   .. important::

      插件版本必须与 OpenSearch 版本一致。
      在上述示例中，所有版本都指定为 3.7.0。

3. 配置 OpenSearch

   在 ``config/opensearch.yml`` 中添加以下配置。

   ::

       # 配置同步路径（使用绝对路径指定）
       configsync.config_path: /path/to/opensearch-3.7.0/data/config/

       # 禁用安全插件（仅限开发环境）
       plugins.security.disabled: true

   .. warning::

      **关于安全的重要注意事项**

      ``plugins.security.disabled: true`` 仅应在开发环境或测试环境中使用。
      在生产环境中，应启用 OpenSearch 的安全插件并进行适当的认证和授权配置。
      在 OpenSearch 2.12 及更高版本中启用安全插件时，首次启动需要设置管理员密码（环境变量 ``OPENSEARCH_INITIAL_ADMIN_PASSWORD``）。
      详情请参阅 :doc:`security`。

   .. tip::

      请根据环境调整集群名称和网络设置等其他配置。
      配置示例::

          cluster.name: fess-cluster
          node.name: fess-node-1
          network.host: 0.0.0.0
          discovery.type: single-node

   .. tip::

      OpenSearch 的堆大小通过 ``config/jvm.options`` 中的 ``-Xms`` / ``-Xmx`` 进行设置。
      建议将 ``-Xms`` 和 ``-Xmx`` 设置为相同的值，以不超过可用物理内存的一半且低于 32GB 为宜。

步骤 2: 安装 Fess
---------------------

1. 下载和解压 Fess

   从 `下载站点 <https://fess.codelibs.org/zh-cn/downloads.html>`__ 下载 TAR.GZ 版。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.tar.gz
       $ tar -xzf fess-15.7.0.tar.gz
       $ cd fess-15.7.0

2. 配置 Fess

   编辑 ``bin/fess.in.sh``，设置到 OpenSearch 的连接信息。
   该文件中预先以注释状态提供了用于连接外部 OpenSearch 集群的配置。

   ::

       $ vi bin/fess.in.sh

   取消文件开头附近以下 2 行的注释（行首的 ``#``）。

   修改前（默认状态）::

       # External opensearch cluster
       #SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       #FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   修改后::

       # External opensearch cluster
       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/path/to/opensearch-3.7.0/data/config/

   .. note::

      - ``FESS_DICTIONARY_PATH`` 请设置与 OpenSearch 的 ``opensearch.yml`` 中指定的 ``configsync.config_path`` 相同的路径。
      - 如果 OpenSearch 在其他主机上运行，请将 ``SEARCH_ENGINE_HTTP_URL`` 更改为适当的主机名或 IP 地址。例: ``SEARCH_ENGINE_HTTP_URL=http://192.168.1.100:9200``
      - 请勿新增 ``SEARCH_ENGINE_HTTP_URL=...`` 行，而应取消注释已有的注释行并进行编辑。

   .. tip::

      要更改 |Fess| 的堆大小，请编辑 ``bin/fess.in.sh`` 中的 ``FESS_MIN_MEM``\ （默认：``256m``）和 ``FESS_MAX_MEM``\ （默认：``2g``），或设置环境变量 ``FESS_HEAP_SIZE``\ 。

3. 确认安装

   确认配置文件已正确编辑::

       $ grep "SEARCH_ENGINE_HTTP_URL" bin/fess.in.sh
       $ grep "FESS_DICTIONARY_PATH" bin/fess.in.sh

步骤 3: 启动
----------------

关于启动步骤，请参阅 :doc:`run`。

使用 RPM 版安装
===================

RPM 版用于 Red Hat Enterprise Linux、CentOS、Fedora 等基于 RPM 的 Linux 发行版。

步骤 1: 安装 OpenSearch
---------------------------

1. 下载和安装 OpenSearch RPM

   从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 RPM 包并安装。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.rpm
       $ sudo rpm -ivh opensearch-3.7.0-linux-x64.rpm

   或者，也可以添加仓库后进行安装。
   详情请参阅 `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/rpm/>`__\ 。

2. 安装 OpenSearch 插件

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. 配置 OpenSearch

   在 ``/etc/opensearch/opensearch.yml`` 中添加以下配置。

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   要添加的配置::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      在生产环境中不要使用 ``plugins.security.disabled: true``\ 。
      请参阅 :doc:`security` 进行适当的安全配置。

步骤 2: 安装 Fess
---------------------

1. 安装 Fess RPM

   从 `下载站点 <https://fess.codelibs.org/zh-cn/downloads.html>`__ 下载 RPM 包并安装。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.rpm
       $ sudo rpm -ivh fess-15.7.0.rpm

2. 配置 Fess

   在 RPM 版中，需要编辑环境变量配置文件 ``/etc/sysconfig/fess``\ 。
   该文件在软件包升级时也会被保留（由于 ``/usr/share/fess/bin/fess.in.sh`` 在升级时会被覆盖，因此请勿直接编辑该文件）。

   ::

       $ sudo vi /etc/sysconfig/fess

   设置到 OpenSearch 的连接信息。默认值如下所示，请根据需要进行更改::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      ``FESS_DICTIONARY_PATH`` 请指定与 ``opensearch.yml`` 中的 ``configsync.config_path`` 相同的路径。

3. 注册和启用服务

   使用 systemd 启用服务（RHEL 8 及更高版本、CentOS 8 及更高版本中 systemd 为标准配置）::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      由于 |Fess| 的服务依赖于 OpenSearch 的服务，因此需要先启动 OpenSearch。

   .. note::

      在不使用 systemd 的传统环境中，可以使用 ``chkconfig`` 注册 |Fess|::

          $ sudo /sbin/chkconfig --add fess

步骤 3: 启动
----------------

关于启动步骤，请参阅 :doc:`run`。

使用 DEB 版安装
===================

DEB 版用于 Debian、Ubuntu 等基于 DEB 的 Linux 发行版。

步骤 1: 安装 OpenSearch
---------------------------

1. 下载和安装 OpenSearch DEB

   从 `Download OpenSearch <https://opensearch.org/downloads.html>`__ 下载 DEB 包并安装。

   ::

       $ wget https://artifacts.opensearch.org/releases/bundle/opensearch/3.7.0/opensearch-3.7.0-linux-x64.deb
       $ sudo dpkg -i opensearch-3.7.0-linux-x64.deb

   或者，也可以添加仓库后进行安装。
   详情请参阅 `Installing OpenSearch <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/debian/>`__\ 。

2. 安装 OpenSearch 插件

   ::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.7.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.7.0

3. 配置 OpenSearch

   在 ``/etc/opensearch/opensearch.yml`` 中添加以下配置。

   ::

       $ sudo vi /etc/opensearch/opensearch.yml

   要添加的配置::

       configsync.config_path: /var/lib/opensearch/data/config/
       plugins.security.disabled: true

   .. warning::

      在生产环境中不要使用 ``plugins.security.disabled: true``\ 。
      请参阅 :doc:`security` 进行适当的安全配置。

步骤 2: 安装 Fess
---------------------

1. 安装 Fess DEB

   从 `下载站点 <https://fess.codelibs.org/zh-cn/downloads.html>`__ 下载 DEB 包并安装。

   ::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.7.0/fess-15.7.0.deb
       $ sudo dpkg -i fess-15.7.0.deb

2. 配置 Fess

   在 DEB 版中，需要编辑环境变量配置文件 ``/etc/default/fess``\ 。
   该文件在软件包升级时也会被保留（由于 ``/usr/share/fess/bin/fess.in.sh`` 在升级时会被覆盖，因此请勿直接编辑该文件）。

   ::

       $ sudo vi /etc/default/fess

   设置到 OpenSearch 的连接信息。默认值如下所示，请根据需要进行更改::

       SEARCH_ENGINE_HTTP_URL=http://localhost:9200
       FESS_DICTIONARY_PATH=/var/lib/opensearch/data/config/

   .. note::

      ``FESS_DICTIONARY_PATH`` 请指定与 ``opensearch.yml`` 中的 ``configsync.config_path`` 相同的路径。

3. 注册和启用服务

   使用 systemd 启用服务::

       $ sudo systemctl daemon-reload
       $ sudo systemctl enable opensearch.service
       $ sudo systemctl enable fess.service

   .. note::

      由于 |Fess| 的服务依赖于 OpenSearch 的服务，因此需要先启动 OpenSearch。

步骤 3: 启动
----------------

关于启动步骤，请参阅 :doc:`run`。

安装后的确认
================

安装完成后，请确认以下内容：

1. **确认配置文件**

   - OpenSearch 的配置文件（opensearch.yml）
   - |Fess| 的配置文件

     - TAR.GZ 版：``bin/fess.in.sh``
     - RPM 版：``/etc/sysconfig/fess``
     - DEB 版：``/etc/default/fess``

2. **目录权限**

   确认配置中指定的目录（``configsync.config_path`` / ``FESS_DICTIONARY_PATH``）存在，并且已设置适当的权限。

   TAR.GZ 版的情况::

       $ ls -ld /path/to/opensearch-3.7.0/data/config/

   RPM/DEB 版的情况::

       $ sudo ls -ld /var/lib/opensearch/data/config/

3. **确认内核参数**

   ::

       $ sysctl vm.max_map_count

   确认该值为 ``262144`` 以上。

4. **确认 Java 版本**

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
============

Q: OpenSearch 的其他版本也能工作吗？
----------------------------------------

A: |Fess| 依赖于特定版本的 OpenSearch。
为了确保插件兼容性，强烈建议使用推荐版本（3.7.0）。
如果使用其他版本，需要适当调整插件版本。

Q: 多个 Fess 实例可以共享同一个 OpenSearch 吗？
-------------------------------------------------------

A: 可以，但不推荐。建议为每个 Fess 实例准备专用的 OpenSearch 集群。
如果多个 Fess 实例共享 OpenSearch，请注意索引名称的冲突。

Q: 如何将 OpenSearch 配置为集群？
-------------------------------------

A: 请参阅 OpenSearch 官方文档 `Cluster formation <https://opensearch.org/docs/latest/tuning-your-cluster/cluster/>`__\ 。
配置为集群时，需要删除 ``discovery.type: single-node`` 设置并添加适当的集群配置。
