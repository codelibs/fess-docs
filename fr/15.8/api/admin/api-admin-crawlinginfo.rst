==========================
API CrawlingInfo
==========================

Vue d'ensemble
==============

L'API CrawlingInfo permet de consulter et de gerer les informations de crawl (sessions de crawl) de |Fess|.
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

   * - Methode
     - Chemin
     - Description
   * - GET
     - /logs
     - Obtention de la liste des informations de crawl
   * - GET
     - /log/{id}
     - Obtention d'une information de crawl
   * - DELETE
     - /log/{id}
     - Suppression d'une information de crawl
   * - DELETE
     - /all
     - Suppression groupee des sessions de crawl (hors sessions en cours)

Obtention de la liste des informations de crawl
===============================================

Requete
-------

::

    GET /api/admin/crawlinginfo/logs

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
     - Nombre d'elements par page (defaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numero de page (base 1, defaut : 1)
   * - ``sessionId``
     - String
     - Non
     - Filtre par ID de session (correspondance partielle)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
          }
        ],
        "total": 10
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID de l'information de crawl
   * - ``sessionId``
     - ID de la session
   * - ``name``
     - Nom de la session
   * - ``expiredTime``
     - Date d'expiration (millisecondes epoch ; retournee sous forme de chaine)
   * - ``createdTime``
     - Heure de creation (millisecondes epoch ; retournee sous forme de nombre)

.. note::

   Chaque objet de journal dans la reponse inclut egalement un champ interne ``crudMode``
   (un entier indiquant le mode d'operation CRUD, toujours ``0`` pour les operations de lecture).
   Les clients peuvent l'ignorer en toute securite.

Obtention d'une information de crawl
====================================

Requete
-------

::

    GET /api/admin/crawlinginfo/log/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
        }
      }
    }

Suppression d'une information de crawl
======================================

Requete
-------

::

    DELETE /api/admin/crawlinginfo/log/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Suppression groupee des sessions de crawl
==========================================

Supprime toutes les sessions de crawl (ainsi que leurs donnees de parametres), a l'exception de celles qui sont actuellement en cours d'execution. Il n'y a pas de seuil d'age ou de duree ; toute session qui n'est pas en cours d'execution est supprimee.

Requete
-------

::

    DELETE /api/admin/crawlinginfo/all

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

Obtention de la liste des informations de crawl
-----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrage par session specifique
-------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

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

Suppression groupee des sessions
--------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-failureurl` - API des URLs en echec
- :doc:`api-admin-joblog` - API des journaux de taches
- :doc:`../../admin/crawlinginfo-guide` - Guide des informations de crawl
