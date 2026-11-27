=====================================
SSO Configuration with OpenID Connect
=====================================

Overview
========

|Fess| supports Single Sign-On (SSO) authentication using OpenID Connect (OIDC).
OpenID Connect is an authentication protocol built on top of OAuth 2.0 that uses ID Tokens (JWT) for user authentication.
By using OpenID Connect authentication, user information authenticated by an OpenID Provider (OP) can be integrated with |Fess|.

.. note::
   OpenID Connect authentication comes from the ``fess-sso-oidc`` plugin, which is not part of
   the distribution. Install it from the System > Plugin page in the administration screen, or
   with ``bin/fess-setup install plugin fess-sso-oidc``. The plugin is named ``fess-sso-oidc``
   while the ``sso.type`` value stays ``oic``.
   Until it is installed, ``sso.type=oic`` only redirects every request to ``/sso/`` back to the
   login page.

How OpenID Connect Authentication Works
---------------------------------------

In OpenID Connect authentication, |Fess| operates as a Relying Party (RP) and collaborates with an external OpenID Provider (OP) for authentication.

1. User accesses the |Fess| SSO endpoint (``/sso/``)
2. |Fess| redirects to the OP's authorization endpoint
3. User authenticates at the OP
4. OP redirects the authorization code to |Fess|
5. |Fess| uses the authorization code to obtain an ID Token from the token endpoint
6. |Fess| decodes the ID Token (JWT), checks its claims, extracts user information and logs in the user

.. note::
   |Fess| uses the Authorization Code Flow. The ID Token is obtained directly from the token endpoint via a back-channel (server-to-server communication) between |Fess| and the OP, without passing through the browser.
   |Fess| decodes the ID Token and extracts claims (such as ``email`` and ``groups``) to construct user information, but does NOT cryptographically verify the JWT signature. OpenID Connect Core allows this because the token is received directly from the token endpoint over TLS, so the token endpoint URL (``oic.token.server.url``) must be HTTPS. ``http`` is accepted only for ``localhost``, ``127.x.x.x`` and ``::1``.
   |Fess| does check the claims: ``aud`` must contain ``oic.client.id`` (and ``azp``, when present, must equal it), ``exp`` must be present and not past (a clock difference of up to 300 seconds is tolerated), and ``iss`` must equal ``oic.issuer`` when that key is set. Without ``oic.issuer``, ``iss`` is not checked, and a warning is logged at the first login after each start. A ``nonce`` is sent with every authorization request, and the ``nonce`` claim of the ID Token must equal it; a token without the claim, or with another value, is refused. An OP that does not return the ``nonce`` cannot be used, and there is no setting to turn this check off. PKCE (S256) is used by default: every authorization request carries a ``code_challenge``, and the token request sends the ``code_verifier``. Set ``oic.pkce=false`` in ``system.properties`` only for an OP that rejects PKCE (the admin console has no field for it; the key is read for each login, so no restart is needed). ``iat`` and ``nbf`` are not checked.

For integration with role-based search, see :doc:`security-role`.

.. note::
   The |Fess| login session does not end when the tokens issued by the OP expire. |Fess| checks ``exp`` of the ID Token only when the user logs in, and the lifetime of the token is not used for the session. When ``oic.jwks.uri`` is not set, the login lasts until the user logs out or the session timeout is reached. To end the |Fess| session when the user logs out at the OP, set up `Back-Channel Logout`_. SAML differs: its session ends with the IdP session (see :doc:`sso-saml`).

.. note::
   When you run several nodes, set the environment variable ``FESS_SESSION_STORE=opensearch`` to share the HTTP session between them; a login started on one node can then be completed on another. Update the plugin on every node to 15.10 before you enable it: a 15.9.0 plugin does not share the login state, and a user who returns to another node stays anonymous. Without a shared session, pin each session to one node on the load balancer.

   With ``FESS_SESSION_STORE=opensearch``, adding or removing an SSO plugin (``fess-sso-saml``, ``fess-sso-oidc`` or ``fess-sso-entraid``) changes the format version of the stored sessions. Every stored session then becomes invalid and all users have to log in again. Install or remove these plugins on all nodes: a node whose set of these plugins differs from that of the other nodes cannot read the sessions they stored, and they cannot read its sessions. Other plugins, such as the storage, script and SPNEGO plugins, do not change the format.

Prerequisites
=============

Before configuring OpenID Connect authentication, verify the following prerequisites:

- |Fess| 15.10 or later is installed
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

To enable OpenID Connect authentication, add the following setting to ``app/WEB-INF/conf/system.properties``:

::

    sso.type=oic

.. note::
   The ``sso.type`` setting and the ``oic.*`` settings described below, except ``oic.issuer`` and ``oic.jwks.uri``, can also be configured and changed from the admin "System > General" page.
   Settings changed through the admin page are saved to ``system.properties`` and persist after restart.
   ``oic.issuer`` and ``oic.jwks.uri`` can only be set in ``system.properties``.

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
     - ``https://accounts.google.com/o/oauth2/auth``
   * - ``oic.token.server.url``
     - Token endpoint URL
     - ``https://accounts.google.com/o/oauth2/token``
   * - ``oic.issuer``
     - Issuer identifier (optional). When set, the ``iss`` claim of the ID Token must equal it exactly (a trailing slash counts)
     - (empty: ``iss`` is not checked)
   * - ``oic.jwks.uri``
     - The OP's ``jwks_uri`` (optional). Setting it turns on back-channel logout (see `Back-Channel Logout`_)
     - (empty: back-channel logout is not used)

.. note::
   These URLs and the issuer can be obtained from the OP's Discovery endpoint (``/.well-known/openid-configuration``); the issuer is its ``issuer`` value.
   The token endpoint URL (``oic.token.server.url``) must be HTTPS. ``http`` is accepted only when the host is ``localhost`` (any case), an IPv4 address of the form ``127.x.x.x``, or ``::1``. The host is compared as written and is never resolved, so a Docker Compose service name (such as ``http://keycloak:8080/...``) or an internal host name is refused over ``http`` even if it points to the same machine.

   Only the token endpoint is checked, not the authorization endpoint (``oic.auth.server.url``). The check runs at login, not at startup. Setting ``oic.issuer`` does not relax this rule; it only turns on the check of the ``iss`` claim.

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
     - (empty)
   * - ``oic.client.secret``
     - Client secret
     - (empty)
   * - ``oic.scope``
     - Requested scopes
     - (empty)

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

.. warning::
   "Omitted" means that the key does not exist at all. If you save ``oic.redirect.url`` blank in the admin "System > General" page, the key is removed and ``{oic.base.url}/sso/`` is used.
   In contrast, a line ``oic.redirect.url=`` (only the value empty) written by hand in ``system.properties`` is not an omitted setting but an empty value: the authorization request then carries a ``redirect_uri`` parameter without a value.
   It does not match the redirect URI registered with the OP, so the OP rejects it and the login fails.
   Either give it a value or remove the line.

User Attribute Configuration
-----------------------------

Configure the default groups and roles to assign to users authenticated via OIDC.
The user ID, groups, and roles are determined as follows:

- **User ID**: Obtained from the ``email`` claim of the ID Token (JWT). For this reason, the ``email`` scope is effectively required (if the ``email`` claim cannot be obtained, login will not work correctly).
- **Groups**: Obtained from the ``groups`` claim of the ID Token. If the ``groups`` claim is not present, the value of ``oic.default.groups`` is used. An empty ``groups`` array counts as present, so ``oic.default.groups`` is not used and the user is treated as having no groups.
- **Roles**: Always taken from the value of ``oic.default.roles`` (there is no mechanism to obtain roles from ID Token claims).

.. note::
   |Fess| uses the values of the ``groups`` claim as they are; it performs no directory lookup and
   does not expand nested (transitive) groups. Whether parent groups appear is therefore decided
   entirely by the OP's claim configuration -- unlike :doc:`sso-entraid`, where |Fess| resolves
   parent groups through the Microsoft Graph API.
   The claim value becomes the search permission verbatim. A provider configured to emit full group
   paths therefore sends values such as ``/parent/child``, and those do not match documents tagged
   with the plain group name.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``oic.default.groups``
     - Default groups (comma-separated)
     - (empty)
   * - ``oic.default.roles``
     - Default roles (comma-separated)
     - (empty)

.. note::
   When using role-based search, you must assign appropriate groups or roles to users.
   See :doc:`security-role` for details.

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
------------------------------

Obtain the following information from the OP's configuration screen or Discovery endpoint for use in |Fess| configuration:

- **Authorization Endpoint**: URL to initiate user authentication
- **Token Endpoint**: URL to obtain tokens
- **Issuer** (optional): ``issuer`` value of the Discovery document, used for ``oic.issuer``
- **Client ID**: Client identifier issued by the OP
- **Client Secret**: Secret key used for client authentication

.. note::
   Most OPs allow you to check the authorization and token endpoint URLs from the
   Discovery endpoint (``https://<OP>/.well-known/openid-configuration``).

Back-Channel Logout
===================

With `OpenID Connect Back-Channel Logout 1.0 <https://openid.net/specs/openid-connect-backchannel-1_0.html>`__, the OP tells |Fess|, server to server, that a login has ended at the OP, and |Fess| ends the session of that login.
Without it, a |Fess| session outlives the logout at the OP.

Enabling
--------

Set the OP's ``jwks_uri`` in ``app/WEB-INF/conf/system.properties``. Setting it turns back-channel logout on; nothing else needs to be switched.

::

    oic.jwks.uri=https://op.example.com/jwks

- ``oic.jwks.uri`` can only be set in ``system.properties`` (the admin page has no field for it).
- ``oic.issuer`` and ``oic.client.id`` have to be set too, because the logout token is checked against them. If either is empty, every logout request is refused.
- ``oic.jwks.uri`` must be HTTPS. As for the token endpoint, ``http`` is accepted only when the host is ``localhost``, ``127.x.x.x`` or ``::1``. The check runs when the keys are fetched for a logout request, and a URL that fails it makes the request be refused.
- ``jwks_uri`` and ``issuer`` can be obtained from the OP's Discovery endpoint (``/.well-known/openid-configuration``), where ``backchannel_logout_supported`` tells whether the OP supports it.

Registering at the OP
---------------------

- In the client settings of the OP, register ``https://<Fess host>/sso/logout`` as the back-channel logout URL.
- Where the OP has the option (``backchannel_logout_session_required``), have it include the session ID (``sid``) in the logout token. With ``sid``, only the one matching session ends, not every session of the user. The ID Token issued at login has to carry the same ``sid``.

Behavior
--------

- The OP posts a ``logout_token`` parameter to ``/sso/logout``. |Fess| answers ``200`` when the logout was recorded and ``400`` otherwise, with ``Cache-Control: no-store`` in both cases.
- The logout token is checked for its signature (RS256, RS384, RS512, ES256, ES384 or ES512, with a key of the ``jwks_uri`` document), ``iss`` (``oic.issuer``), ``aud`` (``oic.client.id``), ``iat`` and ``exp`` (the same 300 seconds of clock skew as for the ID Token; a token issued more than an hour ago is refused), ``jti``, ``events``, the absence of ``nonce``, and the presence of ``sid`` or ``sub``. A token that fails a check, and a token that was already accepted (the same ``jti``), are refused with ``400`` and no session ends. When ``oic.jwks.uri`` is not set, every logout request is refused with ``400`` as well.
- With ``sid`` in the token, only the session of the login that has that ``sid`` ends. With ``sub`` only, every session of that user that was opened before |Fess| received the request ends. A login whose ID Token had no ``sid`` is not ended by a token that carries ``sid``.
- A session ends when it is next used, and that request is handled as anonymous. No logout is sent back to the OP; only the |Fess| session ends. The audit log records ``SESSION_END`` with ``reason`` ``idp_session_ended`` (see :doc:`../install/security`).
- The logout is recorded in the coordinator index of the search engine (``fess_config.coordinator``), which every node reads, so it works with several nodes whether or not the HTTP sessions are shared with ``FESS_SESSION_STORE=opensearch``. On the node that received the request, the session ends at its next request without delay. Another node checks the record at most every 30 seconds, so a session can continue there for up to 30 seconds after the request.
- If the coordinator index cannot be read, no session is ended (one warning is logged). With ``sub`` only, the time of a login can be compared with the time another node received the request, so keep the clocks of the nodes in sync.
- The first refused request of each kind is logged as a warning, and the later ones at DEBUG level. No token, ``sid`` or ``sub`` is logged.
- Encrypted logout tokens (JWE) and front-channel logout are not supported.

Configuration Examples
======================

Minimal Configuration (for Testing)
-------------------------------------

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
-------------------------------------------

The following is a recommended configuration example for production environments.

::

    # Enable SSO
    sso.type=oic

    # Provider configuration
    oic.auth.server.url=https://op.example.com/authorize
    oic.token.server.url=https://op.example.com/token

    # Issuer (the "issuer" value of the Discovery document)
    oic.issuer=https://op.example.com

    # Client configuration
    oic.client.id=your-client-id
    oic.client.secret=your-client-secret
    oic.scope=openid email profile

    # Base URL (use HTTPS for production)
    oic.base.url=https://fess.example.com

Troubleshooting
===============

Common Problems and Solutions
------------------------------

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
- If login fails, ``fess.log`` contains a warning ``Failed to process the OpenID Connect callback:`` followed by the reason
- ``The ID token was not issued for this client``: ``aud`` of the ID Token is not ``oic.client.id``; check the client ID
- ``The ID token has expired``: the clocks of the |Fess| host and the OP differ by more than 300 seconds; synchronize the time (NTP)
- ``The ID token was not issued by the configured issuer``: ``oic.issuer`` differs from the ``iss`` shown in the message; copy the ``issuer`` value of the Discovery document exactly
- ``oic.token.server.url must be https``: use an HTTPS token endpoint URL (``http`` works only for ``localhost``, ``127.x.x.x`` and ``::1``; ``http`` to a Docker Compose service name or an internal host name is refused too)

Cannot Retrieve User Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ensure that the scope includes the required permissions (``email``, ``profile``, etc.)
- Verify that the required scopes are allowed for the client on the OP side
- With Microsoft Entra ID, the ``groups`` claim carries group ``ObjectId`` GUIDs unless a different
  source attribute is selected, so the values will not match group names
- Microsoft Entra ID omits the ``groups`` claim entirely when the user belongs to more than 200
  groups (nested groups count toward this limit), and |Fess| then falls back to
  ``oic.default.groups``

Debug Configuration
--------------------

To investigate problems, you can output detailed OpenID Connect-related logs by adjusting the |Fess| log level.

In ``app/WEB-INF/classes/log4j2.xml``, add the following logger to change the log level:

::

    <Logger name="org.codelibs.fess.sso.oic" level="DEBUG"/>

.. warning::
   With this logger at DEBUG, the claims of the ID Token (such as ``email`` and ``groups``) are
   written to the log file. Restore the log level once the investigation is over, and handle the
   log output accordingly.

Reference
=========

- :doc:`security-role` - Role-based search configuration
- :doc:`sso-saml` - SSO configuration with SAML authentication
- :doc:`sso-entraid` - SSO configuration for Microsoft Entra ID (if you are using Entra ID, you may use this dedicated configuration instead of the generic OpenID Connect settings)
