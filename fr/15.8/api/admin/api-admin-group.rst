==========================
API Group
==========================

Vue d'ensemble
==============

L'API Group permet de gérer les groupes de |Fess|.
Vous pouvez créer, mettre à jour et supprimer des groupes.

URL de base
===========

::

    /api/admin/group

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
     - Obtention de la liste des groupes
   * - GET
     - /setting/{id}
     - Obtention d'un groupe
   * - POST
     - /setting
     - Création d'un groupe
   * - PUT
     - /setting
     - Mise à jour d'un groupe
   * - DELETE
     - /setting/{id}
     - Suppression d'un groupe

Obtention de la liste des groupes
=================================

Requête
-------

::

    GET /api/admin/group/settings

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
     - Nombre d'éléments par page (par défaut : 25)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1)
   * - ``id``
     - String
     - Non
     - Filtre par correspondance exacte sur l'ID de groupe spécifié

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "group_id_1",
            "name": "Engineering",
            "attributes": {
              "gidNumber": "1000"
            },
            "versionNo": 1
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "attributes": {
              "gidNumber": "1001"
            },
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

Obtention d'un groupe
=====================

Requête
-------

::

    GET /api/admin/group/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "attributes": {
            "gidNumber": "1000"
          },
          "versionNo": 1
        }
      }
    }

Création d'un groupe
====================

Requête
-------

::

    POST /api/admin/group/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "attributes": {
        "gidNumber": "1002"
      }
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
     - Nom du groupe (maximum 100 caractères)
   * - ``attributes``
     - Non
     - Map d'attributs (contenant des attributs LDAP comme ``gidNumber``). Les valeurs sont spécifiées sous forme de chaînes de caractères

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

Mise à jour d'un groupe
=======================

Requête
-------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "attributes": {
        "gidNumber": "1002"
      },
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
     - ID du groupe à mettre à jour
   * - ``name``
     - Oui
     - Nom du groupe (maximum 100 caractères)
   * - ``attributes``
     - Non
     - Map d'attributs (contenant des attributs LDAP comme ``gidNumber``). Les valeurs sont spécifiées sous forme de chaînes de caractères
   * - ``versionNo``
     - Oui
     - Numéro de version pour le verrouillage optimiste. Spécifiez la valeur de ``versionNo`` obtenue lors de l'obtention du groupe

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

Suppression d'un groupe
=======================

Requête
-------

::

    DELETE /api/admin/group/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

Exemples d'utilisation
======================

Création d'un nouveau groupe
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "attributes": {
             "gidNumber": "2000"
           }
         }'

Obtention de la liste des groupes
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-user` - API de gestion des utilisateurs
- :doc:`api-admin-role` - API de gestion des rôles
- :doc:`../../admin/group-guide` - Guide de gestion des groupes
