=======================
SharePoint Server连接器
=======================

概述
====

SharePoint Server连接器提供从本地部署的 **SharePoint Server** （2013、2016、2019 或 Subscription
Edition）通过其 REST/OData API（2013 版本还包括 XML/Atom API）获取文档库文件和列表项，并注册到
|Fess| 索引的功能。

此功能需要 ``fess-ds-sharepoint`` 插件。

.. note::

   如果需要爬取 SharePoint Online（Microsoft 365），请使用 :doc:`ds-microsoft365`，而不是本连接器。
   本连接器的 OAuth 支持仅针对 Azure ACS 应用程序专用认证，不具备 Microsoft Graph API 集成功能。

支持的版本: SharePoint Server 2013 / 2016 / 2019 / Subscription Edition (SE)

支持的内容
==========

- 文档库文件
- 列表项
- 列表项附件

前提条件
========

1. 需要安装插件
2. 用于爬取的账户需要拥有对目标站点、列表和文档库的读取权限
3. 从 NTLM、Kerberos（SPNEGO）、OAuth（ACS）中选择且只能选择一种认证方式，并准备好相应的凭据

插件安装
--------

从管理界面的「系统」→「插件」进行安装:

1. 下载 ``fess-ds-sharepoint-X.X.X.jar``
2. 将其放置到 ``$FESS_HOME/app/WEB-INF/lib`` （或 ``/usr/share/fess/app/WEB-INF/lib`` ）下
3. 重启 |Fess|

详情请参阅 :doc:`../../admin/plugin-guide`。

配置方法
========

从管理界面的「爬虫」→「数据存储」→「新建」配置本连接器。

基本设置
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 项目
     - 设置示例
   * - 名称
     - SharePoint
   * - 处理器名称
     - SharePointDataStore
   * - 启用
     - 开

参数设置
--------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

参数列表
~~~~~~~~

**URL / 站点**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``url``
     - 是
     - SharePoint 服务器的基础 URL，例如 ``http://sharepoint.example.com/``
   * - ``site.name``
     - 有条件
     - 在 ``/sites/<site.name>/`` 下爬取的站点集合名称。设置了 ``site.path`` 时则不需要
   * - ``site.path``
     - 否
     - 站点的服务器相对托管路径（例如 ``/teams/eng``；根站点集合使用 ``/``）。设置后将按原样
       使用该值代替硬编码的 ``/sites/`` 前缀，此时不再需要 ``site.name``
   * - ``site.list_id``
     - 否
     - 通过 GUID 指定单个列表进行爬取（列表爬取模式）
   * - ``site.list_name``
     - 否
     - 通过显示名称指定单个列表进行爬取（列表爬取模式）
   * - ``site.doclib_path``
     - 否
     - 站点下的文档库路径（文档库爬取模式），例如 ``/Shared Documents``
   * - ``site.exclude_list``
     - 否
     - 要排除的列表实体类型名称的正则表达式（逗号分隔）。仅在整站爬取时生效
   * - ``site.exclude_folder``
     - 否
     - 要排除的顶级文件夹名称的正则表达式（逗号分隔）。仅在整站爬取时生效
   * - ``site.crawl_subsites``
     - 否
     - 是否递归爬取站点的子站点（默认: ``false``）。详见 `子站点和托管路径`_
   * - ``site.max_depth``
     - 否
     - ``site.crawl_subsites`` 可递归的子站点层数（默认: ``10``）；根站点的深度为 0

**认证**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``auth.ntlm.user``
     - 否
     - NTLM 用户名。设置后即启用 NTLM 认证（可使用 ``DOMAIN\user`` 形式）
   * - ``auth.ntlm.password``
     - 否
     - NTLM 密码
   * - ``auth.ntlm.domain``
     - 否
     - Windows 域，作为独立的 NTLM 字段发送
   * - ``auth.ntlm.workstation``
     - 否
     - NTLM 协商过程中发送的工作站名称
   * - ``auth.kerberos.principal``
     - 否
     - 客户端主体，格式为 ``user@REALM``。设置后即启用 Kerberos/SPNEGO 认证
   * - ``auth.kerberos.keytab``
     - 否
     - 保存该主体密钥的 keytab 文件路径。与 ``auth.kerberos.password`` 互斥
   * - ``auth.kerberos.password``
     - 否
     - 该主体的密码，仅在未设置 keytab 时使用
   * - ``auth.kerberos.strip_port``
     - 否
     - 是否从服务主体名称中去除端口号（默认: ``true``）
   * - ``auth.kerberos.use_canonical_hostname``
     - 否
     - 在构建服务主体名称之前，是否将目标主机解析为其规范名称（默认: ``false``）
   * - ``auth.kerberos.krb5_conf``
     - 否
     - ``krb5.conf`` 文件的路径。仅在尚未设置 ``java.security.krb5.conf`` 时应用
   * - ``auth.kerberos.debug``
     - 否
     - 是否启用 ``Krb5LoginModule`` 的调试输出（默认: ``false``）
   * - ``auth.oauth.client_id``
     - 否
     - Azure ACS 应用程序专用 OAuth 客户端 ID。设置后即启用 OAuth 认证
   * - ``auth.oauth.client_secret``
     - 否
     - OAuth 客户端密钥
   * - ``auth.oauth.tenant``
     - 否
     - 租户名称（不含 ``.sharepoint.com``）
   * - ``auth.oauth.realm``
     - 否
     - Azure AD 领域（目录 ID）

``auth.kerberos.principal`` 、``auth.ntlm.user`` 、``auth.oauth.client_id`` 三者中 **只能设置一个**。详见下文的 `认证`_ 一节。

**列表**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``list.items.number_per_page``
     - 否
     - ``GetListItems`` 的分页大小（默认: ``100``）
   * - ``list.item.content.include_fields``
     - 否
     - 字段名列表（逗号分隔）；设置后，仅将这些列表项字段拼接到 ``content`` 中
   * - ``list.item.content.exclude_fields``
     - 否
     - 字段名模式（逗号分隔，每个元素作为正则表达式处理），在内置的大量标准字段之外，从
       ``content`` 中额外排除的字段
   * - ``list.is_sub_page``
     - 否
     - 是否将列表项视为 SitePages/wiki 子页面，这会影响分页回退方式和 Web 链接的形式
       （默认: ``false``）

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``http.connection_timeout``
     - 否
     - HTTP 连接超时时间（毫秒）；同时也用作连接池等待超时时间（默认: ``30000``）
   * - ``http.socket_timeout``
     - 否
     - HTTP 套接字（读取）超时时间（毫秒，默认: ``30000``）
   * - ``proxy_host``
     - 否
     - HTTP 代理主机
   * - ``proxy_port``
     - 有条件
     - HTTP 代理端口；设置了 ``proxy_host`` 时必需（默认: ``-1`` = 不使用代理）

**筛选与内容**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``include_pattern``
     - 否
     - 项目的值必须匹配该正则表达式才会被爬取。该值具体指什么，参见本表下方的说明
   * - ``exclude_pattern``
     - 否
     - 匹配该正则表达式的项目将被排除，不会被爬取
   * - ``supported_mimetypes``
     - 否
     - 文件的 MIME 类型必须至少匹配其中一个的正则表达式（逗号分隔，默认: ``.*``）
   * - ``max_content_length``
     - 否
     - 文件的最大大小（字节）；超出限制的文件会被跳过而非判定为失败（默认: ``-1`` = 无限制）
   * - ``extractor_name``
     - 否
     - 仅当提取器工厂无法映射某 MIME 类型时使用的备用提取器（默认: ``tikaExtractor``）

**行为**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 参数
     - 必需
     - 说明
   * - ``sp.version``
     - 否
     - 设置为 ``2013`` 可切换到面向 SharePoint 2013 的 XML/Atom、``GetXxxByServerRelativeUrl``
       系列 API（未设置时使用 SharePoint Online / 2016 以后版本的 REST 方言）
   * - ``retry_limit``
     - 否
     - 出现 SharePoint 服务器/客户端异常时，每个爬取单元的最大重试次数（默认: ``2``）
   * - ``role.skip``
     - 否
     - 是否完全跳过逐项权限的获取（默认: ``false``）。详见 `权限`_
   * - ``ignore_error``
     - 否
     - 文件内容提取失败时，是否记录日志并跳过，而不是使该爬取目标失败（默认: ``false``）
   * - ``default_permissions``
     - 否
     - 权限字符串（逗号分隔），会在 SharePoint 返回的权限之外，合并到每个文档的角色列表中
   * - ``delete_old_docs``
     - 否
     - 本次运行中未被重新获取的文档是否会被删除（核心默认值: ``true``）。只要本次运行中有
       任意爬取目标失败，本插件就会将该值强制设为 ``false``
   * - ``number_of_threads``
     - 否
     - 同时处理的爬取目标数量（默认: ``1`` = 不使用线程池），上限为处理器核心数的两倍。
       详见 `并行爬取与负载`_
   * - ``script_type``
     - 否
     - 数据设置中脚本所使用的脚本引擎（默认: ``groovy``）
   * - ``readInterval``
     - 否
     - 连续爬取结果之间的等待时间（毫秒，默认: ``0``）。请注意，与本表中其他参数不同，
       该参数使用驼峰命名

脚本设置
--------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

可用字段
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - 键
     - 列表项（ItemCrawl）
     - 文档库文件（FolderCrawl→FileCrawl）
     - 附件（ItemAttachmentsCrawl→FileCrawl）
   * - ``url``
     - Web 链接
     - 文件 URL
     - 文件 URL
   * - ``host``
     - 主机名
     - 主机名
     - 主机名
   * - ``site``
     - 服务器相对路径（``FileRef``）
     - 服务器相对路径
     - 服务器相对路径
   * - ``title``
     - ``Title`` 字段，否则为 ``FileLeafRef``/文件名
     - 文档库文件自身的 ``Title`` 列表值（如果存在），否则为文件名
     - 文件名
   * - ``titleWithListName``
     - ``"[listName] title"``
     - ``"[listName] filename"`` （文档库爬取时列表名始终为空，因此实际上只是文件名）
     - ``"[listName] filename"``
   * - ``listName``
     - 列表显示名称，或 ``""``
     - 始终为 ``""``
     - 实际的列表名称
   * - ``content``
     - 字段值的拼接
     - 提取的文本
     - 提取的文本
   * - ``digest``
     - ``content`` 的摘要
     - ``content`` 的摘要
     - ``content`` 的摘要
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - 来自列表获取结果
     - 来自列表获取结果
     - 来自列表获取结果
   * - ``created``
     - 来自列表获取结果
     - 来自列表获取结果
     - 来自列表获取结果
   * - ``mimetype``
     - 始终为 ``text/html``
     - 检测得出
     - 检测得出
   * - ``filetype``
     - 由 ``mimetype`` 派生
     - 由 ``mimetype`` 派生
     - 由 ``mimetype`` 派生
   * - ``role``
     - 权限列表，仅在非空时设置
     - 权限列表，仅在非空时设置
     - 权限列表，仅在非空时设置
   * - ``list_name``
     - 有
     - **无**
     - 有
   * - ``list_id``
     - 有
     - **无**
     - 有
   * - ``item_id``
     - 有
     - **无**
     - 有

.. note::

   ``content_length`` 是 ``content.length()``，即提取或拼接后文本的字符数（UTF-16 代码单元数），
   并非文件的字节大小。这与 Box、Google Drive、Dropbox 连接器中 ``file.size`` 的含义不同 ——
   后者是各服务自身文件元数据中的实际字节大小。请勿将本连接器的 ``content_length``
   与它们进行比较。

**动态键: ``val_*``**

列表项 ``FieldValuesAsText`` （SharePoint 针对该项目返回的原始字段值映射，包括
``odata.metadata`` 等 OData 元数据键）中的每个键都会以两种名称公开：一种不带前缀
（仅当该名称尚未是上述固定键之一时才会公开），另一种始终带有 ``val_`` 前缀 ——
例如 ``Status`` 字段会同时以 ``Status`` 和 ``val_Status`` 两种形式出现。

``val_*`` 键仅存在于 **列表项爬取路径（ItemCrawl）** 中。文档库文件
（FolderCrawl→FileCrawl）和列表项附件（ItemAttachmentsCrawl→FileCrawl）
都不会产生任何 ``val_*`` 键。

认证
====

共有三种认证方式可供选择，且 **只能配置其中一种**。如果 ``auth.kerberos.principal`` 、
``auth.ntlm.user`` 、``auth.oauth.client_id`` 中设置了多个，数据设置作业会在发出任何请求之前
就以校验错误失败。这是有意为之的限制：HTTP 客户端只会注册一份凭据，而该凭据注册所在的作用域
对 ``Negotiate`` 挑战和 ``NTLM`` 挑战都同样适用，因此如果配置了多个认证方式，就会产生日志中
毫无线索可寻的 401 错误。

NTLM
----

::

    auth.ntlm.user={SharePoint 用户名}
    auth.ntlm.password={密码}
    auth.ntlm.domain={Windows 域。可选，默认未设置}
    auth.ntlm.workstation={NTLM 协商中发送的工作站名称。可选，默认未设置}

``auth.ntlm.domain`` 和 ``auth.ntlm.workstation`` 默认均为未设置，此时构建出的凭据与本连接器
一直以来构建的完全相同。将域写入用户名中的 ``DOMAIN\user`` 形式仍然有效。设置
``auth.ntlm.domain`` 后，域会改为作为独立的 NTLM 字段发送，这正是拒绝组合形式的服务器
所需要的方式。

Kerberos（SPNEGO）
------------------

**支持的范围仅限于以下配置：** 单个爬虫 JVM、每个 Fess 实例一个 ``krb5.conf``、认证方式为
keytab 或密码、不支持委派（delegation）、不支持通道绑定（channel binding），且与 NTLM、
OAuth 互斥。超出此范围的配置均不受支持。

::

    auth.kerberos.principal={客户端主体，格式为 user@REALM。设置后即启用 Kerberos。}
    auth.kerberos.keytab={保存该主体密钥的 keytab 文件路径。与 auth.kerberos.password 互斥。}
    auth.kerberos.password={该主体的密码。仅在未设置 keytab 时使用。}
    auth.kerberos.strip_port={true 或 false。是否从服务主体名称中去除端口号。默认值为 true。}
    auth.kerberos.use_canonical_hostname={true 或 false。是否将目标主机解析为其规范名称用于服务主体名称。默认值为 false。}
    auth.kerberos.krb5_conf={krb5.conf 文件的路径。仅在尚未设置 java.security.krb5.conf 时应用。}
    auth.kerberos.debug={true 或 false。Krb5LoginModule 的调试输出。默认值为 false。}

- **``krb5.conf`` 应配置在 ``jvm.crawler.options`` 中**，写作
  ``-Djava.security.krb5.conf=/path/to/krb5.conf``。数据存储爬取运行在爬虫的 **子进程** 中，
  因此在只影响 webapp 的地方设置该项不会有任何效果，重启 webapp 也不会使其生效 —— 必须重新
  运行爬取作业才能生效。``auth.kerberos.krb5_conf`` 是在该属性尚未被设置时使用的便捷方式：
  它 **绝不会覆盖已经设置的值** （因为该属性是 JVM 全局的，一个爬虫 JVM 会运行一次爬取作业中
  的所有数据设置）。当它因此未能覆盖时，会在日志中记录一条同时列出两个路径的警告。
- **请在 ``krb5.conf`` 的 ``[libdefaults]`` 中设置 ``udp_preference_limit = 1``。** 如果不
  设置，JDK 会先尝试 UDP，当 KDC 无响应时（不可达、防火墙丢弃了 UDP 88 端口，或响应大小超过
  数据报大小限制），会以每次 30 秒的间隔重试三次，然后才回退到 TCP。如果爬取看起来在每次认证
  时都会卡住约一分半钟，且日志中没有任何记录，通常就是这个原因。
- **务必将主体写成 ``user@REALM`` 的形式。** ``default_realm`` 是 JVM 全局设置，而多个位于
  不同领域（realm）的 SharePoint 场可能需要共享同一个 ``krb5.conf``，因此省略领域的 ``user``
  会按照该文件当时所指定的领域进行解析。
- **``auth.kerberos.use_canonical_hostname`` 默认值为 ``false``**，这是特意做出的与 Apache
  HttpClient 自身默认值不同的选择。启用后，会在构建服务主体名称之前对目标主机执行反向 DNS
  解析，在存在备用访问映射（alternate access mapping）或位于负载均衡器之后的环境中，可能会
  解析出一个未注册任何 SPN 的名称 —— 而由此产生的失败完全看不出与 DNS 有关。只有在 SPN
  确实是针对规范名称注册的情况下，才应启用此项。
- **IIS Extended Protection 设置为 ``tokenChecking=Require`` 时无法工作。** Apache HttpClient
  的 4.5 系列和 5.x 系列均不支持通道绑定（channel binding）。IIS 该设置的默认值为 ``None``，
  因此通常不会遇到这个问题，但一旦遇到就没有变通方法。
- **票据仅在构建爬取用的 HTTP 客户端时获取一次，此后不会更新。** 运行时间超过票据有效期的
  爬取，会从中途开始出现认证失败。
- **``auth.kerberos.password`` 与 ``auth.ntlm.password`` 一样，会以明文形式保存和显示。**
  Fess 没有为数据存储处理器参数提供掩码机制，数据设置编辑界面会将它们渲染为普通文本区域。
  请优先使用 ``auth.kerberos.keytab``，并为 keytab 文件设置严格的访问权限。
- 设置 ``auth.kerberos.debug=true`` 会使 ``Krb5LoginModule`` 将输出写入爬虫进程的标准输出，
  而不是 Fess 日志。

OAuth（ACS）
------------

::

    auth.oauth.client_id={OAuth 客户端 ID}
    auth.oauth.client_secret={OAuth 客户端密钥}
    auth.oauth.tenant={租户名称，不含 .sharepoint.com}
    auth.oauth.realm={Azure AD 领域（目录 ID）}

设置 ``auth.oauth.client_id`` 后，会针对 Windows Azure Access Control Service
（``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``）启用客户端凭据
（应用程序专用）流程。访问令牌会在构建爬取用的 HTTP 客户端时获取一次，并以 ``Bearer``
``Authorization`` 请求头的形式附加到每个请求上；遇到 401 时会更新令牌并重试一次。
**Microsoft 已将 ACS 标记为已弃用，并计划将其淘汰。** 每次以 OAuth 方式配置爬取时，
本连接器都会记录一条相应的警告。这里没有实现 Entra ID 应用注册（基于证书或客户端密钥）
流程 —— 仅支持旧版的 ACS 应用程序专用认证。

在启用 OAuth 之前，只会检查 ``auth.oauth.client_id`` 是否存在；``client_secret`` 、
``tenant`` 、``realm`` 则是无条件读取的，如果省略就会在不产生任何专门校验提示的情况下
悄然保持为空，从而导致令牌获取失败。

**``sp.version=2013`` 与 OAuth 从未能一起正常工作。** 本连接器针对 SharePoint 2013 发出的
所有 API 调用都会经过 XML/Atom 客户端，而该客户端的任何代码路径都不会为请求附加 OAuth
令牌 —— 因此两者同时设置时，所有请求都会以未认证状态发出。爬取过程会准确记录这一情况的
警告日志，并指出 ``auth.ntlm.*`` 作为替代方案；但不会使该作业失败。SharePoint 2013 请
使用 ``auth.ntlm.*``。

权限
====

设置 ``role.skip=true`` （默认 ``false``）会完全跳过逐项权限的获取：不会调用
``GetListItemRole``，也不会为该项目设置 ``role`` 键，文档最终只会带有数据设置本身的
静态权限设置，以及（如果配置了的话）``default_permissions`` —— 完全不会带有任何
来自 SharePoint 的权限。

获取角色时，SharePoint 自身的用户、安全组和 SharePoint 组都会被展开，并映射为 Fess
的搜索角色：

- **本地 AD** 账户或组（登录名包含反斜杠，且不以 Azure 声明前缀开头）通过标准的 AD
  用户/组角色辅助工具进行映射。
- **Azure AD（Entra ID）** 账户（登录名以 ``i:0#.f|membership|`` 开头）会被 **映射两次** ——
  一次使用其完整的 Azure 声明值，一次使用该声明中 ``@`` 之前的 AD 账户部分，因此同一个用户
  会同时获得 Entra ID 形式和 AD 形式两种角色。被判定为 Azure 类型的安全组（通过若干种声明式
  前缀之一识别，其中包括特殊的「全体成员」组 ``spo-grid-all-users``）也会以相同方式，
  同时以两种形式进行映射。
- **SharePoint 组** 会递归展开其自身的成员关系（用户、安全组、嵌套组），并设有已访问组的
  防护机制，以阻止相互包含的组之间发生无限递归。

``default_permissions`` （逗号分隔）会在上述所有映射之后进行合并，即使 SharePoint 对该
项目完全没有返回任何角色（``role.skip=true`` 和「SharePoint 未返回任何内容」这两种情况
都属于此类）也同样会应用。最终的角色列表是数据设置的静态权限设置、SharePoint 派生的角色
（除非被跳过）以及 ``default_permissions`` 三者的并集，并经过去重。

子站点和托管路径
================

设置 ``site.path`` 后，会按原样使用指定的服务器相对托管路径，代替硬编码的 ``/sites/``
前缀，此时不再需要 ``site.name``。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 场景
     - 设置
   * - 根站点集合
     - ``site.path=/``
   * - ``/teams/eng`` 站点
     - ``site.path=/teams/eng``
   * - 传统的 ``/sites/mysite/`` 形式
     - ``site.name=mysite`` （不设置 ``site.path``）

设置 ``site.crawl_subsites`` （默认 ``false``）会使整站爬取（即既未设置 ``site.list_name``
也未设置 ``site.doclib_path`` 的爬取）递归进入通过 ``_api/web/webinfos`` 发现的站点子站点。
保持未设置时，爬取发出的请求与以往完全相同，包括从不请求 ``webinfos``。

子站点的文档会与根站点的文档一起归入同一个数据设置，各自使用自己的服务器相对路径 ——
索引中没有任何信息能标记出某个文档是来自子站点而非根站点。

``site.max_depth`` （默认 ``10``）限制了在 ``site.crawl_subsites=true`` 时，从根站点向下
爬取的子站点层数上限。根站点自身的深度为 0，因此 ``site.max_depth=1`` 只会爬取根站点的
直接子站点，不再继续深入。在 ``site.crawl_subsites=true`` 的情况下将 ``site.max_depth``
设置为小于 ``1`` 的值，会使该功能实际上被关闭 —— 不会爬取任何子站点 —— 并会在爬取开始
时记录一条警告。

启用子站点爬取会使爬取的总耗时大致按发现的子站点数量（受 ``site.max_depth`` 限制）成倍
增加：除了根站点爬取本身已有的所有工作之外，每个子站点还会各自产生一次完整的文件夹列表
获取、列表获取，以及（如果尚未达到深度上限）一次 ``webinfos`` 调用。

`并行爬取与负载`_ 一节中介绍的 ``number_of_threads`` 和 ``readInterval``，对包含子站点
递归的爬取同样适用，与其他任何爬取一样。

并行爬取与负载
==============

``number_of_threads`` （默认 ``1``）是同时处理的爬取目标数量。在默认值下，爬取的运行方式
与以往完全相同：每个目标都在爬取线程上处理，**完全不会创建线程池**。

该值的上限为运行 Fess 的机器处理器核心数的两倍，因此数据设置无法请求超出主机处理能力的
并发度。小于 ``1`` 的值，或空白、无法解析的值，都会回退为 ``1``，而不会被直接采用或使作业
失败。被限制到上限的值，或小于 ``1`` 的值，会同时记录请求值和实际值；无法解析的值会记录
一条警告。空白值不会记录任何日志，因为字段为空只是表示该参数根本没有设置。

HTTP 连接池的大小会随之调整。Apache HttpClient 默认每条路由（route）只允许 2 个连接，
而整次爬取被视为一条路由：如果不提高这个上限，第三个及以后的线程就会把大部分时间花在
等待连接上，而不是发出请求。

**无论 ``readInterval`` 设置为多少，它仍然会以每个间隔一个文档的节奏控制文档的移交。**
线程能让爬取的发现和获取速度更快，但不会让文档到达索引器的速度更快。这是有意为之的设计 ——
如果把运维人员配置的间隔除以线程数，恰好会把该间隔原本要限制的负载放大相同的倍数。如果某个
worker 完成了一个文档处理，而之前的文档仍在移交中，它就只能等待。

提高 ``number_of_threads`` **确实会** 成倍增加的是针对 SharePoint 的请求速率。下文所述的
503 退避等待和 ``X-SharePointHealthScore`` 等待都是按每个爬取目标、在爬取该目标的线程上
应用的，因此 ``n`` 个线程发出的请求最多可达单线程爬取的 ``n`` 倍 —— 包括在场（farm）正在
表明自己很忙的那段时间里也是如此。对于本地部署的场，请逐步提高该值。

有两个因素限制了增加线程数实际能带来的收益：

- **每个 SharePoint 组的成员关系首次被读取时，都是一次一个线程地读取。** 权限的解析要经过
  整次爬取共享的缓存，该缓存在一个组的成员查找期间由单一的锁保护。这把锁可以防止某个线程把
  一个成员仍在读取中的组交给另一个线程，从而避免在不带有任何权限的情况下索引该组所保护的
  项目。一个组一旦被缓存，之后对它的每次引用都只是一次廉价的查找，因此这是一种 **冷缓存
  成本**：拥有众多不同组的站点，其爬取的最初几分钟表现更接近单线程而非 ``n`` 线程，而项目
  共享少数几个组的站点则几乎感觉不到差异。完全不读取权限的 ``role.skip=true`` 可以完全
  避免这一成本。
- 每个站点的发现过程是串行的：一个站点的文件夹列表和列表获取本身就是一个爬取目标，因此
  在该目标完成并将发现结果加入队列之前，线程之间没有任何工作可以分担。

**503 响应** 与其他错误一样会被重试，最多重试 ``retry_limit`` 次，但每次重试前的等待时间
会递增：2 秒、4 秒、8 秒，以 30 秒为上限逐次翻倍，且每次都会在该值的 70%-129% 范围内
随机化。持续返回 503 的爬取目标，会在它实际获得的每一次重试之前都付出这一等待，但最后一次
重试之后不会再等待。

**每一个响应** —— 无论成功与否，包括爬取即将丢弃的某个列表分页 —— 都会被检查
``X-SharePointHealthScore`` 响应头（0 表示空闲，10 表示非常繁忙）。分数达到 9 或以上时，
爬取会在做任何其他事情之前先等待：分数为 9 时等待约 2 秒，为 10 时约 4 秒，此后每增加
1 分等待时间翻倍。**这种等待会在整个爬取过程中不断累积，且没有总量上限**：一个持续处于
高负载、健康分数维持在 9 的场，会给本连接器发出的 **每一个** 请求都额外增加约 2 秒 ——
包括每个文件夹和列表分页的获取 —— 这可能会让原本只需数小时的爬取耗时大幅延长。如果爬取
的速度出现数量级的意外下降，请先检查该时段场的健康分数，再考虑其他原因。

配置示例
========

以下示例均假定使用 NTLM。如果要改用 Kerberos 或 OAuth，请参见 `认证`_ 并替换
``auth.ntlm.*`` 相关的行。

列表爬取
--------

参数:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

脚本:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

文档库爬取
----------

参数:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

脚本:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

爬取 ``/teams/`` 站点
---------------------

``site.path`` 可让你直接指向位于 ``/sites/`` 以外的托管路径下某个站点中的文档库。

参数:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

脚本:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

递归子站点爬取
--------------

从根站点集合开始，沿子站点递归爬取，最深至第 3 层。

参数:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

脚本:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

限制事项
========

- **完全不支持任何形式的增量或差分爬取。** 本连接器中不存在任何变更令牌（change-token）、
  差分查询（delta-query）或「自上次以来已修改」之类的过滤机制 —— 每次运行都会对配置要
  到达的每个列表、文件夹和文件进行完整列举。``delete_old_docs`` 只是控制本次完整爬取
  未再次发现的文档事后是否会被删除，这只是善后清理，并不是增量获取。
- **文件名/文件夹名中的 ``%`` 和 ``#``** 在默认（非 ``2013``）代码路径下受支持。只有
  SharePoint Server 2019 和 Subscription Edition 才允许名称中出现这两个字符；2016 明确
  仍然拒绝，2013 同样拒绝。默认代码路径通过接收已解码路径的
  ``...ByServerRelativePath(decodedUrl=...)`` 系列端点访问这类文件，并且在建立索引所用的
  链接中也会对这两个字符进行转义。**``sp.version=2013`` 无法访问这类文件**，因为它使用更老的
  ``...ByServerRelativeUrl(...)`` 系列端点，而这些端点会把参数当作已编码的 URL 来解释。
  这是有意的限制而非缺陷：SharePoint 2013 的场本身就无法保存这样的名称，因此只有把
  ``sp.version=2013`` 指向 2019 或 Subscription Edition 服务器时才有影响，而这种组合并不推荐。
  参见 `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  和 `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__。
- **无法支持 IIS Extended Protection 的 ``tokenChecking=Require`` 设置。** Apache
  HttpClient 的 4.5 系列和 5.x 系列都没有实现通道绑定（channel binding），而
  Extended Protection 在 ``Require`` 级别正是依赖于此。IIS 该设置的默认值为 ``None``，
  因此大多数场不受影响，但对于设置为 ``Require`` 的场，没有任何变通方法。
- **数据设置参数中的密码会以明文形式保存和显示。** 这一点对 ``auth.ntlm.password`` 和
  ``auth.kerberos.password`` 都同样适用：Fess 没有为数据存储处理器参数提供掩码机制，
  数据设置编辑界面会将它们渲染在普通文本区域中。在可以使用 Kerberos 的环境中，请优先
  使用 ``auth.kerberos.keytab`` 而非 ``auth.kerberos.password``，并为 keytab 文件设置
  严格的访问权限。
- **``sp.version=2013`` 与 OAuth 从未能一起正常工作。** 所有 SharePoint 2013 的 API 调用
  都经过 XML/Atom 客户端，而该客户端的任何代码路径都不会为请求附加 OAuth 令牌，因此两者
  同时设置时所有请求都会以未认证状态发出。SharePoint 2013 请使用 ``auth.ntlm.*``。
- **除 ``/sites/`` 以及通过 ``site.path`` 设置的那一个托管路径之外，其余托管路径仍然不会
  被自动发现。** ``site.crawl_subsites`` 只会从你所配置的根站点开始递归，而 ``site.path``
  也只能到达你所设置的那一个托管路径，并不会覆盖场上的所有托管路径。

故障排除
========

认证静默失败
------------

**症状**: 请求返回 401（或类似错误），但日志中没有明确的原因说明

**确认事项**:

1. 检查 ``auth.kerberos.principal`` 、``auth.ntlm.user`` 、``auth.oauth.client_id`` 中
   是否设置了多个 —— 设置两个及以上会在爬取开始前就以校验错误使作业失败
2. 对于 Kerberos，确认 ``-Djava.security.krb5.conf=...`` 已设置在 ``jvm.crawler.options``
   中。设置在只影响 webapp 的地方不会有任何效果。更改后需要重新运行爬取作业 —— 重启
   webapp 不会使其生效
3. 对于 Kerberos，确认 ``krb5.conf`` 的 ``[libdefaults]`` 中已设置
   ``udp_preference_limit = 1``。如果没有设置，KDC 无响应时会导致每次认证卡住约 90 秒
   （3 次 30 秒的 UDP 重试），且日志中不会留下任何记录
4. 确认主体已写成 ``user@REALM`` 的形式 —— 省略领域的 ``user`` 会按照共享的
   ``krb5.conf`` 当时指定的 ``default_realm`` 进行解析
5. 对于 OAuth，确认 ``client_secret`` 、``tenant`` 、``realm`` 均不为空 —— 只有
   ``client_id`` 的存在性会被校验，其余几项可能在毫无提示的情况下为空
6. 确认 IIS Extended Protection 未设置为 ``tokenChecking=Require`` —— 该设置没有
   任何变通方法
7. 对于长时间运行的爬取，检查是否从中途才开始出现失败 —— Kerberos 票据仅在构建
   HTTP 客户端时获取一次，此后不会更新，因此运行时间超过票据有效期的爬取会从中途开始
   失败

爬取速度缓慢（503 与健康分数）
------------------------------

**症状**: 爬取耗时远超预期，或发生超时

**确认事项**:

1. 检查该缓慢时段内 SharePoint 场的 ``X-SharePointHealthScore``。分数达到 9 或以上
   会在每个请求前增加等待（9 时约 2 秒，10 时约 4 秒，此后逐次翻倍，且无总量上限），
   可能会让原本只需数小时的爬取耗时大幅延长
2. 检查是否反复出现 503 响应。503 最多会被重试 ``retry_limit`` 次，每次重试前依次
   等待 2 秒、4 秒、8 秒（上限 30 秒）
3. 检查 ``number_of_threads`` 是否设置得过高。线程数越多，针对 SharePoint 的请求量
   大致会成比例增加，这可能会推高健康分数。对于本地部署的场，请逐步提高该值
4. 如果设置了 ``site.crawl_subsites=true``，请记住爬取总耗时大致会随发现的子站点
   数量增长 —— 可以考虑通过 ``site.max_depth`` 缩小范围

没有任何内容被索引
------------------

**症状**: 爬取正常结束，但搜索结果为 0 件

**确认事项**:

1. 检查爬虫日志中是否有错误或警告（可在
   ``app/WEB-INF/env/crawler/resources/log4j2.xml`` 中将 ``org.codelibs.fess.ds``
   设置为 ``DEBUG``）
2. 检查 ``url`` 、``site.name`` （或 ``site.path``）、``site.list_name`` 是否有
   拼写错误 —— 注意一旦设置了 ``site.path``，就不再需要 ``site.name``
3. 确认认证确实成功（没有 401）—— 请求从未通过认证，是比 ``role.skip`` 或
   ``default_permissions`` 配置错误更常见得多的原因
4. 如果设置了 ``include_pattern`` 或 ``exclude_pattern``，请注意它们匹配的是
   服务器相对路径（对于文档库文件或列表项附件）或 ``FileRef`` （对于列表项）——
   而不是搜索结果中显示的 URL。检查是否误写成了针对完整 URL 的模式
5. 检查 ``supported_mimetypes`` 或 ``max_content_length`` 是否排除了你期望看到
   的文件
6. 检查 ``site.exclude_list`` 或 ``site.exclude_folder`` 是否无意中排除了目标

参考信息
========

- :doc:`ds-overview` - 数据存储连接器概述
- :doc:`ds-microsoft365` - Microsoft 365 连接器（用于 SharePoint Online）
- :doc:`../../admin/dataconfig-guide` - 数据存储配置指南
- :doc:`../../admin/plugin-guide` - 插件管理指南
