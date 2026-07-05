==========================
API ElevateWord
==========================

Vue d'ensemble
==============

L'API ElevateWord permet de gerer les mots eleves (manipulation du classement de recherche pour des mots-cles specifiques) dans |Fess|.
Vous pouvez placer des documents specifiques en haut ou en bas des resultats pour certaines requetes de recherche.

URL de base
===========

::

    /api/admin/elevateword

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
     - Obtention de la liste des mots eleves
   * - GET
     - /setting/{id}
     - Obtention d'un mot eleve
   * - POST
     - /setting
     - Creation d'un mot eleve
   * - PUT
     - /setting
     - Mise a jour d'un mot eleve
   * - DELETE
     - /setting/{id}
     - Suppression d'un mot eleve
   * - PUT
     - /upload
     - Televersement CSV des mots eleves
   * - GET
     - /download
     - Telechargement CSV des mots eleves

Obtention de la liste des mots eleves
=====================================

Requete
-------

::

    GET /api/admin/elevateword/settings

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
     - Numero de page (commence a 1, par defaut : 1)
   * - ``id``
     - String
     - Non
     - Filtre par correspondance exacte sur l'ID du mot eleve

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "フェス",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

Obtention d'un mot eleve
========================

Requete
-------

::

    GET /api/admin/elevateword/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "フェス",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

Creation d'un mot eleve
=======================

Requete
-------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "ドキュメンテーション",
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
     - Mot-cle a elever
   * - ``reading``
     - Non
     - Lecture phonetique
   * - ``permissions``
     - Non
     - Permissions d'acces (chaine separee par des sauts de ligne, une par ligne. Valeur initiale du formulaire : permissions d'affichage par defaut de la recherche)
   * - ``boost``
     - Oui
     - Valeur de boost (valeur initiale du formulaire : 100.0)
   * - ``labelTypeIds``
     - Non
     - ID des labels cibles (tableau de chaines)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

Mise a jour d'un mot eleve
==========================

Requete
-------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "ドキュメンテーション",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

.. note::

   Lors de la mise a jour, les champs suivants sont requis en plus des champs utilises pour la creation :

   - ``id`` - ID du mot eleve a mettre a jour
   - ``versionNo`` - Numero de version pour le verrouillage optimiste. Indiquez la valeur obtenue via ``GET /setting/{id}``.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

Suppression d'un mot eleve
==========================

Requete
-------

::

    DELETE /api/admin/elevateword/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

Televersement CSV des mots eleves
=================================

Enregistre en masse des mots eleves depuis un fichier CSV. Le fichier est envoye en ``multipart/form-data``. L'import est execute de maniere asynchrone cote serveur.

Requete
-------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``elevateWordFile``
     - Oui
     - Fichier CSV des mots eleves a televerser

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Telechargement CSV des mots eleves
==================================

Telecharge les mots eleves enregistres sous forme de fichier CSV (``elevate.csv``). La reponse est un flux ``application/octet-stream``.

Requete
-------

::

    GET /api/admin/elevateword/download

Exemples d'utilisation
======================

Elevation d'un nom de produit
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

Elevation vers un label specifique
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

Televersement d'un fichier CSV
------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

Telechargement d'un fichier CSV
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-keymatch` - API KeyMatch
- :doc:`api-admin-boostdoc` - API BoostDoc
- :doc:`../../admin/elevateword-guide` - Guide de gestion des mots eleves
