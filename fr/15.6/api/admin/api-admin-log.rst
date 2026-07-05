==========================
API Log
==========================

Vue d'ensemble
==============

L'API Log permet d'obtenir les journaux de |Fess|.
Vous pouvez consulter les journaux de recherche, les journaux de clics, les journaux systeme, etc.

URL de base
===========

::

    /api/admin/log

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /search
     - Obtention des journaux de recherche
   * - GET
     - /click
     - Obtention des journaux de clics
   * - GET
     - /favorite
     - Obtention des journaux de favoris
   * - DELETE
     - /search/delete
     - Suppression des journaux de recherche

Obtention des journaux de recherche
===================================

Requete
-------

::

    GET /api/admin/log/search

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

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "log_id_1",
            "queryId": "query_id_1",
            "query": "fess search",
            "requestedAt": "2025-01-29T10:30:00Z",
            "responseTime": 123,
            "hitCount": 567,
            "user": "guest",
            "roles": ["guest"],
            "languages": ["ja"],
            "clientIp": "192.168.1.100",
            "userAgent": "Mozilla/5.0..."
          }
        ],
        "total": 1234
      }
    }

Obtention des journaux de clics
===============================

Requete
-------

::

    GET /api/admin/log/click

Parametres
~~~~~~~~~~

En plus des parametres des journaux de recherche :

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``url``
     - String
     - Non
     - Filtre par URL cliquee
   * - ``queryId``
     - String
     - Non
     - Filtre par ID de requete de recherche

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "click_log_id_1",
            "queryId": "query_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "order": 1,
            "clickedAt": "2025-01-29T10:31:00Z",
            "user": "guest",
            "clientIp": "192.168.1.100"
          }
        ],
        "total": 567
      }
    }

Obtention des journaux de favoris
=================================

Requete
-------

::

    GET /api/admin/log/favorite

Parametres
~~~~~~~~~~

Memes parametres que les journaux de clics

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "favorite_log_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "createdAt": "2025-01-29T10:32:00Z",
            "user": "user123"
          }
        ],
        "total": 123
      }
    }

Suppression des journaux de recherche
=====================================

Requete
-------

::

    DELETE /api/admin/log/search/delete

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
     - Oui
     - Supprimer les journaux anterieurs a cette date (format ISO 8601)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deletedCount": 5678
      }
    }

Exemples d'utilisation
======================

Obtention des journaux de recherche recents
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Journaux de recherche pour une periode
--------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Journaux de recherche pour une requete specifique
-------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?query=fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression des anciens journaux
--------------------------------

.. code-block:: bash

    # Supprimer les journaux de plus de 30 jours
    curl -X DELETE "http://localhost:8080/api/admin/log/search/delete?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-stats` - API des statistiques
- :doc:`../../admin/log-guide` - Guide des journaux
