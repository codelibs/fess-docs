============================================================
Part 15: Secure Search Infrastructure -- SSO Integration and Search Access Control in a Zero Trust Environment
============================================================

Introduction
============

Enterprise information security requirements are becoming increasingly stringent year after year.
Since search systems aggregate vast amounts of confidential documents, proper authentication and authorization mechanisms are essential.

In this article, we build upon the role-based search introduced in Part 5 and design a security architecture centered on SSO (Single Sign-On) integration.

Target Audience
===============

- Those operating Fess in an enterprise environment
- Those designing SSO integration (OIDC, SAML)
- Those who understand the concepts of zero trust security

Organizing Security Requirements
==================================

Let us organize the typical security requirements for enterprises.

.. list-table:: Security Requirements
   :header-rows: 1
   :widths: 30 70

   * - Requirement
     - Description
   * - Single Sign-On
     - Integrate with an existing IdP to eliminate additional login operations
   * - Role-Based Access
     - Control search results according to user affiliation and permissions
   * - Communication Encryption
     - Encrypt all communications via HTTPS
   * - API Access Control
     - Token-based API authentication and permission management
   * - Audit Logs
     - Record who searched for what

SSO Integration Options
========================

Let us organize the SSO protocols supported by Fess and the scenarios where each is applicable.

.. list-table:: Comparison of SSO Protocols
   :header-rows: 1
   :widths: 20 30 50

   * - Protocol
     - Representative IdPs
     - Applicable Scenarios
   * - OpenID Connect
     - Entra ID, Keycloak, Google
     - Cloud environments, modern authentication infrastructure
   * - SAML 2.0
     - Entra ID, Okta, OneLogin
     - Enterprise environments, when an existing SAML IdP is available
   * - SPNEGO/Kerberos
     - Active Directory
     - Windows Integrated Authentication environments

SSO Integration via OpenID Connect / Entra ID
================================================

This is the most modern and recommended approach.
In addition to generic OpenID Connect integration, Fess also provides dedicated integration functionality for Entra ID (Azure AD).
Here, we explain the integration using Entra ID as an example.

Authentication Flow Overview
-----------------------------

1. A user accesses Fess
2. Fess redirects the user to the Entra ID authentication screen
3. The user authenticates with Entra ID (including MFA)
4. Entra ID returns an authentication token to Fess
5. Fess retrieves user information and group information from the token
6. Roles are assigned based on group information
7. Search results are provided based on roles

Entra ID Configuration
-----------------------

1. Register an application in Entra ID
2. Configure the redirect URI (Fess OIDC callback URL)
3. Grant the required API permissions (User.Read, GroupMember.Read.All, etc.)
4. Obtain the client ID and secret

Fess Configuration
-------------------

Configure the SSO connection information on the [System] > [General] page in the administration console.
The main configuration items are as follows:

- OpenID Connect provider URL (Entra ID endpoint)
- Client ID
- Client secret
- Scopes (openid, profile, email, etc.)
- Group claim settings

Group-to-Role Mapping
----------------------

Map Entra ID groups to Fess roles.
This allows group management in Entra ID to be directly reflected in search result control.

Example: Entra ID group "Engineering" -> Fess role "engineering_role"

SSO Integration via SAML
==========================

SAML integration is suitable for environments with an existing SAML IdP.

Authentication Flow Overview
-----------------------------

In SAML, SAML Assertions are exchanged between the SP (Service Provider = Fess) and the IdP.

1. A user accesses Fess
2. Fess sends a SAML AuthnRequest to the IdP
3. The IdP authenticates the user
4. The IdP returns a SAML Response (containing user attributes) to Fess
5. Fess assigns roles based on user attributes

Fess Configuration
-------------------

The following settings are required for SAML integration:

- IdP metadata URL or XML file
- SP entity ID
- Assertion Consumer Service URL
- Attribute mapping (username, email address, groups)

SPNEGO / Kerberos Integration
================================

In Windows Active Directory environments, integrated Windows authentication via SPNEGO/Kerberos can be used.
When accessing via a browser from a PC joined to the domain, authentication occurs automatically without any additional login operation.

This method is the most transparent for users, but the configuration is the most complex.
An Active Directory domain environment is a prerequisite.

Communication Encryption
=========================

SSL/TLS Configuration
----------------------

In production environments, it is recommended that all access to Fess be conducted over HTTPS.

**Reverse Proxy Method (Recommended)**

Deploy Nginx or Apache HTTP Server as a reverse proxy to handle SSL termination.
Fess itself operates over HTTP, and the reverse proxy handles HTTPS.

::

    [Client] --HTTPS--> [Nginx] --HTTP--> [Fess]

The advantage of this method is that certificate management is consolidated at the reverse proxy.

**Direct Fess Configuration Method**

It is also possible to configure SSL certificates directly on Fess's Tomcat.
This is suitable for small-scale environments or when a reverse proxy is not deployed.

API Access Security
=====================

Let us enhance the security of the API integration introduced in Part 11.

Token Permission Design
------------------------

Configure appropriate permissions for access tokens.

.. list-table:: Token Design Example
   :header-rows: 1
   :widths: 25 25 50

   * - Purpose
     - Permissions
     - Notes
   * - Search widget
     - Search only (read-only)
     - Used on the frontend
   * - Batch processing
     - Search + Indexing
     - Used on the server side
   * - Administration automation
     - Admin API access
     - Used in operational scripts

Token Management
-----------------

- Regular rotation (every 3 to 6 months)
- Immediate revocation of tokens that are no longer needed
- Monitoring of token usage

Auditing and Logs
==================

Audit logs in a search system are important for investigating security incidents and ensuring compliance.

Logs Recorded by Fess
----------------------

- **Search logs**: Who searched for what (can be viewed at [System Info] > [Search Log] in the administration console)
- **Audit logs** (``audit.log``): Operations such as login, logout, access, and permission changes are recorded in a unified manner

Log Retention
--------------

Configure the log retention period according to security requirements.
If there are compliance requirements, consider forwarding logs to an external log management system (SIEM).

Summary
========

In this article, we designed a security architecture for Fess in an enterprise environment.

- Three SSO integration options (OIDC, SAML, SPNEGO) and their applicable scenarios
- Design of Entra ID integration via OpenID Connect
- Communication encryption via SSL/TLS
- Permission design for API access tokens
- Audit log management

Build a secure search infrastructure while balancing security and usability.

The next article will cover search infrastructure automation.

References
==========

- `Fess SSO Configuration <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Fess Security Configuration <https://fess.codelibs.org/ja/15.5/config/security.html>`__
