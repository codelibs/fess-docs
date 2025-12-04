============
Path Mapping
============

Overview
========

This page explains the configuration settings related to path mapping.
Path mapping can be used to replace links displayed in search results.

Management Operations
=====================

Display Method
--------------

To open the path mapping configuration list page shown below, click [Crawler > Path Mapping] in the left menu.

|image0|

Click the configuration name to edit it.

Creating Configuration
----------------------

To open the path mapping configuration page, click the New button.

|image1|

Configuration Items
-------------------

Regular Expression
::::::::::::::::::

Specifies the string to replace.
Notation follows Java regular expressions.

Replacement
:::::::::::

Specifies the string to replace the matched regular expression.

Process Type
::::::::::::

Specifies the timing of replacement.

* Crawling: Replaces the URL after document retrieval during crawling, before indexing.
* Displaying: Replaces the URL before displaying during search.
* Crawling/Displaying: Replaces the URL during both crawling and displaying.
* Stored URL: Replaces the URL before document retrieval during crawling.

Display Order
:::::::::::::

Specifies the processing order of path mapping.
Processed in ascending order.

Deleting Configuration
----------------------

Click the configuration name on the list page, then click the Delete button to display a confirmation screen.
Click the Delete button to remove the configuration.

.. |image0| image:: ../../../resources/images/en/15.4/admin/pathmap-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/pathmap-2.png