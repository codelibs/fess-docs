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
     - Suppression groupee des anciennes sessions de crawl

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
     - Nombre d'elements par page
   * - ``page``
     - Integer
     - Non
     - Numero de page
   * - ``sessionId``
     - String
     - Non
     - Filtre par ID de session

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
     - Date d'expiration
   * - ``createdTime``
     - Heure de creation (millisecondes epoch)

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

Suppression groupee des anciennes sessions de crawl
===================================================

Supprime en bloc les anciennes sessions de crawl, a l'exception des sessions en cours d'execution.

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

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=0" \
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

Suppression groupee des anciennes sessions
------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-failureurl` - API des URLs en echec
- :doc:`api-admin-joblog` - API des journaux de taches
- :doc:`../../admin/crawlinginfo-guide` - Guide des informations de crawl
