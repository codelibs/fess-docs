==========================
API Suggest
==========================

Vue d'ensemble
==============

L'API Suggest permet de gerer la fonctionnalite de suggestion de |Fess|.
Vous pouvez ajouter, supprimer et mettre a jour les mots de suggestion.

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
   * - GET/PUT
     - /settings
     - Obtention de la liste des mots de suggestion
   * - GET
     - /setting/{id}
     - Obtention d'un mot de suggestion
   * - POST
     - /setting
     - Creation d'un mot de suggestion
   * - PUT
     - /setting
     - Mise a jour d'un mot de suggestion
   * - DELETE
     - /setting/{id}
     - Suppression d'un mot de suggestion
   * - DELETE
     - /delete-all
     - Suppression de tous les mots de suggestion

Obtention de la liste des mots de suggestion
============================================

Requete
-------

::

    GET /api/admin/suggest/settings
    PUT /api/admin/suggest/settings

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
            "id": "suggest_id_1",
            "text": "fess",
            "reading": "fess",
            "fields": ["title", "content"],
            "tags": ["product"],
            "roles": ["guest"],
            "lang": "ja",
            "score": 1.0
          }
        ],
        "total": 100
      }
    }

Obtention d'un mot de suggestion
================================

Requete
-------

::

    GET /api/admin/suggest/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "suggest_id_1",
          "text": "fess",
          "reading": "fess",
          "fields": ["title", "content"],
          "tags": ["product"],
          "roles": ["guest"],
          "lang": "ja",
          "score": 1.0
        }
      }
    }

Creation d'un mot de suggestion
===============================

Requete
-------

::

    POST /api/admin/suggest/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "text": "search engine",
      "reading": "search engine",
      "fields": ["title"],
      "tags": ["feature"],
      "roles": ["guest"],
      "lang": "en",
      "score": 1.0
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``text``
     - Oui
     - Texte de suggestion
   * - ``reading``
     - Non
     - Lecture phonetique
   * - ``fields``
     - Non
     - Champs cibles
   * - ``tags``
     - Non
     - Tags
   * - ``roles``
     - Non
     - Roles autorises
   * - ``lang``
     - Non
     - Code de langue
   * - ``score``
     - Non
     - Score (par defaut : 1.0)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_suggest_id",
        "created": true
      }
    }

Mise a jour d'un mot de suggestion
==================================

Requete
-------

::

    PUT /api/admin/suggest/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_suggest_id",
      "text": "search engine",
      "reading": "search engine",
      "fields": ["title", "content"],
      "tags": ["feature", "popular"],
      "roles": ["guest"],
      "lang": "en",
      "score": 2.0,
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_suggest_id",
        "created": false
      }
    }

Suppression d'un mot de suggestion
==================================

Requete
-------

::

    DELETE /api/admin/suggest/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_suggest_id",
        "created": false
      }
    }

Suppression de tous les mots de suggestion
==========================================

Requete
-------

::

    DELETE /api/admin/suggest/delete-all

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "count": 250
      }
    }

Exemples d'utilisation
======================

Ajout d'un mot-cle populaire
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/suggest/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "getting started",
           "fields": ["title"],
           "tags": ["tutorial"],
           "roles": ["guest"],
           "lang": "en",
           "score": 5.0
         }'

Suppression en masse des suggestions
------------------------------------

.. code-block:: bash

    # Supprimer toutes les suggestions
    curl -X DELETE "http://localhost:8080/api/admin/suggest/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-badword` - API des mots interdits
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/suggest-guide` - Guide de gestion des suggestions
