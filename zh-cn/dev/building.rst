==============
构建和测试
==============

本页面说明 |Fess| 的构建方法、测试方法、
发布包的创建方法。

.. contents:: 目录
   :local:
   :depth: 2

构建系统概述
==================

|Fess| 使用 Maven 作为构建工具。
Maven 自动化依赖关系管理、编译、测试和打包。

pom.xml
-------

Maven 的配置文件。位于项目的根目录。

主要配置内容：

- 项目信息（groupId、artifactId、version）
- 依赖库
- 构建插件
- 配置文件

基本构建命令
==================

清理构建
------------

删除构建产物后重新构建：

.. code-block:: bash

    mvn clean compile

创建包
--------------

创建 WAR 文件和发布用 zip 包：

.. code-block:: bash

    mvn package

产物生成在 ``target/`` 目录：

.. code-block:: text

    target/
    ├── fess.war
    └── releases/
        └── fess-{version}.zip

完整构建
--------

执行清理、编译、测试、打包的所有步骤：

.. code-block:: bash

    mvn clean package

下载依赖
--------------------

下载依赖库：

.. code-block:: bash

    mvn dependency:resolve

下载 OpenSearch 插件
---------------------------------

下载 OpenSearch 和必需插件：

.. code-block:: bash

    mvn antrun:run

.. note::

   此命令在设置开发环境时或
   更新插件时执行。

测试
====

|Fess| 使用 JUnit 实现测试。

单元测试的执行
--------------

执行所有单元测试
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

执行特定的测试类
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

执行特定的测试方法
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

执行多个测试类
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

跳过测试
--------------

跳过测试进行构建的情况：

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   开发期间不要跳过测试，务必执行。
   创建 PR 之前，请确认所有测试都通过。

集成测试的执行
--------------

集成测试需要使用 ``integrationTests`` 配置文件。
需要 |Fess| 服务器和 OpenSearch 正在运行：

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

.. note::

   集成测试类使用 ``*Tests.java`` 命名模式（单元测试使用 ``*Test.java``）。

测试的编写
============

单元测试的创建
--------------

测试类的放置
~~~~~~~~~~~~~~~~

将测试类放置在 ``src/test/java/`` 下。
包结构与主代码相同。

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

测试类的基本结构
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: 测试前提条件
            SearchService service = new SearchService();
            String query = "test";

            // When: 执行被测试对象
            SearchResponse response = service.search(query);

            // Then: 验证结果
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

测试的生命周期
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // 所有测试前执行一次
        }

        @BeforeEach
        void setUp() {
            // 每个测试前执行
        }

        @Test
        void testSomething() {
            // 测试
        }

        @AfterEach
        void tearDown() {
            // 每个测试后执行
        }

        @AfterAll
        static void tearDownClass() {
            // 所有测试后执行一次
        }
    }

断言
~~~~~~~~~~

使用 JUnit 5 的断言：

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // 等价性
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // null 检查
    assertNull(obj);
    assertNotNull(obj);

    // 布尔值
    assertTrue(condition);
    assertFalse(condition);

    // 异常
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // 集合
    assertIterableEquals(expectedList, actualList);

测试覆盖率
--------------

使用 JaCoCo 测量测试覆盖率：

.. code-block:: bash

    mvn clean test jacoco:report

报告生成在 ``target/site/jacoco/index.html``。

代码格式化
================

|Fess| 使用以下工具来维护代码质量。

代码格式化器
------------------

统一编码风格：

.. code-block:: bash

    mvn formatter:format

许可证头
----------------

向源文件添加许可证头：

.. code-block:: bash

    mvn license:format

提交前检查
------------------

提交前请同时执行：

.. code-block:: bash

    mvn formatter:format
    mvn license:format

创建发布包
==================

创建 zip 包
------------------

创建用于发布的 zip 包：

.. code-block:: bash

    mvn clean package

生成的产物：

.. code-block:: text

    target/releases/
    └── fess-{version}.zip

创建 RPM 包
------------------

.. code-block:: bash

    mvn rpm:rpm

创建 DEB 包
------------------

.. code-block:: bash

    mvn jdeb:jdeb

配置文件
==========

可以使用 Maven 配置文件来切换测试类型。

build（默认）
-----------------

默认配置文件。运行单元测试（``*Test.java``）：

.. code-block:: bash

    mvn package

integrationTests
----------------

用于运行集成测试（``*Tests.java``）的配置文件：

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

CI/CD
=====

|Fess| 使用 GitHub Actions 执行 CI/CD。

GitHub Actions
-------------

配置文件在 ``.github/workflows/`` 目录。

自动执行的检查：

- 构建
- 单元测试
- 包创建

本地 CI 检查
-----------------------

创建 PR 之前，可以在本地执行与 CI 相同的检查：

.. code-block:: bash

    mvn clean package

故障排除
====================

构建错误
----------

**错误: 依赖下载失败**

.. code-block:: bash

    # 清除 Maven 的本地仓库
    rm -rf ~/.m2/repository
    mvn clean compile

**错误: 内存不足**

.. code-block:: bash

    # 增加 Maven 的内存
    export MAVEN_OPTS="-Xmx2g"
    mvn clean package

**错误: Java 版本过旧**

请使用 Java 21 及以上：

.. code-block:: bash

    java -version

测试错误
----------

**测试超时**

延长测试超时时间：

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch 未启动**

确认端口，如果正在使用则更改：

.. code-block:: bash

    lsof -i :9201

依赖问题
------------

**依赖冲突**

确认依赖树：

.. code-block:: bash

    mvn dependency:tree

排除特定的依赖：

.. code-block:: xml

    <dependency>
        <groupId>org.example</groupId>
        <artifactId>example-lib</artifactId>
        <version>1.0</version>
        <exclusions>
            <exclusion>
                <groupId>conflicting-lib</groupId>
                <artifactId>conflicting-lib</artifactId>
            </exclusion>
        </exclusions>
    </dependency>

构建的最佳实践
========================

定期清理构建
--------------------

定期执行清理构建，避免构建缓存问题：

.. code-block:: bash

    mvn clean package

测试的执行
----------

提交前务必执行测试：

.. code-block:: bash

    mvn test

代码格式化的执行
------------------

创建 PR 之前执行代码格式化：

.. code-block:: bash

    mvn formatter:format
    mvn license:format

依赖更新
------------

定期更新依赖：

.. code-block:: bash

    mvn versions:display-dependency-updates

利用构建缓存
--------------------

为缩短构建时间，利用 Maven 的缓存：

.. code-block:: bash

    # 如果已编译则跳过
    mvn compile

Maven 命令参考
========================

常用命令
--------------

.. code-block:: bash

    # 清理
    mvn clean

    # 编译
    mvn compile

    # 测试
    mvn test

    # 打包
    mvn package

    # 安装（注册到本地仓库）
    mvn install

    # 验证（包括集成测试）
    mvn verify

    # 解析依赖
    mvn dependency:resolve

    # 显示依赖树
    mvn dependency:tree

    # 显示项目信息
    mvn help:effective-pom

    # 代码格式化
    mvn formatter:format

    # 添加许可证头
    mvn license:format

下一步
==========

理解了构建和测试方法后，请参阅以下文档：

- :doc:`workflow` - 开发工作流程
- :doc:`contributing` - 贡献指南
- :doc:`architecture` - 理解代码库

参考资料
======

- `Maven 官方文档 <https://maven.apache.org/guides/>`__
- `JUnit 5 用户指南 <https://junit.org/junit5/docs/current/user-guide/>`__
- `JaCoCo 文档 <https://www.jacoco.org/jacoco/trunk/doc/>`__
