============================================
Serving Multiple Organizations from One Fess
============================================

Introduction
============

When you want to offer a search service to each group company or department, building one Fess per organization multiplies the servers and the crawl configurations to manage by the number of organizations.
With the virtual host feature of Fess, you can publish a single Fess under several host names and switch the search targets, labels and search page by host name.

However, a virtual host only changes what is shown depending on which host name a request came in on; it is not access control.
To reliably keep one organization's documents hidden from another, you must combine it with role-based permissions and login.

In this article, we use two tenants, Company A and Company B, as an example and configure the following in Fess 15.9, step by step.

- Map host names to tenants with "Virtual Host" in [General]
- Set the virtual host and permissions on crawl configurations and labels to separate each tenant's documents
- Give each tenant its own search page with a theme named after the virtual host key
- Log in as a tenant user and confirm that other tenants' documents are not visible
- Add and remove tenants in the correct order

The basics of roles, groups and users are covered in :doc:`guide-05`.

Key Point First: A Virtual Host Is Not Access Control
=====================================================

For each request, Fess evaluates the lines written in "Virtual Host" in [General] from top to bottom, and uses the virtual host name (hereafter, the key) of the first line whose specified header (usually ``Host``) matches.
Once the key is determined, the following features are filtered by that key.

- Search results: only documents whose crawl configuration has that key in "Virtual Hosts" are returned (the same applies to the search API)
- Labels: only labels whose "Virtual Host" field is that key are displayed
- Key Match, Related Content and Related Query: only settings whose "Virtual Host" field is that key are used
- Search page: if there is a theme whose name is the key in lowercase, the page is displayed with that theme

On the other hand, for a request that matches none of the lines, none of this filtering takes place.
If someone accesses the server directly by IP address, or a reverse proxy rewrites the ``Host`` header, the virtual host filtering disappears and the documents of all tenants that the user's permissions allow become searchable.
A misspelled host name or a missing port number in [General] does not cause an error either; it is simply treated as "no match".

To keep documents from being visible across tenants, therefore, combine the following two measures.

- Set the permissions of each tenant's documents to that tenant's role only (for example, ``{role}tenanta_user``)
- Require login for the search page and assign the tenant's role to users

What We Will Build
==================

.. list-table::
   :header-rows: 1
   :widths: 16 26 14 18 26

   * - Tenant
     - Public host name
     - Key
     - Role
     - Crawl target
   * - Company A
     - ``search-a.example.com``
     - ``tenanta``
     - ``tenanta_user``
     - ``https://portal-a.example.com/``
   * - Company B
     - ``search-b.example.com``
     - ``tenantb``
     - ``tenantb_user``
     - ``https://portal-b.example.com/``

Only alphanumeric characters and underscores (``a-zA-Z0-9_``) can be used in a key.
Any other characters are removed when the setting is saved, so if you write ``tenant-a``, the key becomes ``tenanta``, and writing ``tenant-a`` in a crawl configuration will not match it.
``admin``, ``common``, ``error``, ``login`` and ``profile`` are reserved and cannot be used.

The "Virtual Hosts" field of crawl configurations and the "Virtual Host" field of labels are free text, and they are compared with the key case-sensitively.
Theme names can only be lowercase as well, so making your keys lowercase alphanumeric from the start avoids mistakes.

Step 1: Map Host Names to Keys
==============================

Open [System] > [General] in the admin console, write one ``header-name:header-value=key`` entry per line in "Virtual Host", and update.

::

    Host:search-a.example.com=tenanta
    Host:search-b.example.com=tenantb

The header value is compared as an exact, case-insensitive match.
When a browser accesses a non-standard port (anything other than 80 and 443), it adds the port number to the ``Host`` header, so if users access Fess's port 8080 directly, include the port as follows.
You can also list both forms side by side.

::

    Host:search-a.example.com:8080=tenanta
    Host:search-b.example.com:8080=tenantb

The setting takes effect as soon as it is saved; no restart is needed.
You can also write it in the same format in ``virtual.host.headers`` in ``fess_config.properties``, but if [General] has a value, that value takes precedence.

When you put Fess behind a reverse proxy, pass the ``Host`` header sent by the browser through to Fess.
By default, Nginx sets ``Host`` to the ``proxy_pass`` destination, so ``proxy_set_header Host $host;`` is required.

::

    server {
        server_name search-a.example.com search-b.example.com;
        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
        }
    }

In a setup that rewrites ``Host``, you can instead specify ``X-Forwarded-Host`` as the header name (for example, ``X-Forwarded-Host:search-a.example.com=tenanta``).

.. warning::

   The settings in [General] are saved in ``system.properties`` inside the container.
   ``fess01`` in docker-fess has no volume, so recreating the container with ``docker compose down`` also erases the "Virtual Host" value (it survives ``stop`` and ``start``).
   The theme you upload in a later step is also stored inside the container, so it is lost in the same way.
   For ways to keep the settings, see `Docker Installation (Detailed Guide) <https://fess.codelibs.org/stable/install/install-docker.html>`__.

Step 2: Create Tenant Roles and Users
=====================================

1. In [User] > [Role], create roles named ``tenanta_user`` and ``tenantb_user``.
2. In [User] > [User], create the users of each tenant and select that tenant's role in "Roles".
3. In [System] > [General], enable "Login Required".

Logged-in users do not get ``{role}guest``; they search only with the permissions of their user, groups and roles.
If you want to use LDAP or SSO groups as they are, you can specify ``{group}<group name>`` instead of a role.
For how permissions work and LDAP integration, see :doc:`guide-05`; for SSO, see :doc:`guide-15`.

Step 3: Create a Label for Each Tenant
======================================

A label is assigned at crawl time to documents whose URL matches "Included Paths".
Create the labels before crawling.

In [Crawler] > [Label], click [Create New] and enter the following for Company A (create Company B's label in the same way).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Value
   * - Name
     - ``Company A Portal``
   * - Value
     - ``tenanta_docs`` (alphanumeric characters and underscores only)
   * - Included Paths
     - ``https://portal-a\.example\.com/.*``
   * - Permissions
     - ``{role}tenanta_user``
   * - Virtual Host
     - ``tenanta``

The permissions of a new label contain ``{role}guest``.
A label is displayed only when the user has a role listed in its permissions, so if you leave ``{role}guest`` as is, the label is not shown to logged-in tenant users.

A label whose "Virtual Host" is empty is not displayed when accessed through a virtual host.
A label can have only one virtual host, so if you want several tenants to see the same label, create one label per tenant with the same name and value, and put each key in its "Virtual Host".
The same goes for Key Match, Related Content and Related Query: settings whose "Virtual Host" is empty are not used on tenant hosts.

Step 4: Set the Virtual Host and Permissions on Crawl Configurations
====================================================================

In [Crawler] > [Web], create the crawl configuration for Company A.
File system and data store crawl configurations have the same two fields.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Value
   * - Name
     - ``Company A Portal``
   * - URLs
     - ``https://portal-a.example.com/``
   * - Included URLs
     - ``https://portal-a.example.com/.*``
   * - Permissions
     - ``{role}tenanta_user`` (delete the ``{role}guest`` that is entered by default)
   * - Virtual Hosts
     - ``tenanta``

If you leave ``{role}guest``, those documents become visible to access by IP address and to access before login.

For documents shown to several tenants, such as group-wide regulations, write one line per tenant for both tenants in the "Virtual Hosts" and "Permissions" fields of a single crawl configuration.

::

    Virtual Hosts:
    tenanta
    tenantb

    Permissions:
    {role}tenanta_user
    {role}tenantb_user

The virtual hosts and permissions are written into the documents at crawl time.
If you change them in a configuration that has already been crawled, existing documents do not reflect the change until they are crawled again.

After saving the configuration, either create a tenant-specific job with [Create New Job] on the details screen, or run ``Default Crawler`` with [Start Now] in [System] > [Scheduler].

Step 5: Prepare a Search Page for Each Tenant
=============================================

In Fess 15.9, the search page is rendered by a theme.
If you install a theme whose ``name`` in ``theme.yml`` equals the key in lowercase, that theme is used for requests with that key.
There is no need to make it the default theme; requests that match no key use the default theme.

Create it by copying the bundled ``bootstrap`` theme.
With Docker, extract it from the container as follows.

::

    $ docker cp fess01:/usr/share/fess/app/themes/bootstrap ./tenanta

1. In ``tenanta/theme.yml``, change ``name`` to ``tenanta`` and ``displayName`` to something like ``Company A Search``.
2. Replace ``assets/styles.css`` (colors) and ``assets/logo-head.png`` and ``assets/logo.png`` (logos). ``index.html`` does not need to be changed.
3. Package it so that ``theme.yml`` is at the root of the ZIP.

   ::

       $ cd tenanta && zip -r ../tenanta.zip .

4. Upload ``tenanta.zip`` with [Upload] in [System] > [Theme].

The login page (``/login/``) is shared by all tenants and cannot be changed by a theme.
For details on copying the bundled theme, see `Theme Development Guide <https://fess.codelibs.org/stable/dev/theme-development.html>`__.

Verifying the Isolation
=======================

Before switching DNS, you can add ``127.0.0.1 search-a.example.com search-b.example.com`` to your local ``/etc/hosts`` and try each host from a browser, for example ``http://search-a.example.com:8080/`` ([General] needs the lines with the port).
Check the following four cases by searching for a word that occurs in the crawl targets.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Access
     - Expected result
   * - Company A user via ``search-a.example.com``
     - Only Company A's documents appear. The only label is "Company A Portal". The page is displayed with Company A's theme
   * - Company A user via ``search-b.example.com``
     - 0 results (the user has no permission for Company B's documents, and Company A's documents are excluded by the virtual host)
   * - Company A user via the IP address (``http://<server>:8080/``)
     - Only Company A's documents appear (there is no virtual host filtering, but the permissions protect them)
   * - Access without logging in
     - Search is not possible until the user logs in

If you created shared documents for both tenants, they also appear in rows 1 to 3.
If Company B's documents appear in row 3, ``{role}guest`` remains in one of the crawl configurations.
If row 1 returns 0 results, compare the lines in [General] (with or without the port number) with the spelling in "Virtual Hosts" of the crawl configuration.

You can perform the same check with the search API.
In [System] > [Access Token], create a token with the permission ``{role}tenanta_user``, and call the API with different ``Host`` headers.

::

    $ curl -s -H "Authorization: Bearer <Company A token>" \
        -H "Host: search-a.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"
    $ curl -s -H "Authorization: Bearer <Company A token>" \
        -H "Host: search-b.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"

It works as intended if ``response.record_count`` is 1 or more for the first call and 0 for the second.
An access token is not tied to a virtual host; the virtual host is determined by the host name the request is sent to.
What a token can see is determined by the token's permissions, so always give tokens handed to a tenant's systems that tenant's role only.
For how to use the API, see :doc:`guide-11`.

Once in operation, you can check the number of searches per virtual host on the [Audience] tab of [System Info] > [Search Log].

Adding and Removing Tenants
===========================

When adding a tenant, proceed in the following order, because later steps use values from earlier ones.

1. Add a line to "Virtual Host" in [General]
2. Create the role, users and, if needed, access tokens
3. Create the labels (with the virtual host and permissions)
4. Create the crawl configurations (with the virtual host and permissions) and crawl
5. Upload the theme
6. Check the four cases in "Verifying the Isolation"
7. Publish it through DNS and the reverse proxy

When removing a tenant, conversely, start by closing the entry points.

1. Remove the host name from DNS and the reverse proxy
2. Delete the crawl configurations and the jobs created for them ([System] > [Scheduler])
3. Delete the documents from the index (see below)
4. Delete the access tokens, users and role
5. Delete the labels, key matches and other settings for that key, and the theme
6. Delete the line from "Virtual Host" in [General]

Deleting a crawl configuration does not remove the documents already crawled from the index.
Delete the documents in [System Info] > [Search].
This screen does not apply role or virtual host filtering, so the documents of all tenants are in scope.
Search with the tenant's label in the search box, such as ``label:tenantb_docs``, confirm that the count and the results contain only Company B's documents, and then click [Delete All by this Query].
For web documents, you can also specify the beginning of the URL, such as ``site:portal-b.example.com``.

Do not use a query such as ``virtual_host:tenantb``.
By default, ``virtual_host`` is not among the fields available for search, so the whole string is treated as a search for that text in the document body, and it cannot select the documents you intend.

The Option of Separate Instances
================================

In a configuration that shares one Fess, the following cannot be separated.

- The admin console and administrators: every administrator can operate on the settings, users and documents of all tenants
- System-wide settings such as the [General] settings and dictionaries
- The login page

If you want to delegate administration to each tenant, or contracts require separate indexes, run a Fess per tenant and use different index names.
``compose/multi-instance`` in docker-fess connects two Fess instances (ports 8080 and 8081) to one OpenSearch.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess
    $ git checkout v15.9.0
    $ cd compose/multi-instance
    $ docker compose -f compose.yaml -f compose-fess01.yaml -f compose-fess02.yaml up -d

In each Fess's ``FESS_JAVA_OPTS``, the index names for documents, suggestions, crawling, configuration, users, logs and dictionaries (8 items, such as ``-Dfess.config.index.document.search.index=fess01.search``) differ per instance.
Because configuration and users are also split by index, the admin console, users and search logs are per tenant as well.
To add a tenant, copy ``compose-fess02.yaml`` and change the service name, the port and all the index names.

.. warning::

   The OpenSearch in this configuration exposes port 9200 with the security plugin disabled.
   Anyone who can reach port 9200 can read the indexes of all tenants, so close the port in production.

Further Reading
===============

- Learn more about permission design with roles, groups and LDAP: :doc:`guide-05`
- Call the search API from a tenant's systems: :doc:`guide-11`
- Have users log in with SSO and protect access: :doc:`guide-15`
- Scale out Fess and OpenSearch as tenants grow: :doc:`guide-14`
- Embed the search page in an existing site: :doc:`guide-03`

References
==========

- `Virtual Host <https://fess.codelibs.org/stable/config/security-virtual-host.html>`__
- `Multitenancy Configuration <https://fess.codelibs.org/stable/config/multitenancy.html>`__
- `Role-Based Search Configuration <https://fess.codelibs.org/stable/config/security-role.html>`__
- `Label <https://fess.codelibs.org/stable/admin/labeltype-guide.html>`__
- `Theme <https://fess.codelibs.org/stable/admin/theme-guide.html>`__
- `Search <https://fess.codelibs.org/stable/admin/searchlist-guide.html>`__
- `docker-fess multi-instance (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose/multi-instance>`__
