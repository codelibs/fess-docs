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
6. 用户登录
7. |Fess| 在后台使用Microsoft Graph API获取用户的组和角色信息，解析完成后应用于基于角色的搜索

.. note::
   |Fess| 15.8 及以后版本会向授权端点请求 ``response_mode=query``\ ，因此步骤4的授权响应以GET方式返回。
   15.7 及之前版本以跨站POST方式返回，而 |Fess| 的默认值 ``tomcat.sameSiteCookies = lax``
   在该情况下不会发送会话Cookie，因此需要将其改为 ``tomcat.sameSiteCookies = none`` 作为规避方法。
   如果您仅出于该原因设置了 ``none``\ ，现在可以恢复为默认值。

有关基于角色的搜索集成，请参阅 :doc:`security-role`。

前提条件
========

在配置Entra ID认证之前，请验证以下前提条件：

- 已安装 |Fess| 15.8或更高版本
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
   * - ``entraid.response.mode``
     - 授权响应的返回方式。可指定 ``query`` 或 ``form_post``\ 。
     - ``query``
   * - ``entraid.default.groups``
     - 默认组（逗号分隔）
     - （无）
   * - ``entraid.default.roles``
     - 默认角色（逗号分隔）
     - （无）
   * - ``entraid.permission.fields``
     - 额外用作权限值的组/角色字段（逗号分隔）。组/角色的ID（GUID）始终作为权限使用，此处指定的字段（例如 ``mail``）的值将被追加添加。
     - ``mail``
   * - ``entraid.use.ds``
     - 域服务集成。设为 ``true`` 时，对于 ``name@domain`` 格式的权限值，会同时将去除域部分后的本地部分（``name``）也添加为权限。
     - ``true``

.. note::

   组/角色的ID（GUID）始终作为权限使用，但只有启用邮件的组才具有 ``mail`` 值。
   Microsoft 365组启用了邮件，因此组名也会注册为权限。
   而 **安全组未启用邮件，保持默认值时只有GUID会成为权限**\ 。
   如果文件系统的访问权限指定的是安全组名称，则权限不匹配，这些文档不会出现在搜索结果中。

   此时请添加所有组都具有的 ``displayName``\ ：

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` 不带域限定且不唯一，因此未包含在默认值中。
   例如，如果Entra ID中存在名为 ``Administrators`` 的组，它也会匹配访问权限指定了Windows内置组
   ``Administrators`` 的文档。添加前请确认这些名称不会与访问权限中已使用的名称冲突。

.. note::
   使用默认值 ``query`` 时，授权码会包含在回调URL的查询字符串中。
   指定 ``form_post`` 后，授权码不会出现在URL中，因此也不会留在浏览器历史记录以及前端代理或WAF的访问日志中。
   但 ``form_post`` 会使回调成为跨站POST，因此需要 ``tomcat.sameSiteCookies = none``\ 。
   未进行该设置时，会话Cookie不会被发送，登录将失败，因此大多数环境应保持默认值。
   指定其他值时，将输出警告并按 ``query`` 处理。

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

4. 复制并保存生成的 **值**\ （此值不会再次显示）

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

   - ``User.Read`` - 获取已登录用户的组成员关系（``/me/memberOf``）所需。创建应用注册时默认授予
   - ``GroupMember.Read.All`` - 读取组名等组属性以及解析嵌套组所需

6. 点击 **添加权限**

7. 点击 **为<租户名称>授予管理员同意**

.. note::
   管理员同意需要租户管理员权限。

.. note::
   也可以授予 ``Group.Read.All`` 或 ``Directory.Read.All`` 来代替 ``GroupMember.Read.All``\ ，
   组属性的获取与嵌套组的解析同样可以正常工作。但 ``/me/memberOf`` 无法通过 ``Group.Read.All``
   授权，因此无论采用哪种方式都需要 ``User.Read``\ 。

.. note::
   |Fess| 在获取令牌时会请求 ``https://graph.microsoft.com/.default`` 作用域。
   15.8 及以后版本还会向授权端点发送 ``openid profile offline_access https://graph.microsoft.com/.default``\ ，以便针对同一组权限请求同意。
   这意味着将使用在应用注册中配置并已授予同意的所有访问权限。
   因此，若要获取组信息，必须将上述权限添加到应用注册中，并授予管理员同意。

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
直接所属关系的查找与父组的查找都在登录后的同一个后台任务中执行，因此登录本身不会被Microsoft Graph拖慢。
父组的查找最多涵盖一定层级数，获取结果将被缓存一段时间。该后台任务完成后，用户的权限将被重新计算。

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
当各 ``entraid.*`` 属性未设置时，将使用对应 ``aad.*`` 属性的值。此外，``sso.type=aad`` 与 ``sso.type=entraid`` 的处理方式相同。

::

    # 启用SSO（也可使用 sso.type=aad）
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
- 如果将 ``entraid.response.mode`` 设置为 ``form_post``\ ，请确认已配置 ``tomcat.sameSiteCookies = none``\ 。否则回调时不会发送会话Cookie，会反复返回登录页面

发生认证错误
~~~~~~~~~~~~

- 验证租户ID、客户端ID和客户端密钥是否正确配置
- 检查客户端密钥是否已过期
- 验证是否已为API权限授予管理员同意

无法获取组信息
~~~~~~~~~~~~~~

- 验证是否已授予 ``User.Read`` 和 ``GroupMember.Read.All`` 权限
  （``GroupMember.Read.All`` 可以用 ``Group.Read.All`` 或 ``Directory.Read.All`` 代替，
  但 ``/me/memberOf`` 仍然需要 ``User.Read``\ ）
- 验证是否已授予管理员同意
- 检查用户是否在Entra ID中属于组
- 如果无法解析嵌套的父组，日志中会输出 ``Not allowed to read the parent groups of ...`` 警告。
  此时请授予 ``GroupMember.Read.All``
- |Fess| 会在登录完成后于后台解析用户所属的组和角色，因此登录本身不会等待Microsoft Graph的响应。
  在解析完成之前，用户仅缺少与组、角色相关联的权限——用户自身的用户级权限始终存在——因此本应
  可以查看的文档可能暂时不会出现在搜索结果中。解析进行期间，搜索界面会显示相应提示
- 如果解析失败，搜索界面会显示提示，要求用户重新登录；如果问题反复出现，请联系管理员。
  系统不会自动重试，一旦失败，该会话在其余时间内将不再重新解析

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
