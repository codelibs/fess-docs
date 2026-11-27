====================
Security Configuration
====================

This page describes the security configurations recommended for safe operation of |Fess| in production environments.

.. danger::

   **Security is Critical**

   In production environments, it is strongly recommended to implement all security configurations described on this page.
   Failure to implement proper security configurations increases the risk of unauthorized access, data breaches, and system compromise.

Essential Security Configurations
==================================

Change Administrator Password
------------------------------

The default administrator password (``admin`` / ``admin``) must be changed.

**Procedure:**

1. Log in to the admin screen: http://localhost:8080/admin
2. Click "User" → "User"
3. Select the ``admin`` user
4. Set a strong password
5. Click the "Update" button

.. note::

   Once you have changed the password from ``admin``, you cannot set it back to a simple value such as ``admin`` (a blacklist of administrator passwords is configured via ``password.invalid.admin.passwords``). You can also change the initial password of the ``admin`` user before the first startup by setting ``index.user.initial_password`` in ``fess_config.properties``. ``bin/fess-setup init`` sets it for you; see :doc:`fess-setup`.

.. note::

   If you log in as ``admin`` with the initial password, the password change screen is displayed right after login. This is a prompt to change the password, not server-side enforcement (the login has already succeeded, and you can open the admin console without changing it). To make sure the password is changed, set the initial password with ``bin/fess-setup init`` or ``index.user.initial_password`` before the first startup.

**Recommended Password Policy:**

|Fess| provides a built-in feature that enforces the minimum/maximum password length and character-type requirements. Configure the following properties in ``fess_config.properties`` (defaults in parentheses):

- ``password.min.length`` (default: ``8``): Minimum length. 12 or more is recommended.
- ``password.max.length`` (default: ``100``): Maximum length in characters. A password is also limited in UTF-8 bytes by the password hash algorithm, whatever this value is (see below).
- ``password.require.uppercase`` (default: ``false``): Require uppercase letters.
- ``password.require.lowercase`` (default: ``false``): Require lowercase letters.
- ``password.require.digit`` (default: ``false``): Require digits.
- ``password.require.special.char`` (default: ``false``): Require symbols.

.. note::

   By default, the minimum length is ``8`` and all character-type requirements are disabled. To strengthen passwords, set the properties above explicitly. Note that |Fess| has no password expiration (forced periodic change) feature; if you want to enforce periodic password changes as an operational rule, do so manually.

**Password hashing and the byte limit:**

|Fess| stores the password of a local user as a hash. ``app.password.algorithm`` (default: ``bcrypt``) selects the algorithm for new and changed passwords, and ``app.password.bcrypt.cost`` (default: ``10``) sets the cost of BCrypt. While ``app.password.upgrade.enabled`` is ``true`` (default), a user whose stored hash is older (a legacy hash without an ``{id}`` prefix, the hash of another algorithm or a BCrypt hash with a lower cost) gets a new hash at the next successful login. The algorithm is a component, so a plugin can supply another one (see :ref:`webapp-plugin-password-encoder`).

The byte limit belongs to the algorithm. BCrypt reads only the first 72 bytes of a password in UTF-8, so since 15.10 a password longer than 72 bytes is refused when it is set (user management screen, forced password change on the login form, ``/api/v2/auth/password`` and the Admin API) with "Password must be no longer than 72 bytes.", whatever ``password.max.length`` (100 characters by default) allows. A character other than ASCII takes more than one byte (3 bytes for most Japanese, Chinese and Korean characters). An account whose password was set longer than 72 bytes before keeps logging in, because verifying a password applies no length limit. Only its first 72 bytes are compared, so any ending after the 72nd byte is accepted. Setting a new password (at most 72 bytes) removes this.

**Sessions after a password change:**

When the password of a local user is changed, whether by the user or by an administrator on the user management screen or through the Admin API, the other login sessions of that user end at their next check (see below). Each login session looks up the time of the last password change in the user index at most once per ``password.changed.check.interval`` in ``fess_config.properties`` (default: ``60`` seconds; ``0`` or less checks on every request), so the other sessions end within this many seconds, on any node. Users authenticated by LDAP or SSO are not affected, because their passwords are managed outside |Fess|.

**Sessions after a change of roles or groups:**

When the roles or the groups of a local user are changed after a session was opened, the login session of that user ends. This covers editing the user (on the user management screen or through the Admin API) and also deleting a role or a group that the user had. The check interval is the same ``password.changed.check.interval`` (default: ``60`` seconds) as for a password change. Unlike a password change, the session that made the change is not an exception: for example, when an administrator changes their own roles, the administrator's session ends as well and they have to log in again. An ended session is recorded in the audit log as ``SESSION_END`` with ``reason`` ``permissions_changed``. Users authenticated by LDAP or SSO are not affected, because their roles and groups are obtained from the identity provider at each login.

Change the Cipher Key
---------------------

``app.cipher.key`` in ``fess_config.properties`` is the key that encrypts the passwords stored in crawl configurations and data store configurations. The shipped value (``___change__me___``) is public. If the key is still the shipped value, |Fess| writes a warning to ``fess.log`` at startup. If the key is blank, |Fess| aborts the startup (see :ref:`upgrade-1510-cipher-key`). |Fess| does not change the key by itself.

Set it before the first start, together with the initial password of the ``admin`` user::

    $ bin/fess-setup init

For the RPM and DEB packages, run ``/usr/share/fess/bin/fess-setup init``. The command generates a random key, or takes one with ``--cipher-key``; see :doc:`fess-setup`. To set it by hand instead, edit ``app.cipher.key`` in ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` of the ZIP package, ``/etc/fess/fess_config.properties`` of the RPM and DEB packages). With the default ``app.cipher.algorithm`` (``aes``), the key must be 16, 24 or 32 characters.

.. warning::

   Changing the key after passwords have been saved in crawl or data store configurations makes those values impossible to decrypt. Keep the key with your backups of ``fess_config.properties``, and use the same key when you move to another installation.

Enable OpenSearch Security Plugin
----------------------------------

**Procedure:**

1. Remove or comment out the following line from ``opensearch.yml``::

       # plugins.security.disabled: true

2. Configure the security plugin::

       plugins.security.allow_default_init_securityindex: true
       plugins.security.authcz.admin_dn:
         - CN=admin,OU=SSL,O=Test,L=Test,C=DE

3. Configure TLS/SSL certificates

4. Restart OpenSearch

5. Configure the connection to OpenSearch on the |Fess| side.

   Specify the connection URL with the ``SEARCH_ENGINE_HTTP_URL`` environment variable (edit ``bin/fess.in.sh`` or the service environment file; the default value comes from ``search_engine.http.url`` in ``fess_config.properties``)::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200

   Specify the credentials with the following properties in ``fess_config.properties`` (the zip, RPM and DEB packages have no ``SEARCH_ENGINE_USERNAME`` / ``SEARCH_ENGINE_PASSWORD`` environment variables; the docker-fess images do)::

       search_engine.username=admin
       search_engine.password=<strong_password>

For details, refer to the `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__.

Enable HTTPS
------------

HTTP communication is not encrypted and poses risks of eavesdropping and tampering. Always use HTTPS in production environments.

**Method 1: Using a Reverse Proxy (Recommended)**

Deploy Nginx or Apache in front of |Fess| for HTTPS termination.

Nginx configuration example::

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

When TLS is terminated at the reverse proxy, also set the following in ``fess_config.properties`` so that the session cookie gets the ``Secure`` attribute. Restart |Fess| after changing it. Do not set it if users also access |Fess| over plain HTTP, because a session cannot be established over HTTP once it is set::

    session.cookie.secure=true

**Method 2: Configure HTTPS in Fess Itself**

Add the following to ``tomcat_config.properties``::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.SSLEnabled=true
    tomcat.certificateKeystoreFile=[path to keystore file]
    tomcat.certificateKeystorePassword=[password specified when creating the keystore file]
    tomcat.certificateKeyAlias=[certificate alias]
    tomcat.sslProtocol=[SSL protocol (e.g., TLS)]
    tomcat.enabledProtocols=list of enabled protocols (comma-separated) (e.g., TLSv1.2,TLSv1.3)

Recommended Security Configurations
====================================

Firewall Configuration
----------------------

Open only necessary ports and close unnecessary ones.

**Ports to Open:**

- **8080** (or 443 for HTTPS): |Fess| web interface (if external access is required)
- **22**: SSH (administration only, from trusted IP addresses only)

**Ports to Close:**

- **9200, 9300**: OpenSearch (internal communication only, block external access)

Linux (firewalld) configuration example::

    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --add-port=8080/tcp  # only when Fess is accessed directly on port 8080
    $ sudo firewall-cmd --reload

IP address restriction::

    $ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'

Access Control Configuration
-----------------------------

Consider restricting access to the admin screen to specific IP addresses.

Nginx access restriction example::

    location /admin {
        allow 192.168.1.0/24;
        deny all;

        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
    }

Roles and Access Control
------------------------

|Fess| provides two built-in roles:

- ``admin``: Administrator role that can perform all operations, including the admin screen.
- ``guest``: Role assigned to unauthenticated (anonymous) users.

Any other roles can be freely created from the admin screen. In |Fess|, a role is a tag that has only a name and is used mainly for access control of search results (which documents a user can view). The exception is a role named ``admin-`` followed by the name of an admin screen, such as ``admin-user`` or ``admin-scheduler``: it allows a user to open that screen, and the ``-view`` form, such as ``admin-user-view``, allows read-only access.

.. warning::

   The ``admin-*`` roles let you split day-to-day admin screens among operators, but they are not a privilege boundary. A user with ``admin-user`` can give any existing role, including the administrator role, to any user; ``admin-accesstoken`` can issue an access token with the ``Radmin-api`` permission, which grants the whole Admin API; ``admin-scheduler`` can run script jobs on the server; and ``admin-plugin`` can install plugins. Treat every ``admin-*`` role as equivalent to the administrator role (``authentication.admin.roles``, default ``admin``) and grant them only to trusted operators.

Following the principle of least privilege, grant the administrator role (``admin``) only to users who perform administrative tasks, and do not grant it to general search users.

**Procedure:**

1. Click "User" → "Role" in the admin screen
2. Create the necessary roles
3. Assign roles to users in "User" → "User"

Audit Logging
-------------

System operation history, such as authentication and administrative operations, is recorded as an audit log by default. The audit log is output by the ``fess.log.audit`` logger defined in ``log4j2.xml``, and its default output destination is ``audit.log``.

Because it is enabled by default, no additional configuration is required. To customize the output destination or log level, edit the following definition in ``log4j2.xml``::

    <Logger name="fess.log.audit" additivity="false" level="info">
        <AppenderRef ref="AuditFile"/>
    </Logger>

Each audit record is one line of tab-separated ``key:value`` fields (LTSV). A record starts with ``action`` and ends with ``ip`` (the client IP address) and ``time`` (UTC, ISO 8601). When ``app.audit.log.format`` is ``ecs``, or it is empty and the environment variable ``FESS_APP_TYPE`` is ``docker``, records are written as ECS JSON instead, with the fields as ``labels.<key>``.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Action
     - Fields
     - Written when
   * - ``LOGIN``
     - ``user``, ``permissions``
     - A user logs in.
   * - ``LOGOUT``
     - ``user``, ``permissions``
     - A user logs out.
   * - ``SESSION_END``
     - ``user``, ``reason``
     - |Fess| ends a login session on its own, as opposed to a logout that the user asked for (that is ``LOGOUT``). One record is written for each ended session.
   * - ``LOGIN_FAILURE``
     - ``class``, ``user``
     - A login is rejected, on the login form, in the login API or by SSO. A login that an SSO authenticator rejects with an exception is recorded as well.
   * - ``ACCESS``
     - ``user``, ``path``, ``execute``, ``method``, ``id``
     - A request reaches an admin screen or the admin REST API, before the action runs. For the admin REST API this is after the access token has been accepted.
   * - ``ACCESS_DENIED``
     - ``user``, ``path``
     - A request to an admin screen is rejected because of the user's roles, or an admin REST API request is rejected by the access token check (the API answers HTTP 401).
   * - ``UPDATE_PASSWORD``
     - ``user``, ``target``
     - A password is changed: by a user through the login screen or ``/api/v2/auth/password``, or by an administrator who sets a new password for a user on the user admin screen or through the admin REST API.
   * - ``UPDATE_PERMISSION``
     - ``user``, ``permissions``
     - The permissions of an LDAP user are updated.
   * - ``REGISTER_PASSKEY``
     - ``user``, ``target``, ``credentialId``
     - A passkey is registered.
   * - ``DELETE_PASSKEY``
     - ``user``, ``target``, ``credentialId``
     - A passkey is deleted: by the user, or by an administrator on the user admin screen. When an administrator sets a new password for a user, all passkeys of that user are deleted, and one record is written for each passkey.
   * - ``SCRIPT_EXECUTION``
     - ``scriptType``, ``source``, ``user``, ``result``, ``script``
     - A script runs. See :doc:`../config/scripting-overview`.

- ``LOGIN_FAILURE``: ``user`` is the user name that was typed and ``class`` is the type of the credential. When an SSO authenticator rejects a login with an exception, no credential has been resolved, so the record has neither ``user`` nor ``class``, and nothing from the exception is written.
- ``ACCESS``: ``user`` is the logged-in user when the request carries a session. When the admin REST API is called with only an access token and no session, it is the name of the access token (the token itself is never written; ``-`` when the name cannot be obtained). ``user`` of ``ACCESS_DENIED`` follows the same rule. ``method`` is the HTTP method. ``id`` is the value of the ``id`` request parameter and is written only when the request has one (it is not read from an upload request). No other request parameter is written, because the admin forms carry passwords and keys.
- ``ACCESS_DENIED``: for a rejected admin REST API request, only the request path is written. Neither the access token nor the parameter that carried it is recorded.
- ``REGISTER_PASSKEY`` and ``DELETE_PASSKEY``: ``user`` is the user who performed the operation and ``target`` is the name of the user who owns the passkey. ``credentialId`` is the first 8 characters of the credential ID, followed by ``...`` when it is longer. The key of the passkey is never written.
- ``UPDATE_PASSWORD``: ``user`` is the user who changed the password and ``target`` is the name of the user whose password was changed. The password and its hash are never written, and a rejected change writes nothing.
- ``SESSION_END``: ``user`` is the user whose session ended and ``reason`` is why it ended. ``password_changed``: the password of the user was changed after the session was opened. ``permissions_changed``: the roles or the groups of the local user were changed after the session was opened (by editing the user, or by deleting a role or a group that the user had). ``user_not_found``: the document of the local user no longer exists, for example because the user was deleted or renamed. ``idp_session_ended``: the identity provider ended its session (the ``SessionNotOnOrAfter`` of SAML, see :doc:`../config/sso-saml`, or OpenID Connect back-channel logout, see :doc:`../config/sso-oidc`).

Regular Security Updates
------------------------

Apply security updates for |Fess| and OpenSearch regularly.

**Recommended Procedure:**

1. Regularly check security information

   - `Fess Release Information <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch Security Advisories <https://github.com/opensearch-project/OpenSearch/security/advisories>`__

2. Validate updates in a test environment
3. Apply updates to the production environment

Data Protection
===============

Encrypt Backups
---------------

Backup data may contain sensitive information. Store backup files encrypted.

Encrypted backup example::

    $ tar czf fess-backup.tar.gz /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

The data directory of a running OpenSearch (``/var/lib/opensearch``) cannot be backed up consistently by copying files. Use the `OpenSearch snapshot feature <https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`__ for index data. The configuration data of |Fess| can be downloaded from the Backup page of the admin screen (see :doc:`../admin/backup-guide`).

Security Best Practices
========================

Principle of Least Privilege
-----------------------------

- Do not run Fess and OpenSearch as the root user
- Run with a dedicated user account
- Grant minimum necessary filesystem permissions

Network Isolation
-----------------

- Deploy OpenSearch in a private network
- Use VPN or private networks for internal communication
- Deploy only the |Fess| web interface in a DMZ

Regular Security Audits
-----------------------

- Regularly review access logs
- Detect abnormal access patterns
- Conduct regular vulnerability scans

Security Header Configuration
------------------------------

|Fess| sets ``X-Frame-Options: SAMEORIGIN`` on HTML responses by default (``response.headers`` in ``fess_config.properties``), so it does not need to be added in the proxy.

Configure security headers in Nginx or Apache as needed::

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

Security Checklist
==================

Before deploying to production, verify the following checklist:

Basic Configuration
-------------------

- [ ] Administrator password changed
- [ ] Cipher key (``app.cipher.key``) changed from the shipped value
- [ ] HTTPS enabled
- [ ] Default port numbers changed (optional)

Network Security
----------------

- [ ] Unnecessary ports closed with firewall
- [ ] Admin screen access IP restricted (if possible)
- [ ] OpenSearch access restricted to internal network only

Access Control
--------------

- [ ] Configured roles and access permissions appropriately (grant the administrator role only to necessary users)
- [ ] Unnecessary user accounts removed
- [ ] Password policy configured

Monitoring and Logging
----------------------

- [ ] Confirmed that audit logging is enabled
- [ ] Log retention period configured
- [ ] Log monitoring mechanism established (if possible)

Backup and Recovery
-------------------

- [ ] Regular backup schedule configured
- [ ] Backup data encrypted
- [ ] Restore procedures validated

Updates and Patch Management
-----------------------------

- [ ] Security update notification mechanism established
- [ ] Update procedures documented
- [ ] Test environment established for update validation

Security Incident Response
===========================

Response procedure when a security incident occurs:

1. **Incident Detection**

   - Log review
   - Abnormal access pattern detection
   - System behavior anomaly verification

2. **Initial Response**

   - Identify scope of impact
   - Prevent damage escalation (stop relevant services, etc.)
   - Preserve evidence

3. **Investigation and Analysis**

   - Detailed log analysis
   - Identify intrusion routes
   - Identify potentially leaked data

4. **Recovery**

   - Fix vulnerabilities
   - Restore systems
   - Strengthen monitoring

5. **Post-Incident Response**

   - Create incident report
   - Implement recurrence prevention measures
   - Report to stakeholders

Reference Information
=====================

- `OpenSearch Security Plugin <https://opensearch.org/docs/latest/security-plugin/>`__
- `OWASP Top 10 <https://owasp.org/www-project-top-ten/>`__
- `CIS Benchmarks <https://www.cisecurity.org/cis-benchmarks/>`__

For security questions or issues, please contact:

- Issues: https://github.com/codelibs/fess/issues
- Commercial Support: https://www.n2sm.net/
