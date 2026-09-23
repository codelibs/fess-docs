==================================
主题开发指南
==================================

概述
====

在 |Fess| 15.9 中，搜索界面始终是静态主题。静态主题是使用
``/api/v2/*`` API 的独立 SPA（单页应用程序）。主题以 ZIP 文件的形式
分发，从管理界面上传后在管理界面中启用。未选择任何主题时， |Fess|
使用其内置的静态主题 ``bootstrap`` 。

要更改搜索界面的外观，可以安装其他主题（参见 :doc:`../admin/theme-guide` ），
也可以自行制作：最快捷的方法是复制内置主题并修改副本，具体步骤参见
`自定义内置主题`_ 。

.. note::

   静态主题可在 |Fess| 15.7 及以上版本中使用，并在 15.9 中成为默认的
   搜索界面。替换搜索界面 JSP 的 JAR 主题插件在 15.9 中不再改变搜索界面；
   参见 `JAR 主题插件（旧版）`_ 。

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
    version: "15.9.0"
    minFessVersion: "15.9"
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
     - 固定值 ``fess.codelibs.org/v1``\ 。
   * - ``kind``
     - 必需
     - 固定值 ``StaticTheme``\ 。
   * - ``name``
     - 必需
     - 主题名称。必须匹配 ``^[a-z0-9][a-z0-9_-]{0,63}$``\ 。
       用作展开到 ``themes/`` 下的主题目录名（上传时该名称会根据
       ``name`` 自动确定），以及分发 URL（``/themes/<name>/``）。
   * - ``displayName``
     - 必需
     - 显示在管理界面中的名称。
   * - ``version``
     - 必需
     - 语义化版本格式（例如：``15.9.0``、``15.9.1-beta.1``）。按惯例
       ``major.minor`` 与主题面向的 |Fess| 系列一致，这样仅凭版本就能知道
       该主题是为哪个 |Fess| 准备的。
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
     - 主题所支持的 |Fess| 最低版本。请与 ``version`` 的 ``major.minor``
       保持一致。没有 ``maxFessVersion``\ ，参见 `发布`_\ 。
   * - ``supportedLocales``
     - 可选
     - 支持的区域设置列表（例如：``[en, ja, de]``）。
   * - ``entry``
     - 可选
     - SPA 的入口 HTML。默认值为 ``index.html``\ 。
   * - ``spaFallback``
     - 可选
     - 已弃用。为保持兼容仍可指定，但不再读取：自 15.9 起，搜索界面的
       路径始终返回入口 HTML。

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
- 在 ``/``、``/search``、``/advance``、``/help``、``/error``、
  ``/profile``、``/cache``、``/chat`` 各个路径下都会返回入口 HTML
  （默认是 ``index.html``），此后的路由由 SPA 处理。自 15.9 起，无论
  ``spaFallback`` 如何设置都会这样处理；该字段不再被读取。
- 错误也由主题渲染：请求失败时，浏览器会在所请求的 URL 上收到主题的
  入口 HTML，并附带真实的 HTTP 状态码。
- 管理界面（``/admin/*``）、``/api/*``、登录界面等不属于静态主题的处理
  范围，而是由 |Fess| 本体处理。
- 入口 HTML 在返回时附带 ``Content-Security-Policy`` 头，仅允许来自
  |Fess| 自身的脚本、样式、图片和连接（允许内联样式，不允许内联脚本）。
  因此，来自外部 CDN 的字体或脚本不会被加载；请将它们包含在主题中。
- 主题的 SPA 会通过 ``/api/v2/*`` API 获取搜索结果、聊天等数据。

打包
----

使用 `fess-themes <https://github.com/codelibs/fess-themes>`__ 仓库中的
``scripts/package.sh``，可以将主题打包成用于分发的 ZIP 文件。

::

    ./scripts/package.sh example

会生成 ``dist/example-<version>.zip``\ （``<version>`` 为 ``theme.yml`` 中的
``version``）。

.. note::

   ``theme.yml`` 必须放置在 ZIP 的根目录下。如果放在子目录中，
   上传时将无法被识别。

发布
----

|Fess| 项目开发的主题公开在 https://maven.codelibs.org/release/org/codelibs/fess/themes/ 之下，路径为 ``<name>/<version>/<name>-<version>.zip``\ ，旁边是 ``.sha1``\ ，每个主题还有一份列出已公开版本的 ``maven-metadata.xml``\ 。 ``bin/fess-setup install theme <name>`` 会读取该元数据，挑选为正在运行的 |Fess| 构建的版本。

请让主题的版本与其面向的 |Fess| 系列一致，并在归档内容发生变化时提升版本。已公开的版本不会被覆盖，因此保持版本不变的修改根本不会被分发。

清单中没有上限字段也是同样的原因。公开的归档不会再改变，因此无法事后为在更新的 |Fess| 上不再可用的主题补加上限；不为该系列发布，就在知道的那一刻表达了同样的意思。

.. note::

   查询已公开的版本时，请使用 ``maven-metadata.xml`` 而不是目录列表。目录索引是定期生成的，新公开的主题在出现在列表中之前就已经可以通过元数据读取。

安装与启用
----------

1. 在管理界面打开"系统"→"主题"（``/admin/theme/``）。
2. 上传创建好的 ZIP 文件。已公开的主题也可以在命令行用
   ``bin/fess-setup install theme <name>`` 安装，参见
   :doc:`../install/fess-setup`\\ 。
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

.. _theme-customize-bundled:

自定义内置主题
--------------

内置主题 ``bootstrap`` 位于 |Fess| 安装目录的 ``app/themes/bootstrap/``
（RPM/DEB 软件包为 ``/usr/share/fess/app/themes/bootstrap/`` ）。请不要
直接编辑它：升级时它会被替换，而且 ``bootstrap`` 这一名称为其保留，
既无法删除，也无法通过上传替换。请以新名称复制后再修改。

1. 复制该目录，例如复制为 ``mytheme`` ::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. 在 ``theme.yml`` 中，将 ``name`` 改为 ``mytheme`` ，并修改
   ``displayName`` 。 ``name`` 必须与目录名一致。

3. 在 ``index.html`` 中，将所有 ``themes/bootstrap/`` 替换为
   ``themes/mytheme/`` 。内置的 ``index.html`` 在四处引用了自身的目录：
   样式表（ ``assets/styles.css`` ）、两个徽标（ ``assets/logo-head.png``
   和 ``assets/logo.png`` ）以及脚本（ ``assets/app.js`` ）。如果不修改，
   副本将继续加载 ``bootstrap`` 的文件，对 CSS、徽标或消息所做的修改都
   不会显示。其他文件是相对于 ``assets/app.js`` 加载的，因此只需修改这
   四处。

   ::

       $ sed -i 's#themes/bootstrap/#themes/mytheme/#g' /tmp/mytheme/index.html

4. 进行修改：

   - 配色和布局： ``assets/styles.css`` 。
   - 徽标： ``assets/logo-head.png`` （页眉）和 ``assets/logo.png``
     （搜索首页）。
   - 页脚（ ``footer.copyright_org`` ）等文本：每种语言一个的
     ``i18n/messages.<locale>.json`` 文件。
   - 页面结构： ``index.html`` 。

5. 将该目录打包为根目录下包含 ``theme.yml`` 的 ZIP，并在管理界面的
   "系统"→"主题"中上传::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   也可以将该目录放到 ``app/themes/`` 中，然后在同一页面点击"重新加载"。

6. 在该页面将 ``mytheme`` 选为默认主题。

.. note::

   由于内置主题遵循其所属 |Fess| 版本的 ``/api/v2/*`` API，每次升级
   |Fess| 后，请用内置主题的新副本替换原副本，并重新应用您的修改。

JAR 主题插件（旧版）
====================

.. warning::

   自 |Fess| 15.9 起，搜索界面始终由静态主题提供，因此 JAR 主题插件不再
   改变搜索界面。JAR 主题提供的 JSP 中，只有登录界面（ ``/login/`` ）的
   JSP 仍会被使用。请将设计迁移到静态主题；参见 `自定义内置主题`_ 。

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
        <version>15.9.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.9.0</version>
            <relativePath />
        </parent>
    </project>

CSS 与图片的自定义
------------------

JSP 基于 Bootstrap 构建。可以通过覆盖 CSS 来更改配色和布局，或者替换
``images/logo.png`` 来更改徽标。自 15.9 起，这只影响登录界面；搜索界面
是静态主题（参见 `自定义内置主题`_ ）。

构建与安装
----------

::

    mvn clean package

会在 ``target/`` 目录下生成 JAR 文件（例如：``fess-theme-example-15.9.0.jar``）。
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
- :doc:`../admin/plugin-guide` - 插件安装
