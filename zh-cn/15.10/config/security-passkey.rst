============================
通行密钥（WebAuthn）登录配置
============================

概述
====

|Fess|\ 允许本地用户（在管理界面「用户」中创建的用户）使用通行密钥（WebAuthn）代替密码登录。该功能自 15.10 起提供，默认关闭。

- 用户可以使用密码或通行密钥中的任意一种登录。这不是要求两者同时提供的多因素认证。
- 仅适用于 ``fess_user`` 索引中的本地用户。LDAP 或 SSO 用户无法注册通行密钥，使用通行密钥登录时也不会查询 LDAP。
- |Fess|\ 保存通行密钥的公钥和名称等信息。私钥保留在用户的认证器（浏览器、操作系统、安全密钥等）中，不会发送到\ |Fess|\ 。

配置
====

通行密钥的设置写在 ``fess_config.properties`` 中（ZIP 包为 ``app/WEB-INF/classes/fess_config.properties`` ，RPM/DEB 包为 ``/etc/fess/fess_config.properties`` ）。管理界面「系统」→「常规」中没有这些设置项，也不能在 ``system.properties`` 中设置。修改后需要重启\ |Fess|\ 才能生效。使用 Docker 时，可以在 ``FESS_JAVA_OPTS`` 中以 ``-Dfess.config.passkey.enabled=true`` 的形式传入（参见 :doc:`../install/install-docker` ）。

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - 键
     - 默认值
     - 说明
   * - ``passkey.enabled``
     - ``false``
     - 启用通行密钥登录。即使为 ``true`` ，如果下面的 ``passkey.rp.id`` 和 ``passkey.origins`` 没有可用的值，该功能仍保持关闭。
   * - ``passkey.rp.id``
     - （空）
     - 依赖方 ID：通行密钥所绑定的域名（例如 ``example.com`` ）。通行密钥只能在该主机及其子域名上使用。
   * - ``passkey.rp.name``
     - ``Fess``
     - 创建通行密钥时浏览器显示的依赖方名称。
   * - ``passkey.origins``
     - （空）
     - 接受通行密钥操作（ceremony）的来源（Origin，以逗号分隔，例如 ``https://fess.example.com`` ）。每一项都必须是带有主机名的 ``http`` 或 ``https`` 来源。

启用该功能的示例：
::

    passkey.enabled=true
    passkey.rp.id=example.com
    passkey.rp.name=Fess
    passkey.origins=https://fess.example.com

- ``passkey.rp.id`` 是所有通行密钥所绑定的域名。在用户已注册通行密钥之后更改它，会使所有通行密钥无法使用，用户必须在新的 ID 下重新注册，因此请一次选定。 ``passkey.origins`` 中每个来源的主机必须是 ``passkey.rp.id`` 或其子域名。
- ``passkey.origins`` 中按原样列出用户在浏览器中打开\ |Fess|\ 时使用的来源（协议、主机和端口），而不是反向代理后面的地址。来自其他来源的操作会被拒绝。

功能保持关闭的情况
------------------

即使设置了 ``passkey.enabled=true`` ，在下列情况下通行密钥也会\ **保持关闭，且画面上不会显示任何错误**\ 。登录画面不显示通行密钥按钮， ``/api/v2/auth/passkey`` 下的所有 API 都返回 ``404`` ， ``/api/v2/ui/config`` 的 ``features.passkey_enabled`` 为 ``false`` 。原因记录在 ``fess.log`` 的警告中，每条警告在启动后只输出一次。

- ``passkey.rp.id`` 或 ``passkey.origins`` 为空： ``passkey.enabled is true but passkey.rp.id or passkey.origins is empty, so passkeys are disabled.``
- ``passkey.origins`` 中没有任何条目： ``passkey.enabled is true but passkey.origins holds no origin, so passkeys are disabled.``
- ``passkey.origins`` 中有不是 ``http`` 或 ``https`` 来源的条目（没有主机名的值、其他协议等）： ``passkey.origins holds an entry that is not an http or https origin, so passkeys are disabled: entry=...``

``passkey.origins`` 本身可用，但用户打开的来源不在其中时，所有注册和登录都会被拒绝。用户的画面上不会显示原因，请查看 ``fess.log`` ： ``A passkey response came from an origin that is not in passkey.origins: origin=...`` 会显示被拒绝的来源和设置（只输出第一条）。请将该来源添加到 ``passkey.origins`` 。

使用方法
========

登录
----

启用通行密钥且浏览器支持 WebAuthn 时，搜索界面的登录以及管理界面的登录页面上会出现「使用通行密钥登录」按钮。浏览器会请求认证器，用户无需输入用户名即可登录。

通行密钥登录与密码登录使用相同的按 IP 地址的速率限制（ ``theme.api.login.*`` ）。失败会计入限制，成功则退还计数（参见 :doc:`rate-limiting` ）。画面不会告知失败的原因，而是显示与密码错误时相同的消息。

注册和删除通行密钥
------------------

本地用户可以在搜索界面用户菜单的「更改密码」（ ``/profile`` ）页面的「通行密钥」中，注册和删除自己的通行密钥。

1. 输入通行密钥的名称（最多 64 个字符）和当前密码，然后点击「注册通行密钥」。
2. 按照浏览器的提示，在认证器上创建通行密钥。

- 每次注册都需要当前密码。如果目录（LDAP）也接受某个本地用户的用户名和密码，则该用户无法注册通行密钥，因为密码检查无法确定验证的是哪个账户。
- 每个用户最多可以拥有 20 个通行密钥。
- 对于没有通行密钥且无法注册的用户（LDAP 或 SSO 用户，或不支持 WebAuthn 的浏览器），不显示「通行密钥」部分。
- 删除通行密钥会\ **结束该用户的其他登录会话**\ ，以免使用丢失的认证器打开的会话继续存在。其行为与更改密码相同（参见下文「与密码的关系」）。执行删除的会话会保留。

管理员操作
----------

管理界面「用户」→「用户」中用户的详情页面会列出该用户的通行密钥（标签、创建时间、最后使用时间）。管理员无法注册通行密钥，但拥有编辑权限的管理员可以通过「重置」删除通行密钥，例如用户丢失了认证器时。之后用户可以注册新的通行密钥。重置同样会结束该用户的登录会话（参见下文「与密码的关系」）。

将 ``passkey.enabled`` 改回 ``false`` 之后，已有通行密钥的用户的详情页面仍会列出它们，并且可以删除。关闭该功能不会删除通行密钥数据。

与密码的关系
============

- 通行密钥和密码是相互独立的凭据。更改用户的密码，或者由管理员设置新密码，都不会删除已注册的通行密钥，它们仍可用于登录。
- 密码被更改时，该用户的其他登录会话会结束（参见 :doc:`../install/security` ）。这也包括使用通行密钥打开的会话。每个会话最多每隔 ``password.changed.check.interval`` 秒（默认值 ``60`` ）检查一次，因此会话会在该时间内结束。
- 删除通行密钥时，其他会话同样会结束（见上文）。

删除和重命名用户
================

通行密钥仅通过用户名与用户绑定。为避免同名的其他用户继承通行密钥，在下列情况下也会删除通行密钥：

- 删除用户时。
- 创建用户时（删除该名称下遗留的所有通行密钥）。
- 重命名用户时（删除旧名称和新名称两者的通行密钥）。通行密钥不会随重命名而转移，因此用户需要重新注册。重命名为其他用户已使用的名称时，会在删除任何通行密钥之前被拒绝。

存储和备份
==========

通行密钥保存在 ``fess_user.passkey`` 索引中（前缀为 ``index.user.index`` ，默认值为 ``fess_user`` ）。即使通行密钥处于关闭状态，该索引也会在\ |Fess|\ 启动时创建，并在删除或重命名用户时以及用户详情页面中使用。如果不允许\ |Fess|\ 创建索引，请在升级之前创建它（参见 :ref:`upgrade-1510-passkey` ）。

该索引不属于 ``fess_user`` 别名，因此管理界面「备份」中的 ``fess_user.bulk`` 不包含通行密钥。从备份恢复之后，用户需要重新注册通行密钥。

要求
====

- **HTTPS**：浏览器只在安全上下文（HTTPS 或 ``localhost`` ）中允许使用 WebAuthn。\ |Fess|\ 也接受 ``passkey.origins`` 中的 ``http`` 来源，但在生产环境中，请通过 HTTPS 提供\ |Fess|\ 并指定 ``https://`` 来源（参见 :doc:`../install/security` 中的「启用 HTTPS」）。
- **浏览器**：需要提供 WebAuthn API（ ``PublicKeyCredential`` ）的浏览器。在不支持的浏览器中，登录按钮和注册部分都不会显示。
- **认证器**：必须支持可发现凭据（discoverable credentials）和用户验证（PIN、生物识别等）。\ |Fess|\ 要求同时具备这两项，支持 ES256 和 RS256 签名算法，并且不使用证明（attestation）。
- **多节点**：通行密钥操作的质询（challenge）在 HTTP 会话中保存 5 分钟。在负载均衡器后面运行多个节点时，请在节点之间共享会话（环境变量 ``FESS_SESSION_STORE=opensearch`` ），或者让负载均衡器将每个会话固定到一个节点。

API
===

通行密钥 API 位于 ``/api/v2/auth/passkey`` 下。通行密钥处于关闭状态时，所有 API 都返回 ``404`` 。 ``/api/v2/ui/config`` 的 ``features.passkey_enabled`` 表示该功能是否可用（参见 :doc:`../api/api-uiconfig` ）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 端点
     - 说明
   * - ``POST /api/v2/auth/passkey/login/options``
     - 获取登录选项（质询）。
   * - ``POST /api/v2/auth/passkey/login/verify``
     - 验证认证器的响应并登录。
   * - ``GET /api/v2/auth/passkey``
     - 列出已登录用户的通行密钥，并告知该用户是否可以注册（ ``can_register`` ）。
   * - ``POST /api/v2/auth/passkey/register/options``
     - 检查当前密码（ ``current_password`` ）并获取注册选项。
   * - ``POST /api/v2/auth/passkey/register/verify``
     - 验证名称（ ``label`` ）和认证器的响应，并注册通行密钥。
   * - ``DELETE /api/v2/auth/passkey/{credentialId}``
     - 删除已登录用户的一个通行密钥。

``register`` 调用和删除需要 ``X-Fess-CSRF-Token`` 请求头。两个登录调用与 ``/api/v2/auth/login`` 一样，不需要 CSRF 令牌。

故障排除
========

不显示通行密钥按钮
------------------

- 检查 ``/api/v2/ui/config`` 的 ``features.passkey_enabled`` 。如果为 ``false`` ，请在 ``fess.log`` 中查找警告，确认设置是否可用（参见上文「功能保持关闭的情况」）。
- 确认修改后已重启\ |Fess|\ 。
- 确认浏览器支持 WebAuthn，并且页面是通过 HTTPS（或 ``localhost`` ）打开的。
- 如果使用的不是内置主题，该主题必须支持通行密钥按钮。

注册或登录失败
--------------

- 如果 ``fess.log`` 中有包含 ``is not in passkey.origins`` 的警告，请将浏览器中打开的来源添加到 ``passkey.origins`` 。
- 更改 ``passkey.rp.id`` 之后，更改之前注册的通行密钥无法使用。请删除旧的通行密钥并重新注册。
