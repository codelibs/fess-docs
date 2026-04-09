============================================================
第15回：安全的搜索基础设施 -- SSO 集成与零信任环境下的搜索访问控制
============================================================

前言
====

企业的信息安全要求逐年趋于严格。
由于搜索系统汇聚了大量机密文档，因此适当的认证和授权机制不可或缺。

本文在第5回介绍的基于角色的搜索基础上，进一步设计以 SSO（单点登录）集成为核心的安全架构。

目标读者
========

- 在企业环境中运维 Fess 的人员
- 负责 SSO 集成（OIDC、SAML）设计的人员
- 了解零信任安全概念的人员

安全需求整理
=============

下面整理企业典型的安全需求。

.. list-table:: 安全需求
   :header-rows: 1
   :widths: 30 70

   * - 需求
     - 说明
   * - 单点登录
     - 与现有 IdP 集成，免除额外的登录操作
   * - 基于角色的访问
     - 根据用户的归属和权限控制搜索结果
   * - 通信加密
     - 通过 HTTPS 加密所有通信
   * - API 访问控制
     - 基于令牌的 API 认证和权限管理
   * - 审计日志
     - 记录谁搜索了什么

SSO 集成选项
=============

下面整理 Fess 支持的 SSO 协议及其各自的适用场景。

.. list-table:: SSO 协议对比
   :header-rows: 1
   :widths: 20 30 50

   * - 协议
     - 代表性 IdP
     - 适用场景
   * - OpenID Connect
     - Entra ID、Keycloak、Google
     - 云环境、现代认证基础设施
   * - SAML 2.0
     - Entra ID、Okta、OneLogin
     - 企业环境、已有 SAML IdP 的情况
   * - SPNEGO/Kerberos
     - Active Directory
     - Windows 集成认证环境

通过 OpenID Connect / Entra ID 进行 SSO 集成
===============================================

这是最现代且推荐的方法。
Fess 除了提供通用的 OpenID Connect 集成外，还提供了 Entra ID（Azure AD）专用的集成功能。
这里以与 Entra ID 的集成为例进行说明。

认证流程概述
-------------

1. 用户访问 Fess
2. Fess 将用户重定向到 Entra ID 的认证页面
3. 用户在 Entra ID 进行认证（包括 MFA）
4. Entra ID 将认证令牌返回给 Fess
5. Fess 从令牌中获取用户信息和组信息
6. 根据组信息分配角色
7. 基于角色提供搜索结果

Entra ID 端配置
-----------------

1. 在 Entra ID 中注册应用程序
2. 配置重定向 URI（Fess 的 OIDC 回调 URL）
3. 授予所需的 API 权限（User.Read、GroupMember.Read.All 等）
4. 获取客户端 ID 和密钥

Fess 端配置
-------------

在管理界面的 [系统] > [常规] 页面中配置 SSO 连接信息。
主要配置项如下：

- OpenID Connect 提供者 URL（Entra ID 端点）
- 客户端 ID
- 客户端密钥
- 作用域（openid、profile、email 等）
- 组声明设置

组与角色的映射
----------------

将 Entra ID 的组映射到 Fess 的角色。
这样，Entra ID 中的组管理就能直接反映到搜索结果的控制中。

示例：Entra ID 组 "Engineering" -> Fess 角色 "engineering_role"

通过 SAML 进行 SSO 集成
==========================

在已有 SAML IdP 的环境中，SAML 集成是合适的选择。

认证流程概述
-------------

在 SAML 中，SP（Service Provider = Fess）与 IdP 之间交换 SAML Assertion。

1. 用户访问 Fess
2. Fess 向 IdP 发送 SAML AuthnRequest
3. IdP 对用户进行认证
4. IdP 将 SAML Response（包含用户属性）返回给 Fess
5. Fess 根据用户属性分配角色

Fess 端配置
-------------

SAML 集成需要以下配置：

- IdP 的元数据 URL 或 XML 文件
- SP 的实体 ID
- Assertion Consumer Service URL
- 属性映射（用户名、电子邮件地址、组）

SPNEGO / Kerberos 集成
========================

在 Windows Active Directory 环境中，可以使用 SPNEGO/Kerberos 进行 Windows 集成认证。
从加入域的 PC 通过浏览器访问时，无需额外的登录操作即可自动完成认证。

这种方式对用户来说最为透明，但配置也最为复杂。
需要以 Active Directory 域环境为前提。

通信加密
=========

SSL/TLS 配置
--------------

在生产环境中，建议通过 HTTPS 进行对 Fess 的所有访问。

**反向代理方式（推荐）**

部署 Nginx 或 Apache HTTP Server 作为反向代理来进行 SSL 终端处理。
Fess 本身以 HTTP 运行，由反向代理处理 HTTPS。

::

    [客户端] --HTTPS--> [Nginx] --HTTP--> [Fess]

这种方式的优点在于证书管理集中在反向代理上。

**Fess 直接配置方式**

也可以直接在 Fess 的 Tomcat 上配置 SSL 证书。
适用于小规模环境或不部署反向代理的情况。

API 访问安全
==============

下面加强第11回中介绍的 API 集成的安全性。

令牌权限设计
-------------

为访问令牌配置适当的权限。

.. list-table:: 令牌设计示例
   :header-rows: 1
   :widths: 25 25 50

   * - 用途
     - 权限
     - 备注
   * - 搜索组件
     - 仅搜索（只读）
     - 在前端使用
   * - 批处理
     - 搜索 + 索引
     - 在服务器端使用
   * - 管理自动化
     - 管理 API 访问
     - 在运维脚本中使用

令牌管理
---------

- 定期轮换（每3至6个月）
- 立即撤销不再需要的令牌
- 监控令牌的使用情况

审计与日志
===========

搜索系统中的审计日志对于安全事件调查和合规应对至关重要。

Fess 记录的日志
-----------------

- **搜索日志**：记录谁搜索了什么（可在管理界面的 [系统信息] > [搜索日志] 中查看）
- **审计日志** (``audit.log``)：登录、登出、访问、权限变更等操作被统一记录

日志保存
---------

根据安全要求设置日志保存期限。
如果有合规要求，还应考虑将日志转发到外部日志管理系统（SIEM）。

总结
====

本文设计了企业环境下 Fess 的安全架构。

- SSO 集成的3种选项（OIDC、SAML、SPNEGO）及各自的适用场景
- 通过 OpenID Connect 进行 Entra ID 集成的设计
- 通过 SSL/TLS 进行通信加密
- API 访问令牌的权限设计
- 审计日志管理

在兼顾安全性与便利性的同时，构建安全的搜索基础设施吧。

下一回将讨论搜索基础设施的自动化。

参考资料
========

- `Fess SSO 配置 <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Fess 安全配置 <https://fess.codelibs.org/ja/15.5/config/security.html>`__
