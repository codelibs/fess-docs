================================================
SSO Configuration with Windows Integrated Auth
================================================

Overview
========

|Fess| supports Single Sign-On (SSO) authentication using Windows Integrated Authentication (SPNEGO/Kerberos).
By using Windows Integrated Authentication, users who are logged into a Windows domain-joined computer can access |Fess| without additional login operations.

How Windows Integrated Authentication Works
-------------------------------------------

In Windows Integrated Authentication, |Fess| uses the SPNEGO (Simple and Protected GSSAPI Negotiation Mechanism) protocol for Kerberos authentication.

1. User logs into the Windows domain
2. User accesses |Fess|
3. |Fess| sends an SPNEGO challenge
4. Browser obtains a Kerberos ticket and sends it to the server
5. |Fess| validates the ticket and retrieves the username
6. User's group information is retrieved via LDAP
7. User is logged in and group information is applied to role-based search

For role-based search integration, see :doc:`security-role`.

Prerequisites
=============

Before configuring Windows Integrated Authentication, verify the following prerequisites:

- |Fess| 15.7 or later is installed
- An Active Directory (AD) server is available
- |Fess| server is accessible from the AD domain
- You have permission to configure Service Principal Names (SPN) in AD
- An account for retrieving user information via LDAP is available

Active Directory Side Configuration
====================================

Registering Service Principal Name (SPN)
-----------------------------------------

You need to register an SPN for |Fess| in Active Directory.
Open a command prompt on a Windows computer joined to the AD domain and run the ``setspn`` command.

::

    setspn -S HTTP/<Fess server hostname> <AD access user>

Example:

::

    setspn -S HTTP/fess-server.example.local svc_fess

To verify the registration:

::

    setspn -L <AD access user>

.. note::
   After registering the SPN, if you ran the command on the Fess server, log out of Windows and log back in.

Basic Configuration
===================

Enabling SSO
------------

To enable Windows Integrated Authentication, add the following setting in ``app/WEB-INF/conf/system.properties``:

::

    sso.type=spnego

Kerberos Configuration File
----------------------------

Create ``app/WEB-INF/classes/krb5.conf`` with the Kerberos configuration.

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

.. note::
   Replace ``EXAMPLE.LOCAL`` with your AD domain name (uppercase) and ``AD-SERVER.EXAMPLE.LOCAL`` with your AD server hostname.

Login Configuration File
------------------------

Create ``app/WEB-INF/classes/auth_login.conf`` with the JAAS login configuration.

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

.. note::
   ``krb5.conf`` and ``auth_login.conf`` have their default filenames set via ``spnego.krb5.conf`` / ``spnego.login.conf``, but the files themselves must be created.
   If these files do not exist on the classpath, SPNEGO initialization will fail and |Fess| will not start.

Required Settings
-----------------

Add the following settings to ``app/WEB-INF/conf/system.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``spnego.preauth.username``
     - AD connection username
     - (Required)
   * - ``spnego.preauth.password``
     - AD connection password
     - (Required)
   * - ``spnego.krb5.conf``
     - Kerberos configuration file path
     - ``krb5.conf``
   * - ``spnego.login.conf``
     - Login configuration file path
     - ``auth_login.conf``

Optional Settings
-----------------

The following settings can be added as needed.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``spnego.login.client.module``
     - Client module name
     - ``spnego-client``
   * - ``spnego.login.server.module``
     - Server module name
     - ``spnego-server``
   * - ``spnego.allow.basic``
     - Allow Basic authentication
     - ``true``
   * - ``spnego.allow.unsecure.basic``
     - Allow unsecure Basic authentication
     - ``true``
   * - ``spnego.prompt.ntlm``
     - Fall back to Basic authentication when an NTLM token is received
     - ``true``
   * - ``spnego.allow.localhost``
     - Allow localhost access
     - ``true``
   * - ``spnego.allow.delegation``
     - Allow delegation
     - ``false``
   * - ``spnego.exclude.dirs``
     - Directories to exclude from authentication (comma-separated)
     - (None)
   * - ``spnego.logger.level``
     - Internal log level of the SPNEGO library (``1`` =FINEST, ``2`` =FINER, ``3`` =FINE, ``4`` =CONFIG, ``6`` =WARNING, ``7`` =SEVERE; any other value including ``0`` and ``5`` is treated as INFO)
     - (Auto)

.. warning::
   ``spnego.allow.unsecure.basic=true`` may send Base64-encoded credentials over unencrypted connections.
   For production environments, it is strongly recommended to set this to ``false`` and use HTTPS.

.. note::
   When ``spnego.prompt.ntlm=true`` (the default), ``spnego.allow.basic`` must also be ``true``.
   If you set ``spnego.allow.basic=false``, you must also set ``spnego.prompt.ntlm=false``.
   If this condition is not met, an error will occur during SPNEGO initialization.

.. note::
   ``spnego.logger.level`` controls the log level of the SPNEGO library's internal logger (a ``java.util.logging`` logger named ``Spnego``).
   When not set, the level is determined automatically based on the |Fess| log level.

LDAP Configuration
==================

LDAP configuration is required to retrieve group information for users authenticated via Windows Integrated Authentication.
Configure LDAP settings in the |Fess| admin panel under "System" -> "General".

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Example
   * - LDAP URL
     - ``ldap://AD-SERVER.example.local:389``
   * - Base DN
     - ``dc=example,dc=local``
   * - Bind DN
     - ``svc_fess@example.local``
   * - Password
     - Password for AD access user
   * - User DN
     - ``%s@example.local``
   * - Account Filter
     - ``(&(objectClass=user)(sAMAccountName=%s))``
   * - memberOf Attribute
     - ``memberOf``

Browser Settings
================

Client browser settings are required to use Windows Integrated Authentication.

Internet Explorer / Microsoft Edge
-----------------------------------

1. Open Internet Options
2. Select the "Security" tab
3. Click "Sites" for the "Local intranet" zone
4. Click "Advanced" and add the Fess URL
5. Click "Custom level" for the "Local intranet" zone
6. Under "User Authentication" -> "Logon", select "Automatic logon only in Intranet zone"
7. In the "Advanced" tab, check "Enable Integrated Windows Authentication"

Google Chrome
-------------

Chrome typically uses the Windows Internet Options settings.
If additional configuration is needed, set ``AuthServerAllowlist`` via Group Policy or registry.

Mozilla Firefox
---------------

1. Enter ``about:config`` in the address bar
2. Search for ``network.negotiate-auth.trusted-uris``
3. Set the Fess server URL or domain (e.g., ``https://fess-server.example.local``)

Configuration Examples
======================

Minimal Configuration (for Testing)
-------------------------------------

The following is a minimal configuration example for a test environment.

``app/WEB-INF/conf/system.properties``:

::

    # Enable SSO
    sso.type=spnego

    # SPNEGO settings
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-password

``app/WEB-INF/classes/krb5.conf``:

::

    [libdefaults]
        default_realm = EXAMPLE.LOCAL
        default_tkt_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        default_tgs_enctypes = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc
        permitted_enctypes   = aes128-cts rc4-hmac des3-cbc-sha1 des-cbc-md5 des-cbc-crc

    [realms]
        EXAMPLE.LOCAL = {
            kdc = AD-SERVER.EXAMPLE.LOCAL
            default_domain = EXAMPLE.LOCAL
        }

    [domain_realm]
        example.local = EXAMPLE.LOCAL
        .example.local = EXAMPLE.LOCAL

``app/WEB-INF/classes/auth_login.conf``:

::

    spnego-client {
        com.sun.security.auth.module.Krb5LoginModule required;
    };

    spnego-server {
        com.sun.security.auth.module.Krb5LoginModule required
        storeKey=true
        isInitiator=false;
    };

Recommended Configuration (for Production)
-------------------------------------------

The following is a recommended configuration example for production environments.

``app/WEB-INF/conf/system.properties``:

::

    # Enable SSO
    sso.type=spnego

    # SPNEGO settings
    spnego.preauth.username=svc_fess
    spnego.preauth.password=your-secure-password
    spnego.krb5.conf=krb5.conf
    spnego.login.conf=auth_login.conf

    # Security settings (production)
    spnego.allow.basic=false
    spnego.allow.unsecure.basic=false
    spnego.prompt.ntlm=false
    spnego.allow.localhost=false

.. note::
   When setting ``spnego.allow.basic=false``, you must also set ``spnego.prompt.ntlm=false``.
   Since ``spnego.prompt.ntlm`` defaults to ``true``, omitting this setting will cause an error during initialization.

Troubleshooting
===============

Common Issues and Solutions
----------------------------

Authentication Dialog Appears
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the Fess server is added to the Local Intranet zone in browser settings
- Check that "Enable Integrated Windows Authentication" is enabled
- Verify that the SPN is correctly registered (``setspn -L <username>``)

Authentication Errors Occur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the domain name (uppercase) and AD server name in ``krb5.conf`` are correct
- Check that ``spnego.preauth.username`` and ``spnego.preauth.password`` are correct
- Verify network connectivity to the AD server

Cannot Retrieve Group Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that LDAP settings are correct
- Check that Bind DN and password are correct
- Verify that the user belongs to groups in AD

Debug Settings
--------------

To investigate issues, you can output detailed SPNEGO-related logs.

To output verbose internal logs from the SPNEGO library, add the following to ``app/WEB-INF/conf/system.properties``.
``spnego.logger.level=1`` outputs the most detailed logs (FINEST).

::

    spnego.logger.level=1

To output detailed logs for the |Fess|-side SPNEGO integration processing (the ``org.codelibs.fess.sso.spnego`` package), add the following logger to ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.spnego" level="DEBUG"/>

.. note::
   The SPNEGO library itself outputs logs via ``java.util.logging``, so its log level is controlled by ``spnego.logger.level`` rather than ``log4j2.xml``.
   The |Fess|-side integration logs are controlled by the ``log4j2.xml`` logger.

Reference
=========

- :doc:`security-role` - Role-based search configuration
- :doc:`sso-saml` - SSO configuration with SAML authentication
- :doc:`sso-oidc` - SSO configuration with OpenID Connect authentication
- :doc:`sso-entraid` - SSO configuration with Microsoft Entra ID
