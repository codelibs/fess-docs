====================
Index Export Feature
====================

Overview
========

The Index Export feature exports search documents indexed in OpenSearch to HTML or JSON files on the local filesystem. This functionality is useful for:

- Creating static backups of indexed content
- Generating offline copies of documents for archival purposes
- Building static search result pages
- Content migration to other systems

The exported files maintain the original URL path structure from the source documents, making it easy to manage the exported content.

How It Works
============

When the Index Export job runs, it performs the following steps:

1. **Document Retrieval**: Fetches documents from OpenSearch in efficient batches using the Scroll API
2. **Content Processing**: Extracts document fields (title, content, URL, etc.) and removes any excluded fields
3. **Directory Structure Creation**: Replicates the URL path structure in the export directory based on each document's ``url`` field
4. **File Generation**: Creates files (HTML or JSON) containing the document content
5. **Continue Until Complete**: Continues batch processing until the index is fully exported

The Scroll API enables efficient handling of large document sets without memory issues.

.. note::

   Only documents in the search index (``fess.search``) are eligible for export. Documents that do not have a ``url`` field are skipped.

Configuration Properties
========================

Configure the Index Export feature in ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Property
     - Default Value
     - Description
   * - ``index.export.path``
     - ``/var/lib/fess/export``
     - Directory where exported files are stored
   * - ``index.export.exclude.fields``
     - ``cache``
     - Comma-separated list of fields to exclude from export
   * - ``index.export.scroll.size``
     - ``100``
     - Number of documents processed per batch
   * - ``index.export.format``
     - ``html``
     - Export file format (``html`` or ``json``)

Example configuration:

::

    index.export.path=/data/fess/export
    index.export.exclude.fields=cache,boost,role
    index.export.scroll.size=200

Enabling the Job
================

The Index Export job is registered as a scheduled job but is disabled by default.

To enable the job:

1. Log in to the |Fess| administration console
2. Navigate to **System** > **Scheduler**
3. Find **Index Exporter** in the job list
4. Click to edit the job settings
5. Set the schedule using a cron expression
6. Save the settings

Example cron expressions:

- ``0 0 2 * * ?`` - Run daily at 2:00 AM
- ``0 0 3 ? * SUN`` - Run every Sunday at 3:00 AM
- ``0 0 0 1 * ?`` - Run on the first day of each month at midnight

Custom Query Filtering
======================

You can customize the export to target only specific documents by modifying the job script.

The default script for the **Index Exporter** job exports all documents:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.matchAllQuery())
        .execute()

To add a custom query filter:

1. Navigate to **System** > **Scheduler**
2. Edit the **Index Exporter**
3. Modify the job script to include a query filter

Example date filter (export only documents from the last 7 days):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.rangeQuery("created").gte("now-7d"))
        .execute()

Example site filter (export only documents from a specific site):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.wildcardQuery("url", "*example.com*"))
        .execute()

Example to export in JSON format:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .format("json")
        .execute()

Exported File Structure
=======================

Exported files are organized to mirror the original URL structure.

For example, a document with URL ``https://example.com/docs/guide/intro.html`` would be exported to:

::

    /var/lib/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

The file path is determined from the document's ``url`` field according to the following rules:

- The hostname becomes the top-level directory. If the URL contains no hostname, ``_local`` is used.
- If the path ends with a slash or has no path component, an index file (``index.html`` or ``index.json``) is created.
- If the path contains no file extension, an extension matching the format (``.html`` or ``.json``) is appended.
- Characters that are invalid in file names (``< > : " | ? * \``) are replaced with ``_``, and each path component is truncated to a maximum of 200 characters.
- If the URL cannot be parsed or a path traversal is detected, the document is saved under the ``_invalid`` directory using a hash of the URL as the filename.

For HTML format, each file is generated with the following structure:

- ``title`` field → ``<title>`` element
- ``lang`` field → ``lang`` attribute of the ``<html>`` element
- ``content`` field → body of the ``<body>`` element
- All other non-excluded fields → ``<meta name="fess:fieldname" content="value">`` tags inside ``<head>``

::

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Sample Document</title>
    <meta name="fess:url" content="https://example.com/docs/guide/intro.html">
    <meta name="fess:last_modified" content="2024-01-01T00:00:00.000Z">
    <meta name="fess:content_type" content="text/html">
    </head>
    <body>
    Main content body of the document
    </body>
    </html>

For JSON format, each file is a JSON object containing all non-excluded fields:

::

    {
      "url": "https://example.com/docs/guide/intro.html",
      "title": "Sample Document",
      "content": "Main content body of the document",
      "last_modified": "2024-01-01T00:00:00.000Z",
      "content_type": "text/html"
    }

Best Practices
==============

Storage Considerations
----------------------

- Ensure sufficient disk space in the export directory
- Consider using dedicated storage for large document sets
- Implement regular cleanup of old exports if running periodic exports

Performance Tips
----------------

- Adjust ``index.export.scroll.size`` based on document size:
  - Smaller documents: larger batch size (200-500)
  - Larger documents: smaller batch size (50-100)
- Schedule exports during low-usage periods
- Monitor disk I/O during export operations

Security Recommendations
------------------------

- Set appropriate file permissions on the export directory
- Do not expose the export directory directly to the web
- Consider encrypting exported content if it contains sensitive information
- Regularly audit access to exported files

Troubleshooting
===============

Export Job Does Not Run
-----------------------

1. Verify the job is enabled in Scheduler
2. Check the cron expression syntax
3. Review |Fess| logs for error messages:

::

    tail -f /var/log/fess/fess.log | grep IndexExport

Empty Export Directory
----------------------

1. Confirm documents exist in the index
2. Check the export path permissions
3. Verify the query filter (if custom) matches documents

::

    # Check index document count
    curl -X GET "localhost:9201/fess.search/_count?pretty"

Export Fails Midway
-------------------

1. Check available disk space
2. Review logs for memory or timeout errors
3. Consider reducing ``scroll.size`` for large documents
4. Check OpenSearch scroll context timeout settings

Files Not Accessible
--------------------

1. Verify file permissions: ``ls -la /var/lib/fess/export``
2. Check directory ownership matches |Fess| process user
3. Confirm SELinux or AppArmor policies allow access

Related Topics
==============

- :doc:`admin-index-backup` - Index backup and restore procedures
- :doc:`admin-logging` - Configuring log settings for troubleshooting
