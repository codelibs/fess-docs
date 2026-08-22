================================
Google Search Appliance Compatible API
================================

|Fess| also provides an API that returns search results in Google Search Appliance (GSA) compatible XML format.
For details about the XML format, please refer to the `GSA Official Documentation <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__.

Configuration
=============

To enable the Google Search Appliance Compatible API, add ``web.api.gsa=true`` to system.properties.

Request
=======

By sending a request to |Fess| like
``http://localhost:8080/gsa/?q=search_term``,
you can receive search results in GSA-compatible XML format.
The request parameters that can be specified are the same as the `JSON Response Search API <api-search.html>`__.
