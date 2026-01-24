==============
Request Header
==============

Overview
========

Here, we will explain the configuration for request headers. Request headers contain additional information that is added to the requests when crawling and retrieving documents. They can be used, for example, to automatically log in a user based on specific header values, such as in an authentication system.

Management Operations
=====================

Display Configurations
----------------------

To access the list page for configuring request headers shown below, click on "[Crawler > Request Header]" in the left menu.

|image0|

To edit, click on the configuration name.

Create Configuration
--------------------

To open the Request Headers settings page, click on the "Create New" button.

|image1|

Configurations
--------------

Name
::::

Specify the name of the request header to be included in the requests.

Value
:::::

Specify the value of the request header to be included in the requests.

Web Config
::::::::::

Select the web crawl configuration to which the request headers will be applied.
Only the selected crawl configuration will have the request headers added.

Delete Configuration
--------------------

Click on the configuration name on the list page, and when the delete button is clicked, a confirmation screen will appear. Clicking the delete button will remove the configuration.

.. |image0| image:: ../../../resources/images/en/15.5/admin/reqheader-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/reqheader-2.png