====================
SAML认证SSO配置
====================

概述
====

|Fess| 支持使用SAML（安全断言标记语言）2.0进行单点登录（SSO）认证。
通过使用SAML认证，由IdP（身份提供者）认证的用户信息可以与\ |Fess|\ 集成，结合基于角色的搜索功能，可以根据用户权限显示不同的搜索结果。

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

前提条件
========

在配置SAML认证之前，请验证以下前提条件：

- 已安装\ |Fess| 15.8或更高版本
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
   特别是\ ``saml.security.*``\ 、\ ``saml.strict``\ 和\ ``saml.debug``\ 在管理界面中也没有对应项，
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

安全配置
========

对于生产环境，建议启用以下安全设置。

.. note::
   如果保留了不推荐的设置，在加载SAML设置时会向日志输出\ ``Insecure SAML settings: ...``\ 警告。

签名设置
--------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.security.authnrequest_signed``
     - 对认证请求签名
     - ``false``
   * - ``saml.security.want_messages_signed``
     - 要求消息签名
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - 要求断言签名
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - 对登出请求签名
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - 对登出响应签名
     - ``false``
   * - ``saml.security.reject_deprecated_alg``
     - 拒绝SHA-1等已弃用的签名算法
     - ``false``

.. warning::
   安全功能默认是禁用的。
   对于生产环境，强烈建议至少设置\ ``saml.security.want_assertions_signed=true``\ 。

.. note::
   当\ ``saml.security.reject_deprecated_alg``\ 为\ ``false``\ 时，使用SHA-1（``rsa-sha1``\ 和\ ``dsa-sha1``\ ）
   签名的断言和消息同样会被接受。之所以默认不启用，是因为启用后会拒绝仍使用SHA-1签名的IdP。
   请先确认IdP使用SHA-256或更强的算法签名，然后再设置\ ``saml.security.reject_deprecated_alg=true``\ 。

.. warning::
   配置单点登出（``saml.idp.single_logout_service.url``）时，请务必同时设置\
   ``saml.security.want_messages_signed=true``\ 。
   若保持为\ ``false``\ ，则不会对\ ``/sso/logout``\ 收到的LogoutRequest要求签名。
   此时仅校验XML架构、``NotOnOrAfter``\ （若存在）、``Destination``\ （若存在）以及Issuer是否与\
   ``saml.idp.entityid``\ 一致（若存在）；LogoutRequest中的NameID从不与已登录用户进行比对。
   Issuer元素在SAML架构中是可选的，省略该元素的LogoutRequest从不会与IdP的实体ID进行比对。
   因此，攻击者无需知晓IdP的实体ID，即可构造未签名的LogoutRequest，
   诱导用户访问该URL，从而终止已认证用户的会话。
   其影响是强制登出（拒绝服务），而不是账户接管。

加密设置
--------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``saml.security.want_assertions_encrypted``
     - 要求断言加密
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - 要求NameID加密
     - ``false``

SP证书与私钥配置
----------------

当SP对认证请求或登出消息进行签名时（例如 ``saml.security.authnrequest_signed``），或请求对断言或NameID进行加密时（例如 ``saml.security.want_assertions_encrypted``），需要配置SP的私钥和X.509证书。

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
   * - ``saml.strict``
     - 严格模式（执行严格验证）
     - ``true``
   * - ``saml.security.want_xml_validation``
     - 验证消息的XML模式
     - ``true``
   * - ``saml.security.signature_algorithm``
     - 签名算法
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - 请求的认证上下文
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - NameID格式
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| 内部使用SAML库（java-saml），以 ``saml.`` 开头的属性将映射到该库对应的设置（``onelogin.saml2.`` 前缀）。
   因此，除此处列出的设置外，还可以在 ``system.properties`` 中指定绑定（例如 ``saml.sp.assertion_consumer_service.binding``）、组织信息（``saml.organization.*``）、联系人信息（``saml.contacts.*``）等详细设置。

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
如果未设置该值，将使用3600秒。
如果设置的值无法解析为数字，同样会使用3600秒，并在日志中输出以\ ``Invalid saml.request.id.ttl``\ 开头的警告。
如果设置的值小于或等于0，将会在登录从IdP返回之前就丢弃AuthnRequest的ID，因此同样会使用3600秒，并在日志中输出警告。

.. note::
   每个会话最多保留10个未收到响应的AuthnRequest，超出上限后将丢弃最旧的。
   这是为了支持同时从多个标签页发起登录，且无法通过\ ``saml.``\ 开头的设置进行更改。
   如果将上限覆盖为0或更小的值，则会改用10并输出警告。

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
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

    # 确认IdP使用SHA-256或更强的算法签名后再启用
    saml.security.reject_deprecated_alg=true

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
  浏览器不会随该请求发送会话Cookie，因此 |Fess| 找不到可匹配的AuthnRequest ID，当场只失败一次。
  浏览器会返回登录页面并显示"SSO登录处理失败。"，日志中会输出以\
  ``Received a SAML response with no matching AuthnRequest ID in the session``\ 开头的警告。
  此时请设置\ ``tomcat.sameSiteCookies = none``\ （``SameSite=None``\ 需要HTTPS）
- 如果在IdP上的登录耗时过长，断言返回时AuthnRequest ID已经不存在，登录会当场只失败一次，需要重新开始登录。
  输出哪条警告可以判断是什么超时了：以\
  ``Received a SAML response after the session it belongs to had expired``\ 开头的警告表示
  Servlet容器已经丢弃了整个会话；包含\ ``pending AuthnRequest ID(s) of the session had expired``\
  的警告表示会话仍然存在，只是\ ``saml.request.id.ttl``\ 超时。
  这两条警告都只在浏览器确实发送了会话Cookie时输出，这一点与上面的SameSite情形不同
- |Fess| 未在\ ``app/WEB-INF/web.xml``\ 中设置\ ``session-timeout``\ ，因此采用Servlet容器的默认值30分钟。
  该值短于\ ``saml.request.id.ttl``\ 的3600秒，会话及其保存的AuthnRequest ID会先被丢弃，
  因此仅调大\ ``saml.request.id.ttl``\ 并不能延长用户在IdP完成登录的时间，还需要同时延长会话超时时间。
  也正因如此，只有把TTL设置得比会话超时更短时，才会看到\ ``saml.request.id.ttl``\ 的警告

.. note::
   在15.7中，同样的情况会导致\ |Fess|\ 反复重定向到IdP，使登录陷入循环。
   15.8改为只失败一次而不再循环。配置层面的处理方法保持不变。

通过反向代理时Destination验证失败
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当\ |Fess|\ 运行在终结TLS的反向代理或负载均衡器之后时，
即使\ ``saml.sp.base.url``\ 设置正确，断言验证也可能失败。

原因在于SAML库将断言的\ ``Destination``\ 属性与Servlet容器重建的请求URL进行比较，
而不是与配置的ACS URL比较。当代理终结HTTPS时，\ |Fess|\ 看到的请求URL是形如\
``http://<内部主机名>:<内部端口>/sso/``\ 的内部地址，
与IdP发送的\ ``https://fess.example.com/sso/``\ 不一致。
``saml.sp.base.url``\ 不参与该比较，因此仅设置它无法解决问题。

设置\ ``saml.debug=true``\ 后，日志中会输出如下原因：

::

    The response was received at http://... instead of https://fess.example.com/sso/

此时请将\ ``tomcat_config.properties``\ 中的连接器设置调整为对外可见的协议和端口。
以下设置默认处于注释状态：

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

同时请配置反向代理，将原始的\ ``Host``\ 请求头透传给\ |Fess|\ ，
因为请求URL中的主机名部分是根据该请求头构建的。
修改\ ``tomcat_config.properties``\ 后需要重启\ |Fess|\ 。

同样的验证也适用于单点登出消息，因此使用SLO时请一并配置。

签名验证错误
~~~~~~~~~~~~

- 验证IdP证书是否正确配置
- 确保证书未过期
- 证书应仅指定为Base64编码的内容，无换行

用户组/角色未生效
~~~~~~~~~~~~~~~~~

- 验证属性是否在IdP侧正确配置
- 确保\ ``saml.attribute.group.name``\ 的值与IdP发送的属性名匹配
- 启用调试模式以检查SAML断言内容

调试设置
--------

要调查问题，您可以使用以下设置启用调试模式：

::

    saml.debug=true

设置 ``saml.debug=true`` 后，当SAML认证失败时，详细原因将输出到日志中。

此外，通过在 ``app/WEB-INF/classes/log4j2.xml`` 中添加以下logger，可以输出详细的SAML相关日志：

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

参考
====

- :doc:`security-role` - 基于角色的搜索配置
- :doc:`sso-oidc` - 关于使用OpenID Connect进行SSO配置
- :doc:`sso-entraid` - 关于Microsoft Entra ID专用的SSO配置
