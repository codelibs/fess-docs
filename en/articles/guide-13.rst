============================================================
Part 13: Multi-Tenant Search Platform -- Designing a Single Fess Instance to Serve Multiple Organizations
============================================================

Introduction
============

When you want to provide Fess to multiple internal departments or to multiple customers as an MSP (Managed Service Provider), building a separate Fess instance for each tenant is inefficient.

This article explains a multi-tenant design that serves multiple tenants (organizations, departments, or customers) from a single Fess instance.

Target Audience
===============

- Those who want to provide search services to multiple organizations or departments
- Those interested in multi-tenant design with Fess
- Those who want to learn how to use the virtual host feature

Scenario
========

We assume a scenario where the IT department of a corporate group provides search services to three subsidiaries.

.. list-table:: Tenant Configuration
   :header-rows: 1
   :widths: 25 35 40

   * - Tenant
     - Domain
     - Search Target
   * - Company A (Manufacturing)
     - search-a.example.com
     - Product specifications, quality control documents
   * - Company B (Retail)
     - search-b.example.com
     - Store manuals, product information
   * - Company C (Services)
     - search-c.example.com
     - Customer support manuals, FAQ

Each tenant has the following requirements:

- Data must not be visible between tenants (data isolation)
- Each tenant needs a different design (branding)
- Each tenant needs independent crawl settings

Virtual Host Feature
======================

The virtual host feature of Fess allows you to provide different search experiences depending on the hostname used for access.

Virtual Host Configuration
--------------------------

Set the virtual host value in the administration console.
By associating this value with crawl settings and labels, you can achieve data isolation for each tenant.

Design Considerations
---------------------

**DNS / Load Balancer Configuration**

Configure DNS so that each tenant's domain points to the same Fess server.

::

    search-a.example.com → Fess Server (192.168.1.100)
    search-b.example.com → Fess Server (192.168.1.100)
    search-c.example.com → Fess Server (192.168.1.100)

Fess examines the HTTP headers of the request to determine which virtual host is being accessed.
By default, the Host header is used, but you can specify any header using the ``virtual.host.headers`` setting.
The configuration format is ``HeaderName:Value=VirtualHostKey`` (e.g., ``Host:search-a.example.com=tenant-a``).

Tenant Isolation Design
========================

Data Isolation
--------------

Data isolation between tenants is achieved through the ``virtual_host`` field on documents, provided by the virtual host feature.

**Isolation via Virtual Host**

When you set the virtual host key in the "Virtual Host" field of the crawl settings, crawled documents are assigned a ``virtual_host`` field.
During search, this field is used for automatic filtering, so users accessing through each tenant's domain will only see that tenant's documents in the search results.

- ``tenant-a``: Company A's documents
- ``tenant-b``: Company B's documents
- ``tenant-c``: Company C's documents

Additionally, by setting the "Virtual Host" field on labels, you can also separate the labels displayed for each tenant.

**Isolation via Roles**

For stricter isolation requirements, combine role-based search (see Part 5).
Create roles for each tenant and assign them to crawl settings and users.

Crawl Configuration Isolation
------------------------------

Each tenant's crawl configuration is managed independently.

.. list-table:: Crawl Settings by Tenant
   :header-rows: 1
   :widths: 15 30 25 30

   * - Tenant
     - Crawl Target
     - Schedule
     - Label
   * - Company A
     - smb://fs-a/docs/
     - Daily at 1:00
     - tenant-a
   * - Company B
     - https://portal-b.example.com/
     - Daily at 2:00
     - tenant-b
   * - Company C
     - smb://fs-c/manuals/
     - Daily at 3:00
     - tenant-c

Tenant-Specific Themes
========================

Using the theme feature of Fess, you can provide different designs for each tenant.

Theme Design
------------

Prepare themes that match each tenant's brand colors and logo.

- Company A: A solid design befitting a manufacturing company (blue tones)
- Company B: A bright design for retail (green tones)
- Company C: A friendly design for a service company (orange tones)

Linking Virtual Hosts and Themes
---------------------------------

By switching themes for each virtual host, users of each tenant will see a search screen with their own company branding.

Fess offers built-in themes such as ``simple``, ``docsearch``, and ``codesearch``, and also supports custom themes.

API Access Isolation
=====================

API Access Tokens per Tenant
-----------------------------

Issue individual access tokens for each tenant.
By associating roles with tokens, tenant isolation is also applied to API access.

.. list-table:: Access Token Configuration
   :header-rows: 1
   :widths: 20 30 50

   * - Tenant
     - Token Name
     - Assigned Role
   * - Company A
     - tenant-a-api-token
     - tenant-a-role
   * - Company B
     - tenant-b-api-token
     - tenant-b-role
   * - Company C
     - tenant-c-api-token
     - tenant-c-role

When each tenant's system integrates via API (see Part 11), using tenant-specific tokens guarantees that they cannot access other tenants' data.

Operational Considerations
===========================

Resource Management
-------------------

Since a single Fess instance serves multiple tenants, careful attention to resource allocation is necessary.

- **Crawl load balancing**: Stagger tenant crawl schedules to avoid simultaneous execution
- **Index size**: Monitor the total index size across all tenants
- **Memory**: Adjust the JVM heap according to the number of tenants and documents

Adding and Removing Tenants
----------------------------

Standardize the procedure for adding new tenants.

1. Create a label
2. Create a role
3. Register crawl settings
4. Configure the virtual host
5. Issue an access token
6. Add DNS settings

When removing a tenant, do not forget to delete the associated index data.

Scaling Criteria
-----------------

If you observe the following symptoms, consider splitting or scaling Fess instances (see Part 14).

- Search response times are degrading
- Crawls are not completing within the scheduled window
- Out-of-memory errors occur frequently
- The number of tenants exceeds 10

Summary
=======

This article explained multi-tenant design using the virtual host feature of Fess.

- Tenant-specific access through virtual hosts
- Data isolation using labels and roles
- Tenant-specific branding through themes
- Tenant isolation via API access tokens
- Resource management and scaling criteria

With a single Fess instance, you can efficiently serve multiple tenants, keeping management costs low while meeting each tenant's requirements.

The next article will cover scaling strategies for search systems.

References
==========

- `Fess Virtual Host <https://fess.codelibs.org/ja/15.5/config/virtual-host.html>`__

- `Fess Label Settings <https://fess.codelibs.org/ja/15.5/admin/labeltype.html>`__
