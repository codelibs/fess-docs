============================
架构和代码结构
============================

本页面说明 |Fess| 的架构、代码结构、
主要组件。
通过理解 |Fess| 的内部结构，可以高效地进行开发。

.. contents:: 目录
   :local:
   :depth: 2

整体架构
================

|Fess| 由以下主要组件构成：

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │            用户界面                             │
    │  ┌──────────────┐      ┌──────────────┐        │
    │  │   搜索界面    │      │   管理界面    │        │
    │  │  (JSP/HTML)   │      │   (JSP/HTML)  │        │
    │  └──────────────┘      └──────────────┘        │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │             Web 应用层                          │
    │  ┌──────────────────────────────────────────┐  │
    │  │           LastaFlute                       │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │ Action │  │  Form   │  │  Service │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │             业务逻辑层                          │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
    │  │ Crawler  │  │  Job     │  │  Helper  │    │
    │  └──────────┘  └──────────┘  └──────────┘    │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │             数据访问层                          │
    │  ┌──────────────────────────────────────────┐  │
    │  │          DBFlute / OpenSearch             │  │
    │  │  ┌────────┐  ┌─────────┐  ┌──────────┐  │  │
    │  │  │Behavior│  │ Entity  │  │  Query   │  │  │
    │  │  └────────┘  └─────────┘  └──────────┘  │  │
    │  └──────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘
                        ↓
    ┌─────────────────────────────────────────────────┐
    │               数据存储                          │
    │              OpenSearch 3.5.0                   │
    └─────────────────────────────────────────────────┘

层的说明
------------

用户界面层
~~~~~~~~~~~~~~~~~~~~~~~~

用户直接操作的界面。
使用 JSP 和 HTML、JavaScript 实现。

- 搜索界面: 面向最终用户的搜索界面
- 管理界面: 面向系统管理员的设置・管理界面

Web 应用层
~~~~~~~~~~~~~~~~~~~~

使用 LastaFlute 框架的 Web 应用层。

- **Action**: 处理 HTTP 请求并调用业务逻辑
- **Form**: 接收请求参数和验证
- **Service**: 实现业务逻辑

业务逻辑层
~~~~~~~~~~~~~~~~

实现 |Fess| 主要功能的层。

- **Crawler**: 从网站和文件系统收集数据
- **Job**: 定时执行的任务
- **Helper**: 应用程序中使用的辅助类

数据访问层
~~~~~~~~~~~~~~

使用 DBFlute 访问 OpenSearch 的层。

- **Behavior**: 数据操作的接口
- **Entity**: 数据实体
- **Query**: 构建搜索查询

数据存储层
~~~~~~~~~~~~

使用 OpenSearch 3.5.0 作为搜索引擎。

项目结构
==============

目录结构
--------------

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/org/codelibs/fess/
    │   │   │   ├── app/              # Web 应用
    │   │   │   │   ├── web/          # 搜索界面
    │   │   │   │   │   ├── admin/    # 管理界面
    │   │   │   │   │   │   ├── ...Action.java
    │   │   │   │   │   │   └── ...Form.java
    │   │   │   │   │   └── ...Action.java
    │   │   │   │   └── service/      # 服务层
    │   │   │   ├── crawler/          # Crawler
    │   │   │   │   ├── helper/       # Crawler helper
    │   │   │   │   ├── processor/    # Crawl processing
    │   │   │   │   ├── service/      # Crawler service
    │   │   │   │   └── transformer/  # Data transformation
    │   │   │   ├── opensearch/       # OpenSearch related
    │   │   │   │   ├── client/       # OpenSearch client
    │   │   │   │   ├── config/       # Configuration management
    │   │   │   │   ├── log/          # Log management
    │   │   │   │   ├── query/        # Query builder
    │   │   │   │   └── user/         # User management
    │   │   │   ├── helper/           # 辅助类
    │   │   │   │   ├── ...Helper.java
    │   │   │   ├── job/              # 作业
    │   │   │   │   ├── ...Job.java
    │   │   │   ├── util/             # 实用工具
    │   │   │   ├── entity/           # 实体（自动生成）
    │   │   │   ├── mylasta/          # LastaFlute 配置
    │   │   │   │   ├── action/       # Action 基类
    │   │   │   │   ├── direction/    # 应用配置
    │   │   │   │   └── mail/         # 邮件配置
    │   │   │   ├── Constants.java    # 常量定义
    │   │   │   └── FessBoot.java     # 启动类
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties  # 配置文件
    │   │   │   ├── fess_config.xml         # LastaDi component configuration
    │   │   │   ├── fess_message_ja.properties  # 消息（日语）
    │   │   │   ├── fess_message_en.properties  # 消息（英语）
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       ├── WEB-INF/
    │   │       │   ├── view/          # JSP 文件
    │   │       │   │   ├── admin/     # 管理界面 JSP
    │   │       │   │   └── ...
    │   │       │   └── web.xml
    │   │       ├── css/               # CSS 文件
    │   │       ├── js/                # JavaScript 文件
    │   │       └── images/            # 图片文件
    │   └── test/
    │       └── java/org/codelibs/fess/
    │           ├── ...Test.java       # 测试类
    │           └── it/                # 集成测试
    ├── pom.xml                        # Maven 配置
    ├── dbflute_fess/                  # DBFlute 配置
    │   ├── dfprop/                    # DBFlute 属性
    │   └── freegen/                   # FreeGen 配置
    └── README.md

主要包的详情
==================

app 包
------------

Web 应用层的代码。

app.web 包
~~~~~~~~~~~~~~~~

实现搜索界面和面向最终用户的功能。

**主要类:**

- ``SearchAction.java``: 搜索处理
- ``LoginAction.java``: 登录处理

**例:**

.. code-block:: java

    @Execute
    public HtmlResponse index(SearchForm form) {
        // 搜索处理的实现
        return asHtml(path_IndexJsp);
    }

app.web.admin 包
~~~~~~~~~~~~~~~~~~~~~~~

实现管理界面的功能。

**主要类:**

- ``AdminWebconfigAction.java``: Web 爬取配置
- ``AdminSchedulerAction.java``: 调度程序管理
- ``AdminUserAction.java``: 用户管理

**命名规则:**

- ``Admin`` 前缀: Admin 用 Action
- ``Action`` 后缀: Action 类
- ``Form`` 后缀: Form 类

app.service 包
~~~~~~~~~~~~~~~~~~~~

实现业务逻辑的服务层。

**主要类:**

- ``SearchLogService.java``: 搜索服务
- ``UserService.java``: 用户管理服务
- ``ScheduledJobService.java``: 作业管理服务

**例:**

.. code-block:: java

    public class ScheduledJobService {
        @Resource
        private ScheduledJobBhv scheduledJobBhv;

        // Job CRUD operations implementation
    }

crawler 包
----------------

实现数据收集功能。

crawler 包 (fess-crawler 库)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**主要类:**

- ``CrawlerClient.java``: 爬虫客户端接口
- ``HcHttpClient.java``: HTTP 客户端
- ``FileSystemClient.java``: 文件系统客户端
- ``ExtractorFactory.java``: 提取器工厂
- ``TikaExtractor.java``: 使用 Apache Tika 提取
- ``Transformer.java``: 转换接口

crawler 包 (fess main)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**主要类:**

- ``FessStandardTransformer.java``: Fess 标准转换器
- ``FessXpathTransformer.java``: Fess XPath 转换器

opensearch 包
-------------------

实现与 OpenSearch 的集成。

opensearch.client 包
~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch 客户端的实现。

**主要类:**

- ``SearchEngineClient.java``: OpenSearch 客户端

opensearch.query 包
~~~~~~~~~~~~~~~~~~~~~~~~~

实现搜索查询的构建。

**主要类:**

- ``QueryCommand.java``: 查询命令
- ``QueryProcessor.java``: 查询处理

helper 包
---------------

应用程序中使用的辅助类。

**主要类:**

- ``SystemHelper.java``: 系统整体的辅助类
- ``CrawlingConfigHelper.java``: 爬取配置的辅助类
- ``SearchLogHelper.java``: 搜索日志的辅助类
- ``UserInfoHelper.java``: 用户信息的辅助类
- ``ViewHelper.java``: 视图相关的辅助类
- ``QueryHelper.java``: 查询构建的辅助类

**例:**

.. code-block:: java

    public class SystemHelper {
        @PostConstruct
        public void init() {
            // 系统初始化处理
        }
    }

job 包
------------

实现定时执行的作业。

**主要类:**

- ``CrawlJob.java``: 爬取作业
- ``SuggestJob.java``: 建议作业
- ``ScriptExecutorJob.java``: 脚本执行作业

**例:**

.. code-block:: java

    public class CrawlJob extends ExecJob {
        @Override
        public void execute() {
            // 爬取处理的实现
        }
    }

entity 包
---------------

对应 OpenSearch 文档的实体类。
此包由 DBFlute 自动生成。

**主要类:**

- ``SearchLog.java``: 搜索日志
- ``ClickLog.java``: 点击日志
- ``FavoriteLog.java``: 收藏日志
- ``User.java``: 用户信息
- ``Role.java``: 角色信息

.. note::

   entity 包的代码是自动生成的，
   不要直接编辑。
   通过更改模式并重新生成来更新。

mylasta 包
----------------

进行 LastaFlute 的配置和自定义。

mylasta.action 包
~~~~~~~~~~~~~~~~~~~~~~~

定义 Action 的基类。

- ``FessUserBean.java``: 用户信息
- ``FessHtmlPath.java``: HTML 路径定义

mylasta.direction 包
~~~~~~~~~~~~~~~~~~~~~~~~~~

进行应用程序整体的配置。

- ``FessConfig.java``: 配置的读取
- ``FessFwAssistantDirector.java``: 框架配置

设计模式和实现模式
============================

|Fess| 使用以下设计模式。

MVC 模式
----------

使用 LastaFlute 实现 MVC 模式。

- **Model**: Service、Entity
- **View**: JSP
- **Controller**: Action

例：

.. code-block:: java

    // Controller (Action)
    public class SearchAction extends FessSearchAction {
        @Resource
        private SearchHelper searchHelper;  // Model (Service)

        @Execute
        public HtmlResponse index(SearchForm form) {
            return search(form);
        }
    }

DI 模式
---------

使用 LastaFlute 的 DI 容器。

.. code-block:: java

    public class SearchService {
        @Resource
        private SearchEngineClient searchEngineClient;

        @Resource
        private UserInfoHelper userInfoHelper;
    }

Factory 模式
--------------

用于生成各种组件。

.. code-block:: java

    public class ExtractorFactory {
        public Extractor getExtractor(String key) {
            // 根据 MIME 类型生成 Extractor
        }
    }

Strategy 模式
---------------

用于爬虫和转换器。

.. code-block:: java

    public interface Transformer {
        ResultData transform(ResponseData responseData);
    }

    public class HtmlTransformer implements Transformer {
        // HTML 的转换处理
    }

配置管理
======

|Fess| 的配置在多个文件中管理。

fess_config.properties
--------------------

定义应用程序的主要配置。

.. code-block:: properties

    # OpenSearch 连接配置
    search_engine.http.url=http://localhost:9201

    # 爬取配置
    crawler.document.max.site.length=100
    crawler.document.cache.enabled=true

fess_config.xml
--------------

LastaDi component configuration file.

.. code-block:: xml

    <component name="systemProperties" class="org.codelibs.core.misc.DynamicProperties">
        <arg>
            org.codelibs.fess.util.ResourceUtil.getConfPath("system.properties")
        </arg>
    </component>

fess_message_*.properties
------------------------

多语言支持的消息文件。

- ``fess_message_ja.properties``: 日语
- ``fess_message_en.properties``: 英语

数据流
==========

搜索流程
--------

.. code-block:: text

    1. 用户在搜索界面搜索
       ↓
    2. SearchAction 接收搜索请求
       ↓
    3. SearchService 执行业务逻辑
       ↓
    4. SearchEngineClient 向 OpenSearch 发送搜索查询
       ↓
    5. OpenSearch 返回搜索结果
       ↓
    6. SearchService 格式化结果
       ↓
    7. SearchAction 将结果传递给 JSP 显示

爬取流程
------------

.. code-block:: text

    1. CrawlJob 定时执行
       ↓
    2. CrawlingConfigHelper 获取爬取配置
       ↓
    3. CrawlerClient 访问目标站点
       ↓
    4. Extractor 从内容提取文本
       ↓
    5. Transformer 将数据转换为搜索用的格式
       ↓
    6. SearchEngineClient 向 OpenSearch 注册文档

扩展点
==========

|Fess| 可以在以下点进行扩展。

添加自定义爬虫
--------------------

实现 ``CrawlerClient`` 接口，可以支持独特的数据源。

添加自定义转换器
----------------------------

实现 ``Transformer``，可以添加独特的数据转换处理。

添加自定义提取器
--------------------------

实现 ``Extractor``，可以添加独特的内容提取处理。

添加自定义插件
--------------------

通过管理 UI 的插件管理功能来管理插件。

参考资料
======

框架
------------

- `LastaFlute 参考 <https://github.com/lastaflute/lastaflute>`__
- `DBFlute 文档 <https://dbflute.seasar.org/>`__

技术文档
--------------

- `OpenSearch API 参考 <https://opensearch.org/docs/latest/api-reference/>`__
- `Apache Tika <https://tika.apache.org/>`__

下一步
==========

理解了架构后，请参阅以下文档：

- :doc:`workflow` - 实际的开发流程
- :doc:`building` - 构建和测试
- :doc:`contributing` - 创建拉取请求
