==========================
API KeyMatch
==========================

Vue d'ensemble
==============

L'API KeyMatch permet de gerer les correspondances de mots-cles (association entre mots-cles de recherche et resultats) dans |Fess|.
Vous pouvez faire apparaitre des documents specifiques en haut des resultats pour certains mots-cles.

URL de base
===========

::

    /api/admin/keymatch

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
     - Obtention de la liste des KeyMatch
   * - GET
     - /setting/{id}
     - Obtention d'un KeyMatch
   * - POST
     - /setting
     - Creation d'un KeyMatch
   * - PUT
     - /setting
     - Mise a jour d'un KeyMatch
   * - DELETE
     - /setting/{id}
     - Suppression d'un KeyMatch

Obtention de la liste des KeyMatch
==================================

Requete
-------

::

    GET /api/admin/keymatch/settings
    PUT /api/admin/keymatch/settings

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
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

Obtention d'un KeyMatch
=======================

Requete
-------

::

    GET /api/admin/keymatch/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "maxSize": 10,
          "boost": 10.0
        }
      }
    }

Creation d'un KeyMatch
======================

Requete
-------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "maxSize": 5,
      "boost": 20.0
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``term``
     - Oui
     - Mot-cle de recherche
   * - ``query``
     - Oui
     - Requete de correspondance
   * - ``maxSize``
     - Non
     - Nombre maximum d'affichages (par defaut : 10)
   * - ``boost``
     - Non
     - Valeur de boost (par defaut : 1.0)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

Mise a jour d'un KeyMatch
=========================

Requete
-------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

Suppression d'un KeyMatch
=========================

Requete
-------

::

    DELETE /api/admin/keymatch/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_keymatch_id",
        "created": false
      }
    }

Exemples d'utilisation
======================

Creation d'un KeyMatch pour une page produit
--------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

KeyMatch pour les pages de support
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "maxSize": 5,
           "boost": 20.0
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/keymatch-guide` - Guide de gestion des KeyMatch
