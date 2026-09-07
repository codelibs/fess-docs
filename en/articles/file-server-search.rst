=============================================
Open Source Full-Text Search for File Servers
=============================================

Introduction
============

As departments add file servers, nobody can say where a given document lives any more. Windows search works one shared folder at a time and cannot reach across servers, and a NAS with its own full-text search stops at the edge of that box.

One way out is to run a full-text search server in front of the file servers. This page collects the things worth checking before you put Fess, an open source full-text search server, in that position.

Who this is for
===============

- Anyone struggling to search an internal file server or NAS
- Anyone evaluating full-text search and wondering whether open source can do the job
- Anyone who needs to add search without disturbing existing access permissions

Fess is published under the Apache License 2.0 and carries no licence fee.

Where the files can live
========================

The Fess file crawler speaks the protocols below. You configure them in the admin UI under [Crawler] > [File System], as the crawl start URL.

.. list-table:: Supported protocols
   :header-rows: 1
   :widths: 12 33 55

   * - Protocol
     - URL form
     - Typical use
   * - ``file``
     - ``file:///home/share/documents/``
     - A directory on the machine running Fess, including an already-mounted NAS
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Windows file sharing, from SMB 2.0.2 through SMB 3.1.1
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Older equipment that only speaks SMB1/CIFS
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - FTP servers
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 and S3-compatible object storage
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage

The enabled set is held in ``crawler.file.protocols``, which defaults to ``file,smb,smb1,ftp,s3,gcs``.

For Windows file sharing you normally want ``smb``. ``smb1`` is kept for old NAS boxes and print servers that speak nothing else; SMB1 is disabled by default in Windows for security reasons, so it is not something to choose for a new deployment.

Existing access permissions carry over
======================================

The biggest worry when putting search in front of a file server is that documents somebody should not see will turn up in the results. If the HR and finance folders surface for everyone, the search system is unusable no matter how good the ranking is.

Fess answers this by **carrying the file server's own access permissions into search**.

How it works
------------

1. While crawling, Fess reads each file's ACL
2. The accounts and groups that are allowed or denied are recorded as that document's roles
3. At search time those roles are matched against the roles of the signed-in user, and only permitted documents come back

Both allow and deny are handled, distinguished internally by the ``(allow)`` and ``(deny)`` prefixes. Reading roles out of the ACL is enabled by default.

.. list-table:: Settings that govern permission inheritance
   :header-rows: 1
   :widths: 38 14 48

   * - Setting
     - Default
     - What it does
   * - ``smb.role.from.file``
     - ``true``
     - Takes roles from the ACL of files crawled over SMB
   * - ``file.role.from.file``
     - ``true``
     - Takes roles from local file system permissions
   * - ``ftp.role.from.file``
     - ``true``
     - Takes roles from files crawled over FTP
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Which SID types become roles; tunes how users and groups are treated

The prerequisite to check first
-------------------------------

For this to work end to end, **the person searching has to carry the same roles**. The document records "this group may read me", so unless the searching user can tell Fess which groups they belong to, there is nothing to match against.

That makes **integration with Active Directory or LDAP a prerequisite** for permission-aware search: Fess signs users in against the same directory the file server authenticates them with.

If instead you only ever index shared folders that everyone in the company may read, the integration is not required. That distinction is usually what decides the scope of a first deployment.

Which file formats can be read
==============================

Fess extracts text from file contents using Apache Tika, so the body of a document is searchable, not just its name. That is what lets somebody find a document whose title they cannot recall.

The main formats are:

- MS Office (doc, xls, ppt, docx, xlsx, pptx and so on)
- PDF
- Plain text, HTML, XML
- Rich text (rtf)
- Source code (js, c, h, java and so on)
- Archives (gz, tar, zip and so on; the contents are expanded and indexed too)

The full list is on `Supported file types <https://fess.codelibs.org/supported-files.html>`__.

Files that hold no text at all, such as scanned documents and image-only PDFs, cannot be read this way. Whether OCR is needed is worth settling by looking at what is actually in the target folders before you start.

Sizing and topology
===================

Fess stores its index in OpenSearch. A small deployment runs happily with Fess and OpenSearch on the same machine, and OpenSearch can be split out into a cluster as the corpus grows.

When sizing, the file count alone is a poor guide. These three matter more:

- The total size of the target folders, and what share of it is text-bearing
- How often content changes, daily or monthly, which drives the crawl schedule
- Per-file size, since very large files can be excluded from crawling by configuration

Getting started
===============

1. **Run it first** — follow `Quick Start <https://fess.codelibs.org/quick-start.html>`__. With Docker Compose you have something searchable in a few minutes
2. **Create a crawl configuration** — register the target URL and crawl interval under [Crawler] > [File System]
3. **Add credentials** — register the account used to reach the shared folder under [Crawler] > [File Authentication]
4. **Design roles and labels** — labels for departmental filtering, roles for permission-based results

A worked example is in `Part 4: Unified Search for Scattered Files <https://fess.codelibs.org/articles/guide-04.html>`__, which builds a single search box over several file servers and an intranet site.

Summary
=======

- Fess is an open source search server that can index file servers over SMB/CIFS, FTP, local paths, S3 and GCS
- For files crawled over SMB, the access permissions recorded in the ACL are used to filter results, and this is on by default
- Permission-aware search requires integration with Active Directory or LDAP
- Apache Tika makes the body of Office documents and PDFs searchable
- Start small and grow by moving OpenSearch into a cluster

References
==========

- `Crawler Configuration: Web, File Server and Database Crawling <https://fess.codelibs.org/stable/config/crawler-basic.html>`__
- `Access Control with Roles <https://fess.codelibs.org/stable/config/security-role.html>`__
- `Supported file types <https://fess.codelibs.org/supported-files.html>`__
- `Quick Start <https://fess.codelibs.org/quick-start.html>`__
- `Administration Guide <https://fess.codelibs.org/stable/admin/index.html>`__
