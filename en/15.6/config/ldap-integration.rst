==================================
LDAP Integration Guide
==================================

Overview
========

|Fess| supports integration with LDAP (Lightweight Directory Access Protocol) servers,
enabling authentication and user management in enterprise environments.

LDAP integration enables:

- User authentication with Active Directory or OpenLDAP
- Group-based access control
- Automatic user information synchronization

Supported LDAP Servers
======================

|Fess| supports integration with the following LDAP servers:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Other LDAP v3 compatible servers

Prerequisites
=============

- Network access to the LDAP server
- Service account for LDAP searches (bind DN)
- Understanding of LDAP structure (base DN, attribute names, etc.)

Basic Configuration
===================

Add the following configuration to ``app/WEB-INF/conf/system.properties``.

LDAP Connection Settings
------------------------

::

    # Enable LDAP authentication
    ldap.admin.enabled=true

    # LDAP server URL
    ldap.provider.url=ldap://ldap.example.com:389

    # For secure connection (LDAPS)
    # ldap.provider.url=ldaps://ldap.example.com:636

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Bind DN (service account)
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # Bind password
    ldap.admin.security.credentials=your_password

User Search Settings
--------------------

::

    # User search base DN
    ldap.user.search.base=ou=users,dc=example,dc=com

    # User search filter
    ldap.user.search.filter=(uid={0})

    # Username attribute
    ldap.user.name.attribute=uid

Group Search Settings
---------------------

::

    # Group search base DN
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # Group search filter
    ldap.group.search.filter=(member={0})

    # Group name attribute
    ldap.group.name.attribute=cn

Active Directory Configuration
==============================

Configuration example for Microsoft Active Directory.

Basic Configuration
-------------------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Service account (UPN format)
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # User search
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # Group search
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Active Directory Specific Settings
----------------------------------

::

    # Nested group resolution
    ldap.memberof.enabled=true

    # Using memberOf attribute
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

OpenLDAP Configuration
======================

Configuration example for OpenLDAP.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Service account
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # User search
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # Group search
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
    ldap.group.name.attribute=cn

Security Settings
=================

LDAPS (SSL/TLS)
---------------

Use encrypted connections:

::

    # Use LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

    # Use StartTLS
    ldap.start.tls=true

For self-signed certificates, import the certificate into the Java truststore:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Password Protection
-------------------

Set passwords using environment variables:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

Role Mapping
============

You can map LDAP groups to |Fess| roles.

Automatic Mapping
-----------------

Group names are used directly as role names:

::

    # LDAP group "fess-users" -> Fess role "fess-users"
    ldap.group.role.mapping.enabled=true

Custom Mapping
--------------

::

    # Map group names to roles
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

User Information Synchronization
================================

You can synchronize user information from LDAP to |Fess|.

Automatic Synchronization
-------------------------

Automatically synchronize user information on login:

::

    ldap.user.sync.enabled=true

Attributes to Synchronize
-------------------------

::

    # Email address
    ldap.user.email.attribute=mail

    # Display name
    ldap.user.displayname.attribute=displayName

Connection Pooling
==================

Connection pool settings for performance improvement:

::

    # Enable connection pool
    ldap.connection.pool.enabled=true

    # Minimum connections
    ldap.connection.pool.min=1

    # Maximum connections
    ldap.connection.pool.max=10

    # Connection timeout (milliseconds)
    ldap.connection.timeout=5000

Failover
========

Failover to multiple LDAP servers:

::

    # Specify multiple URLs separated by spaces
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Troubleshooting
===============

Connection Error
----------------

**Symptom**: LDAP connection fails

**Check**:

1. Is the LDAP server running?
2. Is the port open in the firewall (389 or 636)?
3. Is the URL correct (``ldap://`` or ``ldaps://``)?
4. Are the bind DN and password correct?

Authentication Error
--------------------

**Symptom**: User authentication fails

**Check**:

1. Is the user search filter correct?
2. Does the user exist within the search base DN?
3. Is the username attribute correct?

Cannot Retrieve Groups
----------------------

**Symptom**: Cannot retrieve user groups

**Check**:

1. Is the group search filter correct?
2. Is the group membership attribute correct?
3. Do the groups exist within the search base DN?

Debug Settings
--------------

Output detailed logs:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Reference Information
=====================

- :doc:`security-role` - Role-Based Access Control
- :doc:`sso-spnego` - SPNEGO (Kerberos) Authentication
- :doc:`../admin/user-guide` - User Management Guide
