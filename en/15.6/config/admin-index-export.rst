======================
Index Export Feature
======================

Overview
========

The Index Export feature allows you to export search documents indexed in OpenSearch to HTML files on the local filesystem. This functionality is useful for:

- Creating static backups of indexed content
- Generating offline copies of documents for archival purposes
- Building static search result pages
- Content migration to other systems

The exported files maintain the original URL path structure from the source documents, making it easy to navigate and manage the exported content.

How It Works
============

When the Index Export job runs, it performs the following process:

1. **Query Documents**: Retrieves documents from OpenSearch using scroll API for efficient batch processing
2. **Process Content**: Extracts document fields (title, content, URL, etc.)
3. **Create Directory Structure**: Replicates the URL path structure in the export directory
4. **Generate HTML Files**: Creates HTML files containing the document content
5. **Continue Until Complete**: Processes all documents in batches until the index is fully exported

The scroll API ensures efficient handling of large document sets without memory issues.

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
     - ``/var/fess/export``
     - Directory where exported files are stored
   * - ``index.export.exclude.fields``
     - ``cache``
     - Comma-separated list of fields to exclude from export
   * - ``index.export.scroll.size``
     - ``100``
     - Number of documents processed per batch

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
3. Find **Index Export Job** in the job list
4. Click to edit the job settings
5. Set the schedule using a cron expression
6. Save the settings

Example cron expressions:

- ``0 0 2 * * ?`` - Run daily at 2:00 AM
- ``0 0 3 ? * SUN`` - Run every Sunday at 3:00 AM
- ``0 0 0 1 * ?`` - Run on the first day of each month at midnight

Custom Query Filtering
======================

You can customize the export job to export only specific documents by modifying the job script.

To add a custom query filter:

1. Navigate to **System** > **Scheduler**
2. Edit the **Index Export Job**
3. Modify the job script to include a query filter

Example script with date filter:

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "created:>=now-7d"
    job.execute()

Example script with site filter:

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "url:*example.com*"
    job.execute()

Exported File Structure
=======================

Exported files are organized to mirror the original URL structure.

For example, a document with URL ``https://example.com/docs/guide/intro.html`` would be exported to:

::

    /var/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

Each exported HTML file contains:

- Document title
- Main content body
- Metadata (last modified date, content type, etc.)
- Original URL reference

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
    curl -X GET "localhost:9201/fess.YYYYMMDD/_count?pretty"

Export Fails Midway
-------------------

1. Check available disk space
2. Review logs for memory or timeout errors
3. Consider reducing ``scroll.size`` for large documents
4. Check OpenSearch scroll context timeout settings

Files Not Accessible
--------------------

1. Verify file permissions: ``ls -la /var/fess/export``
2. Check directory ownership matches |Fess| process user
3. Confirm SELinux or AppArmor policies allow access

Related Topics
==============

- :doc:`admin-index-backup` - Index backup and restore procedures
- :doc:`admin-logging` - Configuring log settings for troubleshooting
