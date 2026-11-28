=============================================
搜索开发团队的 Git、Confluence、Jira 和 Slack
=============================================

前言
====

开发团队的信息按工具分散存放：代码和 README 在 Git 中，设计文档在 Confluence 中，问题在 Jira 中，讨论在 Slack 中。
每次查找“那个规格是在哪里定下来的”时，都要依次在 4 个工具中搜索，十分麻烦。
使用 Fess 的数据存储插件，就可以在一个搜索页面中查找这 4 个工具中的信息。

但是，如果配置有误，就会出现下面这样的情况。

- Git 的文件全部以空 URL 注册，无法从搜索结果打开原始文件
- Slack 的消息全部显示为空标题
- 私有频道中的发言也出现在未登录用户的搜索结果中
- Git 的文件在几天后从索引中消失

本文针对每个工具给出“照抄即可运行的最小配置”，并说明各项设置如何避开上述陷阱。
插件的安装，处理程序名称、参数和脚本的写法，以及作业的创建方法等数据存储通用的步骤，已汇总在 :doc:`datastore-basics` 中。
请先阅读该文章再继续。
文中的设置值以 Fess 15.9 和各插件的 15.9.0 版本为准。

本文要构建的配置
================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - 工具
     - 插件
     - 处理程序名称
     - 工具一侧需要准备的内容
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - 具有读取权限的访问令牌（需要能够通过 HTTPS clone）
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - 爬取用账户的 API 令牌
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - Slack App 的 Bot User OAuth Token（``xoxb-``）

如果使用 Docker 运行，在环境变量 ``FESS_PLUGINS`` 中以空格分隔列出插件名称和版本，即可在启动时一并安装。

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

如果通过管理页面或 ``fess-setup`` 安装，请在安装后重启 Fess。

首先要决定：将搜索结果展示给谁
==============================

新建数据存储配置时，「权限」栏中一开始就填有 ``{role}guest``。
如果保持不变，导入的信息也会被未登录的用户搜索到。

Git、Confluence 和 Jira 的插件不会把原工具的访问权限带入 Fess。
爬取所用账户能读取的内容都会被导入，并对拥有「权限」栏中所写角色或组的人可见。
因此，需要组合以下两点来决定范围。

- 将「权限」栏中的 ``{role}guest`` 改为希望展示的对象（例如 ``{group}developers``）
- 通过爬取用账户的权限，以及后面介绍的 ``jira.jql`` 和 ``include_pattern``，把导入范围缩小到可以展示给这些对象的内容

只有 Slack 的插件可以将私有频道的成员作为权限导入（后述）。
关于组和角色的概念，请参阅 :doc:`guide-05`。

Git 仓库
========

准备
----

``fess-ds-git`` 通过 HTTPS 进行 clone。
不支持 SSH 形式的 URI（``git@...`` 形式）。
对于私有仓库，请创建用于读取的访问令牌。
GitHub 的 classic 令牌需要 ``repo`` 作用域，GitLab 需要 ``read_repository`` 作用域。

参数与脚本
----------

在 [爬虫] > [数据存储] > [新建] 中，将「处理程序名称」选为 ``GitDataStore``。

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

各行的含义如下。

- ``base_url``：脚本中的 ``url`` 是将 ``base_url`` 与仓库内的路径直接连接而成的值。如果省略，``url`` 会成为空字符串，所有文件都会得到相同的文档 ID 并相互覆盖。末尾请以 ``/`` 结束，分支名称要与爬取的分支一致（默认是远程的默认分支，需要更改时使用 ``commit_id``）。
- ``username`` / ``password``：只有两者都指定时才会用于认证。不要把令牌嵌入 ``uri``，而是写在 ``password`` 中（``password`` 在保存时会被加密，``uri`` 则不会）。
- ``include_pattern``：与仓库内路径（例如 ``docs/setup.md``）整体匹配的正则表达式。它不是 URL。
- ``title=path``：如果使用只有文件名的 ``name``，就无法在搜索结果中区分 ``README.md`` 这类同名文件，因此使用路径。

差异爬取与有效期
----------------

爬取成功后，``fess-ds-git`` 会将该提交 ID 写回「参数」栏中的 ``prev_commit_id``。
从第 2 次开始，只注册与上一次提交的差异中的文件，并删除已被删除或重命名的文件对应的文档（反映删除需要 ``base_url``）。

这种差异爬取与 Fess 的文档有效期不太兼容，因此上面的示例中指定了 ``time_to_live``。
数据存储的文档在注册时会被设置有效期。
默认情况下，有效期由 [系统] > [通用] 中的「删除以前的文档」（默认 3 天）决定，超过有效期的文档会被每分钟运行一次的作业「Doc Purger」删除。
在差异爬取中，没有变化的文件不会被重新注册，因此有效期不会延长，会在首次爬取几天后消失。
``time_to_live`` 是以分钟为单位指定该配置中文档有效期的参数，``5256000`` 约为 10 年。

因此，即使修改了脚本、``base_url``、``include_pattern`` 或「权限」栏，也不会反映到没有变化的文件上。
要重新注册所有文件，请按以下步骤操作。

1. 在 [系统信息] > [搜索] 中搜索 ``label:code``，用 [删除此查询的所有内容] 删除旧文档
2. 清空「参数」栏中 ``prev_commit_id=`` 的值并保存
3. 运行作业

修改了「权限」栏或 ``base_url`` 时，文档 ID 会发生变化，因此如果省略步骤 1，旧文档会残留下来。
删除此数据存储配置时，也请先通过步骤 1 删除文档。

Confluence
==========

在 Atlassian Cloud 中，用爬取用账户创建 API 令牌，并将其用作 Basic 认证的密码。
导入的是该账户可以查看的空间中的页面和博客文章。
将「处理程序名称」选为 ``ConfluenceDataStore``。

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home`` 带不带 ``/wiki`` 都可以运行。在 Cloud 中，会为 Confluence 补上 ``/wiki``。
- 如果省略 ``deployment``，主机名以 ``.atlassian.net`` 结尾时视为 ``cloud``，否则视为 ``datacenter``。
- 加上 ``content.comments`` 后，页面的评论也可以作为正文进行搜索。各条评论以空行分隔连接在一起。
- ``include_pattern`` 通过与文档 URL 整体是否匹配来判断。Cloud 页面的 URL 形如 ``https://<站点>/wiki/spaces/<空间键>/pages/<页面ID>``，因此可以用空间键来缩小范围。Data Center 的 URL（``/pages/viewpage.action?pageId=...``）中不包含空间键，因此无法使用这种方法。

在 Data Center 中设置 ``deployment=datacenter``，如果使用个人访问令牌，则指定 ``auth_type=pat`` 和 ``pat.token``。

Jira
====

认证方式与 Confluence 相同。
将「处理程序名称」选为 ``JiraDataStore``，并用 JQL 缩小要导入的问题范围。

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

JQL 的参数名称是 ``jira.jql``。
旧名称 ``issue.jql`` 仍然可以使用，但日志中会出现 ``Parameter "issue.jql" is deprecated`` 的警告。
旧名称计划在 16.0 中删除。
如果省略 ``jira.jql``，则使用 ``created is not empty``，也就是以账户可以查看的所有问题为对象。

加上 ``issue.comments`` 后，问题的评论也会以空行分隔放入正文，从而可以搜索。
评论是按问题逐个通过 API 获取的，因此调用次数会增加（参见后述的速率限制）。

Slack
=====

准备 Slack App
--------------

在 https://api.slack.com/apps 创建 App，在 [OAuth & Permissions] 的 Bot Token Scopes 中添加以下作用域，然后安装到工作区。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 作用域
     - 需要的情况
   * - ``channels:read``、``channels:history``、``users:read``、``team:read``
     - 始终需要
   * - ``groups:read``、``groups:history``
     - 导入私有频道（``include_private=true``）
   * - ``users:read.email``
     - 将私有频道的成员作为权限（``permission_sync=true``）
   * - ``files:read``
     - 也导入文件（``file_crawl=true``）

如果没有 ``team:read``，插件会对每条消息调用 ``chat.getPermalink``，API 调用会大幅增加。
安装后，将 App 添加到每个要导入的频道。
App 未加入的频道会输出警告并被跳过。

公开频道和私有频道要分成 2 个数据存储配置来创建。
原因在“私有频道”一节中说明。

公开频道
--------

将「处理程序名称」选为 ``SlackDataStore``，「权限」栏设为希望展示公开频道的对象。

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

对于消息，``message.title`` 始终是空字符串，因此如果写成 ``title=message.title``，所有结果都会没有标题。
请像上面的示例那样，用发帖人和频道名称构成标题。
线程中的回复也会逐条作为文档注册。
``channel_join`` 等系统消息在默认设置（``ignore_system_events=true``）下会被排除。

私有频道
--------

指定 ``permission_sync=true`` 后，插件会根据私有频道成员的邮箱地址为每位成员创建用户角色，并放入 ``message.roles``。
但是，``default_permissions`` 和「权限」栏的值也会被加入这个值中。
公开频道没有自己的角色，因此如果这两项都为空，公开频道的文档对任何人都不可见。
反之，如果在这两项中的任意一项写入公开频道的展示对象，该对象也会看到私有频道的文档。
由于一个配置无法同时正确处理这两种情况，私有频道要使用单独的配置。

在第 2 个数据存储配置中，删除「权限」栏中的 ``{role}guest`` 使其为空，并在 ``channels`` 中列出要导入的私有频道名称。

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- 如果不写 ``role=message.roles``，计算出的角色不会被使用。此时，爬取开始时会出现 ``no script value references message.roles`` 的警告。
- 如果在 ``channels`` 中混入公开频道，其文档的角色为空，对任何人都不可见。
- 使用此配置时，爬取开始时会出现 ``default_permissions is not set and this crawl's DataConfig permission field is empty`` 的警告。只要没有包含公开频道，就没有问题。
- 无法获取成员的频道，或者连 1 个邮箱地址都无法解析的频道（例如忘记添加 ``users:read.email``），在该次爬取中不会被导入。它们会以频道 ID 和频道名称记录在 [系统信息] > [失败URL] 中。

搜索时，登录 Fess 的用户的用户名会与这些邮箱地址进行比对。
因此，Fess 的用户名必须与 Slack 的邮箱地址一致。
Slack 以小写处理邮箱地址，因此 Fess 的用户名也要使用小写。
不一致的用户只是看不到私有频道的文档，并不会看到他人的文档。
关于通过 SSO 登录时哪个值会成为用户名，请参阅 :doc:`guide-15`。

如果之前已经在没有 ``permission_sync`` 的情况下导入了私有频道，这些文档会在有效期结束前一直以无权限的状态保留。
请先在 [系统信息] > [搜索] 中删除相应文档，再用此配置进行爬取。

标签、提升值与计划
==================

标签是通过上面各脚本中的 ``label="..."`` 行添加的。
要在搜索页面的筛选中显示，请在 [爬虫] > [标签] 中创建相同值（``code``、``docs``、``tickets``、``slack``）的标签。
请注意，如果存在「包含的路径」与文档 URL 匹配的标签，脚本设置的标签会丢失（:doc:`datastore-basics`）。

[爬虫] > [文档提升] 的规则不会应用于数据存储的文档。
如果希望 Confluence 的设计文档排在 Slack 的发言之前，请提高 Confluence 数据存储配置的「提升值」（初始值 ``1.0``）。
该值会与搜索得分相乘，因此请逐步调整并对比搜索结果。

要为各工具设置不同的运行频率，请在各数据存储配置的详细页面中使用 [创建新作业]（:doc:`datastore-basics`）。

API 速率限制
============

Slack 和 Atlassian 的插件会自动重试 ``429`` 和 ``5xx`` 响应，如果有 ``Retry-After`` 头，则等待其指定的秒数（Slack 最长 60 秒）。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 插件
     - 可调整的参数
   * - Slack
     - ``read_interval``\ （每条消息的等待时间，毫秒，默认 ``0``）、``max_retry_count``\ （默认 ``3``）、``retry_interval``\ （到第一次重试前的等待时间，毫秒，默认 ``3000``。每次重试翻倍，上限 60 秒）
   * - Atlassian
     - ``read_interval``\ （API 调用的最小间隔，毫秒，默认 ``0``。在线程间共享）。重试的次数和间隔是固定的

Slack 用完重试次数后，该次爬取会中断。
作业日志中的状态仍为“OK”，因此请按下一节的步骤确认。

确认运行情况
============

作业结果和日志的查看方法已在 :doc:`datastore-basics` 中说明。
数据存储的爬取即使失败，作业有时也会显示为“OK”，因此请根据文档数和日志来判断。
对于本文的配置，还要确认以下几点。

1. 在 [系统信息] > [搜索] 中分别搜索 ``label:code``、``label:docs``、``label:tickets``、``label:slack``，确认数量不为 0
2. 打开 Git 文档的 URL，确认显示的是仓库中的文件。如果 ``fess-crawler.log`` 中出现 ``base_url is blank`` 的警告，请检查 ``base_url``
3. 打开 Git 配置的详细页面，确认参数中已写回 ``prev_commit_id``
4. 在已登出的状态下，搜索只存在于私有频道中的词语，确认一条结果也不出现
5. 以该频道成员的身份登录，确认用同一个词语可以找到

如果在第 5 步中找不到，请确认 Fess 的用户名与 Slack 的邮箱地址是否一致，以及 ``fess-crawler.log`` 中是否出现了 ``private channel(s) skipped`` 的警告。
如果因认证错误等原因导致整个配置失败，会以配置为单位记录在 [系统信息] > [失败URL] 中。

总结
====

- Git 必须指定 ``base_url``，并加上 ``time_to_live``，以免文档在差异爬取中过期。
- Confluence 和 Jira 通过 ``content.comments`` / ``issue.comments`` 一并导入评论，JQL 写在 ``jira.jql`` 中。
- Slack 的标题由 ``message.user`` 和 ``message.channel`` 构成。
- Git、Confluence 和 Jira 不会带入原有的权限，因此要通过「权限」栏和导入范围来决定公开范围。
- Slack 的私有频道使用单独的配置，以 ``permission_sync=true``、``role=message.roles`` 和空的「权限」栏进行导入。
- 各信息来源的优先级通过数据存储配置的「提升值」来调整。

参考资料
========

- `Git连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-git.html>`__
- `Atlassian连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-atlassian.html>`__
- `Slack连接器 <https://fess.codelibs.org/zh-cn/stable/config/datastore/ds-slack.html>`__
- `数据存储爬取 <https://fess.codelibs.org/zh-cn/stable/admin/dataconfig-guide.html>`__
- `常规 <https://fess.codelibs.org/zh-cn/stable/admin/general-guide.html>`__
- `fess-ds-slack 15.9.0 README（作用域与权限同步） <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
