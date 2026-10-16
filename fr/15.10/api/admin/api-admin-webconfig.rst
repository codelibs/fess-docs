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
            "included_urls": ".*example\\.com.*",
            "excluded_urls": ".*\\.(pdf|zip)$",
            "included_doc_urls": "",
            "excluded_doc_urls": "",
            "config_parameter": "",
            "depth": 3,
            "max_access_count": 1000,
            "user_agent": "Mozilla/5.0",
            "num_of_thread": 1,
            "interval_time": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtual_hosts": "",
            "sort_order": 0
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
          "included_urls": ".*example\\.com.*",
          "excluded_urls": ".*\\.(pdf|zip)$",
          "included_doc_urls": "",
          "excluded_doc_urls": "",
          "config_parameter": "",
          "depth": 3,
          "max_access_count": 1000,
          "user_agent": "Mozilla/5.0",
          "num_of_thread": 1,
          "interval_time": 1000,
          "boost": 1.0,
          "available": "true",
          "sort_order": 0,
          "permissions": "{role}admin",
          "virtual_hosts": "",
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   La réponse inclut les champs d'audit ``created_by``, ``created_time``,
   ``updated_by``, ``updated_time`` et ``version_no``, qui sont définis automatiquement
   lors de la création ou de la mise à jour.
   ``version_no`` est requis lors de la mise à jour (voir la section « Mise à jour d'une configuration de crawl Web » ci-dessous).

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
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe)$",
      "user_agent": "Mozilla/5.0",
      "num_of_thread": 3,
      "interval_time": 500,
      "boost": 1.0,
      "available": "true",
      "sort_order": 0,
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
   * - ``included_urls``
     - Non
     - Expression régulière des URLs à crawler
   * - ``excluded_urls``
     - Non
     - Expression régulière des URLs à exclure du crawl
   * - ``included_doc_urls``
     - Non
     - Expression régulière des URLs à indexer
   * - ``excluded_doc_urls``
     - Non
     - Expression régulière des URLs à exclure de l'indexation
   * - ``config_parameter``
     - Non
     - Paramètres de configuration supplémentaires (format ``key=value``, un par ligne)
   * - ``depth``
     - Non
     - Profondeur du crawl (0 ou plus)
   * - ``max_access_count``
     - Non
     - Nombre maximum d'accès (0 ou plus)
   * - ``user_agent``
     - Oui
     - Chaîne User-Agent (200 caractères maximum)
   * - ``num_of_thread``
     - Oui
     - Nombre de threads parallèles (1 ou plus)
   * - ``interval_time``
     - Oui
     - Intervalle entre les accès (en millisecondes, 0 ou plus)
   * - ``boost``
     - Oui
     - Valeur de boost des résultats de recherche
   * - ``available``
     - Oui
     - Activé/Désactivé (chaîne ``"true"`` / ``"false"``)
   * - ``sort_order``
     - Oui
     - Ordre d'affichage (0 ou plus)
   * - ``permissions``
     - Non
     - Rôles autorisés (séparés par des sauts de ligne si plusieurs)
   * - ``virtual_hosts``
     - Non
     - Hôtes virtuels (séparés par des sauts de ligne si plusieurs)

.. note::

   Les champs d'audit tels que ``created_by``, ``created_time``, ``updated_by`` et ``updated_time``
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

Lors d'une mise à jour, les champs de création sont complétés par ``id``, qui identifie la configuration à mettre à jour, et ``version_no``, le numéro de version actuel.
Indiquez pour ``version_no`` la valeur renvoyée par l'API de récupération (GET).

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "included_urls": ".*www\\.example\\.com.*",
      "excluded_urls": ".*\\.(pdf|zip|exe|dmg)$",
      "user_agent": "Mozilla/5.0",
      "depth": 10,
      "max_access_count": 10000,
      "num_of_thread": 5,
      "interval_time": 300,
      "boost": 1.2,
      "available": "true",
      "sort_order": 0,
      "version_no": 1
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
   * - ``version_no``
     - Oui
     - Numéro de version actuel de la configuration à mettre à jour. Indiquez la valeur ``version_no`` contenue dans la réponse de l'API de récupération (GET)

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

Les champs ``included_urls`` / ``excluded_urls`` / ``included_doc_urls`` / ``excluded_doc_urls`` acceptent des expressions régulières.

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
           "included_urls": ".*www\\.example\\.com.*",
           "excluded_urls": ".*/(login|admin|api)/.*",
           "user_agent": "Mozilla/5.0",
           "depth": 5,
           "max_access_count": 10000,
           "num_of_thread": 3,
           "interval_time": 500,
           "boost": 1.0,
           "available": "true",
           "sort_order": 0,
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
           "included_urls": ".*docs\\.example\\.com.*",
           "included_doc_urls": ".*\\.(html|htm)$",
           "user_agent": "Mozilla/5.0",
           "max_access_count": 50000,
           "num_of_thread": 5,
           "interval_time": 200,
           "boost": 1.5,
           "available": "true",
           "sort_order": 0
         }'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-fileconfig` - API de configuration de crawl de fichiers
- :doc:`api-admin-dataconfig` - API de configuration datastore
- :doc:`../../admin/webconfig-guide` - Guide de configuration du crawl Web
