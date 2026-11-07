=============
Crawling Info
=============

Overview
========

Crawling Info page manages execution logs for crawling information.

Management Operations
=====================

Display Crawling Info
---------------------

Select System Info > Crawling Info in the left menu to display a list page of Crawling Info, as below.

|image0|

Running Crawls
--------------

While crawls are running, "Running Crawls" is shown above the list. It has one row for each web, file system or data store crawl configuration with the following items.

- Crawl Configuration: The name of the crawl configuration.
- Processed Documents: The number of documents the running crawl has processed so far. For web and file system crawls this is the number of access results; for data store crawls it is the number of documents indexed for the crawl configuration.
- Progress: The processed documents as a percentage of the number of documents of the previous completed crawl. It is at most 99% until the crawl completes. When there is no previous completed crawl (for example the first crawl), no percentage can be calculated, so ``-`` is shown and only the count is given.

Notes:

- The block shows the state when the page was opened. Reload the page to see the latest values.
- A crawl that finishes is gone from the block the next time the page is opened. A crawl that is stopped, or that the crawler stops without recording (for example the process is killed), disappears within about 30 seconds (by default) after its last update, so it may still be shown for a short time after it is stopped. A stopped or failed crawl leaves the document count of the previous completed crawl unchanged, and so does a crawl that completes without processing any document.
- The progress state is stored by the system in the ``metadata`` field of the crawl configuration. It cannot be edited in the admin UI or the admin API.
- The same information is available from the admin API (see :doc:`../api/admin/api-admin-crawlinginfo`).

Details
-------

To display details for specific crawling session, click the row of crawling info data.

|image1|

Field List
----------

Session ID
::::::::::

The session ID during crawl execution.

Crawler Start Time
::::::::::::::::::

The time when the entire crawl started.

Crawl Start Time (Web/File)
::::::::::::::::::::::::::::

The time when web and file system crawling started.

Crawl Start Time (Data Store)
::::::::::::::::::::::::::::::

The time when data store crawling started.

Crawl End Time (Web/File)
::::::::::::::::::::::::::

The time when web and file system crawling ended.

Crawl Execution Time (Data Store)
::::::::::::::::::::::::::::::::::

The execution time of data store crawling (in milliseconds).

Indexing Execution Time (Data Store)
:::::::::::::::::::::::::::::::::::::

The time taken to index the results of web and file system crawling (in milliseconds).

Index Size (Data Store)
::::::::::::::::::::::::

The number of indexed documents.

Crawl End Time (Data Store)
::::::::::::::::::::::::::::

The time when data store crawling ended.

Crawler Status
::::::::::::::

Whether the crawl was successful or not.

Crawler End Time
::::::::::::::::

The time when the entire crawl ended.

Crawler Execution Time
::::::::::::::::::::::

The total execution time of the crawl (in milliseconds).

.. |image0| image:: ../../../resources/images/en/15.10/admin/crawlinginfo-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/crawlinginfo-2.png
