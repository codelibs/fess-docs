=====
Label
=====

Overview
========

|Fess| categorize search results with labels.
Label configuration page manages the labels.

Management Operations
=====================

Display Configurations
----------------------

Select Crawler > Label in the left menu to display a list page of Label Configuration, as below.

|image0|

Click a label name if you want to edit it.

Create Configuration
--------------------

Click Create New button to display a form page for Label configuration.

|image1|

Configurations
--------------

Name
::::

Label name. This value is displayed on a search result page.

Value
:::::

Label value. This value is used as URL parameter.

Included Paths
::::::::::::::

Paths which matches crawling url/path are assigned to this label.

Excluded Paths
::::::::::::::

Paths which matches crawling url/path are not assigned to this label.

Permissions
:::::::::::

Permissions for this configuration.
This format is "{user/group/role}name".
For example, to display search results on users who belong to developer group, the permission is {group}developer.

Virtual Host
::::::::::::

Virtual Host key for this configuration.
e.g. fess (if setting Host:fess.codelibs.org=fess in General)

Display Order
:::::::::::::

Display order.

Delete Configuration
--------------------

Click a label name on a list page, and click Delete button to display a confirmation dialog.
Click Delete button to delete the configuration.

.. |image0| image:: ../../../resources/images/en/11.3/admin/labeltype-1.png
.. |image1| image:: ../../../resources/images/en/11.3/admin/labeltype-2.png
