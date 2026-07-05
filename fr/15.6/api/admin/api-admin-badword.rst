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
   * - GET/PUT
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

Obtention de la liste des mots interdits
========================================

Requete
-------

::

    GET /api/admin/badword/settings
    PUT /api/admin/badword/settings

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
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word",
            "targetRole": "",
            "targetLabel": ""
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
          "suggestWord": "inappropriate_word",
          "targetRole": "",
          "targetLabel": ""
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
      "suggestWord": "spam_keyword",
      "targetRole": "guest",
      "targetLabel": ""
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
     - Mot-cle a exclure
   * - ``targetRole``
     - Non
     - Role cible (tous les roles si vide)
   * - ``targetLabel``
     - Non
     - Label cible (tous les labels si vide)

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
      "targetRole": "guest",
      "targetLabel": "",
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

Exemples d'utilisation
======================

Exclusion d'un mot-cle spam
---------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam",
           "targetRole": "",
           "targetLabel": ""
         }'

Mot interdit pour un role specifique
------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "internal",
           "targetRole": "guest",
           "targetLabel": ""
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-suggest` - API de gestion des suggestions
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/badword-guide` - Guide de gestion des mots interdits
