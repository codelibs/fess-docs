====================================
开源全文检索服务器 - |Fess| 开发指南
====================================

本指南提供参与 |Fess| 开发所需的信息。
面向从初次接触 |Fess| 开发的人员到经验丰富的开发者等各类人群。

.. contents:: 目录
   :local:
   :depth: 2

目标读者
========

本指南面向以下人员：

- 希望为 |Fess| 的功能添加或改进做出贡献的开发者
- 希望理解 |Fess| 代码的技术人员
- 希望自定义使用 |Fess| 的用户
- 对参与开源项目感兴趣的人员

必备前置知识
============

参与 |Fess| 的开发，以下知识会有所帮助：

**必需**

- Java 编程基础知识（Java 21 及以上）
- Git 和 GitHub 的基本使用方法
- Maven 的基本使用方法

**推荐**

- LastaFlute 框架知识
- DBFlute 知识
- OpenSearch/Elasticsearch 知识
- Web 应用程序开发经验

开发指南的构成
==============

本指南由以下部分组成。

:doc:`getting-started`
    说明 |Fess| 开发概述和开始开发的第一步。
    可以了解开发所需的技术栈和项目整体结构。

:doc:`setup`
    详细说明开发环境的设置步骤。
    从 Java、IDE、OpenSearch 等必要工具的安装，
    到 |Fess| 源代码的获取和运行，逐步解说。

:doc:`architecture`
    说明 |Fess| 的架构和代码结构。
    通过理解主要的包、模块和设计模式，
    可以高效地进行开发。

:doc:`workflow`
    说明 |Fess| 开发的标准工作流程。
    可以学习功能添加、错误修复、代码审查、测试等
    开发工作的进行方式。

:doc:`building`
    说明 |Fess| 的构建方法和测试方法。
    解说构建工具的使用方法、单元测试的执行、
    发布包的创建方法等。

:doc:`contributing`
    说明对 |Fess| 项目的贡献方法。
    可以学习拉取请求的创建、编码规范、
    与社区的沟通方法等。

快速入门
==============

如果想立即开始 |Fess| 的开发，请按照以下步骤：

1. **确认系统要求**

   开发需要以下工具：

   - Java 21 及以上
   - Maven 3.x 及以上
   - Git
   - IDE（Eclipse、IntelliJ IDEA 等）

2. **获取源代码**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **下载 OpenSearch 插件**

   .. code-block:: bash

       mvn antrun:run

4. **运行**

   从 IDE 运行 ``org.codelibs.fess.FessBoot``，
   或从 Maven 运行：

   .. code-block:: bash

       mvn compile exec:java

详情请参阅 :doc:`setup`。

开发环境的选项
==============

|Fess| 的开发可以在以下任一环境中进行：

本地开发环境
--------------

最常见的开发环境。在自己的机器上安装开发工具，
使用 IDE 进行开发。

**优点:**

- 快速构建和运行
- 可以充分利用 IDE 的功能
- 可以离线工作

**缺点:**

- 初始设置需要时间
- 可能因环境差异产生问题

使用 Docker 的开发环境
------------------------

使用 Docker 容器可以构建一致的开发环境。

**优点:**

- 保持环境的一致性
- 设置简单
- 容易恢复到干净状态

**缺点:**

- 需要 Docker 知识
- 性能可能会有所下降

详情请参阅 :doc:`setup`。

常见问题
==========

Q: 开发所需的最低配置是？
--------------------------------

A: 建议使用以下配置：

- CPU: 4核及以上
- 内存: 8GB及以上
- 磁盘: 20GB以上的可用空间

Q: 应该使用哪个 IDE？
---------------------------------

A: 可以使用 Eclipse、IntelliJ IDEA、VS Code 等您喜欢的 IDE。
本指南主要以 Eclipse 为例进行说明，
但也可以使用其他 IDE 进行开发。

Q: LastaFlute 或 DBFlute 的知识是必需的吗？
------------------------------------------

A: 不是必需的，但有这些知识会使开发更顺利。
基本用法本指南也会说明，
详情请参阅各框架的官方文档。

Q: 第一次贡献应该从什么开始？
------------------------------------------------------

A: 建议从以下相对简单的工作开始：

- 文档改进
- 添加测试
- 错误修复
- 现有功能的小改进

详情请参阅 :doc:`contributing`。

相关资源
==========

官方资源
----------

- `Fess 官方网站 <https://fess.codelibs.org/ja/>`__
- `GitHub 仓库 <https://github.com/codelibs/fess>`__
- `Issue 跟踪器 <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

技术文档
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

社区
----------

- `Fess 社区论坛 <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

下一步
==========

要开始开发，建议从 :doc:`getting-started` 开始阅读。

.. toctree::
   :maxdepth: 2
   :caption: 目录:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
