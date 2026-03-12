===============================
Role-Based Search Configuration
===============================

About Role-Based Search
=======================

In |Fess|, you can filter search results based on user authentication information from any authentication system.
For example, a user, User A, with Role a will see Role a information in search results, while User B without Role a won't see it, even if they perform the same search.
This feature allows you to implement searches based on user affiliations, such as departments or positions, for users logged in through portals or single sign-on environments.

|Fess| allows you to obtain role information for Role-Based Search from the following sources:

- Request Parameters

- Request Headers

- Cookies

- |Fess| Authentication Information

I can acquire roll information by the portal and agent type Single Sign-On system by saving the certification information with a cookie for a domain and the pass which Fess operates at the time of the certification.
In addition, I can acquire roll information by the reverse proxy type Single Sign-On system by adding the certification information to a request parameter and a request header at the time of access to Fess.

Role-Based Search Configuration
===============================

Here, we will explain how to configure Role-Based Search using |Fess| authentication information.

Configuration via the |Fess| Administration Interface
-----------------------------------------------------

Start |Fess| and log in as an administrator.
Create roles and users. For example, create Role1 in the role management interface and create users belonging to Role1 in the user management interface.
Next, in the crawl configuration, write {role}Role1 in the Permission field and save it. You can specify it on a per-user basis using {user}username or on a per-group basis using {group}groupname. By crawling with this configuration, an index that can be searched only by the created users will be created.

Login
-----

Log out from the administration interface.
Log in with a user belonging to Role1.
After a successful login, you will be redirected to the search screen.

When you perform a search as usual, only items configured with Role1 in the crawl settings will be displayed.

Additionally, searching without logging in will be done as a guest user.

Logout
------

If you are logged in with a user other than the administrator, you can log out by selecting "Logout" on the search screen.