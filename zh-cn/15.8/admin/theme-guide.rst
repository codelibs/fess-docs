======
主题
======

概述
====

主题功能用于管理"静态主题"，即搜索界面外观（HTML / CSS / JavaScript 等静态资源集合）的集合。静态主题以 ZIP 压缩包的形式上传，并解压到服务器上的主题目录（默认值: ``themes`` ，可通过 ``theme.directory.path`` 更改）。每个主题的根目录下需放置描述主题元数据的 ``theme.yml`` 清单文件。

.. note::
   基于 JSP 的主题通过插件管理进行处理，不在本页的介绍范围内。
   执行本页的操作需要 ``admin-theme`` 角色（仅查看时需要 ``admin-theme-view`` 角色）。

管理方法
======

显示方法
------

要打开已注册主题的列表页面，请单击左侧菜单中的[系统 > 主题]。

主题列表
------

列表页面显示主题目录中已注册的静态主题。各行显示的项目如下所示。

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - 缩略图
     - 显示主题目录中的 ``thumbnail.png`` 。若文件不存在则不显示。
   * - 名称
     - 主题名称（主题的目录名）。单击可显示详情页面。
   * - 显示名称
     - 清单中的 ``displayName`` 。
   * - 版本
     - 清单中的 ``version`` 。
   * - 默认
     - 若已设置为默认主题，则显示勾选标记。
   * - 操作
     - 显示用于删除主题的删除按钮（默认主题不显示此按钮）。

表: 主题列表的项目


设置默认主题
----------

从列表页面上方的下拉菜单中选择主题，然后单击[设为默认]按钮，即可设置应用于搜索界面的默认主题。选择[（无默认）]并保存后，将取消默认主题的指定。设置后主题信息将重新加载并立即生效。


上传主题
----------

单击[上传]按钮将打开上传页面。选择主题 ZIP 文件后单击[上传]按钮，即可安装该主题。

* 仅支持上传 ``.zip`` 格式的压缩包。
* 压缩文件的大小上限默认为 50 MB（ ``theme.upload.max.size`` ）。
* ZIP 压缩包的根目录下必须包含 ``theme.yml`` 清单文件。

若已存在同名主题，则会被替换。被替换的原主题将作为备份保留一段时间（默认 7 天， ``theme.upload.attic.retention.days`` ）。

若上传的压缩包清单验证失败，或解压后的大小、条目数、压缩率超过服务器上限（防 zip 炸弹），则安装将被拒绝并显示错误消息。


theme.yml 清单
----------

在静态主题的根目录下放置描述主题元数据的 ``theme.yml`` （YAML 格式）。可指定的字段如下所示。

.. tabularcolumns:: |p{3cm}|p{2cm}|p{7cm}|
.. list-table::
   :header-rows: 1

   * - 字段
     - 是否必填
     - 说明
   * - ``apiVersion``
     - 必填
     - 指定 ``fess.codelibs.org/v1`` 。
   * - ``kind``
     - 必填
     - 指定 ``StaticTheme`` 。
   * - ``name``
     - 必填
     - 主题名称。必须符合 ``^[a-z0-9][a-z0-9_-]{0,63}$`` 模式，且须与主题的目录名一致。
   * - ``displayName``
     - 必填
     - 在界面上显示的名称（最多 4096 个字符）。
   * - ``version``
     - 必填
     - SemVer 格式的版本号（例如: ``1.0.0`` ）。
   * - ``author``
     - 可选
     - 作者。
   * - ``description``
     - 可选
     - 描述。
   * - ``license``
     - 可选
     - 许可证。
   * - ``homepage``
     - 可选
     - 主页 URL。
   * - ``minFessVersion``
     - 可选
     - 支持的最低 |Fess| 版本。
   * - ``supportedLocales``
     - 可选
     - 支持的区域设置。
   * - ``entry``
     - 可选
     - 入口点文件（默认值: ``index.html`` ）。
   * - ``spaFallback``
     - 可选
     - 是否启用 SPA 模式的回退（默认值: ``true`` ）。

表: theme.yml 的字段


删除主题
------

可通过列表页面的删除按钮或详情页面的[删除]按钮删除主题。已设置为默认主题的主题无法删除，请在删除前先取消默认主题的指定。被删除的主题将作为备份保留一段时间（默认 7 天， ``theme.upload.attic.retention.days`` ）。


重新加载
------

当直接在服务器上编辑主题目录等情况时，单击[重新加载]按钮，可将磁盘上的主题信息重新加载到内存中。


主题详情
------

在列表页面中单击主题名称，将显示详情页面。在详情页面中，可查看清单的内容（名称、显示名称、版本、是否为默认、状态）。


配置属性
======

与主题功能相关的主要配置可在 ``fess_config.properties`` 中修改。

.. tabularcolumns:: |p{6cm}|p{3cm}|p{5cm}|
.. list-table::
   :header-rows: 1

   * - 属性
     - 默认值
     - 说明
   * - ``theme.directory.path``
     - ``themes``
     - 存储主题的目录（相对于 Servlet 上下文的相对路径，或绝对路径）。
   * - ``theme.upload.max.size``
     - ``52428800``
     - 可上传 ZIP 的最大大小（字节，约 50 MB）。
   * - ``theme.upload.max.extracted.size``
     - ``209715200``
     - 解压后的最大总大小（字节，约 200 MB）。
   * - ``theme.upload.max.entries``
     - ``1000``
     - ZIP 中可包含的最大条目数。
   * - ``theme.upload.max.compression.ratio``
     - ``100``
     - 单个条目的最大压缩率。
   * - ``theme.upload.zip.ratio.max``
     - ``50``
     - 累计压缩率上限（防 zip 炸弹）。
   * - ``theme.upload.zip.ratio.check.threshold.bytes``
     - ``65536``
     - 开始评估累计压缩率的压缩字节数。
   * - ``theme.upload.attic.retention.days``
     - ``7``
     - 保留已替换或已删除主题备份的天数。

表: 主题功能的配置属性
