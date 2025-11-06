==============
Document Boost
==============

Overview
========

This page explains the configuration settings related to document boost.
By configuring document boost settings, you can position documents at the top of search results regardless of search terms.

Management Operations
=====================

Display Method
--------------

To open the document boost configuration list page shown below, click [Crawler > Document Boost] in the left menu.

|image0|

Click the configuration name to edit it.

Creating Configuration
----------------------

To open the document boost configuration page, click the New button.

|image1|

Configuration Items
-------------------

Condition
:::::::::

Specifies the condition for documents to position at the top.
For example, to display URLs containing https://www.n2sm.net/ at the top, write url.matches("https://www.n2sm.net/.*").
Conditions can be written in Groovy.

Boost Value Expression
::::::::::::::::::::::

Specifies the weighting value for documents.
Expressions can be written in Groovy.

Sort Order
::::::::::

Configures the sort order for document boost.

Deleting Configuration
----------------------

Click the configuration name on the list page, then click the Delete button to display a confirmation screen. Click the Delete button to remove the configuration.

.. |image0| image:: ../../../resources/images/ja/15.3/admin/boostdoc-1.png
.. |image1| image:: ../../../resources/images/ja/15.3/admin/boostdoc-2.png
