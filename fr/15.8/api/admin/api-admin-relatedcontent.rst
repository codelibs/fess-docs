==========================
RelatedContent API
==========================

Vue d'ensemble
==============

L'API RelatedContent est une API permettant de gerer les contenus associes dans |Fess|.
Vous pouvez afficher des contenus personnalises associes a des mots-cles specifiques.

URL de base
===========

::

    /api/admin/relatedcontent

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
     - Lister les contenus associes
   * - GET
     - /setting/{id}
     - Obtenir un contenu associe
   * - POST
     - /setting
     - Creer un contenu associe
   * - PUT
     - /setting
     - Mettre a jour un contenu associe
   * - DELETE
     - /setting/{id}
     - Supprimer un contenu associe

Lister les contenus associes
============================

Requete
-------

::

    GET /api/admin/relatedcontent/settings

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
     - Nombre d'elements par page (par defaut : 25 ; modifiable via ``paging.page.size`` du fichier ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 1 ; par defaut : 1 ; une valeur inferieure ou egale a 0 est traitee comme 1)
   * - ``term``
     - String
     - Non
     - Filtrer par mot-cle de recherche (recherche avec caracteres generiques)
   * - ``content``
     - String
     - Non
     - Filtrer par contenu (recherche avec caracteres generiques)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

   Chaque element de ``settings`` ainsi que l'objet ``setting`` retourne par
   l'endpoint d'obtention contiennent les champs de l'entite stockee tels quels.
   En plus de ``term``, ``content``, ``sortOrder`` et ``virtualHost``, les champs
   d'audit ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` ainsi que
   le champ de verrouillage optimiste ``versionNo`` sont egalement retournes.
   ``createdTime`` et ``updatedTime`` sont exprimes en millisecondes depuis l'epoque
   (nombres). Les champs non renseignes (null) sont omis de la reponse. De plus,
   l'objet ``response`` de toutes les reponses contient toujours ``version``, qui
   indique la version du produit (voir :doc:`api-admin-overview` pour les details).

Obtenir un contenu associe
==========================

Requete
-------

::

    GET /api/admin/relatedcontent/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

   La valeur de ``versionNo`` requise lors d'une mise a jour (PUT) est celle
   incluse dans cette reponse d'obtention.

Creer un contenu associe
========================

Requete
-------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

Corps de la requete
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
     - Mot-cle de recherche (maximum 10000 caracteres)
   * - ``content``
     - **Oui**
     - Contenu HTML a afficher (maximum 10000 caracteres)
   * - ``sortOrder``
     - **Non**
     - Ordre d'affichage (entier compris entre 0 et 2147483647)
   * - ``virtualHost``
     - **Non**
     - Hote virtuel (maximum 1000 caracteres)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Mettre a jour un contenu associe
=================================

Requete
-------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

Corps de la requete
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
     - Identifiant du contenu associe a mettre a jour (maximum 1000 caracteres)
   * - ``term``
     - **Oui**
     - Mot-cle de recherche (maximum 10000 caracteres)
   * - ``content``
     - **Oui**
     - Contenu HTML a afficher (maximum 10000 caracteres)
   * - ``sortOrder``
     - **Non**
     - Ordre d'affichage (entier compris entre 0 et 2147483647)
   * - ``virtualHost``
     - **Non**
     - Hote virtuel (maximum 1000 caracteres)
   * - ``versionNo``
     - **Oui**
     - Numero de version pour le verrouillage optimiste. Specifier la valeur incluse dans la reponse de ``setting/{id}``.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   Les champs d'audit tels que ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` et ``crudMode`` sont ignores meme s'ils sont inclus dans le
   corps de la requete, car ils sont definis automatiquement cote serveur. Il
   n'est pas necessaire de les specifier lors de la creation ou de la mise a jour.

Supprimer un contenu associe
============================

Requete
-------

::

    DELETE /api/admin/relatedcontent/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Exemples d'utilisation
======================

Contenu associe pour les informations produit
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

Contenu associe pour les informations de support
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

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-relatedquery` - API des requetes associees
- :doc:`../../admin/relatedcontent-guide` - Guide de gestion des contenus associes
