===========
Web Crawling
===========

Overview
========

The Web Crawling configuration page allows you to configure web crawling settings.

Configuration Management
========================

Display Method
--------------

To open the Web Crawling configuration list page shown below, click [Crawler > Web] in the left menu.

|image0|

Click the configuration name to edit it.

Creating a Configuration
------------------------

Click the "Create New" button to open the Web Crawling configuration page.

|image1|

Configuration Options
---------------------

Name
::::

Configuration name.

URL
::::

The URL where crawling begins.

Included URLs for Crawling
::::::::::::::::::::::::::

URLs matching this regular expression (Java format) will be crawled by the |Fess| crawler.

Excluded URLs for Crawling
::::::::::::::::::::::::::

URLs matching this regular expression (Java format) will not be crawled by the |Fess| crawler.

Included URLs for Indexing
::::::::::::::::::::::::::

URLs matching this regular expression (Java format) will be included in the search index.

Excluded URLs for Indexing
::::::::::::::::::::::::::

URLs matching this regular expression (Java format) will be excluded from the search index.

Configuration Parameters
::::::::::::::::::::::::

Specifies crawl configuration information.

Depth
:::::

Specifies the depth for following links contained in crawled documents.

Max Access Count
::::::::::::::::

The number of indexed URLs.

User Agent
::::::::::

Name of |Fess| crawler.

Number of Threads
:::::::::::::::::

The number of threads to use for crawling with this configuration.

Interval
::::::::

The time interval between URL crawls for each thread.

Boost Value
:::::::::::

The boost value is a weight for documents indexed by this configuration.

Permissions
:::::::::::

Specifies permissions for this configuration.
The permission format is as follows: to display search results to users in the developer group, specify {group}developer.
User-level: {user}username, Role-level: {role}rolename, Group-level: {group}groupname.

Virtual Host
::::::::::::

Specifies the virtual host hostname.
For details, see :doc:`../config/virtual-host`.

Status
::::::

If enabled, the default crawler's scheduled job will include this configuration.

Description
:::::::::::

Enter a description.

Deleting a Configuration
------------------------

Click the configuration name on the list page, then click the "Delete" button to display a confirmation screen. Click the "Delete" button to remove the configuration.

Examples
========

Crawling fess.codelibs.org
--------------------------

To create a Web Crawling configuration to crawl pages under https://fess.codelibs.org/, the configuration values are as follows:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Name
     - Fess
   * - URL
     - https://fess.codelibs.org/
   * - Included URLs for Crawling
     - https://fess.codelibs.org/.*

Other configuration values can use default settings.

Crawling Web Authentication Sites
----------------------------------

Fess supports crawling sites with BASIC, DIGEST, and NTLM authentication.
For details on web authentication, refer to the Web Authentication page.

Redmine
:::::::

To crawl Redmine pages (ex. https://<server>/) with password protection, create a setting on Web Config page as below:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Name
     - Redmine
   * - URL
     - https://<server>/my/page
   * - Included URLs for Crawling
     - https://<server>/.*
   * - Configuration Parameters
     - client.robotsTxtEnabled=false (Optional)

and then create the authentication setting on Web Auth page:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Scheme
     - Form
   * - Username
     - (Account for crawling)
   * - Password
     - (Password for the account)
   * - Parameters
     - | encoding=UTF-8
       | token_method=GET
       | token_url=https://<server>/login
       | token_pattern=name="authenticity_token"[^>]+value="([^"]+)"
       | token_name=authenticity_token
       | login_method=POST
       | login_url=https://<server>/login
       | login_parameters=username=${username}&password=${password}
   * - Web Configuration
     - Redmine

XWiki
:::::

To crawl XWiki pages (ex. https://<server>/xwiki/), Web Crawling setting is:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Name
     - XWiki
   * - URL
     - https://<server>/xwiki/bin/view/Main/
   * - Included URLs for Crawling
     - https://<server>/.*
   * - Configuration Parameters
     - client.robotsTxtEnabled=false (Optional)

and the authentication setting is:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Configuration Item
     - Value
   * - Scheme
     - Form
   * - Username
     - (Account for crawling)
   * - Password
     - (Password for the account)
   * - Parameters
     - | encoding=UTF-8
       | token_method=GET
       | token_url=http://<server>/xwiki/bin/login/XWiki/XWikiLogin
       | token_pattern=name="form_token" +value="([^"]+)"
       | token_name=form_token
       | login_method=POST
       | login_url=http://<server>/xwiki/bin/loginsubmit/XWiki/XWikiLogin
       | login_parameters=j_username=${username}&j_password=${password}
   * - Web Configuration
     - XWiki


.. |image0| image:: ../../../resources/images/en/15.5/admin/webconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/webconfig-2.png
.. pdf            :height: 940 px
