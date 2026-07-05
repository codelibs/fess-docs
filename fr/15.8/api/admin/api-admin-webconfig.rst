==========================
WebConfig API
==========================

Vue d'ensemble
==============

L'API WebConfig permet de gérer les configurations de crawl Web de |Fess|.
Vous pouvez manipuler les configurations de crawl pour les URLs cibles, la profondeur de crawl, les patterns d'exclusion, etc.

URL de base
===========

::

    /api/admin/webconfig

.. note::

   Tous les endpoints nécessitent des droits d'administration et un jeton d'accès valide.
   Consultez :doc:`api-admin-overview` pour les modalités d'authentification.

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
     - Obtention de la liste des configurations de crawl Web
   * - GET
     - /setting/{id}
     - Obtention d'une configuration de crawl Web
   * - POST
     - /setting
     - Création d'une configuration de crawl Web
   * - PUT
     - /setting
     - Mise à jour d'une configuration de crawl Web
   * - DELETE
     - /setting/{id}
     - Suppression d'une configuration de crawl Web

Obtention de la liste des configurations de crawl Web
======================================================

Requête
-------

::

    GET /api/admin/webconfig/settings

.. note::

   L'endpoint de liste est accessible à la fois via ``GET`` et via ``PUT``.

Paramètres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - Paramètre
     - Type
     - Requis
     - Description
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, par défaut : 1)
   * - ``size``
     - Integer
     - Non
     - Nombre d'éléments par page (par défaut : 25, selon le paramètre ``paging.page.size``)
   * - ``name``
     - String
     - Non
     - Filtrage par nom de configuration
   * - ``urls``
     - String
     - Non
     - Filtrage par URL de crawl
   * - ``description``
     - String
     - Non
     - Filtrage par description

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "Site d'exemple",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

``total`` représente le nombre total de configurations correspondant aux critères de recherche.

Obtention d'une configuration de crawl Web
==========================================

Requête
-------

::

    GET /api/admin/webconfig/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "Site d'exemple",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   La réponse inclut les champs d'audit ``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime`` et ``versionNo``, qui sont définis automatiquement
   lors de la création ou de la mise à jour.
   ``versionNo`` est requis lors de la mise à jour (voir la section « Mise à jour d'une configuration de crawl Web » ci-dessous).

Création d'une configuration de crawl Web
=========================================

Requête
-------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``name``
     - Oui
     - Nom de la configuration (200 caractères maximum)
   * - ``description``
     - Non
     - Description de la configuration (1 000 caractères maximum)
   * - ``urls``
     - Oui
     - URLs de départ du crawl (séparées par des sauts de ligne si multiples). Indiquez ``http:`` ou ``https:``
   * - ``includedUrls``
     - Non
     - Expression régulière des URLs à crawler
   * - ``excludedUrls``
     - Non
     - Expression régulière des URLs à exclure du crawl
   * - ``includedDocUrls``
     - Non
     - Expression régulière des URLs à indexer
   * - ``excludedDocUrls``
     - Non
     - Expression régulière des URLs à exclure de l'indexation
   * - ``configParameter``
     - Non
     - Paramètres de configuration supplémentaires (format ``key=value``, un par ligne)
   * - ``depth``
     - Non
     - Profondeur du crawl (0 ou plus)
   * - ``maxAccessCount``
     - Non
     - Nombre maximum d'accès (0 ou plus)
   * - ``userAgent``
     - Oui
     - Chaîne User-Agent (200 caractères maximum)
   * - ``numOfThread``
     - Oui
     - Nombre de threads parallèles (1 ou plus)
   * - ``intervalTime``
     - Oui
     - Intervalle entre les accès (en millisecondes, 0 ou plus)
   * - ``boost``
     - Oui
     - Valeur de boost des résultats de recherche
   * - ``available``
     - Oui
     - Activé/Désactivé (chaîne ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - Oui
     - Ordre d'affichage (0 ou plus)
   * - ``permissions``
     - Non
     - Rôles autorisés (séparés par des sauts de ligne si plusieurs)
   * - ``virtualHosts``
     - Non
     - Hôtes virtuels (séparés par des sauts de ligne si plusieurs)

.. note::

   Les champs d'audit tels que ``createdBy``, ``createdTime``, ``updatedBy`` et ``updatedTime``
   sont définis automatiquement côté serveur et n'ont pas besoin d'être fournis dans le corps de la requête.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

Mise à jour d'une configuration de crawl Web
============================================

Requête
-------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Corps de la requête
~~~~~~~~~~~~~~~~~~~

Lors d'une mise à jour, les champs de création sont complétés par ``id``, qui identifie la configuration à mettre à jour, et ``versionNo``, le numéro de version actuel.
Indiquez pour ``versionNo`` la valeur renvoyée par l'API de récupération (GET).

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

Champs supplémentaires pour la mise à jour
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Champ
     - Requis
     - Description
   * - ``id``
     - Oui
     - Identifiant de la configuration à mettre à jour (1 000 caractères maximum)
   * - ``versionNo``
     - Oui
     - Numéro de version actuel de la configuration à mettre à jour. Indiquez la valeur ``versionNo`` contenue dans la réponse de l'API de récupération (GET)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_webconfig_id",
        "created": false
      }
    }

Suppression d'une configuration de crawl Web
============================================

Requête
-------

::

    DELETE /api/admin/webconfig/setting/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples de patterns d'URL
==========================

Les champs ``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` acceptent des expressions régulières.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Pattern
     - Description
   * - ``.*example\\.com.*``
     - Toutes les URLs contenant example.com
   * - ``https://example\\.com/docs/.*``
     - Uniquement sous /docs/
   * - ``.*\\.(pdf|doc|docx)$``
     - Fichiers PDF, DOC, DOCX
   * - ``.*\\?.*``
     - URLs avec paramètres de requête
   * - ``.*/(login|logout|admin)/.*``
     - URLs contenant certains chemins

Exemples d'utilisation
======================

Configuration de crawl pour un site d'entreprise
-------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

Configuration de crawl pour un site de documentation
-----------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-fileconfig` - API de configuration de crawl de fichiers
- :doc:`api-admin-dataconfig` - API de configuration datastore
- :doc:`../../admin/webconfig-guide` - Guide de configuration du crawl Web
