==================================
主题开发指南
==================================

概述
====

通过 |Fess|，可以使用以下两种方法自定义搜索界面的设计。

静态主题（Static Theme）
    这是 |Fess| 15.7 中引入的机制。将主题以 ZIP 文件的形式分发，
    从管理界面上传后即可启用。主题本体是使用 ``/api/v2/*`` API 的独立 SPA
    （单页应用程序），不依赖于 |Fess| 本体的 JSP。如果要新建主题，
    推荐使用这种方法。

JAR 主题插件（旧版）
    这是一种覆盖 ``view`` / ``css`` / ``js`` / ``images`` 的传统类型插件。
    构建为 JAR 后作为插件安装。适用于希望对现有的基于 JSP 的界面进行
    部分替换的场景。

.. note::

   静态主题可在 |Fess| 15.7 及以上版本中使用。如果目标版本为 15.6 及更早版本，
   请使用 JAR 主题插件。关于从管理界面直接编辑搜索界面的 JSP、CSS、图像的方法，
   请参考 :doc:`../admin/design-guide`。

静态主题
========

静态主题是包含 ``theme.yml`` 清单文件和 ``index.html`` 的一组静态资源。
主题本体作为调用 |Fess| 的 ``/api/v2/*`` API 的前端应用程序来实现。

结构
----

静态主题采用如下目录结构。

::

    example/
    ├── theme.yml          # 清单文件(必需)
    ├── index.html         # SPA 的入口 HTML
    ├── assets/            # JavaScript、CSS 等静态资源
    │   └── styles.css
    ├── i18n/              # 多语言消息(messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # 帮助定义(<locale>.json)
    │   └── en.json
    └── thumbnail.png      # 预览图片(可选)

清单文件（theme.yml）
---------------------

``theme.yml`` 是必须放置在 ZIP 根目录下的清单文件。以下是最小配置的
示例。

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "1.0.0"
    minFessVersion: "15.7"
    entry: index.html
    spaFallback: true

可以指定的字段如下。

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - 字段
     - 必需
     - 说明
   * - ``apiVersion``
     - 必需
     - 固定值 ``fess.codelibs.org/v1``。
   * - ``kind``
     - 必需
     - 固定值 ``StaticTheme``。
   * - ``name``
     - 必需
     - 主题名称。必须匹配 ``^[a-z0-9][a-z0-9_-]{0,63}$``。
       用作展开到 ``themes/`` 下的主题目录名（上传时该名称会根据
       ``name`` 自动确定），以及分发 URL（``/themes/<name>/``）。
   * - ``displayName``
     - 必需
     - 显示在管理界面中的名称。
   * - ``version``
     - 必需
     - 语义化版本格式（例如：``1.0.0``、``1.2.3-beta.1``）。
   * - ``author``
     - 可选
     - 作者姓名。
   * - ``description``
     - 可选
     - 主题说明。
   * - ``license``
     - 可选
     - 许可证。
   * - ``homepage``
     - 可选
     - 主页 URL。
   * - ``minFessVersion``
     - 可选
     - 主题所支持的 |Fess| 最低版本。
   * - ``supportedLocales``
     - 可选
     - 支持的区域设置列表（例如：``[en, ja, de]``）。
   * - ``entry``
     - 可选
     - SPA 的入口 HTML。默认值为 ``index.html``。
   * - ``spaFallback``
     - 可选
     - 是否启用 SPA 回退。默认值为 ``true``。

.. note::

   如果从 ZIP 上传，展开目标的目录名会根据 ``name`` 自动确定。如果要在
   ``themes/`` 目录中手动放置主题，请使目录名与 ``name`` 保持一致。
   名称不一致的主题在重新扫描时会被忽略。

.. note::

   用于预览的缩略图，需以 ``thumbnail.png`` 这一固定文件名放置在主题的
   根目录下（会显示在管理界面的主题列表中）。该图片并非通过清单文件的
   字段来识别，而是通过文件名来识别。建议大小控制在 512KB 以内、
   尺寸控制在 512×512 像素以内。

分发与 API
----------

- 静态主题在 ``/themes/<name>/`` 下分发（``<name>`` 为 ``theme.yml``
  中的 ``name``）。
- 当 ``spaFallback`` 启用时，在 ``/``、``/search``、``/help``、``/error``、
  ``/profile``、``/cache``、``/chat`` 等各个路径下都会返回入口 HTML
  （默认是 ``index.html``），此后的路由由 SPA 处理。
- 管理界面（``/admin/*``）、``/api/*``、登录界面等不属于静态主题的处理
  范围，而是由 |Fess| 本体处理。
- 主题的 SPA 会通过 ``/api/v2/*`` API 获取搜索结果、聊天等数据。

打包
----

使用 `fess-themes <https://github.com/codelibs/fess-themes>`__ 仓库中的
``scripts/package.sh``，可以将主题打包成用于分发的 ZIP 文件。

::

    ./scripts/package.sh example

会生成 ``dist/example-<version>.zip``（``<version>`` 为 ``theme.yml`` 中的
``version``）。

.. note::

   ``theme.yml`` 必须放置在 ZIP 的根目录下。如果放在子目录中，
   上传时将无法被识别。

安装与启用
----------

1. 在管理界面打开"系统"→"主题"（``/admin/theme/``）。
2. 上传创建好的 ZIP 文件。
3. 在列表页面的"默认主题"下拉菜单中选择目标主题，点击"设置"按钮启用。

启用机制如下所述。

- 点击"设置"按钮后，所选的主题名称会保存到系统属性 ``theme.default``
  中，成为系统整体的默认主题。
- 如果使主题名称与虚拟主机的键一致，则仅在访问该虚拟主机时才会应用该
  主题。由此可以按虚拟主机切换主题。
- 如果直接更新了磁盘上的 ``themes/`` 目录，可以通过"重新加载"来重新
  扫描。

.. note::

   ZIP 上传存在文件大小、展开后总大小、条目数量等方面的上限，可通过
   ``fess_config.properties`` 中的 ``theme.*`` 属性进行调整（例如：
   ``theme.upload.max.size`` 默认为 50MB，``theme.directory.path`` 默认为
   ``themes``）。展开时会执行防止 ZIP Slip 和 zip bomb 的校验。

JAR 主题插件（旧版）
====================

JAR 主题插件是按主题名称覆盖 |Fess| 本体的 ``view`` / ``css`` / ``js`` /
``images`` 目录的插件。关于插件的一般结构和构建方法，也请参考
:doc:`plugin-architecture`。

结构
----

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # JSP 文件(search.jsp, index.jsp, header.jsp 等)
        ├── css/       # CSS 文件(style.css 等)
        ├── js/        # JavaScript 文件
        └── images/    # 图片文件(logo.png 等)

.. note::

   视图（模板）为 JSP 格式。资源的顶层目录仅识别 ``view`` / ``css`` /
   ``js`` / ``images`` 这 4 个。构件名称必须以 ``fess-theme-`` 开头。

pom.xml
-------

插件以 ``fess-parent`` 作为父 POM，构建为 jar。由于主题仅由资源构成，
通常不需要声明额外的依赖关系。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

CSS 与图片的自定义
------------------

搜索界面由基于 Bootstrap 的 JSP 构成。可以通过覆盖 CSS 来更改配色和
布局，或者替换 ``images/logo.png`` 来更改徽标。关于具体的类名和标记，
请查看实际的 JSP（``view/index.jsp`` / ``view/search.jsp`` 等）。

构建与安装
----------

::

    mvn clean package

会在 ``target/`` 目录下生成 JAR 文件（例如：``fess-theme-example-15.8.0.jar``）。
可以从管理界面的"系统"→"插件"进行安装。安装步骤的详细信息请参考
:doc:`../admin/plugin-guide`。

安装后，JAR 内的各个目录会按主题名称展开到以下位置（主题名称是从构件
名称中去掉 ``fess-theme-`` 后的部分。在上述示例中为 ``example``）。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - JAR 内的目录
     - 展开位置
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

启用
----

JAR 主题通过虚拟主机功能来启用。如果使虚拟主机的键与主题名称一致，
则访问该主机时会应用该主题。

1. 在"系统"→"通用"的虚拟主机设置中，按照 ``Host:localhost:8080=example``
   这样的格式，将请求的 ``Host`` 请求头与主题名称（虚拟主机的键）对应
   起来。
2. 根据需要，也在爬取的 Web 设置等虚拟主机中设置相同的名称（``example``）。

关于虚拟主机的设置方法详情，请参考 :doc:`../admin/general-guide`。

现有主题示例
============

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - 静态主题集
  （收录了 ``codesearch``、``docsearch`` 等多个静态主题）
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__ - JAR 主题
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__ - JAR 主题

参考信息
========

- :doc:`plugin-architecture` - 插件架构
- :doc:`../admin/design-guide` - 页面设计（直接编辑 JSP、CSS、图片）
- :doc:`../admin/plugin-guide` - 插件安装
