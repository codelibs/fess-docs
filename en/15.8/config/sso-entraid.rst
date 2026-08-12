===================================
SSO Configuration with Entra ID
===================================

Overview
========

|Fess| supports Single Sign-On (SSO) authentication using Microsoft Entra ID (formerly Azure AD).
By using Entra ID authentication, you can integrate user information and group information from your Microsoft 365 environment with |Fess| role-based search.

How Entra ID Authentication Works
---------------------------------

In Entra ID authentication, |Fess| operates as an OAuth 2.0/OpenID Connect client and collaborates with Microsoft Entra ID for authentication.

1. User accesses the |Fess| SSO endpoint (``/sso/``)
2. |Fess| redirects to the Entra ID authorization endpoint
3. User authenticates with Entra ID (Microsoft sign-in)
4. Entra ID redirects the authorization code to |Fess|
5. |Fess| uses the authorization code to obtain an access token
6. User is logged in
7. In the background, |Fess| uses the Microsoft Graph API to retrieve the user's group and role information and applies it to role-based search once resolution completes

.. note::
   From |Fess| 15.8, the authorization response in step 4 is returned as a GET request, because
   |Fess| asks the authorization endpoint for ``response_mode=query``. Up to 15.7 it was returned
   as a cross-site POST, and the shipped default ``tomcat.sameSiteCookies = lax`` does not send the
   session cookie on such a request, so ``tomcat.sameSiteCookies = none`` was required as a
   workaround. If you set ``none`` only for that reason, you can restore the default.

For role-based search integration, see :doc:`security-role`.

Prerequisites
=============

Before configuring Entra ID authentication, verify the following prerequisites:

- |Fess| 15.8 or later is installed
- A Microsoft Entra ID (Azure AD) tenant is available
- |Fess| is accessible via HTTPS (required for production environments)
- You have permission to register applications in Entra ID

Basic Configuration
===================

Enabling SSO
------------

To enable Entra ID authentication, add the following setting in ``app/WEB-INF/conf/system.properties``:

::

    sso.type=entraid

Required Settings
-----------------

Configure the information obtained from Entra ID.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``entraid.tenant``
     - Tenant ID (e.g., ``xxx.onmicrosoft.com``)
     - (Required)
   * - ``entraid.client.id``
     - Application (Client) ID
     - (Required)
   * - ``entraid.client.secret``
     - Client secret value
     - (Required)
   * - ``entraid.reply.url``
     - Redirect URI (Callback URL)
     - Uses request URL

.. note::
   Instead of the ``entraid.*`` prefix, you can also use the legacy ``aad.*`` prefix for backward compatibility.

Optional Settings
-----------------

The following settings can be added as needed.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Property
     - Description
     - Default
   * - ``entraid.authority``
     - Authentication server URL
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - State time-to-live (seconds)
     - ``3600``
   * - ``entraid.response.mode``
     - How the authorization response is returned. Either ``query`` or ``form_post``.
     - ``query``
   * - ``entraid.default.groups``
     - Default groups (comma-separated)
     - (None)
   * - ``entraid.default.roles``
     - Default roles (comma-separated)
     - (None)
   * - ``entraid.permission.fields``
     - Group/role fields (comma-separated) to additionally use as permission values. The group/role ID (GUID) is always used as a permission, and the values of the fields specified here (e.g., ``mail``) are added.
     - ``mail``
   * - ``entraid.use.ds``
     - Domain service integration. When ``true``, for permission values in the ``name@domain`` format, the local part (``name``) with the domain part removed is also added as a permission.
     - ``true``

.. note::

   The group/role ID (GUID) is always used as a permission, but only mail-enabled groups have a
   ``mail`` value. Microsoft 365 groups are mail-enabled, so their name is registered as a
   permission as well. **Security groups are not mail-enabled, so with the default only their GUID
   becomes a permission.** If file system access rights name a security group, the permissions do
   not match and those documents do not appear in search results.

   In that case, add ``displayName``, which every group has:

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` is not domain-qualified and is not unique, which is why it is not in the
   default. For example, if Entra ID has a group named ``Administrators``, it also matches
   documents whose access rights name the built-in Windows ``Administrators`` group. Before adding
   it, check that the names do not collide with the ones already used in your access rights.

.. note::
   With the default ``query``, the authorization code is included in the query string of the
   callback URL. ``form_post`` keeps the code out of the URL, and therefore out of browser history
   and the access logs of any front-end proxy or WAF, but it makes the callback a cross-site POST
   and requires ``tomcat.sameSiteCookies = none``. Without that setting the session cookie is not
   sent back and login fails, so most deployments should keep the default. Any other value is
   ignored with a warning and ``query`` is used.

Entra ID Side Configuration
===========================

App Registration in Azure Portal
--------------------------------

1. Sign in to `Azure Portal <https://portal.azure.com/>`_

2. Select **Microsoft Entra ID**

3. Go to **Manage** → **App registrations** → **New registration**

4. Register the application:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Setting
        - Value
      * - Name
        - Any name (e.g., Fess SSO)
      * - Supported account types
        - "Accounts in this organizational directory only"
      * - Platform
        - Web
      * - Redirect URI
        - ``https://<Fess host>/sso/``

5. Click **Register**

Creating a Client Secret
------------------------

1. On the app details page, click **Certificates & secrets**

2. Click **New client secret**

3. Set a description and expiration, then click **Add**

4. Copy and save the generated **Value** (this value will not be shown again)

.. warning::
   The client secret value is only displayed immediately after creation.
   Be sure to record it before navigating away from the page.

Configuring API Permissions
---------------------------

1. Click **API permissions** in the left menu

2. Click **Add a permission**

3. Select **Microsoft Graph**

4. Select **Delegated permissions**

5. Add the following permission:

   - ``User.Read`` - Required to retrieve the signed-in user's group memberships (``/me/memberOf``). Granted by default when the app registration is created
   - ``GroupMember.Read.All`` - Required to read group attributes such as the group name, and to resolve nested groups

6. Click **Add permissions**

7. Click **Grant admin consent for <tenant name>**

.. note::
   Admin consent requires tenant administrator privileges.

.. note::
   ``Group.Read.All`` or ``Directory.Read.All`` can be granted instead of
   ``GroupMember.Read.All``, and the group attribute lookup and the nested group resolution still
   work. However, ``/me/memberOf`` is not authorized by ``Group.Read.All``, so ``User.Read`` is
   required in either case.

.. note::
   |Fess| requests the ``https://graph.microsoft.com/.default`` scope when acquiring a token, and from 15.8 it also sends ``openid profile offline_access https://graph.microsoft.com/.default`` to the authorization endpoint so that consent is requested for the same set. This means that all access permissions configured and consented to on the app registration are used. Therefore, to retrieve group information, you must add the permissions above to the app registration and grant administrator consent.

Information to Obtain
---------------------

The following information is used for Fess configuration:

- **Application (Client) ID**: Found on the Overview page as "Application (client) ID"
- **Tenant ID**: Found on the Overview page as "Directory (tenant) ID" or in ``xxx.onmicrosoft.com`` format
- **Client secret value**: The value created in Certificates & secrets

Group and Role Mapping
======================

With Entra ID authentication, |Fess| automatically retrieves the groups and roles that a user belongs to using the Microsoft Graph API.
The retrieved group IDs and group names can be used for |Fess| role-based search.

Nested Groups
-------------

|Fess| retrieves not only groups that users directly belong to, but also parent groups (nested groups) recursively.
Both the direct membership lookup and the parent group lookup run in the same background task after login, so login itself is never slowed down by Microsoft Graph.
The parent group lookup targets up to a certain number of levels, and the retrieved results are cached for a certain period.
When that background task completes, the user's permissions are recalculated.

Default Group Settings
----------------------

To assign common groups to all Entra ID users:

::

    entraid.default.groups=authenticated_users,entra_users

Configuration Examples
======================

Minimal Configuration (for Testing)
-----------------------------------

The following is a minimal configuration example for verification in a test environment.

::

    # Enable SSO
    sso.type=entraid

    # Entra ID settings
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Recommended Configuration (for Production)
------------------------------------------

The following is a recommended configuration example for production environments.

::

    # Enable SSO
    sso.type=entraid

    # Entra ID settings
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Default groups (optional)
    entraid.default.groups=authenticated_users

Legacy Configuration (Backward Compatibility)
---------------------------------------------

For compatibility with previous versions, the ``aad.*`` prefix can also be used.
When each ``entraid.*`` property is not set, the value of the corresponding ``aad.*`` property is used.
In addition, ``sso.type=aad`` is treated the same as ``sso.type=entraid``.

::

    # Enable SSO (sso.type=aad can also be used)
    sso.type=entraid

    # Legacy configuration keys
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Troubleshooting
===============

Common Issues and Solutions
---------------------------

Cannot Return to Fess After Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the Redirect URI is correctly configured in the Azure Portal app registration
- Ensure the ``entraid.reply.url`` value exactly matches the Azure Portal configuration
- Check that the protocol (HTTP/HTTPS) matches
- Verify the Redirect URI ends with ``/``
- If ``entraid.response.mode`` is set to ``form_post``, verify that ``tomcat.sameSiteCookies = none`` is configured. Without it, the session cookie is not sent with the callback and the sign-in screen keeps reappearing

Authentication Errors Occur
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the Tenant ID, Client ID, and Client Secret are correctly configured
- Check that the client secret has not expired
- Verify that admin consent has been granted for API permissions

Cannot Retrieve Group Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the ``User.Read`` and ``GroupMember.Read.All`` permissions have been granted
  (``Group.Read.All`` or ``Directory.Read.All`` can replace ``GroupMember.Read.All``, but
  ``/me/memberOf`` still requires ``User.Read``)
- Verify that admin consent has been granted
- Check that the user belongs to groups in Entra ID
- If nested parent groups cannot be resolved, ``Not allowed to read the parent groups of ...`` is
  logged as a warning. Grant ``GroupMember.Read.All`` in that case
- |Fess| resolves the user's group and role membership in the background after login completes,
  so login itself never waits on Microsoft Graph. Until resolution finishes, the user is missing
  only the group- and role-scoped permissions — their own user-level permission, and any groups
  and roles configured in ``entraid.default.groups`` and ``entraid.default.roles``, are present
  from the first request — so documents they should be able to see may be temporarily missing
  from search results. The search screen shows a message while resolution is in progress
- If resolution fails, the search screen shows a message, and asks the user to contact an
  administrator if the problem keeps happening. The failure is not necessarily final: resolution
  is retried whenever the access token is renewed, and a later success clears the message and
  restores the missing permissions. To retry straight away, the user has to log out and log in
  again — opening the SSO login URL while still logged in only redirects back to the search
  screen

Debug Settings
--------------

To investigate issues, you can output detailed Entra ID-related logs by adjusting the |Fess| log level.

In ``app/WEB-INF/classes/log4j2.xml``, you can add the following logger to change the log level:

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Reference
=========

- :doc:`security-role` - Role-based search configuration
- :doc:`sso-saml` - SSO configuration with SAML authentication
- :doc:`sso-oidc` - SSO configuration with OpenID Connect authentication
