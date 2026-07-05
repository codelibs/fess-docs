==========================
KeyMatch API
==========================

Vue d'ensemble
==============

L'API KeyMatch permet de gérer les correspondances de mots-clés (association entre mots-clés de recherche et résultats) dans |Fess|.
Vous pouvez faire apparaître des documents spécifiques en haut des résultats pour certains mots-clés.

URL de base
===========

::

    /api/admin/keymatch

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
     - Obtention de la liste des KeyMatch
   * - GET
     - /setting/{id}
     - Obtention d'un KeyMatch
   * - POST
     - /setting
     - Création d'un KeyMatch
   * - PUT
     - /setting
     - Mise à jour d'un KeyMatch
   * - DELETE
     - /setting/{id}
     - Suppression d'un KeyMatch

Obtention de la liste des KeyMatch
===================================

Requête
-------

::

    GET /api/admin/keymatch/settings

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
     - Nombre d'éléments par page (par défaut : 25, valeur du paramètre ``paging.page.size``)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1)
   * - ``term``
     - String
     - Non
     - Filtrage par mot-clé de recherche (correspondance avec caractères génériques)
   * - ``query``
     - String
     - Non
     - Filtrage par requête de correspondance (correspondance avec caractères génériques)

Réponse
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
            "boost": 10.0,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``total`` contient le nombre total d'éléments correspondant aux critères de filtrage (et non le nombre d'éléments de la page courante).
   En plus des champs ci-dessus, chaque objet de configuration peut inclure ``virtualHost``,
   ``createdBy``, ``createdTime``, ``updatedBy`` et ``updatedTime`` lorsque des valeurs sont définies.

Obtention d'un KeyMatch
=======================

Requête
-------

::

    GET /api/admin/keymatch/setting/{id}

Réponse
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
          "boost": 10.0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   ``versionNo`` est le numéro de version utilisé pour le verrouillage optimiste. Lors de la mise à jour d'un KeyMatch,
   spécifiez la valeur de ``versionNo`` obtenue lors de la récupération dans le corps de la requête.
   Si l'identifiant spécifié n'existe pas, une erreur est renvoyée.

Création d'un KeyMatch
======================

Requête
-------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

Corps de la requête
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
   :widths: 20 15 15 50

   * - Champ
     - Type
     - Requis
     - Description
   * - ``term``
     - String
     - Oui
     - Mot-clé de recherche (100 caractères maximum)
   * - ``query``
     - String
     - Oui
     - Requête de correspondance (longueur maximale définie par le paramètre ``form.admin.max.input.size``)
   * - ``maxSize``
     - Integer
     - Oui
     - Nombre maximum d'affichages (entier supérieur ou égal à 0 ; valeur initiale dans l'interface d'administration : 10)
   * - ``boost``
     - Float
     - Oui
     - Valeur de boost (valeur initiale dans l'interface d'administration : 100.0)
   * - ``virtualHost``
     - String
     - Non
     - Nom d'hôte virtuel (1000 caractères maximum ; à spécifier pour basculer les KeyMatch par hôte virtuel)

.. note::

   ``maxSize`` et ``boost`` sont obligatoires via l'API. Les valeurs initiales affichées dans le formulaire de l'interface d'administration
   ne s'appliquent pas via l'API. En cas d'omission, une erreur de validation est renvoyée.
   Par ailleurs, ``createdBy`` et ``createdTime`` sont écrasés côté serveur même s'ils sont spécifiés dans la requête.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

Mise à jour d'un KeyMatch
==========================

Requête
-------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

Corps de la requête
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

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

En plus des champs de création (``term``, ``query``, ``maxSize``, ``boost``, ``virtualHost``),
les champs suivants doivent être spécifiés.

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Champ
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - Identifiant du KeyMatch à mettre à jour (1000 caractères maximum)
   * - ``versionNo``
     - Integer
     - Oui
     - Numéro de version pour le verrouillage optimiste ; spécifier la valeur obtenue lors de la récupération

Réponse
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
==========================

Requête
-------

::

    DELETE /api/admin/keymatch/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
======================

Création d'un KeyMatch pour une page produit
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
-----------------------------------

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

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-elevateword` - API ElevateWord
- :doc:`../../admin/keymatch-guide` - Guide de gestion des KeyMatch
