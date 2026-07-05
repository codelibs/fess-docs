==========================
API Group
==========================

Vue d'ensemble
==============

L'API Group permet de gerer les groupes de |Fess|.
Vous pouvez creer, mettre a jour et supprimer des groupes.

URL de base
===========

::

    /api/admin/group

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET/PUT
     - /settings
     - Obtention de la liste des groupes
   * - GET
     - /setting/{id}
     - Obtention d'un groupe
   * - POST
     - /setting
     - Creation d'un groupe
   * - PUT
     - /setting
     - Mise a jour d'un groupe
   * - DELETE
     - /setting/{id}
     - Suppression d'un groupe

Obtention de la liste des groupes
=================================

Requete
-------

::

    GET /api/admin/group/settings
    PUT /api/admin/group/settings

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
            "id": "group_id_1",
            "name": "Engineering",
            "gidNumber": 1000
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "gidNumber": 1001
          }
        ],
        "total": 5
      }
    }

Obtention d'un groupe
=====================

Requete
-------

::

    GET /api/admin/group/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "gidNumber": 1000
        }
      }
    }

Creation d'un groupe
====================

Requete
-------

::

    POST /api/admin/group/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "gidNumber": 1002
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
     - Nom du groupe
   * - ``gidNumber``
     - Non
     - Numero d'ID du groupe

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

Mise a jour d'un groupe
=======================

Requete
-------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "gidNumber": 1002,
      "versionNo": 1
    }

Reponse
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

Requete
-------

::

    DELETE /api/admin/group/setting/{id}

Reponse
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

Creation d'un nouveau groupe
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "gidNumber": 2000
         }'

Obtention de la liste des groupes
---------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-user` - API de gestion des utilisateurs
- :doc:`api-admin-role` - API de gestion des roles
- :doc:`../../admin/group-guide` - Guide de gestion des groupes
