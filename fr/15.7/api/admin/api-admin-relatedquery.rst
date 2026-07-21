==========================
API RelatedQuery
==========================

Vue d'ensemble
==============

L'API RelatedQuery est une API permettant de gérer les requêtes associées dans |Fess|.
Pour un mot-clé de recherche saisi par l'utilisateur (``term``), vous pouvez enregistrer et
gérer des suggestions de mots-clés de recherche associés (``queries``). Les requêtes associées
enregistrées sont affichées comme suggestions de recherche associées sur l'écran de recherche.

Pour les détails sur l'authentification, le format de réponse commun (champ ``version`` et
codes ``status``), la pagination et les réponses d'erreur, consultez :doc:`api-admin-overview`.

URL de base
===========

::

    /api/admin/relatedquery

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
     - Obtention de la liste des requêtes associées
   * - GET
     - /setting/{id}
     - Obtention d'une requête associée
   * - POST
     - /setting
     - Création d'une requête associée
   * - PUT
     - /setting
     - Mise à jour d'une requête associée
   * - DELETE
     - /setting/{id}
     - Suppression d'une requête associée

Obtention de la liste des requêtes associées
============================================

Requête
-------

::

    GET /api/admin/relatedquery/settings

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
     - Nombre d'éléments par page (par défaut : 25 ; modifiable via ``paging.page.size`` du fichier ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1 ; par défaut : 1)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Chaque paramètre contient ``versionNo`` (numéro de version utilisé pour le verrouillage
   optimiste). ``virtualHost`` et les champs d'audit (``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime``) ne sont inclus que lorsqu'une valeur est définie.
   Un ``virtualHost`` vide n'est pas inclus dans la réponse.

Obtention d'une requête associée
=================================

Requête
-------

::

    GET /api/admin/relatedquery/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

Création d'une requête associée
================================

Requête
-------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``term``
     - Oui
     - Mot-clé de recherche (10 000 caractères maximum)
   * - ``queries``
     - Oui
     - Requêtes associées. Chaîne séparée par des sauts de ligne, une par ligne (les lignes vides sont ignorées ; 10 000 caractères maximum)
   * - ``virtualHost``
     - Non
     - Hôte virtuel (1 000 caractères maximum)

.. note::

   ``crudMode`` étant défini automatiquement côté API, il n'est pas nécessaire de l'inclure dans le corps de la requête.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Mise à jour d'une requête associée
===================================

Requête
-------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
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
     - ID de la requête associée à mettre à jour (1 000 caractères maximum)
   * - ``term``
     - Oui
     - Mot-clé de recherche (10 000 caractères maximum)
   * - ``queries``
     - Oui
     - Requêtes associées. Chaîne séparée par des sauts de ligne, une par ligne (les lignes vides sont ignorées ; 10 000 caractères maximum)
   * - ``virtualHost``
     - Non
     - Hôte virtuel (1 000 caractères maximum)
   * - ``versionNo``
     - Oui
     - Numéro de version utilisé pour le verrouillage optimiste. Spécifiez la valeur incluse dans la réponse lors de l'obtention du paramètre

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Suppression d'une requête associée
====================================

Requête
-------

::

    DELETE /api/admin/relatedquery/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Réponse d'erreur
================

En cas d'échec de la requête, ``status`` est défini sur une valeur différente de 0 et
``message`` contient le détail de l'erreur. Par exemple, pour une erreur de validation
telle qu'un champ obligatoire manquant, ``status`` vaut ``1``. Pour la liste des codes
de statut, consultez :doc:`api-admin-overview`.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "..."
      }
    }

Exemples d'utilisation
======================

Requêtes associées pour les produits
-------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

Requêtes associées pour l'aide
-------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-relatedcontent` - API des contenus associés
- :doc:`api-admin-suggest` - API de gestion des suggestions
- :doc:`../../admin/relatedquery-guide` - Guide de gestion des requêtes associées
