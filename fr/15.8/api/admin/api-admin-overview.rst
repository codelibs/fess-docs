=============================
Vue d'ensemble de l'API Admin
=============================

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
4. Entrez un nom de jeton et definissez, dans le champ "Permissions", les permissions a accorder au jeton (pour utiliser l'API d'administration, saisissez ``{role}admin-api``)
5. Cliquez sur "Creer" pour obtenir le jeton

Utilisation du jeton
--------------------

Incluez le jeton d'acces dans l'en-tete de la requete :

::

    Authorization: Bearer <jeton d'acces>

Vous pouvez aussi omettre ``Bearer`` et ne specifier que le jeton :

::

    Authorization: <jeton d'acces>

La specification via un parametre de requete est egalement possible, mais elle est desactivee par defaut. Si vous definissez un nom de parametre dans ``api.access.token.request.parameter`` du fichier ``fess_config.properties``, vous pourrez transmettre le jeton sous ce nom (la valeur par defaut etant vide, seule la specification par en-tete est active). Par exemple, si vous definissez ``api.access.token.request.parameter=token`` :

::

    ?token=<jeton d'acces>

Exemple cURL
~~~~~~~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

Permissions requises
--------------------

L'acces a l'API d'administration n'est pas controle par fonction, mais par un unique jeu de permissions. Pour utiliser l'un quelconque des endpoints de l'API d'administration, le jeton d'acces doit s'etre vu accorder l'une des permissions definies dans ``api.admin.access.permissions`` du fichier ``fess_config.properties``.

La valeur par defaut est ``Radmin-api``, qui est la forme encodee du role ``admin-api`` (le ``R`` initial est la valeur de ``role.search.role.prefix``). Lors de la creation du jeton d'acces, si vous saisissez ``{role}admin-api`` dans le champ des permissions, il est enregistre en interne sous la forme ``Radmin-api``.

.. note::

   Il n'existe pas de permissions distinctes par ressource (telles que ``admin-scheduler`` ou ``admin-user``), ni de caractere generique (``admin-*``). Un jeton disposant de la permission configuree peut acceder a tous les endpoints de l'API d'administration. Si vous souhaitez modifier les permissions qui autorisent l'acces, changez la valeur de ``api.admin.access.permissions``.

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
   :widths: 20 15 65

   * - Parametre
     - Type
     - Description
   * - ``size``
     - Integer
     - Nombre d'elements par page (par defaut : 25 ; modifiable via ``paging.page.size`` du fichier ``fess_config.properties``)
   * - ``page``
     - Integer
     - Numero de page (commence a 1 ; par defaut : 1 ; une valeur inferieure ou egale a 0 est traitee comme 1)

Reponse
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

   L'objet ``response`` de toutes les reponses contient toujours ``version``
   (par exemple ``"15.8.0"``), indiquant la version du produit. Dans les exemples
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
        "version": "15.8.0",
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
        "version": "15.8.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

Codes de statut HTTP
--------------------

L'API d'administration retourne dans la plupart des cas le statut HTTP ``200``, et
le resultat du traitement est exprime par le champ ``status`` du corps de la reponse.
Par consequent, determinez le succes ou l'echec non pas a partir du code de statut HTTP,
mais a partir de la valeur de ``status`` dans le corps.

Les codes de statut HTTP reellement retournes sont les suivants.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - 200
     - Reponse normale. Outre les cas de succes (``status: 0``), la plupart des erreurs
       sont egalement retournees avec ce code. Par exemple, si le jeton d'acces est absent
       ou invalide, ou si les permissions sont insuffisantes, ``status: 3`` est retourne ;
       une erreur systeme renvoie ``status: 2`` ; dans tous ces cas avec le statut HTTP ``200``.
   * - 400
     - Erreur de validation des parametres de requete. Le ``status`` du corps de la reponse
       est ``1``. Ce code est egalement retourne lorsque l'on tente d'obtenir une ressource
       inexistante.
   * - 401
     - Lorsqu'une exception liee a l'authentification de connexion se produit. Le ``status``
       du corps de la reponse est ``3``. A noter que si le jeton d'acces est absent ou
       invalide, ce n'est pas ce code qui est retourne, mais le statut HTTP ``200`` avec
       ``status: 3``.

.. note::

   L'API d'administration ne retourne pas de codes de statut HTTP tels que ``403``,
   ``404`` ou ``500``. L'insuffisance de permissions et l'inexistence d'une ressource
   sont egalement indiquees par le ``status`` contenu dans le corps de la reponse HTTP
   ``200`` ou ``400``.

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

   Pour la creation d'une configuration de crawl Web, les champs ``name``, ``urls``,
   ``userAgent``, ``numOfThread``, ``intervalTime``, ``boost``, ``available`` et
   ``sortOrder`` sont obligatoires. Les omettre provoque une erreur de validation
   (``status: 1``). ``available`` se specifie sous forme de chaine de caracteres,
   en y placant ``"true"`` ou ``"false"``.

Demarrage d'une tache planifiee
-------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention de la liste des utilisateurs
--------------------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`../api-overview` - Vue d'ensemble de l'API
- :doc:`../../admin/accesstoken-guide` - Guide de gestion des jetons d'acces
