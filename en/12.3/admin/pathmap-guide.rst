============
Path Mapping
============

Overview
========

Path Mapping replaces crawled url/path with given one.
In search result page, replaced url links are used.

Management Operations
=====================

Display Configurations
----------------------

Select Crawler > Path Mapping in the left menu to display a list page of Path Mapping Configuration, as below.

|image0|

Click a mapping name if you want to edit it.

Create Configuration
--------------------

Click Create New button to display a form page for Path Mapping configuration.

|image1|

Configurations
--------------

Regexp.
:::::::

Target string which is written by a regular expression.

Replacement
:::::::::::

Replaced value.

Process Type
::::::::::::

When this is processed. 
Crawling is at crawling/indexing time and replaced url/path is indexed.
View is at searching time and original url/path is indexed.

Display Order
:::::::::::::

Display order.

Delete Configuration
--------------------

Click a mapping on a list page, and click Delete button to display a confirmation dialog.
Click Delete button to delete the configuration.

.. |image0| image:: ../../../resources/images/en/12.3/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/12.3/admin/pathmap-2.png
