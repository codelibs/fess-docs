==================================
Backlog Connector
==================================

Overview
========

The Backlog Connector provides functionality to retrieve issues, Wiki pages, Documents and files
from a Backlog space and register them in the |Fess| index.
It authenticates to the space with an API key.
Each indexed document is restricted to the members of its Backlog project (see "Permissions" below).

This feature requires the ``fess-ds-backlog`` plugin.

Supported Content
=================

- Issues (with their comments)
- Wiki pages
- Documents
- Attachments of issues, Wiki pages and Documents
- Shared files of a project

Every crawl is a full crawl. By default, documents that have disappeared from Backlog are not deleted
at the end of the crawl; they are removed when they expire (see "Removed Content and Revoked Access").

Prerequisites
=============

1. Plugin installation is required
2. A dedicated Backlog user and its API key are required
3. The user must be a member of every project to crawl

Plugin Installation
-------------------

Install from "System" -> "Plugins" in the admin console, or run ``bin/fess-setup install plugin fess-ds-backlog``
and restart |Fess|.
See :doc:`../../admin/plugin-guide` for details.

Backlog Setup
-------------

1. Create a dedicated Backlog user for crawling and issue an API key for it ("Personal Settings" -> "API").
   The crawl sees exactly what this user sees.
2. Add the user to every project to crawl. The connector never requests projects the user has not joined,
   even if the user is a space administrator.
3. Give the user a role without restrictions (Administrator or Normal User). With a restricted role,
   Backlog answers HTTP 403 for some features: a "View only" user cannot download issue attachments,
   and only users without restrictions can download shared files.
   On such a 403, the connector logs one warning per project and feature, skips that feature for that project
   (issue attachments, Wiki attachments, Document attachments or shared files) and continues with the rest.
4. If the space requires two-factor authentication for API access, Backlog answers error code 12
   (RequiredMFAError) and the crawl aborts.

The API key is sent only in the ``Backlog-API-Key`` request header. It is not passed to the script,
not written to the log by this connector, and HTTP redirects are not followed, so the key never leaves the space host.

.. warning::

   Do not enable ``FINE`` logging for the ``org.codelibs.curl`` logger. The HTTP client logs request headers at that level
   and masks only ``Authorization``- and ``Cookie``-style headers, so the ``Backlog-API-Key`` header would be written to the log.

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
     - Company Backlog
   * - Handler Name
     - BacklogDataStore
   * - Permissions
     - (leave empty; see "Permissions")
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    api_key=**********************************************
    space_url=https://example.backlog.com

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``api_key``
     - Yes
     - The Backlog API key. It is not passed to the script and is not logged
   * - ``space_url``
     - Yes
     - The URL of the space, for example ``https://example.backlog.com``. Only ``https`` is accepted, and only the scheme and host may be given (a trailing slash is ignored). A missing, malformed or ``http`` value aborts the crawl
   * - ``project_keys``
     - No
     - Comma-separated project keys to crawl (case-insensitive). If empty, every project the user can see is crawled. A key that is not visible to the user is logged as a warning
   * - ``include_archived``
     - No
     - Also crawl archived projects (default: ``false``)
   * - ``include_issues``
     - No
     - Index issues (default: ``true``)
   * - ``include_comments``
     - No
     - Add issue comments to the issue document (default: ``true``)
   * - ``include_wikis``
     - No
     - Index Wiki pages, in projects where the Wiki is enabled (default: ``true``)
   * - ``include_documents``
     - No
     - Index Documents, in projects where Documents are enabled (default: ``true``)
   * - ``include_attachments``
     - No
     - Download and index the attachments of issues, Wiki pages and Documents (default: ``true``)
   * - ``include_shared_files``
     - No
     - Download and index shared files, in projects where file sharing is enabled (default: ``true``)
   * - ``permission_sync``
     - No
     - Give every document of a project one ``{user}`` role per project member (default: ``true``). See "Permissions"
   * - ``default_permissions``
     - No
     - Comma-separated permissions (``{user}name``, ``{group}name`` or ``{role}name``) added to every document
   * - ``max_file_size``
     - No
     - Files larger than this many bytes are skipped and not indexed (default: ``10485760``)
   * - ``include_pattern``
     - No
     - Regular expression that ``backlog.url`` must match to be indexed
   * - ``exclude_pattern``
     - No
     - Regular expression that ``backlog.url`` must not match. When an issue, Wiki page or Document is filtered out, its attachments are skipped too
   * - ``request_interval``
     - No
     - Milliseconds to wait before every API request (default: ``200``)
   * - ``search_request_interval``
     - No
     - Minimum milliseconds between two search-type requests (issue list, Wiki list). Backlog asks clients to keep at least one second between them (default: ``1000``)
   * - ``max_retry_count``
     - No
     - Number of retries for HTTP 429, 5xx and connection failures (default: ``5``)
   * - ``connection_timeout``
     - No
     - Connection timeout in milliseconds (default: ``10000``)
   * - ``read_timeout``
     - No
     - Read timeout in milliseconds (default: ``30000``)
   * - ``ignore_error``
     - No
     - When text extraction of a downloaded file fails, index the file with empty content instead of recording a failure (default: ``true``)

.. note::

   An invalid value (a non-number, a negative interval or retry count, a non-positive timeout or ``max_file_size``,
   or a boolean other than ``true``/``false``) is logged as a warning and the default is used.
   ``0`` is valid for ``request_interval``, ``search_request_interval`` and ``max_retry_count``.

Script Configuration
--------------------

::

    title=backlog.title
    content=backlog.content
    url=backlog.url
    mimetype=backlog.mimetype
    created=backlog.created
    last_modified=backlog.updated
    role=backlog.roles

.. important::

   ``role=backlog.roles`` is required for the restriction to project members to take effect.
   Without it, only the "Permissions" field of the data store configuration reaches the index.

Available Fields
~~~~~~~~~~~~~~~~

Every document is exposed to the script under the ``backlog`` object.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Field
     - Types
     - Description
   * - ``backlog.type``
     - all
     - ``issue``, ``wiki``, ``document``, ``attachment`` or ``file``
   * - ``backlog.id``
     - all
     - The Backlog ID of the issue, Wiki page, Document, attachment or shared file
   * - ``backlog.project_key``, ``backlog.project_name``
     - all
     - The project
   * - ``backlog.title``
     - all
     - ``[KEY-1] summary`` for an issue; the page name, the Document title or the file name otherwise
   * - ``backlog.content``
     - all
     - Issue: description, attributes, custom fields and comments. Wiki page: the page content. Document: plain text. Attachment and file: the extracted text
   * - ``backlog.url``
     - all
     - See "URLs"
   * - ``backlog.mimetype``
     - all
     - ``text/plain`` for issues, Wiki pages and Documents; the detected type for files
   * - ``backlog.created``, ``backlog.updated``
     - all
     - ISO 8601 UTC timestamps, when Backlog returns them
   * - ``backlog.created_by``, ``backlog.updated_by``
     - all
     - User names, when Backlog returns them
   * - ``backlog.roles``
     - all
     - The search roles (see "Permissions")
   * - ``backlog.issue_key``, ``backlog.issue_type``, ``backlog.status``, ``backlog.priority``, ``backlog.assignee``
     - issue
     - Issue attributes (names)
   * - ``backlog.categories``, ``backlog.milestones``, ``backlog.versions``
     - issue
     - Lists of names
   * - ``backlog.custom_fields``
     - issue
     - Map of custom field name to value text
   * - ``backlog.comments``
     - issue
     - Comment text in the form ``author: content``, separated by blank lines
   * - ``backlog.tags``
     - wiki, document
     - List of tag names
   * - ``backlog.parent_type``, ``backlog.parent_url``, ``backlog.parent_title``
     - attachment
     - The issue, Wiki page or Document the attachment belongs to
   * - ``backlog.size``
     - attachment, file
     - Downloaded size in bytes
   * - ``backlog.path``
     - file
     - Path of the shared file, for example ``/docs/spec.pdf``

URLs
----

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Type
     - URL
   * - issue
     - ``{space_url}/view/{ISSUE-KEY}``
   * - wiki
     - ``{space_url}/alias/wiki/{ID}``
   * - document
     - ``{space_url}/document/{PROJECT}/{ID}``
   * - file
     - ``{space_url}/file/{PROJECT}{directory}{name}`` (each path segment is percent-encoded)
   * - attachment
     - ``{parent URL}#attachment-{ID}``

.. note::

   The URL forms of Documents and shared files, and the download endpoint of Document attachments,
   have not been confirmed against a real Backlog space. If a link does not open the expected page,
   the document is still indexed and searchable; only the link target is wrong.

Permissions
===========

With ``permission_sync=true`` (the default), every document of a project gets the following roles:

- one ``{user}`` role for the ``mailAddress`` and one for the ``userId`` of each project member
  (blank values are skipped), so a member can sign in to |Fess| with either
- the ``default_permissions`` value
- the value of the "Permissions" field of the data store configuration

If the project members cannot be retrieved, or none of them has a usable ``mailAddress`` or ``userId``,
the whole project is skipped and recorded under "Crawler" -> "Failure URL". It is never indexed without its member roles.

With ``permission_sync=false``, only ``default_permissions`` and the "Permissions" field apply.

.. warning::

   Clear the "Permissions" field of the data store configuration. The admin console pre-fills it with ``{role}guest``,
   which every user, anonymous searchers included, holds. If it is left in place, it is merged into the roles of every document
   and all Backlog content becomes searchable by everyone.
   With ``permission_sync=true``, the connector logs a warning per project when a guest role ends up among its roles.

Points to know before relying on the member roles:

- A member identifier is a |Fess| login name. A Backlog ``userId`` such as ``tanaka`` grants access to whichever |Fess| login is called ``tanaka``,
  which need not be the same person (for example an LDAP or Active Directory account name). The ``mailAddress`` role does not have this problem.
  Use ``permission_sync`` only where |Fess| login names are Backlog user IDs or mail addresses.
- A member whose identifier would map to the guest role or to another login is ignored, with a warning that names the project and the member ID:
  a ``userId`` of ``guest``, and any identifier containing a backslash (|Fess| drops everything up to a backslash from a user name).
- Every project member can find every indexed item of the project, attachments and shared files included, even where Backlog itself
  would refuse that member the download (a "View only" user cannot download issue attachments). The roles are per project, not per feature.

Removed Content and Revoked Access
==================================

By default, |Fess| gives each document an expiration (the "Delete old documents" setting of the General page, three days by default)
and does not delete documents that have one when a crawl ends. The documents are removed by the Doc Purger once they expire. So, by default:

- content deleted in Backlog stays searchable for up to about three days
- when a member leaves a project, that member keeps access to the project's already indexed documents for up to about three days.
  The next crawl indexes them again under new document IDs (the ID includes the role list), and the old copies, with the old roles,
  stay until they expire. During that time the remaining members see duplicate results

To remove such documents when the crawl ends instead, add ``keep_expires_docs=false`` to the parameters of the data store configuration.
|Fess| then deletes every document of that configuration that the crawl did not re-index, which also applies to everything the crawl did not reach (see "Error Handling").

Usage Examples
==============

Crawl Specific Projects
-----------------------

Parameters:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    project_keys=PROJ,DOCS
    include_shared_files=false

Issues and Wiki Pages Only, Without Attachments
-----------------------------------------------

Parameters:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    include_documents=false
    include_attachments=false
    include_shared_files=false

Remove Documents Deleted in Backlog When the Crawl Ends
-------------------------------------------------------

Parameters:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    keep_expires_docs=false

Error Handling
==============

- The crawl aborts only on HTTP ``401``, Backlog error code 11 (AuthenticationError) or 12 (RequiredMFAError),
  a missing or malformed ``api_key`` or ``space_url``, or a failure to list the projects.
- On HTTP ``429``, the request waits until the time given by the ``X-RateLimit-Reset`` header (at most 120 seconds; 60 seconds when the header is missing) and is retried.
  On HTTP ``5xx`` and connection failures, the request is retried with exponential backoff (1 second, 2 seconds, 4 seconds, up to 60 seconds).
  When ``max_retry_count`` retries are used up, that item fails.
- Any other failure (``403``, ``404``, exhausted retries) is recorded for that one item and the crawl continues.
- A failed item does not fail the crawl job. Check "Crawler" -> "Failure URL" and the crawler log after a crawl.
- With ``keep_expires_docs=false``, content under a failure is not re-indexed and is therefore deleted at the end of that crawl:
  everything under a failed listing, a skipped project or a feature skipped on a 403 disappears from the index until a later crawl completes without that failure.
  The same applies to a crawl that aborts. By default, such content stays searchable until it expires.

Troubleshooting
===============

The Crawl Aborts at Start
-------------------------

1. Check that ``api_key`` is correct and issued for a user of this space
2. Check that ``space_url`` is an ``https`` URL with only the host, such as ``https://example.backlog.com``
3. If the space requires two-factor authentication for API access, the crawl aborts with RequiredMFAError

A Project Is Not Indexed
------------------------

1. Check that the API user is a member of the project
2. With ``permission_sync=true``, a project whose members cannot be retrieved, or none of whom has a usable mail address or user ID, is skipped. See "Crawler" -> "Failure URL"
3. Check ``project_keys`` and ``include_archived``

Attachments or Shared Files Are Missing
---------------------------------------

Give the API user a role without restrictions. The log contains one warning per project and feature that was skipped on HTTP 403.

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-atlassian` - Atlassian Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../../admin/failureurl-guide` - Failure URL
- :doc:`../../admin/plugin-guide` - Plugin Management Guide
- `Backlog API Documentation <https://developer.nulab.com/docs/backlog/>`_
