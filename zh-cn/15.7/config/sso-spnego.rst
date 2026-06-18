=================================
Windows集成认证SSO配置
=================================

概述
====

|Fess| 支持使用Windows集成认证（SPNEGO/Kerberos）进行单点登录（SSO）认证。
通过使用Windows集成认证，登录到Windows域计算机的用户可以无需额外的登录操作即可访问 |Fess|。

Windows集成认证的工作原理
-------------------------

在Windows集成认证中，|Fess| 使用SPNEGO（简单和受保护的GSSAPI协商机制）协议进行Kerberos认证。

1. 用户登录到Windows域
2. 用户访问 |Fess|
3. |Fess| 发送SPNEGO质询
4. 浏览器获取Kerberos票证并发送到服务器
5. |Fess| 验证票证并获取用户名
6. 通过LDAP获取用户的组信息
7. 用户登录，组信息应用于基于角色的搜索

有关基于角色的搜索集成，请参阅 :doc:`security-role`。

前提条件
========

在配置Windows集成认证之前，请验证以下前提条件：

- 已安装 |Fess| 15.7或更高版本
- Active Directory（AD）服务器可用
- |Fess| 服务器可从AD域访问
- 您有权在AD中配置服务主体名称（SPN）
- 有用于通过LDAP获取用户信息的账户

Active Directory端配置
======================

注册服务主体名称（SPN）
-----------------------

您需要在Active Directory中为 |Fess| 注册SPN。
在加入AD域的Windows计算机上打开命令提示符，运行 ``setspn`` 命令。

::

    setspn -S HTTP/<Fess服务器主机名> <AD访问用户>

示例：

::

    setspn -S HTTP/fess-server.example.local svc_fess

验证注册：

::

    setspn -L <AD访问用户>

.. note::
   注册SPN后，如果在Fess服务器上执行了命令，请从Windows注销并重新登录。

基本配置
========

启用SSO
-------

要启用Windows集成认证，请在 ``app/WEB-INF/conf/system.properties`` 中添加以下设置：

::

    sso.type=spnego

Kerberos配置文件
----------------

创建 ``app/WEB-INF/classes/krb5.conf`` 并配置Kerberos设置。

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   将 ``EXAMPLE.LOCAL`` 替换为您的AD域名（大写），将 ``AD-SERVER.EXAMPLE.LOCAL`` 替换为您的AD服务器主机名。

登录配置文件
------------

创建 ``app/WEB-INF/classes/auth_login.conf`` 并配置JAAS登录设置。

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

.. note::
   ``krb5.conf`` 和 ``auth_login.conf`` 的默认文件名分别由 ``spnego.krb5.conf`` / ``spnego.login.conf`` 指定，但这两个文件本身必须事先创建好。
   如果这些文件不存在于类路径上，SPNEGO初始化将失败，|Fess| 将无法启动。

必需设置
--------

将以下设置添加到 ``app/WEB-INF/conf/system.properties``。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``spnego.preauth.username``
     - AD连接用户名
     - （必需）
   * - ``spnego.preauth.password``
     - AD连接密码
     - （必需）
   * - ``spnego.krb5.conf``
     - Kerberos配置文件路径
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - 登录配置文件路径
     - ``auth_login.conf``

可选设置
--------

可根据需要添加以下设置。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``spnego.login.client.module``
     - 客户端模块名称
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - 服务器模块名称
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - 允许Basic认证
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - 允许非安全Basic认证
     - ``true``
   * - ``spnego.prompt.ntlm``
     - 收到NTLM令牌时回退到Basic认证
     - ``true``
   * - ``spnego.allow.localhost``
     - 允许localhost访问
     - ``true``
   * - ``spnego.allow.delegation``
     - 允许委托
     - ``false``
   * - ``spnego.exclude.dirs``
     - 排除认证的目录（逗号分隔）
     - （无）
   * - ``spnego.logger.level``
     - SPNEGO库内部日志级别（``1`` =FINEST、``2`` =FINER、``3`` =FINE、``4`` =CONFIG、``6`` =WARNING、``7`` =SEVERE。这些值以外的值（包括 ``0`` 和 ``5``）均视为INFO）
     - （自动）

.. warning::
   ``spnego.allow.unsecure.basic=true`` 可能通过未加密的连接发送Base64编码的凭据。
   对于生产环境，强烈建议将此设置为 ``false`` 并使用HTTPS。

.. note::
   ``spnego.prompt.ntlm=true``（默认值）时，``spnego.allow.basic`` 也必须为 ``true``。
   若要将 ``spnego.allow.basic`` 设为 ``false``，则必须同时将 ``spnego.prompt.ntlm`` 设为 ``false``。
   不满足此条件时，SPNEGO初始化时将发生错误。

.. note::
   ``spnego.logger.level`` 控制SPNEGO库内部日志记录器（``java.util.logging`` 中名为 ``Spnego`` 的日志记录器）的日志级别。
   未设置时，将根据 |Fess| 的日志级别自动确定。

LDAP配置
========

需要LDAP配置来获取通过Windows集成认证进行身份验证的用户的组信息。
在 |Fess| 管理面板的"系统"→"常规"中配置LDAP设置。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 项目
     - 示例
   * - LDAP URL
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - 密码
     - AD访问用户的密码
   * - User DN
     - ``%s@example.local``
   * - 账户过滤器
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - memberOf属性
     - ``memberOf``

浏览器设置
==========

使用Windows集成认证需要客户端浏览器设置。

Internet Explorer / Microsoft Edge
----------------------------------

1. 打开Internet选项
2. 选择"安全"选项卡
3. 点击"本地Intranet"区域的"站点"
4. 点击"高级"并添加Fess的URL
5. 点击"本地Intranet"区域的"自定义级别"
6. 在"用户身份验证"→"登录"下，选择"仅在Intranet区域自动登录"
7. 在"高级"选项卡中，勾选"启用集成Windows身份验证"

Google Chrome
-------------

Chrome通常使用Windows Internet选项设置。
如果需要额外配置，通过组策略或注册表设置 ``AuthServerAllowlist``。

Mozilla Firefox
---------------

1. 在地址栏中输入 ``about:config``
2. 搜索 ``network.negotiate-auth.trusted-uris``
3. 设置Fess服务器URL或域（例如：``https://fess-server.example.local``）

配置示例
========

最小配置（用于测试）
--------------------

以下是测试环境中的最小配置示例。

``app/WEB-INF/conf/system.properties``:

::

    # 启用SSO
    sso.type=spnego

    # SPNEGO设置
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf``:

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf``:

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

推荐配置（用于生产）
--------------------

以下是生产环境的推荐配置示例。

``app/WEB-INF/conf/system.properties``:

::

    # 启用SSO
    sso.type=spnego

    # SPNEGO设置
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # 安全设置（生产环境）
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.prompt.ntlm=false
    spnego.allow.localhost=false

.. note::
   设置 ``spnego.allow.basic=false`` 时，必须同时设置 ``spnego.prompt.ntlm=false``。
   由于 ``spnego.prompt.ntlm`` 默认为 ``true``，省略此设置将导致初始化时发生错误。

故障排除
========

常见问题和解决方案
------------------

出现认证对话框
~~~~~~~~~~~~~~

- 验证Fess服务器是否已添加到浏览器设置中的本地Intranet区域
- 检查"启用集成Windows身份验证"是否已启用
- 验证SPN是否正确注册（ ``setspn -L <用户名>`` ）

发生认证错误
~~~~~~~~~~~~

- 验证 ``krb5.conf`` 中的域名（大写）和AD服务器名称是否正确
- 检查 ``spnego.preauth.username`` 和 ``spnego.preauth.password`` 是否正确
- 验证与AD服务器的网络连接

无法获取组信息
~~~~~~~~~~~~~~

- 验证LDAP设置是否正确
- 检查Bind DN和密码是否正确
- 验证用户是否在AD中属于组

调试设置
--------

要调查问题，可以输出SPNEGO相关的详细日志。

要输出SPNEGO库内部的详细日志，请在 ``app/WEB-INF/conf/system.properties`` 中添加以下内容。
``spnego.logger.level=1`` 将输出最详细的日志（FINEST）。

::

    spnego.logger.level=1

要输出 |Fess| 侧SPNEGO联动处理（``org.codelibs.fess.sso.spnego`` 包）的详细日志，请在 ``app/WEB-INF/classes/log4j2.xml`` 中添加以下日志记录器。

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>

.. note::
   SPNEGO库本身的日志通过 ``java.util.logging`` 输出，因此通过 ``spnego.logger.level`` 而非 ``log4j2.xml`` 进行控制。
   |Fess| 侧联动处理的日志通过 ``log4j2.xml`` 中的日志记录器进行控制。

参考信息
========

- :doc:`security-role` - 基于角色的搜索配置
- :doc:`sso-saml` - SAML认证SSO配置
- :doc:`sso-oidc` - OpenID Connect认证SSO配置
- :doc:`sso-entraid` - Microsoft Entra ID SSO配置
