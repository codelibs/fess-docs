====================
SAML认证SSO配置
====================

概述
====

|Fess| 支持使用SAML（安全断言标记语言）2.0进行单点登录（SSO）认证。
通过使用SAML认证，由IdP（身份提供者）认证的用户信息可以与\ |Fess|\ 集成，结合基于角色的搜索功能，可以根据用户权限显示不同的搜索结果。

.. note::
   SAML认证的支持由 ``fess-sso-saml`` 插件提供，该插件不随发行包分发。请从管理界面的
   「系统 > 插件」页面安装，或执行 ``bin/fess-setup install plugin fess-sso-saml`` 。
   该插件使用SAML库 `saml4j <https://github.com/codelibs/saml4j>`__ 处理SAML消息。
   在安装之前，即使设置 ``sso.type=saml``\ ，对 ``/sso/`` 的请求也只会重定向回登录页面。

SAML认证的工作原理
------------------

在SAML认证中，|Fess|\ 作为SP（服务提供者）运行，并与外部IdP协作进行认证。

1. 用户访问\ |Fess|\ 的SSO端点（``/sso/``）
2. |Fess|\ 将认证请求重定向到IdP
3. 用户在IdP进行认证
4. IdP将SAML断言发送给\ |Fess|
5. |Fess|\ 验证断言并登录用户

.. note::
   仅支持如上所述从\ |Fess|\ 的SSO端点（``/sso/``）发起的SP发起（SP-Initiated）登录。
   |Fess|\ 会将每个SAML响应与自身发出的AuthnRequest的ID进行绑定校验，
   因此从IdP门户（如Okta仪表板或Microsoft Entra ID的"我的应用"）上的磁贴发起的
   IdP发起（IdP-Initiated，即未经请求的unsolicited）SSO没有可匹配的AuthnRequest，会被拒绝。
   如果要在IdP侧放置磁贴，请将其链接指向\ |Fess|\ 的\ ``/sso/``\ 端点。

   请注意，在15.7中，若设置了\ ``tomcat.sameSiteCookies=none``\ ，IdP发起的登录会碰巧可用：
   |Fess|\ 会将无法匹配的响应退回给IdP，而IdP会立即返回一个经过请求的断言。
   15.8不再执行这种退回，因此IdP发起的登录无法使用。

有关基于角色的搜索集成，请参阅:doc:`security-role`。

.. note::
   运行多个节点时，请设置环境变量 ``FESS_SESSION_STORE=opensearch`` 以在节点之间共享HTTP会话；这样在一个节点上发起的登录就可以在另一个节点上完成。启用之前，请将每个节点上的插件更新到15.10：15.9.0的插件不会共享登录状态，返回到另一个节点的用户会保持匿名。未共享会话时，请在负载均衡器上将每个会话固定到一个节点。关于共享的内容以及无法连接会话存储时的行为，请参阅 :doc:`session-store`。

   设置了 ``FESS_SESSION_STORE=opensearch`` 时，添加或删除 SSO 插件（ ``fess-sso-saml`` 、 ``fess-sso-oidc`` 、 ``fess-sso-entraid`` ）会改变已存储会话的格式版本。这样一来，所有已存储的会话都会失效，所有用户都必须重新登录。请在所有节点上安装或删除这些插件：这些插件的组合与其他节点不同的节点，无法读取其他节点存储的会话，其他节点也无法读取它的会话。存储、脚本、SPNEGO 等其他插件不会改变该格式。

前提条件
========

在配置SAML认证之前，请验证以下前提条件：

- 已安装\ |Fess| 15.10或更高版本
- 有可用的SAML 2.0兼容IdP（身份提供者）
- |Fess|\ 可通过HTTPS访问（生产环境必需）
- 您有权在IdP侧将\ |Fess|\ 注册为SP

支持的IdP示例：

- Microsoft Entra ID（Azure AD）
- Okta
- Google Workspace
- Keycloak
- OneLogin
- 其他SAML 2.0兼容IdP

基本配置
========

启用SSO
-------

要启用SAML认证，请在\ ``app/WEB-INF/conf/system.properties``\ 中添加以下设置：

::

    sso.type=saml

.. note::
   ``sso.type`` 及基本SAML设置（IdP信息、SP信息、用户属性映射）也可以从管理界面的"系统 > 全局"页面进行配置和更改。
   在管理界面中更改的设置将保存到 ``system.properties`` 中，重启后也会保留。
   但是，签名/加密等安全设置以及SP证书/私钥无法在管理界面中配置，因此请直接写入 ``system.properties``\ 。

.. note::
   以\ ``saml.``\ 开头的设置仅从\ ``system.properties``\ 中读取。
   通过JVM系统属性（如\ ``-Dsaml.security....``\ 或\ ``-Dfess.saml.security....``\ ）指定不会被读取。
   特别是\ ``saml.security.*``\ 在管理界面中也没有对应项，
   因此只能直接写入\ ``system.properties``\ 。

会话Cookie配置
--------------

IdP 通过 **跨站 POST** 将断言返回给 |Fess| 。``SameSite=Lax`` 的 Cookie 不会随此类请求发送，因此使用 |Fess| 附带的默认值时，SAML 登录无法完成。

请将 ``tomcat_config.properties`` 中的 ``tomcat.sameSiteCookies`` 改为 ``none`` 。该文件在 ZIP 软件包中位于 ``lib/classes/`` ，在 DEB/RPM 软件包中位于 ``/etc/fess/`` 。

::

    tomcat.sameSiteCookies = none

.. warning::
   浏览器仅对同时带有 ``Secure`` 属性的 Cookie 接受 ``none`` ，因此 |Fess| 必须通过 HTTPS 提供服务。在普通 HTTP 下，此设置会导致无法登录 |Fess| 。

.. note::
   默认值 ``lax`` 是为回调以重定向（GET）返回的 SSO 方式设定的。SAML 的 HTTP-POST 绑定不属于此类，因此仅在使用 SAML 时才需要修改。修改设置后需要重启 |Fess| 。

SP（服务提供者）配置
--------------------

要将\ |Fess|\ 配置为SP，请指定SP基础URL。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.sp.base.url``
     - SP基础URL
     - ``http://localhost:8080``

.. note::
   ``saml.sp.base.url`` 的默认值为 ``http://localhost:8080``\ 。
   在测试环境以外，请务必设置从外部访问 |Fess| 时使用的URL（生产环境中使用HTTPS）。

此设置会自动配置以下端点：

- **Entity ID**：``{saml.sp.base.url}/sso/metadata``
- **ACS URL**：``{saml.sp.base.url}/sso/``
- **SLO URL**：``{saml.sp.base.url}/sso/logout``

示例::

    saml.sp.base.url=https://fess.example.com

单独URL配置
~~~~~~~~~~~

通常情况下，设置 ``saml.sp.base.url`` 即可自动配置各端点URL，但如有需要，也可以使用以下属性明确指定各URL并进行覆盖。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.sp.entityid``
     - SP Entity ID
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - 断言消费者服务URL
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - 单点登出服务URL
     - ``{saml.sp.base.url}/sso/logout``

IdP（身份提供者）配置
---------------------

配置从您的IdP获取的信息。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.idp.entityid``
     - IdP Entity ID
     - （必需）
   * - ``saml.idp.single_sign_on_service.url``
     - IdP SSO服务URL
     - （必需）
   * - ``saml.idp.x509cert``
     - IdP签名X.509证书（Base64编码，无换行）
     - （必需）
   * - ``saml.idp.single_logout_service.url``
     - IdP SLO服务URL
     - （可选）
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - 额外的IdP签名证书（例如密钥轮换期间）
     - （可选）

.. note::
   IdP证书是签名验证唯一的信任锚点；消息内携带的证书一律不予信任。
   IdP和SP的证书必须是至少2048位的RSA密钥。
   设置了 ``saml.idp.x509certMulti.N`` 时，可以省略 ``saml.idp.x509cert``\ 。

.. note::
   对于\ ``saml.idp.x509cert``，仅指定证书的Base64编码内容，单行无换行。
   不要包含\ ``-----BEGIN CERTIFICATE-----``\ 和\ ``-----END CERTIFICATE-----``\ 行。

获取SP元数据
------------

启动\ |Fess|\ 后，您可以从\ ``/sso/metadata``\ 端点获取XML格式的SP元数据。

::

    https://fess.example.com/sso/metadata

将此元数据导入到您的IdP，或使用元数据内容在IdP侧手动注册SP。

.. note::
   要获取元数据，您必须先完成基本SAML配置（``sso.type=saml``\ 和\ ``saml.sp.base.url``）并启动\ |Fess|\ 。

IdP侧配置
=========

在IdP侧将\ |Fess|\ 注册为SP时，配置以下信息：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 设置
     - 值
   * - ACS URL / Reply URL
     - ``https://<Fess主机>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Fess主机>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``\ （推荐）

从IdP获取的信息
---------------

从您的IdP配置界面或元数据获取以下信息，用于\ |Fess|\ 配置：

- **IdP Entity ID**：标识IdP的URI
- **SSO URL（HTTP-Redirect）**：单点登录端点URL
- **X.509证书**：用于SAML断言签名验证的公钥证书

.. note::
   |Fess| 会对每个断言检查以下内容。这些URL由 ``saml.sp.base.url`` （或各个单独的URL属性）推导得出，而不是取自收到的请求。

   - 断言带有指明SP Entity ID的 ``AudienceRestriction``
   - 已签名Response的 ``Destination`` 以及SubjectConfirmation的 ``Recipient`` 是断言消费者服务URL

用户属性映射
============

您可以将从SAML断言获取的用户属性映射到\ |Fess|\ 的组和角色。

组属性配置
----------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.attribute.group.name``
     - 包含组信息的属性名
     - ``memberOf``
   * - ``saml.default.groups``
     - 默认组（逗号分隔）
     - （无）

示例::

    saml.attribute.group.name=groups
    saml.default.groups=user

.. note::
   |Fess| 直接使用断言中的组值，不会查询目录，也不会展开嵌套组（父组）。
   因此，是否包含父组完全取决于IdP侧的声明配置。
   这与通过Microsoft Graph API解析父组的 :doc:`sso-entraid` 不同。

角色属性配置
------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.attribute.role.name``
     - 包含角色信息的属性名
     - （无）
   * - ``saml.default.roles``
     - 默认角色（逗号分隔）
     - （无）

示例::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   如果无法从IdP获取属性，将使用默认值。
   使用基于角色的搜索时，请配置适当的组或角色。

.. warning::
   设置\ ``saml.attribute.role.name``\ 后，IdP发送的属性值将直接成为 |Fess| 的角色。
   由于\ ``fess_config.properties``\ 中\ ``authentication.admin.roles``\ 的默认值为\ ``admin``\ ，
   角色属性中包含\ ``admin``\ 的用户将获得 |Fess| 的管理员权限。
   请确认IdP侧可以控制角色属性的范围，必要时将\ ``authentication.admin.roles``\ 更改为其他名称。

属性名重复的 IdP
----------------

如果 IdP 将同一个属性名拆分到多个 ``<Attribute>`` 元素中发送，|Fess|\ 会合并它们的值。

Keycloak 默认发送这种形式的断言：除非启用其角色映射器和组映射器的 ``single`` 选项，否则每个值
都会输出为独立的 ``<Attribute>`` 元素，而每个 Keycloak 账户默认都带有多个领域角色。|Fess|\ 侧无需任何设置。

安全配置
========

以下安全设置从\ ``system.properties``\ 中读取。

.. note::
   如果保留了会削弱默认值的设置（配置了单点登出时的\ ``saml.security.want_logout_signed=false``\ 、
   ``saml.security.allow_deprecated_alg=true``\ 或\ ``saml.security.allow_rsa_1_5=true``\ ），
   在加载SAML设置时会向日志输出\ ``Insecure SAML settings: ...``\ 警告。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.session.end_with_idp``
     - IdP会话结束时，同时结束 |Fess| 的登录，结束时间为断言的 ``SessionNotOnOrAfter`` 加上 ``saml.security.clock_drift``。``false`` 表示关闭
     - ``true``

.. note::
   IdP不发送 ``SessionNotOnOrAfter`` 时，此设置不起作用。当IdP将其会话上限设为较短时间时（Keycloak的默认值为10小时），用户可能比以前更早被登出。在IdP处登出并不会在该时间之前结束 |Fess| 的登录。

签名设置
--------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.security.authnrequest_signed``
     - 对认证请求签名（需要 ``saml.sp.privatekey``）
     - ``false``
   * - ``saml.security.want_messages_signed``
     - 要求Response已签名
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - 要求Assertion已签名
     - ``false``
   * - ``saml.security.want_logout_signed``
     - 要求IdP发来的登出消息已签名
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - 接受SHA-1签名
     - ``false``
   * - ``saml.security.signature_algorithm``
     - 发出签名的算法：``rsa-sha256``、``rsa-sha384`` 或 ``rsa-sha512`` 的URI
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   无论这些设置如何，Response或Assertion都必须有一方已签名。
   请使用\ ``saml.security.want_messages_signed``\ 或\ ``saml.security.want_assertions_signed``\ ，要求IdP实际签名的元素带有签名。
   签名必须通过元素自身的ID引用被签名的元素，并使用\ ``rsa-sha256``\ 、\ ``rsa-sha384``\ 或\ ``rsa-sha512``\ （或ECDSA变体）。
   除非设置\ ``saml.security.allow_deprecated_alg=true``\ ，否则SHA-1签名会被拒绝，因此请确认IdP使用SHA-256或更强的算法签名。

.. note::
   配置单点登出（``saml.idp.single_logout_service.url``）时，IdP发送的LogoutRequest和
   LogoutResponse必须使用\ ``saml.idp.x509cert``\ 的密钥签名
   （默认为\ ``saml.security.want_logout_signed=true``\ ）。
   仅当IdP无法对其签名时，才设置\ ``saml.security.want_logout_signed=false``\ 。
   单点登出服务（``/sso/logout``）接受重定向绑定（GET）和POST绑定。
   请同时在IdP侧为POST绑定注册\ ``/sso/logout``\ URL；IdP向断言消费者服务POST的LogoutResponse不会被识别。

加密设置
--------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.security.want_assertions_encrypted``
     - 要求断言加密（需要 ``saml.sp.privatekey``）
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - 接受RSA 1.5密钥传输（需要 ``saml.sp.privatekey``）。否则仅接受OAEP
     - ``false``

.. note::
   除非IdP只能使用RSA 1.5加密，否则请将\ ``saml.security.allow_rsa_1_5``\ 保持为\ ``false``\ 。

SP证书与私钥配置
----------------

当SP对认证请求或登出消息进行签名时（例如 ``saml.security.authnrequest_signed``），或请求对断言或NameID进行加密时（例如 ``saml.security.want_assertions_encrypted``），需要配置SP的私钥（PKCS#8）和X.509证书。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.sp.x509cert``
     - SP的X.509证书（Base64编码，无换行）
     - （空）
   * - ``saml.sp.privatekey``
     - SP的私钥（Base64编码，无换行）
     - （空）

.. note::
   对于 ``saml.sp.x509cert`` 和 ``saml.sp.privatekey``，与 ``saml.idp.x509cert`` 相同，请将Base64编码的内容以单行无换行的形式指定（不包含 ``-----BEGIN ...-----`` 和 ``-----END ...-----`` 行）。
   启用签名/加密时，还需要在IdP侧注册SP证书。SP证书将包含在 ``/sso/metadata`` 的SP元数据中进行公开。

其他安全设置
------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.security.requested_authncontext``
     - 请求的认证上下文（留空则不请求）
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - 请求的认证上下文的比较方式（``exact``、``minimum``、``maximum`` 或 ``better``）
     - ``exact``
   * - ``saml.security.clock_drift``
     - 检查有效期时允许的时钟偏差（秒，0至600）
     - ``120``
   * - ``saml.security.max_message_size``
     - 接受的解码后消息的最大大小（字节，1024至16777216）
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - NameID格式
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   断言的Audience、Recipient、Destination、Issuer和有效期始终会被检查，
   并且响应必须是对\ |Fess|\ 发起的登录的应答。
   没有Audience或Audience不包含SP Entity ID的断言会被拒绝。
   验证始终是严格的：``saml.strict=false`` 会被拒绝。

不再使用的属性
--------------

以下属性会被忽略。日志中会输出一条列出它们名称的警告。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 属性
     - 现在
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1签名默认被拒绝；``saml.security.allow_deprecated_alg=true`` 可接受
   * - ``saml.security.allowed_key_transport_algorithms``
     - 默认仅接受OAEP；``saml.security.allow_rsa_1_5=true`` 可同时接受RSA 1.5
   * - ``saml.security.allow_duplicated_attribute_name``
     - 重复的属性始终会被合并
   * - ``saml.security.reject_missing_audience``
     - 没有Audience的断言始终会被拒绝
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - 请设置 ``saml.idp.x509cert``；指纹不是信任锚点
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``，以及 ``*.binding`` 和 ``*.response.url`` 属性
     - 不再使用

库不认识的其他 ``saml.`` 属性会使SAML登录中止，并给出指明该属性名称的消息，
以免拼写错误的安全设置被忽视。``saml.debug`` 会被接受，但没有任何效果。

AuthnRequest有效期
==================

|Fess|\ 每次访问\ ``/sso/``\ 都会向IdP发送一个AuthnRequest，并将其ID记录在会话中。
IdP返回的SAML响应会根据记录的ID进行校验。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.request.id.ttl``
     - 未收到响应的AuthnRequest的ID保留时长（秒）
     - ``3600``

记录的ID在超过该时长后会被丢弃。
如果超出有效期（例如IdP登录页面一直处于打开状态未处理），返回的断言将无法匹配，登录会当场失败一次。

配置示例
========

最小配置（用于测试）
--------------------

以下是在测试环境中进行验证的最小配置示例。

::

    # 启用SSO
    sso.type=saml

    # SP配置
    saml.sp.base.url=https://fess.example.com

    # IdP配置（设置从IdP管理控制台获取的值）
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...（Base64编码的证书）

    # 默认组
    saml.default.groups=user

推荐配置（用于生产）
--------------------

以下是生产环境的推荐配置示例。

::

    # 启用SSO
    sso.type=saml

    # SP配置
    saml.sp.base.url=https://fess.example.com

    # IdP配置
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...（Base64编码的证书）

    # 用户属性映射
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # 安全设置（生产环境推荐）
    # 要求IdP实际签名的元素带有签名
    # （对Response则设置 saml.security.want_messages_signed=true）
    saml.security.want_assertions_signed=true

故障排除
========

常见问题和解决方案
------------------

认证后无法返回Fess
~~~~~~~~~~~~~~~~~~

- 验证ACS URL是否在IdP侧正确配置
- 确保\ ``saml.sp.base.url``\ 的值与IdP配置匹配
- SAML断言以来自IdP的跨站POST方式发送。
  当\ ``tomcat_config.properties``\ 中的\ ``tomcat.sameSiteCookies``\ 为\ ``lax``\ （默认值）时，
  浏览器不会随该请求发送会话Cookie，登录会当场只失败一次。
  此时请设置\ ``tomcat.sameSiteCookies = none``\ （``SameSite=None``\ 需要HTTPS）
- 如果在IdP上的登录耗时过长，断言返回时AuthnRequest ID已经不存在，登录会当场只失败一次，需要重新开始登录
- |Fess| 未在\ ``app/WEB-INF/web.xml``\ 中设置\ ``session-timeout``\ ，因此采用Servlet容器的默认值30分钟。
  该值短于\ ``saml.request.id.ttl``\ 的3600秒，会话会先被丢弃，
  因此仅调大\ ``saml.request.id.ttl``\ 并不能延长用户在IdP完成登录的时间，还需要同时延长会话超时时间

Destination或Recipient验证失败
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

已签名Response的\ ``Destination``\ 和SubjectConfirmation的\ ``Recipient``\ 必须是\ |Fess|\ 的
断言消费者服务URL。该URL来自\ ``saml.sp.base.url``\ （或
``saml.sp.assertion_consumer_service.url``\ ），而不是到达\ |Fess|\ 的请求，因此
终结TLS的反向代理不会影响该比较。

- 将\ ``saml.sp.base.url``\ 设置为对外可见的URL，包括协议和端口
- 在IdP侧注册相同的ACS URL（``{saml.sp.base.url}/sso/``）
- 如果覆盖了\ ``saml.sp.entityid``\ ，IdP必须将该值用作Audience

签名验证错误
~~~~~~~~~~~~

- 验证IdP证书是否正确配置
- 确保证书未过期
- 证书应仅指定为Base64编码的内容，无换行
- IdP证书必须是至少2048位的RSA密钥
- Response或Assertion必须有一方已签名，且签名必须使用SHA-256或更强的算法
  （仅在设置\ ``saml.security.allow_deprecated_alg=true``\ 时才接受SHA-1）
- 响应被拒绝的原因会以\ ``Authentication failed: <reason> - <detail>``\ 的形式输出到日志

用户组/角色未生效
~~~~~~~~~~~~~~~~~

- 验证属性是否在IdP侧正确配置
- 确保\ ``saml.attribute.group.name``\ 的值与IdP发送的属性名匹配
- 使用Microsoft Entra ID时，除非选择了其他源属性，否则组声明的值为组的\ ``ObjectId``\ （GUID），与组名不一致
- 当用户所属的组超过150个时，Microsoft Entra ID将完全省略组声明（嵌套组也计入此上限），
  此时 |Fess| 将回退到\ ``saml.default.groups``
- 将属性名与IdP实际发送的断言中的属性名进行比较

日志设置
--------

当SAML认证失败时，原因始终会作为警告输出到日志中。
``saml.debug`` 属性没有任何效果。

要输出详细的SAML相关日志，请在 ``app/WEB-INF/classes/log4j2.xml`` 中添加以下logger：

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

参考
====

- :doc:`security-role` - 基于角色的搜索配置
- :doc:`sso-oidc` - 关于使用OpenID Connect进行SSO配置
- :doc:`sso-entraid` - 关于Microsoft Entra ID专用的SSO配置
