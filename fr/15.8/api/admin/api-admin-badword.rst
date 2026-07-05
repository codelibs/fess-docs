==========================
API BadWord
==========================

Vue d'ensemble
==============

L'API BadWord permet de gerer les mots interdits (exclusion de mots inappropries des suggestions) dans |Fess|.
Vous pouvez configurer les mots-cles que vous ne souhaitez pas afficher dans la fonction de suggestion.

URL de base
===========

::

    /api/admin/badword

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
     - Obtention de la liste des mots interdits
   * - GET
     - /setting/{id}
     - Obtention d'un mot interdit
   * - POST
     - /setting
     - Creation d'un mot interdit
   * - PUT
     - /setting
     - Mise a jour d'un mot interdit
   * - DELETE
     - /setting/{id}
     - Suppression d'un mot interdit
   * - PUT
     - /upload
     - Televersement CSV des mots interdits
   * - GET
     - /download
     - Telechargement CSV des mots interdits

Obtention de la liste des mots interdits
========================================

Requete
-------

::

    GET /api/admin/badword/settings

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
     - Filtrer uniquement sur le mot interdit ayant l'ID specifie

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

Obtention d'un mot interdit
===========================

Requete
-------

::

    GET /api/admin/badword/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

Creation d'un mot interdit
==========================

Requete
-------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
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
     - Mot-cle a exclure (ne peut pas contenir d'espaces)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

Mise a jour d'un mot interdit
=============================

Requete
-------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

Suppression d'un mot interdit
=============================

Requete
-------

::

    DELETE /api/admin/badword/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

Televersement CSV des mots interdits
====================================

Enregistre en masse des mots interdits depuis un fichier CSV. Le fichier est envoye en ``multipart/form-data``. L'import est execute de maniere asynchrone cote serveur.

Requete
-------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametre
     - Requis
     - Description
   * - ``badWordFile``
     - Oui
     - Fichier CSV des mots interdits a televerser

Format CSV
~~~~~~~~~~

- La premiere ligne est ignoree en tant que ligne d'en-tete (le nom de colonne est arbitraire ; ``BadWord`` est ecrit lors du telechargement).
- A partir de la deuxieme ligne, ecrivez un mot interdit par ligne en tant que ``suggestWord``.
- Les lignes dont la valeur est vide sont ignorees.
- Prefixez un mot par ``--`` pour le supprimer (par exemple, ``--spam`` supprime ``spam``).
- Specifier un mot deja enregistre est traite comme une mise a jour (l'auteur et la date de mise a jour sont reinitialises).

.. note::

   Comme l'import s'execute de maniere asynchrone cote serveur, une reponse ``status: 0``
   indique que la requete a ete acceptee, et non que l'import est termine.

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Telechargement CSV des mots interdits
=====================================

Telecharge les mots interdits enregistres sous forme de fichier CSV (``badword.csv``). La reponse est un flux ``application/octet-stream``.
Le CSV comporte une ligne d'en-tete ``BadWord`` sur la premiere ligne, suivie d'un mot interdit enregistre par ligne.

Requete
-------

::

    GET /api/admin/badword/download

Exemples d'utilisation
======================

Exclusion d'un mot-cle spam
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

Televersement d'un fichier CSV
------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

Telechargement d'un fichier CSV
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-suggest` - API de gestion des suggestions
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/badword-guide` - Guide de gestion des mots interdits
