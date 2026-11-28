================
数据存储爬取基础
================

前言
====

Google Drive、Slack 和数据库中的内容，无法通过 Web 爬取或文件爬取变为可搜索。
CSV 文件通过文件爬取时，一个文件只会成为一个文档，无法按行搜索。
Fess 将这些数据源作为“数据存储”，通过插件（数据存储连接器）以记录为单位导入。

数据存储的配置页面与 Web 和文件系统的配置页面项目不同。
需要自己编写将哪个值作为 URL 或标题，而且如果保持初始值，文档会以无需登录即可搜索的状态注册。
即使处理失败，作业有时也会显示为“OK”。

本文基于 Fess 15.9 说明所有连接器通用的机制。
通过一个使用 CSV 文件的小示例，完整地走一遍从安装插件、配置、执行到确认结果的过程。
各连接器的认证和参数，请参阅文末列出的各篇文章和参考文档。

与 Web 爬取、文件爬取的区别
===========================

在 Web 爬取和文件爬取中，Fess 会沿着链接和文件夹遍历，并从获取的文档中自动提取标题和正文。
在数据存储爬取中，由连接器从 API 或文件中读取记录。
记录中的哪个值放入索引的哪个字段，需要写在配置的「脚本」中。

Fess 本体不包含数据存储的处理程序。
[爬虫] > [数据存储] 的「处理程序名称」下拉列表中显示的，只有已安装的 ``fess-ds-*`` 插件所提供的处理程序。

此外，数据存储的配置还有以下区别（在后面的章节中说明）。

- 配置页面中没有「标签」项目
- 不应用 [爬虫] > [文档提升] 的规则

安装插件
========

这里以 CSV 连接器 ``fess-ds-csv`` 为例。
插件版本应与所用 Fess 的次版本号一致（15.9 则使用 15.9.x）。

从管理页面安装时，在 [系统] > [插件] 中点击 [安装]。
在 [远程] 选项卡的下拉列表中选择 ``fess-ds-csv``\ ，然后点击 [安装]。
使用本地已有的 jar 文件时，请使用 [本地] 选项卡。

在通过 ZIP 包或 RPM / DEB 安装的环境中，也可以从命令行安装。

.. code-block:: bash

    bin/fess-setup install plugin fess-ds-csv:15.9.0

在 Docker 中，向 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 添加 ``FESS_PLUGINS``\ ，在启动时安装。
多个插件用空格分隔列出（不是逗号分隔）。

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-csv:15.9.0"

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

在 Docker 中从管理页面安装的插件位于容器内，因此重新创建容器后就会消失。
在 Docker 中使用 ``FESS_PLUGINS`` 更为可靠。
修改环境变量后执行 ``up -d``\ ，容器会被重新创建。
关于此时会丢失的设置，请参阅 :doc:`guide-02`\ 。

通过管理页面或 ``fess-setup`` 安装时，请重启 Fess（\ ``FESS_PLUGINS`` 在 Fess 启动前安装插件，因此无需重启）。
重启后，如果 [爬虫] > [数据存储] > [新建] 的「处理程序名称」中显示 ``CsvDataStore``\ ，则说明已安装成功。

配置页面的 3 个字段
===================

数据存储配置的核心是「处理程序名称」「参数」「脚本」这 3 个字段。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 字段
     - 内容
   * - 处理程序名称
     - 使用的连接器。例：``CsvDataStore``\ 、\ ``SlackDataStore``
   * - 参数
     - 对连接器的指示。每行写一个 ``键=值``\ （要读取的文件、连接目标、认证信息等）
   * - 脚本
     - 与索引字段的对应关系。每行写一个 ``字段名=表达式``

参数中的 ``script_type``
------------------------

新建页面的「参数」字段中，默认已填入 ``script_type=javascript``\ 。
这表示用 JavaScript 来计算「脚本」字段中的表达式。
请保留这一行，在其下方添加连接器的参数。

如果删除 ``script_type`` 行，脚本将作为 Groovy 计算（这是为了让 15.9 之前创建的配置继续工作的默认值）。
用 Groovy 计算需要 ``fess-script-groovy`` 插件。
标准 Docker 镜像中包含该插件，但 slim 镜像中不包含。
在没有该插件的环境中，含有表达式的行会因 ``groovy is not found`` 错误而计算失败，该记录不会被注册（像 ``title=subject`` 这样右侧只有项目名的行，不经过脚本引擎，直接使用其值）。
反之，在标准 Docker 镜像中，即使删除了这一行，也会以 Groovy 计算并正常运行，因此不容易察觉。
将连接器参考文档中的示例粘贴到「参数」字段时，请注意不要删除 ``script_type=javascript`` 行。

脚本的写法
----------

「脚本」字段的每一行，左侧是索引的字段名，右侧是 JavaScript 表达式。
字符串用双引号括起来。
请不要在行尾加分号。
加了分号后，表达式的值会变为 ``null``\ ，该字段不会被设置任何内容。
由于不会输出错误或日志，只能通过字段为空来察觉（详情请参阅文末参考文档中的“JavaScript脚本指南”）。

右侧可以引用的项目名因连接器而异。

- CSV、JSON、数据库连接器直接引用列名或字段名（CSV 也可以用 ``cell1``\ 、\ ``cell2`` … 引用）
- 许多云服务类连接器会给获取的对象加上前缀后传递。例如 Box、Google Drive、OneDrive 为 ``file.*``\ ，Slack 为 ``message.*``\ ，Jira 为 ``issue.*``\ ，Salesforce 为 ``object.*``

可用的项目名请在各连接器参考文档（\ ``https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-<名称>.html``\ ）的脚本说明中确认。
如果引用了未定义的名称，例如应写 ``file.url`` 却写成了 ``url``\ ，表达式的计算会失败，该记录不会被注册。

示例：让 CSV 文件可被搜索
=========================

这是一个用 CSV 管理公司内部 FAQ，并使其可被搜索的示例。
将以下内容以 UTF-8 编码保存为 ``faq.csv``\ 。

.. code-block:: text

    faq_id,question,answer
    1,费用报销的截止日期是什么时候,请在每月月底前提交费用报销申请。
    2,如何从公司外部连接内部系统,请使用 VPN 客户端进行连接。
    3,丢失门禁卡时怎么办,请联系总务部申请补办。

用 Excel 保存的 CSV 文件通常不是 UTF-8，而是 Windows 的旧式编码（例如简体中文版 Excel 为 GBK，日文版 Excel 为 MS932）。
此时，请在后面所示的参数中指定编码，例如 ``file_encoding=GBK`` 或 ``file_encoding=MS932``\ 。
请将文件放在 Fess 爬虫可以读取的路径下。
爬虫与 Fess 在同一台服务器上运行，因此在 ZIP 或 RPM / DEB 环境中，请放在运行 Fess 的用户可以读取的目录中。
如果只是在 Docker 中试用，将文件复制到容器内的方法比较简便（重新创建容器后会消失）。

.. code-block:: bash

    docker cp faq.csv fess01:/tmp/faq.csv

在 [爬虫] > [数据存储] 中点击 [新建]，输入以下内容。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 值
   * - 名称
     - 内部FAQ
   * - 处理程序名称
     - ``CsvDataStore``
   * - 参数
     - 见下文
   * - 脚本
     - 见下文
   * - 权限
     - 保持 ``{role}guest``\ （因为是无需登录即可搜索的 FAQ）

参数：

.. code-block:: properties

    script_type=javascript
    files=/tmp/faq.csv
    file_encoding=UTF-8
    has_header_line=true

脚本：

.. code-block:: javascript

    url="https://intranet.example.com/faq/" + faq_id
    title=question
    content=question + " " + answer
    digest=answer
    label="faq"

指定 ``has_header_line=true`` 后，可以在脚本中引用第 1 行的列名（\ ``faq_id``\ 、\ ``question``\ 、\ ``answer``\ ）。
``url`` 中请指定点击搜索结果链接时打开的、能够显示该记录的页面的 URL。
此示例中的 URL 是虚构的。
请替换为实际 FAQ 页面的 URL。

点击 [创建] 保存后，按照后面“计划”一节的步骤创建并运行作业，再按照“确认结果”一节的步骤进行确认。
如果一切顺利，在已注销的状态下（或在浏览器的隐私窗口中）于搜索页面搜索“VPN”，就能找到第 2 条 FAQ。
带有 ``{role}guest`` 的文档会显示给未登录的用户，以及拥有角色 ``guest`` 的用户（包括初始用户 ``admin``\ ）。以其他用户登录时不会显示。

如果想在搜索页面的筛选中显示标签 ``faq``\ ，请在 [爬虫] > [标签] 中创建「值」为 ``faq`` 的标签（参见下一节“标签”）。

索引字段
========

脚本中常设置的字段如下。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 字段
     - 说明
   * - ``url``
     - 必需。搜索结果的链接目标。每条记录应为唯一值
   * - ``title``
     - 搜索结果的标题。搜索对象
   * - ``content``
     - 正文。搜索对象
   * - ``digest``
     - 在搜索结果中显示的摘要
   * - ``label``
     - 标签的值（后述）
   * - ``role``
     - 可以查看的角色。在连接器提供 ACL 时使用（后述）

此外，\ ``config_id``\ 、\ ``boost``\ 、\ ``role``\ 、\ ``virtual_host``\ 、\ ``mimetype`` 等会自动设置（\ ``boost``\ 、\ ``role``\ 、\ ``virtual_host`` 是配置页面中「提升值」「权限」「虚拟主机」的值）。
如果在脚本中指定了相同的字段，则会被脚本的值覆盖。

关于 ``url``\ ，请注意以下几点。

- 表达式的值为 ``null`` 的记录不会被注册。CSV 连接器不会将这样的行记录到失败URL 中，只会在 ``fess-crawler.log`` 中以 WARN 输出 1 行件数
- 文档 ID 由 URL、角色和虚拟主机生成。\ ``url`` 为空字符串的记录或 ``url`` 相同的记录，如果角色和虚拟主机也相同，就会得到相同的文档 ID，相互覆盖，最终只留下最后 1 条

权限
====

新建页面的「权限」中，默认已填入 ``{role}guest``\ 。
该值会成为从该数据存储注册的所有文档的角色。
访客角色会授予未登录的用户，因此保持原样时，文档无需登录即可搜索。
如果是公司内部 FAQ 这类可以公开的数据，保持原样即可。

对于需要限制查看者的数据，请通过以下任一方式控制。

- 将「权限」字段改为希望可以查看的组或角色（例：\ ``{group}sales``\ ）。数据存储内的所有文档都会附加相同的权限
- 如果连接器根据源服务的共享设置（ACL）生成角色，请在脚本中像 ``role=file.roles`` 这样进行映射。项目名因连接器而异（Slack 为 ``message.roles``\ ），有些连接器获取 ACL 还需要额外的参数（如 Slack 的 ``permission_sync=true``\ ）。请查阅各连接器的参考文档

使用 ACL 时，请删除「权限」字段中的 ``{role}guest``\ 。
Box、Slack、Microsoft 365（OneDrive）等连接器，会在 ``file.roles`` / ``message.roles`` 中同时返回「权限」字段的值。
因此，如果保留 ``{role}guest``\ ，即使设置了 ACL，文档仍处于无需登录即可搜索的状态。

反之，如果将「权限」字段留空，脚本中也不设置 ``role``\ ，文档就不会附加任何角色。
这样的文档在搜索页面上对任何人都不会显示。

角色在注册文档时写入。
修改了权限或脚本后，在重新爬取之前不会反映到已有文档。
角色和组的设计在 :doc:`guide-05` 中说明。

标签
====

数据存储的配置页面中，没有 Web 和文件系统配置页面中的「标签」项目。
要附加标签，请使用以下任一方式。

- 在脚本中写 ``label="faq"`` 这样的内容。该数据存储的所有文档都会附加此标签
- 在 [爬虫] > [标签] 中，在「包含的路径」中写入与文档 URL 匹配的正则表达式。注册时会用该正则表达式与 URL 进行比对，并给匹配的文档附加标签

「包含的路径」以与整个 URL 匹配来判定，因此如果需要前缀匹配，请在末尾加上 ``.*``\ （例：\ ``https://intranet\.example\.com/faq/.*``\ ）。

注意：只要 [爬虫] > [标签] 中有任何一个标签与该文档的 URL 匹配，在脚本中附加的标签就会丢失，只保留匹配的标签。
为 Web 爬取创建的标签（例：\ ``https://intranet\.example\.com/.*``\ ），以及只设置了「排除的路径」的标签也是匹配的对象。
在脚本中附加标签时，请确认没有与文档 URL 匹配的标签。

标签的「值」只能使用英文字母、数字和下划线（不能使用连字符以及中文等非 ASCII 字符）。
如果想在搜索页面的标签选项中显示，即使是在脚本中附加，也请在 [爬虫] > [标签] 中注册相同值的标签。
此时「包含的路径」可以为空。

提升值
======

数据存储配置页面中的「提升值」（初始值 ``1.0``\ ）会设置到从该数据存储注册的所有文档上。
提升值在搜索时与得分相乘。
如果想让特定数据源的文档排在前面，请修改此提升值。

[爬虫] > [文档提升] 的规则只适用于通过 Web 爬取和文件爬取注册的文档。
不适用于数据存储的文档。

计划
====

初始状态下的作业「Default Crawler」每天 0:00 运行，爬取所有已启用的 Web、文件系统和数据存储配置。
如果想为每个数据存储设置不同的运行频率，请为每个配置创建作业。

1. 在 [爬虫] > [数据存储] 的列表中点击配置名称，打开详细信息页面
2. 点击 [创建新作业]。会打开调度器的创建页面，其中已填入「名称」（\ ``Data Crawler - 内部FAQ``\ ）以及只爬取此配置的脚本
3. 在「计划」中以 cron 格式（分 时 日 月 星期）输入运行时间，然后点击 [创建]。例：\ ``0 2 * * *``\ （每天 2:00）

「计划」为空的作业不会定期运行，只能手动运行。
如果想立即试用，请在 [系统] > [调度器] 中打开创建的作业，点击 [立即开始]。

即使为配置创建了单独的作业，「Default Crawler」仍会继续爬取该配置。
如果不想重复运行，请将该数据存储配置的「状态」设为禁用。
「Default Crawler」只以已启用的配置为对象，但指定了配置 ID 的作业也会爬取已禁用的配置。
如果为所有配置都创建了专用作业，也可以将「Default Crawler」的「计划」清空（参见 :doc:`guide-04`\ ）。

文档的有效期
============

通过数据存储注册的文档带有有效期。
有效期为该次爬取开始时间起，经过 [系统] > [通用] 中「删除以前的文档」的天数（初始值 ``3`` 天）之后。
过期的文档会由每分钟运行一次的作业「Doc Purger」从索引中删除。
同一文档在下一次爬取中被重新注册后，有效期会延长。

因此，在以下 2 种情况下，文档会从搜索结果中消失。

- 作业的运行间隔比「删除以前的文档」的天数长时
- 在只读取变更项目的增量爬取（如 Git 或 Google Drive 的 ``incremental=true``\ ）中，未变更的文档没有被重新注册时

如果想为每个配置更改有效期，请在参数中以分钟为单位指定 ``time_to_live``\ （例：\ ``time_to_live=11520`` 表示 8 天）。
从源数据中删除的内容，也要等到此有效期到期后才会从搜索结果中消失。
有效期设得过长，删除就迟迟无法反映。

确认结果
========

在数据存储爬取中，即使作业状态为“OK”，也不一定代表成功。
即使连接器中发生异常，Fess 也会以配置为单位或以记录为单位记录下来并继续处理。
因此，作业日志的状态会是“OK”，[系统信息] > [爬网信息] 的「爬虫状态」也不会改变。
请按以下顺序确认。

1. 在 [系统信息] > [作业日志] 中，确认作业已结束。「结果」的 ``Data Config Id:`` 行中显示了目标配置 ID
2. 在 [系统信息] > [爬网信息] 中，确认该会话的「索引大小 (数据存储)」。这是该会话中注册的文档件数（对于「Default Crawler」，是所有数据存储的合计）
3. 在 [系统信息] > [失败URL] 中，确认没有记录错误
4. 从 [系统信息] > [日志文件] 下载 ``fess-crawler.log``\ ，确认 ERROR 和 WARN 行（Docker 和 RPM / DEB 中位于 ``/var/log/fess/``\ ，ZIP 包中位于 ``logs/``\ ）
5. 在 [系统信息] > [搜索] 中搜索 ``label:faq`` 等，确认件数

根据失败方式的不同，留下线索的位置也不同。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 情况
     - 失败URL
     - fess-crawler.log
   * - 找不到处理程序（如配置后删除了插件等）
     - 无记录
     - ``DataStore(...) is not found.``
   * - 整个配置失败（连接器无法继续处理的认证错误、缺少必需参数等）
     - 1 条。URL 栏为 ``D<配置ID>:<配置名称>``
     - ``Failed to process a data crawling: <配置名称>``
   * - 记录级别的失败（脚本计算错误等）
     - 每条记录一条。CSV 中为 ``<文件路径>:<行号>``
     - WARN 行

在 CSV 连接器中，即使 ``files`` 中指定的文件不存在，或扩展名不是 ``.csv`` / ``.tsv``\ ，也不会报错。
它会输出 ``is not found.`` 和 ``No CSV file.`` 的 WARN，然后以 0 件结束。

[系统信息] > [搜索] 不按权限进行筛选，会显示所有文档，因此适合用来确认件数。
但另一方面，它不能用来确认权限是否符合预期。
请以目标用户登录（对于 ``{role}guest`` 的文档则在注销状态下），在普通搜索页面上确认权限（\ :doc:`guide-05`\ ）。

如果不知道连接器传递的项目名，有些连接器在将爬虫的日志级别设为 DEBUG 后，会将获取的值输出到日志中（CSV 连接器会输出每一行的值）。
设置方法请参阅\ `数据存储连接器概述 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-overview.html>`__\ 中的“调试设置”。

各连接器的文章与参考文档
========================

各连接器的设置在以下文章中说明。

- :doc:`guide-06` - Git、Confluence、Jira、Slack
- :doc:`guide-07` - Google Drive、SharePoint Online / OneDrive、Box
- :doc:`guide-12` - 数据库、CSV、Salesforce

参考文档：

- `数据存储连接器概述 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-overview.html>`__ （所有连接器的列表和插件名称）
- `CSV连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-csv.html>`__ / `JSON连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-json.html>`__ / `数据库连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-database.html>`__
- `Google Drive <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-gsuite.html>`__ / `Microsoft 365 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-microsoft365.html>`__ / `Box <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-box.html>`__
- `Atlassian <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-atlassian.html>`__ / `Slack <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-slack.html>`__ / `Git <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-git.html>`__ / `Salesforce <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-salesforce.html>`__
- `数据存储爬取（管理页面） <https://fess.codelibs.org/zh-cn/stable/admin/dataconfig-guide.html>`__ / `调度器 <https://fess.codelibs.org/zh-cn/stable/admin/scheduler-guide.html>`__ / `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__ / `标签 <https://fess.codelibs.org/zh-cn/stable/admin/labeltype-guide.html>`__ / `JavaScript脚本指南 <https://fess.codelibs.org/zh-cn/stable/config/scripting-javascript.html>`__
