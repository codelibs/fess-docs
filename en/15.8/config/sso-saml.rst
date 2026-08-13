=============================
SAML Authentication SSO Setup
=============================

Overview
========

|Fess| supports Single Sign-On (SSO) authentication using SAML (Security Assertion Markup Language) 2.0.
By using SAML authentication, user information authenticated by an IdP (Identity Provider) can be integrated with |Fess|, enabling role-based search results based on user permissions when combined with role-based search.

How SAML Authentication Works
-----------------------------

In SAML authentication, |Fess| operates as an SP (Service Provider) and collaborates with an external IdP for authentication.

1. User accesses the |Fess| SSO endpoint (``/sso/``)
2. |Fess| redirects the authentication request to the IdP
3. User authenticates at the IdP
4. IdP sends SAML assertion to |Fess|
5. |Fess| validates the assertion and logs in the user

.. note::
   Only SP-initiated login, which starts at the |Fess| SSO endpoint (``/sso/``) as shown above, is supported.
   |Fess| binds every SAML response to the ID of the AuthnRequest it sent, so an IdP-initiated
   (unsolicited) response, for example from a |Fess| tile on an Okta dashboard or in the Microsoft
   Entra ID "My Apps" portal, has no AuthnRequest to match against and is rejected.
   If you place a tile on the IdP side, point it at the |Fess| ``/sso/`` endpoint.

   Note that in 15.7 an IdP-initiated login happened to work when ``tomcat.sameSiteCookies=none``
   was set: |Fess| bounced the unmatched response back to the IdP, and the IdP immediately returned
   a solicited assertion. 15.8 no longer bounces the response, so IdP-initiated login does not work.

For role-based search integration, see :doc:`security-role`.

Prerequisites
=============

Before configuring SAML authentication, verify the following prerequisites:

- |Fess| 15.8 or later is installed
- A SAML 2.0 compatible IdP (Identity Provider) is available
- |Fess| is accessible via HTTPS (required for production environments)
- You have permission to register |Fess| as an SP on the IdP side

Supported IdP examples:

- Microsoft Entra ID (Azure AD)
- Okta
- Google Workspace
- Keycloak
- OneLogin
- Other SAML 2.0 compatible IdPs

Basic Configuration
===================

Enabling SSO
------------

To enable SAML authentication, add the following setting to ``app/WEB-INF/conf/system.properties``:

::

    sso.type=saml

.. note::
   ``sso.type`` and the basic SAML settings (IdP info, SP info, user attribute mapping) can also be configured from the admin "System > General" page.
   Settings changed in the admin UI are saved to ``system.properties`` and persist after restart.
   However, security settings such as signing/encryption and the SP certificate/private key cannot be configured in the admin UI, so write them directly in ``system.properties``.

.. note::
   Settings that start with ``saml.`` are read only from ``system.properties``.
   JVM system properties such as ``-Dsaml.security....`` or ``-Dfess.saml.security....`` are not consulted.
   In particular, ``saml.security.*``, ``saml.strict`` and ``saml.debug`` have no field in the admin UI either,
   so writing them directly in ``system.properties`` is the only way to set them.

Session Cookie Configuration
----------------------------

The IdP returns the assertion to |Fess| as a **cross-site POST**. A ``SameSite=Lax`` cookie is not sent on such a request, so SAML login does not complete with the default value shipped with |Fess|.

Change ``tomcat.sameSiteCookies`` to ``none`` in ``tomcat_config.properties``. This file is located in ``lib/classes/`` for the ZIP package and in ``/etc/fess/`` for the DEB/RPM packages.

::

    tomcat.sameSiteCookies = none

.. warning::
   Browsers only accept ``none`` on a cookie that also carries the ``Secure`` attribute, so |Fess| must be served over HTTPS. Over plain HTTP, this setting makes it impossible to log in to |Fess|.

.. note::
   The default ``lax`` is set for SSO methods whose callback returns as a redirect (GET). SAML's HTTP-POST binding is not one of them, so this change is only needed when using SAML. |Fess| must be restarted after changing the setting.

SP (Service Provider) Configuration
------------------------------------

To configure |Fess| as an SP, specify the SP Base URL.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.sp.base.url``
     - SP base URL
     - ``http://localhost:8080``

.. note::
   The default of ``saml.sp.base.url`` is ``http://localhost:8080``.
   Outside of test environments, always set the URL used to access |Fess| externally (HTTPS in production).

This setting automatically configures the following endpoints:

- **Entity ID**: ``{saml.sp.base.url}/sso/metadata``
- **ACS URL**: ``{saml.sp.base.url}/sso/``
- **SLO URL**: ``{saml.sp.base.url}/sso/logout``

Example::

    saml.sp.base.url=https://fess.example.com

Individual URL Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normally, setting ``saml.sp.base.url`` automatically configures each endpoint URL, but you can override individual URLs explicitly with the following properties if needed.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.sp.entityid``
     - SP Entity ID
     - ``{saml.sp.base.url}/sso/metadata``
   * - ``saml.sp.assertion_consumer_service.url``
     - Assertion Consumer Service URL
     - ``{saml.sp.base.url}/sso/``
   * - ``saml.sp.single_logout_service.url``
     - Single Logout Service URL
     - ``{saml.sp.base.url}/sso/logout``

IdP (Identity Provider) Configuration
-------------------------------------

Configure the information obtained from your IdP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.idp.entityid``
     - IdP Entity ID
     - (Required)
   * - ``saml.idp.single_sign_on_service.url``
     - IdP SSO service URL
     - (Required)
   * - ``saml.idp.x509cert``
     - IdP signing X.509 certificate (Base64 encoded, no line breaks)
     - (Required)
   * - ``saml.idp.single_logout_service.url``
     - IdP SLO service URL
     - (Optional)

.. note::
   For ``saml.idp.x509cert``, specify only the Base64-encoded content of the certificate on a single line without line breaks.
   Do not include the ``-----BEGIN CERTIFICATE-----`` and ``-----END CERTIFICATE-----`` lines.

Retrieving SP Metadata
----------------------

After starting |Fess|, you can retrieve the SP metadata in XML format from the ``/sso/metadata`` endpoint.

::

    https://fess.example.com/sso/metadata

Import this metadata into your IdP, or manually register the SP on the IdP side using the metadata contents.

.. note::
   To retrieve the metadata, you must first complete the basic SAML configuration (``sso.type=saml`` and ``saml.sp.base.url``) and start |Fess|.

IdP Side Configuration
======================

When registering |Fess| as an SP on the IdP side, configure the following information:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Value
   * - ACS URL / Reply URL
     - ``https://<Fess host>/sso/``
   * - Entity ID / Audience URI
     - ``https://<Fess host>/sso/metadata``
   * - Name ID Format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`` (Recommended)

Information to Obtain from IdP
------------------------------

Obtain the following information from your IdP's configuration screen or metadata for use in |Fess| configuration:

- **IdP Entity ID**: URI that identifies the IdP
- **SSO URL (HTTP-Redirect)**: Single sign-on endpoint URL
- **X.509 Certificate**: Public key certificate used for SAML assertion signature verification

User Attribute Mapping
======================

You can map user attributes obtained from SAML assertions to |Fess| groups and roles.

Group Attribute Configuration
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.attribute.group.name``
     - Attribute name containing group information
     - ``memberOf``
   * - ``saml.default.groups``
     - Default groups (comma-separated)
     - (None)

Example::

    saml.attribute.group.name=groups
    saml.default.groups=user

.. note::
   |Fess| uses the group values in the assertion as they are; it performs no directory lookup and
   does not expand nested (transitive) groups. Whether parent groups appear is therefore decided
   entirely by the IdP's claim configuration -- unlike :doc:`sso-entraid`, where |Fess| resolves
   parent groups through the Microsoft Graph API.

Role Attribute Configuration
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.attribute.role.name``
     - Attribute name containing role information
     - (None)
   * - ``saml.default.roles``
     - Default roles (comma-separated)
     - (None)

Example::

    saml.attribute.role.name=roles
    saml.default.roles=viewer

.. note::
   If attributes cannot be obtained from the IdP, default values will be used.
   When using role-based search, configure appropriate groups or roles.

.. warning::
   When ``saml.attribute.role.name`` is set, the attribute values sent by the IdP become |Fess| roles
   as they are. Because ``authentication.admin.roles`` in ``fess_config.properties`` defaults to
   ``admin``, any user whose role attribute contains ``admin`` gains |Fess| administrator privileges.
   Check who can control the role attribute on the IdP side, and change
   ``authentication.admin.roles`` to a different name if necessary.

Security Configuration
======================

For production environments, it is recommended to enable the following security settings.

.. note::
   When settings that are not recommended remain in place, an ``Insecure SAML settings: ...``
   warning is written to the log as the SAML settings are loaded.

Signature Settings
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.security.authnrequest_signed``
     - Sign authentication requests
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Require message signatures
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Require assertion signatures
     - ``false``
   * - ``saml.security.logoutrequest_signed``
     - Sign logout requests
     - ``false``
   * - ``saml.security.logoutresponse_signed``
     - Sign logout responses
     - ``false``
   * - ``saml.security.reject_deprecated_alg``
     - Reject deprecated signature algorithms such as SHA-1
     - ``false``

.. warning::
   Security features are disabled by default.
   For production environments, it is strongly recommended to set at least ``saml.security.want_assertions_signed=true``.

.. note::
   While ``saml.security.reject_deprecated_alg`` is ``false``, assertions and messages signed with
   SHA-1 (``rsa-sha1`` and ``dsa-sha1``) are also accepted. It is not enabled by default because
   turning it on rejects IdPs that still sign with SHA-1.
   Confirm that your IdP signs with SHA-256 or stronger, then set ``saml.security.reject_deprecated_alg=true``.

.. warning::
   When Single Logout is configured (``saml.idp.single_logout_service.url``), always set
   ``saml.security.want_messages_signed=true`` as well.
   While it is ``false``, no signature is required on a LogoutRequest received at ``/sso/logout``.
   The only checks performed are the XML schema, ``NotOnOrAfter`` (if present), ``Destination``
   (if present), and that the Issuer matches ``saml.idp.entityid`` (if present); the NameID in the
   LogoutRequest is never compared against the logged-in user. The Issuer element is optional in the
   SAML schema, so a LogoutRequest that omits it is never compared against the IdP entity ID. An
   attacker, without needing to know the IdP entity ID, can therefore craft an unsigned LogoutRequest
   and terminate an authenticated user's session by luring that user to the URL.
   The impact is a forced logout (denial of service), not account takeover.

Encryption Settings
-------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.security.want_assertions_encrypted``
     - Require assertion encryption
     - ``false``
   * - ``saml.security.want_nameid_encrypted``
     - Require NameID encryption
     - ``false``

SP Certificate and Private Key Configuration
--------------------------------------------

When the SP signs authentication requests or logout messages (e.g., ``saml.security.authnrequest_signed``), or requests encryption of assertions or NameID (e.g., ``saml.security.want_assertions_encrypted``), you must configure the SP's private key and X.509 certificate.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.sp.x509cert``
     - SP X.509 certificate (Base64-encoded, no line breaks)
     - (empty)
   * - ``saml.sp.privatekey``
     - SP private key (Base64-encoded, no line breaks)
     - (empty)

.. note::
   For ``saml.sp.x509cert`` and ``saml.sp.privatekey``, as with ``saml.idp.x509cert``, specify the Base64-encoded content as a single line without line breaks (do not include the ``-----BEGIN ...-----`` and ``-----END ...-----`` lines).
   When enabling signing/encryption, also register the SP certificate on the IdP side. The SP certificate is published in the SP metadata at ``/sso/metadata``.

Other Security Settings
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.strict``
     - Strict mode (perform strict validation)
     - ``true``
   * - ``saml.security.want_xml_validation``
     - Validate the XML schema of messages
     - ``true``
   * - ``saml.security.signature_algorithm``
     - Signature algorithm
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``
   * - ``saml.security.requested_authncontext``
     - Requested authentication context
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.sp.nameidformat``
     - NameID format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   |Fess| internally uses a SAML library (java-saml), and properties starting with ``saml.`` are mapped to the library's corresponding settings (the ``onelogin.saml2.`` prefix).
   Therefore, in addition to those listed here, you can specify detailed settings in ``system.properties`` such as bindings (e.g., ``saml.sp.assertion_consumer_service.binding``), organization information (``saml.organization.*``), and contact information (``saml.contacts.*``).

AuthnRequest Expiration
=======================

|Fess| sends one AuthnRequest to the IdP for each access to ``/sso/`` and records its ID in the session.
The SAML response returned by the IdP is validated against the recorded ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.request.id.ttl``
     - How long an unanswered AuthnRequest ID is retained (seconds)
     - ``3600``

A recorded ID is discarded once this period passes.
If it expires (for example the IdP login page was left open), the returned assertion cannot be matched and the login fails once.
If no value is set, 3600 seconds is used.
If a value that cannot be parsed as a number is set, 3600 seconds is also used and a warning beginning with ``Invalid saml.request.id.ttl`` is logged.
A value of zero or less would discard the AuthnRequest ID before a login could return from the IdP, so it is likewise replaced with 3600 seconds and a warning is logged.

.. note::
   At most 10 unanswered AuthnRequests are kept per session; when the cap is exceeded the oldest are discarded.
   This exists so that logins can be started from several tabs at once, and it cannot be changed with a ``saml.`` setting.
   If it is overridden with a value of zero or less, 10 is used instead and a warning is logged.

Configuration Examples
======================

Minimal Configuration (for Testing)
-----------------------------------

The following is a minimal configuration example for verification in a test environment.

::

    # Enable SSO
    sso.type=saml

    # SP configuration
    saml.sp.base.url=https://fess.example.com

    # IdP configuration (set values obtained from IdP admin console)
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(Base64 encoded certificate)

    # Default groups
    saml.default.groups=user

Recommended Configuration (for Production)
------------------------------------------

The following is a recommended configuration example for production environments.

::

    # Enable SSO
    sso.type=saml

    # SP configuration
    saml.sp.base.url=https://fess.example.com

    # IdP configuration
    saml.idp.entityid=https://idp.example.com/saml/metadata
    saml.idp.single_sign_on_service.url=https://idp.example.com/saml/sso
    saml.idp.single_logout_service.url=https://idp.example.com/saml/logout
    saml.idp.x509cert=MIIDpDCCAoygAwIBAgI...(Base64 encoded certificate)

    # User attribute mapping
    saml.attribute.group.name=groups
    saml.attribute.role.name=roles
    saml.default.groups=user

    # Security settings (recommended for production)
    saml.security.want_assertions_signed=true
    saml.security.want_messages_signed=true

    # Enable after confirming the IdP signs with SHA-256 or stronger
    saml.security.reject_deprecated_alg=true

Troubleshooting
===============

Common Issues and Solutions
---------------------------

Cannot return to Fess after authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the ACS URL is correctly configured on the IdP side
- Ensure the ``saml.sp.base.url`` value matches the IdP configuration
- The SAML assertion arrives as a cross-site POST from the IdP. When ``tomcat.sameSiteCookies`` in
  ``tomcat_config.properties`` is ``lax`` (the default), the browser does not send the session cookie
  with it, so |Fess| finds no matching AuthnRequest ID and fails the login once, on the spot. The
  browser returns to the login page showing "SSO login process failed.", and a warning beginning with
  ``Received a SAML response with no matching AuthnRequest ID in the session`` is written to the log.
  Set ``tomcat.sameSiteCookies = none`` in that case (``SameSite=None`` requires HTTPS)
- If the login took too long at the IdP, the AuthnRequest ID is no longer there when the assertion
  comes back, so the login fails once and has to be started again. Which warning appears says what
  ran out: one beginning with ``Received a SAML response after the session it belongs to had
  expired`` means the servlet container discarded the whole session, while one containing
  ``pending AuthnRequest ID(s) of the session had expired`` means the session is still alive and
  only ``saml.request.id.ttl`` elapsed. Both are written only when the browser did send its session
  cookie, which is what separates them from the SameSite case above
- |Fess| leaves ``session-timeout`` unset in ``app/WEB-INF/web.xml``, so the servlet container's
  default of 30 minutes applies and is shorter than the 3600 seconds of ``saml.request.id.ttl``. The
  session, and with it the AuthnRequest ID it holds, is discarded first, so raising
  ``saml.request.id.ttl`` on its own does not give users longer to finish logging in at the IdP:
  raise the session timeout as well. The ``saml.request.id.ttl`` warning is therefore only seen
  where the TTL is set shorter than the session timeout

.. note::
   In 15.7 the same situation caused |Fess| to redirect to the IdP again and again, looping the login.
   15.8 fails once instead of looping. The configuration remedy is unchanged.

Destination validation fails behind a reverse proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When |Fess| runs behind a TLS-terminating reverse proxy or load balancer, assertion validation can
fail even though ``saml.sp.base.url`` is set correctly.

The cause is that the SAML library compares the ``Destination`` attribute of the assertion against
the request URL reconstructed by the servlet container, not against the configured ACS URL. When the
proxy terminates HTTPS, the request URL |Fess| sees is an internal one such as
``http://<internal-host>:<internal-port>/sso/``, which does not match the
``https://fess.example.com/sso/`` sent by the IdP. ``saml.sp.base.url`` is not used for this
comparison, so setting it alone does not fix the problem.

Set ``saml.debug=true`` to have the reason written to the log:

::

    The response was received at http://... instead of https://fess.example.com/sso/

Align the connector settings in ``tomcat_config.properties`` with the externally visible scheme and
port. These settings ship commented out:

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

Also configure the reverse proxy to pass the original ``Host`` header through to |Fess|, because the
host part of the request URL is built from that header. |Fess| must be restarted after changing
``tomcat_config.properties``.

The same validation applies to Single Logout messages, so configure this when using SLO as well.

Signature verification error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the IdP certificate is correctly configured
- Ensure the certificate has not expired
- The certificate should be specified as Base64-encoded content only, without line breaks

User groups/roles not reflected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that attributes are correctly configured on the IdP side
- Ensure the ``saml.attribute.group.name`` value matches the attribute name sent by the IdP
- With Microsoft Entra ID, the group claim carries group ``ObjectId`` GUIDs unless a different
  source attribute is selected, so the values will not match group names
- Microsoft Entra ID omits the group claim entirely when the user belongs to more than 150 groups
  (nested groups count toward this limit), and |Fess| then falls back to ``saml.default.groups``
- Enable debug mode to inspect the SAML assertion contents

Debug Settings
--------------

To investigate issues, you can enable debug mode with the following setting:

::

    saml.debug=true

Setting ``saml.debug=true`` outputs the detailed reason to the log when SAML authentication fails.

You can also output detailed SAML-related logs by adding the following logger to ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Reference
=========

- :doc:`security-role` - Role-based search configuration
- :doc:`sso-oidc` - About SSO configuration with OpenID Connect
- :doc:`sso-entraid` - About SSO configuration dedicated to Microsoft Entra ID
