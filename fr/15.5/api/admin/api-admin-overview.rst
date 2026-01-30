==========================
Vue d'ensemble de l'API Admin
==========================

Vue d'ensemble
==============

L'API d'administration |Fess| est une API RESTful permettant d'acceder aux fonctions d'administration par programmation.
Les configurations de crawl, la gestion des utilisateurs, le controle du planificateur et la plupart des operations disponibles dans l'interface d'administration peuvent etre executees via l'API.

En utilisant cette API, vous pouvez automatiser la configuration de |Fess| ou l'integrer a des systemes externes.

URL de base
===========

L'URL de base de l'API d'administration est au format suivant :

::

    http://<Nom du serveur>/api/admin/

Par exemple, dans un environnement local :

::

    http://localhost:8080/api/admin/

Authentification
================

L'acces a l'API d'administration necessite une authentification par jeton d'acces.

Obtention d'un jeton d'acces
----------------------------

1. Connectez-vous a l'interface d'administration
2. Allez dans "Systeme" -> "Jetons d'acces"
3. Cliquez sur "Nouveau"
4. Entrez un nom de jeton et selectionnez les permissions necessaires
5. Cliquez sur "Creer" pour obtenir le jeton

Utilisation du jeton
--------------------

Incluez le jeton d'acces dans l'en-tete de la requete :

::

    Authorization: Bearer <jeton d'acces>

Ou specifiez-le comme parametre de requete :

::

    ?token=<jeton d'acces>

Exemple cURL
~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Permissions requises
--------------------

Pour utiliser l'API d'administration, le jeton doit avoir les permissions suivantes :

- ``admin-*`` - Acces a toutes les fonctions d'administration
- ``admin-scheduler`` - Gestion du planificateur uniquement
- ``admin-user`` - Gestion des utilisateurs uniquement
- Autres permissions specifiques a chaque fonction

Patterns communs
================

Obtention de la liste (GET/PUT /settings)
-----------------------------------------

Obtient la liste des parametres.

Requete
~~~~~~~

::

    GET /api/admin/<resource>/settings
    PUT /api/admin/<resource>/settings

Parametres (pagination) :

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parametre
     - Type
     - Description
   * - ``size``
     - Integer
     - Nombre d'elements par page (par defaut : 20)
   * - ``page``
     - Integer
     - Numero de page (commence a 0)

Reponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

Obtention d'un parametre unique (GET /setting/{id})
---------------------------------------------------

Obtient un parametre unique en specifiant son ID.

Requete
~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

Reponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

Creation (POST /setting)
------------------------

Cree un nouveau parametre.

Requete
~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

Reponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

Mise a jour (PUT /setting)
--------------------------

Met a jour un parametre existant.

Requete
~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

Reponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

Suppression (DELETE /setting/{id})
----------------------------------

Supprime un parametre.

Requete
~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

Reponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

Format des reponses
===================

Reponse de succes
-----------------

.. code-block:: json

    {
      "response": {
        "status": 0,
        ...
      }
    }

``status: 0`` indique un succes.

Reponse d'erreur
----------------

.. code-block:: json

    {
      "response": {
        "status": 1,
        "errors": [
          {"code": "errors.failed_to_create", "args": ["...", "..."]}
        ]
      }
    }

Codes de statut HTTP
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Requete reussie
   * - 400
     - Parametres de requete invalides
   * - 401
     - Authentification requise (jeton manquant ou invalide)
   * - 403
     - Permission refusee
   * - 404
     - Ressource non trouvee
   * - 500
     - Erreur interne du serveur

APIs disponibles
================

|Fess| fournit les APIs d'administration suivantes.

Configuration du crawl
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-webconfig`
     - Configuration du crawl Web
   * - :doc:`api-admin-fileconfig`
     - Configuration du crawl de fichiers
   * - :doc:`api-admin-dataconfig`
     - Configuration du datastore

Gestion de l'index
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-documents`
     - Operations groupees sur les documents
   * - :doc:`api-admin-crawlinginfo`
     - Informations de crawl
   * - :doc:`api-admin-failureurl`
     - Gestion des URLs en echec
   * - :doc:`api-admin-backup`
     - Sauvegarde/Restauration

Planificateur
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-scheduler`
     - Planification des taches
   * - :doc:`api-admin-joblog`
     - Obtention des journaux de taches

Gestion des utilisateurs et des droits
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-user`
     - Gestion des utilisateurs
   * - :doc:`api-admin-role`
     - Gestion des roles
   * - :doc:`api-admin-group`
     - Gestion des groupes
   * - :doc:`api-admin-accesstoken`
     - Gestion des jetons API

Optimisation de la recherche
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-labeltype`
     - Types de labels
   * - :doc:`api-admin-keymatch`
     - Key Match
   * - :doc:`api-admin-boostdoc`
     - Boost de documents
   * - :doc:`api-admin-elevateword`
     - Mots eleves
   * - :doc:`api-admin-badword`
     - Mots interdits
   * - :doc:`api-admin-relatedcontent`
     - Contenus associes
   * - :doc:`api-admin-relatedquery`
     - Requetes associees
   * - :doc:`api-admin-suggest`
     - Gestion des suggestions

Systeme
-------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-general`
     - Parametres generaux
   * - :doc:`api-admin-systeminfo`
     - Informations systeme
   * - :doc:`api-admin-stats`
     - Statistiques systeme
   * - :doc:`api-admin-log`
     - Obtention des journaux
   * - :doc:`api-admin-storage`
     - Gestion du stockage
   * - :doc:`api-admin-plugin`
     - Gestion des plugins

Dictionnaire
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-dict`
     - Gestion des dictionnaires (synonymes, mots vides, etc.)

Exemples d'utilisation
======================

Creation d'une configuration de crawl Web
-----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "maxAccessCount": 1000,
           "depth": 3,
           "available": true
         }'

Demarrage d'une tache planifiee
-------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention de la liste des utilisateurs
--------------------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`../api-overview` - Vue d'ensemble de l'API
- :doc:`../../admin/accesstoken-guide` - Guide de gestion des jetons d'acces
