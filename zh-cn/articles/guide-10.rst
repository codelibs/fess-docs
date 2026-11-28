===================================
Fess 生产运维：监控、备份与故障处理
===================================

前言
====

在企业内部发布 Fess 之后，运维人员常常会遇到下面这些情况：
直到用户来询问才第一次发现搜索已经不可用；夜间爬取失败了好几天都没有察觉；重建服务器后设置没能恢复。

本文介绍如何利用 Fess 15.9 自带的机制，为这些情况做好准备。

- 通过 ``/api/v2/health`` 和 ``/api/admin/stats``，从外部监控工具检查 Fess 和 OpenSearch 的状态
- 将爬取结束、OpenSearch 状态变化和错误日志通过邮件、Slack、Google Chat 发送通知
- 了解各个日志文件记录了什么、位于何处
- 用 cron 获取设置的备份，并恢复到另一台服务器
- 了解发生故障时应查看 Fess 的哪些页面和哪些日志

以代码方式管理设置的方法见 :doc:`guide-16`，随文档数和用户数增长进行扩展（包括堆的调整）的方法见 :doc:`guide-14`。
示例命令以 :doc:`guide-02` 的 Docker 环境（``fess01`` 和 ``search01``）为前提。
ZIP 版和 RPM/DEB 版的不同之处会在相应位置另行说明。

监控
====

存活监控：/api/v2/health
------------------------

Fess 提供了无需认证即可调用的健康检查 API。

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

HTTP 状态码的含义如下。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 状态码
     - 状态
   * - 200
     - Fess 正常响应，且 OpenSearch 集群为 ``GREEN`` 或 ``YELLOW``
   * - 503
     - OpenSearch 集群为 ``RED``，或者 Fess 无法连接到 OpenSearch（``error.details.engine.status`` 为 ``UNAVAILABLE``）
   * - 无响应/超时
     - Fess 进程已停止，或者 OpenSearch 没有响应、Fess 一直在等待

在监控工具中，请以该状态码作为判断依据。
使用 ``curl`` 时，加上 ``-f`` 后，返回 503 时退出码将不为 0。
如果 OpenSearch 进程没有停止却不再响应，该 API 会等待 OpenSearch 的响应，最长到 ``index.health.timeout``\ （默认 ``10m``）。
请在监控端像上例中的 ``--max-time 10`` 那样设置超时，并将超时也视为异常。
另外，本文以前的版本中介绍的 ``/api/v1/health`` 在 15.9 的标准配置下无法使用（只有安装了插件 ``fess-webapp-v1-api`` 时才会提供 ``/api/v1``）。

Docker 中的 ``fess01`` 通过两种机制使用这个 API。

- ``compose.yaml`` 中的 ``healthcheck`` 每 30 秒调用一次，结果显示为 ``docker compose ps`` 中的 ``(healthy)``
- 容器内的启动脚本也会每 60 秒调用一次，启动后若连续 5 次返回非 200，就会终止容器。由于设置了 ``restart: unless-stopped``，容器随后会被重新启动

因此，如果 OpenSearch 持续处于 ``RED`` 状态几分钟，``fess01`` 就会反复重启。
当 ``fess01`` 不断重启时，请先检查 ``search01``。

资源监控：/api/admin/stats
--------------------------

堆使用率和磁盘剩余空间可以通过管理 API ``GET /api/admin/stats`` 获取。
[系统信息] > [配置信息] 中只有属性列表，不显示内存使用量。

调用管理 API 需要访问令牌。

1. 打开 [系统] > [访问令牌]，点击 [新建]
2. 在「名称」中输入用途（例如 ``monitoring``），在「权限」中输入 ``{role}admin-api``，然后点击 [创建]
3. 从列表中打开创建的令牌，记下「令牌」的值

.. warning::

   ``{role}admin-api`` 的令牌可以使用所有管理 API，包括修改和删除设置的 API。
   没有将其限制为只读的设置。
   保存在监控服务器的文件等位置时，请与管理员密码同等对待。

令牌通过 ``Authorization`` 请求头传递。
下面的示例提取堆使用率（%）以及各文件系统的使用率。

::

    $ curl -fsS -H "Authorization: Bearer <令牌>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

此外还会返回 GC 的次数和累计时间（``jvm.gc``）、操作系统的 CPU 使用率和平均负载（``os``）、OpenSearch 的集群状态和分片数（``engine``）。
字段列表请参阅 `Stats API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-stats.html>`__。

读取这些值时，请注意以下两点。

- ``jvm`` 是 Fess 本体（Web 应用）的 JVM 的值。爬取在另一个 JVM 进程中运行，因此爬虫的内存不足不会体现在这里。请在 ``fess-crawler.log`` 中确认（后述）
- ``fs`` 是运行 Fess 的主机（Docker 中为容器）的文件系统。OpenSearch 数据区的剩余空间请直接向 OpenSearch 查询

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

修改堆大小的方法请参阅 :doc:`guide-14`。

接收通知
--------

Fess 的通知目标通过 [系统] > [通用] 中「通知」栏的 3 个项目进行设置。

- 「通知邮件」：收件人的邮件地址（多个地址用逗号分隔）
- 「Slack Webhook URLs」：Slack 的 Incoming Webhook URL
- 「Google Chat Webhook URLs」：Google Chat 的 Webhook URL

只要设置了其中任意一项，下面 3 种通知就会发送到同样的目标。

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 通知
     - 发送条件
     - 需要的额外设置
   * - 爬取完成（主题 ``[FESS] Crawler completed``）
     - 每次爬取作业结束时发送，无论成功与否。包含状态（OK/FAIL）和已索引的文档数
     - 无
   * - OpenSearch 状态变化（主题 ``[FESS] Status Change``）
     - 调度器作业“Search Engine Monitor”每分钟查询一次 OpenSearch，在集群变为 ``RED`` 时以及从 ``RED`` 恢复时发送
     - 无
   * - 日志通知（主题 ``[FESS] ERROR Log Alert``）
     - 作业“Log Notification”每 5 分钟汇总一次 Fess 和爬虫等输出的 ERROR（或指定级别及以上）日志并发送
     - 在 [通用] 中启用「Log Notification」，并选择「Log Notification Level」

如果无法连接到 OpenSearch，“Search Engine Monitor”作业本身会失败，不会发送状态变化通知。
连接中断请通过从外部监控上一节中的 ``/api/v2/health`` 来发现。

日志通知的默认级别是 ``ERROR``。
失败的计划作业会以 ``WARN``\ （``Failed to execute job: ...``）记录，因此如果也想得知作业失败，请将「Log Notification Level」设为 ``WARN``。
这样一来，其他所有 ``WARN`` 也都会被通知。

如果要通过邮件接收，需要在两个文件中设置 SMTP 服务器，然后重启 Fess。

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties``：用于日志通知、状态变化通知以及 [发送测试邮件] 按钮
- ``fess_env_crawler.properties``：用于爬取完成通知（因为爬取在另一个进程中运行）

这两个文件在 ZIP 版中位于 ``app/WEB-INF/classes/``，在 RPM/DEB 版中位于 ``/etc/fess/``。
设置完成后，用 [通用] 中的 [发送测试邮件] 确认能否收到邮件。

如果想在 Docker 中快速收到通知，无需编辑文件的 Slack 或 Google Chat Webhook 比较方便。
不过，[通用] 中的设置保存在 ``fess01`` 容器内的 ``system.properties`` 中，用 ``docker compose down`` 重建容器后就会丢失（参见 :doc:`guide-02` 中关于停止与重启的一节）。
请在后述的备份中一并备份 ``system.properties``。

查看搜索响应时间和爬取结果
--------------------------

除了外部监控之外，还应在管理页面中定期检查以下 3 个页面。

- [系统信息] > [作业日志]：“Default Crawler”等作业的状态（OK/失败）和结果。“Search Engine Monitor”“Log Notification”这类每分钟或每几分钟运行一次的作业不会记录在这里
- [系统信息] > [爬网信息]：每个会话的「爬虫状态」以及「索引大小 (Web/文件)」「索引大小 (数据存储)」。检查是否比上次大幅减少
- [系统信息] > [搜索日志] 的 [性能] 标签页：响应时间的中位数、p95、p99，以及响应较慢的搜索词。搜索日志的查看方法请参阅 :doc:`guide-08`

阅读日志
========

日志文件的种类
--------------

Fess 按处理类型将日志输出到不同的文件。
请根据要调查的内容选择打开的文件。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 文件
     - 内容
   * - ``fess.log``
     - Fess 本体（搜索页面、管理页面、API、调度器）的日志。启动失败、连接 OpenSearch 的错误、导入备份失败等
   * - ``fess-crawler.log``
     - 爬虫进程的日志。每个 URL 的获取错误、认证失败、爬虫内存不足等
   * - ``audit.log``
     - 登录、注销和管理操作的审计日志
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - 建议词生成、缩略图生成的日志
   * - ``fess-llm.log``
     - AI 搜索模式（RAG）和 LLM 集成的日志
   * - ``searchlog.log``
     - 每次搜索的记录（在 [通用] 中启用了「搜索日志」时）
   * - ``server_*.log``
     - Tomcat 的日志

存放位置因安装方式而异。

- ZIP 版：Fess 解压目录下的 ``logs/``
- RPM/DEB 版：``/var/log/fess/``
- Docker：容器内的 ``/var/log/fess/``。``fess.log``、``fess-crawler.log``、``audit.log`` 等也会输出到标准输出，因此可以用 ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01`` 查看。重建容器后会丢失

无论采用哪种安装方式，都可以在 [系统信息] > [日志文件] 中点击文件名下载。
无法登录服务器的人员也可以在这里查看日志。

各日志在日期变更或超过 100 MB 时会压缩为 ``.log.gz`` 并切换。
压缩文件中，``fess.log`` 和 ``searchlog.log`` 的会在 90 天后、``audit.log`` 的会在 360 天后自动删除。
而 ``fess-crawler.log``、``fess-suggest.log``、``fess-thumbnail.log`` 等爬虫和子进程日志的压缩文件不会被自动删除。
请监控日志目录的容量，并定期删除旧文件。

深入调查时
----------

默认情况下，``fess.log`` 输出 WARN 及以上级别，``fess-crawler.log`` 输出 INFO 及以上级别。
要让 ``fess.log`` 更详细，请将 [系统] > [通用] 中的「日志级别」提高到 ``INFO`` 或 ``DEBUG``。
此更改在重启 Fess 后会恢复原状。
爬虫的日志级别由作业脚本决定。
“Default Crawler”的脚本中包含 ``logLevel("info")``，在 [系统] > [调度器] 中将其改为 ``logLevel("debug")`` 后，从下一次爬取开始就会输出详细日志。
调查结束后请改回原值。
要永久更改级别，请参阅 `日志配置 <https://fess.codelibs.org/zh-cn/stable/config/admin-logging.html>`__。

在论坛等处咨询时，[系统信息] > [维护] 中「诊断」下的 [下载日志] 很有用。
它会下载一个 zip 文件，其中汇总了日志、``system.properties``、``fess_config.properties``、配置索引的内容以及 OpenSearch 的状态。
API 密钥和 ``app.cipher.key`` 等值会被替换为 ``XXXXXXXX``，但日志正文和配置索引的内容不会被屏蔽。
在交给外部之前，请检查其中的内容。

备份
====

数据存放在哪里
--------------

Fess 的数据分布在 3 个地方。
通过 [系统信息] > [备份] 只能获取其中的第 1 种。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 数据
     - 存放位置
     - 备份方法
   * - 爬取配置、调度器、标签、用户、[通用] 中的设置
     - OpenSearch 的配置索引和 ``system.properties``
     - [系统信息] > [备份]，或管理 API
   * - 已爬取的文档、字典（同义词、停用词等）
     - OpenSearch 的 ``fess.*`` 索引和 ``configsync`` 索引
     - OpenSearch 的快照（如果只备份字典，也可以复制文件）
   * - ``fess_config.properties``\ （包括 ``app.cipher.key``）、启动设置、已安装的插件
     - Fess 服务器上的文件
     - 复制文件，或使用配置管理

只要恢复了设置，已爬取的文档就可以通过重新爬取来重建。
仅在重新爬取耗时过长时才需要获取快照。

可从 [备份] 获取的文件
----------------------

[系统信息] > [备份] 中列出了以下文件。
点击名称即可逐个下载文件。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 文件
     - 内容
   * - ``fess_basic_config.bulk``
     - 爬取配置、调度器、标签、关键词匹配、Web/文件认证等设置
   * - ``fess_config.bulk``
     - 在上述内容的基础上，还包括爬网信息、失败 URL、作业日志、用户标签等
   * - ``fess_user.bulk``
     - 用户、角色、组
   * - ``system.properties``
     - [系统] > [通用] 中的设置
   * - ``fess.json`` / ``doc.json``
     - 文档索引的设置和映射
   * - ``*.ndjson``
     - 搜索日志、点击日志、收藏、AI 聊天日志、搜索用户。可以下载，但无法通过上传来恢复

用于恢复设置的是 ``fess_basic_config.bulk``、``fess_user.bulk`` 和 ``system.properties`` 这 3 个文件。
如果使用了用户标签，还要获取 ``fess_config.bulk``。

除后述的认证信息外，``*.bulk`` 中的设置值未经加密。
请将其作为机密文件保管。

用 cron 每天获取
----------------

通过管理 API ``GET /api/admin/backup/file/<文件名>/`` 可以获取与页面上相同的文件。
令牌按照前面“资源监控”中的相同步骤创建，并保存到只有运行脚本的用户才能读取的文件中。

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<令牌>" > /etc/fess-backup/token'

下面的脚本将文件保存到按日期命名的目录中，并删除超过 30 天的目录（保留期限仅为示例）。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Docker 环境：同时复制字典文件
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

要点如下。

- URL 末尾的 ``/`` 不能省略。由于文件名中含有点号，没有 ``/`` 时会被当作对静态文件的请求，返回 404
- 如果 ``curl`` 不加 ``-f``，404 或错误响应也会被保存到文件中，脚本看起来像是成功了。这里用 ``-f`` 和 ``set -e`` 使脚本在失败时停止
- 在 ZIP 版和 RPM/DEB 版中，请将 ``docker cp`` 这一行替换为复制 OpenSearch 端的字典目录（Fess 的 ``FESS_DICTIONARY_PATH`` 所指向的位置）

将脚本保存为 ``/usr/local/bin/fess-backup.sh`` 并赋予执行权限，然后登记到 root 的 crontab 中（以下是每天 2 点 30 分运行的示例）。

::

    30 2 * * * /usr/local/bin/fess-backup.sh

登记后请手动运行一次。
打开 ``fess_basic_config.bulk``，确认以 ``{"index":{"_index":`` 开头的行与设置内容的 JSON 行交替排列。
同样的处理也可以用 ``fessctl`` 编写（参见 :doc:`guide-16`）。

记下 app.cipher.key
-------------------

Fess 15.9 会使用 ``fess_config.properties`` 中的 ``app.cipher.key``，对 Web 认证和文件认证的密码，以及保存在爬取配置和数据存储配置参数中的密码和密钥进行加密后保存。
它们在 ``*.bulk`` 中也保持加密状态。
恢复到另一台服务器时，需要预先设置相同的 ``app.cipher.key``。
如果密钥不同，就无法解密，``fess-crawler.log`` 中会记录 ``CipherFailureException``，使用这些认证信息的爬取会失败。

``fess_config.properties`` 在 ZIP 版中位于 ``app/WEB-INF/classes/``，在 RPM/DEB 版中位于 ``/etc/fess/``。
如果修改过该值，请将此文件与 ``*.bulk`` 一样作为机密对待，并保管在其他位置。
在 Docker 中修改该值时，请在 ``compose.yaml`` 的 ``FESS_JAVA_OPTS`` 中指定 ``-Dfess.config.app.cipher.key=<值>``。
这样即使重建容器，也会使用相同的密钥。

.. warning::

   如果在保存认证信息之后修改 ``app.cipher.key``，之前保存的值将无法解密。
   如需修改，请在登记 Web 认证、文件认证或数据存储的认证信息之前进行。
   对于已在运行的环境，请不要修改该值，而是将其记录下来。

文档索引的快照
--------------

如果想不重新爬取就恢复文档，请使用 OpenSearch 的快照。
除了 ``fess*`` 之外，务必包含保存字典的 ``configsync`` 索引。
如果缺少 ``configsync``，恢复到新的 OpenSearch 时将没有字典文件，文档索引无法打开。

要使用快照，需要在 OpenSearch 端设置仓库路径（``path.repo``）。
docker-fess 的 ``compose-opensearch3.yaml`` 中没有设置该项，使用时请自行添加。
仓库的注册、快照的获取和恢复步骤请参阅 `索引管理 <https://fess.codelibs.org/zh-cn/stable/config/admin-index-backup.html>`__。
恢复需要在 Fess 停止的状态下进行，并且必须先恢复 ``configsync``。

恢复
====

恢复前需要了解的事项
--------------------

从 [备份] 恢复并不是整体替换 OpenSearch 内容的操作。

- 恢复只能通过上传进行。管理 API 仅用于下载，没有用于恢复的 API
- ``*.bulk`` 中的各项设置，仅在服务器上不存在相同设置、或比服务器上的更新时才会写入。获取备份之后修改过的设置不会恢复为旧的内容
- 获取备份之后创建的设置不会被删除，而是保留下来

因此，它不适合“将误改的设置恢复到昨天的状态”这类用途。
请将其用于迁移到新服务器，或恢复重建后的环境。

将设置恢复到另一台服务器的步骤
------------------------------

1. 在迁移目标上安装相同版本的 Fess，并将 ``fess_config.properties`` 中的 ``app.cipher.key`` 设为与迁移源相同的值
2. 安装迁移源上使用的插件（数据存储、SSO 等），然后重启 Fess
3. 登录管理页面，打开 [系统信息] > [备份]
4. 在「批量文件」中选择 ``fess_basic_config.bulk``，点击 [上传]。页面会显示“批量处理已启动。”
5. 用同样的方法上传 ``fess_user.bulk`` 和 ``system.properties``。如果使用了用户标签，还要上传 ``fess_config.bulk``\ （迁移源的爬网信息和作业日志也会一并导入）

导入在后台进行。
稍等片刻后，确认以下几点。

- [爬虫] > [Web]、[文件系统]、[数据存储] 以及 [系统] > [调度器] 中列出了迁移源的设置
- [用户] > [用户] 中列出了迁移源的用户
- [系统] > [通用] 中的通知目标等已变为迁移源的值

最后，恢复字典并重建文档。

- 字典：在 [系统] > [字典] 中打开各类型的页面，上传备份的字典文件。然后执行 [系统信息] > [维护] 中的「重新加载文档索引」。重新加载期间会有短暂的无法搜索
- 文档：在 [系统] > [调度器] 中点击“Default Crawler”的 [立即开始] 重新爬取。如果从快照恢复，请按照前述步骤操作

爬取结束后，在 [系统信息] > [爬网信息] 中确认已索引的文档数。
如果带认证的爬取配置文档数为 0，请检查 ``fess-crawler.log`` 中是否有 ``CipherFailureException``。
如果有，说明 ``app.cipher.key`` 与迁移源不一致。

应对故障
========

下面汇总常见的症状以及在 Fess 中应检查的位置。

搜索页面打不开，或 /api/v2/health 返回 503
------------------------------------------

1. 检查 OpenSearch 的状态。如果 ``curl -s "http://localhost:9200/_cluster/health?pretty"`` 的 ``status`` 为 ``red``，则是 OpenSearch 端的问题。在 Docker 中请查看 ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01``
2. 如果 OpenSearch 正常而 Fess 没有响应，请检查 ``fess.log`` 中启动时的错误
3. 如果刚从快照恢复后就变为 ``red``，可能是没有恢复 ``configsync``\ （见前文）

爬取失败，或已索引的文档数减少
------------------------------

1. 在 [系统信息] > [作业日志] 中打开相应作业的行，查看「结果」
2. 在 [系统信息] > [爬网信息] 中，将最新会话的「爬虫状态」和索引大小与上次进行比较
3. 在 [系统信息] > [失败URL] 中，查看未能获取的 URL 的「类型」「日志」「错误数」。HTTP 的 404、403、410、401 也会记录在这里
4. 详细信息在 ``fess-crawler.log`` 中。用失败 URL 详情中的「线程名称」进行搜索，可以追踪当时前后的日志

如果 ``fess-crawler.log`` 中有 ``OutOfMemoryError``，说明爬虫进程的堆不足。
爬虫的堆由 ``fess_config.properties`` 中的 ``jvm.crawler.options``\ （默认 ``-Xmx512m``）决定，与 Fess 本体的堆相互独立。
调整方法请参阅 :doc:`guide-14`。

收不到通知
----------

对于邮件，首先用 [通用] 中的 [发送测试邮件] 确认能否收到。
如果只有爬取完成的邮件收不到，请检查 ``fess_env_crawler.properties`` 中的 SMTP 服务器。
在 Docker 中，还要确认是否因为用 ``down`` 和 ``up`` 重建了容器而导致 [通用] 中的设置丢失。
如果只有日志通知收不到，请确认「Log Notification」是否已启用、“Log Notification”作业是否已启用，以及「Log Notification Level」（作业失败为 ``WARN``）是否合适。
其他检查项请参阅 `日志通知 <https://fess.codelibs.org/zh-cn/stable/config/admin-log-notification.html>`__ 中的“故障排除”。

搜索缓慢
--------

1. 在 [系统信息] > [搜索日志] 的 [性能] 标签页中，确认是特定搜索词慢还是整体都慢
2. 将 ``/api/admin/stats`` 中的 ``jvm.memory.heap.percent`` 和 ``jvm.gc`` 的累计时间与变慢之前进行比较

延伸阅读
========

- 想用脚本或 ``fessctl`` 管理设置：:doc:`guide-16`
- 想调整堆，或将 OpenSearch、Fess 扩展为多台：:doc:`guide-14`
- 想通过 SSO、审计日志等加强访问保护：:doc:`guide-15`
- 想根据搜索日志改进搜索质量：:doc:`guide-08`

参考资料
========

- `Health API <https://fess.codelibs.org/zh-cn/stable/api/api-health.html>`__
- `Stats API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-stats.html>`__
- `日志通知 <https://fess.codelibs.org/zh-cn/stable/config/admin-log-notification.html>`__
- `日志配置 <https://fess.codelibs.org/zh-cn/stable/config/admin-logging.html>`__
- `日志文件 <https://fess.codelibs.org/zh-cn/stable/admin/log-guide.html>`__
- `备份 <https://fess.codelibs.org/zh-cn/stable/admin/backup-guide.html>`__
- `Backup API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-backup.html>`__
- `索引管理 <https://fess.codelibs.org/zh-cn/stable/config/admin-index-backup.html>`__
- `失败URL <https://fess.codelibs.org/zh-cn/stable/admin/failureurl-guide.html>`__
- `维护 <https://fess.codelibs.org/zh-cn/stable/admin/maintenance-guide.html>`__
