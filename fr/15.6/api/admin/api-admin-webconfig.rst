==========================
API WebConfig
==========================

Vue d'ensemble
==============

L'API WebConfig permet de gerer les configurations de crawl Web de |Fess|.
Vous pouvez manipuler les parametres tels que les URLs cibles du crawl, la profondeur de crawl, les patterns d'exclusion, etc.

URL de base
===========

::

    /api/admin/webconfig

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
     - Obtention de la liste des configurations de crawl Web
   * - GET
     - /setting/{id}
     - Obtention d'une configuration de crawl Web
   * - POST
     - /setting
     - Creation d'une configuration de crawl Web
   * - PUT
     - /setting
     - Mise a jour d'une configuration de crawl Web
   * - DELETE
     - /setting/{id}
     - Suppression d'une configuration de crawl Web

Obtention de la liste des configurations de crawl Web
=====================================================

Requete
-------

::

    GET /api/admin/webconfig/settings
    PUT /api/admin/webconfig/settings

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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Obtention d'une configuration de crawl Web
==========================================

Requete
-------

::

    GET /api/admin/webconfig/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

Creation d'une configuration de crawl Web
=========================================

Requete
-------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
     - Nom de la configuration
   * - ``urls``
     - Oui
     - URLs de depart du crawl (separees par des sauts de ligne si multiples)
   * - ``includedUrls``
     - Non
     - Pattern regex des URLs a crawler
   * - ``excludedUrls``
     - Non
     - Pattern regex des URLs a exclure
   * - ``includedDocUrls``
     - Non
     - Pattern regex des URLs a indexer
   * - ``excludedDocUrls``
     - Non
     - Pattern regex des URLs a exclure de l'indexation
   * - ``configParameter``
     - Non
     - Parametres de configuration supplementaires
   * - ``depth``
     - Non
     - Profondeur du crawl (par defaut : -1=illimite)
   * - ``maxAccessCount``
     - Non
     - Nombre maximum d'acces (par defaut : 100)
   * - ``userAgent``
     - Non
     - User-Agent personnalise
   * - ``numOfThread``
     - Non
     - Nombre de threads paralleles (par defaut : 1)
   * - ``intervalTime``
     - Non
     - Intervalle entre les requetes (millisecondes, par defaut : 0)
   * - ``boost``
     - Non
     - Valeur de boost des resultats de recherche (par defaut : 1.0)
   * - ``available``
     - Non
     - Active/Desactive (par defaut : true)
   * - ``sortOrder``
     - Non
     - Ordre d'affichage
   * - ``permissions``
     - Non
     - Roles autorises
   * - ``virtualHosts``
     - Non
     - Hotes virtuels
   * - ``labelTypeIds``
     - Non
     - IDs des types de labels

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

Mise a jour d'une configuration de crawl Web
============================================

Requete
-------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": true,
      "versionNo": 1
    }

Reponse
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

Requete
-------

::

    DELETE /api/admin/webconfig/setting/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_webconfig_id",
        "created": false
      }
    }

Exemples de patterns d'URL
==========================

includedUrls / excludedUrls
---------------------------

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
     - URLs avec parametres de requete
   * - ``.*/(login|logout|admin)/.*``
     - URLs contenant certains chemins

Exemples d'utilisation
======================

Configuration de crawl pour un site d'entreprise
------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "available": true,
           "permissions": ["guest"]
         }'

Configuration de crawl pour un site de documentation
----------------------------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": true,
           "labelTypeIds": ["documentation_label_id"]
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-fileconfig` - API de configuration de crawl de fichiers
- :doc:`api-admin-dataconfig` - API de configuration datastore
- :doc:`../../admin/webconfig-guide` - Guide de configuration du crawl Web
