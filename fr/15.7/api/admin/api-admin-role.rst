==========================
API Role
==========================

Vue d'ensemble
==============

L'API Role permet de gérer les rôles de |Fess|.
Vous pouvez créer, mettre à jour et supprimer des rôles.

URL de base
===========

::

    /api/admin/role

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
     - Obtention de la liste des rôles
   * - GET
     - /setting/{id}
     - Obtention d'un rôle
   * - POST
     - /setting
     - Création d'un rôle
   * - PUT
     - /setting
     - Mise à jour d'un rôle
   * - DELETE
     - /setting/{id}
     - Suppression d'un rôle

Obtention de la liste des rôles
================================

Requête
-------

::

    GET /api/admin/role/settings

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
     - Nombre d'éléments par page (par défaut : 25. Modifiable via la propriété ``paging.page.size`` dans ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1. Les valeurs de 0 ou moins sont traitées comme 1)
   * - ``id``
     - String
     - Non
     - Filtre par correspondance exacte sur l'ID de rôle spécifié

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "role_id_1",
            "name": "admin",
            "versionNo": 1
          },
          {
            "id": "role_id_2",
            "name": "user",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

Obtention d'un rôle
===================

Requête
-------

::

    GET /api/admin/role/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin",
          "versionNo": 1
        }
      }
    }

Création d'un rôle
==================

Requête
-------

::

    POST /api/admin/role/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
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
     - Nom du rôle (maximum 100 caractères)
   * - ``attributes``
     - Non
     - Map d'attributs. Les valeurs sont spécifiées sous forme de chaînes de caractères

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

Mise à jour d'un rôle
=====================

Requête
-------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - ID du rôle à mettre à jour
   * - ``name``
     - Oui
     - Nom du rôle (maximum 100 caractères)
   * - ``attributes``
     - Non
     - Map d'attributs. Les valeurs sont spécifiées sous forme de chaînes de caractères
   * - ``versionNo``
     - Oui
     - Numéro de version pour le verrouillage optimiste. Spécifiez la valeur de ``versionNo`` obtenue lors de l'obtention du rôle

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

Suppression d'un rôle
=====================

Requête
-------

::

    DELETE /api/admin/role/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

Exemples d'utilisation
======================

Création d'un nouveau rôle
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

Obtention de la liste des rôles
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-user` - API de gestion des utilisateurs
- :doc:`api-admin-group` - API de gestion des groupes
- :doc:`../../admin/role-guide` - Guide de gestion des rôles
