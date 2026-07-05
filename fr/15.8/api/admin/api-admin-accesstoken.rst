==========================
AccessToken API
==========================

Vue d'ensemble
==============

L'API AccessToken est une API permettant de gerer les jetons d'acces API de |Fess|.
Il est possible de creer, recuperer, mettre a jour et supprimer des jetons.

Les jetons d'acces sont utilises pour l'authentification lors d'appels programmatiques a l'API de recherche ou a l'API Admin de |Fess|.
Pour les specifications communes de l'API Admin incluant cette API (methode d'authentification, format des reponses, valeurs de ``status``, reponses d'erreur,
codes de statut HTTP), consultez :doc:`api-admin-overview`.

.. note::

   Pour acceder a cette API, le jeton d'acces utilise dans la requete doit disposer d'une permission
   correspondant a ``api.admin.access.permissions``
   (valeur par defaut : ``{role}admin-api``).

URL de base
===========

::

    /api/admin/accesstoken

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
     - Obtention de la liste des jetons d'acces
   * - GET
     - /setting/{id}
     - Obtention d'un jeton d'acces
   * - POST
     - /setting
     - Creation d'un jeton d'acces
   * - PUT
     - /setting
     - Mise a jour d'un jeton d'acces
   * - DELETE
     - /setting/{id}
     - Suppression d'un jeton d'acces

Obtention de la liste des jetons d'acces
========================================

Requete
-------

::

    GET /api/admin/accesstoken/settings

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
     - Nombre d'elements par page (par defaut : 25 ; modifiable via ``paging.page.size``)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 1 ; par defaut : 1)
   * - ``id``
     - String
     - Non
     - Filtre permettant de recuperer uniquement le jeton ayant l'ID specifie

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Chaque objet jeton contient egalement des informations d'audit et de version telles que
   ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` et ``versionNo``.
   ``createdTime`` et ``updatedTime`` sont exprimes en millisecondes depuis l'epoch (valeur numerique).
   Les champs dont la valeur est ``null`` sont exclus de la reponse.
   ``permissions`` est retourne sous forme de chaine separee par des sauts de ligne (``\n``).

Obtention d'un jeton d'acces
============================

Requete
-------

::

    GET /api/admin/accesstoken/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
        }
      }
    }

Creation d'un jeton d'acces
============================

Requete
-------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom du jeton (1000 caracteres maximum)
   * - ``permissions``
     - Non
     - Permissions accordees a ce jeton. Plusieurs permissions peuvent etre specifiees en les separant par des sauts de ligne (``\n``) (exemple : ``{role}admin-api``). Pour les jetons appelant l'API Admin, une permission correspondant a ``api.admin.access.permissions`` (valeur par defaut : ``{role}admin-api``) est requise.
   * - ``parameterName``
     - Non
     - Nom du parametre de requete permettant de transmettre des permissions supplementaires. Si une requete authentifiee par ce jeton contient un parametre portant ce nom, sa valeur est ajoutee aux ``permissions``. Si omis, aucun parametre n'est configure.
   * - ``expires``
     - Non
     - Date d'expiration, specifiee sous forme de chaine au format ``YYYY-MM-DDTHH:MM:SS`` (exemple : ``2026-01-01T00:00:00``). Si omis, le jeton n'expire pas.

.. note::

   La chaine du jeton (``token``) est generee automatiquement cote serveur. Si ``token``
   est specifie dans le corps de la requete, il est ignore. La reponse de creation ne contient pas la chaine du jeton ;
   pour recuperer la chaine de jeton generee, utilisez "Obtention d'un jeton d'acces" (``GET /setting/{id}``).

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "created": true
      }
    }

Mise a jour d'un jeton d'acces
==============================

Requete
-------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

En plus des champs utilises lors de la creation, les champs suivants sont employes lors de la mise a jour.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - ID du jeton a mettre a jour
   * - ``versionNo``
     - Oui
     - Numero de version pour le verrouillage optimiste. Specifiez le ``versionNo`` du jeton obtenu au prealable.

.. note::

   La chaine du jeton (``token``) ne peut pas etre mise a jour. Si ``token`` est specifie dans le corps de la requete,
   il est ignore et la valeur existante est conservee.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

Suppression d'un jeton d'acces
==============================

Requete
-------

::

    DELETE /api/admin/accesstoken/setting/{id}

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

Creation d'un jeton API
-----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

Appel API utilisant un jeton
----------------------------

Le jeton cree est utilise pour l'authentification lors d'appels a l'API de recherche ou a d'autres APIs.

.. code-block:: bash

    # Utiliser le jeton comme en-tete Authorization
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # Utiliser le jeton comme parametre de requete (necessite la configuration de api.access.token.request.parameter)
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin (authentification, format des reponses, erreurs)
- :doc:`../api-search` - API de recherche
- :doc:`../../admin/accesstoken-guide` - Guide de gestion des jetons d'acces
