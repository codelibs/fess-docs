====================
开发环境设置
====================

本页面详细说明构建 |Fess| 开发环境的步骤。
从 IDE 的选择到源代码的获取、运行、调试，
逐步解说。

.. contents:: 目录
   :local:
   :depth: 2

系统要求
==========

开发环境建议使用以下硬件要求。

硬件要求
--------------

- **CPU**: 4核及以上
- **内存**: 8GB 以上（推荐 16GB）
- **磁盘**: 20GB 以上的可用空间

.. note::

   开发过程中 |Fess| 本体和内置的 OpenSearch 会同时运行，
   请确保有充足的内存和磁盘容量。

软件要求
--------------

- **OS**: Windows 10/11、macOS 11 及以上、Linux（Ubuntu 20.04 及以上等）
- **Java**: JDK 21 及以上
- **Maven**: 3.x 及以上
- **Git**: 2.x 及以上
- **IDE**: Eclipse、IntelliJ IDEA、VS Code 等

必需软件的安装
==========================

Java 的安装
-----------------

|Fess| 的开发需要 Java 21 及以上。

Eclipse Temurin 的安装（推荐）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

推荐使用 Eclipse Temurin（原 AdoptOpenJDK）。

1. 访问 `Adoptium <https://adoptium.net/temurin/releases/>`__
2. 下载 Java 21 的 LTS 版本
3. 按照安装程序的指示进行安装

安装确认
~~~~~~~~~~~~~~

在终端或命令提示符中执行以下命令：

.. code-block:: bash

    java -version

如果显示类似以下输出则成功：

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

环境变量的设置
~~~~~~~~~~~~

**Linux/macOS:**

在 ``~/.bashrc`` 或 ``~/.zshrc`` 中添加以下内容：

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. 打开「编辑系统环境变量」
2. 点击「环境变量」
3. 添加 ``JAVA_HOME``：``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. 在 ``PATH`` 中添加 ``%JAVA_HOME%\bin``

Maven 的安装
------------------

安装 Maven 3.x 及以上。

下载和安装
~~~~~~~~~~~~~~~~~~~~~~~~

1. 访问 `Maven 下载页面 <https://maven.apache.org/download.cgi>`__
2. 下载 Binary zip/tar.gz archive
3. 解压并放置到适当的位置

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. 解压 ZIP 文件
2. 放置到 ``C:\Program Files\Apache\maven`` 等位置

环境变量的设置
~~~~~~~~~~~~

**Linux/macOS:**

在 ``~/.bashrc`` 或 ``~/.zshrc`` 中添加以下内容：

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. 添加 ``MAVEN_HOME``：``C:\Program Files\Apache\maven``
2. 在 ``PATH`` 中添加 ``%MAVEN_HOME%\bin``

安装确认
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

如果显示类似以下输出则成功：

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Git 的安装
----------------

如果未安装 Git，请从以下位置安装。

- **Windows**: `Git for Windows <https://git-scm.com/download/win>`__
- **macOS**: ``brew install git`` 或 `Git 下载页面 <https://git-scm.com/download/mac>`__
- **Linux**: ``sudo apt install git`` (Ubuntu/Debian) 或 ``sudo yum install git`` (RHEL/CentOS)

安装确认：

.. code-block:: bash

    git --version

IDE 的设置
===============

Eclipse 的情况
------------

Eclipse 是 |Fess| 官方文档推荐的 IDE。

Eclipse 的安装
~~~~~~~~~~~~~~~~~~~~

1. 访问 `Eclipse 下载页面 <https://www.eclipse.org/downloads/>`__
2. 下载 "Eclipse IDE for Enterprise Java and Web Developers"
3. 运行安装程序并按照指示进行安装

推荐插件
~~~~~~~~~~~~

Eclipse 默认包含以下插件：

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

项目的导入
~~~~~~~~~~~~~~~~~~~~

1. 启动 Eclipse
2. 选择 ``File`` > ``Import``
3. 选择 ``Maven`` > ``Existing Maven Projects``
4. 指定 Fess 的源代码目录
5. 点击 ``Finish``

运行配置的设置
~~~~~~~~~~~~

1. 选择 ``Run`` > ``Run Configurations...``
2. 右键点击 ``Java Application`` 选择 ``New Configuration``
3. 设置以下内容：

   - **Name**: Fess Boot
   - **Project**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``

4. 点击 ``Apply``

IntelliJ IDEA 的情况
-------------------

IntelliJ IDEA 也是广泛使用的 IDE。

IntelliJ IDEA 的安装
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 访问 `IntelliJ IDEA 下载页面 <https://www.jetbrains.com/idea/download/>`__
2. 下载 Community Edition（免费）或 Ultimate Edition
3. 运行安装程序并按照指示进行安装

项目的导入
~~~~~~~~~~~~~~~~~~~~

1. 启动 IntelliJ IDEA
2. 选择 ``Open``
3. 选择 Fess 源代码目录的 ``pom.xml``
4. 点击 ``Open as Project``
5. 将自动作为 Maven 项目导入

运行配置的设置
~~~~~~~~~~~~

1. 选择 ``Run`` > ``Edit Configurations...``
2. 点击 ``+`` 按钮选择 ``Application``
3. 设置以下内容：

   - **Name**: Fess Boot
   - **Module**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``
   - **JRE**: Java 21

4. 点击 ``OK``

VS Code 的情况
------------

如果喜欢轻量级的开发环境，VS Code 也是一个选择。

VS Code 的安装
~~~~~~~~~~~~~~~~~~~~

1. 访问 `VS Code 下载页面 <https://code.visualstudio.com/>`__
2. 下载并运行安装程序

必要扩展的安装
~~~~~~~~~~~~~~~~~~~~~~~~

安装以下扩展：

- **Extension Pack for Java**: Java 开发所需的扩展集
- **Maven for Java**: Maven 支持

打开项目
~~~~~~~~~~~~~~~~

1. 启动 VS Code
2. 选择 ``File`` > ``Open Folder``
3. 选择 Fess 的源代码目录

源代码的获取
==============

从 GitHub 克隆
-------------------

从 GitHub 克隆 |Fess| 的源代码。

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

使用 SSH 的情况：

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   如果要 fork 后开发，请先在 GitHub 上 fork Fess 仓库，
   然后克隆 fork 的仓库：

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

项目的构建
==================

OpenSearch 插件的下载
---------------------------------

运行 Fess 需要 OpenSearch 的插件。
使用以下命令下载：

.. code-block:: bash

    mvn antrun:run

此命令将执行以下操作：

- 下载 OpenSearch
- 下载并安装必需插件
- 配置 OpenSearch

.. note::

   此命令只需在首次或更新插件时执行。
   不需要每次都执行。

首次构建
--------

构建项目：

.. code-block:: bash

    mvn clean compile

首次构建可能需要较长时间（下载依赖库等）。

构建成功时，会显示类似以下消息：

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Fess 的运行
==========

从命令行运行
--------------------

使用 Maven 运行：

.. code-block:: bash

    mvn compile exec:java

或者，打包后运行：

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

从 IDE 运行
------------

Eclipse 的情况
~~~~~~~~~~~~

1. 右键点击 ``org.codelibs.fess.FessBoot`` 类
2. 选择 ``Run As`` > ``Java Application``

或者，使用创建的运行配置：

1. 点击工具栏运行按钮的下拉菜单
2. 选择 ``Fess Boot``

IntelliJ IDEA 的情况
~~~~~~~~~~~~~~~~~~

1. 右键点击 ``org.codelibs.fess.FessBoot`` 类
2. 选择 ``Run 'FessBoot.main()'``

或者，使用创建的运行配置：

1. 点击工具栏运行按钮的下拉菜单
2. 选择 ``Fess Boot``

VS Code 的情况
~~~~~~~~~~~~

1. 打开 ``src/main/java/org/codelibs/fess/FessBoot.java``
2. 从 ``Run`` 菜单选择 ``Run Without Debugging``

启动确认
--------

Fess 的启动需要 1〜2 分钟。
控制台显示类似以下日志即表示启动完成：

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

在浏览器中访问以下地址确认运行：

- **搜索界面**: http://localhost:8080/
- **管理界面**: http://localhost:8080/admin/

  - 默认用户: ``admin``
  - 默认密码: ``admin``

端口号的更改
--------------

如果默认端口 8080 正在使用，可以在以下文件中更改：

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # 更改端口号
    server.port=8080

调试运行
==========

在 IDE 中调试运行
------------------

Eclipse 的情况
~~~~~~~~~~~~

1. 右键点击 ``org.codelibs.fess.FessBoot`` 类
2. 选择 ``Debug As`` > ``Java Application``
3. 设置断点，跟踪代码的运行

IntelliJ IDEA 的情况
~~~~~~~~~~~~~~~~~~

1. 右键点击 ``org.codelibs.fess.FessBoot`` 类
2. 选择 ``Debug 'FessBoot.main()'``
3. 设置断点，跟踪代码的运行

VS Code 的情况
~~~~~~~~~~~~

1. 打开 ``src/main/java/org/codelibs/fess/FessBoot.java``
2. 从 ``Run`` 菜单选择 ``Start Debugging``

远程调试
--------------

也可以将调试器连接到从命令行启动的 Fess。

以调试模式启动 Fess：

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

从 IDE 连接远程调试：

**Eclipse:**

1. 选择 ``Run`` > ``Debug Configurations...``
2. 右键点击 ``Remote Java Application`` 选择 ``New Configuration``
3. 设置 ``Port: 5005``
4. 点击 ``Debug``

**IntelliJ IDEA:**

1. 选择 ``Run`` > ``Edit Configurations...``
2. 选择 ``+`` > ``Remote JVM Debug``
3. 设置 ``Port: 5005``
4. 点击 ``OK`` 然后执行 ``Debug``

开发有用的设置
==============

日志级别的更改
--------------

调试时更改日志级别可以确认详细信息。

编辑 ``src/main/resources/log4j2.xml``：

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

启用热部署
-------------------

LastaFlute 可以在不重启的情况下反映部分更改。

在 ``src/main/resources/fess_config.properties`` 中设置以下内容：

.. code-block:: properties

    # 启用热部署
    development.here=true

但是，以下更改需要重启：

- 类结构的更改（方法的添加・删除等）
- 配置文件的更改
- 依赖库的更改

内置 OpenSearch 的操作
------------------------

开发环境使用内置的 OpenSearch。

OpenSearch 的位置：

.. code-block:: text

    target/fess/es/

直接访问 OpenSearch API：

.. code-block:: bash

    # 索引列表
    curl -X GET http://localhost:9201/_cat/indices?v

    # 文档搜索
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # 映射确认
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

使用外部 OpenSearch
--------------------

如果要使用外部的 OpenSearch 服务器，
编辑 ``src/main/resources/fess_config.properties``：

.. code-block:: properties

    # 禁用内置 OpenSearch
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

通过 DBFlute 生成代码
======================

|Fess| 使用 DBFlute 从 OpenSearch 的模式
自动生成 Java 代码。

模式更改后的重新生成
----------------------------

如果更改了 OpenSearch 的映射，使用以下命令
重新生成相应的 Java 代码：

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

各命令的说明：

- ``rm -rf mydbflute``: 删除现有的 DBFlute 工作目录
- ``mvn antrun:run``: 下载 OpenSearch 插件
- ``mvn dbflute:freegen``: 从模式生成 Java 代码
- ``mvn license:format``: 添加许可证头

故障排除
==================

构建错误
----------

**错误: Java 版本过旧**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

解决方法：安装 Java 21 及以上，并适当设置 ``JAVA_HOME``。

**错误: 依赖库下载失败**

.. code-block:: text

    [ERROR] Failed to collect dependencies

解决方法：确认网络连接，清除 Maven 的本地仓库后重试：

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

运行错误
--------

**错误: 端口 8080 已被使用**

.. code-block:: text

    Address already in use

解决方法：

1. 终止使用端口 8080 的进程
2. 或者，在 ``fess_config.properties`` 中更改端口号

**错误: OpenSearch 未启动**

请确认日志文件 ``target/fess/es/logs/``。

常见原因：

- 内存不足：增加 JVM 堆大小
- 端口 9201 正在使用：更改端口号
- 磁盘空间不足：确保有足够的磁盘空间

IDE 无法识别项目
----------------------------

**更新 Maven 项目**

- **Eclipse**: 右键点击项目 > ``Maven`` > ``Update Project``
- **IntelliJ IDEA**: 在 ``Maven`` 工具窗口点击 ``Reload All Maven Projects``
- **VS Code**: 从命令面板执行 ``Java: Clean Java Language Server Workspace``

下一步
==========

开发环境设置完成后，请参阅以下文档：

- :doc:`architecture` - 理解代码结构
- :doc:`workflow` - 学习开发工作流程
- :doc:`building` - 构建和测试的方法
- :doc:`contributing` - 创建拉取请求

资源
========

- `Eclipse 下载 <https://www.eclipse.org/downloads/>`__
- `IntelliJ IDEA 下载 <https://www.jetbrains.com/idea/download/>`__
- `VS Code 下载 <https://code.visualstudio.com/>`__
- `Maven 文档 <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
