==========================
General API
==========================

Overview
========

General API is an API for managing |Fess| general settings.
You can retrieve and update system-wide configuration settings.

Base URL
========

::

    /api/admin/general

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /
     - Get general settings
   * - PUT
     - /
     - Update general settings

Get General Settings
====================

Request
-------

::

    GET /api/admin/general

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "crawlerDocumentMaxSize": "10485760",
          "crawlerDocumentMaxSiteLength": "50",
          "crawlerDocumentMaxFetcherSize": "3",
          "crawlerDocumentCrawlerThreadCount": "10",
          "crawlerDocumentMaxDepth": "-1",
          "crawlerDocumentMaxAccessCount": "100",
          "indexerThreadDumpEnabled": "true",
          "indexerUnprocessedDocumentSize": "1000",
          "indexerClickCountEnabled": "true",
          "indexerFavoriteCountEnabled": "true",
          "indexerWebfsMaxContentLength": "10485760",
          "indexerWebfsContentEncoding": "UTF-8",
          "queryReplaceTermWithPrefixQuery": "false",
          "queryMaxSearchResultOffset": "100000",
          "queryMaxPageSize": "1000",
          "queryDefaultPageSize": "20",
          "queryAdditionalDefaultQuery": "",
          "queryGeoEnabled": "false",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "suggestBadWord": "true",
          "suggestPopularWordSeedLength": "1",
          "suggestPopularWordTags": "user",
          "suggestPopularWordFields": "tags",
          "suggestPopularWordExcludeWordFields": "",
          "ldapInitialContextFactory": "com.sun.jndi.ldap.LdapCtxFactory",
          "ldapSecurityAuthentication": "simple",
          "ldapProviderUrl": "ldap://localhost:389",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapBindDn": "",
          "ldapBindPassword": "",
          "notificationLogin": "true",
          "notificationSearchTop": "true"
        }
      }
    }

Update General Settings
=======================

Request
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Request Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "crawlerDocumentMaxSize": "20971520",
      "crawlerDocumentMaxSiteLength": "100",
      "crawlerDocumentCrawlerThreadCount": "20",
      "queryMaxPageSize": "500",
      "queryDefaultPageSize": "50",
      "suggestSearchLog": "true",
      "suggestDocuments": "true",
      "suggestBadWord": "true",
      "notificationLogin": "false",
      "notificationSearchTop": "false"
    }

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Field
     - Description
   * - ``crawlerDocumentMaxSize``
     - Maximum document size to crawl (bytes)
   * - ``crawlerDocumentMaxSiteLength``
     - Maximum crawl site length
   * - ``crawlerDocumentMaxFetcherSize``
     - Maximum fetcher size
   * - ``crawlerDocumentCrawlerThreadCount``
     - Crawler thread count
   * - ``crawlerDocumentMaxDepth``
     - Maximum crawl depth (-1 = unlimited)
   * - ``crawlerDocumentMaxAccessCount``
     - Maximum access count
   * - ``indexerThreadDumpEnabled``
     - Enable thread dump
   * - ``indexerUnprocessedDocumentSize``
     - Unprocessed document count
   * - ``indexerClickCountEnabled``
     - Enable click count
   * - ``indexerFavoriteCountEnabled``
     - Enable favorite count
   * - ``queryReplaceTermWithPrefixQuery``
     - Convert to prefix query
   * - ``queryMaxSearchResultOffset``
     - Maximum search result offset
   * - ``queryMaxPageSize``
     - Maximum items per page
   * - ``queryDefaultPageSize``
     - Default items per page
   * - ``queryAdditionalDefaultQuery``
     - Additional default query
   * - ``suggestSearchLog``
     - Enable suggest from search log
   * - ``suggestDocuments``
     - Enable suggest from documents
   * - ``suggestBadWord``
     - Enable bad word filter
   * - ``ldapProviderUrl``
     - LDAP connection URL
   * - ``ldapBaseDn``
     - LDAP base DN
   * - ``notificationLogin``
     - Login notification
   * - ``notificationSearchTop``
     - Search top notification

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Usage Examples
==============

Update Crawler Settings
-----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "crawlerDocumentMaxSize": "52428800",
           "crawlerDocumentCrawlerThreadCount": "15",
           "crawlerDocumentMaxAccessCount": "1000"
         }'

Update Search Settings
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "queryMaxPageSize": "1000",
           "queryDefaultPageSize": "50",
           "queryMaxSearchResultOffset": "50000"
         }'

Update Suggest Settings
-----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestSearchLog": "true",
           "suggestDocuments": "true",
           "suggestBadWord": "true"
         }'

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`api-admin-systeminfo` - System Info API
- :doc:`../../admin/general-guide` - General Settings Guide

