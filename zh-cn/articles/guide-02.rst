==============================
用 Docker 运行 Fess 并试着搜索
==============================

前言
====

开始评估 Fess 时，最先想知道的是“在自己手边运行起来，能进行什么样的搜索”。
本文将使用 Docker 启动 Fess 15.9，爬取 20 个左右的网页，并按顺序一直进行到试用搜索语法。

我们以 Fess 官方网站上的中文“搜索指南”（说明 AND 检索、通配符检索等内容的一组页面）为素材。
由于将对象限定在一处，爬取几分钟即可完成，也可以阅读搜索结果的内容进行确认。

照本文的步骤原样执行后，您将能够完成以下操作。

- 使用 Docker Compose 启动 Fess 和 OpenSearch，并停止、重启
- 完成管理员的首次登录及系统要求的密码修改
- 创建网页爬取配置，执行爬取，并确认已完成
- 试用 AND、OR、排除、短语、字段指定检索

本文不涉及面向生产环境的设置（监控、备份、SSO、规模扩展）。
请从文末的“延伸阅读”中选择符合目的的文章继续阅读。

本文搭建的环境
==============

使用 docker-fess 仓库的 Compose 文件，会启动以下 2 个容器。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 服务
     - 作用
     - 数据存放位置
   * - ``fess01``
     - Fess 本体（镜像 ``ghcr.io/codelibs/fess:15.9.0``）。在端口 8080 上提供搜索页面和管理页面
     - 无卷（容器内）
   * - ``search01``
     - OpenSearch（镜像 ``ghcr.io/codelibs/fess-opensearch``）。端口 9200 也会公开
     - 卷 ``search01_data`` 和 ``search01_dictionary``

索引、爬取配置、用户、作业日志等全部保存在 OpenSearch 中，因此会保留在 ``search01_data`` 卷中。
而在管理页面的 [系统] > [通用] 中修改的设置，则保存在 ``fess01`` 容器内的 ``system.properties`` 中。
这一区别在后面的“停止与重启”中会产生影响。

.. warning::

   此配置中的 OpenSearch 在安全插件处于禁用状态下，通过主机的端口 9200 公开。
   请将其作为在自己的电脑上试用的配置；如果要在共享服务器上运行，请先阅读 :doc:`guide-10` 和 :doc:`guide-15`。

准备
====

- 可以使用 Docker 和 Docker Compose（``docker compose`` 命令）
- Docker 可用的内存在 4GB 以上（仅 OpenSearch 的堆就占用 1GB）
- 可以连接互联网（用于获取镜像和爬取）

在 Linux 或 WSL2 上，需要调高 OpenSearch 启动所需的 ``vm.max_map_count``。

::

    $ sudo sysctl -w vm.max_map_count=262144

此值在操作系统重启后会恢复原状。
如需持续使用，也请写入 ``/etc/sysctl.conf``。

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

启动 Fess
=========

获取 15.9.0 用的 Compose 文件
-----------------------------

docker-fess 默认分支的 Compose 文件会随新版本的发布而更新。
为了将版本固定为 15.9.0，请获取 ``v15.9.0`` 标签的文件。

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

``compose.yaml`` 中只定义了 ``fess01``，``fess01`` 所依赖的 ``search01`` 位于 ``compose-opensearch3.yaml`` 中。
因此，之后的每条 ``docker compose`` 命令都要用 ``-f`` 指定这 2 个文件。
如果只指定其中一个来执行，启动和停止都无法正确进行。

启动并等待就绪
--------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

首次运行需要获取镜像，因此需要几分钟。
用以下命令确认状态。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

``search01`` 变为 healthy 后，``fess01`` 才会启动。
``fess01`` 的 STATUS 变为 ``(healthy)`` 即表示准备完成。
``fess01`` 的健康检查调用的是 ``/api/v2/health``，启动后的最初 120 秒被视为宽限期。

如果迟迟不变为 healthy，请查看日志。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

如果端口 8080 被其他应用程序占用，请将 ``compose.yaml`` 的 ``ports`` 修改为 ``"9080:8080"`` 等。
其他启动问题请参阅 `安装的故障排除 <https://fess.codelibs.org/zh-cn/stable/install/troubleshooting.html>`__。

在浏览器中打开 ``http://localhost:8080/``，会显示 Fess 的搜索页面。
由于还没有爬取任何内容，此时搜索不会有结果。

登录管理页面
============

打开 ``http://localhost:8080/admin/``，使用用户名 ``admin``、密码 ``admin`` 登录。

初始密码 ``admin`` 被设置为不能继续使用，因此登录后会进入显示“您需要更新密码”的页面。

1. 在「新密码」和「确认新密码」中输入相同的密码（8 个字符以上）
2. 点击 [更新]

更新完成后，会打开管理页面的仪表板。
此后请使用新密码登录。
此密码保存在 OpenSearch 中，因此即使重新创建容器也会保留（如果连同卷一起删除，则会恢复为 ``admin``）。

创建爬取配置
============

确定对象
--------

这次爬取 Fess 官方网站的中文“搜索指南”。
它是 ``https://fess.codelibs.org/zh-cn/stable/user/`` 下的 20 个左右的页面，``stable`` 指当前稳定版（15.9）的文档。

注册网页爬取配置
----------------

1. 从管理页面的左侧菜单打开 [爬虫] > [Web]
2. 点击 [新建]
3. 输入以下项目。其他项目保持默认值

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - 项目
        - 值
      * - 名称
        - ``Fess 搜索指南``
      * - URL
        - ``https://fess.codelibs.org/zh-cn/stable/user/index.html``
      * - 要包含在爬网中的URL
        - ``https://fess.codelibs.org/zh-cn/stable/user/.*``
      * - 最大访问数
        - ``50``

4. 点击 [创建]

各项目的含义如下。

- 「名称」为必填项。为空时无法创建
- 「URL」是爬取的起点
- 「要包含在爬网中的URL」是正则表达式，不会跟随指向与其不匹配的 URL 的链接。如果留空，爬虫会顺着页面内的链接一直爬到其他版本、其他语言乃至外部网站
- 「最大访问数」是为防止正则表达式写错而设的上限

在保持默认值的项目中，「线程数」为 ``1``，「间隔」为 ``10000`` 毫秒。
每个页面等待 10 秒，因此可以减轻对方网站的负载。
「权限」中填有 ``{role}guest``，因此未登录的用户也能看到搜索结果。
按部门区分显示的方法将在 :doc:`guide-05` 中介绍。

.. note::

   如果以 ``/zh-cn/15.9/`` 这样带版本号的 URL 为对象，一个页面也不会被注册。
   这些页面中包含指向 ``/zh-cn/stable/`` 的 ``<link rel="canonical">``。
   Fess 的爬虫不会注册这样的页面，而是转而跟随 canonical 的 URL。
   由于该 URL 不在「要包含在爬网中的URL」的正则表达式范围内，因此什么也不会被注册。
   以自己公司的网站为对象时，也请确认 canonical 的 URL 是否包含在正则表达式中。

.. tip::

   在 [系统] > [向导] 中，只需输入「名称」「爬网路径」「最大访问数」「深度」即可创建爬取配置，并直接进入 [开始爬网]。
   不过，用向导创建的配置中不会填入「要包含在爬网中的URL」，因此无法限定跟随链接的范围。
   像本次这样需要限定对象时，请通过上述 [爬虫] > [Web] 创建。

执行爬取并确认完成
==================

开始爬取
--------

仅保存配置并不会开始爬取。

1. 打开 [系统] > [调度器]
2. 点击列表中的“Default Crawler”
3. 点击 [立即开始]

“Default Crawler”是将已启用的网页、文件系统、数据存储爬取配置一并执行的作业。
此作业在初始状态下设置了 cron 表达式 ``0 0 * * *``，每天也会自动执行 1 次。
如果让容器一直运行，第二天以后也会以相同的配置重新爬取。

本次的配置以 10 秒的间隔获取 20 个左右的页面，因此大约需要几分钟完成。

确认已完成
----------

按以下顺序确认。

1. 打开 [系统信息] > [作业日志]。“Default Crawler”一行的「状态」从「运行中」变为「OK」，即表示作业已结束。如果是「失败」，请点击该行打开详细信息，确认「结果」
2. 打开 [系统信息] > [爬网信息]，点击列表最上方（最新）的会话。「索引大小 (Web/文件)」就是本次爬取注册的文档数。本次大约为 20 个
3. 如果数量比预想的少，请打开 [系统信息] > [失败URL]。其中记录了因连接错误等原因无法获取的 URL 及其原因

即使作业为「OK」，注册数量也可能为 0。
与「要包含在爬网中的URL」的正则表达式不匹配的 URL 不会被视为错误，而是被视为对象之外，因此也不会记录到失败URL中。
如果数量为 0 且失败URL也为空，请重新检查 URL 和正则表达式的写法（``https`` 与 ``http`` 的区别、末尾有无 ``.*`` 等）。

试着搜索
========

打开 ``http://localhost:8080/`` 进行搜索。
搜索页面使用的是 Fess 自带的主题 ``bootstrap``。

首先请输入 ``通配符`` 并搜索。
结果中会列出“通配符检索”页面、“特殊字符”页面等。
点击结果的标题，会打开原始页面（fess.codelibs.org）。

接下来，依次输入以下搜索词。
每一个都可以用刚刚爬取的页面确认结果。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 输入的搜索词
     - 含义
   * - ``字段 URL``
     - 用空格分隔即为 AND 检索，只会显示同时包含两者的页面
   * - ``通配符 OR 模糊``
     - 显示包含其中任意一个的页面。``OR`` 须为半角大写，前后需要空格
   * - ``检索 -标签``
     - 从结果中排除包含“标签”的页面。``-`` 要加在想排除的词的紧前面
   * - ``"范围指定检索"``
     - 查找按原有顺序包含引号中词句的页面（短语检索）
   * - ``title:排序``
     - 只查找标题中包含“排序”的页面（字段指定检索）

如果像 ``or``、``and`` 这样用小写书写，就不会成为运算符，而是被当作普通的搜索词处理。

这里使用的语法，以及通配符、模糊检索、范围指定等其余语法，在刚刚爬取的 `搜索指南 <https://fess.codelibs.org/zh-cn/stable/user/index.html>`__ 中都有说明。
也可以在自己的 Fess 中搜索感兴趣的语法，打开相应页面阅读。

停止与重启
==========

停止的方式不同，保留下来的内容也不同。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 操作
     - 保留的内容
     - 丢失的内容
   * - ``stop`` → ``start``
     - 全部
     - 无
   * - ``down`` → ``up -d``
     - 保存在 OpenSearch 中的内容（索引、爬取配置、用户和密码、作业日志等）
     - 保存在 ``fess01`` 容器内的内容（在 [系统] > [通用] 中修改的设置等）
   * - ``down -v``
     - 无
     - 全部（管理员密码也会恢复为 ``admin``）

平时停止时使用 ``stop``，重启时使用 ``start``。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

``down`` 会删除容器。
OpenSearch 的数据会保留在卷中，但 [通用] 的设置写在 ``fess01`` 容器内的 ``system.properties`` 中，因此会随容器一起消失。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

结束试用、要连同数据一起清理时，请加上 ``-v``。
卷也会被删除，且无法恢复。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

在 [通用] 中修改的部分设置，如果在 ``compose.yaml`` 的 ``FESS_JAVA_OPTS`` 中指定，即使重新创建容器也会保留（也有像 SSO 连接设置这样无法用此方法指定的项目）。
具体步骤请参阅 `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__。

延伸阅读
========

请根据目的继续阅读以下文章。

- 想了解 Fess 的构成及整个系列文章的阅读顺序：:doc:`guide-01`
- 想在现有的内部网站或门户中放置搜索框：:doc:`guide-03`
- 想统一搜索内部网站和文件服务器：:doc:`guide-04`
- 想根据部门或职位改变可见的搜索结果：:doc:`guide-05`
- 想同时搜索 Slack、Confluence、数据库等中的数据：先阅读 :doc:`datastore-basics`，然后阅读 :doc:`guide-06`、:doc:`guide-07`、:doc:`guide-12`
- 想让生成式 AI 根据内部文档回答问题：:doc:`guide-19`
- 想在关键词不一致时也能找到含义相近的文档：:doc:`guide-18`
- 想完善监控和备份以投入生产运营：:doc:`guide-10`
- 想配置 SSO 和访问保护：:doc:`guide-15`
- 想随着文档数量和用户的增加进行扩展：:doc:`guide-14`

参考资料
========

- `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__
- `docker-fess（GitHub） <https://github.com/codelibs/docker-fess>`__
- `网页爬取的设置 <https://fess.codelibs.org/zh-cn/stable/admin/webconfig-guide.html>`__
- `作业日志 <https://fess.codelibs.org/zh-cn/stable/admin/joblog-guide.html>`__
- `搜索指南 <https://fess.codelibs.org/zh-cn/stable/user/index.html>`__
