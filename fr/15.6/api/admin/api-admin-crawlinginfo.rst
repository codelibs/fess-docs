==========================
API CrawlingInfo
==========================

Vue d'ensemble
==============

L'API CrawlingInfo permet d'obtenir les informations de crawl de |Fess|.
Vous pouvez consulter l'etat des sessions de crawl, la progression et les statistiques.

URL de base
===========

::

    /api/admin/crawlinginfo

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
     - Obtention de la liste des informations de crawl
   * - GET
     - /{sessionId}
     - Obtention des details d'une session de crawl
   * - DELETE
     - /{sessionId}
     - Suppression d'une session de crawl

Obtention de la liste des informations de crawl
===============================================

Requete
-------

::

    GET /api/admin/crawlinginfo

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

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``sessionId``
     - ID de la session
   * - ``name``
     - Nom du crawler
   * - ``status``
     - Statut (running/completed/failed)
   * - ``startTime``
     - Heure de debut
   * - ``endTime``
     - Heure de fin
   * - ``crawlingInfoCount``
     - Nombre d'informations de crawl
   * - ``createdDocCount``
     - Nombre de documents crees
   * - ``updatedDocCount``
     - Nombre de documents mis a jour
   * - ``deletedDocCount``
     - Nombre de documents supprimes

Obtention des details d'une session de crawl
============================================

Requete
-------

::

    GET /api/admin/crawlinginfo/{sessionId}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

Suppression d'une session de crawl
==================================

Requete
-------

::

    DELETE /api/admin/crawlinginfo/{sessionId}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

Exemples d'utilisation
======================

Obtention de la liste des informations de crawl
-----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention des sessions de crawl en cours
----------------------------------------

.. code-block:: bash

    # Recuperer toutes les sessions et filtrer celles en cours
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

Obtention des details d'une session specifique
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'une ancienne session
----------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

Surveillance de la progression
------------------------------

.. code-block:: bash

    # Verifier periodiquement la progression de la session en cours
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-failureurl` - API des URLs en echec
- :doc:`api-admin-joblog` - API des journaux de taches
- :doc:`../../admin/crawlinginfo-guide` - Guide des informations de crawl
