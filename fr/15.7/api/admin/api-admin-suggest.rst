==========================
API Suggest
==========================

Vue d'ensemble
==============

L'API Suggest est une API permettant de gerer la fonctionnalite de suggestion de |Fess|.
Vous pouvez obtenir des informations statistiques sur les mots de suggestion et supprimer des mots de suggestion.

URL de base
===========

::

    /api/admin/suggest

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention des informations statistiques sur les mots de suggestion
   * - DELETE
     - /all
     - Suppression de tous les mots de suggestion
   * - DELETE
     - /document
     - Suppression des mots de suggestion issus des documents
   * - DELETE
     - /query
     - Suppression des mots de suggestion issus des requetes de recherche

Obtention des informations statistiques sur les mots de suggestion
==================================================================

Obtient les informations statistiques relatives au nombre de mots de suggestion.

Requete
-------

::

    GET /api/admin/suggest

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 300
        }
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``setting.totalWordsNum``
     - Nombre total de mots de suggestion
   * - ``setting.documentWordsNum``
     - Nombre de mots de suggestion issus des documents
   * - ``setting.queryWordsNum``
     - Nombre de mots de suggestion issus des requetes de recherche

Suppression de tous les mots de suggestion
==========================================

Supprime tous les mots de suggestion.

Requete
-------

::

    DELETE /api/admin/suggest/all

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression des mots de suggestion issus des documents
======================================================

Supprime les mots de suggestion generes a partir des documents.

Requete
-------

::

    DELETE /api/admin/suggest/document

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression des mots de suggestion issus des requetes de recherche
==================================================================

Supprime les mots de suggestion generes a partir des requetes de recherche.

Requete
-------

::

    DELETE /api/admin/suggest/query

Reponse
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

Obtention des informations statistiques
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression de tous les mots de suggestion
------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression des mots de suggestion issus des documents
------------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-badword` - API des mots interdits
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/suggest-guide` - Guide de gestion des suggestions
