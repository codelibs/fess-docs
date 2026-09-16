====================
fess-setup 命令
====================

``bin/fess-setup``\ （Windows 上为 ``bin\fess-setup.bat``\ ）随 |Fess| 的 ZIP 包提供。它用于安装 |Fess| 需要但发行包中未包含的内容：带有 |Fess| 所需插件的 OpenSearch、Playwright 爬虫所需的 Node.js，以及 |Fess| 插件。它还可以检查安装状态。

请在 |Fess| 目录中运行。不带参数运行时，会显示命令列表。

::

    $ cd /path/to/fess-15.9.0
    $ bin/fess-setup <command> [options]

退出码
======

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 退出码
     - 含义
   * - ``0``
     - 命令执行成功。
   * - ``1``
     - 命令执行失败：例如下载失败、指定的版本不存在、OpenSearch 没有面向当前平台的发行版，或 ``check`` 发现了问题。
   * - ``2``
     - 命令行有误：未知的命令，或缺少插件名称等参数。

安装 OpenSearch 和 Node.js
==========================

install opensearch
------------------

::

    $ bin/fess-setup install opensearch [--dest <dir>] [--version <version>]

将此 |Fess| 支持的 OpenSearch 版本下载到 |Fess| 目录下的 ``opensearch/`` 中，安装 |Fess| 所需的 4 个插件（\ ``opensearch-analysis-fess``\ 、\ ``opensearch-analysis-extension``\ 、\ ``opensearch-minhash`` 和 ``opensearch-configsync``\ ），并向其 ``config/opensearch.yml`` 追加以下配置：

- ``configsync.config_path``\ ，其值为该 OpenSearch 的 ``config/dictionary`` 目录
- ``plugins.security.disabled: true``

``opensearch.yml`` 中已有的配置不会重复追加；如果该文件中存在任何 ``plugins.security.*`` 配置，则不会追加 ``plugins.security.disabled: true``\ 。OpenSearch 目录已存在时会跳过下载，因此对已有的安装再次运行该命令时，只会追加缺少的配置。

命令会显示追加的每项配置，然后显示 ``bin/fess.in.sh`` 能否自动找到此 OpenSearch。当它是 |Fess| 目录下 ``opensearch/`` 中唯一带有 ``config/dictionary`` 目录的 OpenSearch 时即可找到：此时 ``bin/fess.in.sh``\ （Windows 上为 ``bin\fess.in.bat``\ ）会将 ``FESS_DICTIONARY_PATH`` 设置为该目录，对于在同一主机上运行的 OpenSearch，无需其他配置。否则，命令会显示需要设置的 ``SEARCH_ENGINE_HTTP_URL`` 和 ``FESS_DICTIONARY_PATH`` 的值，设置方法请参阅 :doc:`install-linux` 或 :doc:`install-windows`\ 。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 选项
     - 说明
   * - ``--dest <dir>``
     - 指定 OpenSearch 的解压目录，以代替 |Fess| 目录下的 ``opensearch/``\ 。\ ``bin/fess.in.sh`` 不会在该目录之外查找 OpenSearch。
   * - ``--version <version>``
     - 要安装的 OpenSearch 版本。插件也会以相同版本安装。

OpenSearch 仅为 Linux 和 Windows 发布官方发行版。在 macOS 等其他平台上，该命令不会下载任何内容，而是以退出码 ``1`` 结束，并建议使用 Homebrew 安装 OpenSearch 后通过 ``install opensearch-plugins`` 添加插件，或者使用 Docker。

.. warning::

   设置了 ``plugins.security.disabled: true`` 的 OpenSearch 会接受未经认证的请求。除非设置了 ``network.host``\ ，OpenSearch 只在回环地址上监听。在让它监听其他地址之前，请改为配置安全插件；详情请参阅 :doc:`security`\ 。

install opensearch-plugins
--------------------------

::

    $ bin/fess-setup install opensearch-plugins --opensearch-home <dir> [--version <version>]

向已有的 OpenSearch 安装 |Fess| 所需的 4 个插件，可代替执行 4 次该 OpenSearch 的 ``bin/opensearch-plugin install``\ 。\ ``--opensearch-home`` 为 OpenSearch 的安装目录，必须指定。\ ``--version`` 用于设置插件版本，该版本必须与 OpenSearch 版本一致。

此命令不会修改 ``opensearch.yml``\ 。请按照 :doc:`install-linux` 或 :doc:`install-windows` 的说明，自行添加 ``configsync.config_path`` 等配置。

install nodejs
--------------

::

    $ bin/fess-setup install nodejs [--dest <dir>] [--version <version>]

将 Playwright 爬虫所需的 Node.js 下载到 |Fess| 目录下的 ``nodejs/`` 中。\ ``bin/fess.in.sh``\ （Windows 上为 ``bin\fess.in.bat``\ ）会在该位置找到它并设置 ``PLAYWRIGHT_NODEJS_PATH``\ 。使用 ``--dest`` 解压到 |Fess| 目录之外时，命令会改为显示需要添加到 ``bin/fess.in.sh`` 中的 ``PLAYWRIGHT_NODEJS_PATH`` 行。\ ``--version`` 用于选择其他版本的 Node.js。关于 Playwright 爬虫，请参阅 :doc:`../config/crawler-advanced`\ 。

管理插件
========

以下命令操作 |Fess| 安装中的插件目录 ``app/WEB-INF/plugin``\ 。安装、升级或删除插件后，请重启 |Fess|\ 。也可以在管理界面的「系统 > 插件」页面管理插件；请参阅 :doc:`../admin/plugin-guide`\ 。

``install plugin``\ 、\ ``list plugins`` 和 ``upgrade plugins`` 可以指定 ``--repository <url>``\ 。指定后，版本列表、jar 及其校验和都从该单个 Maven 仓库（例如内部镜像）获取，而不使用默认的发布仓库、快照仓库和 GitHub。

install plugin
--------------

::

    $ bin/fess-setup install plugin <name>[:<version>]... [--version <version>] [--repository <url>]

安装一个或多个 |Fess| 插件，例如 ``fess-script-groovy`` 或 ``fess-ds-git``\ 。未指定版本的名称会安装为此 |Fess| 构建的最新版本。\ ``<name>:<version>`` 用于固定该插件的版本，\ ``--version`` 则作为所有未指定版本的名称的版本。新版本安装完成后，将删除同一插件之前安装的版本。

jar 从插件的 GitHub 发布获取；发布中没有对应文件时，则从 Maven 仓库获取，并使用 Maven 仓库公布的 SHA-1 校验和进行校验。\ |Fess| 的开发版还会安装其同一版本系列的快照构建，并优先使用快照构建。

使用示例请参阅 :doc:`../admin/plugin-guide`\ 。

list plugins
------------

::

    $ bin/fess-setup list plugins [--repository <url>]

列出为此 |Fess| 发布的插件，并用 ``(installed: <version>)`` 标记已安装的插件。已安装但未在仓库中发布的插件（例如本地构建的 jar）会单独列出。\ |Fess| 的开发版还会列出快照仓库中的插件。

list installed
--------------

::

    $ bin/fess-setup list installed

列出已安装的插件及其版本，不访问仓库。

upgrade plugins
---------------

::

    $ bin/fess-setup upgrade plugins [--repository <url>]

将所有已安装的插件以适合此 |Fess| 的版本重新安装。已经是该版本的插件保持不变。\ ``app/WEB-INF/plugin`` 中的插件是为特定的 |Fess| 发布版本构建的，因此请在升级 |Fess| 后运行此命令。

remove plugin
-------------

::

    $ bin/fess-setup remove plugin <name>...

删除指定插件已安装的 jar。未安装的名称只会给出提示，不影响退出码。

检查安装状态
============

list
----

::

    $ bin/fess-setup list

显示 ``install`` 下载的组件（\ ``opensearch`` 和 ``nodejs``\ ）及各自的版本。

check
-----

::

    $ bin/fess-setup check [--url <engine url>] [--playwright]

检查安装状态，每个检查项输出一行，并标记为 ``OK``\ 、\ ``WARN`` 或 ``FAIL``\ ：

- 搜索引擎：能否连接、版本（各节点报告的版本不一致时为警告）、是否安装了 |Fess| 所需的 4 个插件，以及 ``configsync`` 是否响应。
- |Fess|\ ：插件目录是否存在且可写、每个已安装的插件（为其他 |Fess| 发布版本构建的插件，以及安装了两个版本的插件，均为失败），以及 |Fess| 目录下的 ``nodejs/`` 中是否安装了 Node.js。

搜索引擎的 URL 为 ``--url``\ ，未指定时为环境变量 ``SEARCH_ENGINE_HTTP_URL``\ ，仍未设置时为 ``http://localhost:9200``\ 。\ ``bin/fess-setup`` 不读取 ``bin/fess.in.sh``\ ，因此当 OpenSearch 位于其他位置时，请指定 ``--url``\ 。缺少 Node.js 时只会报告，但指定 ``--playwright`` 后会视为失败。

没有检查项失败时，即使有警告，命令也以退出码 ``0`` 结束；否则以退出码 ``1`` 结束。
