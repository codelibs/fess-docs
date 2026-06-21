==========================
API RelatedQuery
==========================

Vue d'ensemble
==============

L'API RelatedQuery est une API permettant de gerer les requetes associees dans |Fess|.
Pour un mot-cle de recherche saisi par l'utilisateur (``term``), vous pouvez enregistrer et
gerer des suggestions de mots-cles de recherche associes (``queries``). Les requetes associees
enregistrees sont affichees comme suggestions de recherche associees sur l'ecran de recherche.

Pour les details sur l'authentification, le format de reponse commun (champ ``version`` et
codes ``status``), la pagination et les reponses d'erreur, consultez :doc:`api-admin-overview`.

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
   * - GET
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
     - Numero de page (commence a 1 ; par defaut : 1)

Reponse
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

   Chaque parametre contient ``versionNo`` (numero de version utilise pour le verrouillage
   optimiste). ``virtualHost`` et les champs d'audit (``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime``) ne sont inclus que lorsqu'une valeur est definie.
   Un ``virtualHost`` vide n'est pas inclus dans la reponse.

Obtention d'une requete associee
=================================

Requete
-------

::

    GET /api/admin/relatedquery/setting/{id}

Reponse
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

Creation d'une requete associee
================================

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
     - Mot-cle de recherche (10 000 caracteres maximum)
   * - ``queries``
     - Oui
     - Requetes associees. Chaine separee par des sauts de ligne, une par ligne (les lignes vides sont ignorees ; 10 000 caracteres maximum)
   * - ``virtualHost``
     - Non
     - Hote virtuel (1 000 caracteres maximum)

.. note::

   ``crudMode`` etant defini automatiquement cote API, il n'est pas necessaire de l'inclure dans le corps de la requete.

Reponse
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

Mise a jour d'une requete associee
===================================

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
     - ID de la requete associee a mettre a jour (1 000 caracteres maximum)
   * - ``term``
     - Oui
     - Mot-cle de recherche (10 000 caracteres maximum)
   * - ``queries``
     - Oui
     - Requetes associees. Chaine separee par des sauts de ligne, une par ligne (les lignes vides sont ignorees ; 10 000 caracteres maximum)
   * - ``virtualHost``
     - Non
     - Hote virtuel (1 000 caracteres maximum)
   * - ``versionNo``
     - Oui
     - Numero de version utilise pour le verrouillage optimiste. Specifiez la valeur incluse dans la reponse lors de l'obtention du parametre

Reponse
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

Suppression d'une requete associee
====================================

Requete
-------

::

    DELETE /api/admin/relatedquery/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Reponse d'erreur
================

En cas d'echec de la requete, ``status`` est defini sur une valeur differente de 0 et
``message`` contient le detail de l'erreur. Par exemple, pour une erreur de validation
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

Requetes associees pour les produits
-------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

Requetes associees pour l'aide
-------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-relatedcontent` - API des contenus associes
- :doc:`api-admin-suggest` - API de gestion des suggestions
- :doc:`../../admin/relatedquery-guide` - Guide de gestion des requetes associees
