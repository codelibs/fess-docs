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
2. Click "System" → "User"
3. Select the ``admin`` user
4. Set a strong password
5. Click the "Update" button

**Recommended Password Policy:**

- Minimum 12 characters
- Include uppercase letters, lowercase letters, numbers, and symbols
- Avoid dictionary words
- Change regularly (recommended every 90 days)

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

5. Update |Fess| configuration to add OpenSearch authentication credentials::

       SEARCH_ENGINE_HTTP_URL=https://opensearch:9200
       SEARCH_ENGINE_USERNAME=admin
       SEARCH_ENGINE_PASSWORD=<strong_password>

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

**Method 2: Configure HTTPS in Fess Itself**

Add the following to ``system.properties``::

    server.ssl.enabled=true
    server.ssl.key-store=/path/to/keystore.p12
    server.ssl.key-store-password=<password>
    server.ssl.key-store-type=PKCS12

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

    $ sudo firewall-cmd --permanent --add-service=http
    $ sudo firewall-cmd --permanent --add-service=https
    $ sudo firewall-cmd --permanent --remove-service=opensearch  # for custom services
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

Role-Based Access Control (RBAC)
---------------------------------

|Fess| supports multiple user roles. Following the principle of least privilege, grant users only the minimum necessary permissions.

**Role Types:**

- **Administrator**: All permissions
- **General User**: Search only
- **Crawler Administrator**: Manage crawl configurations
- **Search Result Editor**: Edit search results

**Procedure:**

1. Click "System" → "Role" in the admin screen
2. Create necessary roles
3. Assign roles to users in "System" → "User"

Enable Audit Logging
---------------------

Audit logging is enabled by default to record system operation history.

Enable audit logging in the configuration file (``log4j2.xml``)::

    <Logger name="org.codelibs.fess.audit" level="info" additivity="false">
        <AppenderRef ref="AuditFile"/>
    </Logger>

Regular Security Updates
------------------------

Apply security updates for |Fess| and OpenSearch regularly.

**Recommended Procedure:**

1. Regularly check security information

   - `Fess Release Information <https://github.com/codelibs/fess/releases>`__
   - `OpenSearch Security Advisories <https://opensearch.org/security.html>`__

2. Validate updates in a test environment
3. Apply updates to the production environment

Data Protection
===============

Encrypt Backups
---------------

Backup data may contain sensitive information. Store backup files encrypted.

Encrypted backup example::

    $ tar czf fess-backup.tar.gz /var/lib/opensearch /etc/fess
    $ gpg --symmetric --cipher-algo AES256 fess-backup.tar.gz

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

Configure security headers in Nginx or Apache as needed::

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;

Security Checklist
==================

Before deploying to production, verify the following checklist:

Basic Configuration
-------------------

- [ ] Administrator password changed
- [ ] HTTPS enabled
- [ ] Default port numbers changed (optional)

Network Security
----------------

- [ ] Unnecessary ports closed with firewall
- [ ] Admin screen access IP restricted (if possible)
- [ ] OpenSearch access restricted to internal network only

Access Control
--------------

- [ ] Role-based access control configured
- [ ] Unnecessary user accounts removed
- [ ] Password policy configured

Monitoring and Logging
----------------------

- [ ] Audit logging enabled
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
