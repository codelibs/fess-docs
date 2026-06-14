==========================
API AccessToken
==========================

Vue d'ensemble
==============

L'API AccessToken permet de gerer les jetons d'acces API de |Fess|.
Vous pouvez creer, mettre a jour et supprimer des jetons.

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
   :widths: 20 15 15.70

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expires": "2025-01-01T00:00:00",
            "permissions": "{role}admin"
          }
        ],
        "total": 5
      }
    }

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
          "parameterName": "token",
          "expires": "2025-01-01T00:00:00",
          "permissions": "{role}admin"
        }
      }
    }

Creation d'un jeton d'acces
===========================

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
      "parameterName": "token",
      "expires": "2026-01-01T00:00:00",
      "permissions": "{role}user"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom du jeton
   * - ``token``
     - Non
     - Chaine du jeton (genere automatiquement si non specifie)
   * - ``parameterName``
     - Non
     - Nom du parametre (par defaut : "token")
   * - ``expires``
     - Non
     - Date d'expiration (chaine au format ISO 8601. Exemple : ``2026-01-01T00:00:00``)
   * - ``permissions``
     - Non
     - Permissions autorisees. Specifiees sous forme de chaine separee par des sauts de ligne (exemple : ``{role}admin``)

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
      "parameterName": "token",
      "expires": "2026-01-01T00:00:00",
      "permissions": "{role}user\n{role}editor",
      "versionNo": 1
    }

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
           "name": "External App Token",
           "parameterName": "token",
           "permissions": "{role}guest"
         }'

Appel API utilisant un jeton
----------------------------

.. code-block:: bash

    # Utiliser le jeton comme parametre
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # Utiliser le jeton dans l'en-tete Authorization
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../api-search` - API de recherche
- :doc:`../../admin/accesstoken-guide` - Guide de gestion des jetons d'acces
