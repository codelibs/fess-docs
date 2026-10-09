================================
Google Search Appliance Compatible API
================================

.. warning::

   The Google Search Appliance (GSA) compatible API (``/gsa/``) was removed in |Fess| 14.8. Neither |Fess| 15.9 itself nor the plugins that serve the legacy APIs (``fess-webapp-classic-api`` and ``fess-webapp-v1-api``) implement ``/gsa/``, so setting ``web.api.gsa`` has no effect and a request to ``/gsa/`` returns ``404``. To search, use ``/api/v2/search`` described in :doc:`api-search`.
