==========================
API Stats
==========================

Vue d'ensemble
==============

L'API Stats permet d'obtenir les statistiques de |Fess|.
Vous pouvez consulter les donnees statistiques sur les requetes de recherche, les clics, les favoris, etc.

URL de base
===========

::

    /api/admin/stats

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention des statistiques

Obtention des statistiques
==========================

Requete
-------

::

    GET /api/admin/stats

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``from``
     - String
     - Non
     - Date/heure de debut (format ISO 8601)
   * - ``to``
     - String
     - Non
     - Date/heure de fin (format ISO 8601)
   * - ``type``
     - String
     - Non
     - Type de statistiques (query/click/favorite)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 12345,
          "uniqueQueries": 5678,
          "totalClicks": 9876,
          "totalFavorites": 543,
          "averageResponseTime": 123.45,
          "topQueries": [
            {
              "query": "fess",
              "count": 567
            }
          ],
          "topClickedDocuments": [
            {
              "url": "https://example.com/doc1",
              "title": "Document 1",
              "count": 234
            }
          ],
          "queryTrends": [
            {
              "date": "2025-01-01",
              "count": 234
            }
          ]
        }
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``totalQueries``
     - Nombre total de requetes de recherche
   * - ``uniqueQueries``
     - Nombre de requetes uniques
   * - ``totalClicks``
     - Nombre total de clics
   * - ``totalFavorites``
     - Nombre total de favoris
   * - ``averageResponseTime``
     - Temps de reponse moyen (millisecondes)
   * - ``topQueries``
     - Requetes populaires
   * - ``topClickedDocuments``
     - Documents populaires
   * - ``queryTrends``
     - Tendances des requetes

Exemples d'utilisation
======================

Obtention de toutes les statistiques
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Statistiques pour une periode
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Statistiques des requetes
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Top 10 des requetes populaires
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.stats.topQueries[:10]'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-log` - API des journaux
- :doc:`api-admin-systeminfo` - API des informations systeme
- :doc:`../../admin/stats-guide` - Guide des statistiques
