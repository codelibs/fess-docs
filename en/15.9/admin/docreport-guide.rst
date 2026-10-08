===============
Document Report
===============

Overview
========

The Document Report page helps you clean up crawled file servers and the like. It lists documents
with the same content and documents that have not been modified for a long time, and each list can
be downloaded as CSV.

To open the page, select [System Info > Document Report] in the left menu. Viewing requires the
``admin-docreport`` or ``admin-docreport-view`` role. The page only shows and downloads reports; it
does not change any document.

Both tabs can be narrowed with "URL prefix", for example ``smb://server/share/``.

Duplicates
==========

Documents whose content is the same or nearly the same are grouped, largest group first. The groups
use the content signature computed at index time (``content_minhash_bits``, the same one that
collapses duplicate search results), so no reindex is needed. Documents whose content has no words
(such as empty files) are left out.

The screen shows up to ``docreport.duplicate.group.size`` (default: 100) groups and up to
``docreport.duplicate.docs.size`` (default: 10) documents per group. Use [Download CSV] to get every
group. The CSV reads all groups, even on a large index, with the columns
``group, groupSize, url, title, filename, contentLength, lastModified, owner, lastModifier, clickCount, docId``.

.. note::

   The duplicate report needs the content signature, which the index definitions for an OpenSearch without the CodeLibs plugins (``search_engine.type`` of ``vanilla``, ``aws`` or the deprecated ``cloud``) do not compute. With these types the "Duplicates" tab is hidden and only the dormant documents report is available. See :doc:`../config/search-engine-type`.

Dormant Documents
=================

Documents whose last modification is older than the given number of days ("Not modified for
(days)", default 365 from ``docreport.dormant.days``) are listed, oldest first. Documents without a
last modification date are not listed. With "Never opened from search results", documents that have
been clicked from search results are left out.

The screen shows the number of matching documents, their total size and a paged list. Paging stops
at ``indexer.max.result.window.size``; use [Download CSV] to get the documents beyond it.

Settings
========

The following settings in ``fess_config.properties`` adjust the report.

.. list-table::
   :header-rows: 1
   :widths: 40 45 15

   * - Property
     - Description
     - Default
   * - ``docreport.duplicate.group.size``
     - Maximum number of duplicate groups the screen shows
     - ``100``
   * - ``docreport.duplicate.docs.size``
     - Maximum number of documents the screen lists for each group
     - ``10``
   * - ``docreport.duplicate.export.page.size``
     - Number of content signatures read per request when downloading the CSV
     - ``10000``
   * - ``docreport.dormant.days``
     - Default number of days since the last modification after which a document is dormant
     - ``365``
