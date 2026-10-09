========================================
API compatible con Google Search Appliance
========================================

.. warning::

   La API compatible con Google Search Appliance (GSA) (``/gsa/``) se eliminó en |Fess| 14.8. Ni |Fess| 15.9 ni los plugins de las API antiguas (``fess-webapp-classic-api`` y ``fess-webapp-v1-api``) incluyen una implementación de ``/gsa/``, por lo que definir ``web.api.gsa`` no tiene ningún efecto y una solicitud a ``/gsa/`` devuelve ``404``. Para buscar, utilice ``/api/v2/search``, descrita en :doc:`api-search`.
