==================================
LDAP Integration Guide
==================================

Overview
========

|Fess| supports integration with LDAP (Lightweight Directory Access Protocol) servers,
enabling authentication and user management in enterprise environments.

LDAP integration enables:

- User authentication (login) with Active Directory or OpenLDAP
- Group- and role-based access control
- Management of LDAP users, roles, and groups from the administration screen (optional)

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

Configuration Overview
======================

LDAP configuration in |Fess| is managed in two separate locations depending on its purpose.

Connection and Authentication Settings (administration screen / ``system.properties``)
   These settings control the connection to the LDAP server and login authentication.
   They can be configured from the **"System > General"** page in the administration screen,
   under the "LDAP" section, and are saved to
   ``app/WEB-INF/conf/system.properties``.

LDAP Administration and Behavior Settings (``fess_config.properties``)
   These settings control features for managing LDAP users, roles, and groups from the
   administration screen, as well as behaviors such as role resolution. They are defined in
   ``app/WEB-INF/classes/fess_config.properties`` and can be changed by editing that file.

.. note::

   If you only need login authentication, the "Connection and Authentication Settings" alone are
   sufficient. The "LDAP Administration" feature (``ldap.admin.enabled``) is only required when
   you want to create, update, or delete LDAP users, roles, and groups from the administration
   screen.

Connection and Authentication Settings
======================================

These settings can be configured from the "System > General" LDAP section in the administration
screen and are saved to ``app/WEB-INF/conf/system.properties``. You may also edit the file
directly.

.. list-table:: Connection and Authentication Properties
   :header-rows: 1
   :widths: 30 15 55

   * - Property
     - Default
     - Description
   * - ``ldap.provider.url``
     - (none)
     - URL of the LDAP server. Example: ``ldap://ldap.example.com:389``. For LDAPS: ``ldaps://ldap.example.com:636``. Specify multiple URLs separated by spaces for failover.
   * - ``ldap.base.dn``
     - (none)
     - Base DN for LDAP searches. Example: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - (none)
     - DN template used for user authentication (bind). ``%s`` is replaced with the username. Example: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - LDAP authentication method (JNDI ``java.naming.security.authentication``). Normally use ``simple``.
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - JNDI initial context factory class. This normally does not need to be changed.
   * - ``ldap.admin.security.principal``
     - (none)
     - Bind DN of the service account used for LDAP searches. Example: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - (none)
     - Password for the service account above.
   * - ``ldap.account.filter``
     - (none)
     - Filter used to search for a user entry during role resolution. ``%s`` is replaced with the username. Example: ``uid=%s``
   * - ``ldap.group.filter``
     - (empty)
     - Search filter used during group resolution. ``%s`` is replaced with the user's DN or similar. Example: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - Attribute name representing group membership. Used to resolve roles on servers that carry this attribute, such as Active Directory.

Example configuration (when editing ``system.properties`` directly):

::

    # LDAP server URL
    ldap.provider.url=ldap://ldap.example.com:389

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Bind DN template for user authentication (%s is replaced with the username)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Bind DN and password for the search service account
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filter for role resolution
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   The ``%s`` placeholder is processed by Java's ``String.format()``.
   ``ldap.security.principal``, ``ldap.account.filter``, ``ldap.group.filter``, and the
   administration filters all use the ``%s`` format (not the ``{0}`` format).
   Note that usernames passed to filters are automatically escaped inside |Fess| as a
   protection against LDAP injection.

LDAP Administration and Behavior Settings
==========================================

The following properties are defined in ``app/WEB-INF/classes/fess_config.properties``.
Edit this file to change their values.

Enabling the Administration Feature
------------------------------------

.. list-table:: Administration Feature Properties
   :header-rows: 1
   :widths: 35 15 50

   * - Property
     - Default
     - Description
   * - ``ldap.admin.enabled``
     - ``false``
     - Enables the ability to create, update, and delete LDAP users, roles, and groups from the administration screen. **Not required for login authentication** — LDAP login works without enabling this.
   * - ``ldap.admin.sync.password``
     - ``true``
     - Synchronizes the |Fess| password with LDAP when a user is updated from the administration screen.
   * - ``ldap.auth.validation``
     - ``true``
     - Validates LDAP authentication at login.

Filters and Base DNs for User, Role, and Group Administration
--------------------------------------------------------------

Used to operate LDAP entries from the administration screen when ``ldap.admin.enabled=true``.

.. list-table:: Administration Filters and Base DNs
   :header-rows: 1
   :widths: 38 47 15

   * - Property
     - Description
     - Default
   * - ``ldap.admin.user.filter``
     - User search filter (``%s`` is replaced with the username)
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - User search base DN
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - objectClass values for user creation
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - Role search filter
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - Role search base DN
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - objectClass values for role creation
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - Group search filter
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - Group search base DN
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - objectClass values for group creation
     - ``groupOfNames``

Role Resolution and Behavior Control
--------------------------------------

Controls the behavior of role and group resolution after login.

.. list-table:: Behavior Control Properties
   :header-rows: 1
   :widths: 40 15 45

   * - Property
     - Default
     - Description
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - Grants a role based on the username.
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - Grants roles based on group membership.
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - Grants roles based on LDAP roles.
   * - ``ldap.allow.empty.permission``
     - ``true``
     - Allows login for users who have no groups or roles.
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - Strips the NetBIOS name prefix (``DOMAIN\`` format) from group names and similar values.
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - Allows underscores in group names.
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - Converts permission names to lowercase.
   * - ``ldap.samaccountname.group``
     - ``false``
     - Uses the ``sAMAccountName`` attribute for group names (for Active Directory).
   * - ``ldap.max.username.length``
     - ``-1``
     - A typed username longer than this is cut to its first this-many characters (meant for the 20-character logon name of an old Active Directory). The cut name is used for the bind, the user name, the role search, the permission names and the session, and the login is never refused for its length. A negative value (the default ``-1``) does not cut.

.. note::
   For a login with an LDAP username and password, blanks around the typed username are removed (blanks inside the name are kept). The cut is made after that, and a blank left at the end of the cut name is removed as well.

LDAP Role Organizational Units and Nested Groups
------------------------------------------------

Whether a group entry gives a role (permission prefix ``role.search.role.prefix``, default ``R``) or a group (``role.search.group.prefix``, default ``2``) is decided by its DN. For what changed from 15.9, see :doc:`../install/upgrade`.

15.10 parses the DN and treats an entry as a role only when one of its ``ou`` components is exactly ``Role`` or ``Roles`` (case-insensitive). Every other entry is a group, and so is an entry whose DN cannot be parsed.

When ``ldap.group.filter`` is set (it is blank by default), |Fess| uses it to look up the groups that contain the groups of the user (nested groups). Up to 15.9, the DNs of the user's groups were put into that filter without escaping. A DN with an escaped character, such as the comma of ``CN=Sales\, EMEA,...``, did not match, so the nested groups of such a group were silently missing, and a DN that contained characters special to LDAP filters changed the filter. 15.10 escapes the DNs (RFC 4515). The nested groups of such groups are now found, so the users concerned get the permissions of those groups, too.

Reserved Admin User Names
-------------------------

The names listed in ``authentication.admin.users`` are reserved by |Fess| for itself. For SSO they act
as a block list: ``SpnegoAuthenticator`` resolves no credential for a name that matches one, and form
login does not take such a name to LDAP either.

A directory does not distinguish case in an account name -- Active Directory issues a ticket for any
casing of one -- so comparing the reserved names exactly lets the same account log in simply by
changing the spelling. ``authentication.admin.users.ignore.case`` decides how they are compared.

.. list-table:: Comparison of Reserved Names
   :header-rows: 1
   :widths: 40 15 45

   * - Property
     - Default
     - Description
   * - ``authentication.admin.users``
     - ``admin``
     - Reserved admin user names, separated by commas.
   * - ``authentication.admin.users.ignore.case``
     - ``auto``
     - How the reserved names are compared. ``auto`` ignores case only when ``ldap.provider.url`` is set, and compares exactly when it is not. ``true`` and ``false`` decide it outright.

.. note::
   Where ``ldap.provider.url`` is set, ``auto`` ignores case. A directory account whose name differs from a reserved one only in case can then no longer log in, and is no longer synchronised to the directory from the admin UI. Set ``authentication.admin.users.ignore.case=false`` to keep comparing the names exactly.

.. _local-username-policy:

Local User Name Policy
----------------------

|Fess| compares the names of local users (the users of the user management screen, not the users of LDAP or SSO) exactly as typed. ``Alice``, ``alice`` and ``ＡＬＩＣＥ`` (full-width letters) are three users, each with its own login. ``authentication.local.username.policy`` decides whether creating or renaming a local user also refuses a name that differs from the name of another user only in case, width or Unicode composition.

.. list-table:: Policy for Local User Names
   :header-rows: 1
   :widths: 40 15 45

   * - Property
     - Default
     - Description
   * - ``authentication.local.username.policy``
     - ``preserved``
     - ``preserved`` compares names exactly as typed, as in 15.9. ``mapped`` refuses a new or renamed name that is the same as the name of another user once it is mapped (see below). The value is compared without regard to case. An unknown value is treated as ``preserved`` and logged once as a warning.

With ``mapped``, creating or renaming a user on the user management screen or with the Admin API (``POST`` and ``PUT`` of ``/api/admin/user/setting``) is refused in two cases:

- The mapped name is the mapped name of another user. The mapping is that of RFC 8265 ``UsernameCaseMapped``: the full-width and half-width forms (such as half-width katakana) and the ideographic space are replaced by their decomposition mapping, the case is lowered with the root locale, and the result is put in Unicode normalization form C (not NFKC). ``Alice``, ``alice`` and ``ＡＬＩＣＥ`` are the same name once mapped.
- The name is a different spelling of an entry of ``authentication.admin.users`` (see above). ``admin`` can still be created again, because it is the entry as written, while ``Admin``, ``ADMIN`` and the full-width spelling are refused.

A user who is saved under the name it already has is never refused, so users that collide today can still be edited. When |Fess| starts with ``mapped``, it writes one warning to ``fess.log`` that lists up to 20 groups of stored names that are the same once mapped and up to 20 stored names that contain whitespace or control characters. Nothing is changed by it: those users can still log in and be edited.

.. note::

   The policy only decides whether a name is accepted. It does not change login, which looks a user up by the name exactly as typed, the user ID or the stored name. It does not change the permission strings made from a name (``{user}Alice`` and ``{user}alice`` in a role filter, in the permissions of a crawl configuration or in a document) or the documents already indexed. It does not enforce the character rules of RFC 8265 either: a name with spaces, symbols or control characters is still accepted.

   The check is not applied by a backup restore, by the creation of the initial ``admin`` user at the first start or by a direct write to the user index. Two administrators who create ``Alice`` and ``alice`` at the same moment can both succeed, because no mapped name is stored. Folding names at login and in permissions would need a migration of the stored users, roles and indexed documents, and is not part of this setting.

Attribute Mapping
-----------------

The mapping between LDAP attributes and |Fess| user attributes is defined via ``ldap.attr.*``
properties. These normally do not need to be changed, but can be adjusted when the schema
differs. Representative examples:

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   Some property names do not match their corresponding LDAP attribute names — for example,
   ``ldap.attr.state`` maps to ``st`` and ``ldap.attr.city`` maps to ``l``.
   For the complete list, refer to lines beginning with ``ldap.attr.`` in
   ``fess_config.properties``.

Active Directory Configuration
==============================

Configuration example for Microsoft Active Directory (``system.properties`` or the
administration screen).

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Bind DN template for user authentication (UPN format)
    ldap.security.principal=%s@example.com

    # Search service account
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Account filter
    ldap.account.filter=sAMAccountName=%s

    # Use memberOf attribute
    ldap.memberof.attribute=memberOf

    # Group filter
    ldap.group.filter=(member=%s)

To resolve nested groups, you can use the Active Directory-specific
``LDAP_MATCHING_RULE_IN_CHAIN``.

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

OpenLDAP Configuration
======================

Configuration example for OpenLDAP.

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Bind DN template for user authentication
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Search service account
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Account filter
    ldap.account.filter=uid=%s

    # Group filter (for posixGroup)
    ldap.group.filter=(memberUid=%s)

.. note::

   Standard OpenLDAP does not have the ``memberOf`` attribute, so groups are resolved using
   ``ldap.group.filter``. If the ``memberof`` overlay is enabled, ``ldap.memberof.attribute``
   can also be used.

Security Settings
=================

LDAPS (SSL/TLS)
---------------

Use an encrypted connection:

::

    # Use LDAPS
    ldap.provider.url=ldaps://ldap.example.com:636

For self-signed certificates, import the certificate into the Java truststore.

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Password Protection
-------------------

``ldap.admin.security.credentials`` is stored in ``system.properties``.
Credentials configured from the administration screen are stored encrypted internally.
Restrict file permissions appropriately.

Failover
========

To fail over to multiple LDAP servers, specify multiple URLs separated by spaces in
``ldap.provider.url``.

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Troubleshooting
===============

Connection Error
----------------

**Symptom**: LDAP connection fails

**Check**:

1. Is the LDAP server running?
2. Is the port open in the firewall (389 or 636)?
3. Is ``ldap.provider.url`` correct (``ldap://`` or ``ldaps://``)?
4. Are ``ldap.admin.security.principal`` and the password correct?

Authentication Error
--------------------

**Symptom**: User authentication fails

**Check**:

1. Is the ``ldap.security.principal`` template correct (does it contain ``%s``)?
2. Does the user exist within the specified base DN?
3. Is ``ldap.account.filter`` correct?

Cannot Retrieve Groups or Roles
--------------------------------

**Symptom**: Cannot retrieve user groups or roles

**Check**:

1. Is ``ldap.group.filter`` correct?
2. Is ``ldap.memberof.attribute`` correct (for Active Directory)?
3. Do the groups exist within the search base DN?
4. Are the ``ldap.role.search.*.enabled`` properties enabled?

Cannot Manage Users from the Administration Screen
--------------------------------------------------

**Symptom**: Cannot create, edit, or delete LDAP users from the administration screen

**Check**:

1. Is ``ldap.admin.enabled`` set to ``true``?
2. Are the administration base DNs such as ``ldap.admin.user.base.dn`` correct?
3. Does the ``ldap.admin.security.principal`` service account have write permissions?

Debug Settings
--------------

To output detailed logs, add a logger to ``app/WEB-INF/classes/log4j2.xml``.

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Reference Information
=====================

- :doc:`security-role` - Role-Based Access Control
- :doc:`sso-spnego` - SPNEGO (Kerberos) Authentication
- :doc:`../admin/user-guide` - User Management Guide
