=============================
Vue d'ensemble de l'API Admin
=============================

Vue d'ensemble
==============

L'API d'administration |Fess| est une API RESTful permettant d'accéder aux fonctions d'administration par programmation.
Les configurations de crawl, la gestion des utilisateurs, le contrôle du planificateur et la plupart des opérations disponibles dans l'interface d'administration peuvent être exécutées via l'API.

En utilisant cette API, vous pouvez automatiser la configuration de |Fess| ou l'intégrer à des systèmes externes.

URL de base
===========

L'URL de base de l'API d'administration est au format suivant :

::

    http://<Nom du serveur>/api/admin/

Par exemple, dans un environnement local :

::

    http://localhost:8080/api/admin/

Authentification
=================

L'accès à l'API d'administration nécessite une authentification par jeton d'accès.

Obtention d'un jeton d'accès
-----------------------------

1. Connectez-vous à l'interface d'administration
2. Allez dans "Système" -> "Jetons d'accès"
3. Cliquez sur "Nouveau"
4. Entrez un nom de jeton et définissez, dans le champ "Permissions", les permissions à accorder au jeton (pour utiliser l'API d'administration, saisissez ``{role}admin-api``)
5. Cliquez sur "Créer" pour obtenir le jeton

Utilisation du jeton
---------------------

Incluez le jeton d'accès dans l'en-tête de la requête :

::

    Authorization: Bearer <jeton d'accès>

Vous pouvez aussi omettre ``Bearer`` et ne spécifier que le jeton :

::

    Authorization: <jeton d'accès>

La spécification via un paramètre de requête est également possible, mais elle est désactivée par défaut. Si vous définissez un nom de paramètre dans ``api.access.token.request.parameter`` du fichier ``fess_config.properties``, vous pourrez transmettre le jeton sous ce nom (la valeur par défaut étant vide, seule la spécification par en-tête est active). Par exemple, si vous définissez ``api.access.token.request.parameter=token`` :

::

    ?token=<jeton d'accès>

Exemple cURL
~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Permissions requises
---------------------

L'accès à l'API d'administration n'est pas contrôlé par fonction, mais par un unique jeu de permissions. Pour utiliser l'un quelconque des endpoints de l'API d'administration, le jeton d'accès doit s'être vu accorder l'une des permissions définies dans ``api.admin.access.permissions`` du fichier ``fess_config.properties``.

La valeur par défaut est ``Radmin-api``, qui est la forme encodée du rôle ``admin-api`` (le ``R`` initial est la valeur de ``role.search.role.prefix``). Lors de la création du jeton d'accès, si vous saisissez ``{role}admin-api`` dans le champ des permissions, il est enregistré en interne sous la forme ``Radmin-api``.

.. note::

   Il n'existe pas de permissions distinctes par ressource (telles que ``admin-scheduler`` ou ``admin-user``), ni de caractère générique (``admin-*``). Un jeton disposant de la permission configurée peut accéder à tous les endpoints de l'API d'administration. Si vous souhaitez modifier les permissions qui autorisent l'accès, changez la valeur de ``api.admin.access.permissions``.

Patterns communs
=================

Les ressources possédant des paramètres (webconfig, user, role, etc.) suivent le
pattern CRUD commun ci-dessous. Toutefois, certaines ressources (systeminfo, stats,
storage, plugin, log, backup, documents, suggest, racine dict, etc.) disposent d'une
structure d'endpoints propre, différente de ce pattern commun ; reportez-vous à la
page de chaque ressource.

Obtention de la liste (GET /settings)
---------------------------------------

Obtient la liste des paramètres.

Requête
~~~~~~~

::

    GET /api/admin/<resource>/settings

Paramètres (pagination) :

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Paramètre
     - Type
     - Description
   * - ``size``
     - Integer
     - Nombre d'éléments par page (par défaut : 25 ; modifiable via ``paging.page.size`` du fichier ``fess_config.properties``)
   * - ``page``
     - Integer
     - Numéro de page (commence à 1 ; par défaut : 1 ; une valeur inférieure ou égale à 0 est traitée comme 1)

Réponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   L'objet ``response`` de toutes les réponses contient toujours ``version``
   (par exemple ``"15.8.0"``), indiquant la version du produit. Dans les exemples
   suivants, il peut être omis par souci de concision.

Obtention d'un paramètre unique (GET /setting/{id})
-----------------------------------------------------

Obtient un paramètre unique en spécifiant son ID.

Requête
~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

Réponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

Création (POST /setting)
--------------------------

Crée un nouveau paramètre.

Requête
~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

Réponse
~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

Mise à jour (PUT /setting)
-----------------------------

Met à jour un paramètre existant.

Requête
~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

Réponse
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
--------------------------------------

Supprime un paramètre.

Requête
~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

Réponse
~~~~~~~

Le format de la réponse de suppression varie selon la ressource (l'action). De
nombreuses ressources ne retournent que ``status``.

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Pour certaines ressources, le résultat de la suppression est retourné sous forme
de ``ApiUpdateResponse``, avec l'``id`` du paramètre supprimé et ``created``
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
``count`` indiquant le nombre d'éléments supprimés (valeur par défaut ``1``) peut
être ajouté. Reportez-vous à la page de chaque ressource pour le format exact.

Format des réponses
=====================

Toutes les réponses sont encapsulées dans un objet ``response`` et contiennent
toujours ``version``, indiquant la version du produit, ainsi que ``status``,
indiquant le résultat du traitement.

Les valeurs de ``status`` sont les suivantes.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Valeur
     - Description
   * - ``0``
     - OK (succès)
   * - ``1``
     - BAD_REQUEST (requête invalide)
   * - ``2``
     - SYSTEM_ERROR (erreur système)
   * - ``3``
     - UNAUTHORIZED (erreur d'authentification)
   * - ``9``
     - FAILED (échec du traitement)

Réponse de succès
--------------------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` indique un succès.

Réponse d'erreur
--------------------

En cas d'erreur, ``status`` est défini sur une valeur différente de 0 et
``message`` contient le message d'erreur.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

Codes de statut HTTP
----------------------

L'API d'administration retourne dans la plupart des cas le statut HTTP ``200``, et
le résultat du traitement est exprimé par le champ ``status`` du corps de la réponse.
Par conséquent, déterminez le succès ou l'échec non pas à partir du code de statut HTTP,
mais à partir de la valeur de ``status`` dans le corps.

Les codes de statut HTTP réellement retournés sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Réponse normale. Outre les cas de succès (``status: 0``), la plupart des erreurs
       sont également retournées avec ce code. Par exemple, si le jeton d'accès est absent
       ou invalide, ou si les permissions sont insuffisantes, ``status: 3`` est retourné ;
       une erreur système renvoie ``status: 2`` ; dans tous ces cas avec le statut HTTP ``200``.
   * - 400
     - Erreur de validation des paramètres de requête. Le ``status`` du corps de la réponse
       est ``1``. Ce code est également retourné lorsque l'on tente d'obtenir une ressource
       inexistante.
   * - 401
     - Lorsqu'une exception liée à l'authentification de connexion se produit. Le ``status``
       du corps de la réponse est ``3``. À noter que si le jeton d'accès est absent ou
       invalide, ce n'est pas ce code qui est retourné, mais le statut HTTP ``200`` avec
       ``status: 3``.

.. note::

   L'API d'administration ne retourne pas de codes de statut HTTP tels que ``403``,
   ``404`` ou ``500``. L'insuffisance de permissions et l'inexistence d'une ressource
   sont également indiquées par le ``status`` contenu dans le corps de la réponse HTTP
   ``200`` ou ``400``.

APIs disponibles
==================

|Fess| fournit les APIs d'administration suivantes.

Configuration du crawl
------------------------

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
   d'authentification et au contrôle du crawl sont également fournies en tant
   qu'API (pour l'instant, aucune page dédiée n'est disponible) : ``webauth``
   (authentification Web), ``fileauth`` (authentification de fichiers),
   ``reqheader`` (en-têtes de requête), ``pathmap`` (mappage de chemins),
   ``duplicatehost`` (hôtes en double), ``searchlist`` (opérations de
   recherche/liste de documents).

Gestion de l'index
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-documents`
     - Opérations groupées sur les documents
   * - :doc:`api-admin-crawlinginfo`
     - Informations de crawl
   * - :doc:`api-admin-failureurl`
     - Gestion des URLs en échec
   * - :doc:`api-admin-backup`
     - Sauvegarde/Restauration

Planificateur
===============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-scheduler`
     - Planification des tâches
   * - :doc:`api-admin-joblog`
     - Obtention des journaux de tâches

Gestion des utilisateurs et des droits
=========================================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-user`
     - Gestion des utilisateurs
   * - :doc:`api-admin-role`
     - Gestion des rôles
   * - :doc:`api-admin-group`
     - Gestion des groupes
   * - :doc:`api-admin-accesstoken`
     - Gestion des jetons API

Optimisation de la recherche
===============================

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
     - Mots élevés
   * - :doc:`api-admin-badword`
     - Mots interdits
   * - :doc:`api-admin-relatedcontent`
     - Contenus associés
   * - :doc:`api-admin-relatedquery`
     - Requêtes associées
   * - :doc:`api-admin-suggest`
     - Gestion des suggestions

Système
=========

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-general`
     - Paramètres généraux
   * - :doc:`api-admin-systeminfo`
     - Informations système
   * - :doc:`api-admin-stats`
     - Statistiques système
   * - :doc:`api-admin-log`
     - Obtention des journaux
   * - :doc:`api-admin-searchlist`
     - Recherche et gestion des documents
   * - :doc:`api-admin-storage`
     - Gestion du stockage
   * - :doc:`api-admin-plugin`
     - Gestion des plugins

Dictionnaire
==============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Endpoint
     - Description
   * - :doc:`api-admin-dict`
     - Gestion des dictionnaires (synonymes, mots vides, etc.)

Exemples d'utilisation
========================

Création d'une configuration de crawl Web
---------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "userAgent": "Mozilla/5.0 (compatible; Fess)",
           "numOfThread": 1,
           "intervalTime": 1000,
           "boost": 1.0,
           "maxAccessCount": 1000,
           "depth": 3,
           "sortOrder": 1,
           "available": "true"
         }'

.. note::

   Pour la création d'une configuration de crawl Web, les champs ``name``, ``urls``,
   ``userAgent``, ``numOfThread``, ``intervalTime``, ``boost``, ``available`` et
   ``sortOrder`` sont obligatoires. Les omettre provoque une erreur de validation
   (``status: 1``). ``available`` se spécifie sous forme de chaîne de caractères,
   en y plaçant ``"true"`` ou ``"false"``.

Démarrage d'une tâche planifiée
-----------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention de la liste des utilisateurs
------------------------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complémentaires
===============================

- :doc:`../api-overview` - Vue d'ensemble de l'API
- :doc:`../../admin/accesstoken-guide` - Guide de gestion des jetons d'accès
