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
   * - GET
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
     - Nombre d'elements par page (defaut : 25 ; configurable via ``paging.page.size`` dans ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numero de page (base 1 ; defaut : 1)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

   L'objet ``response`` contient toujours ``version`` (version du produit) et ``status`` (code de resultat). Consultez :doc:`api-admin-overview` pour le format de reponse commun. Les exemples suivants peuvent omettre ``version`` par souci de concision.

.. note::

   Dans les reponses, ``jobLogging`` / ``crawler`` / ``available`` sont retournes sous forme de chaines de caracteres (``"true"`` / ``"false"``). ``running`` est un champ booleen, specifique aux reponses, indiquant si la tache est en cours d'execution (ne peut pas etre specifie dans les requetes). ``total`` est le nombre total de taches correspondant a la requete.

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
          "jobLogging": "true",
          "crawler": "true",
          "available": "true",
          "sortOrder": 0,
          "versionNo": 1,
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
     - Nom de la tache (max 100 caracteres)
   * - ``target``
     - Oui
     - Cible d'execution (max 100 caracteres). Specifier ``all`` ou un nom de cible specifique
   * - ``cronExpression``
     - Non
     - Expression Cron (seconde minute heure jour mois jour-semaine). Max 100 caracteres, validee en tant qu'expression cron. Si vide, la tache n'est pas planifiee et ne peut etre demarree que manuellement
   * - ``scriptType``
     - Oui
     - Type de script (max 100 caracteres). Actuellement seul ``groovy`` est supporte
   * - ``scriptData``
     - Non
     - Script a executer. La taille maximale est definie par ``form.admin.max.input.size`` dans ``fess_config.properties``
   * - ``jobLogging``
     - Non
     - Activer la journalisation des taches (chaine)
   * - ``crawler``
     - Non
     - S'il s'agit d'une tache de crawl (chaine)
   * - ``available``
     - Non
     - Active/Desactive (chaine)
   * - ``sortOrder``
     - Oui
     - Ordre d'affichage (entier entre 0 et 2147483647)

.. note::

   ``jobLogging`` / ``crawler`` / ``available`` sont des champs de type chaine. Dans les requetes, specifier ``"on"`` ou ``"true"`` (insensible a la casse) les active ; toute autre valeur (``"false"``, chaine vide ou non specifie) est traitee comme desactivee. Dans les reponses, ils sont retournes sous la forme ``"true"`` / ``"false"``.

.. note::

   ``crudMode`` est defini automatiquement cote serveur et n'a pas besoin d'etre specifie dans les requetes. Les champs d'audit tels que ``createdBy`` / ``createdTime`` sont egalement definis cote serveur.

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
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1,
      "versionNo": 1
    }

.. note::

   Pour les mises a jour, ``id`` (max 1000 caracteres) et ``versionNo`` sont obligatoires. ``versionNo`` est utilise pour le verrouillage optimiste ; specifier la valeur retournee dans la reponse de recuperation. Si la valeur ne correspond pas, la mise a jour echoue. Les autres champs obligatoires (``name`` / ``target`` / ``scriptType`` / ``sortOrder``) sont identiques a ceux de la creation.

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
        "status": 0,
        "jobLogId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``jobLogId``
     - ID du journal de la tache demarree. Emis lorsque la journalisation des taches est activee. Vaut ``null`` lorsque la journalisation des taches est desactivee.

Notes
-----

- Si la tache est deja en cours d'execution, le demarrage echoue et une erreur est retournee (``status`` different de ``0``).
- Si la tache est desactivee (``available`` n'est pas active), le demarrage echoue egalement avec une erreur.
- ``jobLogId`` est emis uniquement lorsque la journalisation des taches est activee (``jobLogging`` est active).

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
           "jobLogging": "true",
           "crawler": "true",
           "available": "true",
           "sortOrder": 1
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
