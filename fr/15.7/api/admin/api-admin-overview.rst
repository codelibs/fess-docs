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

Les ressources possedant des parametres (webconfig, user, role, etc.) suivent le
pattern CRUD commun ci-dessous. Toutefois, certaines ressources (systeminfo, stats,
storage, plugin, log, backup, documents, suggest, racine dict, etc.) disposent d'une
structure d'endpoints propre, differente de ce pattern commun ; reportez-vous a la
page de chaque ressource.

Obtention de la liste (GET /settings)
-------------------------------------

Obtient la liste des parametres.

Requete
~~~~~~~

::

    GET /api/admin/<resource>/settings

Parametres (pagination) :

.. list-table::
   :header-rows: 1
   :widths: 20 15.75

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
        "version": "15.7.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   L'objet ``response`` de toutes les reponses contient toujours ``version``
   (par exemple ``"15.7.0"``), indiquant la version du produit. Dans les exemples
   suivants, il peut etre omis par souci de concision.

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

Le format de la reponse de suppression varie selon la ressource (l'action). De
nombreuses ressources ne retournent que ``status``.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Pour certaines ressources, le resultat de la suppression est retourne sous forme
de ``ApiUpdateResponse``, avec l'``id`` du parametre supprime et ``created``
(``false`` lors d'une suppression).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

De plus, pour les ressources qui retournent un ``ApiDeleteResponse``, un champ
``count`` indiquant le nombre d'elements supprimes (valeur par defaut ``1``) peut
etre ajoute. Reportez-vous a la page de chaque ressource pour le format exact.

Format des reponses
===================

Toutes les reponses sont encapsulees dans un objet ``response`` et contiennent
toujours ``version``, indiquant la version du produit, ainsi que ``status``,
indiquant le resultat du traitement.

Les valeurs de ``status`` sont les suivantes.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Valeur
     - Description
   * - ``0``
     - OK (succes)
   * - ``1``
     - BAD_REQUEST (requete invalide)
   * - ``2``
     - SYSTEM_ERROR (erreur systeme)
   * - ``3``
     - UNAUTHORIZED (erreur d'authentification)
   * - ``9``
     - FAILED (echec du traitement)

Reponse de succes
-----------------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` indique un succes.

Reponse d'erreur
----------------

En cas d'erreur, ``status`` est defini sur une valeur differente de 0 et
``message`` contient le message d'erreur.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to process the request."
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

.. note::

   Outre celles-ci, les ressources suivantes relatives aux informations
   d'authentification et au controle du crawl sont egalement fournies en tant
   qu'API (pour l'instant, aucune page dediee n'est disponible) : ``webauth``
   (authentification Web), ``fileauth`` (authentification de fichiers),
   ``reqheader`` (en-tetes de requete), ``pathmap`` (mappage de chemins),
   ``duplicatehost`` (hotes en double), ``searchlist`` (operations de
   recherche/liste de documents).

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
   * - :doc:`api-admin-searchlist`
     - Recherche et gestion des documents
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
