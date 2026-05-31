============================
Authentication / Session API
============================

Overview
========

The v2 API uses session-based authentication.
Log in via ``POST /auth/login``; on success, a session is established and a CSRF token is issued.

State-changing requests (``POST``) require the ``X-Fess-CSRF-Token`` header.
For information on how to obtain and rotate CSRF tokens, as well as the common response envelope and error model, see :doc:`api-overview`.

This page describes the following four endpoints:

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: Endpoint List
   :header-rows: 1
   :widths: 25 15 60

   * - Endpoint
     - Method
     - Description
   * - ``/auth/me``
     - GET
     - Retrieves the currently authenticated user.
   * - ``/auth/login``
     - POST
     - Logs in with a username and password.
   * - ``/auth/logout``
     - POST
     - Logs out (idempotent).
   * - ``/auth/password``
     - POST
     - Changes the current user's password.

.. _api-auth-userpayload:

Common User Information (UserPayload)
======================================

User information included in the responses of ``GET /auth/me`` and ``POST /auth/login`` is returned in the common ``UserPayload`` structure.
All array fields are non-null; an empty array is returned when there are no values.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``user_id``
     - string
     - User ID. (Required)
   * - ``username``
     - string
     - Display username for the SPA account menu. Currently the same value as ``user_id``, but may be provided independently by the backend in the future. (Required)
   * - ``name``
     - string
     - Display name for the SPA account menu. Currently the same value as ``user_id``. (Required)
   * - ``roles``
     - string[]
     - Array of user roles. (Required)
   * - ``groups``
     - string[]
     - Array of user groups. (Required)
   * - ``permissions``
     - string[]
     - Array of user permissions. (Required)
   * - ``editable``
     - boolean
     - Whether the user information is editable. (Required)
   * - ``admin``
     - boolean
     - ``true`` when the user has any of the configured ``authentication.admin.roles``. Controls the display of the "Administration" item in the SPA. (Required)

Fetching Authentication State
==============================

Request
-------

==================  ====================================================
HTTP Method         GET
Endpoint            ``/api/v2/auth/me``
==================  ====================================================

Retrieves the currently authenticated user.
An anonymous call does not result in an error; it returns ``authenticated: false``.
When authenticated, ``user`` holds the :ref:`UserPayload <api-auth-userpayload>`.

Response
--------

On success (HTTP 200), the following response is returned in the common envelope format (example for authenticated user).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "authenticated": true,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        }
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Response Information
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``authenticated``
     - boolean
     - Whether authenticated. (Required)
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`. Present only when ``authenticated`` is ``true``.

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response
   :header-rows: 1
   :widths: 25 75

   * - Status Code
     - Description
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 500 Internal Server Error
     - An internal server error occurred.

Login
=====

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/auth/login``
==================  ====================================================

Logs in with a username and password.
On successful login, the servlet session ID is rotated, a new CSRF token is issued, and the rate-limit buckets for the caller's IP and the target user are cleared.
If the rate limit is exceeded, a ``Retry-After`` header (in seconds) is included.

Even if a session is already authenticated, no short-circuit occurs; the provided credentials are always validated.

``return_to`` must be a relative path matching ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$``.
Additionally, protocol-relative paths (starting with ``//``) and paths containing ASCII control characters are rejected and silently removed from the echoed response.

.. note::

   This endpoint is **exempt from CSRF validation** (because no token exists before login).

.. note::

   Unlike other state-changing endpoints, this endpoint consolidates oversized request bodies and unsupported ``Content-Type`` into ``400 invalid_request`` (other endpoints return ``413`` / ``415``).

Request Body (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type is ``application/json``.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - Field
     - Type
     - Required
     - Description
   * - ``username``
     - string
     - Yes
     - Username. ``minLength`` is 1.
   * - ``password``
     - string
     - Yes
     - Password. ``minLength`` is 1.
   * - ``return_to``
     - string
     - No
     - Redirect destination after login. Must be a relative path matching the pattern above.

Request example:

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

Response
--------

On success (HTTP 200, LoginResponse), the following response is returned in the common envelope format.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Response Information
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`.
   * - ``csrf_token``
     - string
     - New CSRF token associated with the new session. (Required)
   * - ``return_to``
     - string
     - Echoed only if the request value passed the allowlist.

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response
   :header-rows: 1
   :widths: 25 75

   * - Status Code
     - Description
   * - 400 Bad Request
     - The request is invalid (including oversized request body or unsupported ``Content-Type``).
   * - 401 Unauthorized
     - The credentials are invalid.
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 429 Too Many Requests
     - The rate limit was exceeded. The ``Retry-After`` header indicates the number of seconds to wait.
   * - 500 Internal Server Error
     - An internal server error occurred.

Logout
======

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/auth/logout``
==================  ====================================================

Logs out. This operation is idempotent; if there is no active session, it is a no-op and does not return an error. Always returns ``ok: true``.

The ``X-Fess-CSRF-Token`` header is required.

Response
--------

On success (HTTP 200, OkResponse), the following response is returned in the common envelope format.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Response Information
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``ok``
     - boolean
     - Always ``true``. (Required)

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response
   :header-rows: 1
   :widths: 25 75

   * - Status Code
     - Description
   * - 403 Forbidden
     - The CSRF token is missing or expired.
   * - 405 Method Not Allowed
     - A method other than POST was specified. The ``Allow: POST`` header is included.

Password Change
===============

Request
-------

==================  ====================================================
HTTP Method         POST
Endpoint            ``/api/v2/auth/password``
==================  ====================================================

Changes the current user's password.
Validates ``current_password``, applies the configured password policy to ``new_password``, invalidates the current session, and returns ``re_login_required: true`` to prompt the SPA to redirect to the login page.

Since the session is destroyed server-side, ``csrf_token`` is not returned. The SPA must obtain a new token after re-authentication.

The ``X-Fess-CSRF-Token`` header is required.

Request Body (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type is ``application/json``.

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - Field
     - Type
     - Required
     - Description
   * - ``current_password``
     - string
     - Yes
     - Current password. ``minLength`` is 1.
   * - ``new_password``
     - string
     - Yes
     - New password. Must satisfy the configured password policy. ``minLength`` is 1.
   * - ``confirm_password``
     - string
     - Yes
     - Confirmation password. Must match ``new_password``. ``minLength`` is 1.

Response
--------

On success (HTTP 200), the following response is returned in the common envelope format.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

Each element of ``response`` is as follows:

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Response Information
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Type
     - Description
   * - ``ok``
     - boolean
     - Always ``true``. (Required)
   * - ``re_login_required``
     - boolean
     - Always ``true``. The current session has been invalidated server-side. The SPA must redirect to the login page to obtain a new session and CSRF token. (Required)

Error Response
--------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Error Response
   :header-rows: 1
   :widths: 25 75

   * - Status Code
     - Description
   * - 400 Bad Request
     - The request is invalid.
   * - 401 Unauthorized
     - Authentication is required, or ``current_password`` is invalid.
   * - 403 Forbidden
     - The CSRF token is missing or expired.
   * - 405 Method Not Allowed
     - An unsupported HTTP method was specified.
   * - 413 Payload Too Large
     - The request body exceeds the size limit.
   * - 415 Unsupported Media Type
     - The ``Content-Type`` is not supported.
   * - 429 Too Many Requests
     - The rate limit was exceeded.
   * - 500 Internal Server Error
     - An internal server error occurred.
