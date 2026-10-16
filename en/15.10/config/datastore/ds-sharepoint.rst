===========================
SharePoint Server Connector
===========================

Overview
========

The SharePoint Server Connector retrieves document library files and list items from an
on-premises **SharePoint Server** deployment (2013, 2016, 2019, or Subscription Edition) over its
REST/OData API (and, for 2013, its XML/Atom API), and registers them in the |Fess| index.

This feature requires the ``fess-ds-sharepoint`` plugin.

.. note::

   If you need to crawl SharePoint Online (Microsoft 365) instead, use
   :doc:`ds-microsoft365`, not this connector. This connector's OAuth support targets Azure ACS
   application-only authentication only, and it has no Microsoft Graph API integration.

Supported versions: SharePoint Server 2013 / 2016 / 2019 / Subscription Edition (SE)

Supported Content
=================

- Document library files
- List items
- List item attachments

Prerequisites
=============

1. Plugin installation is required
2. The crawl account needs read access to the sites, lists, and document libraries being crawled
3. Choose exactly one authentication method - NTLM, Kerberos (SPNEGO), or OAuth (ACS) - and have
   its credentials ready

Installing the Plugin
---------------------

Install it from the admin console under "System" -> "Plugin":

1. Download ``fess-ds-sharepoint-X.X.X.jar``
2. Place it under ``$FESS_HOME/app/WEB-INF/lib`` (or ``/usr/share/fess/app/WEB-INF/lib``)
3. Restart |Fess|

See :doc:`../../admin/plugin-guide` for details.

Configuration
=============

Configure this connector in the admin console under "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - SharePoint
   * - Handler Name
     - SharePointDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Parameter List
~~~~~~~~~~~~~~

**URL / Site**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``url``
     - Yes
     - SharePoint server base URL, e.g. ``http://sharepoint.example.com/``
   * - ``site.name``
     - Conditional
     - Site collection name crawled under ``/sites/<site.name>/``. Not needed if ``site.path`` is set
   * - ``site.path``
     - No
     - Server-relative managed path of the site (e.g. ``/teams/eng``; use ``/`` for the root site
       collection). When set, it is used verbatim instead of the hardcoded ``/sites/`` prefix, and
       ``site.name`` is no longer required
   * - ``site.list_id``
     - No
     - Crawl a single list by GUID (List Crawl mode)
   * - ``site.list_name``
     - No
     - Crawl a single list by display name (List Crawl mode)
   * - ``site.doclib_path``
     - No
     - Document-library path under the site (Document Library Crawl mode), e.g. ``/Shared Documents``
   * - ``site.exclude_list``
     - No
     - Comma-separated regex patterns of list entity-type names to exclude. Only applies to a
       whole-site crawl
   * - ``site.exclude_folder``
     - No
     - Comma-separated regex patterns of top-level folder titles to exclude. Only applies to a
       whole-site crawl
   * - ``site.crawl_subsites``
     - No
     - Recurse into the site's subsites (default: ``false``). See `Subsites and Managed Paths`_
   * - ``site.max_depth``
     - No
     - How many subsite hops ``site.crawl_subsites`` may recurse (default: ``10``); the root is depth 0

**Authentication**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``auth.ntlm.user``
     - No
     - NTLM username. Setting it enables NTLM (``DOMAIN\user`` works)
   * - ``auth.ntlm.password``
     - No
     - NTLM password
   * - ``auth.ntlm.domain``
     - No
     - Windows domain, sent as its own NTLM field
   * - ``auth.ntlm.workstation``
     - No
     - Workstation name sent in the NTLM negotiation
   * - ``auth.kerberos.principal``
     - No
     - Client principal, written as ``user@REALM``. Setting it enables Kerberos/SPNEGO
   * - ``auth.kerberos.keytab``
     - No
     - Path to a keytab holding a key for the principal. Mutually exclusive with
       ``auth.kerberos.password``
   * - ``auth.kerberos.password``
     - No
     - The principal's password, used only when no keytab is set
   * - ``auth.kerberos.strip_port``
     - No
     - Strip the port from the service principal name (default: ``true``)
   * - ``auth.kerberos.use_canonical_hostname``
     - No
     - Resolve the target host to its canonical name before building the service principal name
       (default: ``false``)
   * - ``auth.kerberos.krb5_conf``
     - No
     - Path to a ``krb5.conf``. Applied only when ``java.security.krb5.conf`` is not already set
   * - ``auth.kerberos.debug``
     - No
     - Enable ``Krb5LoginModule`` debug output (default: ``false``)
   * - ``auth.oauth.client_id``
     - No
     - Azure ACS application-only OAuth client ID. Setting it enables OAuth
   * - ``auth.oauth.client_secret``
     - No
     - OAuth client secret
   * - ``auth.oauth.tenant``
     - No
     - Tenant name, without ``.sharepoint.com``
   * - ``auth.oauth.realm``
     - No
     - Azure AD realm/directory ID

**Exactly one** of ``auth.kerberos.principal``, ``auth.ntlm.user``, and ``auth.oauth.client_id``
may be set. See `Authentication`_ below.

**List**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``list.items.number_per_page``
     - No
     - Page size for ``GetListItems`` (default: ``100``)
   * - ``list.item.content.include_fields``
     - No
     - Comma-separated field names; if set, only these list-item fields are concatenated into
       ``content``
   * - ``list.item.content.exclude_fields``
     - No
     - Comma-separated field-name patterns (each treated as a regex), excluded from ``content`` in
       addition to a large built-in set of standard fields
   * - ``list.is_sub_page``
     - No
     - Treat list items as SitePages/wiki subpages, affecting paging fallback and the web-link shape
       (default: ``false``)

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``http.connection_timeout``
     - No
     - HTTP connect timeout in ms; also used as the connection-pool wait timeout (default: ``30000``)
   * - ``http.socket_timeout``
     - No
     - HTTP socket (read) timeout in ms (default: ``30000``)
   * - ``proxy_host``
     - No
     - HTTP proxy host
   * - ``proxy_port``
     - Conditional
     - HTTP proxy port; required if ``proxy_host`` is set (default: ``-1`` = no proxy)

**Filtering & Content**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``include_pattern``
     - No
     - Regex an item's value must match to be crawled. See the note under this table for what
       value that is
   * - ``exclude_pattern``
     - No
     - Regex that excludes a matching item from being crawled
   * - ``supported_mimetypes``
     - No
     - Comma-separated regexes a file's MIME type must match at least one of (default: ``.*``)
   * - ``max_content_length``
     - No
     - Maximum file size in bytes; an over-limit file is skipped, not failed (default: ``-1`` = no
       limit)
   * - ``extractor_name``
     - No
     - Fallback extractor used only for a MIME type the extractor factory does not map
       (default: ``tikaExtractor``)

**Behaviour**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``sp.version``
     - No
     - Set to ``2013`` to switch to the XML/Atom, ``GetXxxByServerRelativeUrl`` API family for
       SharePoint 2013 (unset ⇒ SharePoint Online / 2016+ REST dialect)
   * - ``retry_limit``
     - No
     - Max retries per crawl unit on a SharePoint server/client exception (default: ``2``)
   * - ``role.skip``
     - No
     - Skip fetching per-item permissions entirely (default: ``false``). See `Permissions`_
   * - ``ignore_error``
     - No
     - Log and skip a file's content-extraction failure instead of failing the crawl target
       (default: ``false``)
   * - ``default_permissions``
     - No
     - Comma-separated permission strings merged into every document's role list in addition to
       whatever SharePoint returned
   * - ``delete_old_docs``
     - No
     - Whether documents not refreshed this run are deleted (core default: ``true``). This plugin
       forces it to ``false`` for the current run whenever any crawl target failed
   * - ``number_of_threads``
     - No
     - How many crawl targets are worked on at once (default: ``1`` = no thread pool), capped at
       twice the processor count. See `Parallel Crawling and Load`_
   * - ``script_type``
     - No
     - Script engine for the data-config Script (default: ``groovy``)
   * - ``readInterval``
     - No
     - Sleep between successive crawl results, in ms (default: ``0``). Note the camelCase spelling,
       unlike every other parameter here

Script Configuration
--------------------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Available Fields
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - Key
     - List item (ItemCrawl)
     - Doclib file (FolderCrawl->FileCrawl)
     - Attachment (ItemAttachmentsCrawl->FileCrawl)
   * - ``url``
     - Web link
     - File URL
     - File URL
   * - ``host``
     - Hostname
     - Hostname
     - Hostname
   * - ``site``
     - Server-relative path (``FileRef``)
     - Server-relative path
     - Server-relative path
   * - ``title``
     - ``Title`` field, else ``FileLeafRef``/filename
     - The doclib file's own ``Title`` list value if present, else filename
     - Filename
   * - ``titleWithListName``
     - ``"[listName] title"``
     - ``"[listName] filename"`` (list name is always empty for a doclib crawl, so effectively just
       the filename)
     - ``"[listName] filename"``
   * - ``listName``
     - List display name, or ``""``
     - Always ``""``
     - Actual list name
   * - ``content``
     - Concatenation of field values
     - Extracted text
     - Extracted text
   * - ``digest``
     - Abbreviated ``content``
     - Abbreviated ``content``
     - Abbreviated ``content``
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - From the listing
     - From the listing
     - From the listing
   * - ``created``
     - From the listing
     - From the listing
     - From the listing
   * - ``mimetype``
     - Always ``text/html``
     - Detected
     - Detected
   * - ``filetype``
     - Derived from ``mimetype``
     - Derived from ``mimetype``
     - Derived from ``mimetype``
   * - ``role``
     - Permission list, only if non-empty
     - Permission list, only if non-empty
     - Permission list, only if non-empty
   * - ``list_name``
     - Present
     - **Absent**
     - Present
   * - ``list_id``
     - Present
     - **Absent**
     - Present
   * - ``item_id``
     - Present
     - **Absent**
     - Present

.. note::

   ``content_length`` is ``content.length()`` - the character count (UTF-16 code units) of the
   extracted or concatenated text, not the file's byte size. This differs from ``file.size`` in
   the Box, Google Drive, and Dropbox connectors, which is the actual byte size from each
   service's own file metadata. Do not compare this connector's ``content_length`` against those.

**Dynamic keys: ``val_*``**

Every key of a list item's ``FieldValuesAsText`` (the raw field-value map SharePoint returns for
that item, including OData metadata keys such as ``odata.metadata``) is exposed under two names:
once unprefixed (only if that name is not already one of the fixed keys above), and once with a
``val_`` prefix, unconditionally - e.g. a ``Status`` field becomes both ``Status`` and
``val_Status``.

``val_*`` keys exist only on the **list-item crawl path (ItemCrawl)**. A document-library file
(FolderCrawl->FileCrawl) or a list-item attachment (ItemAttachmentsCrawl->FileCrawl) never
produces any ``val_*`` key.

Authentication
==============

Three authentication methods are available, and **exactly one may be configured**. Setting more
than one of ``auth.kerberos.principal``, ``auth.ntlm.user``, and ``auth.oauth.client_id`` fails
the data config job with a validation error before any request is made. This is deliberate: only
one credential is registered with the HTTP client, and the scope it is registered under matches a
``Negotiate`` challenge as readily as an ``NTLM`` one, so configuring more than one would otherwise
produce 401s that nothing in the log explains.

NTLM
----

::

    auth.ntlm.user={SharePoint username}
    auth.ntlm.password={Password}
    auth.ntlm.domain={Windows domain. Optional; unset by default.}
    auth.ntlm.workstation={Workstation name sent in the NTLM negotiation. Optional; unset by default.}

``auth.ntlm.domain`` and ``auth.ntlm.workstation`` both default to unset, which builds exactly the
credential this connector has always built. Writing the domain into the username as
``DOMAIN\user`` keeps working. Setting ``auth.ntlm.domain`` sends the domain as its own NTLM field
instead, which is what a server that rejects the combined form wants.

Kerberos (SPNEGO)
-----------------

**Supported envelope:** a single crawler JVM, one ``krb5.conf`` per Fess instance, a keytab or a
password, no delegation, no channel binding, and mutually exclusive with NTLM and OAuth. Anything
outside that is not supported.

::

    auth.kerberos.principal={Client principal, written as user@REALM. Setting it enables Kerberos.}
    auth.kerberos.keytab={Path to a keytab holding a key for the principal. Mutually exclusive with auth.kerberos.password.}
    auth.kerberos.password={The principal's password. Used only when no keytab is set.}
    auth.kerberos.strip_port={true or false. Strip the port from the service principal name. Default is true.}
    auth.kerberos.use_canonical_hostname={true or false. Resolve the target host to its canonical name for the service principal name. Default is false.}
    auth.kerberos.krb5_conf={Path to a krb5.conf. Applied only when java.security.krb5.conf is not already set.}
    auth.kerberos.debug={true or false. Krb5LoginModule debug output. Default is false.}

- **``krb5.conf`` belongs in ``jvm.crawler.options``**, as
  ``-Djava.security.krb5.conf=/path/to/krb5.conf``. Data-store crawling runs in the crawler
  **child process**, so setting this anywhere that only affects the webapp has no effect, and a
  webapp restart does not pick up a change - the crawl job has to run again. ``auth.kerberos.krb5_conf``
  is a convenience for when nothing has set the property yet: it **never overwrites an
  already-set value**, since the property is JVM-global and one crawler JVM runs every data
  config in a crawl job. When it declines to overwrite, it logs a warning naming both paths.
- **Put ``udp_preference_limit = 1`` in ``krb5.conf``'s ``[libdefaults]``.** Without it, the JDK
  tries UDP first, and when the KDC does not answer (unreachable, a firewall dropping UDP 88, or a
  reply larger than the datagram size), it retries three times at thirty seconds each before
  falling back to TCP. A crawl that looks hung for about a minute and a half per authentication,
  with nothing in the log, is usually this.
- **Always write the principal as ``user@REALM``.** ``default_realm`` is JVM-global, and several
  SharePoint farms in different realms may have to share one ``krb5.conf``, so a bare ``user``
  resolves against whichever realm that file happens to name.
- **``auth.kerberos.use_canonical_hostname`` defaults to ``false``**, deliberately unlike Apache
  HttpClient's own default. With it on, the target host is put through reverse DNS before the
  service principal name is built, which under alternate access mappings or behind a load
  balancer can produce a name no SPN is registered for - and the resulting failure says nothing
  about DNS. Turn it on only if the SPN really is registered against the canonical name.
- **IIS Extended Protection set to ``tokenChecking=Require`` cannot work.** Neither Apache
  HttpClient 4.5 nor 5.x supports channel binding. IIS defaults this to ``None``, so it is usually
  not hit, and there is no workaround when it is.
- **The ticket is obtained once, when the crawl's HTTP client is built, and is never renewed.** A
  crawl that runs longer than the ticket lifetime starts failing to authenticate partway through.
- **``auth.kerberos.password`` is stored and displayed in clear text**, exactly like
  ``auth.ntlm.password``. Fess has no masking mechanism for data-store handler parameters; the
  data config edit screen renders them as a plain text area. Prefer ``auth.kerberos.keytab``, and
  give the keytab file restrictive permissions.
- ``auth.kerberos.debug=true`` makes ``Krb5LoginModule`` write to the crawler process's standard
  output, not to the Fess log.

OAuth (ACS)
-----------

::

    auth.oauth.client_id={OAuth client ID}
    auth.oauth.client_secret={OAuth client secret}
    auth.oauth.tenant={Tenant name, without .sharepoint.com}
    auth.oauth.realm={Azure AD realm/directory ID}

Setting ``auth.oauth.client_id`` enables a client-credentials (app-only) flow against the Windows
Azure Access Control Service, ``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``.
The access token is fetched once, when the crawl's HTTP client is built, applied as a ``Bearer``
``Authorization`` header on every request, and refreshed and retried once on a 401.
**Microsoft has deprecated ACS and scheduled it for retirement**; this connector logs a warning to
that effect on every OAuth-configured crawl. There is no Entra ID app-registration (certificate or
client-secret) flow implemented here - only legacy ACS app-only auth.

Only ``auth.oauth.client_id``'s presence is checked before OAuth is wired up; ``client_secret``,
``tenant``, and ``realm`` are read unconditionally and can silently be blank if omitted, which
breaks token acquisition with no dedicated validation message.

**``sp.version=2013`` and OAuth have never worked together.** Every SharePoint 2013 API call this
connector makes goes through the XML/Atom client, and no code path in that client attaches an
OAuth token to a request - so with both set, every request is sent unauthenticated. The crawl logs
a warning saying exactly this and naming ``auth.ntlm.*`` as the alternative; it does not fail the
job. Use ``auth.ntlm.*`` for SharePoint 2013.

Permissions
===========

``role.skip=true`` (default ``false``) skips fetching per-item permissions entirely: no
``GetListItemRole`` call is made, no ``role`` key is ever set for the item, and the document ends
up carrying only the data config's static Permission setting and, if configured,
``default_permissions`` - no SharePoint-derived permission reaches it at all.

When roles are fetched, SharePoint's own users, security groups, and SharePoint groups are
expanded and mapped to Fess search roles:

- An **on-premises AD** account or group (login name containing a backslash, not starting with an
  Azure claim prefix) is mapped via the standard AD user/group role helpers.
- An **Azure AD (Entra ID)** account (login name starting with ``i:0#.f|membership|``) is mapped
  **twice** - once by its full Azure claim value, once by the AD-account portion before ``@`` in
  that claim - so both an Entra-ID-style and an AD-style role are added for the same user. A
  security group flagged as Azure (by one of several claim-style prefixes, including the special
  ``spo-grid-all-users`` "everyone" group) is mapped the same way, under both forms.
- A **SharePoint group** has its own membership (users, security groups, nested groups) expanded
  recursively, with a visited-group guard to stop infinite recursion between groups that contain
  each other.

``default_permissions`` (comma-separated) is merged in **after** all of the above, and applies
even when SharePoint returned no role for the item at all - the case both ``role.skip=true`` and
"SharePoint returned nothing" produce. The final role list is the union of the data config's
static Permission setting, the SharePoint-derived roles (unless skipped), and
``default_permissions``, de-duplicated.

Subsites and Managed Paths
==========================

Setting ``site.path`` uses the given server-relative managed path verbatim instead of the
hardcoded ``/sites/`` prefix, and ``site.name`` is no longer required.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Setting
   * - Root site collection
     - ``site.path=/``
   * - The ``/teams/eng`` site
     - ``site.path=/teams/eng``
   * - The classic ``/sites/mysite/`` form
     - ``site.name=mysite`` (leave ``site.path`` unset)

Setting ``site.crawl_subsites`` (default ``false``) makes a full site crawl - one where neither
``site.list_name`` nor ``site.doclib_path`` is set - recurse into the site's subsites, discovered
via ``_api/web/webinfos``. Leaving it unset keeps the crawl issuing exactly the same requests it
always has, including never requesting ``webinfos`` at all.

A subsite's documents land in the same data config as the root site's, under their own
server-relative paths - there is nothing in the index that marks a document as having come from a
subsite rather than the root.

``site.max_depth`` (default ``10``) bounds how many subsite hops below the root site are crawled
once ``site.crawl_subsites=true``. The root site itself is depth 0, so ``site.max_depth=1`` crawls
the root's direct children and no further. Setting it below ``1`` while
``site.crawl_subsites=true`` turns the feature back off - no subsite is crawled at all - and is
logged as a warning when the crawl starts.

Turning subsite crawling on **multiplies the crawl's total time** by roughly the number of
subsites discovered (bounded by ``site.max_depth``): each one gets its own full folder listing,
list listing, and (if not at the depth bound) its own ``webinfos`` call, on top of everything the
root site's crawl already does.

``number_of_threads`` and ``readInterval``, described in `Parallel Crawling and Load`_, apply to a
subsite-recursive crawl the same way they apply to any other crawl.

Parallel Crawling and Load
==========================

``number_of_threads`` (default ``1``) is how many crawl targets are worked on at once. At the
default, the crawl runs exactly as it always has: every target is crawled on the crawling thread
and **no thread pool is created at all**.

The value is **capped at twice the processor count** of the machine running Fess, so a data config
cannot ask for more concurrency than the host can serve. A value below ``1`` - or a blank or
unparseable one - falls back to ``1`` rather than being honoured or failing the job. A value that
was capped, or one below ``1``, is logged with both the requested and the actual value; an
unparseable one logs a warning. A blank value logs nothing, because a blank field means the
parameter was simply not set.

The HTTP connection pool is sized to match. Apache HttpClient allows only 2 connections per route
by default, and a whole crawl is a single route: without raising it, every thread past the second
would spend the crawl waiting for a connection rather than making requests.

**``readInterval`` still paces document hand-off, one document per interval, whatever it is set
to.** Threads make the crawl discover and fetch faster; they do not make documents reach the
indexer faster. That is deliberate: dividing an operator's configured interval by the thread count
would multiply exactly the load they configured that interval to limit. A worker that finishes a
document while the previous ones are still being handed over simply waits.

What raising ``number_of_threads`` **does** multiply is the request rate against SharePoint. The
503 backoff and the ``X-SharePointHealthScore`` wait described below are applied per crawl target,
on the thread crawling it, so ``n`` threads make up to ``n`` times the requests a single-threaded
crawl makes - including during a period the farm is signalling that it is busy. On an on-premises
farm, raise this gradually.

Two things put a ceiling on what more threads actually buy:

- **The first time each SharePoint group's membership is read, it is read by one thread at a
  time.** Permissions are resolved through a cache shared by the whole crawl, guarded by a single
  lock held across a group's member lookups. That lock stops one thread from handing another a
  group whose members are still being read, which would index the items that group protects with
  none of its permissions. Once a group is cached, every later reference to it is a cheap lookup,
  so this is a **cold-cache cost**: a crawl of a site with many distinct groups spends its early
  minutes closer to single-threaded than to ``n`` threads, while one whose items share a handful
  of groups barely notices. ``role.skip=true``, which does not read permissions at all, avoids it
  entirely.
- Discovery is sequential per site: a site's folder and list listings are one crawl target, so
  threads have nothing to share out until that target has finished and queued what it found.

**A 503 response** is retried the same as any other error, up to ``retry_limit``, but with an
increasing wait before each retry: 2 seconds, then 4, then 8, doubling up to a 30-second cap, each
randomized to 70-129% of that value. A crawl target that keeps returning 503 pays this wait before
every retry it actually gets, but not after its last one.

**Every response** - successful or not, including a page of a listing the crawl is about to
discard - is inspected for the ``X-SharePointHealthScore`` response header (0 idle to 10 very
busy). A score of 9 or above makes the crawl wait before doing anything else: score 9 waits about
2 seconds, score 10 about 4 seconds, and so on, doubling for each point past 9. **This adds up
across the whole crawl, with no aggregate cap**: a farm sitting at health score 9 under sustained
load adds roughly 2 seconds to *every single request* this connector makes - including every page
of every folder and list listing - which can turn a crawl that would otherwise take hours into one
that takes substantially longer. If a crawl unexpectedly slows down by an order of magnitude,
check the farm's health score during that window before assuming something else is wrong.

Configuration Examples
======================

All of these assume NTLM. To use Kerberos or OAuth instead, see `Authentication`_ and replace the
``auth.ntlm.*`` lines.

List Crawl
----------

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Document Library Crawl
----------------------

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawling a ``/teams/`` Site
---------------------------

``site.path`` lets you point directly at a document library on a site under a managed path other
than ``/sites/``.

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Recursive Subsite Crawl
-----------------------

Starts at the root site collection and follows subsites up to 3 levels deep.

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

Script:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Limitations
===========

- **No incremental or delta crawl of any kind.** There is no change-token, delta-query, or
  "last modified since" filtering anywhere in this connector - every run does a full listing of
  every list, folder, and file it is configured to reach. ``delete_old_docs`` only controls
  whether documents the current full crawl did not see again are deleted afterwards; that is
  post-hoc cleanup, not incremental fetching.
- **``%`` and ``#`` in file/folder names** are supported on the default (non-``2013``) code path.
  Only SharePoint Server 2019 and Subscription Edition accept those two characters in a name at
  all; 2016 explicitly still rejects them, and so does 2013. The default code path reaches such a
  file through the ``...ByServerRelativePath(decodedUrl=...)`` endpoints, which take the decoded
  path, and the crawl escapes both characters in the link it indexes the file under.
  **``sp.version=2013`` cannot reach such a file**, because it uses the older
  ``...ByServerRelativeUrl(...)`` endpoints, which read their argument as an already-encoded URL.
  That is a deliberate limit rather than a gap - a SharePoint 2013 farm cannot hold such a name in
  the first place - so it only matters if ``sp.version=2013`` is pointed at a 2019 or Subscription
  Edition server, which is not a configuration to use. See
  `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  and `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__.
- **IIS Extended Protection ``tokenChecking=Require`` cannot be supported.** Neither Apache
  HttpClient 4.5 nor 5.x implements channel binding, which Extended Protection at ``Require``
  depends on. IIS defaults this setting to ``None``, so most farms are unaffected, and there is no
  workaround for a farm where it is set to ``Require``.
- **Passwords in data-config parameters are stored and displayed in clear text.** This applies to
  ``auth.ntlm.password`` and ``auth.kerberos.password`` alike: Fess has no masking mechanism for
  data-store handler parameters, and the data config edit screen renders them in a plain text
  area. Prefer ``auth.kerberos.keytab`` over ``auth.kerberos.password`` where Kerberos is
  available, and give the keytab file restrictive permissions.
- **``sp.version=2013`` and OAuth have never worked together.** Every SharePoint 2013 API call
  goes through the XML/Atom client, and no code path in that client attaches an OAuth token to a
  request, so with both set every request is sent unauthenticated. Use ``auth.ntlm.*`` for
  SharePoint 2013.
- **Managed paths other than ``/sites/`` and the one set via ``site.path`` are still not
  discovered on their own.** ``site.crawl_subsites`` recurses only from the root site you
  configure, and ``site.path`` reaches exactly the one managed path you set, not every managed
  path on the farm.

Troubleshooting
===============

Authentication Fails Silently
-----------------------------

**Symptom**: requests come back 401 (or similar) with nothing clear in the log to explain why

**Checklist**:

1. Check whether more than one of ``auth.kerberos.principal``, ``auth.ntlm.user``, and
   ``auth.oauth.client_id`` is set - two or more fails the job with a validation error before the
   crawl starts
2. For Kerberos, confirm ``-Djava.security.krb5.conf=...`` is set in ``jvm.crawler.options``.
   Setting it anywhere that only affects the webapp has no effect. After changing it, re-run the
   crawl job - restarting the webapp does not pick it up
3. For Kerberos, confirm ``udp_preference_limit = 1`` is set in ``krb5.conf``'s
   ``[libdefaults]``. Without it, an unresponsive KDC can make each authentication hang for about
   90 seconds (three 30-second UDP retries) with nothing in the log
4. Confirm the principal is written as ``user@REALM`` - a bare ``user`` resolves against
   whatever ``default_realm`` the shared ``krb5.conf`` happens to name
5. For OAuth, confirm ``client_secret``, ``tenant``, and ``realm`` are not blank - only
   ``client_id``'s presence is validated, so the others can be silently empty
6. Confirm IIS Extended Protection is not set to ``tokenChecking=Require`` - there is no
   workaround for that setting
7. For a long-running crawl, check whether it started failing only partway through - the
   Kerberos ticket is obtained once at HTTP client build time and is never renewed, so a crawl
   that outlives the ticket starts failing partway through

The Crawl Is Slow (503s and the Health Score)
---------------------------------------------

**Symptom**: the crawl takes far longer than expected, or times out

**Checklist**:

1. Check the SharePoint farm's ``X-SharePointHealthScore`` during the slow window. A score of 9
   or above adds a wait before every request (about 2 seconds at 9, about 4 at 10, doubling from
   there, with no aggregate cap), which can turn a crawl that should take hours into one that
   takes far longer
2. Check for repeated 503 responses. A 503 is retried up to ``retry_limit`` times, waiting
   2, then 4, then 8 seconds (capped at 30) before each retry
3. Check whether ``number_of_threads`` has been raised too far. More threads mean roughly
   proportionally more requests against SharePoint, which can push the health score higher. Raise
   it gradually on an on-premises farm
4. If ``site.crawl_subsites=true``, remember that total crawl time grows roughly with the number
   of subsites discovered - consider narrowing the scope with ``site.max_depth``

Nothing Gets Indexed
--------------------

**Symptom**: the crawl finishes normally, but search returns zero results

**Checklist**:

1. Check the crawler log for errors or warnings (set ``org.codelibs.fess.ds`` to ``DEBUG`` in
   ``app/WEB-INF/env/crawler/resources/log4j2.xml``)
2. Check ``url``, ``site.name`` (or ``site.path``), and ``site.list_name`` for typos - remember
   that ``site.name`` is not needed once ``site.path`` is set
3. Confirm authentication is actually succeeding (no 401s) - a request that never authenticates
   is a far more common cause than a misconfigured ``role.skip`` or ``default_permissions``
4. If ``include_pattern`` or ``exclude_pattern`` is set, remember these match a server-relative
   path (for a document-library file or a list-item attachment) or the ``FileRef`` (for a list
   item) - not the URL shown in search results. Check for a pattern written for a full URL
5. Check whether ``supported_mimetypes`` or ``max_content_length`` is excluding the files you
   expect to see
6. Check whether ``site.exclude_list`` or ``site.exclude_folder`` is unintentionally excluding
   the target

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-microsoft365` - Microsoft 365 Connector (for SharePoint Online)
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../../admin/plugin-guide` - Plugin Management Guide
