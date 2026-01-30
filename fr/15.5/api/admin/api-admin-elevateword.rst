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
   * - GET/PUT
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

Obtention de la liste des mots eleves
=====================================

Requete
-------

::

    GET /api/admin/elevateword/settings
    PUT /api/admin/elevateword/settings

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "fess",
            "permissions": [],
            "boost": 10.0,
            "targetRole": "",
            "targetLabel": ""
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
          "reading": "fess",
          "permissions": [],
          "boost": 10.0,
          "targetRole": "",
          "targetLabel": ""
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
      "reading": "documentation",
      "permissions": ["guest"],
      "boost": 15.0,
      "targetRole": "user",
      "targetLabel": "docs"
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
     - Roles autorises
   * - ``boost``
     - Non
     - Valeur de boost (par defaut : 1.0)
   * - ``targetRole``
     - Non
     - Role cible
   * - ``targetLabel``
     - Non
     - Label cible

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
      "reading": "documentation",
      "permissions": ["guest", "user"],
      "boost": 20.0,
      "targetRole": "user",
      "targetLabel": "docs",
      "versionNo": 1
    }

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
           "boost": 20.0,
           "permissions": ["guest"]
         }'

Elevation vers un label specifique
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 10.0,
           "targetLabel": "technical_docs",
           "permissions": ["guest"]
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-keymatch` - API KeyMatch
- :doc:`api-admin-boostdoc` - API BoostDoc
- :doc:`../../admin/elevateword-guide` - Guide de gestion des mots eleves
