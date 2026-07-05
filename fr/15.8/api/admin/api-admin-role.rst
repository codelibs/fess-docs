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
   * - GET
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
================================

Requete
-------

::

    GET /api/admin/role/settings

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
     - Nombre d'elements par page (par defaut : 25. Modifiable via la propriete ``paging.page.size`` dans ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 1, par defaut : 1. Les valeurs de 0 ou moins sont traitees comme 1)
   * - ``id``
     - String
     - Non
     - Filtre par correspondance exacte sur l'ID de role specifie

Reponse
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
          "name": "admin",
          "versionNo": 1
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
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom du role (maximum 100 caracteres)
   * - ``attributes``
     - Non
     - Map d'attributs. Les valeurs sont specifiees sous forme de chaines de caracteres

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
     - ID du role a mettre a jour
   * - ``name``
     - Oui
     - Nom du role (maximum 100 caracteres)
   * - ``attributes``
     - Non
     - Map d'attributs. Les valeurs sont specifiees sous forme de chaines de caracteres
   * - ``versionNo``
     - Oui
     - Numero de version pour le verrouillage optimiste. Specifiez la valeur de ``versionNo`` obtenue lors de l'obtention du role

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
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-user` - API de gestion des utilisateurs
- :doc:`api-admin-group` - API de gestion des groupes
- :doc:`../../admin/role-guide` - Guide de gestion des roles
