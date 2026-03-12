==========================
API Dict
==========================

Vue d'ensemble
==============

L'API Dict permet de gerer les fichiers de dictionnaire de |Fess|.
Vous pouvez gerer les dictionnaires de synonymes, de mapping, de mots proteges, etc.

URL de base
===========

::

    /api/admin/dict

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
     - Obtention de la liste des dictionnaires
   * - GET
     - /{id}
     - Obtention du contenu d'un dictionnaire
   * - PUT
     - /{id}
     - Mise a jour du contenu d'un dictionnaire
   * - POST
     - /upload
     - Telechargement d'un fichier de dictionnaire

Obtention de la liste des dictionnaires
=======================================

Requete
-------

::

    GET /api/admin/dict

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dicts": [
          {
            "id": "synonym",
            "name": "Dictionnaire de synonymes",
            "path": "/var/lib/fess/dict/synonym.txt",
            "type": "synonym",
            "updatedAt": "2025-01-29T10:00:00Z"
          },
          {
            "id": "mapping",
            "name": "Dictionnaire de mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "type": "mapping",
            "updatedAt": "2025-01-28T15:30:00Z"
          },
          {
            "id": "protwords",
            "name": "Dictionnaire de mots proteges",
            "path": "/var/lib/fess/dict/protwords.txt",
            "type": "protwords",
            "updatedAt": "2025-01-27T12:00:00Z"
          }
        ],
        "total": 3
      }
    }

Obtention du contenu d'un dictionnaire
======================================

Requete
-------

::

    GET /api/admin/dict/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dict": {
          "id": "synonym",
          "name": "Dictionnaire de synonymes",
          "path": "/var/lib/fess/dict/synonym.txt",
          "type": "synonym",
          "content": "recherche,search,query\nFess,fess\nrecherche plein texte,full-text search",
          "updatedAt": "2025-01-29T10:00:00Z"
        }
      }
    }

Mise a jour du contenu d'un dictionnaire
========================================

Requete
-------

::

    PUT /api/admin/dict/{id}
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "content": "recherche,search,query,lookup\nFess,fess\nrecherche plein texte,full-text search"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``content``
     - Oui
     - Contenu du dictionnaire (separe par des sauts de ligne)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary updated successfully"
      }
    }

Telechargement d'un fichier de dictionnaire
===========================================

Requete
-------

::

    POST /api/admin/dict/upload
    Content-Type: multipart/form-data

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="type"

    synonym
    --boundary
    Content-Disposition: form-data; name="file"; filename="synonym.txt"
    Content-Type: text/plain

    recherche,search,query
    Fess,fess
    --boundary--

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``type``
     - Oui
     - Type de dictionnaire (synonym/mapping/protwords/stopwords)
   * - ``file``
     - Oui
     - Fichier de dictionnaire

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary uploaded successfully"
      }
    }

Types de dictionnaires
======================

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type
     - Description
   * - ``synonym``
     - Dictionnaire de synonymes (expansion des synonymes lors de la recherche)
   * - ``mapping``
     - Dictionnaire de mapping (normalisation des caracteres)
   * - ``protwords``
     - Dictionnaire de mots proteges (mots exclus du stemming)
   * - ``stopwords``
     - Dictionnaire de mots vides (mots exclus de l'indexation)
   * - ``kuromoji``
     - Dictionnaire Kuromoji (analyse morphologique japonaise)

Exemples de format de dictionnaire
==================================

Dictionnaire de synonymes
-------------------------

::

    # Specifier les synonymes separes par des virgules
    recherche,search,query
    Fess,fess
    recherche plein texte,full-text search

Dictionnaire de mapping
-----------------------

::

    # avant => apres
    0 => 0
    1 => 1
    2 => 2

Dictionnaire de mots proteges
-----------------------------

::

    # Mots a proteger du traitement de stemming
    running
    searching
    indexing

Exemples d'utilisation
======================

Obtention de la liste des dictionnaires
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention du contenu du dictionnaire de synonymes
-------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN"

Mise a jour du dictionnaire de synonymes
----------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "content": "recherche,search,query\nFess,fess\ndocument,fichier,file"
         }'

Telechargement d'un fichier de dictionnaire
-------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "type=synonym" \
         -F "file=@synonym.txt"

Notes importantes
=================

- Apres la mise a jour d'un dictionnaire, une reconstruction de l'index peut etre necessaire
- Les fichiers de dictionnaire volumineux peuvent affecter les performances de recherche
- Utilisez l'encodage UTF-8 pour les fichiers de dictionnaire

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../../admin/dict-guide` - Guide de gestion des dictionnaires
