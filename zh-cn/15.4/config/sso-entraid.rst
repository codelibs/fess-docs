================================
Microsoft Entra ID SSO配置
================================

概述
====

|Fess| 支持使用Microsoft Entra ID（前Azure AD）进行单点登录（SSO）认证。
通过使用Entra ID认证，您可以将Microsoft 365环境中的用户信息和组信息与 |Fess| 的基于角色的搜索集成。

Entra ID认证的工作原理
----------------------

在Entra ID认证中，|Fess| 作为OAuth 2.0/OpenID Connect客户端运行，并与Microsoft Entra ID协作进行认证。

1. 用户访问 |Fess| 的SSO端点（``/sso/``）
2. |Fess| 将请求重定向到Entra ID的授权端点
3. 用户在Entra ID进行认证（Microsoft登录）
4. Entra ID将授权码重定向到 |Fess|
5. |Fess| 使用授权码获取访问令牌
6. |Fess| 使用Microsoft Graph API获取用户的组和角色信息
7. 用户登录，组信息应用于基于角色的搜索

有关基于角色的搜索集成，请参阅 :doc:`security-role`。

前提条件
========

在配置Entra ID认证之前，请验证以下前提条件：

- 已安装 |Fess| 15.4或更高版本
- Microsoft Entra ID（Azure AD）租户可用
- |Fess| 可通过HTTPS访问（生产环境必需）
- 您有权在Entra ID中注册应用程序

基本配置
========

启用SSO
-------

要启用Entra ID认证，请在 ``app/WEB-INF/conf/system.properties`` 中添加以下设置：

::

    sso.type=entraid

必需设置
--------

配置从Entra ID获取的信息。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``entraid.tenant``
     - 租户ID（例如：``xxx.onmicrosoft.com``）
     - （必需）
   * - ``entraid.client.id``
     - 应用程序（客户端）ID
     - （必需）
   * - ``entraid.client.secret``
     - 客户端密钥值
     - （必需）
   * - ``entraid.reply.url``
     - 重定向URI（回调URL）
     - 使用请求URL

.. note::
   除了 ``entraid.*`` 前缀外，您还可以使用旧版 ``aad.*`` 前缀以保持向后兼容性。

可选设置
--------

可根据需要添加以下设置。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 描述
     - 默认值
   * - ``entraid.authority``
     - 认证服务器URL
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - State有效期（秒）
     - ``3600``
   * - ``entraid.default.groups``
     - 默认组（逗号分隔）
     - （无）
   * - ``entraid.default.roles``
     - 默认角色（逗号分隔）
     - （无）

Entra ID侧配置
==============

在Azure Portal中注册应用
------------------------

1. 登录 `Azure Portal <https://portal.azure.com/>`_

2. 选择 **Microsoft Entra ID**

3. 转到 **管理** → **应用注册** → **新注册**

4. 注册应用程序：

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - 设置
        - 值
      * - 名称
        - 任意名称（例如：Fess SSO）
      * - 支持的帐户类型
        - "仅此组织目录中的帐户"
      * - 平台
        - Web
      * - 重定向URI
        - ``https://<Fess主机>/sso/``

5. 点击 **注册**

创建客户端密钥
--------------

1. 在应用详情页面，点击 **证书和密码**

2. 点击 **新客户端密钥**

3. 设置描述和过期时间，然后点击 **添加**

4. 复制并保存生成的 **值**（此值不会再次显示）

.. warning::
   客户端密钥值仅在创建后立即显示。
   请务必在离开页面之前记录它。

配置API权限
-----------

1. 点击左侧菜单中的 **API权限**

2. 点击 **添加权限**

3. 选择 **Microsoft Graph**

4. 选择 **委托的权限**

5. 添加以下权限：

   - ``Group.Read.All`` - 获取用户组信息所需

6. 点击 **添加权限**

7. 点击 **为<租户名称>授予管理员同意**

.. note::
   管理员同意需要租户管理员权限。

需要获取的信息
--------------

以下信息用于Fess配置：

- **应用程序（客户端）ID**：在概述页面上，显示为"应用程序(客户端) ID"
- **租户ID**：在概述页面上，显示为"目录(租户) ID"或 ``xxx.onmicrosoft.com`` 格式
- **客户端密钥值**：在证书和密码中创建的值

组和角色映射
============

通过Entra ID认证，|Fess| 使用Microsoft Graph API自动获取用户所属的组和角色。
获取的组ID和组名可用于 |Fess| 的基于角色的搜索。

嵌套组
------

|Fess| 不仅获取用户直接所属的组，还会递归获取父组（嵌套组）。
此处理在登录后异步执行，以最大程度地减少对登录时间的影响。

默认组设置
----------

要为所有Entra ID用户分配通用组：

::

    entraid.default.groups=authenticated_users,entra_users

配置示例
========

最小配置（用于测试）
--------------------

以下是在测试环境中进行验证的最小配置示例。

::

    # 启用SSO
    sso.type=entraid

    # Entra ID设置
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

推荐配置（用于生产）
--------------------

以下是生产环境的推荐配置示例。

::

    # 启用SSO
    sso.type=entraid

    # Entra ID设置
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # 默认组（可选）
    entraid.default.groups=authenticated_users

旧版配置（向后兼容）
--------------------

为了与以前的版本兼容，也可以使用 ``aad.*`` 前缀。

::

    # 启用SSO
    sso.type=entraid

    # 旧版配置键
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

故障排除
========

常见问题和解决方案
------------------

认证后无法返回Fess
~~~~~~~~~~~~~~~~~~

- 验证Azure Portal应用注册中的重定向URI是否正确配置
- 确保 ``entraid.reply.url`` 的值与Azure Portal配置完全匹配
- 验证协议（HTTP/HTTPS）是否匹配
- 验证重定向URI是否以 ``/`` 结尾

发生认证错误
~~~~~~~~~~~~

- 验证租户ID、客户端ID和客户端密钥是否正确配置
- 检查客户端密钥是否已过期
- 验证是否已为API权限授予管理员同意

无法获取组信息
~~~~~~~~~~~~~~

- 验证是否已授予 ``Group.Read.All`` 权限
- 验证是否已授予管理员同意
- 检查用户是否在Entra ID中属于组

调试设置
--------

要调查问题，您可以通过调整 |Fess| 的日志级别来输出详细的Entra ID相关日志。

在 ``app/WEB-INF/classes/log4j2.xml`` 中，您可以添加以下日志记录器来更改日志级别：

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

参考
====

- :doc:`security-role` - 基于角色的搜索配置
- :doc:`sso-saml` - SAML认证SSO配置
- :doc:`sso-oidc` - OpenID Connect认证SSO配置
