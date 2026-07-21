==========================
AccessToken API
==========================

Vue d'ensemble
==============

L'API AccessToken est une API permettant de gérer les jetons d'accès API de |Fess|.
Il est possible de créer, récupérer, mettre à jour et supprimer des jetons.

Les jetons d'accès sont utilisés pour l'authentification lors d'appels programmatiques à l'API de recherche ou à l'API Admin de |Fess|.
Pour les spécifications communes de l'API Admin incluant cette API (méthode d'authentification, format des réponses, valeurs de ``status``, réponses d'erreur,
codes de statut HTTP), consultez :doc:`api-admin-overview`.

.. note::

   Pour accéder à cette API, le jeton d'accès utilisé dans la requête doit disposer d'une permission
   correspondant à ``api.admin.access.permissions``
   (valeur par défaut : ``{role}admin-api``).

URL de base
===========

::

    /api/admin/accesstoken

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
     - Obtention de la liste des jetons d'accès
   * - GET
     - /setting/{id}
     - Obtention d'un jeton d'accès
   * - POST
     - /setting
     - Création d'un jeton d'accès
   * - PUT
     - /setting
     - Mise à jour d'un jeton d'accès
   * - DELETE
     - /setting/{id}
     - Suppression d'un jeton d'accès

Obtention de la liste des jetons d'accès
========================================

Requête
-------

::

    GET /api/admin/accesstoken/settings

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
     - Nombre d'éléments par page (par défaut : 25 ; modifiable via ``paging.page.size``)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1 ; par défaut : 1)
   * - ``id``
     - String
     - Non
     - Filtre permettant de récupérer uniquement le jeton ayant l'ID spécifié

Réponse
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

   Chaque objet jeton contient également des informations d'audit et de version telles que
   ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` et ``versionNo``.
   ``createdTime`` et ``updatedTime`` sont exprimés en millisecondes depuis l'epoch (valeur numérique).
   Les champs dont la valeur est ``null`` sont exclus de la réponse.
   ``permissions`` est retourné sous forme de chaîne séparée par des sauts de ligne (``\n``).

Obtention d'un jeton d'accès
============================

Requête
-------

::

    GET /api/admin/accesstoken/setting/{id}

Réponse
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

Création d'un jeton d'accès
============================

Requête
-------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

Corps de la requête
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
     - Nom du jeton (1000 caractères maximum)
   * - ``permissions``
     - Non
     - Permissions accordées à ce jeton. Plusieurs permissions peuvent être spécifiées en les séparant par des sauts de ligne (``\n``) (exemple : ``{role}admin-api``). Pour les jetons appelant l'API Admin, une permission correspondant à ``api.admin.access.permissions`` (valeur par défaut : ``{role}admin-api``) est requise.
   * - ``parameterName``
     - Non
     - Nom du paramètre de requête permettant de transmettre des permissions supplémentaires. Si une requête authentifiée par ce jeton contient un paramètre portant ce nom, sa valeur est ajoutée aux ``permissions``. Si omis, aucun paramètre n'est configuré.
   * - ``expires``
     - Non
     - Date d'expiration, spécifiée sous forme de chaîne au format ``YYYY-MM-DDTHH:MM:SS`` (exemple : ``2026-01-01T00:00:00``). Si omis, le jeton n'expire pas.

.. note::

   La chaîne du jeton (``token``) est générée automatiquement côté serveur. Si ``token``
   est spécifié dans le corps de la requête, il est ignoré. La réponse de création ne contient pas la chaîne du jeton ;
   pour récupérer la chaîne de jeton générée, utilisez "Obtention d'un jeton d'accès" (``GET /setting/{id}``).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "created": true
      }
    }

Mise à jour d'un jeton d'accès
==============================

Requête
-------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

Corps de la requête
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

En plus des champs utilisés lors de la création, les champs suivants sont employés lors de la mise à jour.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - ID du jeton à mettre à jour
   * - ``versionNo``
     - Oui
     - Numéro de version pour le verrouillage optimiste. Spécifiez le ``versionNo`` du jeton obtenu au préalable.

.. note::

   La chaîne du jeton (``token``) ne peut pas être mise à jour. Si ``token`` est spécifié dans le corps de la requête,
   il est ignoré et la valeur existante est conservée.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

Suppression d'un jeton d'accès
==============================

Requête
-------

::

    DELETE /api/admin/accesstoken/setting/{id}

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

Création d'un jeton API
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

Le jeton créé est utilisé pour l'authentification lors d'appels à l'API de recherche ou à d'autres APIs.

.. code-block:: bash

    # Utiliser le jeton comme en-tete Authorization
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # Utiliser le jeton comme parametre de requete (necessite la configuration de api.access.token.request.parameter)
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin (authentification, format des réponses, erreurs)
- :doc:`../api-search` - API de recherche
- :doc:`../../admin/accesstoken-guide` - Guide de gestion des jetons d'accès
