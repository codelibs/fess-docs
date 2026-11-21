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
``<baseDicon>+<componentName>.xml`` 的 DI 配置文件中 **以相同的组件名
重新注册**。例如，由于 ``systemHelper`` 是在 |Fess| 本体的 ``fess.xml``
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
   核心定义所进行的所有 ``<postConstruct>``\ （例如 ``app.xml`` 中的
   ``queryHelper``）。这些内容需要随 |Fess| 的每次发布进行同步。如果继续
   调用已从核心中删除的方法，该组件定义将因 ``BeanMethodNotFoundException``
   而初始化失败。例如，15.9 删除了 ``systemHelper`` 的
   ``addDesignJspFileName``\ ，因此调用它的替换文件会失败。这一维护成本，
   正是相比替换更推荐使用添加方式的原因。

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

.. _webapp-plugin-password-encoder:

密码哈希算法的添加（fess++.xml）
--------------------------------

本地用户密码的哈希由组件生成。保存的密码以 ``{id}hash`` 的形式写入。 |Fess| 会根据保存值中的 ``id`` （对于新密码，则根据 ``app.password.algorithm`` 的值，默认为 ``bcrypt`` ）查找名为 ``<id>PasswordEncoder`` 的 DI 组件，其方式与解析 ``<sso.type>Authenticator`` 和 ``<storage.type>StorageClient`` 相同。 |Fess| 自行注册 ``bcryptPasswordEncoder`` 。要添加算法，请实现 ``org.codelibs.fess.crypto.password.PasswordEncoder`` ，并将该类注册到 ``fess++.xml`` 中，Lasta Di 会将它合并到 |Fess| 核心的 ``fess.xml`` 中：

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="argon2PasswordEncoder"
            class="com.example.Argon2PasswordEncoder">
        </component>
    </components>

该接口有以下方法：

.. list-table:: PasswordEncoder 的方法
   :header-rows: 1
   :widths: 35 65

   * - 方法
     - 说明
   * - ``String encode(String rawPassword)``
     - 对密码进行哈希。结果保存在由 |Fess| 添加的 ``{id}`` 前缀之后。对于无法如实哈希的密码，请抛出 ``IllegalArgumentException`` ；消息中不得包含密码。
   * - ``boolean matches(String rawPassword, String encodedPassword)``
     - 对照该编码器生成的哈希验证密码。密码错误或哈希格式不正确时，请返回 ``false`` 。
   * - ``boolean needsUpgrade(String encodedPassword)``
     - 可选（默认 ``false`` ）。返回保存的哈希是否弱于 ``encode`` 现在生成的哈希；若返回 ``true`` ，则在该用户下次登录时重新生成哈希。BCrypt 在成本低于 ``app.password.bcrypt.cost`` 时返回 ``true`` 。
   * - ``int getMaxPasswordBytes()``
     - 可选（默认 ``0`` ，表示无限制）。 ``encode`` 接受的密码的最大长度（UTF-8 字节数）。BCrypt 返回 ``72`` 。
   * - ``boolean isVerificationCostly()`` 和 ``void applyTimingPadding()``
     - 可选（默认 ``false`` 和不执行任何操作）。刻意设计得很慢的算法返回 ``true`` ，并在 ``applyTimingPadding()`` 中花费大约一次 ``matches`` 的时间。当登录在未验证任何哈希的情况下失败时（例如用户不存在）， |Fess| 会调用它，使响应时间无法暴露用户是否存在。

使用编码器的步骤如下：

#. 将 jar 放入 ``WEB-INF/plugin`` 目录。与任何 Web应用插件一样，清单中需要 ``Fess-WebAppJar: true`` （参见“pom.xml与清单文件”）；否则找不到该组件。
#. 将 ``fess_config.properties`` 中的 ``app.password.algorithm`` 设为该 ID（对于 ``argon2PasswordEncoder`` 为 ``argon2`` ）。ID 必须为小写，且不得包含 ``}`` 。此后，新设置和修改的密码都会用它进行哈希。以其他 ID 保存的密码，或没有 ID 的旧哈希，只要 ``app.password.upgrade.enabled`` 为 ``true`` （默认），就会在其用户下次成功登录时重新生成哈希。

请注意以下几点：

- 编码器是由所有线程共享的单例，因此必须是线程安全的。
- 长度限制属于编码器。设置密码时（用户管理页面、强制修改密码、 ``/api/v2/auth/password`` 和 Admin API）， |Fess| 会以“密码长度不能超过 N 个字节。”拒绝长于 ``app.password.algorithm`` 所指算法的 ``getMaxPasswordBytes()`` 的密码；为 ``0`` 或更小时，只检查 ``password.max.length`` 。验证已保存的哈希时， |Fess| 不应用任何长度限制；较长的密码是否可以匹配由 ``matches`` 决定。
- 只要仍保存着带有该 ID 的密码，就请保持插件处于安装状态。没有该组件，带有该 ID 的哈希永远无法匹配：这些用户无法登录，其哈希也不会被重新生成。
- 如果 ``app.password.algorithm`` 指定了没有组件的 ID（例如删除插件 jar 之后）， |Fess| 仍会启动，哈希带有其他 ID 的用户仍可登录，但设置密码会失败，并给出指明 ``app.password.algorithm`` 的错误。

搜索界面的自定义
================

Web应用插件无法添加 JSP 视图。这是因为 JSP 视图存放在 |Fess| 本体 WAR 的
``WEB-INF/view/`` 中，而插件 JAR 是挂载到类路径（``WEB-INF/classes``）
上的。如果需要修改搜索界面的设计，请使用主题。主题用于自定义
搜索界面的设计（HTML/CSS/JavaScript）。请参考 :doc:`theme-development`。

构建与安装
==========

::

    mvn clean package

会在 ``target/`` 目录下生成 JAR 文件（例如
``fess-webapp-example-15.10.0.jar``）。生成的 JAR 可以从管理界面安装，
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
   * - ``fess-webapp-bangs``
     - DuckDuckGo 风格的 bang（``!g``），把搜索发送到其他网站
   * - ``fess-webapp-semantic-search``
     - 神经搜索/向量搜索（已弃用；已被 15.8 中的核心集成功能取代）
   * - ``fess-webapp-multimodal``
     - 多模态（图像、文本）搜索

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`theme-development` - 主题自定义
- :doc:`../admin/plugin-guide` - 插件安装
- :doc:`overview` - 开发者文档概述
