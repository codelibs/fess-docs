================================
Bulk Retrieval of Search Results
================================

About Bulk Retrieval of Search Results
======================================

If you want to access search results beyond the regular limit in |Fess| search, you should use scroll search.

Usage
=====

Configuring Scroll Search
-------------------------

You can enable scroll search by setting the following configuration to true in fess_config.properties:

::

    api.search.scroll=true

Using Scroll Search
-------------------

You can access scroll search by making a request to http://localhost:8080/json/scroll?q=Search_Word, which will return search results in NDJSON format.

If you wish to add fields to the response for each document returned, specify the field names separated by commas in the following configuration in fess_config.properties:

::

    query.additional.scroll.response.fields=