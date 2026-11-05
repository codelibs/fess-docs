===========
Failure URL
===========

Overview
========

Failure URL page display URLs/paths which are not correctly crawled.


Management Operations
=====================

Display Failure URL
-------------------

Select System Info > Failure URL in the left menu to display a list page of failure URLs, as below.

|image0|

Clicking a failure URL link displays the details.

Items in the List
-----------------

The list shows the URL, type, MIME type, HTTP status, size (bytes) and last access time.

The MIME type, HTTP status and size are recorded only when the crawler knew them; otherwise they are blank.

- Recorded when: processing failed after the document was fetched (for example text extraction failed or a size limit was exceeded), or the server returned an HTTP status listed in ``crawler.failure.url.status.codes``. When a document is rejected for exceeding a size limit before it is fetched, only the size is recorded.
- Not recorded when: no response was obtained, such as a timeout or a connection error, and for failures of data store crawls.
- The HTTP status is recorded only for ``http`` / ``https`` URLs. It is blank for files, SMB and other protocols.
- For a failure URL recorded before |Fess| 15.10, these items stay blank until the URL fails again.

CSV Download
------------

The [Download CSV] button on the list downloads the failure URLs that match the conditions entered in the search form (URL, error count and type) as a CSV file. The file name is ``failureurl_yyyyMMddHHmmss.csv``.

- The first row holds the column names, in this order: ``url``, ``errorName``, ``errorCount``, ``lastAccessTime``, ``httpStatusCode``, ``mimeType`` and ``contentLength``. The log (stack trace) is not included.
- Every matching row is written, latest last access time first. Paging does not apply and there is no limit on the number of rows.
- ``lastAccessTime`` is in ISO 8601 format in UTC (for example ``2026-01-01T00:00:00.000Z``).
- The character encoding follows "CSV File Encoding" in [System > General]; a UTF-8 file starts with a byte order mark.
- So that a spreadsheet does not run a value as a formula, a value that starts with ``=``, ``+``, ``-``, ``@``, a tab or a carriage return gets a leading ``'``.

Failure URL Details
===================

Failure URL details record exceptions that occurred during crawling.

|image1|

Details Content
---------------

URL
::::

The URL where the exception occurred.

Thread Name
:::::::::::

The thread name that was executing the crawl.
Can be used when checking log files.

Type
::::

The type of exception.

HTTP Status
:::::::::::

The HTTP status of the response for the document. Recorded only for ``http`` / ``https`` URLs, and only when the crawler knew it.

MIME Type
:::::::::

The MIME type of the document. Recorded only when the crawler knew it.

Size (bytes)
::::::::::::

The size of the document. Recorded only when the crawler knew it.

Log
::::

The content of the exception.

Error Count
:::::::::::

The number of times this exception occurred.

Last Access Time
::::::::::::::::

The time when this exception occurred.


.. |image0| image:: ../../../resources/images/en/15.10/admin/failureurl-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/failureurl-2.png
