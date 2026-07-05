======================
Thumbnail Configuration
======================

Overview
========

|Fess| can display thumbnail images in search results.
Thumbnail images are generated based on the MIME Type of search results.
For supported MIME Types, thumbnail images are generated when displaying search results.
Thumbnail generation processes can be configured and added for each MIME Type.

To enable thumbnail image display, log in as an administrator and enable thumbnail display in the General settings.

Supported File Formats
======================

Image Files
-----------

.. list-table::
   :widths: 15 40 20
   :header-rows: 1

   * - Format
     - MIME Type
     - Description
   * - JPEG
     - ``image/jpeg``
     - Photos, etc.
   * - PNG
     - ``image/png``
     - Transparent images, etc.
   * - GIF
     - ``image/gif``
     - Including animated GIFs
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - Bitmap images
   * - TIFF
     - ``image/tiff``
     - High-quality images
   * - SVG
     - ``image/svg+xml``
     - Vector images
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - PSD files

Document Files
--------------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - Format
     - MIME Type
     - Description
   * - PDF
     - ``application/pdf``
     - PDF documents
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Word documents
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - Excel spreadsheets
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - PowerPoint presentations
   * - RTF
     - ``application/rtf``
     - Rich text
   * - PostScript
     - ``application/postscript``
     - PostScript files

HTML Content
------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Format
     - MIME Type
     - Description
   * - HTML
     - ``text/html``
     - Generates thumbnails from embedded images in HTML pages

Required External Tools
=======================

Thumbnail generation requires the following external tools. Install them according to the file formats you need to support.

Basic Tools (Required)
----------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Purpose
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - Image conversion & resize
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   Both ImageMagick 6 (``convert`` command) and ImageMagick 7 (``magick`` command) are supported.

SVG Support
-----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Purpose
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - SVG to PNG conversion
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

PDF Support
-----------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Purpose
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - PDF to PNG conversion
     - ``apt install poppler-utils``
     - ``brew install poppler``

MS Office Support
-----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Purpose
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Office to PDF conversion
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - PDF to PNG conversion
     - ``apt install poppler-utils``
     - ``brew install poppler``

For Red Hat-based OS, install the following packages:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

PostScript Support
------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Purpose
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - PS to PDF conversion
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - PDF to PNG conversion
     - ``apt install poppler-utils``
     - ``brew install poppler``

HTML File Thumbnail Images
==========================

HTML thumbnail images use images specified or included in the HTML.
Thumbnails are searched and displayed in the following order:

1. The content value of a meta tag with name attribute "thumbnail"
2. The content value of a meta tag with property attribute "og:image"
3. An appropriately sized image from an img tag

Configuration
=============

Configuration File
------------------

The thumbnail generator is configured in ``fess_thumbnail.xml``.

::

    src/main/resources/fess_thumbnail.xml

Main Configuration Items (fess_config.properties)
-------------------------------------------------

The following items can be configured in ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

::

    # Minimum width for thumbnail images (pixels)
    thumbnail.html.image.min.width=100

    # Minimum height for thumbnail images (pixels)
    thumbnail.html.image.min.height=100

    # Maximum aspect ratio (width:height or height:width)
    thumbnail.html.image.max.aspect.ratio=3.0

    # Generated thumbnail width
    thumbnail.html.image.thumbnail.width=100

    # Generated thumbnail height
    thumbnail.html.image.thumbnail.height=100

    # Output format
    thumbnail.html.image.format=png

    # XPath to extract images from HTML
    thumbnail.html.image.xpath=//IMG

    # Excluded extensions
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # Thumbnail generation interval (milliseconds)
    thumbnail.generator.interval=0

    # Command execution timeout (milliseconds)
    thumbnail.command.timeout=30000

    # Process destroy timeout (milliseconds)
    thumbnail.command.destroy.timeout=5000

generate-thumbnail Script
=========================

Overview
--------

``generate-thumbnail`` is a shell script that performs actual thumbnail generation.
When installed via RPM/Deb packages, it is installed at ``/usr/share/fess/bin/generate-thumbnail``.

Usage
-----

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

Arguments
---------

.. list-table::
   :widths: 15 40 30
   :header-rows: 1

   * - Argument
     - Description
     - Example
   * - ``type``
     - File type
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - Input file URL
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - Output file path
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - MIME type (optional)
     - ``image/gif``

Supported Types
---------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Type
     - Description
     - Tools Used
   * - ``image``
     - Image files
     - ImageMagick (convert/magick)
   * - ``svg``
     - SVG files
     - rsvg-convert
   * - ``pdf``
     - PDF files
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - MS Office files
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - PostScript files
     - ps2pdf + pdftoppm + ImageMagick

Examples
--------

::

    # Generate thumbnail for image file
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # Generate thumbnail for SVG file
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # Generate thumbnail for PDF file
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # GIF file (specify MIME type to enable format hint)
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

Thumbnail Storage Location
==========================

Default Path
------------

::

    ${FESS_VAR_PATH}/thumbnails/

or

::

    /var/lib/fess/thumbnails/

Directory Structure
-------------------

Thumbnails are stored in a hash-based directory structure.

::

    thumbnails/
    ├── _0/
    │   ├── _1/
    │   │   ├── _2/
    │   │   │   └── _3/
    │   │   │       └── abcdef123456.png
    │   │   └── ...
    │   └── ...
    └── ...

Disabling Thumbnail Job
=======================

To disable the thumbnail job, configure the following:

1. In the administration screen under System > General, uncheck "Display Thumbnails" and click the "Update" button.
2. Set ``thumbnail.crawler.enabled`` to ``false`` in ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

::

    thumbnail.crawler.enabled=false

3. Restart the Fess service.

Troubleshooting
===============

Thumbnails Not Being Generated
------------------------------

1. **Check external tools**

::

    # Check ImageMagick
    which convert || which magick

    # Check rsvg-convert (for SVG)
    which rsvg-convert

    # Check pdftoppm (for PDF)
    which pdftoppm

2. **Check logs**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **Run script manually**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

Errors with GIF/TIFF Files
--------------------------

When using ImageMagick 6, specify the MIME type to enable format hints. This is done automatically if Fess is configured correctly.

Error example::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

Solutions:

- Upgrade to ImageMagick 7
- Or verify that MIME type is being passed correctly

SVG Thumbnails Not Being Generated
----------------------------------

1. Check if ``rsvg-convert`` is installed

::

    which rsvg-convert

2. Test conversion manually

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

Permission Errors
-----------------

Check permissions on the thumbnail storage directory.

::

    ls -la /var/lib/fess/thumbnails/

Fix permissions if necessary.

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

Platform Support
================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Platform
     - Support Status
     - Notes
   * - Linux
     - Fully supported
     - \-
   * - macOS
     - Fully supported
     - Install external tools via Homebrew
   * - Windows
     - Not supported
     - Due to bash script dependency
