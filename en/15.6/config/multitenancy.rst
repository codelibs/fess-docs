==================================
Multitenancy Configuration
==================================

Overview
========

The multitenancy feature of |Fess| allows you to operate multiple tenants
(organizations, departments, customers, etc.) separately within a single |Fess| instance.

Using the virtual host feature, you can provide each tenant with:

- Independent search UI
- Separated content
- Customized design

Virtual Host Feature
====================

Virtual host is a feature that provides different search environments based on the HTTP request hostname.

How It Works
------------

1. User accesses ``tenant1.example.com``
2. |Fess| identifies the hostname
3. Applies the corresponding virtual host configuration
4. Displays tenant-specific content and UI

Virtual Host Configuration
==========================

Configuration via Admin Panel
-----------------------------

1. Log in to the admin panel
2. Navigate to "Crawler" -> "Virtual Host"
3. Click "Create New"
4. Configure the following:

   - **Hostname**: ``tenant1.example.com``
   - **Path**: ``/tenant1`` (optional)

Integration with Crawl Configuration
------------------------------------

By specifying a virtual host in web crawl settings, you can separate content:

1. Create a crawl configuration under "Crawler" -> "Web"
2. Select the target virtual host in the "Virtual Host" field
3. Content crawled with this configuration will only be searchable from the specified virtual host

Access Control
==============

Combining Virtual Hosts and Roles
---------------------------------

By combining virtual hosts with role-based access control,
finer-grained access control is possible:

::

    # Configuration example
    virtual.host=tenant1.example.com
    permissions=role_tenant1_user

Role-Based Search
-----------------

For details, see :doc:`security-role`.

UI Customization
================

You can customize the UI for each virtual host.

Applying Themes
---------------

Apply different themes for each virtual host:

1. Set up themes under "System" -> "Design"
2. Specify the theme in the virtual host configuration

Custom CSS
----------

Apply custom CSS for each virtual host:

::

    # Virtual host-specific CSS file
    /webapp/WEB-INF/view/tenant1/css/custom.css

Label Settings
--------------

Restrict displayed labels for each virtual host:

1. Specify the virtual host in the label type settings
2. Labels will only be displayed on the specified virtual host

API Authentication
==================

Control API access for each virtual host:

Access Tokens
-------------

Issue access tokens linked to virtual hosts:

1. Create a token under "System" -> "Access Token"
2. Associate the token with a virtual host

API Request
-----------

::

    curl -H "Authorization: Bearer TENANT_TOKEN" \
         "https://tenant1.example.com/api/v1/search?q=keyword"

DNS Configuration
=================

Example DNS configuration to achieve multitenancy:

Subdomains to the Same Server
-----------------------------

::

    # DNS configuration
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # Or wildcard
    *.example.com          A    192.168.1.100

Reverse Proxy Configuration
---------------------------

Example reverse proxy configuration using Nginx:

::

    server {
        server_name tenant1.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        server_name tenant2.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

Data Separation
===============

If complete data separation is required, consider the following approaches:

Index-Level Separation
----------------------

Use separate indexes for each tenant:

::

    # Index for tenant 1
    index.document.search.index=fess_tenant1.search

    # Index for tenant 2
    index.document.search.index=fess_tenant2.search

.. note::
   Index-level separation may require custom implementation.

Best Practices
==============

1. **Clear naming conventions**: Use consistent naming conventions for virtual hosts and roles
2. **Testing**: Thoroughly test operations on each tenant
3. **Monitoring**: Monitor resource usage for each tenant
4. **Documentation**: Document tenant configurations

Limitations
===========

- The admin panel is shared across all tenants
- System settings affect all tenants
- Some features may not support virtual hosts

Reference Information
=====================

- :doc:`security-role` - Role-Based Access Control
- :doc:`security-virtual-host` - Virtual Host Configuration Details
- :doc:`../admin/design-guide` - Design Customization
