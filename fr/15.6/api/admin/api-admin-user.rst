==========================
API User
==========================

Vue d'ensemble
==============

L'API User permet de gerer les comptes utilisateurs de |Fess|.
Vous pouvez creer, mettre a jour, supprimer des utilisateurs et configurer leurs permissions.

URL de base
===========

::

    /api/admin/user

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
     - Obtention de la liste des utilisateurs
   * - GET
     - /setting/{id}
     - Obtention d'un utilisateur
   * - POST
     - /setting
     - Creation d'un utilisateur
   * - PUT
     - /setting
     - Mise a jour d'un utilisateur
   * - DELETE
     - /setting/{id}
     - Suppression d'un utilisateur

Obtention de la liste des utilisateurs
======================================

Requete
-------

::

    GET /api/admin/user/settings
    PUT /api/admin/user/settings

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
            "id": "user_id_1",
            "name": "admin",
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "roles": ["admin"],
            "groups": []
          }
        ],
        "total": 10
      }
    }

Obtention d'un utilisateur
==========================

Requete
-------

::

    GET /api/admin/user/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "user_id_1",
          "name": "admin",
          "surname": "Administrator",
          "givenName": "System",
          "mail": "admin@example.com",
          "telephoneNumber": "",
          "homePhone": "",
          "homePostalAddress": "",
          "labeledUri": "",
          "roomNumber": "",
          "description": "",
          "title": "",
          "pager": "",
          "street": "",
          "postalCode": "",
          "physicalDeliveryOfficeName": "",
          "destinationIndicator": "",
          "internationaliSDNNumber": "",
          "state": "",
          "employeeNumber": "",
          "facsimileTelephoneNumber": "",
          "postOfficeBox": "",
          "initials": "",
          "carLicense": "",
          "mobile": "",
          "postalAddress": "",
          "city": "",
          "teletexTerminalIdentifier": "",
          "x121Address": "",
          "businessCategory": "",
          "registeredAddress": "",
          "displayName": "",
          "preferredLanguage": "",
          "departmentNumber": "",
          "uidNumber": "",
          "gidNumber": "",
          "homeDirectory": "",
          "roles": ["admin"],
          "groups": []
        }
      }
    }

Creation d'un utilisateur
=========================

Requete
-------

::

    POST /api/admin/user/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "surname": "Test",
      "givenName": "User",
      "mail": "testuser@example.com",
      "roles": ["user"],
      "groups": ["group_id_1"]
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
     - Nom d'utilisateur (identifiant de connexion)
   * - ``password``
     - Oui
     - Mot de passe
   * - ``surname``
     - Non
     - Nom de famille
   * - ``givenName``
     - Non
     - Prenom
   * - ``mail``
     - Non
     - Adresse email
   * - ``telephoneNumber``
     - Non
     - Numero de telephone
   * - ``roles``
     - Non
     - Tableau des IDs de roles
   * - ``groups``
     - Non
     - Tableau des IDs de groupes

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

Mise a jour d'un utilisateur
============================

Requete
-------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "surname": "Test",
      "givenName": "User Updated",
      "mail": "testuser.updated@example.com",
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

Suppression d'un utilisateur
============================

Requete
-------

::

    DELETE /api/admin/user/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

Exemples d'utilisation
======================

Creation d'un nouvel utilisateur
--------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "surname": "Doe",
           "givenName": "John",
           "mail": "john.doe@example.com",
           "roles": ["user"],
           "groups": []
         }'

Modification des roles d'un utilisateur
---------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-role` - API de gestion des roles
- :doc:`api-admin-group` - API de gestion des groupes
- :doc:`../../admin/user-guide` - Guide de gestion des utilisateurs
