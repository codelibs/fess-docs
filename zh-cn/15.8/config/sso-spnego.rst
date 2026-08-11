=================================
Windows集成认证SSO配置
=================================

概述
====

|Fess| 支持使用Windows集成认证（SPNEGO/Kerberos）进行单点登录（SSO）认证。
通过使用Windows集成认证，登录到Windows域计算机的用户可以无需额外的登录操作即可访问 |Fess|\ 。

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

- 已安装 |Fess| 15.8或更高版本
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
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

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

.. warning::
   使用 ``permitted_enctypes`` 中未列出的加密方式加密的服务票据，会被 Kerberos 接收端以
   ``encryption type not in permitted_enctypes list`` 拒绝。
   Active Directory 通常签发 AES256 服务票据，因此必须包含 AES256。

.. note::
   Java 17 及以后版本默认禁用 RC4（ ``rc4-hmac`` ）、3DES 和 DES，即使列出也不会使用，
   因此上例仅指定 AES。
   ``aes256-cts-hmac-sha384-192`` 和 ``aes128-cts-hmac-sha256-128`` 是 Windows Server 2025 支持的
   AES-SHA2（RFC 8009）加密方式。
   仅持有 RC4 密钥的服务账户无法用于 Kerberos 认证，请重置其密码以生成 AES 密钥。

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
   SPNEGO 在首次登录时初始化，因此即使缺少这些文件 |Fess| 本身仍能启动，但 SSO 登录会失败。

必需设置
--------

将以下设置添加到 ``app/WEB-INF/conf/system.properties``\ 。

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

.. note::
   如果 ``spnego.preauth.username`` 和 ``spnego.preauth.password`` 都留空，服务器端登录模块将使用 keytab。
   如果不希望将 AD 服务账户的密码保存在 |Fess| 的配置文件中，请创建 keytab 并按如下方式配置
   ``auth_login.conf`` 中的 ``spnego-server`` 。

   ::

       spnego-server {
           com.sun.security.auth.module.Krb5LoginModule required
           useKeyTab=true
           keyTab="/var/lib/fess/fess.keytab"
           principal="HTTP/fess-server.example.local@EXAMPLE.LOCAL"
           storeKey=true
           isInitiator=false;
       };

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
     - ``false``
   * - ``spnego.prompt.ntlm``
     - 收到NTLM令牌时回退到Basic认证
     - ``true``
   * - ``spnego.allow.localhost``
     - 允许localhost访问
     - ``false``
   * - ``spnego.allow.delegation``
     - 允许委托
     - ``false``
   * - ``spnego.allowed.realms``
     - 除服务器领域外还允许的 Kerberos 领域（逗号分隔）
     - （无）
   * - ``spnego.logger.level``
     - SPNEGO库内部日志级别（``1`` =FINEST、``2`` =FINER、``3`` =FINE、``4`` =CONFIG、``6`` =WARNING、``7`` =SEVERE。这些值以外的值（包括 ``0`` 和 ``5``）均视为INFO）
     - （自动）

.. warning::
   ``spnego.allow.unsecure.basic=true`` 可能通过未加密的连接发送Base64编码的凭据。
   对于生产环境，强烈建议将此设置为 ``false`` 并使用HTTPS。

.. note::
   当 ``spnego.allow.unsecure.basic=false`` （默认值）时，仅对 ``HttpServletRequest#isSecure()``
   返回 ``true`` 的请求提供 Basic 认证。
   如果在反向代理上终止 TLS 并以 HTTP 转发到 |Fess| ，该值为 ``false`` ，
   因此无法获取 Kerberos 票据而回退到 NTLM 的客户端将无法登录。
   请在 ``tomcat_config.properties`` 中设置 ``tomcat.secure=true`` ，以告知 |Fess| 该请求来自 HTTPS。

.. note::
   将 ``spnego.allow.delegation`` 设为 ``true`` 时，SPNEGO 库会接受客户端选择委托的 Kerberos 凭据，
   并将其关联到已认证的主体。但目前 |Fess| 并未在任何地方使用该凭据，爬取、搜索和 LDAP 查询都仅使用
   用户名。该设置对 SPNEGO 握手本身也没有影响：接受方凭据和 GSS 上下文标志保持不变，
   是否委托凭据完全由客户端决定（浏览器配置以及 Active Directory 中该账户是否被信任用于委托）。
   请保持默认值 ``false``\ ；启用后只会让 JDK 在每个已认证的请求上尝试受约束委托，而不会带来任何好处。

.. warning::
   在 |Fess| 15.8 中，如果客户端主体的领域与服务器的领域不同，登录将默认被拒绝。
   如果用户来自 AD 域树的子域或建立了信任关系的林，
   请在 ``spnego.allowed.realms`` 中以逗号分隔列出这些领域。
   否则，在 15.7 之前能够登录的用户将因 ``Kerberos realm is not allowed`` 而被拒绝。

.. warning::
   |Fess| 以主体中 ``@`` 之前的部分作为用户名，因此用户名中不包含领域。
   在 ``spnego.allowed.realms`` 中添加领域后，在多个领域中拥有相同账户名的用户
   （例如 ``alice@CORP.EXAMPLE.COM`` 与 ``alice@PARTNER.EXAMPLE.COM`` ）将被视为同一个
   |Fess| 用户，并共享该用户的组、角色和文档权限。
   仅当账户名在所列出的所有领域中都能唯一标识一个人时，才添加该领域。

.. note::
   允许列表同样适用于 Basic 认证的回退。如果用户输入 ``user@REALM`` 形式的名称，
   该领域将与 ``spnego.allowed.realms`` 进行比对，未被允许时将拒绝登录。
   单纯的账户名或 ``DOMAIN\user`` 形式不指定领域，因此在 ``krb5.conf`` 的默认领域中进行认证。
   由于 Basic 认证直接针对用户输入的领域进行认证，请将允许列表控制在最小范围；
   若将其作为安全边界使用，请考虑将 ``spnego.allow.basic`` 设为 ``false``\ 。

.. note::
   ``spnego.prompt.ntlm=true``\ （默认值）时，``spnego.allow.basic`` 也必须为 ``true``\ 。
   若要将 ``spnego.allow.basic`` 设为 ``false``，则必须同时将 ``spnego.prompt.ntlm`` 设为 ``false``\ 。
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
如果需要额外配置，通过组策略或注册表设置 ``AuthServerAllowlist``\ 。

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
        default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128
        permitted_enctypes   = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96 aes256-cts-hmac-sha384-192 aes128-cts-hmac-sha256-128

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
   设置 ``spnego.allow.basic=false`` 时，必须同时设置 ``spnego.prompt.ntlm=false``\ 。
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

登录返回 HTTP 400
~~~~~~~~~~~~~~~~~

对于所属组较多的用户，Kerberos 票据（PAC）会变大， ``Authorization`` 请求头可能超过 Tomcat 的
默认上限（8KB），从而返回 400。
此时请求不会到达 |Fess| ，日志中也不会有任何记录。
请在 ``tomcat_config.properties`` 中提高上限。

::

    tomcat.maxHttpHeaderSize=65536

更改服务账户密码后无法认证
~~~~~~~~~~~~~~~~~~~~~~~~~~

服务器凭据仅在首次登录时获取一次，之后会缓存到进程结束为止。
在 AD 中更改服务账户密码或替换 keytab 后，请重启 |Fess| 。
更改 ``spnego.*`` 设置后同样需要重启。

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
