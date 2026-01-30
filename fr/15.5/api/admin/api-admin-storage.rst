==========================
API Storage
==========================

Vue d'ensemble
==============

L'API Storage permet de gerer le stockage de |Fess|.
Vous pouvez consulter l'utilisation du stockage des index et effectuer des optimisations.

URL de base
===========

::

    /api/admin/storage

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
     - Obtention des informations de stockage
   * - POST
     - /optimize
     - Optimisation de l'index
   * - POST
     - /flush
     - Flush de l'index

Obtention des informations de stockage
======================================

Requete
-------

::

    GET /api/admin/storage

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "storage": {
          "indices": [
            {
              "name": "fess.20250129",
              "status": "open",
              "health": "green",
              "docsCount": 123456,
              "docsDeleted": 234,
              "storeSize": "5.2gb",
              "primariesStoreSize": "2.6gb",
              "shards": 5,
              "replicas": 1
            }
          ],
          "totalStoreSize": "5.2gb",
          "totalDocsCount": 123456,
          "clusterHealth": "green",
          "diskUsage": {
            "total": "107374182400",
            "available": "53687091200",
            "used": "53687091200",
            "usedPercent": 50.0
          }
        }
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``indices``
     - Liste des index
   * - ``name``
     - Nom de l'index
   * - ``status``
     - Statut de l'index (open/close)
   * - ``health``
     - Statut de sante (green/yellow/red)
   * - ``docsCount``
     - Nombre de documents
   * - ``docsDeleted``
     - Nombre de documents supprimes
   * - ``storeSize``
     - Taille du stockage
   * - ``primariesStoreSize``
     - Taille des shards primaires
   * - ``shards``
     - Nombre de shards
   * - ``replicas``
     - Nombre de replicas
   * - ``totalStoreSize``
     - Taille totale du stockage
   * - ``totalDocsCount``
     - Nombre total de documents
   * - ``clusterHealth``
     - Sante du cluster
   * - ``diskUsage``
     - Utilisation du disque

Optimisation de l'index
=======================

Requete
-------

::

    POST /api/admin/storage/optimize
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129",
      "maxNumSegments": 1,
      "onlyExpungeDeletes": false,
      "flush": true
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``index``
     - Non
     - Nom de l'index (tous les index si non specifie)
   * - ``maxNumSegments``
     - Non
     - Nombre maximum de segments (par defaut : 1)
   * - ``onlyExpungeDeletes``
     - Non
     - Supprimer uniquement les documents supprimes (par defaut : false)
   * - ``flush``
     - Non
     - Flush apres optimisation (par defaut : true)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index optimization started"
      }
    }

Flush de l'index
================

Requete
-------

::

    POST /api/admin/storage/flush
    Content-Type: application/json

Corps de la requete
~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129"
    }

Description des champs
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``index``
     - Non
     - Nom de l'index (tous les index si non specifie)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index flushed successfully"
      }
    }

Exemples d'utilisation
======================

Obtention des informations de stockage
--------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN"

Optimisation de tous les index
------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "maxNumSegments": 1,
           "flush": true
         }'

Optimisation d'un index specifique
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129",
           "maxNumSegments": 1,
           "onlyExpungeDeletes": false
         }'

Suppression des documents supprimes
-----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "onlyExpungeDeletes": true
         }'

Flush de l'index
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/flush" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129"
         }'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API des informations systeme
- :doc:`../../admin/storage-guide` - Guide de gestion du stockage
