==================================
用代码管理 Fess 配置并重建相同环境
==================================

前言
====

在管理界面中逐步积累的设置，事后无法追溯是谁在什么时候改了什么。
把在测试环境中验证过的设置搬到生产环境时，也只能手动重复同样的界面操作。

本文将 Fess 15.9 的设置写成 Git 仓库中的文件，用脚本将其应用到新启动的 Docker 环境，并一直进行到确认设置已经生效为止。
使用的是 docker-fess 的 Compose 文件、Fess 的管理 API（Admin API）以及它的 CLI 工具 fessctl。

本文不涉及备份的范围和恢复步骤。
请参阅 :doc:`guide-10`。

按存放位置决定管理方式
======================

Fess 的设置并不集中在一个地方。
存放位置不同，转换为代码的方法也不同。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 设置
     - 存放位置
     - 转换为代码的方法
   * - Fess 版本、插件
     - Docker 镜像、容器
     - Compose 文件中的镜像标签和 ``FESS_PLUGINS``
   * - ``fess_config.properties`` 中的项目（如 ``app.cipher.key``）
     - 容器内的文件
     - ``FESS_JAVA_OPTS`` 中的 ``-Dfess.config.<键>``
   * - [系统] > [通用] 中的项目
     - 容器内的 ``system.properties``
     - ``FESS_JAVA_OPTS`` 中的 ``-Dfess.system.<键>``
   * - 爬网配置、标签、调度器、用户等
     - OpenSearch 中的配置用索引
     - 管理 API（fessctl）
   * - 字典（同义词等）
     - OpenSearch 容器的 ``FESS_DICTIONARY_PATH``
     - 通过管理 API 上传字典（fessctl）
   * - 访问令牌、加密密钥的值
     - 令牌在 OpenSearch 中，加密密钥在启动选项中
     - 不放入 Git，而是放在 ``.env`` 或 CI 的 Secrets 中

docker-fess 的 ``fess01`` 容器没有卷，因此 ``system.properties`` 会在 ``docker compose down`` 时随容器一起消失。
保存在 OpenSearch 中的爬网配置等则会保留在卷中。

仓库结构
========

本文用 Git 管理以下文件。

::

    fess-infra/
    ├── compose.yaml               docker-fess v15.9.0 的文件
    ├── compose-opensearch3.yaml   docker-fess v15.9.0 的文件
    ├── compose-site.yaml          针对自己环境的差异
    ├── dict/
    │   └── synonym.txt            同义词词典
    ├── apply.sh                   应用设置的脚本
    ├── .gitignore
    └── .env                       不放入 Git（加密密钥和令牌）

连同版本一起固定 Docker 配置
============================

获取 Compose 文件
-----------------

获取 docker-fess ``v15.9.0`` 标签下的文件。
``compose.yaml`` 指向镜像 ``ghcr.io/codelibs/fess:15.9.0``，``compose-opensearch3.yaml`` 指向 ``ghcr.io/codelibs/fess-opensearch:3.9.0``，因此版本是固定的。

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

不要编辑这两个文件，自己环境的差异写在另一个文件中。
这样在升级 docker-fess 时，只需重新获取这些文件即可。

编写自己环境的差异
------------------

创建 ``compose-site.yaml``。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- ``FESS_PLUGINS`` 中以 ``名称:版本`` 的格式、用空格分隔写出启动时要获取的插件。版本与 Fess 相同，使用 15.9.x。示例中的 ``fess-ds-git`` 是用数据存储爬取 Git 仓库时使用的插件。获取来源固定为 ``maven.codelibs.org``，因此这里只能写已公开发布的插件，并且容器需要能够访问互联网
- ``-Dfess.config.<键>`` 优先于 ``fess_config.properties`` 中的同名项目
- ``-Dfess.system.<键>`` 会成为 [通用] 中项目的默认值。示例中的 ``purge.searchlog.day`` 是 [通用] 中「删除以前的搜索日志」的天数

Compose 按变量名合并 ``environment``，因此 ``compose.yaml`` 中的 ``SEARCH_ENGINE_HTTP_URL`` 等变量会原样保留。
不过，如果在多个文件中写了同一个变量，则会被后面文件中的值替换。
``compose-openai.yaml`` 等叠加文件也会设置 ``FESS_PLUGINS`` 和 ``FESS_JAVA_OPTS``，组合使用时请把这些值合并到一个文件中。

.. note::

   只有当 ``system.properties`` 中没有该键时，才会使用 ``-Dfess.system.<键>``。
   只要在管理界面的 [通用] 中保存过一次，或执行过 ``fessctl general update``，界面上的各项目就会写入 ``system.properties``，此后以那里的值为准。
   在这种状态下，即使修改 ``compose-site.yaml`` 中的值，在执行 ``down`` 并重新创建容器之前也不会生效。

确定加密密钥
------------

``app.cipher.key`` 是用于加密 Web 认证、文件认证的密码，以及保存在爬网配置、数据存储配置参数中的机密值的密钥。
不要沿用默认值 ``___change__me___``，请在首次启动前确定。

密钥字符串会直接用作 AES 密钥，因此长度必须为 16、24 或 32 字节之一。
``openssl rand -hex 16`` 的输出（32 个十六进制字符）为 32 字节。

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

如果在保存认证信息之后更改密钥，已保存的值将无法解密，使用这些设置的爬取会失败。
将备份恢复到其他环境时也需要同一个密钥（:doc:`guide-10`）。
除 ``.env`` 外，还应在密码管理工具等处另存一份。

``FESS_JAVA_OPTS`` 的值可以通过 ``docker inspect`` 看到。
如果想避免这一点，可以改用将 ``fess_config.properties`` 挂载到 ``/opt/fess`` 的方法（参见 `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__ 中的“如何应用配置文件”）。

启动
----

每次执行 Compose 命令时都要指定这 3 个文件。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

``fess01`` 的健康检查会调用 ``/api/v2/health``，当 ``docker compose ... ps`` 显示 ``fess01`` 为 ``(healthy)`` 时即准备就绪。

创建管理 API 用的访问令牌
=========================

调用管理 API 需要访问令牌，而创建令牌的 API 没有令牌也无法调用。
因此，每个新环境都需要在管理界面中手动创建第一个令牌，仅此一次。

1. 使用 ``admin`` / ``admin`` 登录 ``http://localhost:8080/admin/``，按要求设置新密码（8 个字符以上）
2. 打开 [系统] > [访问令牌]，点击 [新建]
3. 在「名称」中输入 ``fess-infra``，在「权限」中输入 ``{role}admin-api``，然后点击 [创建]
4. 从列表中打开创建的令牌，复制「令牌」的值

将复制的值追加到 ``.env``。

::

    $ echo 'FESS_ACCESS_TOKEN=<复制的值>' >> .env

拥有 ``{role}admin-api`` 的令牌可以执行管理 API 的所有操作。
包括更改设置、创建用户乃至下载备份，无法创建限定用途的令牌。
请像对待管理员密码一样对待它，不要放入 Git 或在浏览器中运行的 JavaScript 中。

准备 fessctl
============

fessctl 是调用管理 API 的命令行工具。
安装带有 Fess 15.9 默认值的 0.4.0，并固定版本。
需要 Python 3.13 或更高版本。

::

    $ pipx install fessctl==0.4.0

也可以使用 ``uv tool install fessctl==0.4.0``。
后面的脚本还会使用 ``jq`` 和 ``curl`` 从响应中提取值。

fessctl 从 ``FESS_ENDPOINT``\ （默认值 ``http://localhost:8080``）读取连接目标，从 ``FESS_ACCESS_TOKEN`` 读取令牌，从 ``FESS_VERSION`` 读取所连接 Fess 的版本。
``FESS_VERSION`` 请指定为 ``15.9.0``。
这是因为不同版本调用 API 的方式不同。

确认连接。

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

如果集群状态为 GREEN 或 YELLOW，``ping`` 会以退出码 0 结束。
健康检查没有令牌也能通过，因此要用 ``webconfig list`` 确认令牌是否有效。
如果出现认证错误，请检查令牌的值和权限。
所有命令加上 ``-o json`` 后都会原样输出管理 API 的响应，因此可以用 ``jq`` 提取值。

将字典的初始内容放入 Git
------------------------

上传字典会替换整个文件。
为了不丢失默认内容，先下载当前的同义词词典放入仓库，再对其进行编辑。

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

下载的文件中已包含默认的同义词 ``fess,フエス``\ 。
在文件末尾追加一行同义词。
用逗号分隔的词，无论用其中哪一个搜索，都能找到包含其他词的文档（格式请参阅 `同义词词典 <https://fess.codelibs.org/zh-cn/stable/admin/synonym-guide.html>`__）。

::

    设置,配置

登记日语词时，平假名要写成片假名，小写片假名要写成普通大小的片假名（“フェス”写成“フエス”），全角英文数字要写成半角英文数字。

应用设置的脚本
==============

在 ``apply.sh`` 中，以 fessctl 命令的形式写出要放入环境的设置。
它以在新环境上运行为前提，但如果已有同名设置就会跳过创建，因此再次运行也不会产生重复。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # 标签：爬取时添加到与目标路径匹配的文档上
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Fess 文档" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/zh-cn/stable/.*' \
        --permission '{role}guest'
    fi

    # Web 爬网配置
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Fess 搜索指南")' > /dev/null; then
      fessctl webconfig create --name "Fess 搜索指南" \
        --url https://fess.codelibs.org/zh-cn/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/zh-cn/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # 同义词词典：替换整个文件，然后重新打开文档索引使其加载
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # 开始爬取，并等待作业结束
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

脚本的要点如下。

- 使用默认的文本输出时，API 返回错误后 fessctl 会以非 0 的退出码结束，因此 ``set -e`` 会让脚本中途停止。使用 ``-o json`` 时，很多命令会输出错误响应并以 0 结束，所以要用 ``jq -e`` 检查提取出的值。如果没有值，jq 就会失败，脚本在此停止
- 在 fessctl 0.4.0 中，``labeltype create`` 的 ``--version-no`` 是必需的。新建时指定 ``1``
- ``webconfig create`` 中省略的项目会使用 fessctl 的默认值。``--depth`` 为 ``1``，``--max-access-count`` 为 ``1000000``，因此预期的值不要省略，要写出来。``--permission`` 的默认值是 ``{role}guest``
- 标签的值只能使用字母数字和 ``_``。标签是在爬取时添加的，因此要先于爬网配置创建
- 上传字典时如果不加 ``--yes``，会要求确认并停下来
- 同义词词典在搜索时生效，但 OpenSearch 只在打开索引时构建分析器。因此先用 ``_configsync/flush`` 将字典写出到文件，再 close / open ``fess.update``。在此期间无法搜索，所以在运行中的环境里要在访问量少的时段执行。这与管理界面 [系统信息] > [维护] 中的「重新加载文档索引」是同一操作
- ``scheduler start`` 响应中的 ``job_log_id`` 直接就是 [作业日志] 中的 ID。脚本会等待作业状态变为 ``ok`` 或 ``fail``，如果不是 ``ok`` 就以失败结束。“Default Crawler”会执行所有已启用的爬网配置

修改已有设置的值时，这个脚本只会跳过创建，不会改写值。
请像 ``fessctl webconfig update <ID> --max-access-count 100`` 这样指定 ID 进行更新，或者在连同卷一起重建的环境上重新运行。

从 CI 运行脚本时，不放置 ``.env``，而是通过环境变量从 CI 的 Secrets 中传入 ``FESS_ACCESS_TOKEN`` 和 ``FESS_ENDPOINT``。
这种情况下，请把含有 ``localhost:9200`` 的 3 行改写为能够访问到 OpenSearch 的地址。

确认设置已经生效
================

``apply.sh`` 以退出码 0 结束后，按以下顺序确认。

1. 插件已安装

   ::

       $ fessctl plugin installed

   如果列表中有 ``fess-ds-git`` 的 15.9.0，就说明已经安装。
   ``FESS_PLUGINS`` 中的插件即使获取失败，Fess 也照样启动，只会在 ``docker compose ... logs fess01`` 中出现 ``Failed to download``，因此要在这里确认。

2. [通用] 的值已生效

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   如果返回 ``180``，说明 ``-Dfess.system.purge.searchlog.day`` 已生效。
   管理 API 中的名称是 ``purge_search_log_day`` 这样的 snake_case，与 ``-Dfess.system.`` 后面的键不同。

3. 字典已被替换

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep '配置'

   如果显示出追加的那一行，就说明上传成功。
   也可以用 ``fessctl dict synonym list`` 确认，但默认每次只显示 100 条，追加在末尾的行可能不会出现在第一页。

4. 可以按标签搜索

   ::

       $ curl -fsS --get --data-urlencode 'q=搜索' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   如果返回 1 或以上，说明从爬取、添加标签到搜索都已打通。
   如果为 0，请在管理界面中查看 [系统信息] > [失败URL] 以及 [作业日志] 的结果。

直接调用管理 API
================

fessctl 调用的是 ``/api/admin/`` 下的管理 API。
像爬网配置这样带有设置的资源，都是以下形式（``<resource>`` 为 ``webconfig``、``fileconfig``、``dataconfig``、``labeltype``、``keymatch`` 等）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 请求
     - 操作
   * - ``GET /api/admin/<resource>/settings``
     - 列表
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - 获取 1 条
   * - ``POST /api/admin/<resource>/setting``
     - 创建
   * - ``PUT /api/admin/<resource>/setting``
     - 更新
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - 删除

fessctl 也有同名的子命令（``create``、``list``、``get``、``update``、``delete``），可以像 ``fessctl fileconfig create --help`` 这样查看各项目。
字典上传以 multipart 方式发送到 ``POST /api/admin/dict/<类型>/upload/<字典ID>``。
文件字段的名称因类型而异，同义词为 ``synonymFile``。
JSON 字段名是 ``max_access_count`` 这样的 snake_case。
各字段请参阅从 `Admin API 概述 <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-overview.html>`__ 可以找到的各资源页面。

以下命令返回 Web 爬网配置的数量。

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

如果不加 ``-f``，即使是 404 或 401 响应 curl 也会视为成功，脚本就察觉不到失败。

获取设置的副本
==============

为应对没有写入 Git 的设置（例如在管理界面中直接修改的设置），还要定期获取备份。
涉及的文件和恢复步骤在 :doc:`guide-10` 中说明。
这里只给出一个与 ``apply.sh`` 使用相同准备即可运行的脚本示例。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_VERSION=15.9.0
    dest="backup/$(date +%Y%m%d)"
    umask 077
    mkdir -p "$dest"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      fessctl backup download "$id" --dest "$dest/$id" --force
    done

``fessctl backup download`` 会在 URL 末尾加上 ID 含点号时所需的 ``/``，调用 ``/api/admin/backup/file/<ID>/``。
用 curl 调用时，请不要忘记末尾的 ``/`` 和 ``-f``。
如果末尾没有 ``/``，会返回 404。

管理 API 只能做到下载，恢复只能在管理界面的 [系统信息] > [备份] 中进行。
备份并不能成为重建另一个环境的步骤，因此设置的正本应放在 ``apply.sh`` 一侧。

不能放入 Git 的内容
===================

- ``.env``\ （加密密钥和访问令牌）
- 备份文件。``*.bulk`` 中也包含未加密的值，必须作为机密文件处理。``system.properties`` 中也会包含在 [通用] 中输入的存储密钥、SSO 客户端密钥等

正因如此，才把 ``.env`` 和 ``backup/`` 写入了 ``.gitignore``。
备份请保存在加密存储等限制了访问的地方。

接下来阅读
==========

- 想完善备份对象、恢复和监控：:doc:`guide-10`
- 想确认用 Docker 启动和停止的基础知识：:doc:`guide-02`
- 想从业务系统调用搜索 API：:doc:`guide-11`
- 想在包括访问令牌管理和 SSO 在内的方面保护管理界面：:doc:`guide-15`
- 想自己开发插件：:doc:`guide-17`

参考资料
========

- `使用 Docker 安装（详细） <https://fess.codelibs.org/zh-cn/stable/install/install-docker.html>`__
- `Admin API 概述 <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-overview.html>`__
- `Dict API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-dict.html>`__
- `Backup API <https://fess.codelibs.org/zh-cn/stable/api/admin/api-admin-backup.html>`__
- `字典（生效时机） <https://fess.codelibs.org/zh-cn/stable/admin/dict-guide.html>`__
- `访问令牌 <https://fess.codelibs.org/zh-cn/stable/admin/accesstoken-guide.html>`__
- `fessctl（GitHub） <https://github.com/codelibs/fessctl>`__
- `docker-fess（GitHub） <https://github.com/codelibs/docker-fess>`__
