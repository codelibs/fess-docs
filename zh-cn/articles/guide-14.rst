=========================
随文档和用户增长扩展 Fess
=========================

前言
====

文档和用户增多后，会出现“爬取到早上还没完成”“搜索变慢了”“Fess 因 OutOfMemoryError 停止了”之类的问题。
这时直接增加服务器，未必能解决问题。
因为 Fess 由多个 JVM 进程运行，而不够用的往往只是其中一个。

本文以 Fess 15.9 为对象，按以下顺序说明扩展步骤。

1. 确认哪个进程的什么资源不足
2. 保持单台服务器，调整内存和爬取并行度
3. 将 OpenSearch 分离到其他服务器
4. 将 OpenSearch 组成 3 节点集群
5. 将 Fess 扩展为多台

监控机制的搭建（健康检查、日志、通知）和备份在 :doc:`guide-10` 中介绍。

构成 Fess 的进程
================

即使 Fess 只在 1 台服务器上运行，其内存设置也分为以下几部分。

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - 进程
     - 作用
     - 堆的默认值
     - 设置位置
   * - Fess 主体
     - 搜索页面、管理页面、API、调度器
     - ZIP 版最小 256m、最大 2g，RPM/DEB 版和 Docker 镜像为 512m
     - 环境变量 ``FESS_HEAP_SIZE``
   * - 爬虫
     - 每个爬取作业启动的独立 JVM
     - 最大 512m
     - ``fess_config.properties`` 的 ``jvm.crawler.options``
   * - 建议词生成、缩略图生成
     - 每个作业启动的独立 JVM
     - 最大 256m
     - ``jvm.suggest.options``、``jvm.thumbnail.options``
   * - OpenSearch
     - 保存索引并执行搜索
     - docker-fess 的 ``compose-opensearch3.yaml`` 中为 1g
     - ``OPENSEARCH_JAVA_OPTS`` 或 ``config/jvm.options``

语义搜索使用的分块处理也有独立的 JVM（``jvm.chunk.options``，最大 1g），这部分在 :doc:`guide-18` 中介绍。

如果 ``fess-crawler.log`` 中出现 OutOfMemoryError，不足的是爬虫的 JVM。
这时即使增大 ``FESS_HEAP_SIZE`` 也没有效果。

确认不足的资源
==============

根据症状，检查以下位置。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 症状
     - 检查位置
   * - 搜索很慢
     - 在 [系统信息] > [搜索日志] 的 [性能] 选项卡中，查看响应时间的 p95、p99 以及响应慢的搜索词。区分是只有特定搜索词慢，还是整体都慢。
   * - 爬取完不成
     - 在 [系统信息] > [作业日志] 中，查看爬取作业开始时间和结束时间的变化趋势。如果 ``fess-crawler.log`` 中持续出现 ``Cpu Load XX% is greater than 50%``，说明爬取正被后文所述的负载控制挂起等待。
   * - 爬虫停止
     - 在 ``fess-crawler.log`` 中查找 ``OutOfMemoryError``。
   * - Fess 主体停止、管理页面卡顿
     - 查看 ``fess.log`` 中的 ``OutOfMemoryError``，以及 ``/api/admin/stats`` 的 ``response.stats.jvm.memory.heap.percent``。
   * - OpenSearch 卡顿
     - 查看 ``/api/admin/stats`` 的 ``response.stats.engine.status``，以及 OpenSearch 的 ``_cat/nodes`` 中的堆使用率。``circuit_breaker_exception`` 是堆不足的征兆。

``/api/admin/stats`` 返回的是接收请求的 Fess 主体的 JVM 和 OS，以及 OpenSearch 集群的状态。
不包括爬虫的 JVM 和 OpenSearch 各节点的堆。
调用时需要具有 ``admin-api`` 权限的访问令牌。
创建方法请参阅 `Admin API 概述 <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-overview.html>`__，响应字段请参阅 `Stats API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-stats.html>`__。

OpenSearch 各节点的堆，直接向 OpenSearch 查询。

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

索引的文档数和大小可以用以下命令确认。
``fess.search`` 是搜索所用索引的别名。

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

保持单台进行调整
================

修改 Fess 主体的堆
------------------

使用 Docker 时，在 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 里添加 ``FESS_HEAP_SIZE``。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

修改 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 或 ``volumes`` 后执行 ``docker compose ... up -d``，``fess01`` 容器会被重新创建。
在 [系统] > [通用] 中修改的设置保存在容器内的 ``system.properties`` 中，因此重新创建后会丢失。
本文其他步骤中修改 ``compose.yaml`` 时也是如此。
请先按照 :doc:`guide-10` 的步骤进行备份。

RPM 版修改 ``/etc/sysconfig/fess``、DEB 版修改 ``/etc/default/fess`` 中的 ``FESS_HEAP_SIZE=512m``，然后重启 Fess。
ZIP 版在启动 Fess 的环境中 export ``FESS_HEAP_SIZE``。

是否生效，可以通过运行中进程的参数确认。
Docker 的情况如下。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

``-Xmx`` 的下一行就是该进程的类型。
``FessBoot`` 是 Fess 主体，``exec.Crawler`` 是爬虫。
RPM/DEB 版和 ZIP 版中，请在 Fess 服务器上直接执行 ``sh -c`` 中的命令及其后面的部分。

修改爬虫的堆
------------

``jvm.crawler.options`` 是一个将 JVM 选项以 ``\n`` 分隔排列的值。
由于整个值会被替换，如果只写 ``-Xmx1g``，G1GC 等默认选项都会消失。
请保留默认值，只修改 ``-Xmx512m`` 这一行。

::

    -Xms128m\n\
    -Xmx1g\n\

配置文件的位置，RPM/DEB 版为 ``/etc/fess/fess_config.properties``，ZIP 版为 ``app/WEB-INF/classes/fess_config.properties``。
使用 Docker 时，将镜像中的 ``fess_config.properties`` 取到本地编辑，然后挂载到容器的 ``/opt/fess/fess_config.properties``。
``/opt/fess`` 优先于 ``/etc/fess`` 读取。
由于这个值跨多行，不适合用 ``FESS_JAVA_OPTS`` 中的 ``-Dfess.config.`` 来指定。
步骤请参阅 `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__ 中的“如何应用配置文件”。

重启 Fess 后，在 [系统信息] > [配置信息] 的「应用程序属性」中确认 ``jvm.crawler.options`` 包含 ``-Xmx1g``。
更改从下一次启动的爬虫开始生效。
在爬取运行期间执行上一节的命令，``org.codelibs.fess.exec.Crawler`` 的上一行会显示 ``-Xmx1g``。

爬虫的 JVM 每个爬取作业启动一个。
「Default Crawler」作业用一个爬虫处理所有爬取配置。
如果在爬取配置详情页面中用 [创建新作业] 为每个配置创建作业，它们会分别作为独立的爬虫启动，各自使用 ``-Xmx`` 大小的内存。
要为同时运行的爬虫数设置上限，请使用 ``fess_config.properties`` 的 ``job.max.crawler.processes``\ （默认值 ``0`` 表示无限制）。
超过上限启动的爬取作业不会排队等待，而是直接以错误结束。

建议词生成和缩略图生成的 JVM 也用同样的方法，修改 ``jvm.suggest.options`` 和 ``jvm.thumbnail.options`` 中 ``-Xmx256m`` 这一行。

修改 OpenSearch 的堆
--------------------

在 docker-fess 中，``compose-opensearch3.yaml`` 的 ``search01`` 有以下一行。

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

将这两个值改为相同的值。
通过 ZIP 或 RPM 安装的 OpenSearch，修改 ``config/jvm.options`` 中的 ``-Xms`` 和 ``-Xmx`` 后重启。

上限的参考标准是不超过物理内存的一半，且小于 32GB。
剩余内存会作为 OS 的文件缓存提升搜索速度，因此不要给堆分配过多。
设置为 32GB 以上时，JVM 的 Compressed OOPs 会失效，效率反而下降。
需要更多内存的规模，应增加节点。

索引大小与堆的对应参考值见 `内存配置 <https://fess.codelibs.org/zh-cn/stable/config/setup-memory.html>`__。
从参考值开始，一边观察前面提到的 ``_cat/nodes`` 中的堆使用率和搜索响应时间，一边调整。

在同一台服务器上运行 Fess 和 OpenSearch 时，要确保 Fess 主体、爬虫和 OpenSearch 的堆合计不超过物理内存。

修改爬取并行度
--------------

爬取速度由以下 3 个设置决定。

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - 设置
     - 默认值
     - 位置
   * - 线程数
     - Web 1，文件系统 5
     - 各爬取配置（[爬虫] > [Web]、[文件系统]）
   * - 间隔
     - Web 10000 毫秒，文件系统 1000 毫秒
     - 同上。每个线程每获取一个 URL 后等待的时间
   * - 同时爬虫设置
     - 5
     - [系统] > [通用]。一个爬虫同时处理的爬取配置数量

增加线程数会加快该爬取配置的获取速度，但也会增加爬虫的内存使用量和被爬取服务器的负载。
爬取外部网站或业务中正在使用的服务器时，不要把间隔设得过短。

单台部署中容易忽略的是 ``fess_config.properties`` 的 ``adaptive.load.control``\ （默认值 ``50``）。
当运行 Fess 的服务器的 CPU 使用率在该值以上时，爬取和索引注册线程会等待。
如果同一台服务器上的 OpenSearch 正在使用 CPU 写入索引或执行搜索，爬取可能几乎无法推进。
这时 ``fess-crawler.log`` 中会出现 ``Cpu Load XX% is greater than 50%``。
也可以调高该值，但如果 CPU 长期不足，根本对策是像下一节那样将 OpenSearch 分离到其他服务器。
详情请参阅 `负载控制配置 <https://fess.codelibs.org/zh-cn/stable/config/load-control.html>`__。

将 OpenSearch 分离到其他服务器
==============================

将 OpenSearch 移到其他服务器后，爬取和搜索就不会再争夺 CPU、内存和磁盘 I/O。

OpenSearch 端需要的内容
-----------------------

Fess 使用的 OpenSearch 需要以下 2 项。

- Fess 用的 4 个插件（``opensearch-analysis-fess``、``opensearch-analysis-extension``、``opensearch-minhash``、``opensearch-configsync``）。版本要与 OpenSearch 一致（Fess 15.9 对应 OpenSearch 3.9.0）
- ``opensearch.yml`` 的 ``configsync.config_path``。以绝对路径指定 OpenSearch 配置目录下用于存放词典文件的目录

安装命令见 `在 Linux 上安装（详细步骤） <https://fess.codelibs.org/zh-cn/stable/install/install-linux.html>`__。
docker-fess 的 ``ghcr.io/codelibs/fess-opensearch`` 镜像中已预装这些内容。

将 OpenSearch 放到其他服务器后，端口 9200 会暴露在网络上。
请勿在禁用安全插件的状态下用于生产环境。
设置方法请参阅 :doc:`guide-15` 和 `安全配置 <https://fess.codelibs.org/zh-cn/stable/install/security.html>`__。

Fess 端的设置
-------------

在 Fess 中，用 2 个环境变量指定连接目标和词典位置。

- ``SEARCH_ENGINE_HTTP_URL`` : OpenSearch 的 URL
- ``FESS_DICTIONARY_PATH`` : 与 OpenSearch 端 ``configsync.config_path`` 相同的路径

``FESS_DICTIONARY_PATH`` 是 OpenSearch 服务器上的路径。
Fess 通过 ``configsync`` 插件写入词典文件，因此不需要从 Fess 服务器挂载该目录。
如果没有设置，Fess 无法创建索引，也无法启动。

设置位置：RPM 版为 ``/etc/sysconfig/fess``，DEB 版为 ``/etc/default/fess``，ZIP 版为 ``bin/fess.in.sh``。
使用 Docker 时不使用 ``compose-opensearch3.yaml``，而是在 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 里指定。
v15.9.0 的 ``compose.yaml`` 中，``fess01`` 有等待 ``search01`` 的 ``depends_on``，在不定义 ``search01`` 的部署中，会因 ``service "fess01" depends on undefined service "search01"`` 错误而无法启动。
请删除从 ``depends_on`` 到 ``condition: service_healthy`` 的 3 行。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

这种情况下，之后的 ``docker compose`` 命令只用 ``-f compose.yaml`` 执行。

ZIP 版可以在启动 Fess 之前，用 ``bin/fess-setup check`` 确认连接、4 个插件以及 ``configsync`` 的响应。

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

即使更改连接目标，现有索引也不会迁移到新的 OpenSearch。
要沿用现有文档，请使用快照迁移（`索引管理 <https://fess.codelibs.org/zh-cn/stable/config/admin-index-backup.html>`__ 中的“数据迁移”）。
如果重新爬取即可，连接到空的 OpenSearch 后重新爬取会更简单。

将 OpenSearch 组成 3 节点集群
=============================

OpenSearch 在单台服务器上运行时，该服务器一旦停止，搜索也会停止。
需要冗余时，将 OpenSearch 组成集群。

节点构成
--------

选举负责管理集群的节点（cluster manager）需要过半数同意。
如果能成为 cluster manager 的节点只有 1 台或 2 台，只要 1 台停止就无法完成选举。
因此，要准备 3 台能成为 cluster manager 的节点。
3 台全部同时存放数据的构成是最小构成。

以下是各节点 ``opensearch.yml`` 中与集群构成相关的设置示例（``node.name`` 按节点分别修改）。
``network.host`` 等网络设置和安全设置，请根据环境添加。

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Fess 用的 4 个插件，要在 3 台上都安装相同版本。
``configsync.config_path`` 在 3 台上也使用相同路径。
这是因为 Fess 只向索引设置写入一个 ``FESS_DICTIONARY_PATH`` 的值，所有节点都从该路径读取词典。

docker-fess 的 ``compose/snapshot/compose-cluster.yaml`` 中有用 Docker 组建多节点的示例。
该文件以与开发版 Fess 镜像组合使用为前提，请将其作为 OpenSearch 环境变量写法的参考。

从 Fess 连接
------------

在 ``SEARCH_ENGINE_HTTP_URL`` 中，用逗号分隔列出各节点的 URL。
即使部分节点停止，Fess 也会连接其余节点。

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

分片与副本
----------

Fess 使用 ``fess_config.properties`` 的 ``index.number_of_shards``\ （默认值 ``5``，主分片数）和 ``index.auto_expand_replicas``\ （默认值 ``0-1``，根据数据节点数在 0～1 的范围内自动增减副本）创建文档用的索引。
由于默认值为 ``0-1``，数据节点达到 2 台以上时，无需修改 Fess 设置，每个分片就会创建 1 个副本。
集群状态变为 ``green`` 时，所有副本均已分配。

分片数在创建索引时就已确定，之后即使修改 ``index.number_of_shards``，也不会反映到现有索引上。
要更改分片数，请使用 [系统信息] > [维护] 中的「重新索引」。
指定「分片数」和「最大副本数」，启用「更新别名」后开始，就会创建新索引并复制文档，然后把 ``fess.search`` 和 ``fess.update`` 别名切换到新索引。

重新索引有以下注意事项。

- 文档从开始时 ``fess.update`` 指向的索引中复制。请在没有爬取运行的时间段执行
- 旧索引不会自动删除。磁盘需要有能同时容纳新旧两个索引的容量

页面上的各项请参阅 `维护 <https://fess.codelibs.org/zh-cn/stable/admin/maintenance-guide.html>`__。

确认集群
--------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

如果显示 3 个节点，且 ``status`` 为 ``green``，即告完成。
在 Fess 的 ``/api/admin/stats`` 中，也可以通过 ``response.stats.engine.number_of_nodes`` 和 ``response.stats.engine.status`` 确认同样的内容。

将 Fess 扩展为多台
==================

当搜索用户增加导致 Fess 主体 CPU 不足，或希望 Fess 本身也实现冗余时，将多台 Fess 连接到同一个 OpenSearch。
另外，docker-fess 的 ``compose/multi-instance/`` 是每个 Fess 使用各自索引、并列运行独立搜索服务的构成，与这里说明的构成不同（按组织划分时请参阅 :doc:`guide-13`）。

爬取配置、用户、作业和作业日志保存在 OpenSearch 中，因此从任何一台 Fess 看都是相同的。
而以下内容是每台 Fess 服务器各自持有的，需要在所有服务器上保持一致。

- [系统] > [通用] 的设置（各服务器上的 ``system.properties``）。在设置页面中修改，只会改变该服务器的值
- ``fess_config.properties`` 以及 ``FESS_HEAP_SIZE`` 等环境变量
- 已安装的插件
- ``fess_config.properties`` 的 ``app.cipher.key``。爬取配置和数据存储配置的参数中，名称以 ``password``、``key``、``token``、``secret`` 等结尾的值，会用该密钥加密后保存到 OpenSearch。如果各服务器的密钥不同，就无法解密在其他服务器上保存的值

确定负责爬取的服务器
--------------------

默认作业的「目标」都是 ``all``。
``all`` 与任何 Fess 都匹配，因此保持原样时，「Default Crawler」会在所有服务器上同一时刻运行。

要把爬取交给 1 台服务器，需要同时完成以下 2 项。

1. 只在负责爬取的服务器上，在 ``fess_config.properties`` 中写入识别名，例如 ``scheduler.target.name=crawler``，然后重启。使用 Docker 时，可以在 ``FESS_JAVA_OPTS`` 中指定 ``-Dfess.config.scheduler.target.name=crawler``。其他服务器保持为空
2. 在 [系统] > [调度器] 中打开「Default Crawler」，将「目标」从 ``all`` 改为 ``crawler`` 并保存。用 [创建新作业] 创建的爬取作业也同样修改

「目标」中可以用逗号分隔写入多个识别名。
只做第 1 步，作业仍会像以前一样在所有服务器上运行。
只做第 2 步，由于没有识别名匹配的服务器，爬取在任何服务器上都不会运行。
第 1 步是否生效，可以在负责爬取的服务器的 [系统信息] > [配置信息] 的「应用程序属性」中查看 ``scheduler.target.name`` 的值来确认。

爬取以外的作业（日志汇总、删除旧文档等）的「目标」保持 ``all`` 不变。

固定之后，[立即开始] 也要在负责爬取的服务器的管理页面中点击。
如果在其他服务器上点击，页面上会显示已开始，但该服务器上并不会执行，只会在 ``fess.log`` 中记录 ``Ignoring job``。
如果服务器位于负载均衡器之后，请准备好可以直接访问负责爬取的服务器的途径。

负载均衡器的设置
----------------

Fess 15.9 的登录会话保存在各台 Fess 的内存中。
用负载均衡器分发需要登录使用的搜索页面或管理页面时，请启用粘性会话，让同一用户始终被转发到同一台服务器。
将会话保存到 OpenSearch 并在服务器之间共享的功能，从 15.10 开始可用。

负载均衡器的健康检查可以使用 ``/api/v2/health``。
当 OpenSearch 集群为 ``RED`` 时，以及无法连接 OpenSearch 时，会返回 503。

维护操作的互斥
--------------

[系统信息] > [维护] 中的「重新索引」「重新加载文档索引」「删除爬虫索引」「重建配置索引」会进行互斥控制，避免多台 Fess 同时执行。
如果其他服务器正在执行，会显示“操作已在 <主机名> 上运行。”
这种互斥只针对维护操作，并不会在服务器之间协调作业或 [通用] 的设置。

关于规模参考
============

仅凭文档数或用户数，无法确定所需的构成。
因为每篇文档的正文长度、附件的比例、搜索词的倾向、是否登录使用等，都会使所需的内存和 CPU 产生很大差异。

请像下面这样，根据实测值进行判断。

- 根据索引的 ``store.size``，参照 `内存配置 <https://fess.codelibs.org/zh-cn/stable/config/setup-memory.html>`__ 中的参考表确定 OpenSearch 的堆
- 如果搜索日志的 p95 变差，且 ``_cat/nodes`` 的堆使用率或 CPU 居高不下，就增加 OpenSearch 的堆或节点
- 如果作业日志中的爬取时间变长，并出现 ``Cpu Load`` 日志，就将 OpenSearch 分离到其他服务器
- 如果 OpenSearch 尚有余力而 Fess 主体的 CPU 很高，就将 Fess 扩展为多台

接下来阅读的文章
================

- 想完善监控、日志和备份以投入生产运行：:doc:`guide-10`
- 想保护访问，包括 OpenSearch 的公开范围和登录：:doc:`guide-15`
- 想用代码管理多台服务器设置的统一工作：:doc:`guide-16`
- 想让一个 Fess 按组织分别使用：:doc:`guide-13`
- 想整理部署各阶段需要确认的事项：:doc:`guide-23`

参考资料
========

- `内存配置 <https://fess.codelibs.org/zh-cn/stable/config/setup-memory.html>`__
- `端口与网络配置 <https://fess.codelibs.org/zh-cn/stable/config/setup-port-network.html>`__
- `负载控制配置 <https://fess.codelibs.org/zh-cn/stable/config/load-control.html>`__
- `在 Linux 上安装（详细步骤） <https://fess.codelibs.org/zh-cn/stable/install/install-linux.html>`__
- `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__
- `fess-setup 命令 <https://fess.codelibs.org/zh-cn/stable/install/fess-setup.html>`__
- `维护 <https://fess.codelibs.org/zh-cn/stable/admin/maintenance-guide.html>`__
- `调度器 <https://fess.codelibs.org/zh-cn/stable/admin/scheduler-guide.html>`__
- `搜索日志 <https://fess.codelibs.org/zh-cn/stable/admin/searchlog-guide.html>`__
- `Stats API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-stats.html>`__
- `索引管理 <https://fess.codelibs.org/zh-cn/stable/config/admin-index-backup.html>`__
