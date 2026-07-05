==========================
API RelatedContent
==========================

Vue d'ensemble
==============

L'API RelatedContent permet de gerer les contenus associes dans |Fess|.
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
   * - GET/PUT
     - /settings
     - Obtention de la liste des contenus associes
   * - GET
     - /setting/{id}
     - Obtention d'un contenu associe
   * - POST
     - /setting
     - Creation d'un contenu associe
   * - PUT
     - /setting
     - Mise a jour d'un contenu associe
   * - DELETE
     - /setting/{id}
     - Suppression d'un contenu associe

Obtention de la liste des contenus associes
===========================================

Requete
-------

::

    GET /api/admin/relatedcontent/settings
    PUT /api/admin/relatedcontent/settings

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
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtention d'un contenu associe
==============================

Requete
-------

::

    GET /api/admin/relatedcontent/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "sortOrder": 0,
          "virtualHost": ""
        }
      }
    }

Creation d'un contenu associe
=============================

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
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``term``
     - Oui
     - Mot-cle de recherche
   * - ``content``
     - Oui
     - Contenu HTML a afficher
   * - ``sortOrder``
     - Non
     - Ordre d'affichage
   * - ``virtualHost``
     - Non
     - Hote virtuel

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

Mise a jour d'un contenu associe
================================

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

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

Suppression d'un contenu associe
================================

Requete
-------

::

    DELETE /api/admin/relatedcontent/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_content_id",
        "created": false
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
