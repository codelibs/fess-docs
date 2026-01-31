==========================
API FailureUrl
==========================

Vue d'ensemble
==============

L'API FailureUrl permet de gerer les URLs en echec de crawl dans |Fess|.
Vous pouvez consulter et supprimer les URLs qui ont genere des erreurs pendant le crawl.

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
     - /
     - Obtention de la liste des URLs en echec
   * - DELETE
     - /{id}
     - Suppression d'une URL en echec
   * - DELETE
     - /delete-all
     - Suppression de toutes les URLs en echec

Obtention de la liste des URLs en echec
=======================================

Requete
-------

::

    GET /api/admin/failureurl

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
   * - ``errorCountMin``
     - Integer
     - Non
     - Filtre par nombre minimum d'erreurs
   * - ``configId``
     - String
     - Non
     - Filtre par ID de configuration

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
          }
        ],
        "total": 45
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Champ
     - Description
   * - ``id``
     - ID de l'URL en echec
   * - ``url``
     - URL en echec
   * - ``configId``
     - ID de la configuration de crawl
   * - ``errorName``
     - Nom de l'erreur
   * - ``errorLog``
     - Journal de l'erreur
   * - ``errorCount``
     - Nombre d'occurrences de l'erreur
   * - ``lastAccessTime``
     - Dernier temps d'acces
   * - ``threadName``
     - Nom du thread

Suppression d'une URL en echec
==============================

Requete
-------

::

    DELETE /api/admin/failureurl/{id}

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

Suppression de toutes les URLs en echec
=======================================

Requete
-------

::

    DELETE /api/admin/failureurl/delete-all

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``configId``
     - String
     - Non
     - Supprimer uniquement les URLs en echec de cette configuration
   * - ``errorCountMin``
     - Integer
     - Non
     - Supprimer uniquement les erreurs avec ce nombre minimum

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
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

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

Filtrage par nombre d'erreurs
-----------------------------

.. code-block:: bash

    # Obtenir uniquement les URLs avec 3 erreurs ou plus
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Obtention des URLs en echec d'une configuration specifique
----------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'une URL en echec
------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression de toutes les URLs en echec
---------------------------------------

.. code-block:: bash

    # Supprimer toutes les URLs en echec
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Supprimer uniquement les URLs en echec d'une configuration specifique
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Supprimer uniquement les URLs avec 3 erreurs ou plus
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

Agregation par type d'erreur
----------------------------

.. code-block:: bash

    # Compter par type d'erreur
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`api-admin-joblog` - API des journaux de taches
- :doc:`../../admin/failureurl-guide` - Guide de gestion des URLs en echec
