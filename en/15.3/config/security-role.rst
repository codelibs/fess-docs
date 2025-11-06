===========================
Role-Based Search Configuration
===========================

About Role-Based Search
========================

|Fess| can provide different search results based on authentication information of users authenticated by any authentication system.
For example, User A with role a will see role a information in search results, but User B without role a will not see it when searching.
Using this feature, you can implement searches by department or position for users logged into portals or single sign-on environments.

|Fess| role-based search can obtain role information from:

-  Request parameters

-  Request headers

-  Cookies

-  |Fess| authentication information

In portals or agent-type single sign-on systems, role information can be obtained by storing authentication information in cookies for the domain and path where |Fess| is running during authentication.
In reverse proxy-type single sign-on systems, role information can be obtained by adding authentication information to request parameters or request headers when accessing |Fess|.

Role-Based Search Configuration
================================

This section explains how to configure role-based search using |Fess| authentication information.

Configuration in |Fess| Administration Screen
---------------------------------------------

Start |Fess| and log in as administrator.
Create roles and users.
For example, create Role1 on the role management screen, and create a user belonging to Role1 on the user management screen.
Next, in crawl configuration, enter {role}Role1 in the permission field and save.
To specify by user, describe {user}username; to specify by group, describe {group}groupname.
After that, by crawling with this crawl configuration, an index searchable only by the created user is created.

Login
-----

Log out from the administration screen.
Log in with a user belonging to Role1.
Upon successful login, you will be redirected to the search screen top.

When searching normally, only items with Role1 role settings in crawl configuration will be displayed.

Also, searches without login are searches by the guest user.

Logout
------

When logged in as a user other than administrator, select logout on the search screen to log out.
