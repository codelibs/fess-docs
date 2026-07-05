==========================
API Scheduler
==========================

Vue d'ensemble
==============

L'API Scheduler permet de gerer les taches planifiees de |Fess|.
Vous pouvez demarrer/arreter les taches de crawl, creer/modifier/supprimer des configurations de planification, etc.

URL de base
===========

::

    /api/admin/scheduler

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET/PUT
     - /settings
     - Obtention de la liste des taches planifiees
   * - GET
     - /setting/{id}
     - Obtention d'une tache planifiee
   * - POST
     - /setting
     - Creation d'une tache planifiee
   * - PUT
     - /setting
     - Mise a jour d'une tache planifiee
   * - DELETE
     - /setting/{id}
     - Suppression d'une tache planifiee
   * - PUT
     - /{id}/start
     - Demarrage d'une tache
   * - PUT
     - /{id}/stop
     - Arret d'une tache

Obtention de la liste des taches planifiees
===========================================

Requete
-------

::

    GET /api/admin/scheduler/settings
    PUT /api/admin/scheduler/settings

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
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": true,
            "crawler": true,
            "available": true,
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

Obtention d'une tache planifiee
===============================

Requete
-------

::

    GET /api/admin/scheduler/setting/{id}

Reponse
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
          "jobLogging": true,
          "crawler": true,
          "available": true,
          "sortOrder": 0,
          "running": false
        }
      }
    }

Creation d'une tache planifiee
==============================

Requete
-------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": true,
      "crawler": true,
      "available": true,
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
     - Nom de la tache
   * - ``target``
     - Oui
     - Cible d'execution ("all" ou cible specifique)
   * - ``cronExpression``
     - Oui
     - Expression Cron (secondes minutes heures jour mois jour-semaine)
   * - ``scriptType``
     - Oui
     - Type de script ("groovy")
   * - ``scriptData``
     - Oui
     - Script a executer
   * - ``jobLogging``
     - Non
     - Activer la journalisation (par defaut : true)
   * - ``crawler``
     - Non
     - S'il s'agit d'une tache de crawl (par defaut : false)
   * - ``available``
     - Non
     - Active/Desactive (par defaut : true)
   * - ``sortOrder``
     - Non
     - Ordre d'affichage

Reponse
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
     - Execution tous les jours a 2h du matin
   * - ``0 0 0/6 * * ?``
     - Execution toutes les 6 heures
   * - ``0 0 2 * * MON``
     - Execution tous les lundis a 2h du matin
   * - ``0 0 2 1 * ?``
     - Execution le 1er de chaque mois a 2h du matin

Mise a jour d'une tache planifiee
=================================

Requete
-------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1,
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

Suppression d'une tache planifiee
=================================

Requete
-------

::

    DELETE /api/admin/scheduler/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

Demarrage d'une tache
=====================

Execute immediatement une tache planifiee.

Requete
-------

::

    PUT /api/admin/scheduler/{id}/start

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Notes
-----

- Une erreur est retournee si la tache est deja en cours d'execution
- Une erreur est retournee si la tache est desactivee (``available: false``)

Arret d'une tache
=================

Arrete une tache en cours d'execution.

Requete
-------

::

    PUT /api/admin/scheduler/{id}/stop

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

Creation et execution d'une tache de crawl
------------------------------------------

.. code-block:: bash

    # Creer la tache
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": true,
           "crawler": true,
           "available": true
         }'

    # Executer la tache immediatement
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verification de l'etat des taches
---------------------------------

.. code-block:: bash

    # Verifier l'etat de toutes les taches
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Le champ running indique si la tache est en cours d'execution

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-joblog` - API des journaux de taches
- :doc:`../../admin/scheduler-guide` - Guide de gestion du planificateur
