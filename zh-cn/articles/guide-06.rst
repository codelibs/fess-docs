============================================================
第6回 开发团队的知识中心 -- 代码、Wiki、工单的统合搜索环境
============================================================

前言
========

软件开发团队在日常工作中使用着各种不同的工具。
代码存放在 Git 仓库中，规格说明书在 Confluence 中，任务在 Jira 中，日常沟通在 Slack 中。
虽然每个工具都有搜索功能，但当面对"那个讨论是在哪里进行的？"这样的问题时，逐一搜索所有工具是非常低效的。

本文将介绍如何将开发团队日常使用的各种工具中的信息汇集到 Fess，构建一个可以统合搜索的知识中心。

目标读者
========

- 软件开发团队的负责人和基础设施管理员
- 希望跨工具搜索开发相关信息的人员
- 想要了解数据存储插件基本用法的人员

场景
========

实现对开发团队（20人）信息的统合搜索。

.. list-table:: 目标数据源
   :header-rows: 1
   :widths: 20 30 50

   * - 工具
     - 用途
     - 需要搜索的信息
   * - Git 仓库
     - 源代码管理
     - 代码、README、配置文件
   * - Confluence
     - 文档管理
     - 设计文档、会议记录、操作手册
   * - Jira
     - 工单管理
     - Bug 报告、任务、Story
   * - Slack
     - 沟通协作
     - 技术讨论、决策记录

什么是数据存储爬取
========================

Web 爬取和文件爬取是通过追踪 URL 或文件路径来收集文档的。
而要收集 SaaS 工具中的信息，则需要使用"数据存储爬取"。

数据存储爬取通过各工具的 API 获取数据，并将其注册到 Fess 的索引中。
Fess 为每个工具提供了对应的数据存储插件。

插件的安装
========================

数据存储插件可以从 Fess 的管理界面进行安装。

1. 在管理界面中选择 [系统] > [插件]
2. 确认已安装插件的列表
3. 点击 [安装] 按钮进入安装页面，从 [远程] 选项卡安装所需的插件

本场景中将使用以下插件。

- ``fess-ds-git``: 爬取 Git 仓库
- ``fess-ds-atlassian``: 爬取 Confluence / Jira
- ``fess-ds-slack``: 爬取 Slack 消息

各数据源的配置
====================

Git 仓库的配置
---------------------

爬取 Git 仓库，将代码和文档纳入搜索范围。

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称: 选择 GitDataStore
3. 配置参数

**参数配置示例**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**脚本配置示例**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

在 ``uri`` 中指定仓库的 URL，在 ``username`` / ``password`` 中指定认证信息。对于私有仓库，请将访问令牌设置到 ``password`` 中。``include_pattern`` 可以使用正则表达式来筛选需要爬取的文件扩展名。

Confluence 的配置
------------------

将 Confluence 的页面和博客文章纳入搜索范围。

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称: 选择 ConfluenceDataStore
3. 配置参数

**参数配置示例**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**脚本配置示例**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

在 ``home`` 中指定 Confluence 的 URL，通过 ``auth_type`` 选择认证方式。对于 Confluence Cloud，使用 ``basic`` 认证，并将 API 令牌设置到 ``basic.password`` 中。

Jira 的配置
------------

将 Jira 的工单（Issue）纳入搜索范围。

使用同一 ``fess-ds-atlassian`` 插件中包含的 JiraDataStore 处理器。
可以使用 JQL（Jira Query Language）来筛选需要爬取的工单。
例如，可以仅爬取特定项目的工单，或者仅爬取特定状态（非 Closed）的工单。

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称: 选择 JiraDataStore
3. 配置参数

**参数配置示例**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**脚本配置示例**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

在 ``issue.jql`` 中指定 JQL 查询，以筛选需要爬取的工单。

Slack 的配置
-------------

将 Slack 的消息纳入搜索范围。

1. [爬虫] > [数据存储] > [新建]
2. 处理器名称: 选择 SlackDataStore
3. 配置参数

**参数配置示例**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**脚本配置示例**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

在 ``token`` 中指定 Slack Bot 的 OAuth 令牌。通过 ``channels`` 指定需要爬取的频道，如果要爬取所有频道，请设置为 ``*all``。如果要爬取私有频道，需要设置 ``include_private=true``，并且需要提前将 Bot 邀请到该频道。

标签的使用
============

通过标签区分信息来源
------------------------

通过为每个数据源设置标签，可以在搜索时切换信息来源。

- ``code``: 来自 Git 仓库的代码
- ``docs``: Confluence 的文档
- ``tickets``: Jira 的工单
- ``discussions``: Slack 的消息

用户可以通过"全部"进行跨源搜索，也可以根据需要通过标签进行筛选。

提升搜索质量
===============

利用文档提升
--------------------------

在开发团队的知识中心中，并非所有文档的重要性都相同。
例如，可以考虑以下优先级顺序。

1. Confluence 的文档（正式的规格说明书和操作手册）
2. Jira 的工单（最新的问题和进行中的任务）
3. Git 仓库（代码和 README）
4. Slack 的消息（讨论记录）

使用文档提升功能，可以提高符合特定条件的文档的搜索评分。
在管理界面的 [爬虫] > [文档提升] 中，可以根据 URL 模式或标签来设置提升值。

利用关联内容
--------------------

通过在搜索结果中显示"关联内容"，可以帮助用户更快地找到所需信息。
例如，在搜索 Confluence 的设计文档时，如果相关的 Jira 工单作为"关联内容"显示出来，将会非常方便。

运维注意事项
===============

爬取调度
--------------------

为每个数据源设置合适的爬取频率。

.. list-table:: 调度示例
   :header-rows: 1
   :widths: 25 25 50

   * - 数据源
     - 推荐频率
     - 原因
   * - Confluence
     - 每4小时
     - 文档更新频率中等
   * - Jira
     - 每2小时
     - 工单更新较为频繁
   * - Git
     - 每日
     - 配合发布周期
   * - Slack
     - 每4小时
     - 不需要实时性但需要保持新鲜度

应对 API 速率限制
----------------------

SaaS 工具的 API 存在速率限制。
需要适当设置爬取间隔，以避免触发 API 的速率限制。
特别是 Slack API 的速率限制较为严格，因此在设置爬取间隔时需要留有余量。

访问令牌管理
----------------------

数据存储插件的配置需要各工具的 API 访问令牌。
从安全角度出发，请注意以下几点。

- 最小权限原则: 使用只读访问令牌
- 定期轮换: 定期更新令牌
- 使用专用账户: 使用服务账户而非个人账户

总结
======

本文介绍了如何将开发团队日常使用的各种工具中的信息汇集到 Fess，构建统合搜索的知识中心。

- 通过数据存储插件收集 Git、Confluence、Jira、Slack 的数据
- 通过标签为开发者提供便捷的搜索体验
- 通过文档提升控制信息的优先级
- API 速率限制和令牌管理等运维注意事项

借助开发团队的知识中心，可以快速回答"那个讨论在哪里？""那份规格说明书在哪里？"等问题，实现高效的信息检索环境。

下一期将介绍云存储的跨平台搜索。

参考资料
========

- `Fess 数据存储配置 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess 插件管理 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
