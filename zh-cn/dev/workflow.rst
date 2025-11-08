==============
开发工作流程
==============

本页面说明 |Fess| 开发中的标准工作流程。
可以学习功能添加、错误修复、测试、代码审查等
开发工作的进行方式。

.. contents:: 目录
   :local:
   :depth: 2

基本开发流程
==============

|Fess| 的开发按照以下流程进行：

.. code-block:: text

    1. 确认・创建 Issue
       ↓
    2. 创建分支
       ↓
    3. 编码
       ↓
    4. 执行本地测试
       ↓
    5. 提交
       ↓
    6. 推送
       ↓
    7. 创建拉取请求
       ↓
    8. 代码审查
       ↓
    9. 回应审查反馈
       ↓
    10. 合并

详细说明各步骤。

Step 1: 确认・创建 Issue
=========================

开始开发前，确认 GitHub 的 Issue。

确认现有 Issue
-----------------

1. 访问 `Fess 的 Issue 页面 <https://github.com/codelibs/fess/issues>`__
2. 查找想要处理的 Issue
3. 在 Issue 上评论，告知开始工作

.. tip::

   如果是首次贡献，建议从带有 ``good first issue`` 标签的 Issue 开始。

创建新 Issue
-----------------

对于新功能或错误修复，创建 Issue。

1. 点击 `New Issue <https://github.com/codelibs/fess/issues/new>`__
2. 选择 Issue 模板
3. 填写必要信息：

   - **标题**: 简洁明了的说明
   - **描述**: 详细的背景、预期行为、当前行为
   - **重现步骤**: 错误的情况
   - **环境信息**: OS、Java 版本、Fess 版本等

4. 点击 ``Submit new issue``

Issue 模板
~~~~~~~~~~~~~~~~~~

**错误报告:**

.. code-block:: markdown

    ## 问题描述
    错误的简要说明

    ## 重现步骤
    1. ...
    2. ...
    3. ...

    ## 预期行为
    应该如何

    ## 实际行为
    当前如何

    ## 环境
    - OS:
    - Java 版本:
    - Fess 版本:

**功能请求:**

.. code-block:: markdown

    ## 功能描述
    想要添加的功能说明

    ## 背景和动机
    为什么需要此功能

    ## 建议的实现方法
    如何实现（可选）

Step 2: 创建分支
====================

创建工作分支。

分支命名规则
--------------

分支名遵循以下格式：

.. code-block:: text

    <type>/<issue-number>-<short-description>

**type 的种类:**

- ``feature``: 添加新功能
- ``fix``: 修复错误
- ``refactor``: 重构
- ``docs``: 更新文档
- ``test``: 添加・修改测试

**例:**

.. code-block:: bash

    # 添加新功能
    git checkout -b feature/123-add-search-filter

    # 修复错误
    git checkout -b fix/456-fix-crawler-timeout

    # 更新文档
    git checkout -b docs/789-update-api-docs

创建分支的步骤
----------------

1. 获取最新的 main 分支：

   .. code-block:: bash

       git checkout main
       git pull origin main

2. 创建新分支：

   .. code-block:: bash

       git checkout -b feature/123-add-search-filter

3. 确认分支已创建：

   .. code-block:: bash

       git branch

Step 3: 编码
==================

进行功能实现或错误修复。

编码规范
--------------

|Fess| 遵循以下编码规范。

基本风格
~~~~~~~~~~~~~~

- **缩进**: 4个空格
- **行长度**: 建议在120字符以内
- **编码**: UTF-8
- **换行符**: LF（Unix 风格）

命名规则
~~~~~~

- **类名**: PascalCase（例: ``SearchService``）
- **方法名**: camelCase（例: ``executeSearch``）
- **常量**: UPPER_SNAKE_CASE（例: ``MAX_SEARCH_SIZE``）
- **变量**: camelCase（例: ``searchResults``）

注释
~~~~~~

- **Javadoc**: public 的类和方法必需
- **实现注释**: 对复杂的逻辑添加中文或英文说明

**例:**

.. code-block:: java

    /**
     * 执行搜索。
     *
     * @param query 搜索查询
     * @return 搜索结果
     */
    public SearchResponse executeSearch(String query) {
        // 规范化查询
        String normalizedQuery = normalizeQuery(query);

        // 执行搜索
        return searchEngine.search(normalizedQuery);
    }

null 的处理
~~~~~~~~~

- 尽可能不返回 ``null``
- 推荐使用 ``Optional``
- 明确进行 ``null`` 检查

**例:**

.. code-block:: java

    // 好的例子
    public Optional<User> findUser(String id) {
        return userRepository.findById(id);
    }

    // 应避免的例子
    public User findUser(String id) {
        return userRepository.findById(id);  // null 的可能性
    }

异常处理
~~~~~~

- 适当捕获和处理异常
- 输出日志
- 向用户提供易懂的消息

**例:**

.. code-block:: java

    try {
        // 处理
    } catch (IOException e) {
        logger.error("文件读取错误", e);
        throw new FessSystemException("文件读取失败", e);
    }

日志输出
~~~~~~

使用适当的日志级别：

- ``ERROR``: 发生错误时
- ``WARN``: 应警告的情况
- ``INFO``: 重要信息
- ``DEBUG``: 调试信息
- ``TRACE``: 详细的跟踪信息

**例:**

.. code-block:: java

    if (logger.isDebugEnabled()) {
        logger.debug("搜索查询: {}", query);
    }

开发中的测试
------------

开发期间，通过以下方法进行测试：

本地运行
~~~~~~~~~~

在 IDE 或命令行运行 Fess，确认行为：

.. code-block:: bash

    mvn compile exec:java

调试运行
~~~~~~~~~~

使用 IDE 的调试器，跟踪代码的运行。

单元测试的执行
~~~~~~~~~~~~~~

执行与更改相关的测试：

.. code-block:: bash

    # 执行特定的测试类
    mvn test -Dtest=SearchServiceTest

    # 执行所有测试
    mvn test

详情请参阅 :doc:`building`。

Step 4: 执行本地测试
=========================

提交前务必执行测试。

单元测试的执行
--------------

.. code-block:: bash

    mvn test

集成测试的执行
--------------

.. code-block:: bash

    mvn verify

代码风格检查
--------------------

.. code-block:: bash

    mvn checkstyle:check

执行所有检查
-------------------

.. code-block:: bash

    mvn clean verify

Step 5: 提交
==============

提交更改。

提交消息的规范
--------------------

提交消息遵循以下格式：

.. code-block:: text

    <type>: <subject>

    <body>

    <footer>

**type 的种类:**

- ``feat``: 新功能
- ``fix``: 修复错误
- ``docs``: 仅文档更改
- ``style``: 不影响代码含义的更改（格式等）
- ``refactor``: 重构
- ``test``: 添加・修改测试
- ``chore``: 构建过程或工具的更改

**例:**

.. code-block:: text

    feat: 添加搜索过滤功能

    使用户可以按文件类型过滤搜索结果。

    Fixes #123

提交步骤
----------

1. 暂存更改：

   .. code-block:: bash

       git add .

2. 提交：

   .. code-block:: bash

       git commit -m "feat: 添加搜索过滤功能"

3. 确认提交历史：

   .. code-block:: bash

       git log --oneline

提交粒度
------------

- 一个提交包含一个逻辑更改
- 大的更改分成多个提交
- 提交消息要易懂且具体

Step 6: 推送
==============

将分支推送到远程仓库。

.. code-block:: bash

    git push origin feature/123-add-search-filter

首次推送的情况：

.. code-block:: bash

    git push -u origin feature/123-add-search-filter

Step 7: 创建拉取请求
=========================

在 GitHub 创建拉取请求（PR）。

PR 的创建步骤
-----------

1. 访问 `Fess 仓库 <https://github.com/codelibs/fess>`__
2. 点击 ``Pull requests`` 选项卡
3. 点击 ``New pull request``
4. 选择基础分支（``main``）和比较分支（工作分支）
5. 点击 ``Create pull request``
6. 填写 PR 内容（按照模板）
7. 点击 ``Create pull request``

PR 模板
---------------

.. code-block:: markdown

    ## 更改内容
    此 PR 更改了什么

    ## 相关 Issue
    Closes #123

    ## 更改类型
    - [ ] 新功能
    - [ ] 修复错误
    - [ ] 重构
    - [ ] 更新文档
    - [ ] 其他

    ## 测试方法
    如何测试此更改

    ## 检查清单
    - [ ] 代码正常工作
    - [ ] 已添加测试
    - [ ] 已更新文档
    - [ ] 遵循编码规范

PR 的描述
-------

PR 描述应包含以下内容：

- **更改目的**: 为什么需要此更改
- **更改内容**: 更改了什么
- **测试方法**: 如何测试的
- **截图**: UI 更改的情况

Step 8: 代码审查
====================

维护者审查代码。

审查要点
------------

审查时会检查以下要点：

- 代码质量
- 是否符合编码规范
- 测试的充实度
- 对性能的影响
- 安全问题
- 文档的更新

审查意见的例子
------------------

**批准:**

.. code-block:: text

    LGTM (Looks Good To Me)

**修改请求:**

.. code-block:: text

    这里是否需要 null 检查？

**建议:**

.. code-block:: text

    这个处理移到 Helper 类可能更好。

Step 9: 回应审查反馈
===================================

回应审查意见。

回应反馈的步骤
----------------------

1. 阅读审查意见
2. 进行必要的修改
3. 提交更改：

   .. code-block:: bash

       git add .
       git commit -m "fix: 回应审查意见"

4. 推送：

   .. code-block:: bash

       git push origin feature/123-add-search-filter

5. 在 PR 页面回复评论

对意见的回复
--------------

务必回复审查意见：

.. code-block:: text

    已修改。请确认。

或者：

.. code-block:: text

    感谢您的指正。
    出于○○的原因采用了当前的实现，您觉得如何？

Step 10: 合并
=============

审查获得批准后，维护者合并 PR。

合并后的处理
------------

1. 更新本地的 main 分支：

   .. code-block:: bash

       git checkout main
       git pull origin main

2. 删除工作分支：

   .. code-block:: bash

       git branch -d feature/123-add-search-filter

3. 删除远程分支（如果 GitHub 未自动删除）：

   .. code-block:: bash

       git push origin --delete feature/123-add-search-filter

常见开发场景
==================

功能添加
------

1. 创建 Issue（或确认现有 Issue）
2. 创建分支：``feature/xxx-description``
3. 实现功能
4. 添加测试
5. 更新文档
6. 创建 PR

修复错误
------

1. 确认错误报告的 Issue
2. 创建分支：``fix/xxx-description``
3. 添加重现错误的测试
4. 修复错误
5. 确认测试通过
6. 创建 PR

重构
--------------

1. 创建 Issue（说明重构的理由）
2. 创建分支：``refactor/xxx-description``
3. 执行重构
4. 确认现有测试通过
5. 创建 PR

更新文档
--------------

1. 创建分支：``docs/xxx-description``
2. 更新文档
3. 创建 PR

开发提示
==========

高效开发
----------

- **小的提交**: 频繁提交
- **早期反馈**: 利用 Draft PR
- **测试自动化**: 利用 CI/CD
- **代码审查**: 也审查他人的代码

问题解决
--------

遇到困难时，使用以下资源：

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- GitHub 的 Issue 评论

下一步
==========

理解了工作流程后，也请参阅以下文档：

- :doc:`building` - 构建和测试的详情
- :doc:`contributing` - 贡献指南
- :doc:`architecture` - 理解代码库

参考资料
======

- `GitHub 流程 <https://docs.github.com/ja/get-started/quickstart/github-flow>`__
- `提交消息指南 <https://chris.beams.io/posts/git-commit/>`__
- `代码审查的最佳实践 <https://google.github.io/eng-practices/review/>`__
