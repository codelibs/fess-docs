=============================================
Open Source Full-Text Search for File Servers
=============================================

Introduction
============

As each department adds its own file servers, nobody can tell any more where a given document is stored.
Windows search works only within a single shared folder, so it cannot search across several servers.
The full-text search built into a NAS cannot span devices either.

One way to solve this problem is to set up a full-text search server dedicated to your file servers.
This page summarizes the points you should check before adopting Fess, an open source full-text search server, to search file servers.
The content is based on Fess 15.9.

Target Audience
===============

- Those who struggle to search internal file servers and NAS devices
- Those considering full-text search who want to know whether it can be done with open source
- Those who want to introduce search without breaking existing access permissions

Fess is released under the Apache License 2.0 and can be used without license fees.

Where Files Can Be Searched
===========================

File crawling in Fess supports the following protocols.
In the admin console, go to [Crawler] > [File System] and enter the location where crawling starts in "Paths".

.. list-table:: Supported protocols
   :header-rows: 1
   :widths: 12 33 55

   * - Protocol
     - Path format
     - Main use
   * - ``file``
     - ``file:/home/share/documents/``
     - Directories on the server running Fess, including mounted NAS volumes
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Windows file shares and NAS devices that share files over SMB
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Connections that use the legacy SMB1 implementation; a fallback for old devices that ``smb`` cannot connect to
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - FTP servers
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 and S3-compatible object storage (requires the ``fess-storage-s3`` plugin)
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage (requires the ``fess-storage-gcs`` plugin)

The protocols handled by Fess itself are determined by the ``crawler.file.protocols`` setting, whose default in 15.9 is ``file,smb,smb1,ftp``.
In 15.9, ``s3`` and ``gcs`` were moved out of Fess itself into plugins.
Both plugins are bundled in the Docker image, but on Fess installed from the ZIP or RPM/DEB packages, install them from [System] > [Plugin] and restart Fess before using them.

To search Windows file shares, use ``smb``.
Unless you configure otherwise on the Fess side, ``smb`` negotiates the connection version with the server in the range from SMB1 to SMB 3.1.1.
``smb1`` connects through a different implementation (the legacy jcifs) and is not something to choose for a new setup.

Carrying Over Existing Access Permissions
=========================================

When you add search to file servers, the biggest concern is "documents that should not be visible showing up in search results".
If HR or accounting shared folders appear in every employee's search results, the search system itself becomes unusable.

Fess solves this by bringing the file server's access permissions into search.
However, a newly created crawl configuration does not filter results by permissions as is. Be sure to check the mechanism below and the next section, "Removing {role}guest from Permissions".

How It Works
------------

1. During crawling, Fess reads the ACL (access control list) of each file
2. It records the accounts and groups allowed to read the file, and the accounts and groups denied, as "roles" of that document in the ``role`` field
3. The values written in "Permissions" of the crawl configuration are added to the same ``role`` field
4. At search time, Fess matches these against the roles of the logged-in user and returns only the documents the user is authorized to see

In the ``role`` field, users are recorded with ``1`` and groups with ``2`` prefixed to the name (for example, ``1taro`` and ``2sales``).
Deny entries are additionally prefixed with ``D`` (for example, ``D2contractors``).
A value written as ``{role}guest`` in "Permissions" is recorded as ``Rguest``.
The ``(allow)`` and ``(deny)`` you see in the admin console are notations for entering values in "Permissions", not values that get recorded.

Extracting roles from ACLs is enabled by default.

.. list-table:: Settings for carrying over permissions (fess_config.properties)
   :header-rows: 1
   :widths: 38 14 48

   * - Setting
     - Default
     - Description
   * - ``smb.role.from.file``
     - ``true``
     - Gets roles from the ACLs of files crawled with ``smb`` and ``smb1``
   * - ``file.role.from.file``
     - ``true``
     - Gets roles from the access permissions of files crawled with ``file`` (see the notes below)
   * - ``ftp.role.from.file``
     - ``true``
     - Gets roles from the owner and group of files crawled with ``ftp``
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - The SID types adopted as roles, and the type each is recorded as. By default, users (1) and domain groups (2) are recorded as they are, local groups (4) as groups, and built-in SIDs such as Everyone (5) as users

Removing {role}guest from Permissions
-------------------------------------

When you create a new configuration under [Crawler] > [File System], "Permissions" is prefilled with ``{role}guest``.
If you save it as is, every document gets ``Rguest`` alongside the roles taken from its ACL.
Because users who are not logged in are given the ``guest`` role, **files restricted by ACLs are all shown in searches by users who are not logged in**.

To make ACL-based filtering take effect, delete ``{role}guest`` from "Permissions" in the crawl configuration and save it.
Documents that have already been crawled are registered again with the new permissions on the next crawl.

Logged-in users are not given the ``guest`` role.
So even if ``{role}guest`` remains, logged-in users get results that follow the ACLs.
As shown in "Verifying the Behavior", always check while not logged in as well.

Matching the Names on the Login Side
------------------------------------

For this mechanism to work end to end, the users who search must also have the same roles.
The document side records "members of this group can read it", so the match cannot be made unless the searching user can tell Fess which groups they belong to.

For this reason, permission-aware search requires integration with Active Directory or LDAP.
The setup uses the same directory for logging in to Fess that the file servers use for authentication.
LDAP is configured under [System] > [General].
The procedure and how to think about roles are explained in :doc:`guide-05`.

Because matching is done on name strings, keep the following in mind.

- Names taken from ACLs are recorded as account names without the domain name (``EXAMPLE\taro`` becomes ``1taro``)
- For users who log in through LDAP, group names are taken by default from the CN in ``memberOf``. If a group's account name on the file server differs from its CN, they do not match
- Built-in groups such as Everyone are recorded as roles with those names. Users who log in through LDAP usually do not have those roles, so folders shared only with built-in groups may be shown to nobody. If needed, split the crawl configuration and supply the roles in "Permissions"

Conversely, if you only target shared folders that all employees may see equally, this integration is not required.
This is the dividing line when deciding the scope of your deployment.

Notes for Each Protocol
-----------------------

``smb`` / ``smb1``
   The crawl account needs permission to read not only the file contents but also the file's access permissions (security information).
   Files whose access permissions cannot be read are not indexed, and are recorded in [System Info] > [Failure URL].

``file``
   If the file system does not provide ACLs (as with typical Linux file systems), only two roles are recorded: the owning user and group.
   Read access granted to "others" does not become a role.
   If you mount a NAS on the Fess server and crawl it with ``file``, the owner visible at the mount point is recorded, not the ACLs on the NAS.
   For file servers where you want ACL-based filtering, crawl them directly with ``smb`` instead of mounting them.

``ftp``
   The owner and group returned by the FTP server are recorded as roles.

Which File Formats Can Be Read
==============================

Fess uses Apache Tika to extract text from the contents of files.
Because the body text is searchable, not just the file name, you can find "documents whose title you cannot remember".

The main supported formats are as follows.

- MS Office (doc, xls, ppt, docx, xlsx, pptx, etc.)
- PDF
- Text, HTML, XML
- Rich Text (rtf)
- Source code (js, c, h, java, etc.)
- Archives (gz, tar, zip, etc.)

For the complete list, see `Supported File Formats <https://fess.codelibs.org/supported-files.html>`__.

Files that contain no text, such as image PDFs and scanned documents, cannot have their body text searched as they are.
In Fess 15.9 you can enable OCR with Tesseract, which reads text from image files, images embedded in Office documents, and PDFs that contain no text.
OCR is disabled by default.
Install ``tesseract`` on the host where the crawler runs and set ``crawler.document.ocr.enabled=true``.
PDFs in which only some pages are scanned images are not covered.
For the procedure, see `OCR Configuration <https://fess.codelibs.org/stable/config/crawler-ocr.html>`__.
Because OCR lengthens crawl time, we recommend first checking how many scanned documents the target folders contain.

Architecture and Scale
======================

Fess uses OpenSearch to store the search index.
At a small scale, Fess and OpenSearch can run together on the same server, and as the number of target files grows you can separate OpenSearch into a cluster.

When estimating the scale, checking the following in addition to the number of files makes the estimate more accurate.

- The total size of the target folders, and the proportion of files that contain text
- The update frequency (daily, or a few times a month). This affects how you design the crawl interval
- The size per file

By default there is an upper limit on the size of files that can be indexed.
The defaults in ``app/WEB-INF/classes/crawler/contentlength.xml`` are 2.5 MB for HTML and 10 MB for everything else; files that exceed them are not indexed and are recorded in [Failure URL].
Separately, writing something like ``client.maxContentLength=10485760`` in "Config Parameters" of the crawl configuration limits the size of the files that are fetched in the first place (no limit by default).
For folders with many large documents, decide before deployment whether to revise these limits.
For how to configure them, see the section on file size settings in `Crawler Configuration <https://fess.codelibs.org/stable/config/crawler-basic.html>`__.

The crawl interval also needs attention.
Fess deletes documents from the index that have not been updated by a crawl for a certain number of days.
This number of days is "Delete old documents" under [System] > [General], and defaults to 3 days.
The default job "Default Crawler" runs every day, so this is not a problem, but if you reduce it to, say, once a week, make this number of days longer than the run interval.

What to Look for in a File Server Search Tool
=============================================

When comparing search tools for file servers, it is easier to choose if you check whether they meet the following points before comparing product names.

.. list-table:: Items to check when choosing a search tool
   :header-rows: 1
   :widths: 30 70

   * - Item
     - In Fess
   * - Can it search across multiple servers and NAS devices?
     - By registering multiple crawl configurations, you can search across them from a single search box
   * - Can it search the body text of files?
     - Apache Tika extracts the body text of Office documents and PDFs and makes it searchable. Scanned documents become searchable when OCR is enabled
   * - Can it carry over existing access permissions?
     - It gets roles from the ACLs of files crawled over SMB and filters search results accordingly. Integration with Active Directory or LDAP and a review of "Permissions" in the crawl configuration are required
   * - Does it incur license fees?
     - It is released under the Apache License 2.0 and incurs no license fees
   * - Can you try it locally?
     - You can start it with Docker Compose and try searching on your own machine

Deployment Steps
================

1. **Get it running** — Start Fess following the `Quick Start Guide <https://fess.codelibs.org/quick-start.html>`__ or :doc:`guide-02`
2. **Create a crawl configuration** — Under [Crawler] > [File System], register a name and paths. If you filter by ACLs, delete ``{role}guest`` from "Permissions" before saving
3. **Set up credentials** — Register the account used to access the shared folders under [Crawler] > [File Authentication], and select the configuration from step 2 in "File Crawl Config"
4. **Check the crawl account's permissions** — On the file server side, confirm that the account can read both the contents and the access permissions of the target folders
5. **Integrate login** — Configure LDAP (Active Directory) under [System] > [General]
6. **Run a crawl and check the results** — Under [System] > [Scheduler], open "Default Crawler", click [Start Now], and check the results as described in "Verifying the Behavior" below

If you need to narrow results by department, also set up labels under [Crawler] > [Label].

The concrete steps for searching multiple file servers and internal websites from a single search box are covered in :doc:`guide-04`, and designing result filtering with roles and groups is covered in :doc:`guide-05`.

Verifying the Behavior
======================

After the crawl finishes, check the following in order.
The built-in ``admin`` user also has the ``guest`` role, so do not use it to check filtering.

1. Open [System Info] > [Failure URL] and check that no files failed to be indexed because of access errors or size limits
2. Under [System Info] > [Search], search for a file in a restricted folder. This screen does not filter by role, so all documents are shown
3. Click [Update] on the result to open the edit screen and check the ``role`` field. Confirm that it contains values from the ACL such as ``1taro`` or ``2sales``, and that it does not contain ``Rguest``
4. While logged out, search for the same file on the search page and confirm that it is not shown
5. Log in as a user in a group that can read the folder, search, and confirm that it is shown
6. Log in as a user not in that group, search, and confirm that it is not shown

If the names in the ``role`` field in step 3 differ from the names on the LDAP side, review each item in "Matching the Names on the Login Side".

Summary
=======

- Fess is an open source search server that can make file servers (SMB, FTP, local) searchable in full text. S3 and GCS are supported through plugins
- For files crawled over SMB, the access permissions recorded in the ACLs are used to filter search results. Reading ACLs is enabled by default
- Unless you remove ``{role}guest`` from "Permissions" in the crawl configuration, users who are not logged in see all documents
- Permission-aware search requires integration with Active Directory or LDAP, and matching names on both sides
- Apache Tika makes the body text of Office documents and PDFs searchable, and enabling OCR makes scanned documents searchable too
- You can start small and expand by clustering OpenSearch as the number of targets grows

Further Reading
===============

- Steps for searching multiple file servers and internal websites together: :doc:`guide-04`
- Designing result filtering with roles and groups: :doc:`guide-05`
- Trying Fess locally with Docker: :doc:`guide-02`

References
==========

- `File Crawling (File Server Search) <https://fess.codelibs.org/stable/admin/fileconfig-guide.html>`__
- `File Authentication <https://fess.codelibs.org/stable/admin/fileauth-guide.html>`__
- `Crawler Configuration: Web, File Server, and Database Crawling <https://fess.codelibs.org/stable/config/crawler-basic.html>`__
- `OCR Configuration <https://fess.codelibs.org/stable/config/crawler-ocr.html>`__
- `Role-Based Search Configuration <https://fess.codelibs.org/stable/config/security-role.html>`__
- `LDAP Integration Guide <https://fess.codelibs.org/stable/config/ldap-integration.html>`__
- `Failure URL <https://fess.codelibs.org/stable/admin/failureurl-guide.html>`__
- `Supported File Formats <https://fess.codelibs.org/supported-files.html>`__
- `Quick Start Guide <https://fess.codelibs.org/quick-start.html>`__
