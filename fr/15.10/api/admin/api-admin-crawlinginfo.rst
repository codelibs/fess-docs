==========================
API CrawlingInfo
==========================

Vue d'ensemble
==============

L'API CrawlingInfo permet de consulter et de gérer les informations de crawl (sessions de crawl) de |Fess|.
Vous pouvez obtenir la liste des sessions de crawl, les consulter individuellement, les supprimer, etc.

URL de base
===========

::

    /api/admin/crawlinginfo

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /logs
     - Obtention de la liste des informations de crawl
   * - GET
     - /progress
     - Obtenir la progression des explorations en cours
   * - GET
     - /log/{id}
     - Obtention d'une information de crawl
   * - DELETE
     - /log/{id}
     - Suppression d'une information de crawl
   * - DELETE
     - /all
     - Suppression groupée des sessions de crawl (hors sessions en cours)

Obtention de la liste des informations de crawl
===============================================

Requête
-------

::

    GET /api/admin/crawlinginfo/logs

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
     - Nombre d'éléments par page (par défaut : 25 ; modifiable avec ``paging.page.size`` dans ``fess_config.properties``)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (base 1, défaut : 1)
   * - ``session_id``
     - String
     - Non
     - Filtre par ID de session (correspondance partielle)

Ces paramètres sont indiqués dans le corps JSON de la requête (par exemple ``{"size": 50, "page": 1}``). Les valeurs indiquées dans la chaîne de requête de l'URL (par exemple ``?size=50``) sont ignorées ; si elles ne figurent pas dans le corps, les 25 premiers éléments sont donc toujours retournés.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "session_id": "20250129100000",
            "name": "Default Crawler",
            "expired_time": "1738200000000",
            "created_time": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "session_id": "20250128100000",
            "name": "Default Crawler",
            "expired_time": "1738113600000",
            "created_time": 1738022400000
          }
        ],
        "total": 10
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID de l'information de crawl
   * - ``session_id``
     - ID de la session
   * - ``name``
     - Nom de la session
   * - ``expired_time``
     - Date d'expiration (millisecondes epoch ; retournée sous forme de chaîne)
   * - ``created_time``
     - Heure de création (millisecondes epoch ; retournée sous forme de nombre)

.. note::

   Chaque objet de journal dans la réponse inclut également un champ interne ``crud_mode``
   (un entier indiquant le mode d'opération CRUD, toujours ``0`` pour les opérations de lecture).
   Les clients peuvent l'ignorer en toute sécurité.

Obtenir la progression des explorations en cours
================================================

Renvoie la progression des explorations en cours, une entrée par configuration d'exploration (web, système de fichiers ou magasin de données). Ce sont les mêmes informations que « Explorations en cours » sur la page Informations sur l'exploration de l'interface d'administration (voir :doc:`../../admin/crawlinginfo-guide`).

Requête
-------

::

    GET /api/admin/crawlinginfo/progress

Ce point d'accès n'accepte aucun paramètre.

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "progress": [
          {
            "config_id": "Wabc123",
            "name": "Example Site",
            "count": 4200,
            "last_count": 10000,
            "updated_time": 1738144800000,
            "percent": 42
          },
          {
            "config_id": "Ddef456",
            "name": "Example Database",
            "count": 1500,
            "last_count": 0,
            "updated_time": 1738144795000
          }
        ],
        "total": 2
      }
    }

Champs de la réponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``progress``
     - Tableau des explorations en cours, trié par nom de configuration d'exploration. Tableau vide si aucune exploration n'est en cours
   * - ``total``
     - Nombre d'éléments de ``progress``

Chaque élément de ``progress`` comporte les champs suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``config_id``
     - ID de la configuration d'exploration (commence par ``W`` pour le web, ``F`` pour le système de fichiers et ``D`` pour un magasin de données)
   * - ``name``
     - Nom de la configuration d'exploration (``config_id`` si la configuration est introuvable)
   * - ``count``
     - Nombre de documents que l'exploration en cours a traités jusqu'ici
   * - ``last_count``
     - Nombre de documents de la dernière exploration terminée (``0`` si inconnu)
   * - ``updated_time``
     - Heure d'écriture de ``count`` (millisecondes epoch, nombre)
   * - ``percent``
     - ``count`` en pourcentage de ``last_count`` (de ``0`` à ``99``). Omis s'il n'y a pas d'exploration terminée précédente

.. note::

   Une exploration terminée ou arrêtée n'est pas incluse. Si le crawler s'arrête sans l'enregistrer (par exemple lorsque le processus est tué), l'exploration n'est plus incluse environ 30 secondes (par défaut) après sa dernière mise à jour. Le ``count`` d'une exploration web ou de système de fichiers est le nombre de résultats d'accès ; celui d'une exploration de magasin de données est le nombre de documents indexés pour la configuration d'exploration.

Obtention d'une information de crawl
====================================

Requête
-------

::

    GET /api/admin/crawlinginfo/log/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "session_id": "20250129100000",
          "name": "Default Crawler",
          "expired_time": "1738200000000",
          "created_time": 1738108800000
        }
      }
    }

Suppression d'une information de crawl
======================================

Requête
-------

::

    DELETE /api/admin/crawlinginfo/log/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Suppression groupée des sessions de crawl
==========================================

Supprime toutes les sessions de crawl (ainsi que leurs données de paramètres), à l'exception de celles qui sont actuellement en cours d'exécution. Il n'y a pas de seuil d'âge ou de durée ; toute session qui n'est pas en cours d'exécution est supprimée.

Requête
-------

::

    DELETE /api/admin/crawlinginfo/all

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

Obtention de la liste des informations de crawl
-----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

Filtrage par session spécifique
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"session_id": "20250129100000"}'

Obtention d'une information de crawl
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'une information de crawl
--------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression groupée des sessions
--------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-failureurl` - API des URLs en échec
- :doc:`api-admin-joblog` - API des journaux de tâches
- :doc:`../../admin/crawlinginfo-guide` - Guide des informations de crawl
