==========================
API FailureUrl
==========================

Vue d'ensemble
==============

L'API FailureUrl permet de gerer les URLs en echec lors du crawl de |Fess|.
Vous pouvez obtenir la liste des URLs ayant provoque une erreur pendant le crawl, les consulter individuellement, les supprimer, etc.

URL de base
===========

::

    /api/admin/failureurl

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
     - Obtention de la liste des URLs en echec
   * - GET
     - /log/{id}
     - Obtention d'une URL en echec
   * - DELETE
     - /log/{id}
     - Suppression d'une URL en echec
   * - DELETE
     - /all
     - Suppression de toutes les URLs en echec

Obtention de la liste des URLs en echec
=======================================

Requete
-------

::

    GET /api/admin/failureurl/logs

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
   * - ``url``
     - String
     - Non
     - Filtre par URL
   * - ``errorCountMin``
     - Integer
     - Non
     - Filtre par nombre minimum d'erreurs
   * - ``errorCountMax``
     - Integer
     - Non
     - Filtre par nombre maximum d'erreurs
   * - ``errorName``
     - String
     - Non
     - Filtre par nom d'erreur

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "threadName": "Crawler-1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": 1738144800000,
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": 1738143000000,
            "configId": "webConfig_id_1"
          }
        ],
        "total": 45
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
     - ID de l'URL en echec
   * - ``url``
     - URL en echec
   * - ``threadName``
     - Nom du thread
   * - ``errorName``
     - Nom de l'erreur
   * - ``errorLog``
     - Journal d'erreur
   * - ``errorCount``
     - Nombre d'occurrences de l'erreur
   * - ``lastAccessTime``
     - Heure du dernier acces (millisecondes epoch)
   * - ``configId``
     - ID de la configuration de crawl

Obtention d'une URL en echec
============================

Requete
-------

::

    GET /api/admin/failureurl/log/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "threadName": "Crawler-1",
          "errorName": "ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": 3,
          "lastAccessTime": 1738144800000,
          "configId": "webConfig_id_1"
        }
      }
    }

Suppression d'une URL en echec
==============================

Requete
-------

::

    DELETE /api/admin/failureurl/log/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Suppression de toutes les URLs en echec
=======================================

Supprime toutes les URLs en echec. Cette operation ne prend aucun parametre.

Requete
-------

::

    DELETE /api/admin/failureurl/all

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Types d'erreurs
===============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Nom de l'erreur
     - Description
   * - ``ConnectException``
     - Erreur de connexion
   * - ``HttpStatusException``
     - Erreur de statut HTTP (404, 500, etc.)
   * - ``SocketTimeoutException``
     - Erreur de delai d'attente
   * - ``UnknownHostException``
     - Erreur de resolution du nom d'hote
   * - ``SSLException``
     - Erreur de certificat SSL
   * - ``IOException``
     - Erreur d'entree/sortie

Exemples d'utilisation
======================

Obtention de la liste des URLs en echec
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrage par nombre d'erreurs
-----------------------------

.. code-block:: bash

    # Obtenir uniquement les URLs ayant echoue 3 fois ou plus
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrage par nom d'erreur
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention d'une URL en echec
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'une URL en echec
------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression de toutes les URLs en echec
---------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Agregation par type d'erreur
----------------------------

.. code-block:: bash

    # Compter par type d'erreur
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`api-admin-joblog` - API des journaux de taches
- :doc:`../../admin/failureurl-guide` - Guide de gestion des URLs en echec
