==========================
按角色和组区分显示搜索结果
==========================

前言
====

当公司内部的文档都能通过一个 Fess 检索之后，接下来的问题就是“给谁看什么”。
人事部的考核资料出现在全体员工的搜索结果中是不行的；反过来，面向全公司的规章只有部分人能看到也不行。

在 Fess 中，爬网配置的「权限」里填写的值会记录到每个文档中，每次搜索时都会与已登录用户的权限进行比对。
本文在 Fess 15.9 中配置按部门区分显示，并逐步进行到确认每个用户能看到哪些文档为止。

按照本文的步骤操作后，您将能够：

- 用组和权限设置部门、高管、全体员工这 3 种公开范围
- 将 Active Directory 的组直接用作权限
- 使标签的显示范围与文档保持一致
- 确认每个用户能看到的文档，以及文档中记录的权限

SSO 的配置在 :doc:`guide-15` 中介绍，通过虚拟主机为多个组织区分使用在 :doc:`guide-13` 中介绍。

权限的机制
==========

权限的写法
----------

在爬网配置的「权限」中，按以下格式每行填写一个值。
只要其中任意一个与用户的权限一致，该文档就会显示在搜索结果中。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 写法
     - 匹配的用户
   * - ``{user}用户名``
     - 该用户本人
   * - ``{group}组名``
     - 属于该组的用户
   * - ``{role}角色名``
     - 拥有该角色的用户
   * - ``(deny){group}组名``
     - 对匹配的用户，即使其他值允许也不显示（也可以加在 ``{user}`` 和 ``{role}`` 前）

用户拥有的权限
--------------

每次搜索时，Fess 按以下方式确定用户的权限。

- 已登录的用户：带本人用户名的 ``{user}``、所属组的 ``{group}``、所拥有角色的 ``{role}``
- 未登录的访客：``{role}guest``

这里的要点是，已登录的用户不会带有 ``{role}guest``。
新建爬网配置的「权限」中一开始就填有 ``{role}guest``。
如果保持不变，文档就会变成未登录的访客能看到、已登录的用户反而看不到。
对于希望全体员工都能看到的文档，请在权限中填写全体员工都所属的组（或角色）。

另外，初始用户 ``admin`` 拥有角色 ``admin`` 和 ``guest``。
在仍登录着管理界面的浏览器中搜索时，会以 ``admin`` 身份进行搜索，因此只显示 ``{role}guest`` 的文档，不显示各部门的文档。

角色与组的区分
--------------

角色和组的比对机制完全相同。
区别在于值的来源。
在 Fess 的用户管理中，可以为每个用户同时分配角色和组。
在 LDAP（Active Directory）集成中，所属组（``memberOf``）会成为 ``{group}组名``\ （只有 DN 中包含 ``ou=Role`` 的条目会成为 ``{role}``）。

本文中，为了让 Fess 用户和 Active Directory 都能使用相同的权限值，部门、全体员工等组织单位全部用组来表示。

本文搭建的配置
==============

以一家公司为例：其公司门户 ``https://intra.example.com/`` 上有各部门的页面和面向全公司的页面。

.. list-table:: 组与用户
   :header-rows: 1
   :widths: 20 40 40

   * - 用户
     - 所属部门
     - 组
   * - ``sato``
     - 销售部
     - ``Sales``、``AllStaff``
   * - ``suzuki``
     - 开发部
     - ``Engineering``、``AllStaff``
   * - ``tanaka``
     - 人事部
     - ``HR``、``AllStaff``
   * - ``yamada``
     - 高管
     - ``Executives``、``AllStaff``

.. list-table:: 爬网配置的权限
   :header-rows: 1
   :widths: 25 40 35

   * - 爬网配置
     - URL
     - 权限
   * - 销售部
     - ``https://intra.example.com/sales/``
     - ``{group}Sales`` 和 ``{group}Executives``
   * - 开发部
     - ``https://intra.example.com/dev/``
     - ``{group}Engineering`` 和 ``{group}Executives``
   * - 人事部
     - ``https://intra.example.com/hr/``
     - ``{group}HR`` 和 ``{group}Executives``
   * - 全公司通用
     - ``https://intra.example.com/common/``
     - ``{group}AllStaff``

在此配置下，每个用户能看到的文档如下。

.. list-table:: 每个用户能看到的文档
   :header-rows: 1
   :widths: 30 70

   * - 用户
     - 搜索结果中出现的文档
   * - ``sato``
     - 销售部、全公司通用
   * - ``suzuki``
     - 开发部、全公司通用
   * - ``tanaka``
     - 人事部、全公司通用
   * - ``yamada``
     - 销售部、开发部、人事部、全公司通用
   * - 未登录的访客
     - 无
   * - ``admin``\ （搜索界面）
     - 无

如果希望未登录的访客也能看到全公司通用的文档，请在全公司通用的配置中再加上 ``{role}guest``。
这种情况下，``admin`` 也会看到全公司通用的文档。

组名在比对时区分大小写。
``{group}sales`` 和 ``{group}Sales`` 会被视为不同的组，因此组的名称和权限的值要写成相同的拼写。

使用 Fess 用户进行配置
======================

创建组和用户
------------

1. 在管理界面的 [用户] > [组] 中点击 [新建]，在「名称」中输入 ``Sales``，然后点击 [创建]。用同样的方法创建 ``Engineering``、``HR``、``Executives``、``AllStaff``
2. 在 [用户] > [用户] 中点击 [新建]，输入「用户名」「密码」「密码 (确认)」。密码需要 8 个字符以上
3. 在「组」中按照上表选择所属的组，然后点击 [创建]

用户、组和角色保存在 OpenSearch 中，因此即使在 Docker 中重新创建容器也会保留。

创建爬网配置
------------

为每个部门在 [爬虫] > [Web] 中创建爬网配置。
下表是销售部的示例。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 值
   * - 名称
     - ``销售部门户``
   * - URL
     - ``https://intra.example.com/sales/``
   * - 要包含在爬网中的URL
     - ``https://intra.example.com/sales/.*``
   * - 权限
     - 删除初始值 ``{role}guest``，输入以下 2 行

::

    {group}Sales
    {group}Executives

开发部、人事部、全公司通用也同样创建，只需按表修改 URL 和权限。
创建完成后，在 [系统] > [调度器] 中对「Default Crawler」点击 [立即开始]，执行爬取。
如何确认爬取已完成，请参阅 :doc:`guide-02`。

.. note::

   在文件系统的爬网配置（SMB 或本地文件）中，从文件 ACL 读取的权限会\ **追加**\ 到「权限」的值上，一并记录到文档中。
   此行为默认启用。
   因此，文件服务器上的文档有时会比「权限」中填写的范围显示得更广。
   与 ACL 的组合方式请参阅 :doc:`file-server-search`。
   数据存储爬网配置的权限在 :doc:`datastore-basics` 中介绍。

使用 Active Directory 的组
==========================

如果用户由 Active Directory 管理，请配置 LDAP 集成，而不是在 Fess 中创建用户和组。
已登录用户的 ``memberOf`` 属性中的组会成为 ``{group}`` 权限。

配置 LDAP 连接
--------------

在 [系统] > [通用] 的「LDAP」部分中填写，然后点击 [更新]。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 输入示例
   * - LDAP URL
     - ``ldap://ad.example.com:389``
   * - 基本DN
     - ``dc=example,dc=com``
   * - 绑定DN
     - ``cn=fess,cn=Users,dc=example,dc=com``\ （用于查询的服务账户）
   * - 密码
     - 服务账户的密码
   * - 用户DN
     - ``%s@example.com``\ （``%s`` 处填入登录名）
   * - 帐户过滤器
     - ``sAMAccountName=%s``
   * - memberOf属性
     - ``memberOf``

各项目的详细说明，以及用于解析嵌套组的「组过滤器」的写法，请参阅 `LDAP集成指南 <https://fess.codelibs.org/zh-cn/stable/config/ldap-integration.html>`__。

.. warning::

   [通用] 的设置保存在 ``system.properties`` 中。
   在 docker-fess 的构成中，该文件位于 ``fess01`` 容器内，因此用 ``down`` → ``up`` 重新创建容器后会丢失（参见 :doc:`guide-02` 中关于停止与重启的小节）。

组名与权限的对应
----------------

组的 DN 中最末端的 ``CN`` 的值会成为组名。

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - memberOf 的值
     - 用户的权限
   * - ``CN=Sales,OU=Groups,DC=example,DC=com``
     - ``{group}Sales``
   * - ``CN=AllStaff,OU=Groups,DC=example,DC=com``
     - ``{group}AllStaff``

只要将 Active Directory 一侧的组名设为 ``Sales``、``Engineering``、``HR``、``Executives``、``AllStaff``，上一章的爬网配置就可以直接使用。
如果名称不同，请将权限的值改写为与 Active Directory 的组名一致。

面向全体员工的组，请准备一个所有人都直接所属的组。
Active Directory 的主要组（通常是 ``Domain Users``）不包含在 ``memberOf`` 属性中，因此即使写成 ``{group}Domain Users`` 也不会匹配。

用户获得了哪些权限，可以将 ``org.codelibs.fess.ldap`` 的日志设为 DEBUG 来确认。
从 LDAP 获取权限时，以 ``Roles:`` 开头的行会输出到 ``fess.log``。
设置方法请参阅 LDAP集成指南中的“调试设置”。
该行中的值以后文介绍的内部格式（如 ``2Sales``）显示。

如果要让用户通过 SSO（Entra ID、OpenID Connect、SAML、SPNEGO）登录，需要为每种方式安装对应的 ``fess-sso-*`` 插件。
接收组和角色的方式也因方式而异，请参阅 :doc:`guide-15`。

使标签的显示范围保持一致
========================

标签也有「权限」，用于决定是否在搜索界面的标签选项中显示该标签。
它不影响文档是否显示，但新建的标签一开始也填有 ``{role}guest``，因此保持不变的话，已登录用户的选项中不会显示该标签。

下面是附加到人事部文档的标签示例。
在 [爬虫] > [标签] 中点击 [新建]，按如下内容输入。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 值
   * - 名称
     - ``人事部``
   * - 值
     - ``hr``\ （仅限字母、数字和下划线）
   * - 包含的路径
     - ``https://intra.example.com/hr/.*``
   * - 权限
     - ``{group}HR`` 和 ``{group}Executives``\ （与文档相同的范围）

标签的权限在保存时就会反映到选项中。
而将标签附加到文档的「包含的路径」是在爬取时应用的，因此请在创建标签后执行爬取。

更改权限后重新爬取
==================

权限是在爬取时记录到文档中的。
即使更改了爬网配置的「权限」，已在索引中的文档的权限也不会改变。
更改后，请执行包含该爬网配置的作业（如「Default Crawler」）。

在 Web 和文件系统的爬网配置中，权限发生变化的文档会在下一次爬取时重新获取，并替换相同 URL 的旧文档。
在重新爬取完成之前，这些文档会以旧的权限继续出现在搜索结果中。
缩小公开范围时，请立即执行爬取。

如果只想立即重新爬取某个爬网配置，请在该爬网配置的详细信息界面中点击 [创建新作业]，然后用 [立即开始] 运行创建的作业。

确认运行效果
============

按用户搜索
----------

1. 在浏览器的隐私窗口中打开 ``http://localhost:8080/``。这是因为在已登录管理界面的窗口中会以 ``admin`` 身份搜索
2. 不登录进行搜索，确认不显示各部门和全公司通用的文档
3. 通过搜索界面顶部的登录链接以 ``sato`` 登录，确认只显示销售部和全公司通用的文档
4. 点击界面顶部的用户名，选择「注销」，然后用 ``suzuki``、``tanaka``、``yamada`` 同样进行确认

确认时，使用所有文档中都包含的词（例如公司名）进行搜索，更容易比较显示的文档范围。

查看文档中记录的权限
--------------------

如果显示结果与预期不符，请确认文档中记录的权限。

1. 打开管理界面的 [系统信息] > [搜索]，用文档 URL 或标题中的词进行搜索。此界面不按权限过滤，会显示所有文档
2. 点击目标文档的 [更新] 会打开编辑界面，``role`` 字段中显示记录的权限。仅用于确认，请不要保存

``role`` 字段的值以如下内部格式显示。

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - 权限
     - role 字段中的显示
     - 示例
   * - ``{user}用户名``
     - ``1`` + 名称
     - ``1sato``
   * - ``{group}组名``
     - ``2`` + 名称
     - ``2Sales``
   * - ``{role}角色名``
     - ``R`` + 名称
     - ``Rguest``
   * - 带 ``(deny)``
     - 开头加 ``D``
     - ``D2Sales``

如果销售部文档的 ``role`` 字段为 ``2Sales`` 和 ``2Executives``，说明权限已按配置记录。
如果仍残留 ``Rguest``，说明更改权限后没有重新爬取，或者忘记删除初始值 ``{role}guest``。

不向未登录的用户显示任何内容
============================

如果将 Fess 放在公司外部人员也能访问的网络中，或者根本不允许未登录时搜索，请在 [系统] > [通用] 中启用「需要登录」。
启用后，未登录的访客将无法进行搜索。

这是与基于权限的区分显示相互独立的设置。
即使仍有带 ``{role}guest`` 的文档，也不会再向未登录的访客显示。
此设置同样保存在 ``system.properties`` 中，因此在 Docker 中需要与 LDAP 设置同样注意。

延伸阅读
========

- 想利用文件服务器的 ACL 区分显示：:doc:`file-server-search`
- 想通过 SSO 让用户直接用公司账户登录：:doc:`guide-15`
- 想让多个组织分别使用一个 Fess：:doc:`guide-13`
- 想为 Slack 或云存储中的文档也加上权限：:doc:`datastore-basics`
- 想搜索开发团队的 Git、Confluence、Jira、Slack：:doc:`guide-06`

参考资料
========

- `基于角色的搜索配置 <https://fess.codelibs.org/zh-cn/stable/config/security-role.html>`__
- `角色检索（面向用户） <https://fess.codelibs.org/zh-cn/stable/user/role-search.html>`__
- `LDAP集成指南 <https://fess.codelibs.org/zh-cn/stable/config/ldap-integration.html>`__
- `用户 <https://fess.codelibs.org/zh-cn/stable/admin/user-guide.html>`__
- `组 <https://fess.codelibs.org/zh-cn/stable/admin/group-guide.html>`__
- `标签 <https://fess.codelibs.org/zh-cn/stable/admin/labeltype-guide.html>`__
- `搜索（管理界面） <https://fess.codelibs.org/zh-cn/stable/admin/searchlist-guide.html>`__
