==========================
API BoostDoc
==========================

Vue d'ensemble
==============

L'API BoostDoc permet de gerer les parametres de boost de documents dans |Fess|.
Vous pouvez ajuster le classement de recherche des documents correspondant a des conditions specifiques.

URL de base
===========

::

    /api/admin/boostdoc

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
     - Obtention de la liste des boosts de documents
   * - GET
     - /setting/{id}
     - Obtention d'un boost de document
   * - POST
     - /setting
     - Creation d'un boost de document
   * - PUT
     - /setting
     - Mise a jour d'un boost de document
   * - DELETE
     - /setting/{id}
     - Suppression d'un boost de document

Obtention de la liste des boosts de documents
=============================================

Requete
-------

::

    GET /api/admin/boostdoc/settings
    PUT /api/admin/boostdoc/settings

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
            "id": "boostdoc_id_1",
            "urlExpr": ".*docs\\.example\\.com.*",
            "boostExpr": "3.0",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtention d'un boost de document
================================

Requete
-------

::

    GET /api/admin/boostdoc/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": ".*docs\\.example\\.com.*",
          "boostExpr": "3.0",
          "sortOrder": 0
        }
      }
    }

Creation d'un boost de document
===============================

Requete
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``urlExpr``
     - Oui
     - Pattern regex de l'URL
   * - ``boostExpr``
     - Oui
     - Expression de boost (valeur ou formule)
   * - ``sortOrder``
     - Non
     - Ordre d'application

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Mise a jour d'un boost de document
==================================

Requete
-------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Suppression d'un boost de document
==================================

Requete
-------

::

    DELETE /api/admin/boostdoc/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_boostdoc_id",
        "created": false
      }
    }

Exemples d'expressions de boost
===============================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Expression de boost
     - Description
   * - ``2.0``
     - Boost avec une valeur fixe
   * - ``doc['boost'].value * 2``
     - Double la valeur de boost du document
   * - ``Math.log(doc['click_count'].value + 1)``
     - Boost logarithmique base sur le nombre de clics
   * - ``doc['last_modified'].value > now - 7d ? 3.0 : 1.0``
     - Triple si mis a jour dans la derniere semaine

Exemples d'utilisation
======================

Boost pour le site de documentation
-----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*docs\\.example\\.com.*",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

Boost pour le nouveau contenu
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*",
           "boostExpr": "doc[\"last_modified\"].value > now - 30d ? 2.0 : 1.0",
           "sortOrder": 10
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/boostdoc-guide` - Guide de gestion des boosts de documents
