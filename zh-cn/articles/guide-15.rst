=============================
用 SSO 和访问保护守护搜索平台
=============================

前言
====

企业内部的搜索平台汇集了受权限保护的文档。
许多项目的需求是：不给用户分发 Fess 专用的密码，而是让用户通过企业内部的身份提供方（IdP）登录，并按其所属的组筛选搜索结果。

本文在 Fess 15.9 中完成以下配置，并逐一确认其能够正常工作。

- 通过 Entra ID、OpenID Connect、SAML、SPNEGO 中的任一方式实现单点登录（SSO）
- 通过「需要登录」，禁止未登录的用户进行搜索
- 在终止 TLS 的反向代理之后，让 Fess 正确识别 HTTPS
- 重新审视访问令牌，以及审计日志和搜索日志的保留期限

如何设计角色和组，以及如何将其写入爬网配置的权限中，请参见 :doc:`guide-05`。

SSO 由插件提供
==============

在 Fess 15.9 中，SSO 的认证处理已从核心拆分为 4 个插件。

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - 方式
     - 插件
     - 「SSO Type」（``sso.type``）
     - 用户名的来源
     - 组和角色的来源
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID（``entraid``）
     - 已登录账户的用户名（通常为 UPN）
     - 通过 Microsoft Graph 获取的组和角色
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect（``oic``）
     - ID Token 的 ``email`` 声明
     - ID Token 的 ``groups`` 声明。角色仅来自「默认角色」
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML（``saml``）
     - 断言的 NameID
     - 「组属性名称」（默认为 ``memberOf``）和「角色属性名称」所指属性的值
   * - SPNEGO（Kerberos）
     - ``fess-sso-spnego``
     - SPNEGO（``spnego``）
     - Kerberos 主体中 ``@`` 之前的部分
     - 通过 [通用] 的 LDAP 设置获取的组

只有 OpenID Connect 的插件名（``oidc``）与 ``sso.type`` 的值（``oic``）不同。

无论哪种方式，步骤都相同。

1. 安装插件并重启 Fess
2. 在 IdP 一侧注册 Fess。返回地址（重定向 URI、ACS URL）为 ``https://<Fess主机>/sso/``
3. 在管理界面的 [系统] > [通用] 中，在对应方式的区域输入 IdP 的信息，选择「SSO Type」并更新
4. 在浏览器中打开 ``https://<Fess主机>/sso/``，确认能够经由 IdP 登录

安装插件
--------

Docker 镜像（``ghcr.io/codelibs/fess:15.9.0``）中包含 4 个 SSO 插件（名称带 ``-slim`` 的镜像中不包含）。
ZIP、DEB、RPM 版不附带这些插件，请通过 [系统] > [插件] 的 [安装] 进行安装，或使用以下命令安装。

::

    $ bin/fess-setup install plugin fess-sso-entraid

安装或删除插件后，请重启 Fess。
请使用与 Fess 相同次版本（15.9.x）的插件。

如果在没有插件的情况下选择「SSO Type」，``/sso/`` 只会返回登录页面，并且 ``fess.log`` 中会输出一次 ``No SSO authenticator is registered as ...`` 的 WARN。

设置的保存位置
--------------

在 [通用] 中输入的值保存在 ``system.properties`` 中（ZIP 版为 ``app/WEB-INF/conf/``，DEB、RPM 版为 ``/etc/fess/``）。
OpenID Connect、SAML、Entra ID 的项目在每次登录处理时都会被读取，因此保存后无需重启即可生效。
SPNEGO 的项目在整个进程中共享，因此修改后需要重启。

Docker 的 ``fess01`` 容器没有卷，执行 ``docker compose down`` 后再 ``up``，[通用] 中的设置就会丢失。
重新创建容器前，请从 [系统信息] > [备份] 下载 ``system.properties``，重新创建后再从同一页面上传以恢复设置。

使用 Entra ID 实现 SSO
======================

对于使用 Microsoft 365 的组织，``fess-sso-entraid`` 最为便捷。
组会在登录后从 Microsoft Graph 获取，因此无需在 IdP 一侧配置组声明。

Entra ID 一侧的设置
-------------------

在 Azure Portal 的「应用注册」中新建注册，并进行如下设置。

- 支持的帐户类型：仅此组织目录中的帐户
- 重定向 URI：平台选择「Web」，填写 ``https://fess.example.com/sso/``\ （包括末尾的 ``/`` 在内都要一致）
- 在「证书和密码」中创建客户端密钥并记下其值（仅在刚创建后显示）
- 在「API权限」中添加 Microsoft Graph 的委托的权限 ``User.Read`` 和 ``GroupMember.Read.All``，并授予管理员同意

如果没有 ``GroupMember.Read.All``，将无法获取嵌套的上级组，``fess.log`` 中会输出 ``Not allowed to read the parent groups of ...`` 的警告。

Fess 一侧的设置
---------------

在 [系统] > [通用] 的「Entra ID」区域中输入。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 项目
     - 键
     - 值
   * - 租户 (ID或域)
     - ``entraid.tenant``
     - 目录（租户）ID，或 ``yourcompany.onmicrosoft.com``
   * - 客户端ID
     - ``entraid.client.id``
     - 应用程序（客户端）ID
   * - 客户端密码
     - ``entraid.client.secret``
     - 所创建密钥的值
   * - 回复URL
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

最后，在「系统」区域的「SSO Type」中选择「Entra ID」，然后点击 [更新]。

让组与文档的权限保持一致
------------------------

对于从 Entra ID 获得的组和角色，其 ID（GUID）一定会成为权限。
此外，「权限字段」（``entraid.permission.fields``，默认为 ``mail``）中列出的属性值也会成为权限。

安全组未启用邮件，因此保持默认值时只有 GUID 会成为权限。
如果文件服务器的 ACL 是用组名编写的，请将「权限字段」设置为 ``mail,displayName``。
但 ``displayName`` 并不唯一，如果存在与 Windows 内置组（如 ``Administrators``）同名的组，它也会匹配该内置组的文档。

在爬网配置的权限中，将获取到的值原样加上 ``{group}`` 前缀填写（例如 ``{group}sales@example.com``）。

.. warning::

   「默认角色」（``entraid.default.roles``）会授予租户内的所有用户。
   如果在这里填入 ``admin``，所有人都将能够进入管理界面。

使用 OpenID Connect、SAML、SPNEGO 实现 SSO
==========================================

OpenID Connect
--------------

与 Keycloak、Okta 等 OpenID Connect 提供方集成时使用 ``fess-sso-oidc``。
在提供方一侧，将 Fess 注册为 Web 应用程序（客户端），并将重定向 URI 设置为 ``https://fess.example.com/sso/``。

在 [通用] 的「OpenID Connect」区域中需要输入的主要项目如下。

- 授权服务器URL（``oic.auth.server.url``）和令牌服务器URL（``oic.token.server.url``）：分别输入提供方 ``/.well-known/openid-configuration`` 中的值。令牌服务器URL 必须使用 ``https``\ （仅 ``localhost``、``127.x.x.x``、``::1`` 可以使用 ``http``）
- 客户端ID、客户端密码
- 范围：``openid email``。用户名取自 ``email`` 声明，因此必须包含 ``email``
- 基本URL（``oic.base.url``）：``https://fess.example.com``。如果将重定向URL 留空，则为 ``{基本URL}/sso/``

组方面，ID Token 中 ``groups`` 声明的值会原样成为权限。
不会像 Entra ID 那样追溯上级组，如果需要嵌套的组，请在提供方一侧将其包含在声明中。
角色不从声明中获取，只会授予「默认角色」的值。

用于验证签发者（``iss``）的 ``oic.issuer`` 在 [通用] 中没有对应项目，请直接写入 ``system.properties``。

SAML
----

使用 ``fess-sso-saml`` 时，Fess 作为 SP 运行。
IdP 通过跨站 POST 返回断言，因此保持默认的 ``tomcat.sameSiteCookies = lax`` 时登录无法完成。
请在 ``tomcat_config.properties`` 中做如下修改，然后重启 Fess。

::

    tomcat.sameSiteCookies = none

``none`` 只能在 HTTPS 下使用。
在 HTTP 下将无法登录，因此请先完成后文所述的 HTTPS 设置。

在 [通用] 的「SAML」区域中输入以下内容。

- SP基本URL（``saml.sp.base.url``）：``https://fess.example.com``。SP 的 Entity ID（``{SP基本URL}/sso/metadata``）和 ACS URL（``{SP基本URL}/sso/``）由此确定
- IdP实体ID、IdP SSO URL、IdP X.509证书：从 IdP 的管理界面抄写。证书去掉 ``-----BEGIN CERTIFICATE-----`` 这些行，将 Base64 内容写成一行填入
- 组属性名称（默认为 ``memberOf``）、角色属性名称：与 IdP 发送的属性名保持一致

没有读取 IdP 元数据 URL 的功能。
反过来，Fess 的 SP 元数据可以从 ``https://fess.example.com/sso/metadata`` 获取，并导入到 IdP 中。
用户名为 NameID，NameID 格式默认为电子邮件地址格式。
仅支持从 Fess 的 ``/sso/`` 开始的 SP-Initiated 登录，从 IdP 门户的磁贴开始的登录会被拒绝。

在生产环境中，请在 ``system.properties`` 中添加 ``saml.security.want_assertions_signed=true``，强制要求断言签名。
签名和加密的设置在 [通用] 中没有对应项目，也无法通过 JVM 系统属性指定，因此请直接写入文件。

.. warning::

   设置「角色属性名称」后，IdP 发送的值会原样成为 Fess 的角色。
   管理员角色为 ``authentication.admin.roles=admin``，因此 IdP 发送了 ``admin`` 的用户会成为管理员。

SPNEGO（Windows 集成认证）
--------------------------

要让已加入域的 Windows 无需输入密码即可登录，请使用 ``fess-sso-spnego``。
需要在 AD 中注册 SPN（``setspn -S HTTP/<Fess主机名> <服务账号>``），在 ``app/WEB-INF/classes/`` 中创建 ``krb5.conf`` 和 ``auth_login.conf``，并配置浏览器的内网设置。
组通过 [通用] 的「LDAP」区域的设置从 AD 获取。
请按照 `Windows集成认证SSO配置 <https://fess.codelibs.org/zh-cn/stable/config/sso-spnego.html>`__ 进行操作，修改 [通用] 中的 SPNEGO 项目后请重启。

确认 SSO 正常工作
=================

首先，在已注销的状态下打开 ``https://fess.example.com/sso/``，确认会跳转到 IdP 的登录页面。

登录后，在同一浏览器中打开 ``https://fess.example.com/api/v2/auth/me``。

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

确认 ``groups`` 中包含预期的组，以及 ``admin`` 是否符合预期。
在 Entra ID 中，组是在登录后获取的，因此刚登录时 ``permission_state`` 为 ``PENDING``，获取完成后变为 ``RESOLVED``。

审计日志 ``audit.log`` 中也会记录带有用户名和权限的 ``LOGIN`` 行。

登录失败时，会返回登录页面并显示“SSO登录处理失败。”。
原因会输出到 ``fess.log`` 的 WARN（如 ``Failed to process SSO login``）中。

即使 SSO 设置有误，也可以从 ``/login/`` 以本地 ``admin`` 用户登录并进行修正。

.. note::

   已登录的用户不会被授予 ``{role}guest``。
   仅带有默认 ``{role}guest`` 的爬网配置的文档，会从通过 SSO 登录的用户的搜索结果中消失。
   权限的组合方法请参见 :doc:`guide-05`。

禁止未登录的用户搜索
====================

在 [系统] > [通用] 中启用「需要登录」后，未登录的用户将无法搜索。

- 如果 SSO 可用（已安装插件且已选择「SSO Type」），打开内置 ``bootstrap`` 主题搜索页面的用户会被自动转到 ``/sso/``，在 IdP 登录后返回原来的搜索
- 没有 SSO 时，搜索页面上会显示登录对话框
- ``/api/v2/`` 的搜索 API 也将无法匿名使用，只有附带访问令牌的调用才能通过

即使不启用「需要登录」，只要 SSO 可用且启用了「显示登录链接」，搜索页面上登录链接的目标就会变为 ``/sso/``。

通过 HTTPS 公开
===============

在反向代理上终止 TLS
--------------------

在由 Nginx 等终止 TLS、再以 HTTP 转发给 Fess 的架构中，Fess 收到的请求看起来是 ``http://``。
这样一来，SAML 的断言验证（``Destination`` 的比对）会失败，SPNEGO 也不会提供 Basic 认证的回退。

请在 ``tomcat_config.properties`` 中告知 Fess 从外部看到的协议和端口。
该文件在 ZIP 版中位于 ``lib/classes/``，在 DEB、RPM 版和 Docker 镜像中位于 ``/etc/fess/``。

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

在代理一侧，请将 ``Host`` 头原样传给 Fess（Nginx 中为 ``proxy_set_header Host $host;``）。
这是因为 Fess 会根据 ``Host`` 头构建请求 URL 的主机名。

同时，请通过 ``fess_config.properties`` 的 ``session.cookie.secure=true`` 为会话 Cookie 添加 ``Secure`` 属性。
默认（空）时交由 Tomcat 判断，但在由代理终止 TLS 的生产环境中，请明确设置为 ``true``。
在 SAML 中使用 ``tomcat.sameSiteCookies = none`` 时，``SameSite=None`` 的 Cookie 同样需要 ``Secure`` 属性。

两个文件修改后都需要重启 Fess。

由 Fess 直接接收 TLS
--------------------

不使用代理时，请在 ``tomcat_config.properties`` 中设置 ``tomcat.SSLEnabled=true``、``tomcat.certificateKeystoreFile``、``tomcat.certificateKeystorePassword``、``tomcat.certificateKeyAlias`` 等。
配置示例请参见 `安全配置 <https://fess.codelibs.org/zh-cn/stable/install/security.html>`__。

关闭 OpenSearch 的端口
----------------------

docker-fess 的 ``compose-opensearch3.yaml`` 会在主机的 9200 端口上公开禁用了安全插件的 OpenSearch。
Fess 通过容器之间的网络（``http://search01:9200``）连接，因此在共享服务器上可以去掉 ``search01`` 的 ``ports``。

管理访问令牌
============

供业务系统调用 API 的令牌在 [系统] > [访问令牌] 中创建。
API 的调用方法请参见 :doc:`guide-11`，这里只列出安全运维的要点。

- 搜索用的令牌只授予该系统可以查看的文档的权限（例如 ``{group}sales``）
- 授予了 ``{role}admin-api`` 的令牌不仅能注册文档，还能使用 Admin API 的所有端点。不存在“仅注册”这样的窄权限
- 设置「过期」，到期后重新创建。不再需要的令牌请删除
- 令牌放在服务器一侧，不要嵌入在浏览器中运行的 JavaScript 里
- 「参数名称」保持为空。设置后，就可以通过 URL 参数追加权限
- 可以签发令牌的 ``admin-accesstoken`` 角色和可以显示令牌值的 ``admin-accesstoken-view`` 角色，应视同管理员对待

确定日志的保留期限
==================

日志文件的位置和监控请参见 :doc:`guide-10`。
这里整理用于安全审查的记录及其保留期限。

审计日志（``audit.log``）会逐行记录登录（``LOGIN``）、登录失败（``LOGIN_FAILURE``）、注销（``LOGOUT``）、对管理界面和 Admin API 的访问（``ACCESS``）、因权限不足而被拒绝（``ACCESS_DENIED``）等。
该文件在 ZIP 版中输出到 ``logs/``，在 DEB、RPM 版和 Docker 镜像中输出到 ``/var/log/fess/``，也可以从 [系统信息] > [日志文件] 下载。
默认格式为 LTSV，Docker 镜像中为 ECS 格式的 JSON。
轮转后的文件会在 360 天后删除（``log4j2.xml`` 中的 ``backup.audit.max.age``）。

谁搜索了什么，记录在保存于 OpenSearch 的搜索日志中，可以在 [系统信息] > [搜索日志] 中查看。
[通用] 中「删除以前的搜索日志」的默认值为 ``-1``，即不删除搜索日志而一直保留。
该天数同样适用于点击日志、收藏日志和聊天日志。
如果公司内部规定了保留期限，请输入该天数。

多台运行时
==========

Fess 15.9 的登录会话保存在各个 Fess 进程的内存中。
SSO 过程中使用的值（OpenID Connect 的 ``state`` 和 SAML 的 AuthnRequest ID）也保存在会话中，因此在负载均衡器后面部署多台时，请启用粘性会话，将同一用户始终分配到同一台 Fess。
多台架构本身请参见 :doc:`guide-14`。

另外，将会话保存到 OpenSearch 以在多台之间共享的功能，以及本地用户的通行密钥（Passkey）登录，都是 15.10 及以后版本的功能。

接下来阅读
==========

- 角色和组的设计，以及爬网配置中权限的写法：:doc:`guide-05`
- 使用访问令牌的 API 集成：:doc:`guide-11`
- 日志的位置、监控和备份：:doc:`guide-10`
- 扩展为多台架构：:doc:`guide-14`
- 将文件服务器的 ACL 反映到搜索结果中：:doc:`file-server-search`

参考资料
========

- `Microsoft Entra ID SSO配置 <https://fess.codelibs.org/zh-cn/stable/config/sso-entraid.html>`__
- `使用OpenID Connect进行SSO配置 <https://fess.codelibs.org/zh-cn/stable/config/sso-oidc.html>`__
- `SAML认证SSO配置 <https://fess.codelibs.org/zh-cn/stable/config/sso-saml.html>`__
- `Windows集成认证SSO配置 <https://fess.codelibs.org/zh-cn/stable/config/sso-spnego.html>`__
- `常规 <https://fess.codelibs.org/zh-cn/stable/admin/general-guide.html>`__
- `访问令牌 <https://fess.codelibs.org/zh-cn/stable/admin/accesstoken-guide.html>`__
- `安全配置 <https://fess.codelibs.org/zh-cn/stable/install/security.html>`__
- `日志配置 <https://fess.codelibs.org/zh-cn/stable/config/admin-logging.html>`__
