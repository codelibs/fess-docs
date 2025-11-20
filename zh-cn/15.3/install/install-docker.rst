==============================
使用 Docker 安装（详细）
==============================

本页面说明使用 Docker 和 Docker Compose 安装 |Fess| 的步骤。
使用 Docker 可以简单快速地构建 |Fess| 环境。

前提条件
========

- 满足 :doc:`prerequisites` 中描述的系统要求
- 已安装 Docker 20.10 或更高版本
- 已安装 Docker Compose 2.0 或更高版本

确认 Docker 安装
=======================

使用以下命令确认 Docker 和 Docker Compose 的版本。

::

    $ docker --version
    $ docker compose version

.. note::

   如果使用旧版本的 Docker Compose，请使用 ``docker-compose`` 命令。
   本文档使用新的 ``docker compose`` 命令格式。

关于 Docker 镜像
=====================

|Fess| 的 Docker 镜像由以下组件构成：

- **Fess**: 全文搜索系统主体
- **OpenSearch**: 搜索引擎

官方 Docker 镜像发布在 `Docker Hub <https://hub.docker.com/r/codelibs/fess>`__。

步骤 1: 获取 Docker Compose 文件
=======================================

使用 Docker Compose 启动需要以下文件。

方法 1: 单独下载文件
----------------------------------

下载以下文件：

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose-opensearch3.yaml

方法 2: 使用 Git 克隆仓库
--------------------------------

如果已安装 Git，也可以克隆整个仓库：

::

    $ git clone --depth 1 --branch v15.3.2 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

步骤 2: 确认 Docker Compose 文件
=======================================

``compose.yaml`` 的内容
----------------------

``compose.yaml`` 包含 Fess 的基本配置。

主要配置项：

- **端口号**: Fess Web 界面的端口（默认: 8080）
- **环境变量**: Java 堆大小等配置
- **卷**: 数据持久化配置

``compose-opensearch3.yaml`` 的内容
---------------------------------

``compose-opensearch3.yaml`` 包含 OpenSearch 的配置。

主要配置项：

- **OpenSearch 版本**: 使用的 OpenSearch 版本
- **内存设置**: JVM 堆大小
- **卷**: 索引数据持久化配置

自定义配置（可选）
------------------------------

如需更改默认配置，请编辑 ``compose.yaml``。

例：更改端口号::

    services:
      fess:
        ports:
          - "9080:8080"  # 映射到主机的 9080 端口

例：更改内存设置::

    services:
      fess:
        environment:
          - "FESS_HEAP_SIZE=2g"  # 将 Fess 的堆大小设置为 2GB

步骤 3: 启动 Docker 容器
================================

基本启动
----------

使用以下命令启动 Fess 和 OpenSearch：

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   - 使用 ``-f`` 选项指定多个 Compose 文件
   - 使用 ``-d`` 选项在后台运行

确认启动日志::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

按 ``Ctrl+C`` 可退出日志显示。

确认启动
--------

确认容器状态::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

请确认以下容器正在运行：

- ``fess``
- ``opensearch``

.. tip::

   启动可能需要几分钟。
   请等待日志中显示「Fess is ready」或类似消息。

步骤 4: 在浏览器中访问
==============================

启动完成后，访问以下 URL：

- **搜索页面**: http://localhost:8080/
- **管理页面**: http://localhost:8080/admin

默认管理员账号：

- 用户名: ``admin``
- 密码: ``admin``

.. warning::

   **关于安全的重要注意事项**

   在生产环境中，必须更改管理员密码。
   详情请参阅 :doc:`security`。

数据持久化
============

为了在删除 Docker 容器后仍保留数据，会自动创建卷。

确认卷::

    $ docker volume ls

|Fess| 相关的卷：

- ``fess-es-data``: OpenSearch 的索引数据
- ``fess-data``: Fess 的配置数据

.. important::

   即使删除容器，卷也不会被删除。
   要删除卷，需要明确执行 ``docker volume rm`` 命令。

停止 Docker 容器
===================

停止容器::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

停止并删除容器::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` 命令会删除容器，但不会删除卷。
   如需同时删除卷，请添加 ``-v`` 选项::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **注意**: 执行此命令会删除所有数据。

高级配置
========

自定义环境变量
--------------------

通过在 ``compose.yaml`` 中添加或更改环境变量，可以进行详细配置。

主要环境变量：

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - 环境变量
     - 说明
   * - ``FESS_HEAP_SIZE``
     - Fess 的 JVM 堆大小（默认: 1g）
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch 的 HTTP 端点
   * - ``TZ``
     - 时区（例: Asia/Shanghai）

例::

    environment:
      - "FESS_HEAP_SIZE=4g"
      - "TZ=Asia/Shanghai"

通过配置文件进行设置
--------------------

|Fess| 的详细设置写在 ``fess_config.properties`` 文件中。
在 Docker 环境中，可以通过以下方法应用这些文件设置。

方法 1：挂载配置文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

通过挂载包含 ``fess_config.properties`` 及其他配置文件的目录，
可以将主机端编辑的设置应用到容器中。

1. 在主机端创建配置目录::

       $ mkdir -p /path/to/fess-config

2. 获取配置文件模板（仅首次）::

       $ docker run --rm codelibs/fess:15.3 cat /opt/fess/app/WEB-INF/conf/fess_config.properties > /path/to/fess-config/fess_config.properties

3. 编辑 ``/path/to/fess-config/fess_config.properties`` 并添加所需的设置::

       # LDAP 配置示例
       ldap.admin.enabled=true
       ldap.admin.initial.dn=cn=admin,dc=example,dc=com
       ldap.admin.user.filter=uid=%s

4. 在 ``compose.yaml`` 中添加卷挂载::

       services:
         fess:
           volumes:
             - /path/to/fess-config:/opt/fess/app/WEB-INF/conf

5. 启动容器::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   ``fess_config.properties`` 包含 LDAP 设置、爬虫设置、
   邮件设置和其他系统配置。
   即使使用 ``docker compose down`` 删除容器，主机端的文件也会保留。

方法 2：通过系统属性进行配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

可以通过环境变量使用系统属性来覆盖 ``fess_config.properties`` 中的配置项。

在 ``fess_config.properties`` 中写入的配置项（例如 ``crawler.document.cache.enabled=false``）
可以用 ``-Dfess.config.设置项名称=值`` 的格式指定。

在 ``compose.yaml`` 的环境变量中添加 ``FESS_JAVA_OPTS``::

    services:
      fess:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   ``-Dfess.config.`` 之后的部分对应 ``fess_config.properties`` 中的配置项名称。

   示例：

   - ``fess_config.properties`` 中的设置：``crawler.document.cache.enabled=false``
   - 系统属性：``-Dfess.config.crawler.document.cache.enabled=false``

LDAP 配置示例::

    services:
      fess:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.ldap.admin.enabled=true -Dfess.config.ldap.admin.initial.dn=cn=admin,dc=example,dc=com -Dfess.config.ldap.admin.user.filter=uid=%s"

常用配置项：

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - fess_config.properties 的配置项
     - 说明
   * - ``crawler.document.cache.enabled``
     - 爬虫文档缓存
   * - ``adaptive.load.control``
     - 自适应负载控制值
   * - ``query.facet.fields``
     - 分面搜索字段
   * - ``ldap.admin.enabled``
     - 启用 LDAP 认证
   * - ``ldap.admin.initial.dn``
     - LDAP 管理员 DN
   * - ``ldap.admin.user.filter``
     - LDAP 用户过滤器

.. tip::

   - 系统属性会覆盖 ``fess_config.properties`` 中的值
   - 可以用空格分隔指定多个设置
   - 结合方法 1（挂载配置文件）可实现更灵活的配置

连接到外部 OpenSearch
------------------------

如果要使用现有的 OpenSearch 集群，请编辑 ``compose.yaml`` 更改连接目标。

1. 不使用 ``compose-opensearch3.yaml``::

       $ docker compose -f compose.yaml up -d

2. 设置 ``SEARCH_ENGINE_HTTP_URL``::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

Docker 网络配置
-----------------------

如需与多个服务联动，可以使用自定义网络。

例::

    networks:
      fess-network:
        driver: bridge

    services:
      fess:
        networks:
          - fess-network

使用 Docker Compose 的生产运维
=========================

在生产环境使用 Docker Compose 时的推荐配置：

1. **设置资源限制**::

       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 4G
           reservations:
             cpus: '1.0'
             memory: 2G

2. **设置重启策略**::

       restart: unless-stopped

3. **日志设置**::

       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"

4. **启用安全配置**

   启用 OpenSearch 的安全插件并设置适当的认证。
   详情请参阅 :doc:`security`。

故障排除
====================

容器无法启动
------------------

1. 确认日志::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. 确认端口号冲突::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. 确认磁盘空间::

       $ df -h

内存不足错误
--------------

如果 OpenSearch 因内存不足无法启动，需要增加 ``vm.max_map_count``。

Linux 的情况::

    $ sudo sysctl -w vm.max_map_count=262144

永久设置::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

数据初始化
------------

删除所有数据并恢复到初始状态::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   执行此命令会完全删除所有数据。

下一步
==========

安装完成后，请参阅以下文档：

- :doc:`run` - |Fess| 的启动和初始设置
- :doc:`security` - 生产环境的安全配置
- :doc:`troubleshooting` - 故障排除

常见问题
==========

Q: Docker 镜像有多大？
--------------------------------------------

A: Fess 镜像约 1GB，OpenSearch 镜像约 800MB。
首次启动时可能需要较长的下载时间。

Q: 可以在 Kubernetes 上运行吗？
----------------------------------

A: 可以。可以将 Docker Compose 文件转换为 Kubernetes 清单，
或使用 Helm Chart 在 Kubernetes 上运行。
详情请参阅 Fess 官方文档。

Q: 如何更新容器？
----------------------------------------------

A: 按以下步骤更新：

1. 获取最新的 Compose 文件
2. 停止容器::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. 获取新镜像::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. 启动容器::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: 可以配置多节点吗？
--------------------------------

A: 可以。通过编辑 ``compose-opensearch3.yaml`` 定义多个 OpenSearch 节点，
可以配置为集群。但是，在生产环境中推荐使用 Kubernetes 等编排工具。
