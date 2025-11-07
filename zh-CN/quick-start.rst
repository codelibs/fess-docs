==============
快速构建指南
==============

概述
========

本说明面向希望快速体验 Fess 的用户。
本文档描述使用 Fess 的最小步骤。

这里的步骤是用于试用的启动方法，关于面向运营的构建步骤，请参考使用 Docker 的 :doc:`安装步骤 <setup>` 等。
（此处启动的 Fess 是用于简单的功能确认，不推荐在此环境下进行运营）

前期准备
========

在启动 Fess 之前，请先安装 Java 21。
推荐使用 `Eclipse Temurin <https://adoptium.net/temurin>`__ 的 Java 21。

下载
============

从 `GitHub 发布站点 <https://github.com/codelibs/fess/releases>`__ 下载最新的 Fess ZIP 包。

安装
============

解压下载的 fess-x.y.z.zip。

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

启动 Fess
===========

执行 fess 脚本启动 Fess。
（在 Windows 的情况下，请执行 fess.bat）

::

    $ ./bin/fess

访问管理界面
==================

访问 \http://localhost:8080/admin。
默认管理员账户的用户名/密码为 admin/admin。

.. warning::

   请务必更改默认密码。
   在生产环境中，强烈建议在首次登录后立即更改密码。

创建爬取配置
================

登录后，点击左侧菜单的"爬虫">"网页"。
点击"新建"按钮，创建网页爬取的配置信息。

请输入以下信息：

- **名称**: 爬取配置的名称（例：公司网站）
- **URL**: 爬取目标的 URL（例：https://www.example.com/）
- **最大访问数**: 爬取页面数的上限
- **间隔**: 爬取间隔（毫秒）

执行爬取
============

点击左侧菜单的"系统">"调度器"。
点击"Default Crawler"作业的"立即启动"按钮，即可立即开始爬取。

如需定时执行，选择"Default Crawler"并设置定时计划。
如果开始时间为上午 10:35，则设置为 35 10 \* \* ? （格式为"分 时 日 月 星期 年"）。
更新后，将在该时间之后开始爬取。

可以在"爬取信息"中确认是否已开始。
爬取完成后，会话信息中会显示 WebIndexSize 的信息。

搜索
====

爬取完成后，访问 \http://localhost:8080/ 并进行搜索，即可显示搜索结果。

停止 Fess
===========

使用 Ctrl-C 或 kill 命令等停止 fess 进程。

了解更多
==================

请参考以下文档等。

* `文档列表 <documentation>`__
* `[连载] 简单导入！ OSS全文检索服务器Fess入门 <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* `开发者信息 <development>`__
* `讨论论坛 <https://discuss.codelibs.org/c/fessja/>`__

