====
常规
====

概述
====

在此管理页面,可以管理 |Fess| 的配置。
可以在不重启 |Fess| 的情况下更改各种 |Fess| 配置。

|image0|

配置内容
======

系统
------

JSON响应
::::::::::::

指定是否启用 JSON API。

需要登录
:::::::::::

指定搜索功能是否需要登录。

显示登录链接
::::::::::::::

设置是否在搜索界面显示登录页面的链接。

折叠重复结果
::::::::::::::

设置是否启用重复结果折叠。

显示缩略图
:::::::::::

设置是否启用缩略图显示。

默认标签值
:::::::::::::::

描述默认添加到搜索条件的标签值。
按角色或组指定时,请加上 role: 或 group: 前缀,如"role:admin=label1"。

默认排序值
:::::::::::::::

描述默认添加到搜索条件的排序值。
按角色或组指定时,请加上 role: 或 group: 前缀,如"role:admin=content_length.desc"。

虚拟主机
::::::::

设置虚拟主机。
详情请参考 :doc:`配置指南的虚拟主机 <../config/virtual-host>`。

热门词响应
:::::::::::::::::

指定是否启用热门词 API。

CSV文件编码
::::::::::::::::::

指定下载 CSV 文件的编码。

添加搜索参数
:::::::::::::::::

在搜索结果显示中传递参数时启用。

搜索文件代理
:::::::::::

指定是否启用搜索结果的文件代理。

使用浏览器区域设置
:::::::::::::::::

指定搜索时是否使用浏览器的区域设置。

SSO类型
:::::::

指定单点登录(Single Sign-On)类型。

- **无**: 不使用SSO
- **OpenID Connect**: 使用OpenID Connect
- **SAML**: 使用SAML
- **SPNEGO**: 使用SPNEGO
- **Entra ID**: 使用Microsoft Entra ID

爬虫
--------

检查上次修改时间
::::::::::::::

执行差分爬取时启用。

同时爬虫设置
::::::::::::::

指定同时执行的爬取配置数。

用户代理
::::::

指定爬虫使用的用户代理名称。

删除以前的文档
::::::::::::::::::

指定索引后的有效期天数。

要忽略的错误类型
:::::::::::::::

超过阈值的失败 URL 将被排除在爬取对象之外,但此处指定的异常名称等即使超过阈值也会作为爬取对象。

失败次数阈值
::::::::::::

如果爬取对象的文档被记录为失败 URL 的次数超过此处指定的次数,则在下次爬取时将被排除。

日志记录
------

搜索日志
::::::

指定是否启用搜索日志记录。

用户日志
::::::::

指定是否启用用户日志记录。

收藏日志
:::::::::::

指定是否启用收藏日志记录。

删除以前的搜索日志
:::::::::::::::

删除指定天数之前的搜索日志。

删除以前的作业日志
:::::::::::::::::

删除指定天数之前的作业日志。

删除以前的用户日志
::::::::::::::::::

删除指定天数之前的用户日志。

要删除日志的机器人名称
:::::::::::::::::

指定要从搜索日志中排除的机器人名称。

日志级别
::::::::

指定 fess.log 的日志级别。

建议
--------

按搜索词建议
::::::::::::::

指定是否从搜索日志生成建议候选。

按文档建议
::::::::::::::::::

指定是否从已索引的文档生成建议候选。

删除以前的建议信息
::::::::::::::::::::

删除指定天数之前的建议数据。

LDAP
----

LDAP URL
::::::::

指定 LDAP 服务器的 URL。

基本DN
:::::::

指定登录搜索界面的基本识别名。

绑定DN
:::::::

指定管理员的绑定DN。

密码
::::::::

指定绑定DN的密码。

用户DN
:::::::

指定用户的识别名。

帐户过滤器
:::::::::::::::

指定用户的 Common Name 或 uid 等。

组过滤器
::::::::::::::

指定要获取的组的过滤条件。

memberOf属性
:::::::::::

指定 LDAP 服务器可用的 memberOf 属性名。
对于 Active Directory,为 memberOf。
对于其他 LDAP 服务器,也可能是 isMemberOf。

安全认证
:::::::

指定 LDAP 的安全认证方式（例如: simple）。

初始上下文工厂
:::::::::::

指定 LDAP 的初始上下文工厂类（例如: com.sun.jndi.ldap.LdapCtxFactory）。

OpenID Connect
--------------

客户端ID
:::::::

指定 OpenID Connect 提供商的客户端 ID。

客户端密钥
::::::::

指定 OpenID Connect 提供商的客户端密钥。

认证服务器URL
::::::::::

指定 OpenID Connect 的认证服务器 URL。

令牌服务器URL
::::::::::

指定 OpenID Connect 的令牌服务器 URL。

重定向URL
::::::::

指定 OpenID Connect 的重定向 URL。

范围
::::

指定 OpenID Connect 的范围。

基础URL
::::::

指定 OpenID Connect 的基础 URL。

默认组
:::::

指定 OpenID Connect 认证时分配给用户的默认组。

默认角色
::::::

指定 OpenID Connect 认证时分配给用户的默认角色。

SAML
----

SP基础URL
::::::::

指定 SAML Service Provider 的基础 URL。

组属性名
::::::

指定从 SAML 响应中获取组的属性名。

角色属性名
::::::::

指定从 SAML 响应中获取角色的属性名。

默认组
:::::

指定 SAML 认证时分配给用户的默认组。

默认角色
::::::

指定 SAML 认证时分配给用户的默认角色。

SPNEGO
------

Krb5配置
::::::

指定 Kerberos 5 配置文件的路径。

登录配置
::::::

指定 JAAS（Java Authentication and Authorization Service）登录配置文件的路径。

登录客户端模块
::::::::::

指定 JAAS 的客户端登录模块名称。

登录服务器模块
::::::::::

指定 JAAS 的服务器登录模块名称。

预认证用户名
:::::::::

指定 SPNEGO 预认证使用的用户名。

预认证密码
::::::::

指定 SPNEGO 预认证使用的密码。

允许Basic认证
::::::::::

指定是否允许 Basic 认证回退。

允许非安全Basic认证
:::::::::::::::

指定是否允许在非安全（HTTP）连接上使用 Basic 认证。

NTLM提示
::::::

指定是否启用 NTLM 提示。

允许本地主机
:::::::::

指定是否允许从本地主机访问。

允许委托
::::::

指定是否允许 Kerberos 委托。

排除目录
::::::

指定从 SPNEGO 认证中排除的目录。

Entra ID
--------

客户端ID
:::::::

指定 Microsoft Entra ID 的应用程序（客户端）ID。

客户端密钥
::::::::

指定 Microsoft Entra ID 的客户端密钥。

租户
::::

指定 Microsoft Entra ID 的租户 ID。

认证机构
::::::

指定 Microsoft Entra ID 的认证机构 URL。

回复URL
:::::

指定 Microsoft Entra ID 的回复（重定向）URL。

状态TTL
:::::

指定认证状态的有效期（TTL）。

默认组
:::::

指定 Entra ID 认证时分配给用户的默认组。

默认角色
::::::

指定 Entra ID 认证时分配给用户的默认角色。

权限字段
::::::

指定从 Entra ID 获取权限信息的字段。

使用域服务
::::::::

指定是否使用 Entra ID 域服务。

公告显示
---------

登录页面
:::::::::::

描述在登录界面显示的消息。

搜索首页
::::::::::::

描述在搜索首页界面显示的消息。

高级搜索页面
::::::::::

描述在高级搜索界面显示的消息。

通知
----

通知邮件
::::::

指定爬取完成时通知的邮箱地址。
可以用逗号分隔指定多个地址。使用此功能需要邮件服务器。

Slack Webhook URL
:::::::::::::::::

指定用于 Slack 通知的 Webhook URL。

Google Chat Webhook URL
:::::::::::::::::::::::

指定用于 Google Chat 通知的 Webhook URL。

存储
--------

配置各项后,左侧菜单将显示[系统 > 存储]菜单。
有关文件管理,请参考 :doc:`存储 <../admin/storage-guide>`。

类型
::::

指定存储类型。
选择"自动"时,将根据端点自动判断存储类型。

- **自动**: 根据端点自动判断
- **S3**: Amazon S3
- **GCS**: Google Cloud Storage

存储桶
::::::

指定要管理的存储桶名称。

端点
:::::::::::

指定存储服务器的端点 URL。

- S3: 为空时使用 AWS 默认端点
- GCS: 为空时使用 Google Cloud 默认端点
- MinIO 等: MinIO 服务器的端点 URL

访问密钥
::::::::::

指定 S3 或 S3 兼容存储的访问密钥。

密钥
:::::::::::::

指定 S3 或 S3 兼容存储的密钥。

区域
::::

指定 S3 的区域（例如: ap-northeast-1）。

项目ID
::::::

指定 GCS 的 Google Cloud 项目 ID。

凭证路径
::::::::

指定 GCS 用服务账户凭证 JSON 文件的路径。

示例
==

LDAP配置示例
----------

.. tabularcolumns:: |p{4cm}|p{4cm}|p{4cm}|
.. list-table:: LDAP/Active Directory 的配置
   :header-rows: 1

   * - 名称
     - 值 (LDAP)
     - 值 (Active Directory)
   * - LDAP URL
     - ldap://SERVERNAME:389
     - ldap://SERVERNAME:389
   * - 基本DN
     - cn=Directory Manager
     - dc=fess,dc=codelibs,dc=org
   * - 绑定DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - manager@fess.codelibs.org
   * - 用户DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - %s@fess.codelibs.org
   * - 帐户过滤器
     - cn=%s 或 uid=%s
     - (&(objectClass=user)(sAMAccountName=%s))
   * - 组过滤器
     -
     - (member:1.2.840.113556.1.4.1941:=%s)
   * - memberOf
     - isMemberOf
     - memberOf


.. |image0| image:: ../../../resources/images/en/15.6/admin/general-1.png
.. pdf            :height: 940 px
