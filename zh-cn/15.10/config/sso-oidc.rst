=====================================
使用OpenID Connect进行SSO配置
=====================================

概述
====

|Fess| 支持使用OpenID Connect（OIDC）进行单点登录（SSO）认证。
OpenID Connect是基于OAuth 2.0的认证协议，使用ID Token（JWT）进行用户认证。
通过使用OpenID Connect认证，由OpenID提供者（OP）认证的用户信息可以与 |Fess| 集成。

.. note::
   OpenID Connect认证的支持由 ``fess-sso-oidc`` 插件提供，该插件不随发行包分发。请从管理
   界面的「系统 > 插件」页面安装，或执行 ``bin/fess-setup install plugin fess-sso-oidc`` 。
   插件名为 ``fess-sso-oidc``\ ，而 ``sso.type`` 的取值仍为 ``oic``\ 。
   在安装之前，即使设置 ``sso.type=oic``\ ，对 ``/sso/`` 的请求也只会重定向回登录页面。

OpenID Connect认证的工作原理
----------------------------

在OpenID Connect认证中，|Fess| 作为依赖方（RP）运行，并与外部OpenID提供者（OP）协作进行认证。

1. 用户访问 |Fess| 的SSO端点（``/sso/``）
2. |Fess| 将请求重定向到OP的授权端点
3. 用户在OP进行认证
4. OP将授权码重定向到 |Fess|
5. |Fess| 使用授权码从令牌端点获取ID Token
6. |Fess| 校验ID Token（JWT）中的声明，获取用户信息并登录用户

.. note::
   |Fess| 使用授权码流程（Authorization Code Flow）。ID Token不经过浏览器，而是通过 |Fess| 与OP之间的后端通道（服务器间通信）直接从令牌端点获取。
   |Fess| 通过解码ID Token来提取声明（如 ``email`` 和 ``groups``）以构建用户信息，但不对JWT签名进行密码学验证。由于令牌是通过TLS直接从令牌端点接收的，OpenID Connect Core允许这样做，因此令牌端点URL（``oic.token.server.url``）必须为HTTPS。只有 ``localhost``、``127.x.x.x`` 和 ``::1`` 可以使用 ``http``。
   |Fess| 会校验声明：``aud`` 必须包含 ``oic.client.id``\ （``azp`` 存在时也必须与其一致），``exp`` 必须存在且尚未过期（允许最多300秒的时钟偏差），设置了 ``oic.issuer`` 时 ``iss`` 必须与其一致。未设置 ``oic.issuer`` 时不校验 ``iss``，并会在每次启动后的首次登录时记录一条警告。每次授权请求都会发送 ``nonce``，ID Token 中的 ``nonce`` 声明必须与其一致；缺少该声明或值不同的令牌会被拒绝。不返回 ``nonce`` 的OP无法使用，也没有关闭此校验的设置。默认使用PKCE（S256）：每个授权请求都带有 ``code_challenge``，令牌请求会发送 ``code_verifier``。仅当OP拒绝PKCE时，才在 ``system.properties`` 中设置 ``oic.pkce=false``（管理画面中没有对应的项目；每次登录都会读取该键，因此无需重启）。不校验 ``iat`` 和 ``nbf``。

有关基于角色的搜索集成，请参阅 :doc:`security-role`。

.. note::
   即使 OP 签发的令牌过期，|Fess| 的登录会话也不会结束。|Fess| 只在用户登录时检查 ID 令牌的 ``exp`` ，令牌的有效期不用于会话。未设置 ``oic.jwks.uri`` 时，登录会一直持续到用户退出登录或达到会话超时为止。要在用户于OP端登出时结束 |Fess| 的会话，请设置 `后端通道登出`_ 。SAML 则不同：其会话随 IdP 会话一起结束（参见 :doc:`sso-saml` ）。

.. note::
   运行多个节点时，请设置环境变量 ``FESS_SESSION_STORE=opensearch`` 以在节点之间共享HTTP会话；这样在一个节点上发起的登录就可以在另一个节点上完成。启用之前，请将每个节点上的插件更新到15.10：15.9.0的插件不会共享登录状态，返回到另一个节点的用户会保持匿名。未共享会话时，请在负载均衡器上将每个会话固定到一个节点。

   设置了 ``FESS_SESSION_STORE=opensearch`` 时，添加或删除 SSO 插件（ ``fess-sso-saml`` 、 ``fess-sso-oidc`` 、 ``fess-sso-entraid`` ）会改变已存储会话的格式版本。这样一来，所有已存储的会话都会失效，所有用户都必须重新登录。请在所有节点上安装或删除这些插件：这些插件的组合与其他节点不同的节点，无法读取其他节点存储的会话，其他节点也无法读取它的会话。存储、脚本、SPNEGO 等其他插件不会改变该格式。

前提条件
========

在配置OpenID Connect认证之前，请验证以下前提条件：

- 已安装 |Fess| 15.10或更高版本
- 有可用的OpenID Connect兼容提供者（OP）
- |Fess| 可通过HTTPS访问（生产环境必需）
- 您有权在OP侧将 |Fess| 注册为客户端（RP）

支持的提供者示例：

- Microsoft Entra ID（Azure AD）
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- 其他OpenID Connect兼容提供者

基本配置
========

启用SSO功能
-----------

要启用OpenID Connect认证，请在 ``app/WEB-INF/conf/system.properties`` 中添加以下设置：

::

    sso.type=oic

.. note::
   ``sso.type`` 以及后文说明的各项 ``oic.*`` 设置（``oic.issuer`` 和 ``oic.jwks.uri`` 除外），也可以通过管理画面的"系统 > 全局"页面进行设置和修改。
   在管理画面中修改的设置将保存到 ``system.properties``，重启后仍会保留。
   ``oic.issuer`` 和 ``oic.jwks.uri`` 只能在 ``system.properties`` 中设置。

提供者配置
----------

配置从OP获取的信息。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``oic.auth.server.url``
     - 授权端点URL
     - ``https://accounts.google.com/o/oauth2/auth``
   * - ``oic.token.server.url``
     - 令牌端点URL
     - ``https://accounts.google.com/o/oauth2/token``
   * - ``oic.issuer``
     - 颁发者标识符（可选）。设置后，ID Token的 ``iss`` 声明必须与其完全一致（末尾的斜杠也会区分）
     - (空字符串：不校验 ``iss``)
   * - ``oic.jwks.uri``
     - OP的 ``jwks_uri`` （可选）。设置后启用后端通道登出（参见 `后端通道登出`_ ）
     - (空字符串：不使用后端通道登出)

.. note::
   这些URL和颁发者可以从OP的Discovery端点（``/.well-known/openid-configuration``）获取，颁发者即其中的 ``issuer`` 值。
   令牌端点URL（``oic.token.server.url``）必须为HTTPS。只有当主机是 ``localhost`` （不区分大小写）、形如 ``127.x.x.x`` 的IPv4地址或 ``::1`` 时，才允许使用 ``http``。主机按字面字符串比较，不会进行名称解析，因此Docker Compose的服务名（如 ``http://keycloak:8080/...``）或内部主机名即使指向同一台机器，使用 ``http`` 也会被拒绝。

   此检查只针对令牌端点，不针对授权端点（``oic.auth.server.url``）。检查在登录时进行，而不是在启动时。设置 ``oic.issuer`` 不会放宽这一规则，只是启用对 ``iss`` 声明的校验。

客户端配置
----------

配置在OP侧注册的客户端信息。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``oic.client.id``
     - 客户端ID
     - (空字符串)
   * - ``oic.client.secret``
     - 客户端密钥
     - (空字符串)
   * - ``oic.scope``
     - 请求的范围
     - (空字符串)

.. note::
   范围必须至少包含 ``openid``\ 。
   要获取用户的电子邮件地址，请指定 ``openid email``\ 。

重定向URL配置
-------------

配置认证后的回调URL。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``oic.redirect.url``
     - 重定向URL（回调URL）
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - |Fess| 的基础URL
     - ``http://localhost:8080``

.. note::
   如果省略 ``oic.redirect.url``，它将从 ``oic.base.url`` 自动构建。
   对于生产环境，请将 ``oic.base.url`` 设置为HTTPS的URL。

.. warning::
   “省略”是指该键根本不存在。在管理画面的“系统 > 全局”页面中将 ``oic.redirect.url`` 留空保存时，该键会被删除，因此会使用 ``{oic.base.url}/sso/``。相反，在 ``system.properties`` 中手写 ``oic.redirect.url=``\ （仅值为空）则不是省略，而是空值，授权请求会带上一个没有值的 ``redirect_uri`` 参数。它与在OP中注册的重定向URI不一致，因此会被OP拒绝，导致无法登录。请指定一个值，或删除该行。

用户属性配置
------------

配置分配给通过OIDC认证的用户的默认组和角色。
用户ID、组和角色分别按如下方式确定：

- **用户ID**：从ID Token（JWT）的 ``email`` 声明中获取。因此，范围中实际上必须包含 ``email``\ （如果无法获取 ``email`` 声明，登录将无法正常完成）。
- **组**：从ID Token的 ``groups`` 声明中获取。如果 ``groups`` 声明不存在，则使用 ``oic.default.groups`` 的值。如果 ``groups`` 声明是空数组，则视为存在，因此不会使用 ``oic.default.groups``，该用户将被视为没有任何组。
- **角色**：始终使用 ``oic.default.roles`` 的值（不存在从ID Token声明中获取角色的机制）。

.. note::
   |Fess| 直接使用 ``groups`` 声明中的值，不会查询目录，也不会展开嵌套组（父组）。
   因此，是否包含父组完全取决于OP侧的声明配置。
   这与通过Microsoft Graph API解析父组的 :doc:`sso-entraid` 不同。
   声明的值会原样成为检索权限。如果OP侧配置为输出组的完整路径，
   则会发送 ``/父组/子组`` 这样的值并原样成为权限名称，与仅标记了组名的文档不匹配。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``oic.default.groups``
     - 默认组（逗号分隔）
     - (空字符串)
   * - ``oic.default.roles``
     - 默认角色（逗号分隔）
     - (空字符串)

.. note::
   使用基于角色的搜索时，需要为用户分配适当的组或角色。
   详情请参阅 :doc:`security-role`。

OP侧配置
========

在OP侧将 |Fess| 注册为客户端（RP）时，请配置以下信息：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 设置项目
     - 设置值
   * - 应用程序类型
     - Web应用程序
   * - 重定向URI / 回调URL
     - ``https://<Fess主机>/sso/``
   * - 允许的范围
     - ``openid`` 以及所需的范围（``email``、``profile`` 等）

从OP获取的信息
--------------

从OP的配置界面或Discovery端点获取以下信息，用于 |Fess| 的配置：

- **授权端点（Authorization Endpoint）**：启动用户认证的URL
- **令牌端点（Token Endpoint）**：获取令牌的URL
- **颁发者（Issuer）**：可选。Discovery文档中的 ``issuer`` 值，用于 ``oic.issuer``
- **客户端ID**：OP颁发的客户端标识符
- **客户端密钥**：用于客户端认证的密钥

.. note::
   大多数OP允许您从Discovery端点（``https://<OP>/.well-known/openid-configuration``）
   确认授权端点和令牌端点的URL。

后端通道登出
============

使用 `OpenID Connect Back-Channel Logout 1.0 <https://openid.net/specs/openid-connect-backchannel-1_0.html>`__ 时，登录在OP端结束后，OP会通过服务器之间的通信通知 |Fess| ，|Fess| 随即结束该登录的会话。
不使用此功能时，即使在OP端登出，|Fess| 的会话也会继续存在。

启用
----

在 ``app/WEB-INF/conf/system.properties`` 中设置OP的 ``jwks_uri`` 。设置后即启用后端通道登出，无需切换其他设置。

::

    oic.jwks.uri=https://op.example.com/jwks

- ``oic.jwks.uri`` 只能在 ``system.properties`` 中设置（管理画面中没有对应的项目）。
- 登出令牌要根据 ``oic.issuer`` 和 ``oic.client.id`` 进行校验，因此这两项也必须设置。任意一项为空时，所有登出请求都会被拒绝。
- ``oic.jwks.uri`` 必须为HTTPS。与令牌端点相同，只有当主机是 ``localhost`` 、 ``127.x.x.x`` 或 ``::1`` 时才允许使用 ``http`` 。此检查在收到登出请求并获取密钥时进行，不满足条件时请求会被拒绝。
- ``jwks_uri`` 和 ``issuer`` 可以从OP的Discovery端点（ ``/.well-known/openid-configuration`` ）获取。OP是否支持此功能，可以通过同一文档中的 ``backchannel_logout_supported`` 确认。

在OP端注册
----------

- 在OP的客户端设置中，将 ``https://<Fess主机>/sso/logout`` 注册为后端通道登出URL。
- 如果OP提供该选项（ ``backchannel_logout_session_required`` ），请让OP在登出令牌中包含会话ID（ ``sid`` ）。包含 ``sid`` 时，只结束对应的一个会话，而不是该用户的所有会话。登录时签发的ID Token中也必须包含相同的 ``sid`` 。

行为
----

- OP向 ``/sso/logout`` POST ``logout_token`` 参数。|Fess| 在记录登出成功时返回 ``200`` ，否则返回 ``400`` ，两种响应都带有 ``Cache-Control: no-store`` 。
- 登出令牌的校验内容包括：签名（使用 ``jwks_uri`` 文档中的密钥，算法为RS256、RS384、RS512、ES256、ES384或ES512）、 ``iss`` （ ``oic.issuer`` ）、 ``aud`` （ ``oic.client.id`` ）、 ``iat`` 和 ``exp`` （与ID Token相同，允许最多300秒的时钟偏差；签发时间超过1小时的令牌会被拒绝）、 ``jti`` 、 ``events`` 、不含 ``nonce`` 、含有 ``sid`` 或 ``sub`` 。校验失败的令牌和已经接受过的令牌（相同的 ``jti`` ）会以 ``400`` 被拒绝，会话不会结束。未设置 ``oic.jwks.uri`` 时，所有登出请求也都会以 ``400`` 被拒绝。
- 令牌包含 ``sid`` 时，只结束具有该 ``sid`` 的登录的会话。令牌只包含 ``sub`` 时，该用户在 |Fess| 收到请求之前开始的所有会话都会结束。ID Token中没有 ``sid`` 的登录，不会被包含 ``sid`` 的令牌结束。
- 会话在下一次被使用时结束，该请求按未登录处理。不会向OP发送登出，只结束 |Fess| 的会话。审计日志会记录 ``reason`` 为 ``idp_session_ended`` 的 ``SESSION_END`` （参见 :doc:`../install/security` ）。
- 登出记录在搜索引擎的协调器索引（ ``fess_config.coordinator`` ）中，所有节点都会读取它。因此，运行多个节点时，无论是否通过 ``FESS_SESSION_STORE=opensearch`` 共享HTTP会话，此功能都能工作。在收到请求的节点上，会话会在下一次请求时立即结束。其他节点最多每30秒检查一次记录，因此在请求之后，会话在这些节点上最多可能继续存在30秒。
- 无法读取协调器索引时，不会结束任何会话（记录一次警告）。令牌只包含 ``sub`` 时，可能会将登录时间与其他节点收到请求的时间进行比较，因此请保持各节点的时钟同步。
- 被拒绝的请求按种类只将第一次记录为警告，之后的以DEBUG级别记录。令牌、 ``sid`` 和 ``sub`` 不会被记录到日志中。
- 不支持加密的登出令牌（JWE）和前端通道登出。

配置示例
========

最小配置（用于验证环境）
------------------------

以下是在验证环境中进行功能确认的最小配置示例。

::

    # 启用SSO
    sso.type=oic

    # 提供者配置（设置从OP获取的值）
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # 客户端配置
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # 重定向URL（验证环境）
    oic.redirect.url=http://localhost:8080/sso/

推荐配置（用于生产环境）
------------------------

以下是在生产环境中使用的推荐配置示例。

::

    # 启用SSO
    sso.type=oic

    # 提供者配置
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # 颁发者（Discovery文档中的"issuer"值）
    oic.issuer=https://op.example.com

    # 客户端配置
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # 基础URL（生产环境使用HTTPS）
    oic.base.url=https://fess.example.com

故障排除
========

常见问题和解决方案
------------------

认证后无法返回 |Fess|
~~~~~~~~~~~~~~~~~~~~~

- 请确认OP侧的重定向URI是否正确配置
- 请确认 ``oic.redirect.url`` 或 ``oic.base.url`` 的值是否与OP侧的配置一致
- 请确认协议（HTTP/HTTPS）是否一致

发生认证错误
~~~~~~~~~~~~

- 请确认客户端ID和客户端密钥是否正确配置
- 请确认范围中是否包含 ``openid``
- 请确认授权端点URL和令牌端点URL是否正确
- 如果登录失败，``fess.log`` 中会记录以 ``Failed to process the OpenID Connect callback:`` 开头的警告，后面跟着原因
- ``The ID token was not issued for this client``：ID Token的 ``aud`` 不是 ``oic.client.id``，请确认客户端ID
- ``The ID token has expired``：|Fess| 主机与OP的时钟相差超过300秒，请同步时间（NTP）
- ``The ID token was not issued by the configured issuer``：``oic.issuer`` 与消息中显示的 ``iss`` 不同，请原样复制Discovery文档中的 ``issuer`` 值
- ``oic.token.server.url must be https``：请使用HTTPS的令牌端点URL（只有 ``localhost``、``127.x.x.x`` 和 ``::1`` 可以使用 ``http``；指向Docker Compose服务名或内部主机名的 ``http`` 也会被拒绝）

无法获取用户信息
~~~~~~~~~~~~~~~~

- 请确认范围中是否包含所需的权限（``email``、``profile`` 等）
- 请确认OP侧是否为客户端允许了所需的范围
- 使用Microsoft Entra ID时，除非选择了其他源属性，否则\ ``groups``\ 声明的值为组的\ ``ObjectId``\ （GUID），与组名不一致
- 当用户所属的组超过200个时，Microsoft Entra ID将完全省略\ ``groups``\ 声明（嵌套组也计入此上限），
  此时 |Fess| 将回退到\ ``oic.default.groups``

调试设置
--------

要调查问题，可以通过调整 |Fess| 的日志级别来输出OpenID Connect相关的详细日志。

在 ``app/WEB-INF/classes/log4j2.xml`` 中，可以添加以下日志记录器来更改日志级别：

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

.. warning::
   将该日志记录器设置为DEBUG后，ID Token的声明（如 ``email`` 和 ``groups``）会被写入日志文件。
   调查结束后请将日志级别恢复原状，并谨慎处理输出的日志。

参考信息
========

- :doc:`security-role` - 基于角色的搜索配置
- :doc:`sso-saml` - 使用SAML认证进行SSO配置
- :doc:`sso-entraid` - Microsoft Entra ID专用的SSO配置（使用Entra ID时，也可以使用专用配置代替通用的OpenID Connect配置）
