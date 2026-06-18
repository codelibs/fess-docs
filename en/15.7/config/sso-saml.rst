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

For role-based search integration, see :doc:`security-role`.

Prerequisites
=============

Before configuring SAML authentication, verify the following prerequisites:

- |Fess| 15.7 or later is installed
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

Security Configuration
======================

For production environments, it is recommended to enable the following security settings.

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

.. warning::
   Security features are disabled by default.
   For production environments, it is strongly recommended to set at least ``saml.security.want_assertions_signed=true``.

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

Troubleshooting
===============

Common Issues and Solutions
---------------------------

Cannot return to Fess after authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the ACS URL is correctly configured on the IdP side
- Ensure the ``saml.sp.base.url`` value matches the IdP configuration

Signature verification error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the IdP certificate is correctly configured
- Ensure the certificate has not expired
- The certificate should be specified as Base64-encoded content only, without line breaks

User groups/roles not reflected
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that attributes are correctly configured on the IdP side
- Ensure the ``saml.attribute.group.name`` value matches the attribute name sent by the IdP
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
