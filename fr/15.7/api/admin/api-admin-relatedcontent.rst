==========================
RelatedContent API
==========================

Vue d'ensemble
==============

L'API RelatedContent est une API permettant de gérer les contenus associés dans |Fess|.
Vous pouvez afficher des contenus personnalisés associés à des mots-clés spécifiques.

URL de base
===========

::

    /api/admin/relatedcontent

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
     - Lister les contenus associés
   * - GET
     - /setting/{id}
     - Obtenir un contenu associé
   * - POST
     - /setting
     - Créer un contenu associé
   * - PUT
     - /setting
     - Mettre à jour un contenu associé
   * - DELETE
     - /setting/{id}
     - Supprimer un contenu associé

Lister les contenus associés
============================

Requête
-------

::

    GET /api/admin/relatedcontent/settings

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
     - Numéro de page (commence à 1 ; par défaut : 1 ; une valeur inférieure ou égale à 0 est traitée comme 1)
   * - ``term``
     - String
     - Non
     - Filtrer par mot-clé de recherche (recherche avec caractères génériques)
   * - ``content``
     - String
     - Non
     - Filtrer par contenu (recherche avec caractères génériques)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
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

   Chaque élément de ``settings`` ainsi que l'objet ``setting`` retourné par
   l'endpoint d'obtention contiennent les champs de l'entité stockée tels quels.
   En plus de ``term``, ``content``, ``sortOrder`` et ``virtualHost``, les champs
   d'audit ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` ainsi que
   le champ de verrouillage optimiste ``versionNo`` sont également retournés.
   ``createdTime`` et ``updatedTime`` sont exprimés en millisecondes depuis l'époque
   (nombres). Les champs non renseignés (null) sont omis de la réponse. De plus,
   l'objet ``response`` de toutes les réponses contient toujours ``version``, qui
   indique la version du produit (voir :doc:`api-admin-overview` pour les détails).

Obtenir un contenu associé
==========================

Requête
-------

::

    GET /api/admin/relatedcontent/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
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

.. note::

   La valeur de ``versionNo`` requise lors d'une mise à jour (PUT) est celle
   incluse dans cette réponse d'obtention.

Créer un contenu associé
========================

Requête
-------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Champ
     - Requis
     - Description
   * - ``term``
     - **Oui**
     - Mot-clé de recherche (maximum 10000 caractères)
   * - ``content``
     - **Oui**
     - Contenu HTML à afficher (maximum 10000 caractères)
   * - ``sortOrder``
     - **Non**
     - Ordre d'affichage (entier compris entre 0 et 2147483647)
   * - ``virtualHost``
     - **Non**
     - Hôte virtuel (maximum 1000 caractères)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Mettre à jour un contenu associé
=================================

Requête
-------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
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
     - **Oui**
     - Identifiant du contenu associé à mettre à jour (maximum 1000 caractères)
   * - ``term``
     - **Oui**
     - Mot-clé de recherche (maximum 10000 caractères)
   * - ``content``
     - **Oui**
     - Contenu HTML à afficher (maximum 10000 caractères)
   * - ``sortOrder``
     - **Non**
     - Ordre d'affichage (entier compris entre 0 et 2147483647)
   * - ``virtualHost``
     - **Non**
     - Hôte virtuel (maximum 1000 caractères)
   * - ``versionNo``
     - **Oui**
     - Numéro de version pour le verrouillage optimiste. Spécifier la valeur incluse dans la réponse de ``setting/{id}``.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   Les champs d'audit tels que ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` et ``crudMode`` sont ignorés même s'ils sont inclus dans le
   corps de la requête, car ils sont définis automatiquement côté serveur. Il
   n'est pas nécessaire de les spécifier lors de la création ou de la mise à jour.

Supprimer un contenu associé
============================

Requête
-------

::

    DELETE /api/admin/relatedcontent/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Exemples d'utilisation
======================

Contenu associé pour les informations produit
---------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

Contenu associé pour les informations de support
------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-relatedquery` - API des requêtes associées
- :doc:`../../admin/relatedcontent-guide` - Guide de gestion des contenus associés
