=================
通过插件扩展 Fess
=================

前言
====

如果没有适合公司内部自有系统的 ``fess-ds-*`` 插件，或者想在所有文档注册之前对其进行加工，就需要自己编写插件。
本文面向 Java 开发者，说明如何基于官方模板创建可在 Fess 15.9 上运行的插件，并完成安装和运行确认。

按照本文的步骤操作后，您将能够：

- 理解插件的种类，以及 Fess 区分它们的机制
- 基于 ``fess-ds-example`` 构建数据存储插件，将其加入 Fess 并注册文档
- 基于 ``fess-ingest-example`` 创建在注册前加工文档的 Ingester

本文假定可以使用 Java 21 或更高版本和 Maven 3，并且 Fess 15.9 已在运行（:doc:`guide-02`）。
数据存储设置界面的用法在 :doc:`datastore-basics` 中说明，先阅读该文会更容易理解本文的步骤。

插件的种类
==========

插件是 jar 文件，放置在 Fess 安装目录的 ``app/WEB-INF/plugin/`` 中。
Fess 根据 jar 文件名的开头部分（前缀）判断插件的种类（``PluginHelper.ArtifactType``）。
15.9 中的种类如下。

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - 前缀
     - 作用
     - 可参考的仓库
   * - ``fess-ds``
     - 数据存储。从外部系统获取记录并注册
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester。在注册前加工文档
     - ``fess-ingest-example``
   * - ``fess-script``
     - 脚本引擎
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - Web 应用扩展（添加 API 或端点）
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - 缩略图生成
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - 爬虫客户端
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - AI 搜索模式使用的 LLM 提供商
     - ``fess-llm-openai``
   * - ``fess-storage``
     - 对象存储（S3 / GCS）
     - ``fess-storage-s3``
   * - ``fess-sso``
     - 单点登录的认证方式
     - ``fess-sso-oidc``

所有仓库都公开在 https://github.com/codelibs 上。

搜索界面的设计不通过插件来更改。
用于替换 JSP 的 ``fess-theme-*`` JAR 主题插件已在 15.9 中删除，搜索界面改为由 ``theme.yml``\ 、\ ``index.html``\ 、\ ``assets/`` 组成的 ZIP 主题。
主题在 [系统] > [主题] 中上传。
制作方法请参阅 `主题开发指南 <https://fess.codelibs.org/zh-cn/stable/dev/theme-development.html>`__\ ，嵌入现有网站的方法请参阅 :doc:`guide-03`。

创建数据存储插件
================

获取模板
--------

``fess-ds-example`` 是作为数据存储插件模板公开的仓库。
其默认分支对应开发中的版本（15.10.0-SNAPSHOT），因此要为 15.9 构建，需要使用与 15.9.0 对应的提交。

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

该提交与默认分支的区别只有 ``pom.xml`` 中的 2 行（项目版本和父 POM 版本）。
也可以停留在默认分支，将下一节中的 2 处改为 15.9 用的值，结果相同。

pom.xml
-------

``pom.xml`` 的要点如下。

.. code-block:: xml

    <artifactId>fess-ds-example</artifactId>
    <packaging>jar</packaging>
    <version>15.9.0-SNAPSHOT</version>

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.9.0</version>
        <relativePath />
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.opensearch</groupId>
            <artifactId>opensearch</artifactId>
            <version>${opensearch.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

``fess-parent`` 的版本要与安装插件的 Fess 版本一致。
在 ``fess-parent`` 15.9.0 中，\ ``fess.version`` 为 ``15.9.0``\ ，因此会针对 Fess 15.9.0 的 API 进行编译。
Fess 本体和 OpenSearch 的类在运行时由 Fess 提供，因此设为 ``provided``\ 。
实际的 ``pom.xml`` 中还有其他依赖项和构建设置，请先直接使用。
``fess`` 的 jar 不是从 Maven Central 获取，而是从 ``fess-parent`` 声明的 CodeLibs 仓库（\ ``https://maven.codelibs.org/release/``\ ）获取。
在使用代理或镜像的环境中，请确保可以访问该仓库。

改成自己的插件时，\ ``artifactId`` 必须以 ``fess-ds-`` 开头。
如后文所述，管理界面中「处理程序名称」的候选项只从文件名以 ``fess-ds`` 开头的 jar 中收集。

数据存储类
----------

数据存储继承 ``org.codelibs.fess.ds.AbstractDataStore``\ ，并实现 ``getName()`` 和 ``storeData(...)``\ 。
下面是从 ``ExampleDataStore`` 中只保留处理骨架的代码。
它用于理解机制，构建时请直接使用仓库中的 ``ExampleDataStore``\ （测试使用了骨架中没有的方法，替换后测试将无法通过编译）。

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.HashMap;
    import java.util.LinkedHashMap;
    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback, final DataStoreParams paramMap,
                final Map<String, String> scriptMap, final Map<String, Object> defaultDataMap) {
            final String scriptType = getScriptType(paramMap);
            final int dataSize = Integer.parseInt(paramMap.getAsString("data.size", "10"));

            for (int i = 0; i < dataSize && alive; i++) {
                // 从外部系统获取的 1 条记录（此处为固定值）
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // 脚本针对“参数 + 记录”进行求值
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(source);

                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }
                callback.store(paramMap, dataMap);
            }
        }
    }

各部分的作用如下。

- ``getName()`` 的返回值作为该数据存储的名称注册到 ``DataStoreFactory`` 中。惯例是返回类的简单名称
- ``paramMap`` 中存放数据存储设置的「参数」栏的值。用 ``getAsString(键, 默认值)`` 取出
- ``scriptMap`` 是「脚本」栏中 ``字段名=表达式`` 形式的各行。\ ``convertValue()`` 对表达式求值，并将结果放入索引的字段
- ``defaultDataMap`` 中存放由数据存储设置决定的值，例如设置 ID、权限（角色）、提升值、虚拟主机等。先复制它，再添加各个字段
- 用 ``callback.store()`` 逐条注册。作业停止后 ``alive`` 会变为 ``false``\ ，因此要将它放入循环条件

也就是说，哪条记录的值放入哪个字段并不写在插件中，而是由管理员在「脚本」栏中决定。
插件的职责是获取记录并将其放入 ``resultMap``\ 。

实际的 ``ExampleDataStore`` 除此之外还实现了以记录为单位的异常处理（记录到 [失败URL]）和爬取统计（\ ``CrawlerStatsHelper``\ ）。
创建自己的插件时，请复制 ``ExampleDataStore`` 而不是这个骨架，并改写标有 ``// CUSTOMIZE:`` 的位置（获取记录的部分）。

DI 配置文件
-----------

仅创建类并不会被 Fess 加载。
需要在 ``src/main/resources/fess_ds++.xml`` 中将其注册为组件。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

DI 容器（Lasta Di）会将类路径上的 ``fess_ds++.xml`` 合并到 Fess 本体的 ``fess_ds.xml`` 中。
通过 ``<postConstruct name="register">``\ ，组件生成后会调用 ``AbstractDataStore.register()``\ ，并以 ``getName()`` 的名称注册。
如果更改了类名或包名，请同时修改 ``class`` 属性。

构建
----

::

    $ mvn clean package

``target/`` 中会生成 3 个 jar。
要放入 Fess 的是不带 ``-sources`` 或 ``-javadoc`` 的 ``fess-ds-example-15.9.0-SNAPSHOT.jar``\ 。
可以用 ``unzip -l`` 确认其中包含 ``fess_ds++.xml`` 和 ``ExampleDataStore.class``\ 。

安装
====

从管理界面安装最为简便。

1. 在 [系统] > [插件] 中点击 [安装]
2. [远程] 选项卡的下拉列表保持为第一项 ``-``\ 。如果选择了其他插件，安装的将是那个插件
3. 在 [本地] 选项卡的「Jar文件」中选择构建好的 jar，然后点击 [安装]
4. 重启 Fess

上传的 jar 以 ``<名称>-<版本>.jar`` 的形式保存在 ``app/WEB-INF/plugin/`` 中。
由于从文件名中读取名称和版本，请不要更改 Maven 生成的文件名，直接上传。
也可以不使用管理界面，直接将 jar 复制到该目录后重启，效果相同（Docker 镜像中为 ``/usr/share/fess/app/WEB-INF/plugin/``\ ）。

使用 Docker 时，\ ``FESS_PLUGINS`` 是获取仓库中已发布插件的机制，不能用于自己编写的 jar。
请从管理界面安装后，用 ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01`` 重启。
jar 放置在容器内，因此用 ``down`` 和 ``up`` 重新创建容器后会消失。
这种情况下请重新安装。

确认运行
========

确认处理程序名称
----------------

重启后，打开 [爬虫] > [数据存储] > [新建]，确认「处理程序名称」下拉列表中有 ``ExampleDataStore``\ 。
这些候选项由 ``app/WEB-INF/plugin/`` 中文件名以 ``fess-ds`` 开头的 jar 生成。
Fess 读取 jar 中的 ``fess_ds++.xml``\ ，将 ``class`` 属性中所写类的简单名称作为候选项（缓存 60 秒）。
如果没有显示，请检查 jar 的文件名、jar 中的 ``fess_ds++.xml`` 以及是否已重启。

创建数据存储设置
----------------

在同一界面中按如下内容输入，然后点击 [创建]。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 值
   * - 名称
     - ``Example``
   * - 处理程序名称
     - ``ExampleDataStore``
   * - 参数
     - 在已填入的 ``script_type=javascript`` 的下一行添加 ``data.size=5``
   * - 脚本
     - ``title=title``\ 、\ ``content=body``\ 、\ ``url=url`` 共 3 行

当脚本右侧与记录的键（\ ``title``\ 、\ ``body``\ 、\ ``url``\ ）一致时，\ ``convertValue()`` 不使用脚本引擎，而是直接返回该值。
如果写成 ``content=title + " " + body`` 这样的表达式，则由 ``script_type`` 指定的引擎求值。
如果删除 ``script_type``\ ，将被视为 ``groovy``\ ，在未安装 ``fess-script-groovy`` 的环境中表达式求值会失败，因此请保留，不要删除。

``url`` 是必需的。
``callback.store()`` 不接受没有 ``url`` 的文档，会抛出异常。

运行作业
--------

1. 在 [爬虫] > [数据存储] 列表中点击 ``Example``\ ，然后点击 [创建新作业]
2. 调度器的创建界面打开后，直接点击 [创建]
3. 在 [系统] > [调度器] 中打开创建的作业，点击 [立即开始]

确认结果
--------

确认以下 4 点。

1. 在 [系统信息] > [作业日志] 中，作业状态为「OK」
2. 在 [系统信息] > [爬网信息] 中，该会话的「索引大小 (数据存储)」为 ``5``
3. [系统信息] > [失败URL] 中没有记录
4. 在 [系统信息] > [搜索] 中搜索 ``Sample``\ ，显示 ``Sample 0`` 到 ``Sample 4`` 共 5 条结果

即使作业状态为「OK」，也不一定表示数据存储的处理成功。
例如，从脚本中删除 ``url=url`` 后运行，\ ``callback.store()`` 会对所有记录抛出异常，注册数为 0。
``ExampleDataStore`` 以记录为单位捕获异常，因此 [失败URL] 中会记录 ``record:0`` 到 ``record:4``\ ，\ ``fess-crawler.log`` 中会输出 WARN，但作业日志仍为「OK」。
对于像骨架那样不捕获异常的代码，整个设置都会失败，[失败URL] 中只以 ``D<设置ID>:Example`` 的形式记录 1 条。
确认步骤和日志位置汇总在 :doc:`datastore-basics` 中关于确认结果的一节。

确认到这里之后，就可以将 ``createSourceRecord()`` 等获取记录的部分替换为读取实际 API 或文件的处理。
外部系统的连接目标和认证信息不要写在代码中，而是通过「参数」栏用 ``paramMap`` 接收。

模板的 ``src/test`` 中有使用 UTFlute 的 ``LastaDiTestCase`` 的测试。
通过实现了 ``IndexUpdateCallback`` 的测试类收集传给 ``store()`` 的 ``dataMap``\ ，检查条数和字段值。
因此无需 OpenSearch 即可运行 ``mvn test``\ 。
改写获取记录的部分后，也请相应地修改这些测试。

使用 Ingester 在注册前加工文档
==============================

无论是数据存储、Web 还是文件系统的爬取，Ingester 都会在文档发送到索引之前被调用。
可用于为所有文档添加公共字段、对值进行规范化等处理。
没有按设置启用或禁用的机制，安装后会应用于所有爬取。

继承 ``org.codelibs.fess.ingest.Ingester``\ ，只重写需要的 ``process`` 方法。

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 方法
     - 调用时机
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - 数据存储爬取（在 ``callback.store()`` 中）
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - Web、文件爬取注册索引时
   * - ``process(ResultData target, ResponseData responseData)``
     - 处理 Web、文件爬取获取的响应时
   * - ``protected process(Map<String, Object> target)``
     - 上面两个 ``Map`` 版本默认调用的方法。想同时作用于数据存储和 Web、文件爬取时，只重写这一个

下面是从 ``fess-ingest-example`` 的 ``ExampleIngester`` 中只保留数据存储处理的代码。

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {
        private static final Logger logger = LogManager.getLogger(ExampleIngester.class);

        public ExampleIngester() {
            setPriority(50);
        }

        @Override
        public Map<String, Object> process(final Map<String, Object> target, final DataStoreParams params) {
            target.put("ingested_by", ExampleIngester.class.getSimpleName());
            logger.info("DATASTORE CRAWL: {}", target);
            return target;
        }
    }

注册在 ``src/main/resources/fess_ingest++.xml`` 中进行。
其内容与 ``fess_ds++.xml`` 形式相同，为名为 ``exampleIngester`` 的组件加上 ``<postConstruct name="register">``\ 。
``Ingester.register()`` 会将自身添加到 ``IngestFactory`` 中。

模板的获取、构建、安装和重启与数据存储的步骤相同（15.9 用的提交为 ``8a1e45ddb63a118802287120effd3ce49fb60bfb``\ ，jar 为 ``fess-ingest-example-15.9.0-SNAPSHOT.jar``\ ）。
自己的插件中，artifactId 要以 ``fess-ingest-`` 开头。

实现时请注意以下几点。

- 修改 ``target`` 后务必将其返回。返回值会原样传给下一个 Ingester 和索引器，且没有 ``null`` 检查。返回 ``null`` 并不会排除该文档，而是会破坏注册处理
- 多个 Ingester 按 ``priority`` 从小到大的顺序执行（默认值为 99）。下一个 Ingester 会接收前一个 Ingester 修改后的 ``target``
- 如果 ``process`` 中发生异常，Fess 会在日志中输出 WARN 并继续执行下一个 Ingester。文档的注册不会停止。异常发生前对 ``target`` 所做的修改会保留

运行确认方法是：再次运行在上文“确认运行”中创建的数据存储设置的作业。
Ingester 在爬虫进程中运行，因此如果 ``fess-crawler.log`` 中每个文档都输出了 ``DATASTORE CRAWL:`` 行，就说明它已被调用。
仓库中的 ``ExampleIngester`` 也会将 Web、文件爬取的文档以 ``WEB/FILE CRAWL:`` 逐条输出到日志。
由于它作用于所有爬取，确认完成后请在 [系统] > [插件] 中删除，并重启 Fess。

升级 Fess 时
============

插件要使用与安装目标 Fess 相同次版本的 ``fess-parent`` 构建（Fess 15.9 则为 15.9.x）。
已公开的插件也针对 Fess 的每个次版本发布了对应的版本。

将 Fess 升级到 15.10 时，请将 ``pom.xml`` 中 ``fess-parent`` 的版本改为对应版本并重新构建。
在 [系统] > [插件] 列表中删除旧的 jar，安装新的 jar 后重启。
``bin/fess-setup upgrade plugins`` 是从插件仓库获取新版本的机制，因此无法用这种方法更新仓库中没有的自制插件。

延伸阅读
========

- 想详细了解数据存储设置的参数、脚本、权限和调度：:doc:`datastore-basics`
- 想查看已公开的数据存储插件的配置示例：:doc:`guide-06`\ 、\ :doc:`guide-07`\ 、\ :doc:`guide-12`
- 想更改搜索界面的外观：:doc:`guide-03`
- 想使用 LLM 插件启用 AI 搜索模式：:doc:`guide-19`
- 想使用 Web 应用插件（MCP 服务器）：:doc:`guide-20`

参考资料
========

- `插件架构 <https://fess.codelibs.org/zh-cn/stable/dev/plugin-architecture.html>`__
- `数据存储插件开发 <https://fess.codelibs.org/zh-cn/stable/dev/datastore-plugin.html>`__
- `Ingest插件 <https://fess.codelibs.org/zh-cn/stable/dev/ingest-plugin.html>`__
- `主题开发指南 <https://fess.codelibs.org/zh-cn/stable/dev/theme-development.html>`__
- `插件（管理界面） <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `fess-ds-example（GitHub） <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example（GitHub） <https://github.com/codelibs/fess-ingest-example>`__
