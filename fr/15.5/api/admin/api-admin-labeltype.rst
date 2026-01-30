==========================
API LabelType
==========================

Vue d'ensemble
==============

L'API LabelType permet de gerer les types de labels de |Fess|.
Vous pouvez manipuler les types de labels utilises pour la classification et le filtrage des resultats de recherche.

URL de base
===========

::

    /api/admin/labeltype

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
     - Obtention de la liste des types de labels
   * - GET
     - /setting/{id}
     - Obtention d'un type de label
   * - POST
     - /setting
     - Creation d'un type de label
   * - PUT
     - /setting
     - Mise a jour d'un type de label
   * - DELETE
     - /setting/{id}
     - Suppression d'un type de label

Obtention de la liste des types de labels
=========================================

Requete
-------

::

    GET /api/admin/labeltype/settings
    PUT /api/admin/labeltype/settings

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
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtention d'un type de label
============================

Requete
-------

::

    GET /api/admin/labeltype/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "sortOrder": 0,
          "permissions": [],
          "virtualHost": ""
        }
      }
    }

Creation d'un type de label
===========================

Requete
-------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": ["guest"]
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom d'affichage du label
   * - ``value``
     - Oui
     - Valeur du label (utilisee dans les recherches)
   * - ``includedPaths``
     - Non
     - Regex des chemins cibles (separes par des sauts de ligne si multiples)
   * - ``excludedPaths``
     - Non
     - Regex des chemins a exclure (separes par des sauts de ligne si multiples)
   * - ``sortOrder``
     - Non
     - Ordre d'affichage
   * - ``permissions``
     - Non
     - Roles autorises
   * - ``virtualHost``
     - Non
     - Hote virtuel

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

Mise a jour d'un type de label
==============================

Requete
-------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": ["guest"],
      "versionNo": 1
    }

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

Suppression d'un type de label
==============================

Requete
-------

::

    DELETE /api/admin/labeltype/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_label_id",
        "created": false
      }
    }

Exemples d'utilisation
======================

Creation d'un label pour la documentation
-----------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": ["guest"]
         }'

Recherche avec un label
-----------------------

.. code-block:: bash

    # Filtrage par label
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`../search-api` - API de recherche
- :doc:`../../admin/labeltype-guide` - Guide de gestion des types de labels
