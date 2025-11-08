========================
贡献指南
========================

欢迎为 |Fess| 项目做出贡献！
本页面说明对 |Fess| 的贡献方法、社区指南、
拉取请求的创建步骤等。

.. contents:: 目录
   :local:
   :depth: 2

开始
======

|Fess| 是一个开源项目，
通过社区的贡献而成长。
无论编程经验水平如何，任何人都可以做出贡献。

贡献方法
========

可以通过各种方式为 |Fess| 做出贡献。

代码贡献
----------

- 添加新功能
- 修复错误
- 性能改进
- 重构
- 添加测试

文档贡献
----------------

- 改进用户手册
- 添加・更新 API 文档
- 创建教程
- 翻译

Issue 报告
-----------

- 错误报告
- 功能请求
- 问题或建议

社区活动
--------------

- GitHub Discussions 的讨论
- 在论坛回答问题
- 撰写博客文章或教程
- 活动演讲

首次贡献
==========

如果是第一次为 |Fess| 做出贡献，建议按照以下步骤进行。

Step 1: 理解项目
---------------------------

1. 在 `Fess 官方网站 <https://fess.codelibs.org/ja/>`__ 确认基本信息
2. 通过 :doc:`getting-started` 理解开发概述
3. 通过 :doc:`architecture` 学习代码结构

Step 2: 查找 Issue
-------------------

在 `GitHub 的 Issue 页面 <https://github.com/codelibs/fess/issues>`__
查找带有 ``good first issue`` 标签的 Issue。

这些 Issue 是适合初次贡献者的相对简单的任务。

Step 3: 设置开发环境
----------------------------

按照 :doc:`setup` 构建开发环境。

Step 4: 创建分支并开始工作
----------------------------

按照 :doc:`workflow` 创建分支并开始编码。

Step 5: 创建拉取请求
--------------------------

提交更改并创建拉取请求。

编码规范
==============

|Fess| 为了维护一致的代码，
遵循以下编码规范。

Java编码风格
----------------------

基本风格
~~~~~~~~~~

- **缩进**: 4个空格
- **换行符**: LF（Unix 风格）
- **编码**: UTF-8
- **行长度**: 建议在120字符以内

命名规则
~~~~~~

- **包**: 小写，点分隔（例: ``org.codelibs.fess``）
- **类**: PascalCase（例: ``SearchService``）
- **接口**: PascalCase（例: ``Crawler``）
- **方法**: camelCase（例: ``executeSearch``）
- **变量**: camelCase（例: ``searchResult``）
- **常量**: UPPER_SNAKE_CASE（例: ``MAX_SEARCH_SIZE``）

注释
~~~~~~

**Javadoc:**

对 public 的类、方法、字段编写 Javadoc。

.. code-block:: java

    /**
     * 执行搜索。
     *
     * @param query 搜索查询
     * @return 搜索结果
     * @throws SearchException 搜索失败时
     */
    public SearchResponse executeSearch(String query) throws SearchException {
        // 实现
    }

**实现注释:**

对复杂的逻辑，添加中文或英文注释。

.. code-block:: java

    // 规范化查询（全角转半角）
    String normalizedQuery = QueryNormalizer.normalize(query);

类和方法的设计
~~~~~~~~~~~~~~~~~~~~

- **单一职责原则**: 一个类只有一个职责
- **小方法**: 一个方法只做一件事
- **有意义的名称**: 类名、方法名要明确表达意图

异常处理
~~~~~~

.. code-block:: java

    // 好的例子: 适当的异常处理
    try {
        executeSearch(query);
    } catch (IOException e) {
        logger.error("搜索过程中发生错误", e);
        throw new SearchException("搜索执行失败", e);
    }

    // 应避免的例子: 空的catch块
    try {
        executeSearch(query);
    } catch (IOException e) {
        // 什么都不做
    }

null 的处理
~~~~~~~~~

- 尽可能不返回 ``null``
- 推荐使用 ``Optional``
- 用 ``@Nullable`` 注解明确 null 的可能性

.. code-block:: java

    // 好的例子
    public Optional<User> findUser(String id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // 使用例
    findUser("123").ifPresent(user -> {
        // 用户存在时的处理
    });

测试的编写
~~~~~~~~~~

- 为所有 public 方法编写测试
- 测试方法名以 ``test`` 开头
- 使用 Given-When-Then 模式

.. code-block:: java

    @Test
    public void testSearch() {
        // Given: 测试前提条件
        SearchService service = new SearchService();
        String query = "test";

        // When: 执行被测试对象
        SearchResponse response = service.search(query);

        // Then: 验证结果
        assertNotNull(response);
        assertEquals(10, response.getDocuments().size());
    }

代码审查指南
========================

拉取请求的审查流程
----------------------------

1. **自动检查**: CI 自动执行构建和测试
2. **代码审查**: 维护者审查代码
3. **反馈**: 根据需要请求修改
4. **批准**: 审查获得批准
5. **合并**: 维护者合并到 main 分支

审查要点
----------

审查时会确认以下要点：

**功能性**

- 是否满足需求
- 是否按预期工作
- 是否考虑了边界情况

**代码质量**

- 是否遵循编码规范
- 代码是否易读易维护
- 抽象是否适当

**测试**

- 是否编写了充分的测试
- 测试是否通过
- 测试是否进行了有意义的验证

**性能**

- 对性能是否有影响
- 资源使用是否适当

**安全性**

- 是否存在安全问题
- 输入验证是否适当

**文档**

- 必要的文档是否更新
- Javadoc 是否适当编写

对审查意见的回应
--------------------

对审查意见要迅速且礼貌地回应。

**需要修改时:**

.. code-block:: text

    感谢您的指正。已经修改。
    [修改内容的简要说明]

**需要讨论时:**

.. code-block:: text

    感谢您的意见。
    出于○○的原因采用了当前的实现，
    △△这样的实现会更好吗？

拉取请求的最佳实践
================================

PR 的大小
---------

- 力求小而易于审查的 PR
- 一个 PR 包含一个逻辑变更
- 大的更改分成多个 PR

PR 的标题
-----------

使用清晰且描述性的标题：

.. code-block:: text

    feat: 添加搜索结果过滤功能
    fix: 修复爬虫超时问题
    docs: 更新 API 文档

PR 的描述
-------

包含以下信息：

- **更改内容**: 更改了什么
- **原因**: 为什么需要这个更改
- **测试方法**: 如何测试的
- **截图**: UI 更改的情况
- **相关 Issue**: Issue 编号（例: Closes #123）

.. code-block:: markdown

    ## 更改内容
    添加了可以按文件类型过滤搜索结果的功能。

    ## 原因
    因为收到许多用户"想只搜索特定文件类型"的需求。

    ## 测试方法
    1. 在搜索屏幕选择文件类型过滤器
    2. 执行搜索
    3. 确认只显示所选文件类型的结果

    ## 相关 Issue
    Closes #123

提交消息
----------------

编写清晰且描述性的提交消息：

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**例:**

.. code-block:: text

    feat: 添加搜索过滤功能

    使用户可以按文件类型过滤搜索结果。

    - 添加过滤器UI
    - 实现后端过滤处理
    - 添加测试

    Closes #123

Draft PR 的活用
--------------

将进行中的 PR 创建为 Draft PR，
完成后改为 Ready for review。

.. code-block:: text

    1. 创建 PR 时选择「Create draft pull request」
    2. 工作完成后点击「Ready for review」

社区指南
======================

行为准则
------

|Fess| 社区遵守以下行为准则：

- **尊重**: 尊重所有人
- **协作**: 提供建设性反馈
- **开放**: 欢迎不同的观点和经验
- **礼貌**: 注意使用礼貌的措辞

沟通
----------------

**提问的地方:**

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 一般问题和讨论
- `Issue 跟踪器 <https://github.com/codelibs/fess/issues>`__: 错误报告和功能请求
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 日语论坛

**提问方法:**

- 具体提问
- 说明尝试过的方法
- 包含错误消息或日志
- 注明环境信息（OS、Java 版本等）

**回答方法:**

- 礼貌、友好
- 提供具体的解决方案
- 提供参考资料的链接

感谢的表达
--------

对贡献表示感谢。
即使是小的贡献，对项目也是有价值的。

常见问题
==========

Q: 初学者也可以贡献吗？
---------------------------

A: 可以，欢迎！建议从带有 ``good first issue`` 标签的 Issue 开始。
文档改进也是适合初学者的贡献。

Q: 拉取请求大约多久会被审查？
-------------------------------------------------

A: 通常在几天内审查。
但根据维护者的时间安排可能会有所变化。

Q: 如果拉取请求被拒绝了怎么办？
-----------------------------------

A: 确认被拒绝的原因，根据需要修改后可以重新提交。
如有不明白的地方，请随时提问。

Q: 如果违反了编码规范怎么办？
---------------------------------------

A: 会在审查中指出，所以修改即可。
可以通过运行 Checkstyle 来提前检查。

Q: 如果想添加大功能怎么办？
-------------------------------

A: 建议先创建 Issue，讨论建议内容。
通过事先达成共识可以避免工作的浪费。

Q: 可以用日语提问吗？
-------------------------------

A: 可以，日语或英语都可以。
Fess 是日本发起的项目，所以日语支持也很充实。

贡献类型别指南
================

文档改进
----------------

1. Fork 文档仓库：

   .. code-block:: bash

       git clone https://github.com/codelibs/fess-docs.git

2. 进行更改
3. 创建拉取请求

错误报告
------

1. 搜索现有 Issue 确认是否重复
2. 创建新 Issue
3. 包含以下信息：

   - 错误描述
   - 重现步骤
   - 预期行为
   - 实际行为
   - 环境信息

功能请求
------------

1. 创建 Issue
2. 说明以下内容：

   - 功能描述
   - 背景和动机
   - 建议的实现方法（可选）

代码审查
------------

审查他人的拉取请求也是一种贡献：

1. 找到感兴趣的 PR
2. 确认代码
3. 提供建设性反馈

许可证
========

|Fess| 在 Apache License 2.0 下发布。
贡献的代码也适用相同的许可证。

通过创建拉取请求，
视为您同意您的贡献在此许可证下发布。

致谢
====

感谢您对 |Fess| 项目的贡献！
您的贡献使 |Fess| 成为更好的软件。

下一步
==========

准备好贡献后：

1. 通过 :doc:`setup` 设置开发环境
2. 通过 :doc:`workflow` 确认开发流程
3. 在 `GitHub <https://github.com/codelibs/fess>`__ 查找 Issue

参考资料
======

- `GitHub 流程 <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `如何为开源做贡献 <https://opensource.guide/ja/how-to-contribute/>`__
- `如何编写好的提交消息 <https://chris.beams.io/posts/git-commit/>`__

社区资源
==================

- **GitHub**: `codelibs/fess <https://github.com/codelibs/fess>`__
- **Discussions**: `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- **Forum**: `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- **Twitter**: `@codelibs <https://twitter.com/codelibs>`__
- **Website**: `fess.codelibs.org <https://fess.codelibs.org/ja/>`__
