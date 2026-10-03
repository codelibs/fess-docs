==================================
OCR Configuration
==================================

Overview
========

|Fess| extracts text from documents with Apache Tika.
Tika's Tesseract OCR parser is bundled with |Fess|. When you enable it, |Fess| recognizes text in images and scanned PDFs and makes that text searchable.

OCR runs when both of the following conditions are met:

- The ``tesseract`` command is installed on the host where the |Fess| crawler process runs
- OCR is enabled in |Fess|

OCR is disabled by default.
If ``tesseract`` is not installed, |Fess| skips OCR. No error occurs.

What OCR Applies To
===================

When OCR is enabled, it applies to the following:

- Image files (PNG, JPEG, TIFF, GIF, BMP, etc.)
- Images embedded in documents handled by Tika (such as Office files)
- PDFs whose text layer is empty (scanned PDFs)

Handling of Scanned PDFs
------------------------

|Fess| normally extracts text from PDFs with PDFBox.
When OCR is enabled and PDFBox gets no text at all from a PDF, |Fess| re-extracts the PDF through Tika.
Tika renders the pages as images and runs OCR on them.

.. note::
   PDFs that already contain some text are not OCR'd.
   Mixed PDFs, where only some pages are scanned images, are not covered.

Installing Tesseract
====================

Install Tesseract on the host where |Fess| runs.
To recognize Japanese text, you also need the Japanese trained data (traineddata).

Debian / Ubuntu::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux (enable EPEL first)::

    $ sudo dnf install tesseract tesseract-langpack-jpn

To check the installed languages, run::

    $ tesseract --list-langs

Enabling OCR
============

Set the following properties in ``fess_config.properties``.

- ZIP package: ``app/WEB-INF/classes/fess_config.properties``
- RPM/DEB package: ``/etc/fess/fess_config.properties``

::

    # Enable OCR (default: false)
    crawler.document.ocr.enabled=true

    # Tesseract language(s), joined with + (default: eng)
    crawler.document.ocr.language=jpn+eng

    # Timeout in seconds for one Tesseract run (default: 120)
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Property
     - Default
     - Description
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - Set to ``true`` to enable OCR.
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Tesseract language(s). Join multiple languages with ``+`` (for example, ``jpn+eng``). The matching traineddata must be installed.
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Timeout for one Tesseract run (one image or one PDF page), in seconds.

You can also set these as JVM system properties.
For example, specify them in ``FESS_JAVA_OPTS``. This is handy in Docker environments.

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   Restart |Fess| after changing these settings.

Using OCR with Docker
=====================

To use OCR in a Docker environment, add Tesseract to the |Fess| image.
Build an image with Tesseract by using ``compose/tesseract/Dockerfile`` in `docker-fess <https://github.com/codelibs/docker-fess>`__.

Example ``compose/tesseract/Dockerfile``::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

In ``compose/compose.yaml``, replace the ``image:`` line with ``build: ./tesseract`` and enable the ``FESS_JAVA_OPTS`` line.
This works the same way as ``build: ./playwright``.

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

After the change, rebuild the image and start the containers::

    $ docker compose up -d --build

.. note::
   If you use a non-Alpine base image, such as ``-noble`` or ``-al2023``, add Tesseract with that distribution's package manager instead of ``apk``.

See :doc:`../install/install-docker` for details.

Per-Crawl-Configuration Settings
================================

If you specify ``config.tika.tesseract.config`` in the "Configuration Parameters" of a crawl configuration, you can override the OCR settings for that crawl configuration only.

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties`` is a classpath resource name, not a file system path.
Place the file in the |Fess| configuration directory, which is on the crawler's classpath.

- ZIP package: ``app/WEB-INF/classes/``
- RPM/DEB package: ``/etc/fess/``

In ``tesseract.properties``, write Tika ``TesseractOCRConfig`` properties.
Only simple keys such as ``language`` and ``timeoutSeconds`` are reliably applied.

::

    language=jpn
    timeoutSeconds=300

For that crawl configuration, this takes precedence over the global settings above.

Operational Notes
=================

- OCR is CPU-intensive and slows crawling considerably. Consider reducing the number of crawler threads, or enabling OCR only for the crawl configurations that need it.
- For new web crawl configurations, the default excluded URL pattern excludes image URLs (jpg, png, gif, etc.). To crawl images on a web site, remove these from "Excluded URLs for Crawling". File crawls include images.
- The crawler's size limits also apply. For the indexing size limit per file type (default: 10 MB), see :doc:`crawler-basic`.
- OCR accuracy depends on the quality of the scan. Handwriting is generally not recognized well.
- Files that were indexed before OCR was enabled are not OCR'd as they are. With incremental crawling ("Check Last Modified" in :doc:`../admin/general-guide`) on, a file whose modification time has not changed is not fetched again by a re-crawl. To OCR those files, turn "Check Last Modified" off for one crawl, or delete the documents from the index and crawl again.

Upgrade Notes
=============

Up to 15.8, the bundled ``tika.xml`` excluded ``org.apache.tika.parser.ocr.TesseractOCRParser``.
From 15.9, the bundled ``tika.xml`` no longer excludes this parser.

If you kept a customized ``tika.xml``, remove the following line:

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

If this line remains, OCR stays off even with ``crawler.document.ocr.enabled=true``.

The location of ``tika.xml`` is as follows:

- ZIP package: ``app/WEB-INF/conf/tika.xml``
- RPM/DEB package: ``/etc/fess/tika.xml``

Verifying OCR
=============

1. Create a file crawl configuration for a folder that contains a scanned image (an image with text in it).
2. Run the crawl.
3. Search for a word that appears in the image and confirm that the image appears in the search results.

If the image does not appear, check the following:

- ``tesseract --list-langs`` lists the language you use
- ``crawler.document.ocr.enabled`` is ``true``
- ``tika.xml`` does not still exclude ``TesseractOCRParser``
- ``fess-crawler.log`` of the crawl shows ``OCR is enabled`` (a ``Tesseract OCR is not available`` warning means that |Fess| cannot use Tesseract)
