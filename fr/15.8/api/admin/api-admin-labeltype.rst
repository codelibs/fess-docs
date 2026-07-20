==========================
LabelType API
==========================

Vue d'ensemble
==============

L'API LabelType permet de gérer les types de labels de |Fess|.
Les types de labels permettent de classer les résultats de recherche en fonction des chemins
cibles du crawl et des hôtes virtuels, et peuvent être utilisés pour le filtrage
(restriction) par label dans l'interface de recherche.

Pour les méthodes d'authentification et les spécifications communes des réponses
(code ``status``, champ ``version``, format des erreurs, codes de statut HTTP, etc.),
consultez :doc:`api-admin-overview`.
Pour accéder à cette API, un jeton d'accès disposant de la permission d'API d'administration
(``admin-api``) doit être spécifié dans l'en-tête ``Authorization: Bearer <jeton d'accès>``.

URL de base
===========

::

    /api/admin/labeltype

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
     - Obtention de la liste des types de labels
   * - GET
     - /setting/{id}
     - Obtention d'un type de label
   * - POST
     - /setting
     - Création d'un type de label
   * - PUT
     - /setting
     - Mise à jour d'un type de label
   * - DELETE
     - /setting/{id}
     - Suppression d'un type de label

Obtention de la liste des types de labels
==========================================

Requête
-------

::

    GET /api/admin/labeltype/settings

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
     - Nombre d'éléments par page. La valeur par défaut est celle du paramètre ``paging.page.size`` (``25`` par défaut).
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à ``1``). La valeur par défaut est ``1``.
   * - ``name``
     - String
     - Non
     - Filtrage par nom d'affichage (recherche avec caractères génériques).
   * - ``value``
     - String
     - Non
     - Filtrage par valeur de label (recherche avec caractères génériques).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Chaque objet de configuration inclut également ``createdBy`` / ``createdTime`` /
   ``updatedBy`` / ``updatedTime`` à des fins d'audit, ainsi que ``versionNo`` pour le
   verrouillage optimiste (les champs dont la valeur est ``null`` sont omis). L'objet
   ``response`` contient toujours ``version``, indiquant la version du produit, mais
   celui-ci peut être omis dans les exemples suivants par souci de concision.

Obtention d'un type de label
=============================

Requête
-------

::

    GET /api/admin/labeltype/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "permissions": "{role}admin",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

Création d'un type de label
============================

Requête
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~~

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
     - Nom d'affichage du label (100 caractères maximum).
   * - ``value``
     - String
     - Oui
     - Valeur du label (utilisée avec le paramètre ``label`` lors des recherches). Seuls les caractères alphanumériques et les tirets bas (``_``) sont autorisés ; la valeur doit correspondre à l'expression régulière ``^[a-zA-Z0-9_]+$`` (100 caractères maximum).
   * - ``includedPaths``
     - String
     - Non
     - Expression régulière des chemins cibles du label. Si plusieurs valeurs sont spécifiées, elles sont séparées par un saut de ligne (``\n``).
   * - ``excludedPaths``
     - String
     - Non
     - Expression régulière des chemins à exclure du label. Si plusieurs valeurs sont spécifiées, elles sont séparées par un saut de ligne (``\n``).
   * - ``permissions``
     - String
     - Non
     - Rôles, groupes ou utilisateurs autorisés à accéder (ex. : ``{role}admin``). Si plusieurs valeurs sont spécifiées, elles sont séparées par un saut de ligne (``\n``).
   * - ``sortOrder``
     - Integer
     - Non
     - Ordre d'affichage (entier supérieur ou égal à 0). La valeur par défaut est ``0``.
   * - ``virtualHost``
     - String
     - Non
     - Hôte virtuel (1000 caractères maximum).

.. note::

   Les champs d'audit tels que ``createdBy`` / ``createdTime`` sont définis
   automatiquement côté serveur et n'ont pas besoin d'être spécifiés dans la requête.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

En cas de création réussie, ``created`` prend la valeur ``true``.

Mise à jour d'un type de label
================================

Requête
-------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest",
      "versionNo": 1
    }

Lors d'une mise à jour, les champs suivants sont obligatoires en plus de ceux utilisés lors de la création.

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
     - ID du type de label à mettre à jour.
   * - ``versionNo``
     - Integer
     - Oui
     - Numéro de version pour le verrouillage optimiste. Spécifiez la valeur ``versionNo`` présente dans la réponse obtenue lors de la lecture. Si la version spécifiée ne correspond pas à la version actuelle, la mise à jour échoue.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

Dans le cas d'une mise à jour, ``created`` prend la valeur ``false``.

Suppression d'un type de label
================================

Requête
-------

::

    DELETE /api/admin/labeltype/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
=======================

Création d'un label pour la documentation
------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Obtention de la liste des types de labels
------------------------------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Recherche avec un label
------------------------

.. code-block:: bash

    # Filtrage par label
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Informations complémentaires
=============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../api-search` - API de recherche
- :doc:`../../admin/labeltype-guide` - Guide de gestion des types de labels
