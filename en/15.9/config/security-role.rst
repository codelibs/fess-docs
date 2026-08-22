================================
Role-Based Search Configuration
================================

About Role-Based Search
========================

|Fess| can provide different search results based on the authentication information of users authenticated by any authentication system.
For example, User A with role a will see role a information in search results, but User B without role a will not see it when searching.
Using this feature, you can implement searches by department or position for users logged into portals or single sign-on environments.

|Fess| role-based search can obtain role information from the following sources:

-  Request parameters

-  Request headers

-  Cookies

-  |Fess| authentication information

In portals or agent-type single sign-on systems, role information can be obtained by storing authentication information in cookies for the domain and path where |Fess| is running during authentication.
In reverse proxy-type single sign-on systems, role information can be obtained by adding authentication information to request parameters or request headers when accessing |Fess|.

.. note::
    Obtaining role information from request parameters, request headers, and cookies is disabled by default.
    To use these sources, you must configure the key names to reference (``parameterKey``, ``headerKey``, ``cookieKey``), value encryption (``encryptedParameterValue``, etc.), and delimiters (``valueSeparator``, ``roleSeparator``) in the ``roleQueryHelper`` component of ``app/WEB-INF/classes/fess.xml``.
    By default, only role-based search using |Fess| authentication information is enabled.

Role-Based Search Configuration
================================

This section explains how to configure role-based search using |Fess| authentication information.

Configuration in |Fess| Administration Screen
---------------------------------------------

Start |Fess| and log in as an administrator.
Create roles and users.
For example, create Role1 on the role management screen, and create a user belonging to Role1 on the user management screen.
If you want to assign by group, create a group on the group management screen and assign it to users.

Next, in the crawl configuration, enter ``{role}Role1`` in the permission field and save.
To specify by user, use ``{user}username``; to specify by group, use ``{group}groupname``.
When specifying multiple permissions, separate each entry with a newline.

After crawling with this crawl configuration, an index is created that is searchable only by users belonging to the specified roles, users, and groups.
Logged-in users are automatically granted permissions representing themselves (``{user}username``), their roles (``{role}``), and their groups (``{group}``), which are matched against the permissions set on documents.

.. note::
    To explicitly deny access from a specific role, user, or group, prefix the entry with ``(deny)``, for example ``(deny){role}Role1``. Prefixing with ``(allow)`` grants access, which is treated the same as having no prefix.

.. note::
    When integrating with LDAP or single sign-on, the user's role and group information is retrieved from the authentication source and treated as permissions in the same way.
    The behavior during LDAP integration can be controlled by ``ldap.role.search.user.enabled``, ``ldap.role.search.group.enabled``, and ``ldap.role.search.role.enabled`` in ``fess_config.properties`` (all default to ``true``).

Login
-----

Log out from the administration screen.
Log in with a user belonging to Role1.
Upon successful login, you will be redirected to the top of the search screen.

When searching normally, only items whose crawl configuration has the Role1 role set will be displayed.

Also, searches performed without logging in are treated as searches by the guest user.
For documents you want to display to users who are not logged in, set ``{role}guest`` in the permission field of the crawl configuration (the default value is defined by ``role.search.guest.permissions``).

Logout
------

When logged in as a user other than an administrator, select logout on the search screen to log out.
