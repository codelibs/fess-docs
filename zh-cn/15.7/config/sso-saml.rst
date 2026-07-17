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

有关基于角色的搜索集成，请参阅:doc:`security-role`。

前提条件
========

在配置SAML认证之前，请验证以下前提条件：

- 已安装\ |Fess| 15.7或更高版本
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

安全配置
========

对于生产环境，建议启用以下安全设置。

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

.. warning::
   安全功能默认是禁用的。
   对于生产环境，强烈建议至少设置\ ``saml.security.want_assertions_signed=true``\ 。

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

故障排除
========

常见问题和解决方案
------------------

认证后无法返回Fess
~~~~~~~~~~~~~~~~~~

- 验证ACS URL是否在IdP侧正确配置
- 确保\ ``saml.sp.base.url``\ 的值与IdP配置匹配

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
