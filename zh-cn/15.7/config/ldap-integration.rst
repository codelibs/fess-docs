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
   保存至 ``app/WEB-INF/conf/system.properties``。

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
保存至 ``app/WEB-INF/conf/system.properties``。也可以直接编辑该文件。

.. list-table:: 连接与认证属性
   :header-rows: 1
   :widths: 30 15 55

   * - 属性
     - 默认值
     - 说明
   * - ``ldap.provider.url``
     - （无）
     - LDAP服务器的URL。例: ``ldap://ldap.example.com:389``。使用LDAPS时为 ``ldaps://ldap.example.com:636``。用空格分隔指定多个URL时可实现故障转移。
   * - ``ldap.base.dn``
     - （无）
     - LDAP搜索的基础DN。例: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - （无）
     - 用户认证（绑定）所使用的DN模板。``%s`` 将被替换为用户名。例: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - LDAP认证方式（JNDI的 ``java.naming.security.authentication``）。通常使用 ``simple``。
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
     - 解析用户角色时，用于搜索用户条目的过滤器。``%s`` 将被替换为用户名。例: ``uid=%s``
   * - ``ldap.group.filter``
     - （空）
     - 解析组时使用的搜索过滤器。``%s`` 将被替换为用户的DN等。例: ``(member=%s)``
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
     - 启用通过管理界面对LDAP用户/角色/组进行创建、更新、删除的功能。**登录认证不需要此功能**，不启用也可通过LDAP进行登录。
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
     - 用户名的最大长度。``-1`` 表示无限制。

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
``LDAP_MATCHING_RULE_IN_CHAIN``。

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
   若已启用 ``memberof`` overlay，也可使用 ``ldap.memberof.attribute``。

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
