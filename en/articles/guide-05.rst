===========================================================================
Part 5: Tailoring Search to Users -- Role-Based Search Result Control
===========================================================================

Introduction
============

In the previous part, we introduced how to integrate multiple data sources for cross-source searching.
However, once cross-source searching becomes available, a new challenge arises:
controlling which information should be visible and which should be restricted.

It would be problematic if confidential HR documents appeared in search results for all employees.
In this article, we will design and build a system that controls search results based on users' departments and permissions, using Fess's role-based search feature.

Target Audience
===============

- Those who need access control on search results
- Those who want to build a search platform with information security in mind
- Those who have basic knowledge of Active Directory or LDAP

Scenario
========

A company has three departments:

- **Sales**: Manages customer information, quotations, and proposals
- **Engineering**: Manages design documents, source code specifications, and meeting minutes
- **HR**: Manages personnel evaluations, salary information, and employment regulations

There are also documents that all departments can access in common (internal policies, employee benefits guides, etc.).

The desired search experience is as follows:

- Sales employees can search only Sales and shared documents
- Engineering employees can search only Engineering and shared documents
- HR employees can search only HR and shared documents
- Management can search all documents

How Role-Based Search Works
============================

Fess's role-based search operates through the following process:

1. **During crawling**: Role information (which roles can access the document) is attached to each document
2. **During login**: The user's role information is retrieved (via Fess internal authentication or external authentication)
3. **During search**: Only documents matching the user's roles are displayed in search results

This mechanism provides access control at the search engine level.

Role Design
============

User and Group Design
----------------------

First, let's organize the relationship between users, groups, and roles in Fess.

.. list-table:: Role Design
   :header-rows: 1
   :widths: 20 30 50

   * - Group
     - Role
     - Accessible Documents
   * - sales (Sales)
     - sales_role
     - Sales documents + shared documents
   * - engineering (Engineering)
     - engineering_role
     - Engineering documents + shared documents
   * - hr (HR)
     - hr_role
     - HR documents + shared documents
   * - management (Management)
     - management_role
     - All documents

Setting Up Groups and Roles in Fess
-------------------------------------

**Creating Roles**

1. In the admin panel, go to [User] > [Role]
2. Create the following roles:

   - ``sales_role``
   - ``engineering_role``
   - ``hr_role``
   - ``management_role``

**Creating Groups**

1. Go to [User] > [Group]
2. Create the following groups:

   - ``sales``
   - ``engineering``
   - ``hr``
   - ``management``

**Creating Users and Assigning Roles**

1. Go to [User] > [User]
2. Assign groups and roles to each user

Assigning Permissions in Crawl Configuration
=============================================

To attach access control information to documents, specify permissions in the crawl configuration.
Permissions are entered in the format ``{role}rolename``, ``{group}groupname``, or ``{user}username``, separated by line breaks.

Department-Specific Crawl Configuration
-----------------------------------------

**Sales File Server**

1. Go to [Crawler] > [File System] > [Create New]
2. Configure the following:

   - Path: ``smb://fileserver/sales/``
   - Permissions: Enter ``{role}sales_role`` and ``{role}management_role`` separated by a line break

With this configuration, documents crawled from the Sales file server can only be viewed in search results by users who have ``sales_role`` or ``management_role``.

**Engineering File Server**

1. Go to [Crawler] > [File System] > [Create New]
2. Configure the following:

   - Path: ``smb://fileserver/engineering/``
   - Permissions: Enter ``{role}engineering_role`` and ``{role}management_role`` separated by a line break

**HR File Server**

1. Go to [Crawler] > [File System] > [Create New]
2. Configure the following:

   - Path: ``smb://fileserver/hr/``
   - Permissions: Enter ``{role}hr_role`` and ``{role}management_role`` separated by a line break

**Shared Documents**

1. Go to [Crawler] > [Web] or [File System] > [Create New]
2. Permissions: Leave the default ``{role}guest``

By default, ``{role}guest`` is automatically entered. Since all users, including guest users, have the ``guest`` role, all users can view these search results.

Integration with External Authentication
==========================================

In real enterprise environments, most organizations want to integrate with an existing directory service rather than using Fess's built-in user management.

Active Directory / LDAP Integration
--------------------------------------

Fess supports LDAP integration, allowing authentication and role assignment using Active Directory user information.

To enable LDAP integration, configure the LDAP connection settings in the Fess configuration file.

The main configuration items are:

- LDAP server URL
- Bind DN (connection account)
- User search base DN
- Group search base DN
- User attribute mapping

When LDAP integration is enabled, users can log in to Fess using their Active Directory accounts.
Since group membership information is automatically reflected as roles, there is no need to manually configure roles for each user in Fess.

SSO Integration
----------------

As a more advanced configuration, integration with Single Sign-On (SSO) is also possible.
Fess supports the following SSO protocols:

- **OpenID Connect (OIDC)**: Entra ID (Azure AD), Keycloak, etc.
- **SAML**: Integration with various IdPs
- **SPNEGO/Kerberos**: Windows Integrated Authentication

With SSO integration, users can automatically access Fess using their regular login credentials, and role information is also automatically reflected.
Details of SSO integration will be covered in Part 15, "Building a Secure Search Platform."

Verification
=============

Once the role-based search configuration is complete, verify that it works correctly.

Verification Steps
-------------------

1. Log in as a Sales user and search for "quotation"
   -- Verify that only Sales and shared documents are displayed

2. Log in as an Engineering user and search with the same keyword
   -- Verify that Sales documents are not displayed

3. Log in as a Management user and search with the same keyword
   -- Verify that documents from all departments are displayed

Verification Checklist
-----------------------

- Documents that the user does not have permission to access must not appear in search results at all
- Shared documents must be displayed for all users
- Search behavior when not logged in (scope of guest access)

Design Considerations
======================

Role Granularity
-----------------

Role granularity should be determined based on organizational structure and security requirements.

**Coarse granularity**: Set roles at the department level (the scenario in this article)

- Advantage: Simple configuration, easy to manage
- Disadvantage: Cannot achieve fine-grained access control within a department

**Fine granularity**: Set roles at the project or team level

- Advantage: Fine-grained access control is possible
- Disadvantage: The number of roles increases, making management more complex

It is recommended to start with coarse granularity and refine as needed.

Integration with File Server ACL
----------------------------------

When crawling file servers, it is also possible to use the file's ACL (Access Control List) information for permission control.
In this case, the permission settings on the file system are directly reflected in search result visibility.

When leveraging file server ACL, check the permission-related configuration items in the crawl settings.

Summary
========

In this article, we designed and built department-specific search result control using Fess's role-based search.

- Designing and registering roles, groups, and users
- Assigning roles to crawl configurations
- Automatic role reflection through Active Directory / LDAP integration
- SSO integration options (OIDC, SAML, SPNEGO)

Role-based search enables you to provide the convenience of cross-source searching while maintaining information security.
This concludes the fundamentals section. Starting from the next part, we will move on to practical solutions, covering how to build a knowledge hub for development teams.

References
==========

- `Fess Role Settings <https://fess.codelibs.org/ja/15.5/admin/role.html>`__

- `Fess LDAP Integration <https://fess.codelibs.org/ja/15.5/config/ldap.html>`__
