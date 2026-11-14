======================================
Passkey (WebAuthn) Login Configuration
======================================

Overview
========

|Fess| lets a local user (a user created under "User" in the administration screen) log in with a passkey (WebAuthn) instead of a password. The feature is new in 15.10 and is off by default.

- A user can log in with either the password or a passkey. It is not multi-factor authentication that asks for both.
- Only a local user of the ``fess_user`` index is covered. An LDAP or SSO user cannot register a passkey, and a passkey login never asks LDAP.
- |Fess| stores the public key and the name of a passkey and the like. The private key stays in the user's authenticator (a browser, an OS, a security key, and so on) and never reaches |Fess|.

Settings
========

Passkey settings go in ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` for the ZIP package, ``/etc/fess/fess_config.properties`` for RPM/DEB). There is no item for them in "System" > "General" in the administration screen, and they cannot be set in ``system.properties``. A restart of |Fess| is required to apply a change. With Docker, you can pass them as ``-Dfess.config.passkey.enabled=true`` in ``FESS_JAVA_OPTS`` (see :doc:`../install/install-docker`).

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Key
     - Default
     - Description
   * - ``passkey.enabled``
     - ``false``
     - Enables login with a passkey. Even when ``true``, the feature stays off unless ``passkey.rp.id`` and ``passkey.origins`` below hold usable values.
   * - ``passkey.rp.id``
     - (empty)
     - Relying party ID: the domain the passkeys are bound to (for example ``example.com``). A passkey works on this host and its subdomains only.
   * - ``passkey.rp.name``
     - ``Fess``
     - The relying party name the browser shows when a passkey is created.
   * - ``passkey.origins``
     - (empty)
     - The origins (comma-separated) a passkey ceremony is accepted from (for example ``https://fess.example.com``). Each entry must be an ``http`` or ``https`` origin with a host name.

An example that turns the feature on:
::

    passkey.enabled=true
    passkey.rp.id=example.com
    passkey.rp.name=Fess
    passkey.origins=https://fess.example.com

- ``passkey.rp.id`` is the domain every passkey is bound to. Changing it after users have registered passkeys makes all of them unusable, and users have to register again under the new ID, so choose it once. The host of each origin in ``passkey.origins`` must be ``passkey.rp.id`` or a subdomain of it.
- ``passkey.origins`` lists, as they are, the origins (scheme, host and port) users open |Fess| at in the browser, not the addresses behind a reverse proxy. A ceremony from any other origin is rejected.

When the feature stays off
--------------------------

Even with ``passkey.enabled=true``, the passkeys **stay off without any error on the screen** in the cases below. The login screens show no passkey button, every API under ``/api/v2/auth/passkey`` answers ``404``, and ``features.passkey_enabled`` of ``/api/v2/ui/config`` is ``false``. The reason is in a warning in ``fess.log``; each warning is written only once after startup.

- ``passkey.rp.id`` or ``passkey.origins`` is empty: ``passkey.enabled is true but passkey.rp.id or passkey.origins is empty, so passkeys are disabled.``
- ``passkey.origins`` holds no entry: ``passkey.enabled is true but passkey.origins holds no origin, so passkeys are disabled.``
- ``passkey.origins`` holds an entry that is not an ``http`` or ``https`` origin (a value without a host name, another scheme, and so on): ``passkey.origins holds an entry that is not an http or https origin, so passkeys are disabled: entry=...``

When ``passkey.origins`` is usable but the origin a user opens is not in it, every registration and login is rejected. The user's screen shows no reason, so look at ``fess.log``: ``A passkey response came from an origin that is not in passkey.origins: origin=...`` shows the rejected origin and the setting (only the first one is written). Add that origin to ``passkey.origins``.

Usage
=====

Logging in
----------

When passkeys are on and the browser supports WebAuthn, a "Sign in with a passkey" button appears in the login of the search screen and on the login page of the administration screen. The browser asks for the authenticator, and the user logs in without typing a user name.

A passkey login uses the same per-IP-address rate limit (``theme.api.login.*``) as a password login. A failure counts against it, and a success gives the count back (see :doc:`rate-limiting`). The screen does not tell the reason of a failure; it shows the same message as for a wrong password.

Registering and deleting passkeys
---------------------------------

A local user registers and deletes their own passkeys under "Passkeys" on "Change Password" (``/profile``) in the user menu of the search screen.

1. Enter a name for the passkey (up to 64 characters) and the current password, and press "Register a passkey".
2. Follow the browser's prompts to create the passkey on an authenticator.

- The current password is required for each registration. A local user whose name and password the directory (LDAP) also accepts cannot register a passkey, because the password check cannot tell which account it verified.
- A user can have up to 20 passkeys.
- The "Passkeys" section is not shown to a user who has no passkeys and cannot register one (an LDAP or SSO user, or a browser without WebAuthn).
- Deleting a passkey **ends the other login sessions** of the user, so that a session opened with a lost authenticator does not survive. It works the same way as a password change (see "Relation to the password" below). The session that made the deletion stays.

Administrator actions
---------------------

The details page of a user under "User" in the administration screen lists the passkeys of the user (label, creation time, last use time). An administrator cannot register a passkey, but an administrator with the edit permission can delete one with "Reset", for example when the user lost the authenticator. The user can then register a new passkey. A reset also ends the login sessions of that user (see "Relation to the password" below).

After ``passkey.enabled`` is set back to ``false``, the details page still lists the passkeys of a user who has some, and they can be deleted. Turning the feature off does not delete passkey data.

Relation to the password
========================

- A passkey and a password are separate credentials. Changing a user's password, or an administrator setting a new one, does not delete the registered passkeys, and they can still be used to log in.
- When a password is changed, the other login sessions of the user end (see :doc:`../install/security`). This includes a session opened with a passkey. Each session checks at most once every ``password.changed.check.interval`` seconds (default ``60``), so the sessions end within that time.
- Deleting a passkey ends the other sessions the same way (see above).

Deleting and renaming users
===========================

A passkey is bound to a user by the user name only. So that another user of the same name does not inherit it, passkeys are also deleted in these cases:

- When a user is deleted.
- When a user is created (any passkey left under that name is deleted).
- When a user is renamed (the passkeys of both the previous and the new name are deleted). A passkey does not follow a rename, so the user registers again. A rename to a name another user already has is refused before any passkey is deleted.

Storage and backup
==================

Passkeys are stored in the ``fess_user.passkey`` index (the prefix is ``index.user.index``, ``fess_user`` by default). The index is created when |Fess| starts even if passkeys are off, and it is used when a user is deleted or renamed and on the user details page. If |Fess| is not allowed to create indices, create it before the upgrade (see :ref:`upgrade-1510-passkey`).

The index does not join the ``fess_user`` alias, so the ``fess_user.bulk`` of "Backup" in the administration screen does not contain passkeys. After a restore from a backup, users register their passkeys again.

Requirements
============

- **HTTPS**: Browsers allow WebAuthn only in a secure context (HTTPS, or ``localhost``). |Fess| also accepts an ``http`` origin in ``passkey.origins``, but in production serve |Fess| over HTTPS and give ``https://`` origins (see "Enable HTTPS" in :doc:`../install/security`).
- **Browser**: A browser that provides the WebAuthn API (``PublicKeyCredential``) is required. In a browser without it, neither the login button nor the registration section is shown.
- **Authenticator**: It must support discoverable credentials and user verification (a PIN, biometrics, and so on). |Fess| requires both, supports the ES256 and RS256 signature algorithms, and does not use attestation.
- **Multiple nodes**: The challenge of a passkey ceremony is kept in the HTTP session for 5 minutes. When you run several nodes behind a load balancer, share sessions between the nodes (environment variable ``FESS_SESSION_STORE=opensearch``) or make the load balancer pin each session to one node.

API
===

The passkey APIs are under ``/api/v2/auth/passkey``. All of them answer ``404`` while passkeys are off. ``features.passkey_enabled`` of ``/api/v2/ui/config`` tells whether the feature is available (see :doc:`../api/api-uiconfig`).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Endpoint
     - Description
   * - ``POST /api/v2/auth/passkey/login/options``
     - Gets the login options (the challenge).
   * - ``POST /api/v2/auth/passkey/login/verify``
     - Verifies the response of the authenticator and logs in.
   * - ``GET /api/v2/auth/passkey``
     - Lists the passkeys of the signed-in user and tells whether the user can register one (``can_register``).
   * - ``POST /api/v2/auth/passkey/register/options``
     - Checks the current password (``current_password``) and gets the registration options.
   * - ``POST /api/v2/auth/passkey/register/verify``
     - Verifies the name (``label``) and the response of the authenticator, and registers the passkey.
   * - ``DELETE /api/v2/auth/passkey/{credentialId}``
     - Deletes a passkey of the signed-in user.

The ``register`` calls and the deletion need the ``X-Fess-CSRF-Token`` header. The two login calls need no CSRF token, like ``/api/v2/auth/login``.

Troubleshooting
===============

The passkey button is not shown
-------------------------------

- Check ``features.passkey_enabled`` of ``/api/v2/ui/config``. If it is ``false``, look for a warning in ``fess.log`` to see whether the settings are usable (see "When the feature stays off" above).
- Check that |Fess| was restarted after the change.
- Check that the browser supports WebAuthn and that the page is opened over HTTPS (or ``localhost``).
- If you use a theme other than the bundled one, the theme must support the passkey button.

Registration or login fails
---------------------------

- If ``fess.log`` has a warning containing ``is not in passkey.origins``, add the origin opened in the browser to ``passkey.origins``.
- After ``passkey.rp.id`` is changed, passkeys registered before the change cannot be used. Delete the old passkeys and register again.
