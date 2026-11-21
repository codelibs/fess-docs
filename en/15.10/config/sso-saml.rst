=============================
SAML Authentication SSO Setup
=============================

Overview
========

|Fess| supports Single Sign-On (SSO) authentication using SAML (Security Assertion Markup Language) 2.0.
By using SAML authentication, user information authenticated by an IdP (Identity Provider) can be integrated with |Fess|, enabling role-based search results based on user permissions when combined with role-based search.

.. note::
   SAML authentication comes from the ``fess-sso-saml`` plugin, which is not part of the
   distribution. Install it from the System > Plugin page in the administration screen, or with
   ``bin/fess-setup install plugin fess-sso-saml``.
   The plugin processes SAML messages with the SAML library `saml4j <https://github.com/codelibs/saml4j>`__.
   Until it is installed, ``sso.type=saml`` only redirects every request to ``/sso/`` back to
   the login page.

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

.. note::
   When you run several nodes, set the environment variable ``FESS_SESSION_STORE=opensearch`` to share the HTTP session between them; a login started on one node can then be completed on another. Update the plugin on every node to 15.10 before you enable it: a 15.9.0 plugin does not share the login state, and a user who returns to another node stays anonymous. Without a shared session, pin each session to one node on the load balancer.

   With ``FESS_SESSION_STORE=opensearch``, adding or removing an SSO plugin (``fess-sso-saml``, ``fess-sso-oidc`` or ``fess-sso-entraid``) changes the format version of the stored sessions. Every stored session then becomes invalid and all users have to log in again. Install or remove these plugins on all nodes: a node whose set of these plugins differs from that of the other nodes cannot read the sessions they stored, and they cannot read its sessions. Other plugins, such as the storage, script and SPNEGO plugins, do not change the format.

Prerequisites
=============

Before configuring SAML authentication, verify the following prerequisites:

- |Fess| 15.10 or later is installed
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
   In particular, ``saml.security.*`` has no field in the admin UI either,
   so writing it directly in ``system.properties`` is the only way to set it.

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
   * - ``saml.idp.x509certMulti.1``, ``.2``, ...
     - Additional IdP signing certificates (for example, during a key rollover)
     - (Optional)

.. note::
   The IdP certificate is the only trust anchor for signatures; a certificate carried inside a message is never trusted.
   IdP and SP certificates must be RSA keys of at least 2048 bits.
   ``saml.idp.x509cert`` may be left out when ``saml.idp.x509certMulti.N`` is set.

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

.. note::
   |Fess| checks the following on every assertion. The URLs are derived from ``saml.sp.base.url`` (or the individual URL properties), not from the incoming request.

   - The assertion carries an ``AudienceRestriction`` that names the SP entity ID
   - The ``Destination`` of a signed Response and the ``Recipient`` of the SubjectConfirmation are the assertion consumer service URL

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

IdPs that repeat an attribute name
----------------------------------

If the IdP splits the same attribute name across several ``<Attribute>`` elements, |Fess| merges
their values.

Keycloak sends assertions of this shape by default: its role and group mappers emit one
``<Attribute>`` element per value unless their ``single`` option is enabled, and every Keycloak
account carries several default realm roles. No setting is needed in |Fess| for this.

Security Configuration
======================

The following security settings are read from ``system.properties``.

.. note::
   When settings that weaken the defaults remain in place (``saml.security.want_logout_signed=false``
   with Single Logout configured, ``saml.security.allow_deprecated_alg=true`` or
   ``saml.security.allow_rsa_1_5=true``), an ``Insecure SAML settings: ...`` warning is written to the
   log as the SAML settings are loaded.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.session.end_with_idp``
     - End the |Fess| login when the IdP session ends, at the ``SessionNotOnOrAfter`` of the assertion plus ``saml.security.clock_drift``. ``false`` turns it off
     - ``true``

.. note::
   The setting has no effect when the IdP sends no ``SessionNotOnOrAfter``. When the IdP caps its session at a short time (the default in Keycloak is 10 hours), users can be logged out sooner than before. Logging out at the IdP does not end the |Fess| login before that time. When the login ends this way, a ``SESSION_END`` record with the reason ``idp_session_ended`` is written to the audit log (see :doc:`../install/security`).

Signature Settings
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.security.authnrequest_signed``
     - Sign authentication requests (requires ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.want_messages_signed``
     - Require the Response to be signed
     - ``false``
   * - ``saml.security.want_assertions_signed``
     - Require the Assertion to be signed
     - ``false``
   * - ``saml.security.want_logout_signed``
     - Require logout messages from the IdP to be signed
     - ``true``
   * - ``saml.security.allow_deprecated_alg``
     - Accept SHA-1 signatures
     - ``false``
   * - ``saml.security.signature_algorithm``
     - Algorithm of outgoing signatures: the URI of ``rsa-sha256``, ``rsa-sha384`` or ``rsa-sha512``
     - ``http://www.w3.org/2001/04/xmldsig-more#rsa-sha256``

.. note::
   Whatever these settings say, either the Response or the Assertion must be signed.
   Use ``saml.security.want_messages_signed`` or ``saml.security.want_assertions_signed`` to require the signature on the element your IdP signs.
   The signature must reference the signed element by its own ID and use ``rsa-sha256``, ``rsa-sha384`` or ``rsa-sha512`` (or the ECDSA variants).
   SHA-1 signatures are rejected unless ``saml.security.allow_deprecated_alg=true``, so confirm that your IdP signs with SHA-256 or stronger.

.. note::
   When Single Logout is configured (``saml.idp.single_logout_service.url``), the LogoutRequest and
   LogoutResponse sent by the IdP must be signed with the key of ``saml.idp.x509cert``
   (``saml.security.want_logout_signed=true`` is the default).
   Set ``saml.security.want_logout_signed=false`` only for an IdP that cannot sign them.
   The single logout service (``/sso/logout``) accepts the redirect binding (GET) and the POST binding.
   Register the ``/sso/logout`` URL for the POST binding on the IdP side as well; a LogoutResponse
   that the IdP posts to the assertion consumer service is not recognized.

Encryption Settings
-------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``saml.security.want_assertions_encrypted``
     - Require assertion encryption (requires ``saml.sp.privatekey``)
     - ``false``
   * - ``saml.security.allow_rsa_1_5``
     - Accept RSA 1.5 key transport (requires ``saml.sp.privatekey``). Only OAEP is accepted otherwise
     - ``false``

.. note::
   Leave ``saml.security.allow_rsa_1_5`` at ``false`` unless your IdP can only encrypt with RSA 1.5.

SP Certificate and Private Key Configuration
--------------------------------------------

When the SP signs authentication requests or logout messages (e.g., ``saml.security.authnrequest_signed``), or requests encryption of assertions or NameID (e.g., ``saml.security.want_assertions_encrypted``), you must configure the SP's private key (PKCS#8) and X.509 certificate.

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
   * - ``saml.security.requested_authncontext``
     - Requested authentication context (a blank value requests none)
     - ``urn:oasis:names:tc:SAML:2.0:ac:classes:Password``
   * - ``saml.security.requested_authncontextcomparison``
     - Comparison for the requested authentication context (``exact``, ``minimum``, ``maximum`` or ``better``)
     - ``exact``
   * - ``saml.security.clock_drift``
     - Clock drift tolerated when checking validity periods (seconds, 0 to 600)
     - ``120``
   * - ``saml.security.max_message_size``
     - Largest decoded message accepted (bytes, 1024 to 16777216)
     - ``1048576``
   * - ``saml.sp.nameidformat``
     - NameID format
     - ``urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress``

.. note::
   The audience, recipient, destination, issuer and validity period of an assertion are always checked,
   and a response must answer a login that |Fess| started.
   An assertion that has no Audience, or whose Audience does not name the SP entity ID, is rejected.
   Validation is always strict: ``saml.strict=false`` is refused.

Properties That Are No Longer Used
----------------------------------

The following properties are ignored. One warning that names them is written to the log.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Property
     - Now
   * - ``saml.security.reject_deprecated_alg``
     - SHA-1 signatures are rejected by default; ``saml.security.allow_deprecated_alg=true`` accepts them
   * - ``saml.security.allowed_key_transport_algorithms``
     - Only OAEP is accepted by default; ``saml.security.allow_rsa_1_5=true`` accepts RSA 1.5 as well
   * - ``saml.security.allow_duplicated_attribute_name``
     - Repeated attributes are always merged
   * - ``saml.security.reject_missing_audience``
     - An assertion with no audience is always rejected
   * - ``saml.idp.certfingerprint``, ``saml.idp.certfingerprint_algorithm``
     - Set ``saml.idp.x509cert``; a fingerprint is not a trust anchor
   * - ``saml.security.sign_metadata``, ``saml.security.want_nameid_encrypted``, ``saml.security.want_xml_validation``, ``saml.security.logoutrequest_signed``, ``saml.security.logoutresponse_signed``, ``saml.security.digest_algorithm``, ``saml.keystore.*``, ``saml.contacts.*``, ``saml.organization.*``, ``saml.compress.*``, ``saml.parsing.*``, ``saml.unique_id_prefix``, the ``*.binding`` and ``*.response.url`` properties
     - No longer used

Any other ``saml.`` property that the library does not know stops SAML logins with a message that names it,
so that a mistyped security setting cannot go unnoticed. ``saml.debug`` is accepted and has no effect.

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
    # Require the signature on the element your IdP signs
    # (saml.security.want_messages_signed=true for the Response)
    saml.security.want_assertions_signed=true

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
  with it and the login fails once. Set ``tomcat.sameSiteCookies = none`` in that case
  (``SameSite=None`` requires HTTPS)
- If the login took too long at the IdP, the AuthnRequest ID is no longer there when the assertion
  comes back, so the login fails once and has to be started again
- |Fess| leaves ``session-timeout`` unset in ``app/WEB-INF/web.xml``, so the servlet container's
  default of 30 minutes applies and is shorter than the 3600 seconds of ``saml.request.id.ttl``.
  Raising ``saml.request.id.ttl`` on its own therefore does not give users longer to finish logging
  in at the IdP: raise the session timeout as well

Destination or Recipient validation fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Destination`` of a signed Response and the ``Recipient`` of the SubjectConfirmation must be the
assertion consumer service URL of |Fess|. That URL comes from ``saml.sp.base.url`` (or
``saml.sp.assertion_consumer_service.url``), not from the request that reaches |Fess|, so a
TLS-terminating reverse proxy does not affect the comparison.

- Set ``saml.sp.base.url`` to the externally visible URL, including the scheme and port
- Register the same ACS URL (``{saml.sp.base.url}/sso/``) on the IdP side
- If ``saml.sp.entityid`` is overridden, the IdP must use that value as the Audience

Signature verification error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the IdP certificate is correctly configured
- Ensure the certificate has not expired
- The certificate should be specified as Base64-encoded content only, without line breaks
- The IdP certificate must be an RSA key of at least 2048 bits
- Either the Response or the Assertion must be signed, and the signature must use SHA-256 or stronger
  (SHA-1 is accepted only with ``saml.security.allow_deprecated_alg=true``)
- The reason a response was rejected is written to the log as ``Authentication failed: <reason> - <detail>``

User groups/roles not reflected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that attributes are correctly configured on the IdP side
- Ensure the ``saml.attribute.group.name`` value matches the attribute name sent by the IdP
- With Microsoft Entra ID, the group claim carries group ``ObjectId`` GUIDs unless a different
  source attribute is selected, so the values will not match group names
- Microsoft Entra ID omits the group claim entirely when the user belongs to more than 150 groups
  (nested groups count toward this limit), and |Fess| then falls back to ``saml.default.groups``
- Compare the attribute names with those in the assertion the IdP actually sends

Log Settings
------------

When SAML authentication fails, the reason is always written to the log as a warning.
The ``saml.debug`` property has no effect.

To output detailed SAML-related logs, add the following logger to ``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.sso.saml" level="DEBUG"/>

Reference
=========

- :doc:`security-role` - Role-based search configuration
- :doc:`sso-oidc` - About SSO configuration with OpenID Connect
- :doc:`sso-entraid` - About SSO configuration dedicated to Microsoft Entra ID
