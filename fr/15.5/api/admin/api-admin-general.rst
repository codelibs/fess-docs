==========================
API General
==========================

Vue d'ensemble
==============

L'API General permet de gerer les parametres generaux de |Fess|.
Vous pouvez obtenir et mettre a jour les parametres globaux du systeme.

URL de base
===========

::

    /api/admin/general

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention des parametres generaux
   * - PUT
     - /
     - Mise a jour des parametres generaux

Obtention des parametres generaux
=================================

Requete
-------

::

    GET /api/admin/general

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "crawlerDocumentMaxSize": "10485760",
          "crawlerDocumentMaxSiteLength": "50",
          "crawlerDocumentMaxFetcherSize": "3",
          "crawlerDocumentCrawlerThreadCount": "10",
          "crawlerDocumentMaxDepth": "-1",
          "crawlerDocumentMaxAccessCount": "100",
          "indexerThreadDumpEnabled": "true",
          "indexerUnprocessedDocumentSize": "1000",
          "indexerClickCountEnabled": "true",
          "indexerFavoriteCountEnabled": "true",
          "queryMaxSearchResultOffset": "100000",
          "queryMaxPageSize": "1000",
          "queryDefaultPageSize": "20",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "suggestBadWord": "true",
          "ldapProviderUrl": "ldap://localhost:389",
          "ldapBaseDn": "dc=example,dc=com",
          "notificationLogin": "true",
          "notificationSearchTop": "true"
        }
      }
    }

Mise a jour des parametres generaux
===================================

Requete
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "crawlerDocumentMaxSize": "20971520",
      "crawlerDocumentMaxSiteLength": "100",
      "crawlerDocumentCrawlerThreadCount": "20",
      "queryMaxPageSize": "500",
      "queryDefaultPageSize": "50",
      "suggestSearchLog": "true",
      "suggestDocuments": "true",
      "suggestBadWord": "true"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``crawlerDocumentMaxSize``
     - Taille maximale des documents a crawler (octets)
   * - ``crawlerDocumentMaxSiteLength``
     - Longueur maximale du site a crawler
   * - ``crawlerDocumentMaxFetcherSize``
     - Taille maximale du fetcher
   * - ``crawlerDocumentCrawlerThreadCount``
     - Nombre de threads du crawler
   * - ``crawlerDocumentMaxDepth``
     - Profondeur maximale du crawl (-1=illimitee)
   * - ``crawlerDocumentMaxAccessCount``
     - Nombre maximum d'acces
   * - ``indexerClickCountEnabled``
     - Activer le comptage des clics
   * - ``indexerFavoriteCountEnabled``
     - Activer le comptage des favoris
   * - ``queryMaxSearchResultOffset``
     - Offset maximum des resultats de recherche
   * - ``queryMaxPageSize``
     - Nombre maximum d'elements par page
   * - ``queryDefaultPageSize``
     - Nombre d'elements par page par defaut
   * - ``suggestSearchLog``
     - Activer les suggestions depuis les logs de recherche
   * - ``suggestDocuments``
     - Activer les suggestions depuis les documents
   * - ``suggestBadWord``
     - Activer le filtre des mots interdits
   * - ``ldapProviderUrl``
     - URL de connexion LDAP
   * - ``ldapBaseDn``
     - DN de base LDAP

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
======================

Mise a jour des parametres du crawler
-------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "crawlerDocumentMaxSize": "52428800",
           "crawlerDocumentCrawlerThreadCount": "15",
           "crawlerDocumentMaxAccessCount": "1000"
         }'

Mise a jour des parametres de recherche
---------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "queryMaxPageSize": "1000",
           "queryDefaultPageSize": "50",
           "queryMaxSearchResultOffset": "50000"
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations systeme
- :doc:`../../admin/general-guide` - Guide des parametres generaux
