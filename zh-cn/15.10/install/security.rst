==================
安全配置
==================

本页面说明在生产环境中安全运行 |Fess| 的推荐安全配置。

.. danger::

   **安全非常重要**

   强烈建议在生产环境中实施本页面描述的所有安全配置。
   如果疏忽安全配置，将增加未经授权访问、数据泄漏、系统入侵等风险。

必需的安全配置
====================

更改管理员密码
--------------------

必须更改默认管理员密码（``admin`` / ``admin``）。

**步骤:**

1. 登录管理页面: http://localhost:8080/admin
2. 点击「用户」→「用户」
3. 选择 ``admin`` 用户
4. 设置强密码
5. 点击「更新」按钮

.. note::

   一旦将密码从 ``admin`` 更改后，就不能再设置回 ``admin`` 这样的简单字符串（``password.invalid.admin.passwords`` 中配置了管理员密码黑名单）。此外，在首次启动前，可以通过在 ``fess_config.properties`` 中设置 ``index.user.initial_password`` 来更改 ``admin`` 用户的初始密码。也可以用 ``bin/fess-setup init`` 设置（参见 :doc:`fess-setup`）。

**推荐密码策略:**

|Fess| 具备强制密码最小/最大长度及字符类型要求的内置功能。请在 ``fess_config.properties`` 中设置以下属性（括号内为默认值）。

- ``password.min.length`` （默认值: ``8``）：最小长度。建议设置为 12 以上。
- ``password.max.length`` （默认值: ``100``）：最大长度。
- ``password.require.uppercase`` （默认值: ``false``）：要求包含大写字母。
- ``password.require.lowercase`` （默认值: ``false``）：要求包含小写字母。
- ``password.require.digit`` （默认值: ``false``）：要求包含数字。
- ``password.require.special.char`` （默认值: ``false``）：要求包含符号。

.. note::

   默认情况下，最小长度为 ``8``，且所有字符类型要求均处于禁用状态。若要增强密码强度，请显式设置上述属性。另外，|Fess| 没有密码过期（强制定期更改）功能。如果希望将定期更改密码作为运维规则强制执行，请手动进行。

**密码更改后的会话：**

本地用户的密码被更改后（无论是用户本人更改，还是管理员在用户管理界面或通过 Admin API 更改），该用户的其他登录会话会在下一次请求时结束。更改通过各节点的缓存来确认，缓存的有效期由 ``fess_config.properties`` 中的 ``password.changed.cache.expire`` 指定（默认值：``10`` 秒；``0`` 或更小时每次请求都确认）。执行更改的节点立即生效，其他节点最迟在该秒数内生效。通过 LDAP 或 SSO 认证的用户不受影响，因为其密码在 |Fess| 之外管理。

更改加密密钥
------------

``fess_config.properties`` 中的 ``app.cipher.key`` 是用于加密爬取设置和数据存储设置中所保存密码的密钥。随附的值（``___change__me___``）是公开的。如果密钥为空或仍是随附的值，|Fess| 会在启动时向 ``fess.log`` 输出警告（参见 :ref:`upgrade-1510-cipher-key`）。|Fess| 不会自动更改密钥。

请在首次启动之前，与 ``admin`` 用户的初始密码一起设置::

    $ bin/fess-setup init

RPM / DEB 包请运行 ``/usr/share/fess/bin/fess-setup init``。命令会生成随机密钥，也可以用 ``--cipher-key`` 指定（参见 :doc:`fess-setup`）。如需手动设置，请编辑 ``fess_config.properties`` 中的 ``app.cipher.key``（ZIP 包为 ``app/WEB-INF/classes/fess_config.properties``，RPM / DEB 包为 ``/etc/fess/fess_config.properties``）。在默认的 ``app.cipher.algorithm``（``aes``）下，密钥必须是 16、24 或 32 个字符。

.. warning::

   在爬取设置或数据存储设置中保存了密码之后再更改密钥，这些值将无法解密。请将密钥与 ``fess_config.properties`` 的备份一起保管，迁移到其他环境时使用同一个密钥。

启用 OpenSearch 安全插件
--------------------------------------

**步骤:**

1. 从 ``opensearch.yml`` 中删除或注释掉以下行::

       # plugins.security.disabled: true

2. 配置安全插件::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. 配置 TLS/SSL 证书

4. 重启 OpenSearch

5. 在 |Fess| 一侧配置连接到 OpenSearch 的信息。

   请通过环境变量 ``SEARCH_ENGINE_HTTP_URL`` 指定连接 URL（可编辑 ``bin/fess.in.sh`` 或服务的环境配置文件；默认值来自 ``fess_config.properties`` 中的 ``search_engine.http.url``）::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   请通过 ``fess_config.properties`` 中的以下属性指定认证信息（zip、RPM、DEB 包中没有 ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD`` 环境变量；docker-fess 镜像支持这些环境变量）::

       search_engine.username=admin
       search_engine.password=<strong_password>

详情请参阅 `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__\ 。

启用 HTTPS
------------

HTTP 通信未加密，存在窃听或篡改的风险。在生产环境中必须使用 HTTPS。

**方法 1: 使用反向代理（推荐）**

在 |Fess| 前端部署 Nginx 或 Apache，进行 HTTPS 终止。

Nginx 配置示例::

    server {
        listen 443 ssl http2;
        server_name your-fess-domain.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

如果在反向代理处终止 TLS，请同时在 ``fess_config.properties`` 中添加以下设置，使会话 Cookie 带有 ``Secure`` 属性。修改后需要重启 |Fess|。设置后将无法通过 HTTP 建立会话，因此如果用户还会通过 HTTP 访问，请不要设置::

    session.cookie.secure=true

**方法 2: 在 Fess 自身配置 HTTPS**

在 ``tomcat_config.properties`` 中添加以下内容::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[密钥库文件路径]
    tomcat.certificateKeystorePassword=[创建密钥库文件时指定的密码]
    tomcat.certificateKeyAlias=[证书别名]
    tomcat.sslProtocol=[SSL 协议（例如：TLS）]
    tomcat.enabledProtocols=启用的协议列表（逗号分隔）（例如：TLSv1.2,TLSv1.3）

推荐的安全配置
====================

防火墙设置
------------------

仅开放必要的端口，关闭不必要的端口。

**应开放的端口:**

- **8080**\ （或 HTTPS 的 443）: |Fess| Web 界面（如需要外部访问）
- **22**: SSH（仅限管理用，仅允许可信 IP 地址）

**应关闭的端口:**

- **9200, 9300**: OpenSearch（仅限内部通信，阻止外部访问）

Linux (firewalld) 配置示例::

    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --add-port=8080/tcp  # 仅在直接通过 8080 端口访问 Fess 时
    $ sudo firewall-cmd --reload

IP 地址限制::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

访问控制设置
----------------

考虑将管理页面的访问限制为特定 IP 地址。

Nginx 访问限制示例::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

角色与访问控制
--------------------

|Fess| 预置了两个角色。

- ``admin``: 可执行包括管理页面在内的所有操作的管理员角色
- ``guest``: 分配给未登录（匿名）用户的角色

除此之外的角色可以在管理页面中自由创建。\ |Fess| 中的角色只是一个仅有名称的标签，主要用于搜索结果的访问控制（决定用户可以查看哪些文档）。但是，名称为 ``admin-`` 后接管理页面名称的角色（例如 ``admin-user`` 或 ``admin-scheduler``）是打开相应管理页面的权限；带有 ``-view`` 的角色（例如 ``admin-user-view``）仅允许只读访问。

.. warning::

   ``admin-*`` 角色用于将日常使用的管理页面分配给不同的运维人员，但它并不是权限边界。例如，拥有 ``admin-user`` 的用户可以将包括管理员角色在内的任意现有角色授予任意用户；``admin-accesstoken`` 可以颁发带有 ``Radmin-api`` 权限（可使用 Admin API 的全部功能）的访问令牌；``admin-scheduler`` 可以在服务器上执行脚本作业；``admin-plugin`` 可以安装插件。请将所有 ``admin-*`` 角色视同管理员角色（``authentication.admin.roles``，默认值为 ``admin``），仅授予受信任的运维人员。

遵循最小权限原则，管理员角色（``admin``）仅应授予执行管理业务的用户，不要授予普通搜索用户。

**步骤:**

1. 在管理页面点击「用户」→「角色」
2. 创建必要的角色
3. 在「用户」→「用户」中为用户分配角色

审计日志
--------

认证、管理操作等系统操作历史，默认会作为审计日志被记录。审计日志由 ``log4j2.xml`` 中定义的 ``fess.log.audit`` 记录器输出，默认输出目标为 ``audit.log``\ 。

由于默认已启用，无需额外配置。如需自定义输出目标或日志级别，请编辑 ``log4j2.xml`` 中的以下定义::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

每条审计记录是一行以制表符分隔的 ``key:value`` 字段（LTSV）。记录以 ``action`` 开头，以 ``ip`` （客户端 IP 地址）和 ``time`` （UTC，ISO 8601）结尾。当 ``app.audit.log.format`` 为 ``ecs``，或为空且环境变量 ``FESS_APP_TYPE`` 为 ``docker`` 时，记录会改为以 ECS 格式的 JSON 输出，各字段为 ``labels.<key>`` 。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - action
     - 字段
     - 记录的时机
   * - ``LOGIN``
     - ``user`` 、 ``permissions``
     - 用户登录时。
   * - ``LOGOUT``
     - ``user`` 、 ``permissions``
     - 用户退出登录时。
   * - ``LOGIN_FAILURE``
     - ``class`` 、 ``user``
     - 登录表单、登录 API 或 SSO 拒绝登录时。SSO 认证器以异常拒绝登录时也会记录。
   * - ``ACCESS``
     - ``user`` 、 ``path`` 、 ``execute`` 、 ``method`` 、 ``id``
     - 对管理画面或 Admin API 的请求在执行处理之前到达时。对于 Admin API，是在访问令牌被接受之后。
   * - ``ACCESS_DENIED``
     - ``user`` 、 ``path``
     - 对管理画面的请求因用户的角色被拒绝时，或对 Admin API 的请求被访问令牌检查拒绝时（API 返回 HTTP 401）。
   * - ``UPDATE_PASSWORD``
     - ``user`` 、 ``target``
     - 密码被更改时。包括用户自己通过登录画面或 ``/api/v2/auth/password`` 更改，以及管理员在用户管理画面或通过 Admin API 为用户设置新密码。
   * - ``UPDATE_PERMISSION``
     - ``user`` 、 ``permissions``
     - LDAP 用户的权限被更新时。
   * - ``SCRIPT_EXECUTION``
     - ``scriptType`` 、 ``source`` 、 ``user`` 、 ``result`` 、 ``script``
     - 脚本被执行时。请参阅 :doc:`../config/scripting-overview` 。

- ``LOGIN_FAILURE``： ``user`` 是输入的用户名， ``class`` 是凭据的类型。SSO 认证器以异常拒绝登录时，尚未确定凭据，因此记录中既没有 ``user`` 也没有 ``class``，也不会写入异常的任何内容。
- ``ACCESS``： ``method`` 是 HTTP 方法。 ``id`` 是请求参数 ``id`` 的值，仅在请求中带有该参数时记录（不会从上传请求中读取）。由于管理画面的表单包含密码和密钥，因此不会记录其他请求参数。
- ``ACCESS_DENIED``：对于被拒绝的 Admin API 请求，仅记录请求路径。访问令牌及传递它的参数都不会被记录。
- ``UPDATE_PASSWORD``： ``user`` 是更改密码的用户， ``target`` 是被更改密码的用户的名称。密码及其哈希值不会被记录，被拒绝的更改也不会被记录。

定期安全更新
------------------------------

请定期应用 |Fess| 和 OpenSearch 的安全更新。

**推荐步骤:**

1. 定期确认安全信息

   - `Fess 发布信息 <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch 安全公告 <https://github.com/opensearch-project/OpenSearch/security/advisories>`__

2. 在测试环境验证更新
3. 将更新应用到生产环境

数据保护
========

备份加密
------------------

备份数据可能包含机密信息。请加密保存备份文件。

加密备份示例::

    $ tar czf fess-backup.tar.gz /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

无法通过复制文件的方式一致地备份正在运行的 OpenSearch 的数据目录（``/var/lib/opensearch``）。索引数据请使用 `OpenSearch 快照功能 <https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`__。|Fess| 的配置数据可以在管理界面的备份页面下载（参见 :doc:`../admin/backup-guide`）。

安全最佳实践
============================

最小权限原则
------------

- 不要以 root 用户运行 Fess 和 OpenSearch
- 使用专用用户账号运行
- 授予最小必要的文件系统权限

网络隔离
--------------

- 将 OpenSearch 部署在专用网络
- 内部通信使用 VPN 或专用网络
- 仅将 |Fess| 的 Web 界面部署在 DMZ

定期安全审计
----------------------

- 定期确认访问日志
- 检测异常访问模式
- 定期实施脆弱性扫描

安全头配置
------------------------

|Fess| 默认会为 HTML 响应添加 ``X-Frame-Options: SAMEORIGIN``（``fess_config.properties`` 中的 ``response.headers``），因此无需在代理中重复添加。

根据需要，在 Nginx 或 Apache 中配置安全头::

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

安全检查清单
========================

部署到生产环境前，请确认以下检查清单：

基本设置
--------

- [ ] 已更改管理员密码
- [ ] 已将加密密钥（``app.cipher.key``）从随附的值更改
- [ ] 已启用 HTTPS
- [ ] 已更改默认端口号（可选）

网络安全
----------------------

- [ ] 已用防火墙关闭不必要的端口
- [ ] 已对管理页面进行 IP 限制（如可能）
- [ ] 已将 OpenSearch 的访问限制为仅限内部网络

访问控制
----------

- [ ] 已适当配置角色和访问权限（仅将管理员角色授予必要的用户）
- [ ] 已删除不必要的用户账号
- [ ] 已配置密码策略

监控和日志
--------

- [ ] 已确认审计日志已启用
- [ ] 已配置日志保存期限
- [ ] 已构建日志监控机制（如可能）

备份和恢复
--------------------

- [ ] 已设置定期备份计划
- [ ] 已加密备份数据
- [ ] 已验证恢复步骤

更新和补丁管理
----------------------

- [ ] 已建立接收安全更新通知的机制
- [ ] 已文档化更新步骤
- [ ] 已建立在测试环境验证更新的体系

安全事件响应
==========================

发生安全事件时的响应步骤：

1. **检测事件**

   - 确认日志
   - 检测异常访问模式
   - 确认系统行为异常

2. **初期响应**

   - 确定影响范围
   - 防止损害扩大（停止相关服务等）
   - 保全证据

3. **调查和分析**

   - 详细分析日志
   - 确定入侵路径
   - 确定可能泄漏的数据

4. **恢复**

   - 修复脆弱性
   - 恢复系统
   - 加强监控

5. **事后处理**

   - 创建事件报告
   - 实施防止再发措施
   - 向相关人员报告

参考信息
======

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

如有安全相关的问题或疑问，请联系：

- Issues: https://github.com/codelibs/fess/issues
- 商业支持: https://www.n2sm.net/
