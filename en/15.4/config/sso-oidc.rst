=====================================
SSO Configuration with OpenID Connect
=====================================

Overview
========

|Fess| supports Single Sign-On (SSO) authentication using OpenID Connect (OIDC).
OpenID Connect is an authentication protocol built on top of OAuth 2.0 that uses ID Tokens (JWT) for user authentication.
By using OpenID Connect authentication, user information authenticated by an OpenID Provider (OP) can be integrated with |Fess|.

How OpenID Connect Authentication Works
---------------------------------------

In OpenID Connect authentication, |Fess| operates as a Relying Party (RP) and collaborates with an external OpenID Provider (OP) for authentication.

1. User accesses the |Fess| SSO endpoint (``/sso/``)
2. |Fess| redirects to the OP's authorization endpoint
3. User authenticates at the OP
4. OP redirects the authorization code to |Fess|
5. |Fess| uses the authorization code to obtain an ID Token from the token endpoint
6. |Fess| validates the ID Token (JWT) and logs in the user

For integration with role-based search, see :doc:`security-role`.

Prerequisites
=============

Before configuring OpenID Connect authentication, verify the following prerequisites:

- |Fess| 15.4 or later is installed
- An OpenID Connect-compatible provider (OP) is available
- |Fess| is accessible via HTTPS (required for production environments)
- You have permission to register |Fess| as a client (RP) on the OP side

Examples of supported providers:

- Microsoft Entra ID (Azure AD)
- Google Workspace / Google Cloud Identity
- Okta
- Keycloak
- Auth0
- Other OpenID Connect-compatible providers

Basic Configuration
===================

Enabling SSO
------------

To enable OpenID Connect authentication, add the following setting in ``app/WEB-INF/conf/system.properties``:

::

    sso.type=oic

Provider Configuration
----------------------

Configure the information obtained from your OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``oic.auth.server.url``
     - Authorization endpoint URL
     - (Required)
   * - ``oic.token.server.url``
     - Token endpoint URL
     - (Required)

.. note::
   These URLs can be obtained from the OP's Discovery endpoint (``/.well-known/openid-configuration``).

Client Configuration
--------------------

Configure the client information registered with the OP.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``oic.client.id``
     - Client ID
     - (Required)
   * - ``oic.client.secret``
     - Client secret
     - (Required)
   * - ``oic.scope``
     - Requested scopes
     - (Required)

.. note::
   The scope must include at least ``openid``.
   To retrieve the user's email address, specify ``openid email``.

Redirect URL Configuration
--------------------------

Configure the callback URL after authentication.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``oic.redirect.url``
     - Redirect URL (callback URL)
     - ``{oic.base.url}/sso/``
   * - ``oic.base.url``
     - |Fess| base URL
     - ``http://localhost:8080``

.. note::
   If ``oic.redirect.url`` is omitted, it is automatically constructed from ``oic.base.url``.
   For production environments, set ``oic.base.url`` to an HTTPS URL.

OP-Side Configuration
=====================

When registering |Fess| as a client (RP) on the OP side, configure the following information:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Value
   * - Application type
     - Web application
   * - Redirect URI / Callback URL
     - ``https://<Fess host>/sso/``
   * - Allowed scopes
     - ``openid`` and required scopes (``email``, ``profile``, etc.)

Information to Obtain from OP
-----------------------------

Obtain the following information from the OP's configuration screen or Discovery endpoint for use in |Fess| configuration:

- **Authorization Endpoint**: URL to initiate user authentication
- **Token Endpoint**: URL to obtain tokens
- **Client ID**: Client identifier issued by the OP
- **Client Secret**: Secret key used for client authentication

.. note::
   Most OPs allow you to check the authorization and token endpoint URLs from the
   Discovery endpoint (``https://<OP>/.well-known/openid-configuration``).

Configuration Examples
======================

Minimal Configuration (for Testing)
-----------------------------------

The following is a minimal configuration example for verification in a test environment.

::

    # Enable SSO
    sso.type=oic

    # Provider configuration (set values obtained from OP)
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Client configuration
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email

    # Redirect URL (test environment)
    oic.redirect.url=http://localhost:8080/sso/

Recommended Configuration (for Production)
------------------------------------------

The following is a recommended configuration example for production environments.

::

    # Enable SSO
    sso.type=oic

    # Provider configuration
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Client configuration
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # Base URL (use HTTPS for production)
    oic.base.url=https://fess.example.com

Troubleshooting
===============

Common Problems and Solutions
-----------------------------

Cannot Return to Fess After Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the redirect URI is correctly configured on the OP side
- Ensure that the ``oic.redirect.url`` or ``oic.base.url`` value matches the OP configuration
- Verify that the protocol (HTTP/HTTPS) matches

Authentication Errors Occur
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the client ID and client secret are correctly configured
- Ensure that the scope includes ``openid``
- Verify that the authorization endpoint URL and token endpoint URL are correct

Cannot Retrieve User Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ensure that the scope includes the required permissions (``email``, ``profile``, etc.)
- Verify that the required scopes are allowed for the client on the OP side

Debugging
---------

To investigate problems, you can output detailed OpenID Connect-related logs by adjusting the |Fess| log level.

In ``app/WEB-INF/classes/log4j2.xml``, you can add the following logger to change the log level:

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

Reference
=========

- :doc:`security-role` - Role-based search configuration
- :doc:`sso-saml` - SSO configuration with SAML authentication
