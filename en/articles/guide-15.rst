=============================================
Protecting Search with SSO and Access Control
=============================================

Introduction
============

An internal search platform gathers documents protected by permissions.
Rather than handing out Fess-specific passwords, most deployments want users to sign in through the organization's identity provider (IdP) and have search results narrowed by the groups they belong to.

In this article, we configure the following in Fess 15.9 and go as far as confirming that each of them works.

- Single sign-on (SSO) with Entra ID, OpenID Connect, SAML, or SPNEGO
- "Login Required", so that users who are not logged in cannot search
- Making Fess correctly recognize HTTPS behind a reverse proxy that terminates TLS
- Reviewing access tokens and the retention periods of the audit log and search log

How to design roles and groups, and how to write them in the permissions of crawl configurations, is covered in :doc:`guide-05`.

SSO Is Provided by Plugins
==========================

In Fess 15.9, the SSO authentication logic was split out of the core into four plugins.

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - Method
     - Plugin
     - "SSO Type" (``sso.type``)
     - Source of the user name
     - Source of groups and roles
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID (``entraid``)
     - The user name of the signed-in account (usually the UPN)
     - Groups and roles retrieved through Microsoft Graph
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect (``oic``)
     - The ``email`` claim of the ID Token
     - The ``groups`` claim of the ID Token. Roles come only from "Default Roles"
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML (``saml``)
     - The NameID of the assertion
     - The values of the attributes named in "Group Attribute Name" (default ``memberOf``) and "Role Attribute Name"
   * - SPNEGO (Kerberos)
     - ``fess-sso-spnego``
     - SPNEGO (``spnego``)
     - The part of the Kerberos principal before ``@``
     - Groups retrieved through the LDAP settings in [General]

OpenID Connect is the only one whose plugin name (``oidc``) differs from its ``sso.type`` value (``oic``).

The procedure is the same for every method.

1. Install the plugin and restart Fess
2. Register Fess with the IdP. The return address (redirect URI or ACS URL) is ``https://<Fess host>/sso/``
3. In the admin console, under [System] > [General], enter the IdP information in the section for the method, select the "SSO Type", and update
4. Open ``https://<Fess host>/sso/`` in a browser and confirm that you can log in through the IdP

Installing the Plugin
---------------------

The Docker image (``ghcr.io/codelibs/fess:15.9.0``) includes the four SSO plugins (images with ``-slim`` in their name do not).
They are not bundled with the ZIP, DEB, and RPM packages, so install them from [Install] in [System] > [Plugin], or with the following command.

::

    $ bin/fess-setup install plugin fess-sso-entraid

Restart Fess after installing or removing a plugin.
Use a plugin of the same minor version as Fess (15.9.x).

If you select an "SSO Type" without the plugin installed, ``/sso/`` just returns to the login page, and a WARN ``No SSO authenticator is registered as ...`` is written once to ``fess.log``.

Where the Settings Are Stored
-----------------------------

The values entered in [General] are saved to ``system.properties`` (``app/WEB-INF/conf/`` for the ZIP package, ``/etc/fess/`` for DEB and RPM).
The OpenID Connect, SAML, and Entra ID settings are read on every login, so they take effect as soon as they are saved, without a restart.
The SPNEGO settings are shared by the whole process, so a restart is required after changing them.

The ``fess01`` container in Docker has no volume, so the [General] settings are lost when you run ``docker compose down`` and then ``up``.
Before recreating the container, download ``system.properties`` from [System Info] > [Backup], and after recreating it, upload the file from the same screen to restore the settings.

SSO with Entra ID
=================

For organizations using Microsoft 365, ``fess-sso-entraid`` is the easiest choice.
Groups are retrieved from Microsoft Graph after login, so there is no need to configure group claims on the IdP side.

Entra ID Settings
-----------------

Create a new registration under "App registrations" in the Azure Portal, and configure it as follows.

- Supported account types: Accounts in this organizational directory only
- Redirect URI: ``https://fess.example.com/sso/`` with the platform "Web" (it must match exactly, including the trailing ``/``)
- Under "Certificates & secrets", create a client secret and note down its value (it is shown only right after creation)
- Under "API permissions", add the Microsoft Graph delegated permissions ``User.Read`` and ``GroupMember.Read.All``, and grant admin consent

Without ``GroupMember.Read.All``, nested parent groups cannot be retrieved, and a warning ``Not allowed to read the parent groups of ...`` is written to ``fess.log``.

Fess Settings
-------------

Enter the values in the "Entra ID" section of [System] > [General].

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Field
     - Key
     - Value
   * - Tenant (ID or Domain)
     - ``entraid.tenant``
     - The Directory (tenant) ID, or ``yourcompany.onmicrosoft.com``
   * - Client ID
     - ``entraid.client.id``
     - The Application (client) ID
   * - Client Secret
     - ``entraid.client.secret``
     - The value of the secret you created
   * - Reply URL
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

Finally, select "Entra ID" for "SSO Type" in the "System" section and click [Update].

Matching Groups with Document Permissions
-----------------------------------------

For the groups and roles obtained from Entra ID, their ID (GUID) always becomes a permission.
In addition, the values of the attributes listed in "Permission Fields" (``entraid.permission.fields``, default ``mail``) also become permissions.

Security groups are not mail-enabled, so with the default only their GUID becomes a permission.
If the ACLs on your file server are written with group names, set "Permission Fields" to ``mail,displayName``.
However, ``displayName`` is not unique, so a group with the same name as a Windows built-in group (such as ``Administrators``) also matches the documents of that built-in group.

In the permissions of a crawl configuration, write the retrieved value as is, prefixed with ``{group}`` (for example, ``{group}sales@example.com``).

.. warning::

   "Default Roles" (``entraid.default.roles``) are given to every user in the tenant.
   If you put ``admin`` here, everyone can enter the admin console.

SSO with OpenID Connect, SAML, or SPNEGO
========================================

OpenID Connect
--------------

Use ``fess-sso-oidc`` to integrate with OpenID Connect providers such as Keycloak or Okta.
On the provider side, register Fess as a web application (client) and set the redirect URI to ``https://fess.example.com/sso/``.

The main fields to enter in the "OpenID Connect" section of [General] are as follows.

- Authorization Server URL (``oic.auth.server.url``) and Token Server URL (``oic.token.server.url``): enter each value from the provider's ``/.well-known/openid-configuration``. The Token Server URL must use ``https`` (``http`` is allowed only for ``localhost``, ``127.x.x.x``, and ``::1``)
- Client ID and Client Secret
- Scope: ``openid email``. The user name is taken from the ``email`` claim, so ``email`` is required
- Base URL (``oic.base.url``): ``https://fess.example.com``. If you leave Redirect URL empty, it becomes ``{Base URL}/sso/``

For groups, the values of the ``groups`` claim in the ID Token become permissions as they are.
Unlike Entra ID, parent groups are not followed, so if you need nested groups, include them in the claim on the provider side.
Roles are not taken from claims; only the values of "Default Roles" are given.

``oic.issuer``, which validates the issuer (``iss``), has no field in [General], so write it directly in ``system.properties``.

SAML
----

With ``fess-sso-saml``, Fess acts as the SP.
The IdP returns the assertion with a cross-site POST, so login does not complete with the default ``tomcat.sameSiteCookies = lax``.
Change it as follows in ``tomcat_config.properties`` and restart Fess.

::

    tomcat.sameSiteCookies = none

``none`` works only over HTTPS.
Over plain HTTP you will no longer be able to log in, so complete the HTTPS configuration described later first.

Enter the following in the "SAML" section of [General].

- SP Base URL (``saml.sp.base.url``): ``https://fess.example.com``. This determines the SP Entity ID (``{SP Base URL}/sso/metadata``) and the ACS URL (``{SP Base URL}/sso/``)
- IdP Entity ID, IdP SSO URL, and IdP X.509 Certificate: copy them from the IdP's admin console. For the certificate, enter the Base64 text on a single line, without the ``-----BEGIN CERTIFICATE-----`` lines
- Group Attribute Name (default ``memberOf``) and Role Attribute Name: match the attribute names the IdP sends

There is no feature to load the IdP's metadata URL.
Conversely, Fess's SP metadata is available at ``https://fess.example.com/sso/metadata`` and can be loaded into the IdP.
The user name is the NameID, and the NameID format defaults to the email address format.
Only SP-initiated login, which starts at Fess's ``/sso/``, is supported; logins started from a tile in the IdP's portal are rejected.

In production, add ``saml.security.want_assertions_signed=true`` to ``system.properties`` to require signed assertions.
The signing and encryption settings have no fields in [General] and cannot be specified as JVM system properties either, so write them directly in the file.

.. warning::

   When "Role Attribute Name" is set, the values sent by the IdP become Fess roles as they are.
   The administrator role is ``authentication.admin.roles=admin``, so a user for whom the IdP sends ``admin`` becomes an administrator.

SPNEGO (Windows Integrated Authentication)
------------------------------------------

To let users on domain-joined Windows machines log in without entering a password, use ``fess-sso-spnego``.
It requires registering an SPN in AD (``setspn -S HTTP/<Fess host name> <service account>``), creating ``krb5.conf`` and ``auth_login.conf`` in ``app/WEB-INF/classes/``, and configuring the browser's intranet settings.
Groups are retrieved from AD using the settings in the "LDAP" section of [General].
Follow the procedure in `SSO Configuration with Windows Integrated Auth <https://fess.codelibs.org/stable/config/sso-spnego.html>`__, and restart Fess after changing the SPNEGO fields in [General].

Confirming That SSO Works
=========================

First, while logged out, open ``https://fess.example.com/sso/`` and confirm that you are taken to the IdP's login screen.

After logging in, open ``https://fess.example.com/api/v2/auth/me`` in the same browser.

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

Check that ``groups`` contains the groups you expect and that ``admin`` is as intended.
With Entra ID, groups are retrieved after login, so ``permission_state`` is ``PENDING`` right after login and changes to ``RESOLVED`` once retrieval completes.

The audit log ``audit.log`` also records a ``LOGIN`` line with the user name and permissions.

If login fails, you are returned to the login screen with the message "SSO login process failed."
The cause is written to ``fess.log`` as a WARN (such as ``Failed to process SSO login``).

Even if the SSO settings are wrong, you can log in as the local ``admin`` user from ``/login/`` and fix them.

.. note::

   Logged-in users are not given ``{role}guest``.
   Documents from crawl configurations that have only the default ``{role}guest`` disappear from the search results of users who log in with SSO.
   For how to put permissions together, see :doc:`guide-05`.

Preventing Users Who Are Not Logged In from Searching
=====================================================

When you enable "Login Required" in [System] > [General], users who are not logged in can no longer search.

- If SSO is available (the plugin is installed and an "SSO Type" is selected), users who open the search page of the bundled ``bootstrap`` theme are automatically sent to ``/sso/``, and after logging in at the IdP they return to their original search
- Without SSO, a login dialog is shown on the search page
- The search API under ``/api/v2/`` can no longer be used anonymously either; only calls with an access token are accepted

Even without enabling "Login Required", if SSO is available and "Show Login Link" is enabled, the login link on the search page points to ``/sso/``.

Publishing over HTTPS
=====================

Terminating TLS at a Reverse Proxy
----------------------------------

In a setup where Nginx or a similar proxy terminates TLS and forwards to Fess over HTTP, the requests Fess receives look like ``http://``.
As is, SAML assertion validation (matching the ``Destination``) fails, and SPNEGO does not offer the Basic authentication fallback.

In ``tomcat_config.properties``, tell Fess the scheme and port seen from outside.
This file is in ``lib/classes/`` for the ZIP package, and in ``/etc/fess/`` for DEB, RPM, and the Docker image.

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

On the proxy side, pass the original ``Host`` header through to Fess (with Nginx, ``proxy_set_header Host $host;``).
This is because Fess builds the host name of the request URL from the ``Host`` header.

In addition, set ``session.cookie.secure=true`` in ``fess_config.properties`` to add the ``Secure`` attribute to the session cookie.
The default (empty) leaves the decision to Tomcat, but in production environments where a proxy terminates TLS, set ``true`` explicitly.
When you use ``tomcat.sameSiteCookies = none`` for SAML, ``SameSite=None`` cookies also require the ``Secure`` attribute.

Both files require a restart of Fess after changes.

Accepting TLS Directly in Fess
------------------------------

Without a proxy, set ``tomcat.SSLEnabled=true``, ``tomcat.certificateKeystoreFile``, ``tomcat.certificateKeystorePassword``, ``tomcat.certificateKeyAlias``, and so on in ``tomcat_config.properties``.
For a configuration example, see `Security Configuration <https://fess.codelibs.org/stable/install/security.html>`__.

Closing the OpenSearch Port
---------------------------

The ``compose-opensearch3.yaml`` of docker-fess exposes OpenSearch, with its security plugin disabled, on port 9200 of the host.
Fess connects over the network between the containers (``http://search01:9200``), so on a shared server you can remove ``ports`` from ``search01``.

Managing Access Tokens
======================

Tokens for calling the API from business systems are created in [System] > [Access Token].
How to call the API is covered in :doc:`guide-11`, so here we only list the points for operating tokens safely.

- Give a search token only the permissions of the documents that system is allowed to see (for example, ``{group}sales``)
- A token with ``{role}admin-api`` can use not only document registration but every Admin API endpoint. There is no narrower permission such as "registration only"
- Set "Expires", and recreate the token when it expires. Delete tokens that are no longer needed
- Keep tokens on the server side; do not embed them in JavaScript that runs in the browser
- Leave "Parameter Name" empty. If you set it, permissions can be added through a URL parameter
- Treat the ``admin-accesstoken`` role, which can issue tokens, and the ``admin-accesstoken-view`` role, which can display their values, as equivalent to administrators

Deciding How Long to Keep Logs
==============================

Log file locations and monitoring are covered in :doc:`guide-10`.
Here, we sort out the records used for security reviews and their retention periods.

The audit log (``audit.log``) records, one line each, logins (``LOGIN``), login failures (``LOGIN_FAILURE``), logouts (``LOGOUT``), access to the admin console and the Admin API (``ACCESS``), denials due to insufficient privileges (``ACCESS_DENIED``), and more.
The file is written to ``logs/`` for the ZIP package, and to ``/var/log/fess/`` for DEB, RPM, and the Docker image, and can also be downloaded from [System Info] > [Log File].
The default format is LTSV; in the Docker image it is JSON in ECS format.
Rotated files are deleted after 360 days (``backup.audit.max.age`` in ``log4j2.xml``).

Who searched for what is recorded in the search log stored in OpenSearch, which you can review in [System Info] > [Search Log].
The default for "Delete old search logs" in [General] is ``-1``, which keeps search logs without deleting them.
This number of days also applies to the click log, the favorite log, and the chat log.
If your internal rules define a retention period, enter that number of days.

Running Multiple Instances
==========================

In Fess 15.9, login sessions are held in the memory of each Fess process.
The values used during SSO (the OpenID Connect ``state`` and the SAML AuthnRequest ID) are also stored in the session, so when you place multiple instances behind a load balancer, enable sticky sessions so that the same user is always routed to the same Fess.
For multi-instance configurations themselves, see :doc:`guide-14`.

Note that storing sessions in OpenSearch to share them among multiple instances, and passkey login for local users, are features of 15.10 and later.

What to Read Next
=================

- Designing roles and groups, and writing permissions in crawl configurations: :doc:`guide-05`
- API integration with access tokens: :doc:`guide-11`
- Log locations, monitoring, and backups: :doc:`guide-10`
- Scaling out to multiple instances: :doc:`guide-14`
- Reflecting file server ACLs in search results: :doc:`file-server-search`

References
==========

- `SSO Configuration with Entra ID <https://fess.codelibs.org/stable/config/sso-entraid.html>`__
- `SSO Configuration with OpenID Connect <https://fess.codelibs.org/stable/config/sso-oidc.html>`__
- `SAML Authentication SSO Setup <https://fess.codelibs.org/stable/config/sso-saml.html>`__
- `SSO Configuration with Windows Integrated Auth <https://fess.codelibs.org/stable/config/sso-spnego.html>`__
- `General Settings <https://fess.codelibs.org/stable/admin/general-guide.html>`__
- `Access Token <https://fess.codelibs.org/stable/admin/accesstoken-guide.html>`__
- `Security Configuration <https://fess.codelibs.org/stable/install/security.html>`__
- `Log Configuration <https://fess.codelibs.org/stable/config/admin-logging.html>`__
