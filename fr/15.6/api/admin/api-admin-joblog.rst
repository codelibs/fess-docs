==========================
API JobLog
==========================

Vue d'ensemble
==============

L'API JobLog permet d'obtenir les journaux d'execution des taches de |Fess|.
Vous pouvez consulter l'historique d'execution des taches planifiees et des taches de crawl, les informations d'erreur, etc.

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
     - /
     - Obtention de la liste des journaux de taches
   * - GET
     - /{id}
     - Obtention des details d'un journal de tache
   * - DELETE
     - /{id}
     - Suppression d'un journal de tache
   * - DELETE
     - /delete-all
     - Suppression de tous les journaux de taches

Obtention de la liste des journaux de taches
============================================

Requete
-------

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - Non
     - Filtre par statut (ok/fail/running)
   * - ``from``
     - String
     - Non
     - Date/heure de debut (format ISO 8601)
   * - ``to``
     - String
     - Non
     - Date/heure de fin (format ISO 8601)

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
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
          }
        ],
        "total": 100
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
     - ID du journal de tache
   * - ``jobName``
     - Nom de la tache
   * - ``jobStatus``
     - Statut de la tache (ok/fail/running)
   * - ``target``
     - Cible d'execution
   * - ``scriptType``
     - Type de script
   * - ``scriptData``
     - Script execute
   * - ``scriptResult``
     - Resultat de l'execution
   * - ``startTime``
     - Heure de debut
   * - ``endTime``
     - Heure de fin
   * - ``executionTime``
     - Temps d'execution (millisecondes)

Obtention des details d'un journal de tache
===========================================

Requete
-------

::

    GET /api/admin/joblog/{id}

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
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

Suppression d'un journal de tache
=================================

Requete
-------

::

    DELETE /api/admin/joblog/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

Suppression de tous les journaux de taches
==========================================

Requete
-------

::

    DELETE /api/admin/joblog/delete-all

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
     - Supprimer les journaux anterieurs a cette date/heure (format ISO 8601)
   * - ``status``
     - String
     - Non
     - Supprimer uniquement les journaux avec ce statut

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

Exemples d'utilisation
======================

Obtention de la liste des journaux de taches
--------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention des taches echouees uniquement
----------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Journaux de taches pour une periode specifique
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention des details d'un journal de tache
-------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression des anciens journaux de taches
------------------------------------------

.. code-block:: bash

    # Supprimer les journaux de plus de 30 jours
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression des journaux de taches echouees uniquement
------------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

Detection des taches longues
----------------------------

.. code-block:: bash

    # Extraire les taches ayant dure plus d'une heure
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

Calcul du taux de succes des taches
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-scheduler` - API du planificateur
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/joblog-guide` - Guide de gestion des journaux de taches
