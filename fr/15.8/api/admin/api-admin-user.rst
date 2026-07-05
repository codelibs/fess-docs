==========================
User API
==========================

Vue d'ensemble
==============

L'API User est une API REST pour gérer les comptes utilisateurs de |Fess|.
Vous pouvez créer, récupérer, mettre à jour et supprimer des utilisateurs, et leur attribuer des rôles et des groupes.

Il s'agit d'une API d'administration ; son accès requiert une authentification par jeton d'accès administrateur.
Consultez :doc:`api-admin-overview` pour la méthode d'authentification et les spécifications communes.

Chaque réponse est encapsulée dans un objet ``response`` et contient les champs communs suivants :

- ``version`` : La chaîne de version du produit |Fess|.
- ``status`` : Le code de statut du résultat (``0`` = succès, ``1`` = requête invalide, ``2`` = erreur système, ``3`` = non autorisé, ``9`` = échec).

URL de base
===========

::

    /api/admin/user

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
     - Lister les utilisateurs
   * - GET
     - /setting/{id}
     - Récupérer un utilisateur
   * - POST
     - /setting
     - Créer un utilisateur
   * - PUT
     - /setting
     - Mettre à jour un utilisateur
   * - DELETE
     - /setting/{id}
     - Supprimer un utilisateur

Lister les utilisateurs
=======================

Requête
-------

::

    GET /api/admin/user/settings

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page. La valeur par défaut est la valeur configurée ``paging.page.size`` (par défaut : 25).
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1). La valeur par défaut est 1.

.. note::

   Dans l'implémentation actuelle, l'endpoint de liste des utilisateurs n'applique pas les paramètres ``size`` et ``page``.
   Il retourne toujours la première page, avec le nombre d'éléments défini par le paramètre serveur ``paging.page.size`` (par défaut : 25), trié par nom d'utilisateur (``name``) en ordre croissant.
   Le nombre total d'utilisateurs correspondants est disponible dans ``response.total``.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : Le tableau des utilisateurs de la page courante.
- ``total`` : Le nombre total d'utilisateurs correspondants.

Récupérer un utilisateur
========================

Requête
-------

::

    GET /api/admin/user/setting/{id}

Spécifiez l'identifiant de document de l'utilisateur cible dans ``{id}``.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["admin"],
          "groups": [],
          "versionNo": 1
        }
      }
    }

.. note::

   ``attributes`` contient tous les attributs enregistrés pour l'utilisateur, à l'exception de ``name``, ``password``, ``roles`` et ``groups``.
   ``password`` n'est pas inclus dans la réponse.

Créer un utilisateur
====================

Requête
-------

::

    POST /api/admin/user/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom d'utilisateur (identifiant de connexion)
   * - ``password``
     - Non
     - Mot de passe
   * - ``confirmPassword``
     - Non
     - Mot de passe de confirmation
   * - ``attributes``
     - Non
     - Map d'attributs (voir ci-dessous)
   * - ``roles``
     - Non
     - Tableau des identifiants de rôles
   * - ``groups``
     - Non
     - Tableau des identifiants de groupes

.. note::

   L'API REST n'effectue pas de vérification d'obligation du mot de passe, de vérification de correspondance entre ``password`` et ``confirmPassword``, ni de validation de politique de mot de passe (celles-ci ne s'appliquent que dans l'interface d'administration).
   En pratique, il est recommandé de spécifier un ``password`` valide dont la valeur correspond à ``confirmPassword``.

Les clés de ``attributes`` sont les noms d'attributs de l'entité utilisateur (les noms d'éléments dérivés du schéma LDAP).
Les clés les plus courantes sont :

- ``surname``, ``givenName``, ``displayName``, ``mail``
- ``telephoneNumber``, ``mobile``, ``homePhone``
- ``employeeNumber``, ``title``, ``description``, ``homeDirectory``
- ``uidNumber``, ``gidNumber``

``uidNumber`` et ``gidNumber`` doivent être numériques (leur type est validé lors de la mise à jour).
De nombreuses autres clés d'attributs LDAP peuvent également être spécifiées.

.. note::

   Lors de la création, l'identifiant de l'utilisateur (identifiant de document) est automatiquement généré comme la valeur encodée en Base64 URL du nom d'utilisateur
   (par exemple, le nom d'utilisateur ``admin`` devient ``YWRtaW4=``).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` : L'identifiant de document de l'utilisateur créé.
- ``created`` : ``true`` lors de la création.

Mettre à jour un utilisateur
============================

Requête
-------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - L'identifiant de document de l'utilisateur à mettre à jour.
   * - ``name``
     - Oui
     - Nom d'utilisateur (identifiant de connexion)
   * - ``versionNo``
     - Oui
     - Numéro de version (pour le verrouillage optimiste)
   * - ``password``
     - Non
     - Nouveau mot de passe (mis à jour uniquement si spécifié)
   * - ``confirmPassword``
     - Non
     - Mot de passe de confirmation
   * - ``attributes``
     - Non
     - Map d'attributs (voir « Créer un utilisateur »)
   * - ``roles``
     - Non
     - Tableau des identifiants de rôles
   * - ``groups``
     - Non
     - Tableau des identifiants de groupes

.. note::

   Lors de la mise à jour, ``id``, ``name`` et ``versionNo`` sont obligatoires.
   ``versionNo`` est la valeur retournée lors de la récupération de l'utilisateur cible (GET), et correspond à la version du document OpenSearch.
   Si elle ne correspond pas à la version actuelle, la requête est traitée comme un conflit et la mise à jour est rejetée.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : ``false`` pour une mise à jour.

Supprimer un utilisateur
========================

Requête
-------

::

    DELETE /api/admin/user/setting/{id}

Spécifiez l'identifiant de document de l'utilisateur à supprimer dans ``{id}``.

.. note::

   Vous ne pouvez pas supprimer l'utilisateur actuellement connecté.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` : L'identifiant de document de l'utilisateur supprimé.

Exemples d'utilisation
======================

Créer un nouvel utilisateur
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["user"],
           "groups": []
         }'

Modifier les rôles d'un utilisateur
------------------------------------

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

Références
==========

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-role` - API de gestion des rôles
- :doc:`api-admin-group` - API de gestion des groupes
- :doc:`../../admin/user-guide` - Guide de gestion des utilisateurs
