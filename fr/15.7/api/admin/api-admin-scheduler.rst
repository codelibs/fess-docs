==========================
API Scheduler
==========================

Vue d'ensemble
==============

L'API Scheduler permet de gérer les tâches planifiées de |Fess|.
Vous pouvez démarrer/arrêter les tâches de crawl, créer/modifier/supprimer des configurations de planification, etc.

URL de base
===========

::

    /api/admin/scheduler

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /settings
     - Obtention de la liste des tâches planifiées
   * - GET
     - /setting/{id}
     - Obtention d'une tâche planifiée
   * - POST
     - /setting
     - Création d'une tâche planifiée
   * - PUT
     - /setting
     - Mise à jour d'une tâche planifiée
   * - DELETE
     - /setting/{id}
     - Suppression d'une tâche planifiée
   * - PUT
     - /{id}/start
     - Démarrage d'une tâche
   * - PUT
     - /{id}/stop
     - Arrêt d'une tâche

Obtention de la liste des tâches planifiées
===========================================

Requête
-------

::

    GET /api/admin/scheduler/settings

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
     - Nombre d'éléments par page (défaut : 25 ; configurable via ``paging.page.size`` dans ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (base 1 ; défaut : 1)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": "true",
            "crawler": "true",
            "available": "true",
            "sortOrder": 0,
            "versionNo": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   L'objet ``response`` contient toujours ``version`` (version du produit) et ``status`` (code de résultat). Consultez :doc:`api-admin-overview` pour le format de réponse commun. Les exemples suivants peuvent omettre ``version`` par souci de concision.

.. note::

   Dans les réponses, ``jobLogging`` / ``crawler`` / ``available`` sont retournés sous forme de chaînes de caractères (``"true"`` / ``"false"``). ``running`` est un champ booléen, spécifique aux réponses, indiquant si la tâche est en cours d'exécution (ne peut pas être spécifié dans les requêtes). ``total`` est le nombre total de tâches correspondant à la requête.

Obtention d'une tâche planifiée
===============================

Requête
-------

::

    GET /api/admin/scheduler/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cronExpression": "0 0 0 * * ?",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "jobLogging": "true",
          "crawler": "true",
          "available": "true",
          "sortOrder": 0,
          "versionNo": 1,
          "running": false
        }
      }
    }

Création d'une tâche planifiée
==============================

Requête
-------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom de la tâche (max 100 caractères)
   * - ``target``
     - Oui
     - Cible d'exécution (max 100 caractères). Spécifier ``all`` ou un nom de cible spécifique
   * - ``cronExpression``
     - Non
     - Expression Cron (seconde minute heure jour mois jour-semaine). Max 100 caractères, validée en tant qu'expression cron. Si vide, la tâche n'est pas planifiée et ne peut être démarrée que manuellement
   * - ``scriptType``
     - Oui
     - Type de script (max 100 caractères). Actuellement seul ``groovy`` est supporté
   * - ``scriptData``
     - Non
     - Script à exécuter. La taille maximale est définie par ``form.admin.max.input.size`` dans ``fess_config.properties``
   * - ``jobLogging``
     - Non
     - Activer la journalisation des tâches (chaîne)
   * - ``crawler``
     - Non
     - S'il s'agit d'une tâche de crawl (chaîne)
   * - ``available``
     - Non
     - Activé/Désactivé (chaîne)
   * - ``sortOrder``
     - Oui
     - Ordre d'affichage (entier entre 0 et 2147483647)

.. note::

   ``jobLogging`` / ``crawler`` / ``available`` sont des champs de type chaîne. Dans les requêtes, spécifier ``"on"`` ou ``"true"`` (insensible à la casse) les active ; toute autre valeur (``"false"``, chaîne vide ou non spécifié) est traitée comme désactivée. Dans les réponses, ils sont retournés sous la forme ``"true"`` / ``"false"``.

.. note::

   ``crudMode`` est défini automatiquement côté serveur et n'a pas besoin d'être spécifié dans les requêtes. Les champs d'audit tels que ``createdBy`` / ``createdTime`` sont également définis côté serveur.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Exemples d'expressions Cron
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Expression Cron
     - Description
   * - ``0 0 2 * * ?``
     - Exécution tous les jours à 2h du matin
   * - ``0 0 0/6 * * ?``
     - Exécution toutes les 6 heures
   * - ``0 0 2 * * MON``
     - Exécution tous les lundis à 2h du matin
   * - ``0 0 2 1 * ?``
     - Exécution le 1er de chaque mois à 2h du matin

Mise à jour d'une tâche planifiée
=================================

Requête
-------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1,
      "versionNo": 1
    }

.. note::

   Pour les mises à jour, ``id`` (max 1000 caractères) et ``versionNo`` sont obligatoires. ``versionNo`` est utilisé pour le verrouillage optimiste ; spécifier la valeur retournée dans la réponse de récupération. Si la valeur ne correspond pas, la mise à jour échoue. Les autres champs obligatoires (``name`` / ``target`` / ``scriptType`` / ``sortOrder``) sont identiques à ceux de la création.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

Suppression d'une tâche planifiée
=================================

Requête
-------

::

    DELETE /api/admin/scheduler/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

Démarrage d'une tâche
=====================

Exécute immédiatement une tâche planifiée.

Requête
-------

::

    PUT /api/admin/scheduler/{id}/start

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "jobLogId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``jobLogId``
     - ID du journal de la tâche démarrée. Émis lorsque la journalisation des tâches est activée. Vaut ``null`` lorsque la journalisation des tâches est désactivée.

Notes
-----

- Si la tâche est déjà en cours d'exécution, le démarrage échoue et une erreur est retournée (``status`` différent de ``0``).
- Si la tâche est désactivée (``available`` n'est pas activé), le démarrage échoue également avec une erreur.
- ``jobLogId`` est émis uniquement lorsque la journalisation des tâches est activée (``jobLogging`` est activé).

Arrêt d'une tâche
=================

Arrête une tâche en cours d'exécution.

Requête
-------

::

    PUT /api/admin/scheduler/{id}/stop

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
======================

Création et exécution d'une tâche de crawl
------------------------------------------

.. code-block:: bash

    # Créer la tâche
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": "true",
           "crawler": "true",
           "available": "true",
           "sortOrder": 1
         }'

    # Exécuter la tâche immédiatement
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Vérification de l'état des tâches
---------------------------------

.. code-block:: bash

    # Vérifier l'état de toutes les tâches
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Le champ running indique si la tâche est en cours d'exécution

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-joblog` - API des journaux de tâches
- :doc:`../../admin/scheduler-guide` - Guide de gestion du planificateur
