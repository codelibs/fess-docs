==========================
API SearchLog
==========================

Vue d'ensemble
==============

L'API SearchLog permet d'obtenir et de gerer les journaux de recherche de |Fess|.
Elle peut etre utilisee pour l'analyse du comportement de recherche des utilisateurs et l'amelioration de la qualite de recherche.

URL de base
===========

::

    /api/admin/searchlog

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
     - Obtention de la liste des journaux de recherche
   * - GET
     - /{id}
     - Obtention des details d'un journal de recherche
   * - DELETE
     - /{id}
     - Suppression d'un journal de recherche
   * - DELETE
     - /delete-all
     - Suppression en masse des journaux de recherche
   * - GET
     - /stats
     - Obtention des statistiques de recherche

Obtention de la liste des journaux de recherche
===============================================

Requete
-------

::

    GET /api/admin/searchlog

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'elements par page (par defaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 0)
   * - ``from``
     - String
     - Non
     - Date/heure de debut (format ISO 8601)
   * - ``to``
     - String
     - Non
     - Date/heure de fin (format ISO 8601)
   * - ``query``
     - String
     - Non
     - Filtre par requete de recherche
   * - ``user``
     - String
     - Non
     - Filtre par ID utilisateur

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "searchlog_id_1",
            "searchWord": "Fess installation",
            "requestedAt": "2025-01-29T10:00:00Z",
            "responseTime": 125,
            "hitCount": 234,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user001",
            "userSessionId": "session_abc123",
            "clientIp": "192.168.1.100",
            "referer": "https://example.com/",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user", "admin"],
            "languages": ["ja"]
          },
          {
            "id": "searchlog_id_2",
            "searchWord": "configuration recherche",
            "requestedAt": "2025-01-29T09:55:00Z",
            "responseTime": 98,
            "hitCount": 567,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user002",
            "userSessionId": "session_def456",
            "clientIp": "192.168.1.101",
            "referer": "",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user"],
            "languages": ["ja", "en"]
          }
        ],
        "total": 10000
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID du journal de recherche
   * - ``searchWord``
     - Mot-cle de recherche
   * - ``requestedAt``
     - Date/heure de la recherche
   * - ``responseTime``
     - Temps de reponse (millisecondes)
   * - ``hitCount``
     - Nombre de resultats
   * - ``queryOffset``
     - Offset des resultats
   * - ``queryPageSize``
     - Taille de la page
   * - ``user``
     - ID utilisateur
   * - ``userSessionId``
     - ID de session
   * - ``clientIp``
     - Adresse IP du client
   * - ``referer``
     - Referent
   * - ``userAgent``
     - Agent utilisateur
   * - ``roles``
     - Roles de l'utilisateur
   * - ``languages``
     - Langues de recherche

Obtention des details d'un journal de recherche
===============================================

Requete
-------

::

    GET /api/admin/searchlog/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "searchlog_id_1",
          "searchWord": "Fess installation",
          "requestedAt": "2025-01-29T10:00:00Z",
          "responseTime": 125,
          "hitCount": 234,
          "queryOffset": 0,
          "queryPageSize": 10,
          "user": "user001",
          "userSessionId": "session_abc123",
          "clientIp": "192.168.1.100",
          "referer": "https://example.com/",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "roles": ["user", "admin"],
          "languages": ["ja"],
          "clickLogs": [
            {
              "url": "https://fess.codelibs.org/install.html",
              "docId": "doc_123",
              "order": 1,
              "clickedAt": "2025-01-29T10:00:15Z"
            }
          ]
        }
      }
    }

Suppression d'un journal de recherche
=====================================

Requete
-------

::

    DELETE /api/admin/searchlog/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search log deleted successfully"
      }
    }

Suppression en masse des journaux de recherche
==============================================

Requete
-------

::

    DELETE /api/admin/searchlog/delete-all

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``before``
     - String
     - Non
     - Supprimer les journaux anterieurs a cette date (format ISO 8601)
   * - ``user``
     - String
     - Non
     - Supprimer uniquement les journaux d'un utilisateur specifique

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

Obtention des statistiques de recherche
=======================================

Requete
-------

::

    GET /api/admin/searchlog/stats

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
   * - ``interval``
     - String
     - Non
     - Intervalle d'agregation (hour/day/week/month)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalSearches": 50000,
          "uniqueUsers": 1234,
          "averageResponseTime": 156,
          "averageHitCount": 345,
          "zeroHitRate": 0.05,
          "topSearchWords": [
            {"word": "Fess", "count": 1500},
            {"word": "installation", "count": 800},
            {"word": "configuration", "count": 650}
          ],
          "searchesByDate": [
            {"date": "2025-01-29", "count": 2500},
            {"date": "2025-01-28", "count": 2300},
            {"date": "2025-01-27", "count": 2100}
          ]
        }
      }
    }

Exemples d'utilisation
======================

Obtention de la liste des journaux de recherche
-----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention par periode
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?from=2025-01-01T00:00:00Z&to=2025-01-31T23:59:59Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Journaux de recherche d'un utilisateur specifique
-------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?user=user001" \
         -H "Authorization: Bearer YOUR_TOKEN"

Journaux de recherche pour un mot-cle specifique
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?query=Fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention des statistiques de recherche
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31&interval=day" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression des anciens journaux de recherche
---------------------------------------------

.. code-block:: bash

    # Supprimer les journaux de plus de 30 jours
    curl -X DELETE "http://localhost:8080/api/admin/searchlog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraction des mots-cles de recherche populaires
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.topSearchWords'

Analyse de la qualite de recherche
----------------------------------

.. code-block:: bash

    # Verification du taux de zero resultat
    curl -X GET "http://localhost:8080/api/admin/searchlog/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '{zeroHitRate: .response.stats.zeroHitRate, averageHitCount: .response.stats.averageHitCount}'

Evolution du nombre de recherches par jour
------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?interval=day&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.searchesByDate'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-stats` - API des statistiques systeme
- :doc:`../../admin/searchlog-guide` - Guide de gestion des journaux de recherche
- :doc:`../../config/search-analytics` - Guide de configuration de l'analyse de recherche
