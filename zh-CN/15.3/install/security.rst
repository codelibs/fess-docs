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
2. 点击「系统」→「用户」
3. 选择 ``admin`` 用户
4. 设置强密码
5. 点击「更新」按钮

**推荐密码策略:**

- 至少 12 个字符
- 包含大写字母、小写字母、数字、符号
- 避免使用字典中的单词
- 定期更改（建议每 90 天）

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

5. 更新 |Fess| 的配置，添加 OpenSearch 的认证信息::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200
       SEARCH_ENGINE_USERNAME=admin
       SEARCH_ENGINE_PASSWORD=<strong_password>

详情请参阅 `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__。

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

**方法 2: 在 Fess 自身配置 HTTPS**

在 ``system.properties`` 中添加以下内容::

    server.ssl.enabled=true
    server.ssl.key-store=/path/to/keystore.p12
    server.ssl.key-store-password=<password>
    server.ssl.key-store-type=PKCS12

推荐的安全配置
====================

防火墙设置
------------------

仅开放必要的端口，关闭不必要的端口。

**应开放的端口:**

- **8080**（或 HTTPS 的 443）: |Fess| Web 界面（如需要外部访问）
- **22**: SSH（仅限管理用，仅允许可信 IP 地址）

**应关闭的端口:**

- **9200, 9300**: OpenSearch（仅限内部通信，阻止外部访问）

Linux (firewalld) 配置示例::

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # 自定义服务的情况
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

基于角色的访问控制 (RBAC)
-----------------------------

|Fess| 支持多个用户角色。遵循最小权限原则，仅授予用户必要的最小权限。

**角色类型:**

- **管理员**: 所有权限
- **普通用户**: 仅限搜索
- **爬虫管理员**: 爬取配置管理
- **搜索结果编辑者**: 搜索结果编辑

**步骤:**

1. 在管理页面点击「系统」→「角色」
2. 创建必要的角色
3. 在「系统」→「用户」中为用户分配角色

启用审计日志
--------------

为了记录系统操作历史，审计日志默认启用。

在配置文件（``log4j2.xml``）中启用审计日志::

    <Logger name="org.codelibs.fess.audit" level="info" additivity="false">
        <AppenderRef ref="AuditFile"/>
    </Logger>

定期安全更新
------------------------------

请定期应用 |Fess| 和 OpenSearch 的安全更新。

**推荐步骤:**

1. 定期确认安全信息

   - `Fess 发布信息 <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch 安全公告 <https://opensearch.org/security.html>`__

2. 在测试环境验证更新
3. 将更新应用到生产环境

数据保护
========

备份加密
------------------

备份数据可能包含机密信息。请加密保存备份文件。

加密备份示例::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

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

根据需要，在 Nginx 或 Apache 中配置安全头::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

安全检查清单
========================

部署到生产环境前，请确认以下检查清单：

基本设置
--------

- [ ] 已更改管理员密码
- [ ] 已启用 HTTPS
- [ ] 已更改默认端口号（可选）

网络安全
----------------------

- [ ] 已用防火墙关闭不必要的端口
- [ ] 已对管理页面进行 IP 限制（如可能）
- [ ] 已将 OpenSearch 的访问限制为仅限内部网络

访问控制
----------

- [ ] 已配置基于角色的访问控制
- [ ] 已删除不必要的用户账号
- [ ] 已配置密码策略

监控和日志
--------

- [ ] 已启用审计日志
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
