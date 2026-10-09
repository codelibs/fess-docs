===========
TagType API
===========

Vue d'ensemble
==============

L'API TagType permet de gérer les tags des utilisateurs de |Fess|, c'est-à-dire les tags propres à
chaque utilisateur que les utilisateurs connectés posent sur des documents (voir
:doc:`../../admin/tagtype-guide`). Elle gère les tags de tous les utilisateurs, que
``user.tag.enabled`` vaille ``true`` ou non.

Pour les méthodes d'authentification et les spécifications communes des réponses
(code ``status``, champ ``version``, format des erreurs, codes de statut HTTP, etc.),
consultez :doc:`api-admin-overview`.
Pour accéder à cette API, un jeton d'accès disposant de la permission d'API d'administration
(``admin-api``) doit être indiqué dans l'en-tête ``Authorization: Bearer <jeton d'accès>``.

Les noms des champs JSON de cette API sont en snake_case (``sort_order``, ``virtual_host``,
``seq_no``, ``primary_term``, etc.).

URL de base
===========

::

    /api/admin/tagtype

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
     - Obtention de la liste des tags
   * - GET
     - /setting/{id}
     - Obtention d'un tag
   * - POST
     - /setting
     - Création d'un tag
   * - PUT
     - /setting
     - Mise à jour d'un tag
   * - DELETE
     - /setting/{id}
     - Suppression d'un tag

Obtention de la liste des tags
==============================

Requête
-------

::

    GET /api/admin/tagtype/settings

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Obligatoire
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page. Par défaut, la valeur de ``paging.page.size`` (``25`` par défaut).
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1). Par défaut ``1``.
   * - ``name``
     - String
     - Non
     - Filtre sur le nom du tag (recherche avec joker : correspond aux noms qui contiennent le texte).
   * - ``owner``
     - String
     - Non
     - Filtre sur le propriétaire (recherche avec joker : correspond aux propriétaires qui contiennent le texte).

Les tags sont triés par ordre de tri, nom et propriétaire.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.9",
        "status": 0,
        "settings": [
          {
            "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
            "seq_no": 12,
            "primary_term": 1,
            "name": "to-review",
            "owner": "alice",
            "permissions": "{user}alice",
            "virtual_host": "",
            "sort_order": 0
          }
        ],
        "total": 5
      }
    }

.. note::

   La liste ne lit pas les chemins des tags, qui peuvent être longs : ses éléments n'ont donc pas de
   ``paths``. PUT remplace le tag en entier : pour modifier un tag, obtenez-le d'abord avec
   ``GET /setting/{id}`` afin de conserver ses ``paths``.

Obtention d'un tag
==================

Requête
-------

::

    GET /api/admin/tagtype/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
          "seq_no": 12,
          "primary_term": 1,
          "name": "to-review",
          "owner": "alice",
          "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
          "permissions": "{user}alice",
          "virtual_host": "",
          "sort_order": 0
        }
      }
    }

``seq_no`` et ``primary_term`` identifient la version lue du tag. ``paths`` et ``permissions``
contiennent une valeur par ligne.

Création d'un tag
=================

Requête
-------

::

    POST /api/admin/tagtype/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "specs",
      "owner": "bob",
      "paths": "https://www.example.com/spec.pdf",
      "permissions": "{user}bob\n{role}guest",
      "sort_order": 0
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Champ
     - Type
     - Obligatoire
     - Description
   * - ``name``
     - String
     - Oui
     - Nom du tag. Il est normalisé en NFKC, les suites d'espaces sont réduites et les extrémités
       rognées ; le résultat doit compter de 1 à ``user.tag.name.max.length`` (par défaut : ``50``)
       caractères, sans caractère de contrôle ni de format.
   * - ``owner``
     - String
     - Oui
     - Identifiant de connexion du propriétaire (1000 caractères au maximum).
   * - ``paths``
     - String
     - Non
     - URL des documents sur lesquels poser le tag, séparées par un saut de ligne (``\n``). Chacune
       doit être égale au champ ``url`` d'un document. Au plus ``user.tag.max.paths`` (par défaut :
       ``10000``).
   * - ``permissions``
     - String
     - Non
     - Utilisateurs/groupes/rôles qui peuvent voir le tag (ex. ``{role}guest``), séparés par un saut
       de ligne (``\n``). Vide, seul le propriétaire voit le tag. ``{role}guest`` (la valeur de
       ``role.search.guest.permissions``) partage le tag avec tous les utilisateurs connectés.
   * - ``virtual_host``
     - String
     - Non
     - Hôte virtuel (1000 caractères au maximum).
   * - ``sort_order``
     - Integer
     - Non
     - Ordre d'affichage (entier positif ou nul). ``0`` s'il est omis.

L'identifiant d'un tag est le SHA-256 de sa valeur, formée du nom et du propriétaire ; il est donc
décidé par le serveur. Le propriétaire et le nom identifient ensemble un tag : si le propriétaire a
déjà un tag de ce nom, la création échoue avec une erreur de validation (``status: 1``, « A tag with
the same name and owner already exists. »).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "41e429a7d0081e25390c3840268d736dca00250167bab94250389aee9e08e2ed",
        "created": true
      }
    }

En cas de création réussie, ``created`` vaut ``true``.

Mise à jour d'un tag
====================

Requête
-------

::

    PUT /api/admin/tagtype/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
      "seq_no": 12,
      "primary_term": 1,
      "name": "reviewed",
      "owner": "alice",
      "paths": "https://www.example.com/a.html",
      "permissions": "{user}alice",
      "virtual_host": "",
      "sort_order": 0
    }

Le corps contient tous les champs de la création, plus les champs suivants. Le tag est remplacé en
entier : envoyez aussi les ``paths`` à conserver.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - Champ
     - Type
     - Obligatoire
     - Description
   * - ``id``
     - String
     - Oui
     - L'identifiant du tag à mettre à jour.
   * - ``seq_no``
     - Integer
     - Oui
     - Le ``seq_no`` du tag renvoyé par ``GET /setting/{id}``.
   * - ``primary_term``
     - Integer
     - Oui
     - Le ``primary_term`` du tag renvoyé par ``GET /setting/{id}``.

- Si le tag a été modifié après sa lecture, c'est-à-dire que ``seq_no`` et ``primary_term`` ne
  correspondent plus, la mise à jour échoue avec une erreur de validation (``status: 1``, « The tag
  was changed by someone else. Reload it and try again. »). Obtenez à nouveau le tag et
  recommencez.
- Modifier ``name`` ou ``owner`` donne au tag un nouvel identifiant ; l'``id`` de la réponse est le
  nouveau. Si le propriétaire a déjà un tag du nouveau nom, la mise à jour échoue avec « A tag with
  the same name and owner already exists. ».
- Lorsque le propriétaire change, la permission utilisateur de l'ancien propriétaire dans
  ``permissions`` est remplacée par celle du nouveau propriétaire.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "c1fd8e024cbadfc79468e66fa52350e46cc31837aabf75b7ee6d929edaa20396",
        "created": false
      }
    }

Lors d'une mise à jour, ``created`` vaut ``false``.

Suppression d'un tag
====================

Requête
-------

::

    DELETE /api/admin/tagtype/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Si le tag est modifié pendant sa suppression, celle-ci échoue avec « The tag was changed by someone
else. Reload it and try again. ».

Comment les modifications atteignent les documents
==================================================

La création, la mise à jour et la suppression d'un tag par cette API sont enregistrées
immédiatement dans les tags. Tant que ``user.tag.enabled`` vaut ``true``, la modification destinée
aux documents (chemins ajoutés et retirés, renommage ou suppression) est mise en file d'attente et
appliquée par la tâche « Log Aggregator » (``log_aggregator``) chaque minute. Tant qu'il vaut
``false``, rien n'est mis en file ; exécutez la tâche « Tag Updater » (``tag_updater``) après avoir
activé les tags. Voir :doc:`../../admin/tagtype-guide`.

Exemples d'utilisation
======================

Partager un tag avec tous les utilisateurs connectés
----------------------------------------------------

.. code-block:: bash

    # Lire le tag, avec paths, seq_no et primary_term
    curl "http://localhost:8080/api/admin/tagtype/setting/0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Le renvoyer avec {role}guest ajouté aux permissions
    curl -X PUT "http://localhost:8080/api/admin/tagtype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "0698e7f9c98a9b64ef11a2bbc71d8d2668c6907b397fa86c23ba19b7fec02d6c",
           "seq_no": 12,
           "primary_term": 1,
           "name": "to-review",
           "owner": "alice",
           "paths": "https://www.example.com/a.html\nhttps://www.example.com/b.html",
           "permissions": "{user}alice\n{role}guest",
           "sort_order": 0
         }'

Obtention des tags d'un utilisateur
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/tagtype/settings" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"owner": "alice", "size": 50, "page": 1}'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../api-tag` - API des tags
- :doc:`../../admin/tagtype-guide` - Guide de gestion des tags
