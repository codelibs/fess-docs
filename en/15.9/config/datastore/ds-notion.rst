==================================
Notion Connector
==================================

Overview
========

The Notion Connector provides functionality to retrieve pages and database rows
from Notion and register them in the |Fess| index.
It authenticates as a Notion internal integration and indexes everything that the integration has been shared with.

This feature requires the ``fess-ds-notion`` plugin.

Supported Content
=================

- Pages (the text of their blocks)
- Database rows, together with their property values
- Notion-hosted file and PDF block attachments (each indexed as its own document)
- Unresolved page comments (folded into the page document)

The following are out of scope:

- Files that are only linked from Notion (external files); only Notion-hosted ``file`` and ``pdf`` blocks are downloaded
- Pages and database rows that are in Notion's trash
- Per-page access control (see "Permissions" below)

Prerequisites
=============

1. Plugin installation is required
2. A Notion internal integration must be created
3. The integration must be shared with the pages and databases to crawl

Plugin Installation
-------------------

Install from "System" -> "Plugins" in the admin console, or run ``bin/fess-setup install plugin fess-ds-notion``
and restart |Fess|.
See :doc:`../../admin/plugin-guide` for details.

Notion Integration Setup
------------------------

1. Create an internal integration in Notion and copy its "Internal Integration Secret".
2. On the integration's "Configuration" page, enable the following capabilities:

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - Capability
        - Required
        - Used for
      * - Read content
        - Always
        - Reading pages, blocks, databases and database rows. Without it, every request fails with ``401 unauthorized`` and the crawl aborts immediately
      * - Read comments
        - Only if ``include_comments=true`` (the default)
        - Fetching page comments. If the capability is missing, a warning is logged once and comment crawling is disabled for the rest of that crawl; the crawl itself does not fail
      * - Read user information
        - Optional
        - Resolving user IDs (``created_by``, ``last_edited_by`` and ``people`` properties) to display names. Without it, the user ID is indexed instead of the name

3. Share the integration with every page or database it should crawl in Notion.
   Adding a capability alone does not grant access to any content.

Configuration
=============

Configure in the admin console under "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - Company Notion
   * - Handler Name
     - NotionDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    token=secret_************************************

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``token``
     - Yes
     - The internal integration secret. It is not passed to the script and is not logged
   * - ``root_page_ids``
     - No
     - Comma-separated IDs of the pages to start crawling from. When both this and ``database_ids`` are empty, every page and database shared with the integration is discovered through Notion's search
   * - ``database_ids``
     - No
     - Comma-separated IDs of the databases to start crawling from. Every row of each database is indexed
   * - ``include_comments``
     - No
     - Fetch each page's unresolved comments and add their text to ``notion.content`` and ``notion.comments`` (default: ``true``)
   * - ``include_files``
     - No
     - Download Notion-hosted ``file`` and ``pdf`` block attachments, extract their text and index each as its own document (default: ``true``)
   * - ``max_file_size``
     - No
     - An attachment larger than this many bytes is skipped entirely, not even indexed with empty content (default: ``10485760``)
   * - ``include_pattern``
     - No
     - Regular expression that a document's ``notion.url`` must match to be indexed (see "Crawl Scope")
   * - ``exclude_pattern``
     - No
     - Regular expression that a document's ``notion.url`` must not match (see "Crawl Scope")
   * - ``request_interval``
     - No
     - Milliseconds to wait before each Notion API request, to stay under Notion's rate limit of about 3 requests per second (default: ``350``)
   * - ``max_retry_count``
     - No
     - Maximum number of retries for a request that ends in ``429``, ``5xx`` or ``529``, or in a transport failure such as a timeout (default: ``5``)
   * - ``connection_timeout``
     - No
     - Connection timeout of each API request, in milliseconds (default: ``10000``)
   * - ``read_timeout``
     - No
     - Read timeout of each API request, in milliseconds (default: ``30000``)
   * - ``ignore_error``
     - No
     - When text extraction fails for an attachment that was downloaded, index the attachment with empty content instead of failing the document (default: ``true``). A download failure always fails the document regardless of this setting

.. note::

   For a numeric parameter, a blank or non-numeric value falls back to its default with a warning in the log.
   So does a negative ``request_interval`` or ``max_retry_count`` (``0`` is valid for both), and a ``true``/``false``
   parameter set to anything else.

Script Configuration
--------------------

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time
    created=notion.created_time

Available Fields
~~~~~~~~~~~~~~~~

Every document, whether a page, a database row or an attachment, is exposed to the script under the ``notion`` object.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``notion.type``
     - ``page`` for a page or a database row, ``file`` for an attachment
   * - ``notion.id``
     - The page ID, or the block ID for an attachment
   * - ``notion.title``
     - The page title (the property of type ``title``, whatever its name), or the file name of an attachment
   * - ``notion.content``
     - For a page: the non-title property values (database rows only), the text of its blocks and its comment text, joined together. For an attachment: the extracted text
   * - ``notion.url``
     - The Notion URL of the page. For an attachment, the URL of the containing page with ``#<block ID>`` appended
   * - ``notion.mimetype``
     - ``text/html`` for a page, the detected MIME type for an attachment
   * - ``notion.created_time``
     - Creation time of the page. Not available for an attachment
   * - ``notion.last_edited_time``
     - Last edited time of the page or of the attachment block
   * - ``notion.created_by``
     - Creator of the page: the name if Notion returned one, otherwise the user ID. Not available for an attachment
   * - ``notion.last_edited_by``
     - Last editor, in the same format. Not available for an attachment
   * - ``notion.parent_id``
     - ID of the parent page, database, data source or block. Empty for a page placed directly in the workspace. Not available for an attachment
   * - ``notion.properties``
     - Map of database column name to formatted text, for a database row. Empty for a normal page. Not available for an attachment
   * - ``notion.comments``
     - The comment text of the page, joined together. Empty when ``include_comments=false`` or the page has no comments. Not available for an attachment
   * - ``notion.page_url``
     - URL of the containing page. Attachments only
   * - ``notion.page_title``
     - Title of the containing page. Attachments only
   * - ``notion.size``
     - Size of the attachment in bytes, when Notion reported it. Attachments only

Crawl Scope
===========

- When neither ``root_page_ids`` nor ``database_ids`` is set, the connector uses Notion's search to discover every page and database shared with the integration.
  Notion does not guarantee that search is exhaustive; if some content is missing from the index, set ``root_page_ids`` or ``database_ids`` explicitly.
- From each starting point, every child page and child database reachable from it is crawled too, so a single root page is usually enough to reach a whole section of a workspace.
- ``include_pattern`` and ``exclude_pattern`` decide only whether the document of that page (or attachment) is indexed.
  They never stop the connector from discovering the descendants: the blocks of a page are always walked before the pattern is checked against the page's own URL,
  so the children of an excluded page are still crawled and indexed under their own URLs.
  To exclude a whole subtree, the pattern must match every URL under it, not just its root.
- A page or database row that is in Notion's trash is skipped.

Permissions
===========

The Notion API does not expose the sharing settings of a page, so this connector cannot synchronize per-page access control.
Every document is indexed with only the permissions set in the "Permissions" field of the data store configuration.

.. warning::

   Everything shared with the integration becomes searchable by the roles granted in that field, regardless of who can see it in Notion.
   Share the integration only with the pages and databases that those roles should be able to search.

Error Handling
==============

- The crawl aborts only on HTTP ``401`` (the token cannot authenticate) or on a ``429`` response that names ``public_api_request_blocked`` (Notion's rate limiter is blocking the integration).
  The crawl also aborts if Notion's search fails while neither ``root_page_ids`` nor ``database_ids`` is set, because there is nothing to start from.
- Any other failure is handled per document: a ``404`` or ``403`` for one page, database, comment thread or block, or running out of ``max_retry_count`` on one request, is logged and skipped, and the crawl continues.
- Every per-document failure is recorded under "Crawler" -> "Failure URL" with the URL of that document (the Notion URL of a page, ``<page URL>#<block ID>`` for an attachment).
  The signed download URL of an attachment is never recorded or logged.
- With ``keep_expires_docs=false`` in the parameters, documents of the data store that were not re-indexed in a crawl are deleted at the end of it, and that includes a crawl that aborts.
  By default the documents carry an expiration and stay in the index until it passes.

Usage Examples
==============

Crawl a Specific Page Tree
--------------------------

Parameters:

::

    token=secret_************************************
    root_page_ids=0123456789abcdef0123456789abcdef
    include_comments=false

Script:

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time

Crawl a Database
----------------

Parameters:

::

    token=secret_************************************
    database_ids=fedcba9876543210fedcba9876543210
    include_files=false

Script:

::

    title=notion.title
    content=notion.content
    url=notion.url
    created=notion.created_time
    last_modified=notion.last_edited_time

Crawl Everything Shared With the Integration
--------------------------------------------

Parameters:

::

    token=secret_************************************
    request_interval=500

Troubleshooting
===============

The crawl aborts immediately with ``401``
-----------------------------------------

Check that the token is the "Internal Integration Secret" of the integration and that the "Read content" capability is enabled.

Pages are missing from the index
--------------------------------

1. Verify that the integration has been shared with the page or database
2. If you rely on discovery, set ``root_page_ids`` or ``database_ids`` explicitly, because Notion's search is not guaranteed to be exhaustive
3. Check ``include_pattern`` and ``exclude_pattern``
4. Check "Crawler" -> "Failure URL" for documents that failed individually

Comments are not indexed
------------------------

Enable the "Read comments" capability of the integration. Without it, a warning is logged once and comments are skipped for that crawl.
Only unresolved comments are indexed.

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-slack` - Slack Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../../admin/failureurl-guide` - Failure URL
- :doc:`../../admin/plugin-guide` - Plugin Management Guide
- `Notion API Documentation <https://developers.notion.com/>`_
