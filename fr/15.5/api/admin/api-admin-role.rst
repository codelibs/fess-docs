==========================
API Role
==========================

Vue d'ensemble
==============

L'API Role permet de gerer les roles de |Fess|.
Vous pouvez creer, mettre a jour et supprimer des roles.

URL de base
===========

::

    /api/admin/role

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
     - Obtention de la liste des roles
   * - GET
     - /setting/{id}
     - Obtention d'un role
   * - POST
     - /setting
     - Creation d'un role
   * - PUT
     - /setting
     - Mise a jour d'un role
   * - DELETE
     - /setting/{id}
     - Suppression d'un role

Obtention de la liste des roles
===============================

Requete
-------

::

    GET /api/admin/role/settings
    PUT /api/admin/role/settings

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
            "id": "role_id_1",
            "name": "admin"
          },
          {
            "id": "role_id_2",
            "name": "user"
          }
        ],
        "total": 5
      }
    }

Obtention d'un role
===================

Requete
-------

::

    GET /api/admin/role/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin"
        }
      }
    }

Creation d'un role
==================

Requete
-------

::

    POST /api/admin/role/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
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
     - Nom du role

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

Mise a jour d'un role
=====================

Requete
-------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

Suppression d'un role
=====================

Requete
-------

::

    DELETE /api/admin/role/setting/{id}

Reponse
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

Creation d'un nouveau role
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

Obtention de la liste des roles
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-user` - API de gestion des utilisateurs
- :doc:`api-admin-group` - API de gestion des groupes
- :doc:`../../admin/role-guide` - Guide de gestion des roles
