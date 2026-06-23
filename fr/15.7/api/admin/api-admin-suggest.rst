==========================
Suggest API
==========================

Vue d'ensemble
==============

L'API Suggest est une API permettant de gérer les mots de suggestion utilisés par la fonctionnalité de suggestion de |Fess|.
Elle permet d'obtenir des informations statistiques sur le nombre de mots de suggestion et de supprimer des mots de suggestion.

Les mots de suggestion se divisent en deux catégories : ceux générés à partir des documents crawlés (issus des documents)
et ceux générés à partir des requêtes de recherche des utilisateurs (issus des requêtes de recherche). Cette API permet
de les supprimer par catégorie ou de les supprimer tous ensemble.

Authentification
================

L'accès à cette API nécessite une authentification par jeton d'accès. Veuillez spécifier le jeton d'accès dans l'en-tête de la requête.

::

    Authorization: Bearer <jeton d'accès>

Le jeton d'accès doit disposer des droits de l'API Admin (par défaut ``Radmin-api``).
Pour plus d'informations sur l'obtention d'un jeton d'accès et les détails des droits, consultez :doc:`api-admin-overview`.

URL de base
===========

::

    /api/admin/suggest

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
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
     - Suppression des mots de suggestion issus des requêtes de recherche

Obtention des informations statistiques sur les mots de suggestion
==================================================================

Obtient les informations statistiques relatives au nombre de mots de suggestion.

Requête
-------

::

    GET /api/admin/suggest

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
        }
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``setting.totalWordsNum``
     - Nombre total de mots de suggestion (nombre de mots de suggestion enregistrés dans l'index de suggestion)
   * - ``setting.documentWordsNum``
     - Nombre de mots de suggestion issus des documents (nombre de mots de suggestion dont la fréquence documentaire est supérieure ou égale à 1)
   * - ``setting.queryWordsNum``
     - Nombre de mots de suggestion issus des requêtes de recherche (nombre de mots de suggestion dont la fréquence de requête est supérieure ou égale à 1)

.. note::

   ``documentWordsNum`` et ``queryWordsNum`` ne sont pas exclusifs l'un de l'autre. Si un mot de suggestion est issu
   à la fois d'un document et d'une requête de recherche, il est comptabilisé dans les deux totaux. Par conséquent,
   la somme de ``documentWordsNum`` et de ``queryWordsNum`` peut ne pas correspondre à ``totalWordsNum``.

Suppression de tous les mots de suggestion
==========================================

Supprime tous les mots de suggestion. Tous les mots de suggestion présents dans l'index de suggestion sont concernés,
qu'ils soient issus de documents ou de requêtes de recherche.

Requête
-------

::

    DELETE /api/admin/suggest/all

Réponse
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

Supprime les mots de suggestion générés à partir des documents (mots de suggestion issus des documents).

Requête
-------

::

    DELETE /api/admin/suggest/document

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Suppression des mots de suggestion issus des requêtes de recherche
==================================================================

Supprime les mots de suggestion générés à partir des requêtes de recherche (mots de suggestion issus des requêtes de recherche).

Requête
-------

::

    DELETE /api/admin/suggest/query

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

En cas d'échec d'une opération de suppression, un statut HTTP ``400`` est retourné. Le champ ``status`` du corps de la réponse
est défini à ``1`` (BAD_REQUEST) et le champ ``message`` contient le message d'erreur.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

Si le jeton d'accès est absent ou invalide, ou si les droits sont insuffisants, le champ ``status`` du corps de la réponse
est défini à ``3`` (UNAUTHORIZED). Pour la liste des valeurs de ``status`` et des codes de statut HTTP,
consultez :doc:`api-admin-overview`.

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

Suppression des mots de suggestion issus des requêtes de recherche
------------------------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-badword` - API des mots interdits
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/suggest-guide` - Guide de gestion des suggestions
