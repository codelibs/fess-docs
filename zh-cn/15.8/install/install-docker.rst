========================
使用 Docker 安装（详细）
========================

本页面说明使用 Docker 和 Docker Compose 安装 |Fess| 的步骤。
使用 Docker 可以简单快速地构建 |Fess| 环境。

前提条件
========

- 满足 :doc:`prerequisites` 中所述的系统要求
- 已安装 Docker 20.10 或更高版本
- 已安装 Docker Compose 2.0 或更高版本

确认 Docker 安装
================

使用以下命令确认 Docker 和 Docker Compose 的版本。

::

    $ docker --version
    $ docker compose version

.. note::

   如果使用旧版本的 Docker Compose，请使用 ``docker-compose`` 命令。
   本文档使用新的 ``docker compose`` 命令格式。

关于 Docker 镜像
================

使用 Docker Compose 启动 |Fess| 后，将运行以下 2 个容器。

- **Fess** (``fess01``)：全文搜索系统本体
- **OpenSearch** (``search01``)：搜索引擎

官方 Docker 镜像发布于 `GitHub Container Registry <https://github.com/codelibs/docker-fess/pkgs/container/fess>`__\ 。
Compose 文件及启动步骤由 `docker-fess <https://github.com/codelibs/docker-fess>`__ 仓库管理。

步骤 1: 获取 Docker Compose 文件
================================

使用 Docker Compose 启动需要以下文件。

方法 1: 单独下载文件
--------------------

下载以下文件：

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
    $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

方法 2: 使用 Git 克隆仓库
-------------------------

如果已安装 Git，也可以克隆整个仓库：

::

    $ git clone --depth 1 --branch v15.8.0 https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

步骤 2: 确认 Docker Compose 文件
================================

``compose.yaml`` 的内容
-----------------------

``compose.yaml`` 包含 Fess 本体（``fess01`` 服务）的配置。

主要配置项：

- **端口号**：Fess Web 界面的端口（默认：8080）
- **环境变量**：OpenSearch 的连接地址 (``SEARCH_ENGINE_HTTP_URL``)、词典文件路径 (``FESS_DICTIONARY_PATH``) 等
- **启动顺序**：已通过 ``depends_on`` 设置为在 OpenSearch (``search01``) 变为正常状态后再启动

``compose-opensearch3.yaml`` 的内容
-----------------------------------

``compose-opensearch3.yaml`` 包含搜索引擎（``search01`` 服务，OpenSearch）的配置。

主要配置项：

- **OpenSearch 镜像**：使用的 OpenSearch 镜像（``ghcr.io/codelibs/fess-opensearch``）
- **内存设置**：JVM 堆大小
- **卷**：用于数据持久化的卷（``search01_data``：索引数据，``search01_dictionary``：词典文件）

自定义配置（可选）
------------------

如需更改默认设置，请编辑 ``compose.yaml``\ 。

示例：更改端口号::

    services:
      fess01:
        ports:
          - "9080:8080"  # 映射到主机的 9080 端口

示例：更改内存设置::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=2g"  # 将 Fess 的堆大小设置为 2GB

步骤 3: 启动 Docker 容器
========================

基本启动
--------

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

- ``fess01``
- ``search01``

.. tip::

   启动可能需要几分钟。首先 OpenSearch (``search01``) 变为正常状态后，Fess (``fess01``) 才会启动。
   可以通过 ``docker compose ... ps`` 确认各容器的状态，``fess01`` 启动后即可在浏览器中访问 http://localhost:8080/。

步骤 4: 通过浏览器访问
======================

启动完成后，访问以下 URL：

- **搜索页面**：http://localhost:8080/
- **管理页面**：http://localhost:8080/admin

默认管理员账号：

- 用户名：``admin``
- 密码：``admin``

.. warning::

   **关于安全的重要提示**

   在生产环境中，请务必更改管理员密码。
   详情请参阅 :doc:`security`。

启用 AI 搜索模式（LLM 插件）
============================

自 |Fess| 15.8 起，AI 搜索模式（RAG Chat）功能已拆分为 ``fess-llm-*`` 插件。
官方 `docker-fess <https://github.com/codelibs/docker-fess>`__ 仓库中附带了面向主要 LLM 提供商的 overlay 文件。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Overlay
     - 用途
   * - ``compose-ollama.yaml``
     - Ollama（本地 LLM，会启动额外的 ``ollama01`` 服务）
   * - ``compose-gemini.yaml``
     - Google Gemini（云端 API）
   * - ``compose-openai.yaml``
     - OpenAI（云端 API）

每个 overlay 都会通过 ``FESS_PLUGINS`` 自动获取相应的插件，并在 ``FESS_JAVA_OPTS`` 中设置
``-Dfess.config.rag.chat.enabled=true`` 以启用 RAG Chat。
对于使用云端 API 的 Gemini 和 OpenAI，还需通过 ``-Dfess.system.rag.llm.name`` 指定所使用的提供商，
并设置 API 密钥 (``rag.llm.<provider>.api.key``) 和模型 (``rag.llm.<provider>.model``)。
Ollama 会直接使用 ``rag.llm.name`` 的默认值 (``ollama``)，因此无需显式指定，
只需设置连接地址 (``rag.llm.ollama.api.url``)。

使用 Gemini 的示例::

    $ export GEMINI_API_KEY="AIzaSy..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

使用 OpenAI 的示例::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

.. note::

   使用的模型可以通过 ``GEMINI_MODEL`` 和 ``OPENAI_MODEL`` 环境变量更改
   （默认值分别为 ``gemini-2.5-flash`` 和 ``gpt-5-mini``）。

使用 Ollama 的示例::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gpt-oss:20b

.. warning::

   ``compose-ollama.yaml`` 中的 ``ollama01`` 服务默认配置为使用 NVIDIA GPU
   （需要安装 `NVIDIA Container Toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`__）。
   如果要在未配备 GPU 的环境中运行，请删除或注释掉 ``compose-ollama.yaml`` 中的 ``deploy:`` 块（``reservations`` 下的 GPU 指定部分）。

.. tip::

   启动后，可以在管理界面「系统 > 全局设置」的设置页面中更改所使用的 LLM 提供商 (``rag.llm.name``)
   以及各提供商专属的设置。但这些更改会保存到容器内的配置文件中，
   一旦重新创建容器（先执行 ``docker compose down`` 再执行 ``up``），这些更改就会丢失。
   如需持久化保存设置，请像上面的示例一样在 Compose 文件的 ``FESS_JAVA_OPTS`` 中指定。

数据持久化
==========

|Fess| 的数据（索引、抓取的文档、用户信息、设置等）全部保存在 OpenSearch 中。
这些数据会持久化保存在 OpenSearch 的卷中，因此即使删除容器，数据也会被保留。
Fess 本体（``fess01``）的容器本身不保存状态，也没有专用的卷。

确认卷::

    $ docker volume ls

``compose-opensearch3.yaml`` 中定义的主要卷：

- ``search01_data``：OpenSearch 的索引数据（包含 Fess 的全部数据）
- ``search01_dictionary``：词典文件

.. note::

   Docker Compose 的卷名会带有项目名称（默认为 Compose 文件所在目录的名称）作为前缀。
   例如在 ``compose`` 目录中启动时，实际的卷名会类似于 ``compose_search01_data``\ 。

.. important::

   即使删除容器，卷也不会被删除。
   要删除卷，需要显式执行 ``docker volume rm`` 命令。

停止 Docker 容器
================

停止容器::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop

停止并删除容器::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ``down`` 命令会删除容器，但不会删除卷。
   如果还要删除卷（如 ``search01_data`` 等），请添加 ``-v`` 选项::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

   **注意**：执行此命令会删除保存在 OpenSearch 中的所有数据。

高级配置
========

自定义环境变量
--------------

通过在 ``compose.yaml`` 中添加或更改环境变量，可以进行详细配置。

主要环境变量：

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 环境变量
     - 说明
   * - ``FESS_HEAP_SIZE``
     - Fess 的 JVM 堆大小（Docker 镜像的默认值：512m）
   * - ``FESS_JAVA_OPTS``
     - 指定额外的 JVM 选项（例如通过 ``-Dfess.config.*`` 覆盖配置等）
   * - ``FESS_PLUGINS``
     - 启动时自动安装的插件（以空格分隔的 ``name:version`` 格式。例：``fess-ds-wikipedia:15.8.0``）
   * - ``SEARCH_ENGINE_HTTP_URL``
     - OpenSearch 的 HTTP 端点（``compose.yaml`` 的默认值：``http://search01:9200``）
   * - ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD``
     - 连接到已启用认证的 OpenSearch 时使用的凭据
   * - ``FESS_DICTIONARY_PATH``
     - 词典文件的路径（与 OpenSearch 共享的目录）
   * - ``FESS_PORT``
     - Fess 在容器内监听的端口（默认值：8080）

示例::

    services:
      fess01:
        environment:
          - "FESS_HEAP_SIZE=4g"

.. note::

   如需更改时区，请在 ``FESS_JAVA_OPTS`` 中像 ``-Duser.timezone=Asia/Tokyo`` 这样指定。

如何应用配置文件
----------------

|Fess| 的详细设置写在 ``fess_config.properties`` 文件中。
在 Docker 镜像中，``fess_config.properties`` 位于容器内的 ``/etc/fess``\ 。
在 Docker 环境中应用设置有以下方法。

方法 1: 挂载配置文件
~~~~~~~~~~~~~~~~~~~~

由于 ``/etc/fess`` 中还包含 Fess 运行所需的其他配置文件，如果直接用挂载替换整个目录，会导致启动失败。
请改用会被添加到类路径开头的覆盖目录 ``/opt/fess``\ 。该目录初始状态为空。

1. 在主机端创建用于存放配置文件的目录::

       $ mkdir -p /path/to/fess-config

2. 获取配置文件模板（仅首次需要）::

       $ curl -o /path/to/fess-config/fess_config.properties https://raw.githubusercontent.com/codelibs/fess/refs/tags/fess-15.8.0/src/main/resources/fess_config.properties

3. 编辑 ``/path/to/fess-config/fess_config.properties`` 并写入所需的设置::

       # 示例
       crawler.document.cache.enabled=false
       adaptive.load.control=20
       query.facet.fields=label,host

4. 在 ``compose.yaml`` 的 ``fess01`` 服务中添加卷挂载::

       services:
         fess01:
           volumes:
             - /path/to/fess-config/fess_config.properties:/opt/fess/fess_config.properties

5. 启动容器::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   由于 ``/opt/fess`` 会被添加到类路径开头，放置在此处的 ``fess_config.properties``
   会优先于镜像自带的 ``/etc/fess/fess_config.properties``\ 。
   属性文件是按文件为单位加载的，不会按配置项逐项合并。
   因此，不仅要包含想要覆盖的配置项，还必须放置 **包含全部配置项的完整文件**\ 。
   如果只想更改部分配置项，请使用下面的「方法 2」。

方法 2: 通过系统属性进行设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

可以通过环境变量，以系统属性的形式覆盖 ``fess_config.properties`` 中的配置项。

``fess_config.properties`` 中记载的配置项（例如 ``crawler.document.cache.enabled=false``），
可以用 ``-Dfess.config.配置项名称=值`` 的格式指定。

在 ``compose.yaml`` 的 ``fess01`` 服务的环境变量中添加 ``FESS_JAVA_OPTS``::

    services:
      fess01:
        environment:
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.cache.enabled=false -Dfess.config.adaptive.load.control=20 -Dfess.config.query.facet.fields=label,host"

.. note::

   ``-Dfess.config.`` 之后的部分对应 ``fess_config.properties`` 中的配置项名称。
   如果只想覆盖部分配置项，使用这种方法更简单。

连接到外部 OpenSearch
---------------------

如果要使用现有的 OpenSearch 集群，请不使用 ``compose-opensearch3.yaml``，仅通过 ``compose.yaml`` 启动，并更改连接目标。

1. 启动时不指定 ``compose-opensearch3.yaml``::

       $ docker compose -f compose.yaml up -d

2. 在 ``compose.yaml`` 的 ``fess01`` 服务中设置连接目标::

       environment:
         - "SEARCH_ENGINE_HTTP_URL=http://your-opensearch-host:9200"

.. note::

   如果要连接到已启用认证的 OpenSearch，还需要指定 ``SEARCH_ENGINE_USERNAME`` 和 ``SEARCH_ENGINE_PASSWORD``\ 。

其他 Overlay 与构成
-------------------

``docker-fess`` 仓库中除上述内容外，还包含按用途划分的 Compose 文件和目录。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 文件 / 目录
     - 用途
   * - ``compose-dashboards3.yaml``
     - 添加 OpenSearch Dashboards（端口 5601，用于数据可视化）
   * - ``compose-minio.yaml``
     - 添加 MinIO（对象存储），并将其用作 Fess 存储功能的保存位置
   * - ``vanilla/``
     - 与不含 Fess 专用插件的原生 OpenSearch 组合使用的构成（词典管理等部分功能不可用）
   * - ``snapshot/``
     - 使用开发版（snapshot）镜像的构成（包括集群构成以及与 Elasticsearch 8 的组合）
   * - ``multi-instance/``
     - 启动多个共享同一个 OpenSearch 的 Fess 实例的构成

Docker 网络配置
---------------

如需与多个服务联动，可以使用自定义网络。

示例::

    networks:
      fess-network:
        driver: bridge

    services:
      fess01:
        networks:
          - fess-network

使用 Docker Compose 的生产运维
==============================

在生产环境中使用 Docker Compose 时的推荐设置：

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

4. **启用安全设置**

   启用 OpenSearch 的安全插件，并配置适当的认证。
   详情请参阅 :doc:`security`。

故障排除
========

容器无法启动
------------

1. 确认日志::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs

2. 确认端口号是否冲突::

       $ sudo netstat -tuln | grep 8080
       $ sudo netstat -tuln | grep 9200

3. 确认磁盘空间::

       $ df -h

内存不足错误
------------

如果 OpenSearch 因内存不足而无法启动，需要增大 ``vm.max_map_count``\ 。

Linux 的情况::

    $ sudo sysctl -w vm.max_map_count=262144

永久设置::

    $ echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
    $ sudo sysctl -p

数据初始化
----------

删除所有数据并恢复到初始状态::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v
    $ docker volume prune

.. warning::

   执行此命令会彻底删除所有数据。

下一步
======

安装完成后，请参阅以下文档：

- :doc:`run` - |Fess| 的启动与初次设置
- :doc:`security` - 生产环境的安全设置
- :doc:`troubleshooting` - 故障排除

常见问题
========

Q: 下载镜像需要多少磁盘空间？
-----------------------------

A：Fess 和 OpenSearch 的镜像会在首次启动时下载，合计需要几 GB 左右的磁盘空间。
根据网络环境的不同，下载可能需要较长时间。

Q: 可以在 Kubernetes 上运行吗？
-------------------------------

A：可以。可以使用 ``kompose`` 等工具将 Docker Compose 文件转换为 Kubernetes 清单，
也可以自行编写清单进行运维（官方未提供 Helm chart）。

Q: 如何更新容器？
-----------------

A：按以下步骤进行更新：

1. 获取最新的 Compose 文件
2. 停止容器::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

3. 获取新镜像::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

4. 启动容器::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Q: 可以配置多节点吗？
---------------------

A：可以。可以参考 ``docker-fess`` 仓库中的 ``snapshot/compose-cluster.yaml``，将 OpenSearch 配置为多个节点，
也可以参考 ``multi-instance/``，配置多个共享同一个 OpenSearch 的 Fess 实例。
不过，在生产环境中建议使用 Kubernetes 等编排工具。
