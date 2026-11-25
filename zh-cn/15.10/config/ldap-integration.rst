==============================
LDAP集成指南
==============================

概述
====

|Fess| 支持与LDAP（轻量级目录访问协议）服务器集成，
可以实现企业环境中的认证和用户管理。

通过LDAP集成可以实现:

- 使用Active Directory或OpenLDAP进行用户认证（登录）
- 基于组和角色的访问控制
- 通过管理界面管理LDAP用户/角色/组（可选）

支持的LDAP服务器
================

|Fess| 支持与以下LDAP服务器集成:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- 其他LDAP v3兼容服务器

前提条件
========

- 对LDAP服务器的网络访问
- 用于LDAP搜索的服务账号（绑定DN）
- 对LDAP结构（基础DN、属性名等）的了解

设置方法概述
============

|Fess| 的LDAP设置根据用途在两个地方进行管理。

连接与认证设置（管理界面 / ``system.properties``）
   与LDAP服务器的连接及登录认证相关的设置。
   可通过管理界面 **"系统 > 通用"** 页面中的"LDAP"部分进行设置，
   保存至 ``app/WEB-INF/conf/system.properties``\ 。

LDAP管理功能与行为设置（``fess_config.properties``）
   通过管理界面管理LDAP用户/角色/组的功能，
   以及角色解析等行为相关的设置。这些设置在
   ``app/WEB-INF/classes/fess_config.properties`` 中定义，
   如需更改值请编辑此文件。

.. note::

   仅使用登录认证时，只需"连接与认证设置"即可运行。
   "LDAP管理功能"（``ldap.admin.enabled``）仅在需要通过管理界面
   对LDAP端的用户/角色/组进行创建、更新、删除时才需要启用。

连接与认证设置
==============

这些设置可通过管理界面"系统 > 通用"的LDAP部分进行配置，
保存至 ``app/WEB-INF/conf/system.properties``\ 。也可以直接编辑该文件。

.. list-table:: 连接与认证属性
   :header-rows: 1
   :widths: 30 15 55

   * - 属性
     - 默认值
     - 说明
   * - ``ldap.provider.url``
     - （无）
     - LDAP服务器的URL。例: ``ldap://ldap.example.com:389``\ 。使用LDAPS时为 ``ldaps://ldap.example.com:636``\ 。用空格分隔指定多个URL时可实现故障转移。
   * - ``ldap.base.dn``
     - （无）
     - LDAP搜索的基础DN。例: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - （无）
     - 用户认证（绑定）所使用的DN模板。\ ``%s`` 将被替换为用户名。例: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - LDAP认证方式（JNDI的 ``java.naming.security.authentication``）。通常使用 ``simple``\ 。
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - JNDI初始上下文工厂类。通常无需更改。
   * - ``ldap.admin.security.principal``
     - （无）
     - 用于LDAP搜索的服务账号绑定DN。例: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - （无）
     - 上述服务账号的密码。
   * - ``ldap.account.filter``
     - （无）
     - 解析用户角色时，用于搜索用户条目的过滤器。\ ``%s`` 将被替换为用户名。例: ``uid=%s``
   * - ``ldap.group.filter``
     - （空）
     - 解析组时使用的搜索过滤器。\ ``%s`` 将被替换为用户的DN等。例: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - 表示组成员关系的属性名。用于在Active Directory或具有该属性的服务器上解析角色。

设置示例（直接编辑 ``system.properties`` 时）:

::

    # LDAP服务器URL
    ldap.provider.url=ldap://ldap.example.com:389

    # 基础DN
    ldap.base.dn=dc=example,dc=com

    # 用户认证绑定DN模板（%s将被替换为用户名）
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 搜索用服务账号的绑定DN和密码
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 角色解析用过滤器
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   ``%s`` 占位符由Java的 ``String.format()`` 处理。
   ``ldap.security.principal``、``ldap.account.filter``、``ldap.group.filter`` 以及
   各管理用过滤器均使用 ``%s`` 格式（而非 ``{0}`` 格式）。
   另外，传递给过滤器的用户名会由 |Fess| 内部自动转义，以防止LDAP注入攻击。

LDAP管理功能与行为设置
======================

以下属性在 ``app/WEB-INF/classes/fess_config.properties`` 中定义。
如需更改值请编辑此文件。

管理功能的启用
--------------

.. list-table:: 管理功能属性
   :header-rows: 1
   :widths: 35 15 50

   * - 属性
     - 默认值
     - 说明
   * - ``ldap.admin.enabled``
     - ``false``
     - 启用通过管理界面对LDAP用户/角色/组进行创建、更新、删除的功能。\ **登录认证不需要此功能**，不启用也可通过LDAP进行登录。
   * - ``ldap.admin.sync.password``
     - ``true``
     - 在管理界面更新用户时，将 |Fess| 端的密码与LDAP同步。
   * - ``ldap.auth.validation``
     - ``true``
     - 登录时执行LDAP认证验证。

用户/角色/组管理用过滤器与基础DN
---------------------------------

在 ``ldap.admin.enabled=true`` 时，用于通过管理界面操作LDAP条目。

.. list-table:: 管理用过滤器/基础DN
   :header-rows: 1
   :widths: 38 47 15

   * - 属性
     - 说明
     - 默认值
   * - ``ldap.admin.user.filter``
     - 用户搜索过滤器（``%s`` 替换为用户名）
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - 用户搜索基础DN
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - 创建用户时的objectClass
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - 角色搜索过滤器
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - 角色搜索基础DN
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - 创建角色时的objectClass
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - 组搜索过滤器
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - 组搜索基础DN
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - 创建组时的objectClass
     - ``groupOfNames``

角色解析与行为控制
------------------

控制登录后角色/组解析的行为。

.. list-table:: 行为控制属性
   :header-rows: 1
   :widths: 40 15 45

   * - 属性
     - 默认值
     - 说明
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - 根据用户名授予角色。
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - 根据组授予角色。
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - 根据角色授予角色。
   * - ``ldap.allow.empty.permission``
     - ``true``
     - 允许组/角色为空的用户登录。
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - 从组名等中去除NetBIOS名（``DOMAIN\`` 格式的前缀）。
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - 允许组名中包含下划线。
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - 将权限名转换为小写。
   * - ``ldap.samaccountname.group``
     - ``false``
     - 使用 ``sAMAccountName`` 属性作为组名（适用于Active Directory）。
   * - ``ldap.max.username.length``
     - ``-1``
     - 输入的用户名超过该长度时，保留开头的该数量字符，其余截去（用于旧版 Active Directory 的 20 个字符的登录名）。绑定、用户名、角色搜索、权限名称和会话都使用截断后的名称，不会因长度而拒绝登录。负值（默认值 ``-1``）表示不截断。

.. note::
   使用 LDAP 用户名和密码登录时，会去除输入的用户名前后的空白（名称中间的空白保留）。截断在此之后进行，截断后的名称末尾残留的空白也会被去除。

LDAP 的角色 OU 与嵌套组
-----------------------

组条目是作为角色（权限前缀 ``role.search.role.prefix``，默认 ``R``）还是作为组（``role.search.group.prefix``，默认 ``2``），由其 DN 决定。与 15.9 相比的变更请参阅 :doc:`../install/upgrade`。

15.10 会解析 DN，只有当某个 ``ou`` 组成部分恰好是 ``Role`` 或 ``Roles``\ （不区分大小写）时，才把条目当作角色。其他所有条目都是组，无法解析 DN 的条目也是组。

设置了 ``ldap.group.filter`` 时（默认为空），|Fess| 会用它查找包含用户所属组的组（嵌套组）。直到 15.9，用户所属组的 DN 是不经转义直接放入该过滤器的。包含转义字符的 DN（例如 ``CN=Sales\, EMEA,...`` 中的逗号）无法匹配，因此这类组的嵌套组会在没有任何错误的情况下缺失；包含 LDAP 过滤器特殊字符的 DN 则会改变过滤器。15.10 会转义 DN（RFC 4515）。这类组的嵌套组现在可以找到，相关用户也会获得这些组的权限。

保留的管理员用户名
------------------

``authentication.admin.users`` 中列出的名称由 |Fess| 为自身保留。在SSO中它们作为阻止列表：
``SpnegoAuthenticator`` 不会为匹配的名称解析凭据，表单登录也不会将该名称交给LDAP。

目录不区分账户名称的大小写——Active Directory 对任何写法都会签发票据——因此按完全一致比较时，
同一账户只要改变大小写就能登录。``authentication.admin.users.ignore.case`` 决定比较方式。

.. list-table:: 保留名称的比较
   :header-rows: 1
   :widths: 40 15 45

   * - 属性
     - 默认值
     - 说明
   * - ``authentication.admin.users``
     - ``admin``
     - 保留的管理员用户名，以逗号分隔。
   * - ``authentication.admin.users.ignore.case``
     - ``auto``
     - 保留名称的比较方式。``auto`` 仅在设置了 ``ldap.provider.url`` 时忽略大小写，未设置时按完全一致比较。``true`` 与 ``false`` 直接指定。

.. note::
   在设置了 ``ldap.provider.url`` 的配置中，``auto`` 会忽略大小写。此时，目录中仅大小写与保留名称不同的账户将无法登录，也不再从管理界面同步到目录。若需按完全一致比较，请设置 ``authentication.admin.users.ignore.case=false``。

.. _local-username-policy:

本地用户名策略
--------------

|Fess| 对本地用户（用户管理页面中的用户，不包括 LDAP 或 SSO 用户）的名称按输入原样进行比较。 ``Alice`` 、 ``alice`` 和 ``ＡＬＩＣＥ`` （全角字母）是三个用户，各有自己的登录。 ``authentication.local.username.policy`` 决定创建或重命名本地用户时，是否也拒绝与其他用户的名称仅在大小写、字符宽度或 Unicode 组合方式上不同的名称。

.. list-table:: 本地用户名策略
   :header-rows: 1
   :widths: 40 15 45

   * - 属性
     - 默认值
     - 说明
   * - ``authentication.local.username.policy``
     - ``preserved``
     - ``preserved`` 与 15.9 相同，按输入原样比较名称。 ``mapped`` 会拒绝经过映射（见下文）后与其他用户的名称相同的新名称或重命名后的名称。该值的比较不区分大小写。未知的值按 ``preserved`` 处理，并记录一次警告。

使用 ``mapped`` 时，在用户管理页面或通过 Admin API（ ``/api/admin/user/setting`` 的 ``POST`` 和 ``PUT`` ）创建或重命名用户，在以下两种情况下会被拒绝：

- 映射后的名称与其他用户映射后的名称相同。映射与 RFC 8265 的 ``UsernameCaseMapped`` 相同：全角形式和半角形式（如半角片假名）以及表意文字空格被替换为其分解映射，使用根区域设置转换为小写，结果转换为 Unicode 规范化形式 C（不是 NFKC）。 ``Alice`` 、 ``alice`` 和 ``ＡＬＩＣＥ`` 映射后是同一个名称。
- 名称是 ``authentication.admin.users`` 中某个条目的另一种写法（见上文）。 ``admin`` 因为就是条目本身的写法，所以仍可重新创建，而 ``Admin`` 、 ``ADMIN`` 和全角写法会被拒绝。

以其已有的名称保存的用户不会被拒绝，因此目前已冲突的用户仍可编辑。使用 ``mapped`` 启动 |Fess| 时，它会在 ``fess.log`` 中写入一条警告，列出最多 20 组映射后相同的已保存名称，以及最多 20 个包含空白或控制字符的已保存名称。它不会更改任何内容：这些用户仍可登录并可被编辑。

.. note::

   该策略只决定是否接受某个名称。它不会改变登录（按输入原样的名称查找用户）、用户 ID 和保存的名称。它也不会改变由名称生成的权限字符串（角色过滤器、爬取配置的权限或文档中的 ``{user}Alice`` 和 ``{user}alice`` ）以及已建立索引的文档。它也不强制执行 RFC 8265 的字符规则：包含空格、符号或控制字符的名称仍会被接受。

   从备份恢复、首次启动时创建初始 ``admin`` 用户以及直接写入用户索引时，不会进行此检查。两名管理员同时创建 ``Alice`` 和 ``alice`` 时，可能两者都成功，因为不保存映射后的名称。要在登录和权限中统一名称，需要迁移已保存的用户、角色和已建立索引的文档，这不属于此设置。

属性映射
--------

LDAP属性与 |Fess| 用户属性的对应关系通过 ``ldap.attr.*`` 属性定义。
通常无需更改，但在模式不同时可进行调整。典型示例:

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   ``ldap.attr.state`` 映射到 ``st``，``ldap.attr.city`` 映射到 ``l`` 等，
   存在属性名与LDAP属性名不一致的情况。
   完整列表请参考 ``fess_config.properties`` 中以 ``ldap.attr.`` 开头的行。

Active Directory设置
====================

针对Microsoft Active Directory的设置示例（``system.properties`` 或管理界面）。

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 用户认证绑定DN模板（UPN格式）
    ldap.security.principal=%s@example.com

    # 搜索用服务账号
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 账号过滤器
    ldap.account.filter=sAMAccountName=%s

    # 使用memberOf属性
    ldap.memberof.attribute=memberOf

    # 组过滤器
    ldap.group.filter=(member=%s)

如需解析嵌套组（嵌套组），可使用Active Directory特有的
``LDAP_MATCHING_RULE_IN_CHAIN``\ 。

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

OpenLDAP设置
============

针对OpenLDAP的设置示例。

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 用户认证绑定DN模板
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # 搜索用服务账号
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 账号过滤器
    ldap.account.filter=uid=%s

    # 组过滤器（posixGroup时）
    ldap.group.filter=(memberUid=%s)

.. note::

   标准OpenLDAP不具有 ``memberOf`` 属性，
   因此使用 ``ldap.group.filter`` 解析组。
   若已启用 ``memberof`` overlay，也可使用 ``ldap.memberof.attribute``\ 。

安全设置
========

LDAPS（SSL/TLS）
----------------

使用加密连接:

::

    # 使用LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

使用自签名证书时，将证书导入Java truststore:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

密码保护
--------

``ldap.admin.security.credentials`` 保存在 ``system.properties`` 中。
通过管理界面设置的认证信息会在内部加密后保存。
请对文件访问权限进行适当限制。

故障转移
========

如需对多个LDAP服务器进行故障转移，在 ``ldap.provider.url`` 中
用空格分隔指定多个URL。

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

故障排除
========

连接错误
--------

**症状**: LDAP连接失败

**确认事项**:

1. LDAP服务器是否已启动
2. 防火墙是否开放端口（389或636）
3. ``ldap.provider.url`` 是否正确（``ldap://`` 或 ``ldaps://``）
4. ``ldap.admin.security.principal`` 和密码是否正确

认证错误
--------

**症状**: 用户认证失败

**确认事项**:

1. ``ldap.security.principal`` 的模板是否正确（是否包含 ``%s``）
2. 用户是否存在于指定基础DN内
3. ``ldap.account.filter`` 是否正确

无法获取组/角色
---------------

**症状**: 无法获取用户的组或角色

**确认事项**:

1. ``ldap.group.filter`` 是否正确
2. ``ldap.memberof.attribute`` 是否正确（Active Directory时）
3. 组是否存在于搜索基础DN内
4. ``ldap.role.search.*.enabled`` 是否已启用

无法通过管理界面管理用户
------------------------

**症状**: 无法通过管理界面创建、编辑、删除LDAP用户

**确认事项**:

1. ``ldap.admin.enabled`` 是否设置为 ``true``
2. ``ldap.admin.user.base.dn`` 等管理用基础DN是否正确
3. ``ldap.admin.security.principal`` 的服务账号是否具有写入权限

调试设置
--------

如需输出详细日志，在 ``app/WEB-INF/classes/log4j2.xml`` 中添加日志记录器。

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

参考信息
========

- :doc:`security-role` - 基于角色的访问控制
- :doc:`sso-spnego` - SPNEGO（Kerberos）认证
- :doc:`../admin/user-guide` - 用户管理指南
