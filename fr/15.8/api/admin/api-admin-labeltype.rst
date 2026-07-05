==========================
LabelType API
==========================

Apercu
======

L'API LabelType permet de gerer les types de labels de |Fess|.
Les types de labels permettent de classer les resultats de recherche en fonction des chemins
cibles du crawl et des hotes virtuels, et peuvent etre utilises pour le filtrage
(restriction) par label dans l'interface de recherche.

Pour les methodes d'authentification et les specifications communes des reponses
(code ``status``, champ ``version``, format des erreurs, codes de statut HTTP, etc.),
consultez :doc:`api-admin-overview`.
Pour acceder a cette API, un jeton d'acces disposant de la permission d'API d'administration
(``admin-api``) doit etre specifie dans l'en-tete ``Authorization: Bearer <jeton d'acces>``.

URL de base
===========

::

    /api/admin/labeltype

Liste des points de terminaison
================================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
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
     - Creation d'un type de label
   * - PUT
     - /setting
     - Mise a jour d'un type de label
   * - DELETE
     - /setting/{id}
     - Suppression d'un type de label

Obtention de la liste des types de labels
==========================================

Requete
-------

::

    GET /api/admin/labeltype/settings

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Obligatoire
     - Description
   * - ``size``
     - Integer
     - Non
     - Nombre d'elements par page. La valeur par defaut est celle du parametre ``paging.page.size`` (``25`` par defaut).
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a ``1``). La valeur par defaut est ``1``.
   * - ``name``
     - String
     - Non
     - Filtrage par nom d'affichage (recherche avec caracteres generiques).
   * - ``value``
     - String
     - Non
     - Filtrage par valeur de label (recherche avec caracteres generiques).

Reponse
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

   Chaque objet de configuration inclut egalement ``createdBy`` / ``createdTime`` /
   ``updatedBy`` / ``updatedTime`` a des fins d'audit, ainsi que ``versionNo`` pour le
   verrouillage optimiste (les champs dont la valeur est ``null`` sont omis). L'objet
   ``response`` contient toujours ``version``, indiquant la version du produit, mais
   celui-ci peut etre omis dans les exemples suivants par souci de concision.

Obtention d'un type de label
=============================

Requete
-------

::

    GET /api/admin/labeltype/setting/{id}

Reponse
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

Creation d'un type de label
============================

Requete
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Corps de la requete
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
     - Nom d'affichage du label (100 caracteres maximum).
   * - ``value``
     - String
     - Oui
     - Valeur du label (utilisee avec le parametre ``label`` lors des recherches). Seuls les caracteres alphanumeriques et les tirets bas (``_``) sont autorises ; la valeur doit correspondre a l'expression reguliere ``^[a-zA-Z0-9_]+$`` (100 caracteres maximum).
   * - ``includedPaths``
     - String
     - Non
     - Expression reguliere des chemins cibles du label. Si plusieurs valeurs sont specifees, elles sont separees par un saut de ligne (``\n``).
   * - ``excludedPaths``
     - String
     - Non
     - Expression reguliere des chemins a exclure du label. Si plusieurs valeurs sont specifees, elles sont separees par un saut de ligne (``\n``).
   * - ``permissions``
     - String
     - Non
     - Roles, groupes ou utilisateurs autorises a acceder (ex. : ``{role}admin``). Si plusieurs valeurs sont specifees, elles sont separees par un saut de ligne (``\n``).
   * - ``sortOrder``
     - Integer
     - Non
     - Ordre d'affichage (entier superieur ou egal a 0). La valeur par defaut est ``0``.
   * - ``virtualHost``
     - String
     - Non
     - Hote virtuel (1000 caracteres maximum).

.. note::

   Les champs d'audit tels que ``createdBy`` / ``createdTime`` sont definis
   automatiquement cote serveur et n'ont pas besoin d'etre specifies dans la requete.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

En cas de creation reussie, ``created`` prend la valeur ``true``.

Mise a jour d'un type de label
================================

Requete
-------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Corps de la requete
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

Lors d'une mise a jour, les champs suivants sont obligatoires en plus de ceux utilises lors de la creation.

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
     - ID du type de label a mettre a jour.
   * - ``versionNo``
     - Integer
     - Oui
     - Numero de version pour le verrouillage optimiste. Specifiez la valeur ``versionNo`` presente dans la reponse obtenue lors de la lecture. Si la version specifiee ne correspond pas a la version actuelle, la mise a jour echoue.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

Dans le cas d'une mise a jour, ``created`` prend la valeur ``false``.

Suppression d'un type de label
================================

Requete
-------

::

    DELETE /api/admin/labeltype/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
=======================

Creation d'un label pour la documentation
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

Voir aussi
===========

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../api-search` - API de recherche
- :doc:`../../admin/labeltype-guide` - Guide de gestion des types de labels
