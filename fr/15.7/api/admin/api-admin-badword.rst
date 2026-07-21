==========================
API BadWord
==========================

Vue d'ensemble
==============

L'API BadWord permet de gérer les mots interdits (exclusion de mots inappropriés des suggestions) dans |Fess|.
Vous pouvez configurer les mots-clés que vous ne souhaitez pas afficher dans la fonction de suggestion.

URL de base
===========

::

    /api/admin/badword

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
     - Obtention de la liste des mots interdits
   * - GET
     - /setting/{id}
     - Obtention d'un mot interdit
   * - POST
     - /setting
     - Création d'un mot interdit
   * - PUT
     - /setting
     - Mise à jour d'un mot interdit
   * - DELETE
     - /setting/{id}
     - Suppression d'un mot interdit
   * - PUT
     - /upload
     - Téléversement CSV des mots interdits
   * - GET
     - /download
     - Téléchargement CSV des mots interdits

Obtention de la liste des mots interdits
========================================

Requête
-------

::

    GET /api/admin/badword/settings

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
     - Filtrer uniquement sur le mot interdit ayant l'ID spécifié

Réponse
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

Requête
-------

::

    GET /api/admin/badword/setting/{id}

Réponse
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

Création d'un mot interdit
==========================

Requête
-------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

Corps de la requête
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
     - Mot-clé à exclure (ne peut pas contenir d'espaces)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

Mise à jour d'un mot interdit
=============================

Requête
-------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

Réponse
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

Requête
-------

::

    DELETE /api/admin/badword/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

Téléversement CSV des mots interdits
====================================

Enregistre en masse des mots interdits depuis un fichier CSV. Le fichier est envoyé en ``multipart/form-data``. L'import est exécuté de manière asynchrone côté serveur.

Requête
-------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Paramètre
     - Requis
     - Description
   * - ``badWordFile``
     - Oui
     - Fichier CSV des mots interdits à téléverser

Format CSV
~~~~~~~~~~

- La première ligne est ignorée en tant que ligne d'en-tête (le nom de colonne est arbitraire ; ``BadWord`` est écrit lors du téléchargement).
- À partir de la deuxième ligne, écrivez un mot interdit par ligne en tant que ``suggestWord``.
- Les lignes dont la valeur est vide sont ignorées.
- Préfixez un mot par ``--`` pour le supprimer (par exemple, ``--spam`` supprime ``spam``).
- Spécifier un mot déjà enregistré est traité comme une mise à jour (l'auteur et la date de mise à jour sont réinitialisés).

.. note::

   Comme l'import s'exécute de manière asynchrone côté serveur, une réponse ``status: 0``
   indique que la requête a été acceptée, et non que l'import est terminé.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Téléchargement CSV des mots interdits
=====================================

Télécharge les mots interdits enregistrés sous forme de fichier CSV (``badword.csv``). La réponse est un flux ``application/octet-stream``.
Le CSV comporte une ligne d'en-tête ``BadWord`` sur la première ligne, suivie d'un mot interdit enregistré par ligne.

Requête
-------

::

    GET /api/admin/badword/download

Exemples d'utilisation
======================

Exclusion d'un mot-clé spam
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

Téléversement d'un fichier CSV
------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

Téléchargement d'un fichier CSV
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-suggest` - API de gestion des suggestions
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/badword-guide` - Guide de gestion des mots interdits
