==============================
为现有网站嵌入搜索框和搜索页面
==============================

前言
====

想为企业内部门户或产品网站添加搜索功能时，让用户记住 Fess 的 URL 并不现实。
人们期望的是：在平时常用页面的页眉中有一个搜索框，搜索结果页面看起来也像是该网站的一部分。

本文使用 Fess 15.9，依次尝试以下 3 种只需在浏览器端即可完成的方法。

- 在现有页面中放置 HTML 搜索表单，在 Fess 的搜索页面中显示结果
- 使用 Fess Site Search（FSS），在现有网站的页面中显示搜索结果
- 修改 Fess 搜索页面（主题）的外观，使其与现有网站一致

同时，还将设置“路径映射”，把搜索结果的链接目标改为用户可以访问的 URL。

从业务系统的服务器调用搜索 API 来构建自有页面的方法，将在 :doc:`guide-11` 中介绍。

前提条件
========

- 已按照 :doc:`guide-02` 的步骤，使 Docker Compose 的 Fess 15.9 在 ``http://localhost:8080/`` 上运行，并且已爬取过至少一项内容
- 一个本地 HTML 文件，用来代替现有网站

现有网站通常与 Fess 处于不同的源（协议、主机、端口的组合）。
为了在本文中也形成同样的条件，请在放置 HTML 文件的目录中执行以下命令，然后通过 ``http://localhost:8000/`` 打开。

::

    $ python3 -m http.server 8000

如何选择方法
============

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - 方法
     - 显示搜索结果的位置
     - Fess 端需要的内容
   * - 搜索表单
     - 跳转到 Fess 的搜索页面（``/search``）显示
     - 无
   * - Fess Site Search
     - 现有网站的页面中
     - 插件 ``fess-webapp-v1-api``
   * - 修改主题
     - Fess 的搜索页面（改变外观）
     - 主题的 ZIP（或 [通用] 中的设置）

搜索表单和修改主题可以组合使用。
如果希望从现有网站跳转后的页面也具有相同的外观，请同时设置两者。

放置搜索表单并发送到 Fess 的搜索页面
====================================

放置表单
--------

在现有页面中想要放置搜索框的位置，编写以下表单。

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">搜索</button>
    </form>

搜索词作为 ``q`` 参数发送到 Fess 的 ``/search``，结果显示在 Fess 的搜索页面中。
``maxlength`` 与 Fess 端搜索词长度的上限 ``query.max.length``\ （默认值 ``1000``）保持一致。
在生产环境中，请将 ``action`` 的 URL 改为用户访问的 Fess URL。

如果只想让用户搜索带有特定标签的文档，请将标签的值作为 ``fields.label`` 一并发送。

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">搜索</button>
    </form>

``intranet`` 是在 [爬虫] > [标签] 中创建的标签的值。
如果发送不存在的值，结果将为 0 条。
标签的创建方法请参见 :doc:`guide-04`。

确认
----

1. 从 ``http://localhost:8000/`` 打开 HTML 文件，用已爬取文档中包含的词进行搜索
2. 如果浏览器跳转到 ``http://localhost:8080/search?q=...``，并在 Fess 的搜索页面中显示结果，即表示完成

如果结果为 0 条，请在 ``http://localhost:8080/`` 的搜索框中搜索同一个词进行比较。
如果那里也是 0 条，那么问题不在表单，而在于爬取或权限。

关于搜索建议
------------

`搜索表单集成 <https://fess.codelibs.org/zh-cn/stable/config/search-form-integration.html>`__ 页面中有一个为表单添加搜索建议的示例。
但是，该示例加载的 ``/js/suggestor.js`` 和 ``/js/jquery-3.7.1.min.js`` 并未包含在 15.9 的 Fess 中，因此在 15.9 中，该示例无法直接运行。
表单部分（将 ``q`` 发送到 ``/search``）可以直接使用。

如果想在现有网站的搜索框中显示搜索建议，请使用以下任一方法。

- 在下一节的 Fess Site Search 中启用搜索建议
- 从自己的脚本中调用 ``/api/v2/suggest-words``\ （API 的用法请参见 :doc:`guide-11`）

跳转到 Fess 的搜索页面之后，由 Fess 自带的主题显示搜索建议。

使用 Fess Site Search 在页面中显示结果
======================================

Fess Site Search（FSS）是一个在现有网站的页面中显示搜索表单和搜索结果的 JavaScript。
用户无需离开现有网站即可进行搜索。

FSS 的 JavaScript 并不由 Fess 提供。
请下载用 FSS JS Generator（https://fss-generator.codelibs.org/）生成的文件，并放置到现有网站的服务器上。

安装 v1 API 插件
----------------

FSS 调用 Fess 的 ``/api/v1``。
15.9 的 Fess 本体只提供 ``/api/v2``，``/api/v1`` 由插件 ``fess-webapp-v1-api`` 提供。
该插件未包含在 Docker 镜像中。

使用 Docker Compose 时，在 ``compose.yaml`` 中 ``fess01`` 的 ``environment`` 里添加以下一行。

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

如果已经指定了其他插件，请在同一个值中用空格分隔并列出。
保存后，指定 2 个 Compose 文件执行 ``up -d``。
``fess01`` 会被重新创建，并在启动时安装插件。
由于容器会被重新创建，在 [系统] > [通用] 中修改的设置会与执行 ``down`` 时一样恢复原状（参见 :doc:`guide-02` 中关于停止与重启的一节）。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

也可以在管理页面的 [系统] > [插件] > [安装] 中安装（安装后需要重启 Fess）。
但是在 Docker 中，插件放置在容器内，因此用 ``down`` 重新创建容器后插件就会消失。
如果在 ``FESS_PLUGINS`` 中指定，每次重新创建时都会重新安装。

``fess01`` 变为 healthy 后，确认 API 是否有响应。

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

如果返回包含 ``"record_count"`` 的 JSON，即表示准备就绪。
如果返回 404，说明插件没有安装。
此时，``fess.log`` 中会输出一次以 ``No plugin serves the legacy API`` 开头的 WARN。
如果插件已安装却不返回 JSON，请检查 [系统] > [通用] 中的「JSON响应」是否被关闭。
关闭「JSON响应」后，不仅 ``/api/v1``，``/api/v2`` 也不再响应，Fess 自身的搜索页面也将无法使用。

生成并放置 JavaScript
---------------------

1. 打开 https://fss-generator.codelibs.org/，在生成器中指定配色、字体等，然后点击 [Generate]
2. 用 [Download JS] 下载 JavaScript 文件
3. 将文件名改为 ``fess-ss.js``，并放到与 HTML 文件相同的目录中

在显示搜索结果的页面（例如 ``result.html``）中，编写以下代码。

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="zh"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="zh"
      ></fess-search-result>
    </div>

``fess-url`` 是用于搜索的 Fess URL，``suggest-url`` 是用于搜索建议的 Fess URL。
在生产环境中，请设为用户的浏览器可以访问的 Fess URL。

在其他页面的页眉中，只放置搜索表单。

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

表单将搜索词放入 ``fss.query`` 参数并跳转到 ``result.html``，由 ``result.html`` 中的 FSS 执行搜索。
从不加载 FSS 的页面发送时，只要编写一个以 ``result.html?fss.query=搜索词`` 的形式跳转的表单，也能同样工作。

其他属性（每页条数 ``:page-size``、按标签筛选 ``:enable-label``、在新标签页中打开链接 ``link-target="_blank"`` 等）请参阅 FSS JS Generator 的手册。

确认
----

1. 打开 ``http://localhost:8000/result.html``，用搜索表单进行搜索
2. 如果页面中显示了搜索结果，即表示完成
3. 如果没有显示，请在浏览器开发者工具的网络标签页中检查对 ``/api/v1/documents`` 的请求。如果是 404，请检查插件；如果是 CORS 错误，请检查下一项

注意事项
--------

从浏览器的角度看，从 ``localhost:8000`` 的页面调用 ``localhost:8080`` 的 API 属于跨源通信。
Fess 在默认设置中为 ``api.cors.allow.origin=*``，接受来自任何源的调用。
如果想将调用方限制为现有网站，相关设置将在 :doc:`guide-11` 中介绍。

FSS 从其他源发出的搜索，即使用户已登录 Fess，也会被视为未登录用户（访客）的搜索。
这是因为 FSS 在调用 API 时不附带 Cookie，而且在默认的 ``api.cors.allow.origin=*`` 下，附带凭据的跨源通信也不被允许。
因此，结果中只会出现权限中含有 ``{role}guest`` 的文档。
如果要按部门显示不同的文档，请让用户在 Fess 的搜索页面中登录（参见 :doc:`guide-05`）。

修改 Fess 搜索页面的外观
========================

15.9 的搜索页面由打包了 HTML、CSS 和 JavaScript 的“主题”来显示。
以前版本中的 [页面设计] 和 JSP 编辑已不复存在。
如果没有进行任何设置，将使用自带的主题 ``bootstrap``。

无需制作 ZIP 即可修改的内容
---------------------------

在 [系统] > [通用] 的「显示通知」中的「搜索首页」里填写的内容，会显示在自带主题的搜索首页和搜索结果页面上。
也可以填写 HTML，但 ``<script>`` 和 ``<style>`` 等会被移除。
如果只是想显示一行面向内部的通知，就不需要制作主题。

使用已发布的主题
----------------

Fess 项目发布了面向文档搜索的 ``docsearch`` 等主题。

1. 打开 [系统] > [主题]
2. 在「安装主题」的「名称」中选择主题，然后点击 [选择]
3. 在「版本」中选择适用于 15.9 的版本（``15.9.x``），然后点击 [安装]
4. 在列表上方的「默认主题」中选择已安装的主题，然后点击 [设置]

重新打开 ``http://localhost:8080/``，页面就会以新主题显示。
选择「（无默认）」并点击 [设置]，即可恢复为自带的 ``bootstrap``。

复制自带主题并修改徽标和配色
----------------------------

自带主题不能直接编辑，也不能通过上传同名的 ``bootstrap`` 主题来替换。
请以其他名称复制后再进行修改。
这里使用 ``mytheme``。

1. 从容器中取出自带主题

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. 将 ``mytheme/theme.yml`` 中的 ``name`` 改为 ``mytheme``，将 ``displayName`` 改为 ``My Theme`` 等
3. 修改以下文件

   - 配色和布局：``assets/styles.css``
   - 徽标：``assets/logo-head.png``\ （页眉）和 ``assets/logo.png``\ （搜索首页）
   - 页脚中的组织名称：``i18n/messages.zh-CN.json`` 中的 ``footer.copyright_org``\ （英文界面为 ``messages.en.json``）

4. 打包时使 ``theme.yml`` 位于 ZIP 的根目录

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. 在 [系统] > [主题] 中通过 [上传] 上传 ``mytheme.zip``
6. 在「默认主题」中选择 ``mytheme``，然后点击 [设置]

不要修改 ``index.html``。
自带的 ``index.html`` 以 ``{{themePath}}/assets/...`` 的形式引用主题内的文件。
Fess 在提供页面时会将 ``{{themePath}}`` 替换为 ``themes/mytheme``，因此只需修改名称，就会加载复制后主题中的文件。

确认
----

重新打开 ``http://localhost:8080/``，确认徽标和配色已经改变。
如果没有改变，请在开发者工具的网络标签页中查看样式表是否从 ``/themes/mytheme/assets/styles.css`` 加载。
如果是从 ``/themes/bootstrap/`` 加载的，说明默认主题的设置没有生效。

主题的注意事项
--------------

- 搜索页面会附带 ``Content-Security-Policy`` 标头，将脚本、样式和图像的来源限制为 Fess 自身。外部 CDN 的字体和脚本不会被加载，请将它们放入主题的 ZIP 中
- 搜索页面不会显示在其他页面的 ``iframe`` 中（因为 ``theme.index.frame.ancestors`` 的默认值为 ``'none'``）。如果想在门户中显示搜索结果，请使用 FSS
- Docker 的 ``fess01`` 没有卷。上传的主题放在容器内，默认主题的设置保存在 ``system.properties`` 中，因此用 ``down`` 重新创建容器后两者都会消失。平时请使用 ``stop``/``start``，重新创建容器后请重新上传并设置
- 自带主题是针对同版本 Fess 的 ``/api/v2`` 制作的。升级 Fess 后，请从新的自带主题重新复制，并重新应用修改

主题的结构和 ``theme.yml`` 的各项内容，请参见\ `主题开发指南 <https://fess.codelibs.org/zh-cn/stable/dev/theme-development.html>`__。

将搜索结果的链接目标改为面向用户的 URL
======================================

有时希望爬取时使用内部主机名，而让用户通过门户的 URL 打开文档。
例如，爬取 ``http://intranet-web01:8080/docs/``，而在搜索结果中打开 ``https://portal.example.com/docs/``。
这时，可以使用路径映射，仅在显示时替换 URL。

1. 打开 [爬虫] > [路径映射]，点击 [新建]
2. 按如下内容输入，然后点击 [创建]

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - 项目
        - 值
      * - 正则表达式
        - ``^http://intranet-web01:8080/docs/``
      * - 替换
        - ``https://portal.example.com/docs/``
      * - 处理类型
        - 显示
      * - 排序顺序
        - ``0``

「显示」只替换搜索结果中显示的 URL 和链接目标。
索引中保存的 URL 不会改变，因此无需重新爬取，保存后即可反映到搜索结果中。
如果选择「爬网」或「爬网/显示」，替换后的 URL 会保存到索引中。
请注意，如果只想修改显示却选择了这些选项，之后爬取的 URL 也会随之改变。

确认时，请用能搜到目标文档的词进行搜索，查看结果中的 URL 和链接目标是否为 ``https://portal.example.com/docs/...``。
通过 API 获取结果时，替换后的 URL 位于 ``url_link`` 而不是 ``url`` 中（参见 :doc:`guide-11`）。

将文件服务器的路径转换为 Web 服务器 URL 的示例，请参见\ `路径映射 <https://fess.codelibs.org/zh-cn/stable/admin/pathmap-guide.html>`__。

接下来阅读的文章
================

- 想从业务系统的服务器调用搜索 API：:doc:`guide-11`
- 想按部门改变门户中显示的文档：:doc:`guide-05`
- 想统一搜索网站和文件服务器，并用标签加以区分：:doc:`guide-04`
- 想为每个组织显示不同的主题或搜索对象：:doc:`guide-13`
- 想要求登录后才能使用搜索页面：:doc:`guide-15`

参考资料
========

- `搜索表单集成 <https://fess.codelibs.org/zh-cn/stable/config/search-form-integration.html>`__
- `主题 <https://fess.codelibs.org/zh-cn/stable/admin/theme-guide.html>`__
- `主题开发指南 <https://fess.codelibs.org/zh-cn/stable/dev/theme-development.html>`__
- `路径映射 <https://fess.codelibs.org/zh-cn/stable/admin/pathmap-guide.html>`__
- `插件 <https://fess.codelibs.org/zh-cn/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search（GitHub） <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api（GitHub） <https://github.com/codelibs/fess-webapp-v1-api>`__
