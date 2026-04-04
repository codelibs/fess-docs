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

Virtual Host Header Configuration
==================================

To enable the virtual host feature, configure the ``virtual.host.headers`` property.
This property is defined in ``fess_config.properties``.

Configuration Format
--------------------

Specify each entry in the format ``HeaderName:HeaderValue=VirtualHostKey``, one per line:

::

    # fess_config.properties
    virtual.host.headers=Host:tenant1.example.com=tenant1\n\
    Host:tenant2.example.com=tenant2

For multiple virtual hosts, separate entries with newlines.

Virtual Host Key Restrictions
-----------------------------

Virtual host keys have the following restrictions:

- Only alphanumeric characters and underscores (``a-zA-Z0-9_``) are allowed. Other characters are automatically removed.
- The following key names are reserved and cannot be used: ``admin``, ``common``, ``error``, ``login``, ``profile``

Admin Panel Configuration
==========================

Crawl Configuration
--------------------

By specifying a virtual host in web crawl settings, you can separate content:

1. Log in to the admin panel
2. Create a crawl configuration under "Crawler" -> "Web"
3. Select a virtual host key defined in ``virtual.host.headers`` in the "Virtual Host" field
4. Content crawled with this configuration will only be searchable from the specified virtual host

Access Control
==============

Combining Virtual Hosts and Roles
---------------------------------

By combining virtual hosts with role-based access control,
finer-grained access control is possible.

Configure the virtual host and permissions together in the crawl configuration:

::

    # Virtual host in crawl configuration
    tenant1

    # Permissions in crawl configuration
    {role}tenant1_user

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

To apply custom CSS per virtual host, edit CSS files in the admin panel under "System" -> "Design". You can also place custom templates in the view directory corresponding to the virtual host key.

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

Use separate |Fess| instances and indexes for each tenant:

::

    # Tenant 1 Fess instance (fess_config.properties)
    index.document.search.index=fess_tenant1.search

    # Tenant 2 Fess instance (fess_config.properties)
    index.document.search.index=fess_tenant2.search

.. note::
   ``index.document.search.index`` can only be set to one value per instance.
   For complete index-level separation, you need to run separate |Fess| instances per tenant
   or implement custom code. For typical multitenancy, logical separation via the virtual host feature is sufficient.

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
