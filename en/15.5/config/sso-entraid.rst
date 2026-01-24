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
6. |Fess| uses Microsoft Graph API to retrieve user's group and role information
7. User is logged in and group information is applied to role-based search

For role-based search integration, see :doc:`security-role`.

Prerequisites
=============

Before configuring Entra ID authentication, verify the following prerequisites:

- |Fess| 15.5 or later is installed
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
   * - ``entraid.default.groups``
     - Default groups (comma-separated)
     - (None)
   * - ``entraid.default.roles``
     - Default roles (comma-separated)
     - (None)

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

   - ``Group.Read.All`` - Required to retrieve user group information

6. Click **Add permissions**

7. Click **Grant admin consent for <tenant name>**

.. note::
   Admin consent requires tenant administrator privileges.

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
This processing is executed asynchronously after login to minimize impact on login time.

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

::

    # Enable SSO
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

Authentication Errors Occur
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that the Tenant ID, Client ID, and Client Secret are correctly configured
- Check that the client secret has not expired
- Verify that admin consent has been granted for API permissions

Cannot Retrieve Group Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Verify that ``Group.Read.All`` permission has been granted
- Verify that admin consent has been granted
- Check that the user belongs to groups in Entra ID

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
