================================================
Controlling Search Results with Roles and Groups
================================================

Introduction
============

Once your internal documents can all be searched from a single Fess, the next question is "who gets to see what".
You do not want HR evaluation documents showing up in every employee's search results, and you equally do not want company-wide policies to be visible to only a few people.

In Fess, the values you write in the "Permissions" field of a crawl configuration are recorded with each document, and on every search they are matched against the rights of the user who is logged in.
In this article, we set up per-department access control in Fess 15.9 and work through to checking which documents each user can see.

By following the steps in this article, you will be able to:

- Set up three kinds of visibility (department, executives, all employees) with groups and permissions
- Use Active Directory groups directly as permissions
- Align the visibility of labels with that of the documents
- Check which documents each user can see, and which rights are recorded in a document

SSO configuration is covered in :doc:`guide-15`, and serving several organizations with virtual hosts in :doc:`guide-13`.

How Permissions Work
====================

Writing Permissions
-------------------

In the "Permissions" field of a crawl configuration, write values in the following formats, one per line.
If any one of them matches the user's rights, the document is shown in the search results.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Format
     - Matching users
   * - ``{user}username``
     - That user
   * - ``{group}groupname``
     - Users who belong to that group
   * - ``{role}rolename``
     - Users who have that role
   * - ``(deny){group}groupname``
     - Users who match are not shown the document, even if another value allows it (can also be used with ``{user}`` and ``{role}``)

Rights a User Has
-----------------

On every search, Fess determines the user's rights as follows.

- A logged-in user: ``{user}`` with their own user name, ``{group}`` for each group they belong to, and ``{role}`` for each role they have
- A visitor who is not logged in: ``{role}guest``

The important point here is that logged-in users do not get ``{role}guest``.
The "Permissions" field of a new crawl configuration contains ``{role}guest`` from the start.
If you leave it as is, the documents are visible to visitors who are not logged in, but not to logged-in users.
For documents you want all employees to see, write in the permissions a group (or role) that every employee belongs to.

Note also that the initial user ``admin`` has the roles ``admin`` and ``guest``.
If you search in a browser that is still logged in to the admin console, the search runs as ``admin``, so only ``{role}guest`` documents are shown and department documents are not.

Roles or Groups?
----------------

Roles and groups are matched in exactly the same way.
The difference is where the values come from.
In Fess's own user management, you can assign both roles and groups to each user.
With LDAP (Active Directory) integration, the groups a user belongs to (``memberOf``) become ``{group}groupname`` (only entries whose DN contains ``ou=Role`` become ``{role}``).

In this article, all organizational units such as departments and all employees are expressed as groups, so that the same permission values work for both Fess users and Active Directory.

What We Will Build
==================

As an example, we take a company whose intranet portal ``https://intra.example.com/`` has pages for each department and pages for the whole company.

.. list-table:: Groups and users
   :header-rows: 1
   :widths: 20 40 40

   * - User
     - Department
     - Groups
   * - ``sato``
     - Sales
     - ``Sales``, ``AllStaff``
   * - ``suzuki``
     - Engineering
     - ``Engineering``, ``AllStaff``
   * - ``tanaka``
     - Human Resources
     - ``HR``, ``AllStaff``
   * - ``yamada``
     - Executives
     - ``Executives``, ``AllStaff``

.. list-table:: Permissions of the crawl configurations
   :header-rows: 1
   :widths: 25 40 35

   * - Crawl configuration
     - URL
     - Permissions
   * - Sales
     - ``https://intra.example.com/sales/``
     - ``{group}Sales`` and ``{group}Executives``
   * - Engineering
     - ``https://intra.example.com/dev/``
     - ``{group}Engineering`` and ``{group}Executives``
   * - Human Resources
     - ``https://intra.example.com/hr/``
     - ``{group}HR`` and ``{group}Executives``
   * - Company-wide
     - ``https://intra.example.com/common/``
     - ``{group}AllStaff``

With this setup, each user sees the following documents.

.. list-table:: Documents visible to each user
   :header-rows: 1
   :widths: 30 70

   * - User
     - Documents in the search results
   * - ``sato``
     - Sales, Company-wide
   * - ``suzuki``
     - Engineering, Company-wide
   * - ``tanaka``
     - Human Resources, Company-wide
   * - ``yamada``
     - Sales, Engineering, Human Resources, Company-wide
   * - Visitors who are not logged in
     - None
   * - ``admin`` (search page)
     - None

If you also want visitors who are not logged in to see the company-wide documents, add ``{role}guest`` to the company-wide configuration as well.
In that case, ``admin`` also sees the company-wide documents.

Group names are matched case-sensitively.
``{group}sales`` and ``{group}Sales`` are treated as different groups, so spell the group name and the permission value exactly the same way.

Setting Up with Fess Users
==========================

Creating Groups and Users
-------------------------

1. In the admin console, go to [User] > [Group], click [Create New], enter ``Sales`` in "Name" and click [Create]. Create ``Engineering``, ``HR``, ``Executives`` and ``AllStaff`` in the same way
2. In [User] > [User], click [Create New] and enter "Username", "Password" and "Password (Confirm)". The password must be at least 8 characters long
3. In "Groups", select the groups as shown in the table above, and click [Create]

Users, groups and roles are stored in OpenSearch, so they remain even if you recreate the containers in Docker.

Creating the Crawl Configurations
---------------------------------

For each department, create a crawl configuration in [Crawler] > [Web].
The following table shows the Sales example.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Value
   * - Name
     - ``Sales Portal``
   * - URLs
     - ``https://intra.example.com/sales/``
   * - Included URLs
     - ``https://intra.example.com/sales/.*``
   * - Permissions
     - Delete the default ``{role}guest`` and enter the following two lines

::

    {group}Sales
    {group}Executives

Create Engineering, Human Resources and Company-wide in the same way, changing the URL and permissions as shown in the table.
When you have created them, click [Start Now] for "Default Crawler" in [System] > [Scheduler] to run the crawl.
For how to check that the crawl has finished, see :doc:`guide-02`.

.. note::

   In file system crawl configurations (SMB or local files), the rights read from the file's ACL are recorded in the document **in addition to** the values in "Permissions".
   This behavior is enabled by default.
   As a result, documents on a file server may be visible more widely than the scope written in "Permissions".
   For how to combine this with ACLs, see :doc:`file-server-search`.
   Permissions in data store crawl configurations are covered in :doc:`datastore-basics`.

Using Active Directory Groups
=============================

If your users are managed in Active Directory, configure LDAP integration instead of creating users and groups in Fess.
The groups in the logged-in user's ``memberOf`` attribute become ``{group}`` rights.

Configuring the LDAP Connection
-------------------------------

Fill in the "LDAP" section of [System] > [General] and click [Update].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Example
   * - LDAP URL
     - ``ldap://ad.example.com:389``
   * - Base DN
     - ``dc=example,dc=com``
   * - Bind DN
     - ``cn=fess,cn=Users,dc=example,dc=com`` (a service account for lookups)
   * - Password
     - The service account's password
   * - User DN
     - ``%s@example.com`` (``%s`` is replaced by the login name)
   * - Account Filter
     - ``sAMAccountName=%s``
   * - memberOf Attribute
     - ``memberOf``

For details of each field, and how to write a "Group Filter" that resolves nested groups, see the `LDAP Integration Guide <https://fess.codelibs.org/stable/config/ldap-integration.html>`__.

.. warning::

   The [General] settings are saved in ``system.properties``.
   In the docker-fess setup, this file is inside the ``fess01`` container, so it is lost when you recreate the container with ``down`` → ``up`` (see the section on stopping and restarting in :doc:`guide-02`).

Mapping Group Names to Permissions
----------------------------------

The value of the innermost ``CN`` in the group's DN becomes the group name.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - memberOf value
     - User's right
   * - ``CN=Sales,OU=Groups,DC=example,DC=com``
     - ``{group}Sales``
   * - ``CN=AllStaff,OU=Groups,DC=example,DC=com``
     - ``{group}AllStaff``

If you name the groups in Active Directory ``Sales``, ``Engineering``, ``HR``, ``Executives`` and ``AllStaff``, the crawl configurations from the previous chapter work unchanged.
If the names differ, rewrite the permission values to match the Active Directory group names.

For all employees, prepare a group that everyone belongs to directly.
The Active Directory primary group (usually ``Domain Users``) is not included in the ``memberOf`` attribute, so writing ``{group}Domain Users`` does not match.

To check which rights a user received, set the log level of ``org.codelibs.fess.ldap`` to DEBUG.
When the rights are obtained from LDAP, a line starting with ``Roles:`` is written to ``fess.log``.
For how to configure this, see "Debug Settings" in the LDAP Integration Guide.
The values on this line are shown in the internal format described later (such as ``2Sales``).

To let users log in with SSO (Entra ID, OpenID Connect, SAML or SPNEGO), you need the ``fess-sso-*`` plugin for that method.
How groups and roles are received also differs by method, so see :doc:`guide-15`.

Aligning the Visibility of Labels
=================================

Labels also have "Permissions", which decide whether the label is shown among the label choices on the search page.
They do not affect whether documents are shown, but new labels also contain ``{role}guest`` from the start, so as is they are not shown in the choices for logged-in users.

Here is an example of a label to attach to Human Resources documents.
In [Crawler] > [Label], click [Create New] and enter the following.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Value
   * - Name
     - ``Human Resources``
   * - Value
     - ``hr`` (alphanumeric characters and underscores only)
   * - Included Paths
     - ``https://intra.example.com/hr/.*``
   * - Permissions
     - ``{group}HR`` and ``{group}Executives`` (the same scope as the documents)

A label's permissions take effect in the choices as soon as you save it.
The "Included Paths" that attach the label to documents, on the other hand, are applied at crawl time, so run a crawl after creating the label.

Recrawl After Changing Rights
=============================

Permissions are recorded in documents at crawl time.
Changing the "Permissions" of a crawl configuration does not change the rights of documents already in the index.
After the change, run a job that includes that crawl configuration (such as "Default Crawler").

For web and file system crawl configurations, documents whose rights have changed are fetched again on the next crawl, and the old document with the same URL is replaced.
Until the recrawl finishes, the documents keep appearing in search results with the old rights.
When you narrow the visibility, run the crawl right away.

To recrawl just one crawl configuration immediately, click [Create New Job] on that crawl configuration's details page, and run the created job with [Start Now].

Checking the Behavior
=====================

Searching as Each User
----------------------

1. Open ``http://localhost:8080/`` in a private browser window. In a window that is logged in to the admin console, searches run as ``admin``
2. Search without logging in, and check that no department or company-wide documents are shown
3. Log in as ``sato`` from the login link at the top of the search page, and check that only Sales and company-wide documents are shown
4. Click the user name at the top of the page, select "Logout", and check the same with ``suzuki``, ``tanaka`` and ``yamada``

When checking, searching for a word that appears in every document (for example, your company name) makes it easier to compare the range of documents shown.

Viewing the Rights Recorded in a Document
-----------------------------------------

If documents are not shown as you expect, check the rights recorded in the document.

1. In the admin console, open [System Info] > [Search] and search for words from the document's URL or title. This screen does not filter by rights and shows all documents
2. Click [Update] for the target document to open the edit screen, where the rights recorded in the ``role`` field are shown. Only look; do not save

The values in the ``role`` field are shown in the following internal format.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Permission
     - Shown in the role field
     - Example
   * - ``{user}username``
     - ``1`` + name
     - ``1sato``
   * - ``{group}groupname``
     - ``2`` + name
     - ``2Sales``
   * - ``{role}rolename``
     - ``R`` + name
     - ``Rguest``
   * - With ``(deny)``
     - ``D`` prefixed
     - ``D2Sales``

If the ``role`` field of a Sales document contains ``2Sales`` and ``2Executives``, the permissions are recorded as configured.
If ``Rguest`` remains, either you have not recrawled after changing the permissions, or you forgot to delete the default ``{role}guest``.

Showing Nothing to Users Who Are Not Logged In
==============================================

If you place Fess on a network that people outside the company can reach, or if you do not allow searching without logging in at all, enable "Login Required" in [System] > [General].
When enabled, visitors who are not logged in can no longer search.

This setting is independent of access control by permissions.
Even if documents with ``{role}guest`` remain, they are no longer shown to visitors who are not logged in.
This setting is also saved in ``system.properties``, so in Docker the same caution applies as for the LDAP settings.

What to Read Next
=================

- Control visibility using file server ACLs: :doc:`file-server-search`
- Let users log in with their company accounts via SSO: :doc:`guide-15`
- Use one Fess for several organizations: :doc:`guide-13`
- Add rights to documents from Slack or cloud storage: :doc:`datastore-basics`
- Search a development team's Git, Confluence, Jira and Slack: :doc:`guide-06`

References
==========

- `Role-Based Search Configuration <https://fess.codelibs.org/stable/config/security-role.html>`__
- `Role Search (for users) <https://fess.codelibs.org/stable/user/role-search.html>`__
- `LDAP Integration Guide <https://fess.codelibs.org/stable/config/ldap-integration.html>`__
- `User <https://fess.codelibs.org/stable/admin/user-guide.html>`__
- `Group <https://fess.codelibs.org/stable/admin/group-guide.html>`__
- `Label <https://fess.codelibs.org/stable/admin/labeltype-guide.html>`__
- `Search (admin console) <https://fess.codelibs.org/stable/admin/searchlist-guide.html>`__
