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
     - Nombre d'elements par page (defaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numero de page (commence a 1, defaut : 1)
   * - ``url``
     - String
     - Non
     - Filtre par URL (les caracteres generiques ``*`` ``?`` sont supportes)
   * - ``errorCountMin``
     - Integer
     - Non
     - Borne inferieure du nombre d'erreurs (superieur ou egal a la valeur specifiee)
   * - ``errorCountMax``
     - Integer
     - Non
     - Borne superieure du nombre d'erreurs (inferieur ou egal a la valeur specifiee)
   * - ``errorName``
     - String
     - Non
     - Filtre par nom d'erreur (correspondance avec caracteres generiques sur le nom de classe complet stocke ; ``*`` ``?`` supportes)

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
            "errorName": "java.net.ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": "3",
            "lastAccessTime": "1738144800000",
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "org.codelibs.fess.exception.ContentNotFoundException",
            "errorLog": "Not found: https://example.com/not-found",
            "errorCount": "1",
            "lastAccessTime": "1738143000000",
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
     - Nom de l'erreur (nom de classe complet de l'exception survenue ; ex. ``java.net.ConnectException``)
   * - ``errorLog``
     - Journal d'erreur (message de l'exception ou trace de la pile)
   * - ``errorCount``
     - Nombre d'occurrences de l'erreur (valeur numerique sous forme de chaine)
   * - ``lastAccessTime``
     - Heure du dernier acces (millisecondes epoch sous forme de chaine)
   * - ``configId``
     - ID de la configuration de crawl

.. note::

   Tous les champs de la reponse sont retournes sous forme de chaines (JSON string). ``errorCount`` est une valeur numerique representee sous forme de chaine, et ``lastAccessTime`` est le nombre de millisecondes epoch represente sous forme de chaine.

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
          "errorName": "java.net.ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": "3",
          "lastAccessTime": "1738144800000",
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

``errorName`` contient le nom de classe complet de l'exception survenue pendant le crawl, tel qu'il a ete capture. Il ne s'agit pas d'une enumeration fixe ; tout nom de classe peut apparaitre selon l'exception levee. Voici quelques exemples representatifs.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Nom de l'erreur (exemple)
     - Description
   * - ``java.net.ConnectException``
     - Connexion refusee (impossible de se connecter au serveur)
   * - ``java.net.UnknownHostException``
     - Nom d'hote impossible a resoudre (erreur DNS)
   * - ``java.net.SocketTimeoutException``
     - Delai de connexion ou de lecture depasse
   * - ``javax.net.ssl.SSLException``
     - Erreur de negociation SSL/TLS ou de certificat
   * - ``java.io.IOException``
     - Erreur d'entree/sortie
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - URL ayant retourne un code de statut HTTP configure dans ``crawler.failure.url.status.codes`` (defaut : 403, 404, 410)
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - Le contenu a depasse la longueur maximale autorisee

Exemples d'utilisation
======================

Obtention de la liste des URLs en echec
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=1" \
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

    # errorName contient le nom de classe complet ; specifier avec un caractere generique
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=*ConnectException" \
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
