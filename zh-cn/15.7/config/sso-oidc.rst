=====================================
使用OpenID Connect进行SSO配置
=====================================

概述
====

|Fess| 支持使用OpenID Connect（OIDC）进行单点登录（SSO）认证。
OpenID Connect是基于OAuth 2.0的认证协议，使用ID Token（JWT）进行用户认证。
通过使用OpenID Connect认证，由OpenID提供者（OP）认证的用户信息可以与 |Fess| 集成。

OpenID Connect认证的工作原理
----------------------------

在OpenID Connect认证中，|Fess| 作为依赖方（RP）运行，并与外部OpenID提供者（OP）协作进行认证。

1. 用户访问 |Fess| 的SSO端点（``/sso/``）
2. |Fess| 将请求重定向到OP的授权端点
3. 用户在OP进行认证
4. OP将授权码重定向到 |Fess|
5. |Fess| 使用授权码从令牌端点获取ID Token
6. |Fess| 从ID Token（JWT）中获取用户信息并登录用户

.. note::
   |Fess| 使用授权码流程（Authorization Code Flow）。ID Token不经过浏览器，而是通过 |Fess| 与OP之间的后端通道（服务器间通信）直接从令牌端点获取。
   |Fess| 通过解码ID Token来提取声明（如 ``email`` 和 ``groups``）以构建用户信息，但不对JWT签名进行密码学验证。
   因此，与令牌端点的通信必须使用HTTPS，并请确认 |Fess| 与OP之间的通信路径是可信的。

有关基于角色的搜索集成，请参阅 :doc:`security-role`。

前提条件
========

在配置OpenID Connect认证之前，请验证以下前提条件：

- 已安装 |Fess| 15.7或更高版本
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
   ``sso.type`` 以及后文说明的各项 ``oic.*`` 设置，也可以通过管理画面的"系统 > 全局"页面进行设置和修改。
   在管理画面中修改的设置将保存到 ``system.properties``，重启后仍会保留。

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

.. note::
   这些URL可以从OP的Discovery端点（``/.well-known/openid-configuration``）获取。

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

用户属性配置
------------

配置分配给通过OIDC认证的用户的默认组和角色。
用户ID、组和角色分别按如下方式确定：

- **用户ID**：从ID Token（JWT）的 ``email`` 声明中获取。因此，范围中实际上必须包含 ``email``\ （如果无法获取 ``email`` 声明，登录将无法正常完成）。
- **组**：从ID Token的 ``groups`` 声明中获取。如果 ``groups`` 声明不存在，则使用 ``oic.default.groups`` 的值。
- **角色**：始终使用 ``oic.default.roles`` 的值（不存在从ID Token声明中获取角色的机制）。

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
- **客户端ID**：OP颁发的客户端标识符
- **客户端密钥**：用于客户端认证的密钥

.. note::
   大多数OP允许您从Discovery端点（``https://<OP>/.well-known/openid-configuration``）
   确认授权端点和令牌端点的URL。

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

无法获取用户信息
~~~~~~~~~~~~~~~~

- 请确认范围中是否包含所需的权限（``email``、``profile`` 等）
- 请确认OP侧是否为客户端允许了所需的范围

调试设置
--------

要调查问题，可以通过调整 |Fess| 的日志级别来输出OpenID Connect相关的详细日志。

在 ``app/WEB-INF/classes/log4j2.xml`` 中，可以添加以下日志记录器来更改日志级别：

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

参考信息
========

- :doc:`security-role` - 基于角色的搜索配置
- :doc:`sso-saml` - 使用SAML认证进行SSO配置
- :doc:`sso-entraid` - Microsoft Entra ID专用的SSO配置（使用Entra ID时，也可以使用专用配置代替通用的OpenID Connect配置）
