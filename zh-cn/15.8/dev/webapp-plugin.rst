==================================
Web应用插件
==================================

概述
====

Web应用插件（``fess-webapp-*``）是用于扩展 |Fess| 的Web应用程序的插件。
与其他类型的插件不同，它并非直接添加 Action 类或 JSP，而是通过对 DI 容器
（Lasta Di）\ **添加或替换组件** 来扩展功能。典型的用途如下：

- 添加新组件（辅助类、服务等）
- 替换（子类化）\ |Fess| 本体的组件
- 添加 REST API 端点（``WebApiManager``）
- 扩展搜索行为（查询命令、Rank Fusion 等）

.. note::

   Web应用插件以 JAR 文件的形式分发，其中的类和 DI 配置文件会被加载到
   |Fess| 的Web应用程序的类路径中。它并不能添加 JSP 视图。如果需要自定义
   搜索界面的设计，请参考 :doc:`theme-development`。

基本结构
========

以Web应用插件的实现模板
`fess-webapp-example <https://github.com/codelibs/fess-webapp-example>`__
为例，插件由"实现类"和"DI 注册文件"构成：

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # 要添加的组件
        │   └── CustomSystemHelper.java   # 核心组件的替换
        └── resources/
            ├── app++.xml                 # 组件的添加（合并）
            └── fess+systemHelper.xml     # 组件的替换

.. note::

   实现类的包名使用 ``org.codelibs.fess.webapp.<插件名>``\ 。DI 配置文件
   存放在 ``src/main/resources/`` 中。与数据存储插件不同，这里不包含
   ``src/main/webapp/`` 或 JSP。

pom.xml与清单文件
=================

Web应用插件以 ``fess-parent`` 作为父 POM，构建为 jar。由 |Fess| 本体在
运行时提供的 ``fess``、``opensearch`` 需以 ``provided`` 作用域声明；
``lastaflute``、``dbflute-runtime``、``corelib`` 等运行时所需的库，则以
通常的作用域声明。

Web应用插件中最重要的一点，是在 JAR 清单文件中添加
``Fess-WebAppJar: true``\ 。通过这一声明，|Fess| 会将插件的类和 DI 配置
文件挂载到Web应用程序的类加载器中。该设置通过 ``maven-jar-plugin``
完成：

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-jar-plugin</artifactId>
                <configuration>
                    <archive>
                        <manifestEntries>
                            <Fess-WebAppJar>true</Fess-WebAppJar>
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>

.. warning::

   如果不添加 ``Fess-WebAppJar: true``，插件的类和 DI 配置文件将不会被
   加载到Web应用程序的类路径中，组件的添加与替换也将不会生效。

关于 pom.xml 的完整构成（父 POM、依赖关系的声明方法等），请参考
:doc:`plugin-architecture`。

扩展模式
========

组件的添加（app++.xml）
-----------------------

最基本的扩展方式是添加自己的组件。Lasta Di 会将类路径上的 ``app++.xml``
**合并** 到由 |Fess| 本体的 ``app.xml`` 构建而成的 ``app`` 命名空间中
（末尾的 ``++`` 是追加合并的约定）。由于添加的组件使用了 |Fess| 本体中
不存在的名称，因此不会覆盖任何内容。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

在组件的实现中，初始化使用 ``@PostConstruct``，|Fess| 本体的组件则通过
``ComponentUtil`` 获取后复用（不进行复制或覆盖）：

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // 由 DI 生成后仅调用一次的初始化处理
        }

        public String getPluginLabel() {
            // 复用核心的 SystemHelper 获取正在运行的 Fess 版本
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   请首先考虑这种"组件的添加"方式。只要不需要修改核心功能，它就比替换
   更安全，也更易于维护。

核心组件的替换（fess+componentName.xml）
-----------------------------------------

如果想要改变 |Fess| 本体组件的行为，需要将目标类子类化，并在名为
``<baseDicon>+<componentName>.xml`` 的 DI 配置文件中 \*\*以相同的组件名
重新注册\*\*。例如，由于 ``systemHelper`` 是在 |Fess| 本体的 ``fess.xml``
中声明的，因此替换文件应为 ``fess+systemHelper.xml``\ （而不是
``app+systemHelper.xml``）。

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import java.nio.file.Path;

    import org.codelibs.fess.helper.SystemHelper;

    public class CustomSystemHelper extends SystemHelper {

        @Override
        protected void parseProjectProperties(final Path propPath) {
            try {
                super.parseProjectProperties(propPath);
            } catch (final Exception e) {
                // 自定义处理
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   替换（单个 ``+``）会 **整体** 替换组件定义。因此，替换文件中必须写出
   核心定义所进行的所有 ``<postConstruct>``\ 。例如，在替换
   ``systemHelper`` 时，必须将设计 JSP 名称的映射
   （``addDesignJspFileName``）从核心的 ``fess.xml`` 中全部复制过来并
   写入。这些内容需要随 |Fess| 的每次发布进行同步，一旦有遗漏，部分画面
   （如 ``chat`` / ``login`` 等）将无法解析。这一维护成本，正是相比替换
   更推荐使用添加方式的原因。

REST API的添加（fess_api++.xml）
---------------------------------

要添加新的 REST API 端点，需要实现 ``WebApiManager``\ 。继承
``BaseApiManager``，并在 ``@PostConstruct`` 中向 ``WebApiManagerFactory``
注册自身。注册后的 API 管理器会在每次请求时被 ``WebApiFilter`` 调用。
通过 ``fess_api++.xml`` 注册组件：

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleApiManager"
            class="org.codelibs.fess.webapp.example.api.ExampleApiManager">
        </component>
    </components>

.. code-block:: java

    package org.codelibs.fess.webapp.example.api;

    import java.io.IOException;

    import org.codelibs.fess.api.BaseApiManager;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;
    import jakarta.servlet.FilterChain;
    import jakarta.servlet.ServletException;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;

    public class ExampleApiManager extends BaseApiManager {

        public ExampleApiManager() {
            // 该管理器所处理路径的前缀
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // 判断该管理器是否处理此请求
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // 处理请求并写入响应
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // 设置响应头（如有需要）
        }
    }

作为实现示例，可以参考提供 ``/api/v1`` 的
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__，
以及提供 ``/json`` / ``/suggest`` 的
`fess-webapp-classic-api <https://github.com/codelibs/fess-webapp-classic-api>`__\ 。

搜索界面的自定义
================

Web应用插件无法添加 JSP 视图。这是因为 JSP 视图存放在 |Fess| 本体 WAR 的
``WEB-INF/view/`` 中，而插件 JAR 是挂载到类路径（``WEB-INF/classes``）
上的。如果需要修改搜索界面的设计，请使用以下方式之一：

- **主题**：自定义搜索界面的设计（HTML/CSS/JavaScript）。请参考
  :doc:`theme-development`。
- **替换 systemHelper**：通过上述"核心组件的替换"方式，可以更改设计
  JSP 名称的映射（但 JSP 文件本身仍由 |Fess| 本体提供）。

构建与安装
==========

::

    mvn clean package

会在 ``target/`` 目录下生成 JAR 文件（例如
``fess-webapp-example-15.8.0.jar``）。生成的 JAR 可以从管理界面安装，
也可以放置到 ``app/WEB-INF/plugin/`` 目录后重启 |Fess|\ 。安装步骤的详细
信息请参考 :doc:`../admin/plugin-guide`。

公开插件示例
============

|Fess| 项目公开了以下Web应用插件。这些插件已在
`GitHub <https://github.com/codelibs>`__ 上公开，可作为开发参考：

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 插件
     - 说明
   * - ``fess-webapp-example``
     - 插件实现的模板
   * - ``fess-webapp-v1-api``
     - ``/api/v1`` REST API
   * - ``fess-webapp-classic-api``
     - ``/json`` / ``/suggest`` 旧版REST API
   * - ``fess-webapp-mcp``
     - MCP（Model Context Protocol）服务器
   * - ``fess-webapp-semantic-search``
     - 神经搜索/向量搜索
   * - ``fess-webapp-multimodal``
     - 多模态（图像、文本）搜索

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`theme-development` - 主题自定义
- :doc:`../admin/plugin-guide` - 插件安装
- :doc:`overview` - 开发者文档概述
