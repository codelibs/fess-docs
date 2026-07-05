=============================
Thumbnail Image Configuration
=============================

Displaying Thumbnail Images
===========================

In |Fess|, you have the option to display thumbnail images in search results. Thumbnail images are generated based on the MIME type of the search result. If the MIME type is supported, thumbnail images are automatically generated when displaying search results. You can configure the process of generating thumbnail images for different MIME types.

To enable the display of thumbnail images, log in as an administrator, go to the General Settings, and enable the Thumbnail Display option. Don't forget to save your changes.

Thumbnail Images for HTML Files
===============================

Thumbnail images for HTML files utilize images specified within the HTML document or images contained within it. Thumbnail images are determined based on the following criteria, in order:

- The value of the `content` attribute in the meta tag with the `name` attribute set to "thumbnail."
- The value of the `content` attribute in the meta tag with the `property` attribute set to "og:image."
- An `img` tag with an image of an appropriate size for a thumbnail.

Thumbnail Images for MS Office Files
====================================

Thumbnail images for MS Office files are generated using LibreOffice and ImageMagick. Thumbnail generation requires the unoconv and convert commands to be installed.

Package Installation
--------------------

For Redhat-based operating systems, install the following packages to enable image creation:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

Generation Scripts
------------------

When installed via RPM/Deb packages, the script for generating MS Office thumbnails is located at /usr/share/fess/bin/generate-thumbnail.

Thumbnail Images for PDF Files
==============================

Thumbnail images for PDF files are generated using ImageMagick. Thumbnail generation requires the convert command to be installed.

Disabling Thumbnail Jobs
========================

To disable thumbnail jobs, follow these steps:

1. In the admin panel, navigate to System > General, uncheck the "Thumbnail Display" option, and click "Update."
2. Set ``thumbnail.crawler.enabled`` to ``false`` in either ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Restart the Fess service.
