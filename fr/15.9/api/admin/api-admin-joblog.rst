==========================
API JobLog
==========================

Vue d'ensemble
==============

L'API JobLog permet de consulter et de gérer les journaux d'exécution des tâches de |Fess|.
Vous pouvez obtenir l'historique d'exécution des tâches planifiées et des tâches de crawl, les résultats d'exécution, les informations d'erreur, et les supprimer.

URL de base
===========

::

    /api/admin/joblog

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /logs
     - Obtention de la liste des journaux de tâches
   * - GET
     - /log/{id}
     - Obtention d'un journal de tâche
   * - DELETE
     - /log/{id}
     - Suppression d'un journal de tâche

Obtention de la liste des journaux de tâches
============================================

Requête
-------

::

    GET /api/admin/joblog/logs

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page (défaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (base 1, défaut : 1)
   * - ``id``
     - String
     - Non
     - Filtre par ID de journal de tâche (correspondance exacte)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "job_name": "Default Crawler",
            "job_status": "ok",
            "target": "all",
            "script_type": "javascript",
            "script_data": "return container.getComponent(\"crawlJob\").execute();",
            "script_result": "Job completed successfully",
            "start_time": "1738116000000",
            "end_time": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "job_name": "Default Crawler",
            "job_status": "fail",
            "target": "all",
            "script_type": "javascript",
            "script_data": "return container.getComponent(\"crawlJob\").execute();",
            "script_result": "Error: Connection timeout",
            "start_time": "1738029600000",
            "end_time": "1738030215000"
          }
        ],
        "total": 100
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID du journal de tâche
   * - ``job_name``
     - Nom de la tâche
   * - ``job_status``
     - Statut de la tâche (``ok`` : succès, ``fail`` : échec, ``running`` : en cours d'exécution)
   * - ``target``
     - Cible d'exécution (nom de la cible du planificateur ; valeur par défaut : ``all``)
   * - ``script_type``
     - Type de script (ex. : ``javascript``)
   * - ``script_data``
     - Script exécuté
   * - ``script_result``
     - Résultat d'exécution
   * - ``start_time``
     - Heure de début (millisecondes epoch ; retournée sous forme de chaîne)
   * - ``end_time``
     - Heure de fin (millisecondes epoch ; retournée sous forme de chaîne). Non retournée pour les tâches en cours d'exécution.

.. note::

   Chaque objet de journal dans la réponse inclut également un champ interne ``crud_mode``
   (un entier indiquant le mode d'opération CRUD, toujours ``0`` pour les opérations de lecture).
   Les clients peuvent l'ignorer en toute sécurité.

Obtention d'un journal de tâche
================================

Requête
-------

::

    GET /api/admin/joblog/log/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "job_name": "Default Crawler",
          "job_status": "ok",
          "target": "all",
          "script_type": "javascript",
          "script_data": "return container.getComponent(\"crawlJob\").execute();",
          "script_result": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "start_time": "1738116000000",
          "end_time": "1738118723000"
        }
      }
    }

Si le journal de tâche correspondant à l'ID spécifié n'existe pas, une réponse d'erreur
est retournée avec une valeur différente de 0 dans ``status``.

Suppression d'un journal de tâche
==================================

Requête
-------

::

    DELETE /api/admin/joblog/log/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Si le journal de tâche correspondant à l'ID spécifié n'existe pas, une réponse d'erreur
est retournée avec une valeur différente de 0 dans ``status``.

Exemples d'utilisation
======================

Obtention de la liste des journaux de tâches
--------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

Extraction des tâches en échec uniquement
-----------------------------------------

.. code-block:: bash

    # Filtrer les taches en echec avec jq
    curl -X GET "http://localhost:8080/api/admin/joblog/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 1000}' | \
         jq '.response.logs[] | select(.job_status=="fail")'

Obtention d'un journal de tâche
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'un journal de tâche
----------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Calcul du taux de réussite des tâches
--------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 1000}' | \
         jq '.response.logs | {total: length, ok: [.[] | select(.job_status=="ok")] | length, fail: [.[] | select(.job_status=="fail")] | length}'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-scheduler` - API du planificateur
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/joblog-guide` - Guide de gestion des journaux de tâches
