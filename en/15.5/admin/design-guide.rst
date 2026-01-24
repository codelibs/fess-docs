===========
Page Design
===========

Overview
========

This section describes the configuration settings for the design of the search interface.

Configuration
=============

Display Method
--------------

To open the page design configuration list page shown below, click [System > Page Design] in the left menu.

|image0|


File Manager
------------

You can download or delete files available on the search screen.

Page File Display
-----------------

You can edit JSP files for the search screen.
Click the edit button for the target JSP file to edit that file.
Clicking the "Use Default" button allows you to edit the JSP file as it was at installation.
Save your changes by clicking the "Update" button on the edit screen to apply them.

Below is a description of the editable pages.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - /index.jsp
     - JSP file for the search top page. This JSP file includes JSP files for each section.
   * - /header.jsp
     - JSP file for the header.
   * - /footer.jsp
     - JSP file for the footer.
   * - /search.jsp
     - JSP file for the search results list page. This JSP file includes JSP files for each section.
   * - /searchResults.jsp
     - JSP file representing the search results section of the search results list page. This JSP file is used when there are search results. Modify this to customize the presentation of search results.
   * - /searchNoResult.jsp
     - JSP file representing the search results section of the search results list page. This JSP file is used when there are no search results.
   * - /searchOptions.jsp
     - JSP file for the search options screen.
   * - /advance.jsp
     - JSP file for the advanced search screen.
   * - /help.jsp
     - JSP file for the help page.
   * - /error/error.jsp
     - JSP file for the search error page. Modify this to customize the presentation of search errors.
   * - /error/notFound.jsp
     - JSP file for the error page displayed when a page is not found.
   * - /error/system.jsp
     - JSP file for the error page displayed for system errors.
   * - /error/redirect.jsp
     - JSP file for the error page displayed when an HTTP redirect occurs.
   * - /error/badRequest.jsp
     - JSP file for the error page displayed when a bad request occurs.
   * - /cache.hbs
     - File for displaying cached search results.
   * - /login/index.jsp
     - JSP file for the login screen.
   * - /profile/index.jsp
     - JSP for the user password change screen.
   * - /profile/newpassword.jsp
     - JSP for the administrator password update screen. Prompts for password change if the username and password are the same string at login.


Table: Editable JSP Files

|image1|

Upload Files
------------

You can upload files to use on the search screen.
Supported file types include jpg, gif, png, css, and js.

File Upload
:::::::::::

Specify the file to upload.

Filename (Optional)
:::::::::::::::::::

Use this to specify a filename for the uploaded file.
If omitted, the uploaded filename is used.
For example, specifying logo.png will change the image on the search top page.


.. |image0| image:: ../../../resources/images/en/15.5/admin/design-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/design-2.png
