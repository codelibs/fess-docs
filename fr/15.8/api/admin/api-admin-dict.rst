==========================
API Dict
==========================

Vue d'ensemble
==============

L'API Dict est une API permettant de gerer les dictionnaires de |Fess|.
L'endpoint racine permet d'obtenir la liste des dictionnaires disponibles.
La consultation, la creation, la mise a jour et la suppression des entrees de dictionnaire individuelles, ainsi que le televersement et le telechargement des fichiers de dictionnaire, s'effectuent via les sous-endpoints propres a chaque type de dictionnaire (synonym, kuromoji, mapping, protwords, stopwords, stemmeroverride).

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

   * - Methode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention de la liste des dictionnaires

Endpoints propres a chaque type de dictionnaire
-----------------------------------------------

``{type}`` doit etre l'une des valeurs suivantes : ``synonym`` , ``kuromoji`` , ``mapping`` , ``protwords`` , ``stopwords`` , ``stemmeroverride`` .
Ces valeurs correspondent a la valeur du champ ``type`` inclus dans la reponse de la liste des dictionnaires.
``{dictId}`` est l'ID du dictionnaire obtenu via l'obtention de la liste des dictionnaires.

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - Methode
     - Chemin
     - Description
   * - GET
     - /{type}/settings/{dictId}
     - Obtention de la liste des entrees de dictionnaire
   * - GET
     - /{type}/setting/{dictId}/{id}
     - Obtention d'une entree de dictionnaire
   * - POST
     - /{type}/setting/{dictId}
     - Creation d'une entree de dictionnaire
   * - PUT
     - /{type}/setting/{dictId}
     - Mise a jour d'une entree de dictionnaire
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - Suppression d'une entree de dictionnaire
   * - PUT
     - /{type}/upload/{dictId}
     - Televersement d'un fichier de dictionnaire
   * - GET
     - /{type}/download/{dictId}
     - Telechargement d'un fichier de dictionnaire

Obtention de la liste des dictionnaires
=======================================

Obtient la liste des fichiers de dictionnaire disponibles.

Requete
-------

::

    GET /api/admin/dict

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``settings[].id``
     - ID du dictionnaire (utilise comme ``{dictId}`` dans les operations sur les dictionnaires individuels)
   * - ``settings[].type``
     - Type de dictionnaire
   * - ``settings[].path``
     - Chemin du fichier de dictionnaire
   * - ``settings[].timestamp``
     - Date et heure de mise a jour du fichier de dictionnaire
   * - ``total``
     - Nombre total de fichiers de dictionnaire

Obtention de la liste des entrees de dictionnaire
=================================================

Obtient la liste des entrees du dictionnaire specifie.

Requete
-------

::

    GET /api/admin/dict/{type}/settings/{dictId}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``dictId``
     - String
     - Oui
     - ID du dictionnaire (parametre de chemin)
   * - ``size``
     - Integer
     - Non
     - Nombre d'elements par page (defaut : 25)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 1, defaut : 1)

Reponse
-------

Les champs de chaque element du tableau ``settings`` de la reponse varient selon le type de dictionnaire (voir « Champs des entrees par type de dictionnaire » ci-dessous).

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
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

Obtention d'une entree de dictionnaire
======================================

Obtient une entree specifique du dictionnaire.

Requete
-------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``dictId``
     - String
     - Oui
     - ID du dictionnaire (parametre de chemin)
   * - ``id``
     - Long
     - Oui
     - ID de l'entree (parametre de chemin)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

Creation d'une entree de dictionnaire
=====================================

Cree une nouvelle entree dans le dictionnaire.

Requete
-------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Corps de la requete (exemple synonym)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

Mise a jour d'une entree de dictionnaire
========================================

Met a jour une entree existante du dictionnaire.

Requete
-------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

Corps de la requete (exemple synonym)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Suppression d'une entree de dictionnaire
========================================

Supprime une entree du dictionnaire.

Requete
-------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``dictId``
     - String
     - Oui
     - ID du dictionnaire (parametre de chemin)
   * - ``id``
     - Long
     - Oui
     - ID de l'entree (parametre de chemin)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

Televersement d'un fichier de dictionnaire
==========================================

Televerse et remplace l'integralite du fichier de dictionnaire.

Requete
-------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

Le nom du champ de fichier varie selon le type de dictionnaire (voir « Champs des entrees par type de dictionnaire » ci-dessous).

Reponse
-------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

Telechargement d'un fichier de dictionnaire
===========================================

Telecharge le fichier de dictionnaire.

Requete
-------

::

    GET /api/admin/dict/{type}/download/{dictId}

La reponse est le binaire du fichier de dictionnaire ( ``application/octet-stream`` ).

Champs des entrees par type de dictionnaire
===========================================

Les champs du corps de requete de creation/mise a jour d'une entree de dictionnaire ainsi que ceux de la reponse varient selon le type de dictionnaire.
``id`` (ID de l'entree) et ``dictId`` (ID du dictionnaire) sont inclus de maniere commune dans la reponse.

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - Type
     - Champs de l'entree
     - Champ du fichier televerse
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

Obtention de la liste des entrees du dictionnaire de synonymes
--------------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

Ajout d'une entree au dictionnaire de synonymes
-----------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

Televersement du fichier de dictionnaire de synonymes
-----------------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

Telechargement du fichier de dictionnaire de synonymes
------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../../admin/dict-guide` - Guide de gestion des dictionnaires
