====================================================================
Building an Elasticsearch-based Search Server with Fess - Role-based Search
====================================================================

Introduction
========

In this article, we will introduce the role-based search feature, which is one of the distinctive features of Fess.

This article uses Fess 15.3.0 for the explanation.
For information on how to build Fess, please refer to the\ `Introduction <https://fess.codelibs.org/ja/articles/article-1.html>`__\.

Target Audience
========

-  Those who want to build a search system in authenticated systems such as portal sites

-  Those who want to build an environment where searches are performed according to access permissions

Required Environment
==========

The content of this article has been tested in the following environment.

-  Ubuntu 22.04

-  OpenJDK 21

Role-based Search
================

Fess's role-based search is a feature that differentiates search results based on authenticated user information.
For example, sales staff member A with the sales department role will see search results containing sales department role information, but technical staff member B without the sales department role will not see it even when searching.
By using this feature, you can implement search by department or position for users logged into portals or single sign-on environments.

By default, Fess's role-based search can differentiate search results based on user information managed by Fess.
It can also be used in conjunction with authentication information from LDAP or Active Directory.
In addition to these authentication systems, role information can be obtained from the following locations:

1. Request parameters

2. Request headers

3. Cookies

4. J2EE authentication information

For usage, in portal servers or agent-type single sign-on systems, authentication information can be passed to Fess by saving the authentication information in cookies for the domain and path where Fess is running during authentication.
Also, in reverse proxy-type single sign-on systems, Fess can obtain role information by adding authentication information to request parameters or request headers when accessing Fess.
By integrating with various authentication systems in this way, search results can be differentiated for each user.

Settings for Using Role-based Search
====================================

It is assumed that Fess 15.3.0 is installed.
If you have not installed it yet, please refer to the\ `Introduction <https://fess.codelibs.org/ja/articles/article-1.html>`__\ and install it.

This time, we will explain role-based search using Fess's user management feature.

Configuration Overview
----------

This time, we will create two roles: sales department (sales) and technical department (eng). User taro will belong to the sales role and be able to get search results from \https://www.n2sm.net/, and user hanako will belong to the eng role and be able to get search results from \https://fess.codelibs.org/.

Creating Roles
------------

First, access the administration screen.
\http://localhost:8080/admin/

From User > Role > New, enter "sales" as the name and create the sales role.
Similarly, create the eng role as well.

Role List
|image0|


Creating Crawler Roles
----------------------

Click User > Role > sales > Create New Crawler Role.
Enter "Sales Department" as the name, leave the value as "sales", and click [Create].
Then, the Sales Department configuration will be added to the Crawler > Role list.

Similarly, register "Technical Department" as the name of the crawler role for the eng role.

Crawler Role List
|image1|


Creating Users
--------------

From User > User > New, create taro and hanako users with the following settings.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - Taro
     - Hanako
   * - Username
     - taro
     - hanako
   * - Password
     - taro
     - hanako
   * - Role
     - sales
     - eng


Verifying Registered Users
------------------

With this configuration, three users - admin, taro, and hanako - can log in to Fess.
Please confirm that you can log in with each user in order.
When you access \http://localhost:8080/admin/ and log in with the admin user, the administration screen will be displayed as usual.
Next, log out the admin user. Click the button in the upper right corner of the administration screen.

Logout Button
|image2|

Enter the username and password to log in as taro or hanako.
If login is successful, the search screen at \http://localhost:8080/ will be displayed.

Adding Crawl Configurations
------------------

Register the crawl targets.
This time, users with the sales department role will be able to search only \https://www.n2sm.net/, and users with the technical department role will be able to search only \https://fess.codelibs.org/.
To register these crawl configurations, click Crawler > Web > New to create web crawl configurations.
This time, we will use the following settings. The rest are defaults.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * -
     - N2SM
     - Fess
   * - Name
     - N2SM
     - Fess
   * - URL
     - \https://www.n2sm.net/
     - \https://fess.codelibs.org/
   * - URLs to Crawl
     - \https://www.n2sm.net/.*
     - \https://fess.codelibs.org/.*
   * - Max Access Count
     - 10
     - 10
   * - Interval
     - 3000 milliseconds
     - 3000 milliseconds
   * - Role
     - Sales Department
     - Technical Department

Starting the Crawl
--------------

After registering the crawl configurations, click [Start Now] from System > Scheduler > Default Crawler. Wait for a while until the crawl is complete.

Search
----

After the crawl is complete, access \http://localhost:8080/ and search for words like "fess" without logging in to confirm that no search results are displayed.
Next, log in as the taro user and search similarly.
Since the taro user has the sales role, only search results from \https://www.n2sm.net/ will be displayed.

Search Screen with sales Role
|image3|

Log out the taro user and log in as the hanako user.
When you search as before, since the hanako user has the eng role, only search results from \https://fess.codelibs.org/ will be displayed.

Search Screen with eng Role
|image4|

Summary
======

We introduced role-based search, which is one of Fess's security features.
While we mainly explained role-based search using J2EE authentication information, the passing of authentication information to Fess is a general implementation that can accommodate various authentication systems.
Since search results can be differentiated by user attributes, it is possible to implement systems that require search based on viewing permissions, such as internal portal sites and shared folders.

References
========

-  `Fess <https://fess.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/3/role-1.png
.. |image1| image:: ../../resources/images/ja/article/3/role-2.png
.. |image2| image:: ../../resources/images/ja/article/3/logout.png
.. |image3| image:: ../../resources/images/ja/article/3/search-by-sales.png
.. |image4| image:: ../../resources/images/ja/article/3/search-by-eng.png
