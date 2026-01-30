==================================
LDAP集成指南
==================================

概述
====

|Fess| 支持与LDAP（轻量级目录访问协议）服务器集成，
可以实现企业环境中的认证和用户管理。

通过LDAP集成可以实现:

- 使用Active Directory或OpenLDAP进行用户认证
- 基于组的访问控制
- 用户信息的自动同步

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
- LDAP搜索用的服务账号（绑定DN）
- 对LDAP结构（基础DN、属性名等）的了解

基本设置
========

在 ``app/WEB-INF/conf/system.properties`` 中添加以下设置。

LDAP连接设置
------------

::

    # 启用LDAP认证
    ldap.admin.enabled=true

    # LDAP服务器URL
    ldap.provider.url=ldap://ldap.example.com:389

    # 安全连接（LDAPS）时
    # ldap.provider.url=ldaps://ldap.example.com:636

    # 基础DN
    ldap.base.dn=dc=example,dc=com

    # 绑定DN（服务账号）
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # 绑定密码
    ldap.admin.security.credentials=your_password

用户搜索设置
----------------

::

    # 用户搜索的基础DN
    ldap.user.search.base=ou=users,dc=example,dc=com

    # 用户搜索过滤器
    ldap.user.search.filter=(uid={0})

    # 用户名属性
    ldap.user.name.attribute=uid

组搜索设置
----------------

::

    # 组搜索的基础DN
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # 组搜索过滤器
    ldap.group.search.filter=(member={0})

    # 组名属性
    ldap.group.name.attribute=cn

Active Directory设置
====================

针对Microsoft Active Directory的设置示例。

基本设置
--------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 服务账号（UPN格式）
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # 用户搜索
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # 组搜索
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Active Directory特定设置
--------------------------

::

    # 嵌套组解析
    ldap.memberof.enabled=true

    # 使用memberOf属性
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

OpenLDAP设置
============

针对OpenLDAP的设置示例。

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # 服务账号
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # 用户搜索
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # 组搜索
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
    ldap.group.name.attribute=cn

安全设置
================

LDAPS（SSL/TLS）
----------------

使用加密连接:

::

    # 使用LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

    # 使用StartTLS
    ldap.start.tls=true

使用自签名证书时，将证书导入Java truststore:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

密码保护
----------------

使用环境变量设置密码:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

角色映射
================

可以将LDAP组映射到 |Fess| 的角色。

自动映射
--------------

组名直接用作角色名:

::

    # LDAP组 "fess-users" → Fess角色 "fess-users"
    ldap.group.role.mapping.enabled=true

自定义映射
------------------

::

    # 组名映射到角色
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

用户信息同步
==================

可以将LDAP中的用户信息同步到 |Fess|。

自动同步
--------

登录时自动同步用户信息:

::

    ldap.user.sync.enabled=true

同步的属性
------------

::

    # 邮箱地址
    ldap.user.email.attribute=mail

    # 显示名
    ldap.user.displayname.attribute=displayName

连接池
==============

用于提高性能的连接池设置:

::

    # 启用连接池
    ldap.connection.pool.enabled=true

    # 最小连接数
    ldap.connection.pool.min=1

    # 最大连接数
    ldap.connection.pool.max=10

    # 连接超时（毫秒）
    ldap.connection.timeout=5000

故障转移
================

多LDAP服务器的故障转移:

::

    # 用空格分隔指定多个URL
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

故障排除
======================

连接错误
----------

**症状**: LDAP连接失败

**确认事项**:

1. LDAP服务器是否已启动
2. 防火墙是否开放端口（389或636）
3. URL是否正确（``ldap://`` 或 ``ldaps://``）
4. 绑定DN和密码是否正确

认证错误
----------

**症状**: 用户认证失败

**确认事项**:

1. 用户搜索过滤器是否正确
2. 用户是否存在于搜索基础DN内
3. 用户名属性是否正确

无法获取组
----------------------

**症状**: 无法获取用户的组

**确认事项**:

1. 组搜索过滤器是否正确
2. 组的成员属性是否正确
3. 组是否存在于搜索基础DN内

调试设置
------------

输出详细日志:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

参考信息
========

- :doc:`security-role` - 基于角色的访问控制
- :doc:`sso-spnego` - SPNEGO（Kerberos）认证
- :doc:`../admin/user-guide` - 用户管理指南
