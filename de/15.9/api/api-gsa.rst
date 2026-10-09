====================================
Google Search Appliance-kompatible API
====================================

.. warning::

   Die zur Google Search Appliance (GSA) kompatible API (``/gsa/``) wurde in |Fess| 14.8 entfernt. Weder |Fess| 15.9 selbst noch die Plugins für die alten APIs (``fess-webapp-classic-api`` und ``fess-webapp-v1-api``) enthalten eine Implementierung von ``/gsa/``. Die Einstellung ``web.api.gsa`` hat daher keine Wirkung, und eine Anfrage an ``/gsa/`` liefert ``404``. Verwenden Sie zum Suchen ``/api/v2/search`` aus :doc:`api-search`.
