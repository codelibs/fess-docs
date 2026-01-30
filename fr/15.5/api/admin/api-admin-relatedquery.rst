==========================
API RelatedQuery
==========================

Vue d'ensemble
==============

L'API RelatedQuery permet de gerer les requetes associees dans |Fess|.
Vous pouvez suggerer des mots-cles de recherche associes pour des requetes de recherche specifiques.

URL de base
===========

::

    /api/admin/relatedquery

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
     - Obtention de la liste des requetes associees
   * - GET
     - /setting/{id}
     - Obtention d'une requete associee
   * - POST
     - /setting
     - Creation d'une requete associee
   * - PUT
     - /setting
     - Mise a jour d'une requete associee
   * - DELETE
     - /setting/{id}
     - Suppression d'une requete associee

Obtention de la liste des requetes associees
============================================

Requete
-------

::

    GET /api/admin/relatedquery/settings
    PUT /api/admin/relatedquery/settings

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
            "id": "query_id_1",
            "term": "fess",
            "queries": ["fess tutorial", "fess installation", "fess configuration"]
          }
        ],
        "total": 5
      }
    }

Obtention d'une requete associee
================================

Requete
-------

::

    GET /api/admin/relatedquery/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": ["fess tutorial", "fess installation", "fess configuration"],
          "virtualHost": ""
        }
      }
    }

Creation d'une requete associee
===============================

Requete
-------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search"],
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
   * - ``queries``
     - Oui
     - Tableau des requetes associees
   * - ``virtualHost``
     - Non
     - Hote virtuel

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

Mise a jour d'une requete associee
==================================

Requete
-------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search", "search tips"],
      "virtualHost": "",
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

Suppression d'une requete associee
==================================

Requete
-------

::

    DELETE /api/admin/relatedquery/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_query_id",
        "created": false
      }
    }

Exemples d'utilisation
======================

Requetes associees pour les produits
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": ["product features", "product pricing", "product comparison", "product reviews"]
         }'

Requetes associees pour l'aide
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": ["help center", "help documentation", "help contact support"]
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-relatedcontent` - API des contenus associes
- :doc:`api-admin-suggest` - API de gestion des suggestions
- :doc:`../../admin/relatedquery-guide` - Guide de gestion des requetes associees
