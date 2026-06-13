==========================
API JobLog
==========================

Vue d'ensemble
==============

L'API JobLog permet d'obtenir les journaux d'execution des taches de |Fess|.
Vous pouvez consulter l'historique d'execution des taches planifiees et des taches de crawl, ainsi que les informations d'erreur.

URL de base
===========

::

    /api/admin/joblog

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /logs
     - Obtention de la liste des journaux de taches
   * - GET
     - /log/{id}
     - Obtention d'un journal de tache
   * - DELETE
     - /log/{id}
     - Suppression d'un journal de tache

Obtention de la liste des journaux de taches
============================================

Requete
-------

::

    GET /api/admin/joblog/logs

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
     - Nombre d'elements par page
   * - ``page``
     - Integer
     - Non
     - Numero de page

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": 1738116000000,
            "endTime": 1738118723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": 1738029600000,
            "endTime": 1738030215000
          }
        ],
        "total": 100
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID du journal de tache
   * - ``jobName``
     - Nom de la tache
   * - ``jobStatus``
     - Statut de la tache
   * - ``target``
     - Cible d'execution
   * - ``scriptType``
     - Type de script
   * - ``scriptData``
     - Script execute
   * - ``scriptResult``
     - Resultat d'execution
   * - ``startTime``
     - Heure de debut (millisecondes epoch)
   * - ``endTime``
     - Heure de fin (millisecondes epoch)

Obtention d'un journal de tache
===============================

Requete
-------

::

    GET /api/admin/joblog/log/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": 1738116000000,
          "endTime": 1738118723000
        }
      }
    }

Suppression d'un journal de tache
=================================

Requete
-------

::

    DELETE /api/admin/joblog/log/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
======================

Obtention de la liste des journaux de taches
--------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Extraction des taches en echec uniquement
-----------------------------------------

.. code-block:: bash

    # Filtrer les taches en echec avec jq
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

Obtention d'un journal de tache
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'un journal de tache
---------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Calcul du taux de reussite des taches
-------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-scheduler` - API du planificateur
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/joblog-guide` - Guide de gestion des journaux de taches
