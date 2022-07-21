================================
Google Search Appliance Compatible API
================================

Google Search Appliance(GSA) Compatible API returns a search result as XML format for GSA.
For more details about XML format, see `GSA official document <https://www.google.com/support/enterprise/static/gsa/docs/admin/74/gsa_doc_set/xml_reference/results_format.html>`__.

Configuration
==================

To enable GSA Compatible API, set ``web.api.gsa=true`` in system.properties.

Request
==================

Accessing to ``http://localhost:8080/gsa/?q=WORD``, |Fess| returns a result as GSA compatible format.
For request parameters, see :doc:`Search API <api-search>`.
