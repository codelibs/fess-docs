===================================
API compatible Google Search Appliance
===================================

.. warning::

   L'API compatible Google Search Appliance (GSA) (``/gsa/``) a été supprimée dans |Fess| 14.8. Ni |Fess| 15.9 lui-même ni les plugins des anciennes API (``fess-webapp-classic-api`` et ``fess-webapp-v1-api``) ne contiennent d'implémentation de ``/gsa/`` : le paramètre ``web.api.gsa`` n'a donc aucun effet et une requête vers ``/gsa/`` renvoie ``404``. Pour rechercher, utilisez ``/api/v2/search``, décrit dans :doc:`api-search`.
