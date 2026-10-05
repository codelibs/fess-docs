==========================
API FailureUrl
==========================

Vue d'ensemble
==============

L'API FailureUrl permet de gérer les URLs en échec lors du crawl de |Fess|.
Vous pouvez obtenir la liste des URLs ayant provoqué une erreur pendant le crawl, les consulter individuellement, les supprimer, etc.

URL de base
===========

::

    /api/admin/failureurl

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
     - Obtention de la liste des URLs en échec
   * - GET
     - /log/{id}
     - Obtention d'une URL en échec
   * - DELETE
     - /log/{id}
     - Suppression d'une URL en échec
   * - DELETE
     - /all
     - Suppression de toutes les URLs en échec

Obtention de la liste des URLs en échec
=======================================

Requête
-------

::

    GET /api/admin/failureurl/logs

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
     - Nombre d'éléments par page (défaut : 20)
   * - ``page``
     - Integer
     - Non
     - Numéro de page (commence à 1, défaut : 1)
   * - ``url``
     - String
     - Non
     - Filtre par URL (les caractères génériques ``*`` ``?`` sont supportés)
   * - ``error_count_min``
     - Integer
     - Non
     - Borne inférieure du nombre d'erreurs (supérieur ou égal à la valeur spécifiée)
   * - ``error_count_max``
     - Integer
     - Non
     - Borne supérieure du nombre d'erreurs (inférieur ou égal à la valeur spécifiée)
   * - ``error_name``
     - String
     - Non
     - Filtre par nom d'erreur (correspondance avec caractères génériques sur le nom de classe complet stocké ; ``*`` ``?`` supportés)

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "thread_name": "Crawler-1",
            "error_name": "java.net.ConnectException",
            "error_log": "Connection refused: connect",
            "error_count": "3",
            "last_access_time": "1738144800000",
            "config_id": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "thread_name": "Crawler-2",
            "error_name": "org.codelibs.fess.exception.ContentNotFoundException",
            "error_log": "Not found: https://example.com/not-found",
            "error_count": "1",
            "last_access_time": "1738143000000",
            "config_id": "webConfig_id_1"
          }
        ],
        "total": 45
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
     - ID de l'URL en échec
   * - ``url``
     - URL en échec
   * - ``thread_name``
     - Nom du thread
   * - ``error_name``
     - Nom de l'erreur (nom de classe complet de l'exception survenue ; ex. ``java.net.ConnectException``)
   * - ``error_log``
     - Journal d'erreur (message de l'exception ou trace de la pile)
   * - ``error_count``
     - Nombre d'occurrences de l'erreur (valeur numérique sous forme de chaîne)
   * - ``last_access_time``
     - Heure du dernier accès (millisecondes epoch sous forme de chaîne)
   * - ``config_id``
     - ID de la configuration de crawl

.. note::

   Tous les champs de la réponse sont retournés sous forme de chaînes (JSON string). ``error_count`` est une valeur numérique représentée sous forme de chaîne, et ``last_access_time`` est le nombre de millisecondes epoch représenté sous forme de chaîne.

Obtention d'une URL en échec
============================

Requête
-------

::

    GET /api/admin/failureurl/log/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "thread_name": "Crawler-1",
          "error_name": "java.net.ConnectException",
          "error_log": "Connection refused: connect",
          "error_count": "3",
          "last_access_time": "1738144800000",
          "config_id": "webConfig_id_1"
        }
      }
    }

Suppression d'une URL en échec
==============================

Requête
-------

::

    DELETE /api/admin/failureurl/log/{id}

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Suppression de toutes les URLs en échec
=======================================

Supprime toutes les URLs en échec. Cette opération ne prend aucun paramètre.

Requête
-------

::

    DELETE /api/admin/failureurl/all

Réponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Types d'erreurs
===============

``error_name`` contient le nom de classe complet de l'exception survenue pendant le crawl, tel qu'il a été capturé. Il ne s'agit pas d'une énumération fixe ; tout nom de classe peut apparaître selon l'exception levée. Voici quelques exemples représentatifs.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Nom de l'erreur (exemple)
     - Description
   * - ``java.net.ConnectException``
     - Connexion refusée (impossible de se connecter au serveur)
   * - ``java.net.UnknownHostException``
     - Nom d'hôte impossible à résoudre (erreur DNS)
   * - ``java.net.SocketTimeoutException``
     - Délai de connexion ou de lecture dépassé
   * - ``javax.net.ssl.SSLException``
     - Erreur de négociation SSL/TLS ou de certificat
   * - ``java.io.IOException``
     - Erreur d'entrée/sortie
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - URL ayant retourné un code de statut HTTP configuré dans ``crawler.failure.url.status.codes`` (défaut : 403, 404, 410)
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - Le contenu a dépassé la longueur maximale autorisée

Exemples d'utilisation
======================

Obtention de la liste des URLs en échec
---------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 100, "page": 1}'

Filtrage par nombre d'erreurs
-----------------------------

.. code-block:: bash

    # Obtenir uniquement les URLs ayant echoue 3 fois ou plus
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"error_count_min": 3}'

Filtrage par nom d'erreur
-------------------------

.. code-block:: bash

    # error_name contient le nom de classe complet ; specifier avec un caractere generique
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"error_name": "*ConnectException"}'

Obtention d'une URL en échec
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression d'une URL en échec
------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression de toutes les URLs en échec
---------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Agrégation par type d'erreur
----------------------------

.. code-block:: bash

    # Compter par type d'erreur
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 1000}' | \
         jq '[.response.logs[].error_name] | group_by(.) | map({error: .[0], count: length})'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`api-admin-joblog` - API des journaux de tâches
- :doc:`../../admin/failureurl-guide` - Guide de gestion des URLs en échec
