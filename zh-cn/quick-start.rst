==============
快速构建指南
==============

概述
========

本说明面向希望快速体验 Fess 的用户。
本文档描述使用 Fess 的最小步骤。

这里的步骤是用于试用的启动方法，关于面向运营的构建步骤，请参考使用 Docker 的 :doc:`安装步骤 <setup>` 等。
（此处启动的 Fess 是用于简单的功能确认，不推荐在此环境下进行运营）

.. tip::

   **最快方式：Docker（推荐）**

   如果您已安装 Docker，只需几个命令即可在约 3 分钟内启动 Fess，无需安装其他依赖。

----

使用 Docker 快速开始（推荐）
============================

Docker 提供了最快、最可靠的 Fess 运行方式。所有依赖都已打包，无需额外安装。

**环境要求：**

- Docker 20.10 或更高版本
- Docker Compose 2.0 或更高版本

**Step 1: 下载 Docker Compose 文件**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Step 2: 启动容器**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Step 3: 验证启动**

等待几分钟让服务初始化完成，然后在浏览器中打开：

- **搜索界面:** http://localhost:8080/
- **管理面板:** http://localhost:8080/admin
- **默认账户:** admin / admin

.. warning::

   **安全提醒:** 请在首次登录后立即更改默认管理员密码。

**Step 4: 停止**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

关于高级 Docker 配置（自定义设置、外部 OpenSearch、Kubernetes），
请参阅 `Docker 安装指南 <15.5/install/install-docker.html>`__。

----

使用 ZIP 包启动
================

如果您不使用 Docker，可以通过 ZIP 包直接运行 Fess。

.. note::

   此方法适用于评估和试用。生产环境部署建议使用 Docker 或 :doc:`RPM/DEB 包安装 <setup>`。

前期准备
--------

在启动 Fess 之前，请先安装 Java 21。
推荐使用 `Eclipse Temurin <https://adoptium.net/temurin>`__ 的 Java 21。

验证 Java 安装：

.. code-block:: bash

    java -version

下载
----

从 `GitHub 发布站点 <https://github.com/codelibs/fess/releases>`__ 下载最新的 Fess ZIP 包。

安装
----

解压下载的 fess-x.y.z.zip。

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

启动 Fess
-----------

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
