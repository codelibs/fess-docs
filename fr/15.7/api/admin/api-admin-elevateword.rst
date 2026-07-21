==========================
API ElevateWord
==========================

Vue d'ensemble
==============

L'API ElevateWord permet de gérer les mots élevés (manipulation du classement de recherche pour des mots-clés spécifiques) dans |Fess|.
Vous pouvez placer des documents spécifiques en haut ou en bas des résultats pour certaines requêtes de recherche.

URL de base
===========

::

    /api/admin/elevateword

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
     - Obtention de la liste des mots élevés
   * - GET
     - /setting/{id}
     - Obtention d'un mot élevé
   * - POST
     - /setting
     - Création d'un mot élevé
   * - PUT
     - /setting
     - Mise à jour d'un mot élevé
   * - DELETE
     - /setting/{id}
     - Suppression d'un mot élevé
   * - PUT
     - /upload
     - Téléversement CSV des mots élevés
   * - GET
     - /download
     - Téléchargement CSV des mots élevés

Obtention de la liste des mots élevés
=====================================

Requête
-------

::

    GET /api/admin/elevateword/settings

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
     - Nombre d'éléments par page (par défaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1)
   * - ``id``
     - String
     - Non
     - Filtre par correspondance exacte sur l'ID du mot élevé

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

Obtention d'un mot élevé
========================

Requête
-------

::

    GET /api/admin/elevateword/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

Création d'un mot élevé
=======================

Requête
-------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``suggestWord``
     - Oui
     - Mot-clé à élever
   * - ``reading``
     - Non
     - Lecture phonétique
   * - ``permissions``
     - Non
     - Permissions d'accès (chaîne séparée par des sauts de ligne, une par ligne. Valeur initiale du formulaire : permissions d'affichage par défaut de la recherche)
   * - ``boost``
     - Oui
     - Valeur de boost (valeur initiale du formulaire : 100.0)
   * - ``labelTypeIds``
     - Non
     - ID des labels cibles (tableau de chaînes)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

Mise à jour d'un mot élevé
==========================

Requête
-------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   Lors de la mise à jour, les champs suivants sont requis en plus des champs utilisés pour la création :

   - ``id`` - ID du mot élevé à mettre à jour
   - ``versionNo`` - Numéro de version pour le verrouillage optimiste. Indiquez la valeur obtenue via ``GET /setting/{id}``.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

Suppression d'un mot élevé
==========================

Requête
-------

::

    DELETE /api/admin/elevateword/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

Téléversement CSV des mots élevés
=================================

Enregistre en masse des mots élevés depuis un fichier CSV. Le fichier est envoyé en ``multipart/form-data``. L'import est exécuté de manière asynchrone côté serveur.

Requête
-------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``elevateWordFile``
     - Oui
     - Fichier CSV des mots élevés à téléverser

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Téléchargement CSV des mots élevés
==================================

Télécharge les mots élevés enregistrés sous forme de fichier CSV (``elevate.csv``). La réponse est un flux ``application/octet-stream``.

Requête
-------

::

    GET /api/admin/elevateword/download

Exemples d'utilisation
======================

Élévation d'un nom de produit
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

Élévation vers un label spécifique
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

Téléversement d'un fichier CSV
------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

Téléchargement d'un fichier CSV
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-keymatch` - API KeyMatch
- :doc:`api-admin-boostdoc` - API BoostDoc
- :doc:`../../admin/elevateword-guide` - Guide de gestion des mots élevés
