======================
Thumbnail Configuration
======================

Displaying Thumbnail Images
============================

|Fess| can display thumbnail images in search results.
Thumbnail images are generated based on the MIME Type of search results.
For supported MIME Types, thumbnail images are generated when displaying search results.
Thumbnail generation processes can be configured and added for each MIME Type.

To enable thumbnail image display, log in as an administrator and enable thumbnail display in the General settings.

HTML File Thumbnail Images
===========================

HTML thumbnail images use images specified or included in the HTML.
Thumbnails are searched and displayed in the following order:

- The content value of a meta tag with name attribute "thumbnail"
- The content value of a meta tag with property attribute "og:image"
- An appropriately sized image from an img tag

MS Office File Thumbnail Images
================================

MS Office thumbnail images are generated using LibreOffice and ImageMagick.
If the unoconv and convert commands are installed, thumbnail images will be generated.

Package Installation
--------------------

For Red Hat-based OS, install the following packages for image generation:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

Generation Script
-----------------

When installed via RPM/Deb packages, the MS Office thumbnail generation script is installed at /usr/share/fess/bin/generate-thumbnail.

PDF File Thumbnail Images
==========================

PDF thumbnail images are generated using ImageMagick.
If the convert command is installed, thumbnail images will be generated.

Disabling Thumbnail Job
=======================

To disable the thumbnail job, configure the following:

1. In the administration screen under System > General, uncheck "Display Thumbnails" and click the "Update" button.
2. Set ``thumbnail.crawler.enabled`` to ``false`` in ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Restart the Fess service.
