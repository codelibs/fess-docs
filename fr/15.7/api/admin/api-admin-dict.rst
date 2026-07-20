==========================
API Dict
==========================

Vue d'ensemble
==============

L'API Dict est une API permettant de gérer les dictionnaires de |Fess|.
L'endpoint racine permet d'obtenir la liste des dictionnaires disponibles.
La consultation, la création, la mise à jour et la suppression des entrées de dictionnaire individuelles, ainsi que le téléversement et le téléchargement des fichiers de dictionnaire, s'effectuent via les sous-endpoints propres à chaque type de dictionnaire (synonym, kuromoji, mapping, protwords, stopwords, stemmeroverride).

URL de base
===========

::

    /api/admin/dict

Liste des endpoints
===================

Racine des dictionnaires
------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention de la liste des dictionnaires

Endpoints propres à chaque type de dictionnaire
-----------------------------------------------

``{type}`` doit être l'une des valeurs suivantes : ``synonym`` , ``kuromoji`` , ``mapping`` , ``protwords`` , ``stopwords`` , ``stemmeroverride`` .
Ces valeurs correspondent à la valeur du champ ``type`` inclus dans la réponse de la liste des dictionnaires.
``{dictId}`` est l'ID du dictionnaire obtenu via l'obtention de la liste des dictionnaires.

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /{type}/settings/{dictId}
     - Obtention de la liste des entrées de dictionnaire
   * - GET
     - /{type}/setting/{dictId}/{id}
     - Obtention d'une entrée de dictionnaire
   * - POST
     - /{type}/setting/{dictId}
     - Création d'une entrée de dictionnaire
   * - PUT
     - /{type}/setting/{dictId}
     - Mise à jour d'une entrée de dictionnaire
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - Suppression d'une entrée de dictionnaire
   * - PUT
     - /{type}/upload/{dictId}
     - Téléversement d'un fichier de dictionnaire
   * - GET
     - /{type}/download/{dictId}
     - Téléchargement d'un fichier de dictionnaire

Obtention de la liste des dictionnaires
=======================================

Obtient la liste des fichiers de dictionnaire disponibles.

Requête
-------

::

    GET /api/admin/dict

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
          }
        ],
        "total": 2
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``settings[].id``
     - ID du dictionnaire (utilisé comme ``{dictId}`` dans les opérations sur les dictionnaires individuels)
   * - ``settings[].type``
     - Type de dictionnaire
   * - ``settings[].path``
     - Chemin du fichier de dictionnaire
   * - ``settings[].timestamp``
     - Date et heure de mise à jour du fichier de dictionnaire
   * - ``total``
     - Nombre total de fichiers de dictionnaire

Obtention de la liste des entrées de dictionnaire
=================================================

Obtient la liste des entrées du dictionnaire spécifié.

Requête
-------

::

    GET /api/admin/dict/{type}/settings/{dictId}

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``dictId``
     - String
     - Oui
     - ID du dictionnaire (paramètre de chemin)
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page (défaut : 25)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, défaut : 1)

Réponse
-------

Les champs de chaque élément du tableau ``settings`` de la réponse varient selon le type de dictionnaire (voir « Champs des entrées par type de dictionnaire » ci-dessous).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "検索,サーチ",
            "outputs": "検索,サーチ,リサーチ"
          }
        ],
        "total": 1
      }
    }

L'exemple ci-dessus correspond au dictionnaire ``synonym``.

Obtention d'une entrée de dictionnaire
======================================

Obtient une entrée spécifique du dictionnaire.

Requête
-------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``dictId``
     - String
     - Oui
     - ID du dictionnaire (paramètre de chemin)
   * - ``id``
     - Long
     - Oui
     - ID de l'entrée (paramètre de chemin)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

Création d'une entrée de dictionnaire
=====================================

Crée une nouvelle entrée dans le dictionnaire.

Requête
-------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Corps de la requête (exemple synonym)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

Mise à jour d'une entrée de dictionnaire
========================================

Met à jour une entrée existante du dictionnaire.

Requête
-------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Corps de la requête (exemple synonym)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Suppression d'une entrée de dictionnaire
========================================

Supprime une entrée du dictionnaire.

Requête
-------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``dictId``
     - String
     - Oui
     - ID du dictionnaire (paramètre de chemin)
   * - ``id``
     - Long
     - Oui
     - ID de l'entrée (paramètre de chemin)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Téléversement d'un fichier de dictionnaire
==========================================

Téléverse et remplace l'intégralité du fichier de dictionnaire.

Requête
-------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

Le nom du champ de fichier varie selon le type de dictionnaire (voir « Champs des entrées par type de dictionnaire » ci-dessous).

Réponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Téléchargement d'un fichier de dictionnaire
===========================================

Télécharge le fichier de dictionnaire.

Requête
-------

::

    GET /api/admin/dict/{type}/download/{dictId}

La réponse est le binaire du fichier de dictionnaire ( ``application/octet-stream`` ).

Champs des entrées par type de dictionnaire
===========================================

Les champs du corps de requête de création/mise à jour d'une entrée de dictionnaire ainsi que ceux de la réponse varient selon le type de dictionnaire.
``id`` (ID de l'entrée) et ``dictId`` (ID du dictionnaire) sont inclus de manière commune dans la réponse.

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - Type
     - Champs de l'entrée
     - Champ du fichier téléversé
   * - ``synonym``
     - ``inputs`` (requis), ``outputs`` (requis)
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` (requis), ``segmentation`` (requis), ``reading`` (requis), ``pos`` (requis)
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` (requis), ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` (requis)
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` (requis)
     - ``stopwordsFile``
   * - ``stemmeroverride``
     - ``input`` (requis), ``output`` (requis)
     - ``stemmerOverrideFile``

Exemples d'utilisation
======================

Obtention de la liste des dictionnaires
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention de la liste des entrées du dictionnaire de synonymes
--------------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

Ajout d'une entrée au dictionnaire de synonymes
-----------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

Téléversement du fichier de dictionnaire de synonymes
-----------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

Téléchargement du fichier de dictionnaire de synonymes
------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../../admin/dict-guide` - Guide de gestion des dictionnaires
