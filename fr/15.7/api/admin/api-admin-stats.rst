==========================
API Stats
==========================

Vue d'ensemble
==============

L'API Stats est une API permettant d'obtenir les metriques systeme du serveur sur lequel |Fess| s'execute.
Elle permet de consulter les statistiques de la JVM, du systeme d'exploitation, du processus, du cluster du moteur de recherche (OpenSearch) et du systeme de fichiers.

.. note::

   Cette API ne retourne pas de donnees d'analyse de recherche telles que les requetes de recherche ou les clics.
   Pour la recherche et la gestion des documents dans l'index, consultez :doc:`api-admin-searchlist`.

URL de base
===========

::

    /api/admin/stats

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
     - Obtention des statistiques systeme

Obtention des statistiques systeme
==================================

Requete
-------

::

    GET /api/admin/stats

Cet endpoint n'accepte pas de parametres de requete.

Reponse
-------

La reponse contient ``version`` indiquant la version du produit, ``status`` indiquant le resultat du traitement,
et un objet ``stats`` contenant les metriques systeme.
``stats`` possede cinq cles : ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "stats": {
          "jvm": {
            "memory": {
              "heap": {
                "used": 536870912,
                "committed": 1073741824,
                "max": 2147483648,
                "percent": 25
              },
              "nonHeap": {
                "used": 134217728,
                "committed": 268435456
              }
            },
            "pools": [
              {"key": "mapped", "count": 1, "used": 4096, "capacity": 4096}
            ],
            "gc": [
              {"key": "young", "count": 12, "time": 345}
            ],
            "threads": {"count": 80, "peak": 95},
            "classes": {"loaded": 12000, "total_loaded": 12500, "unloaded": 500},
            "uptime": 3600000
          },
          "os": {
            "memory": {
              "physical": {"free": 2147483648, "total": 8589934592},
              "swapSpace": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "loadAverages": [0.5, 0.4, 0.3]
          },
          "process": {
            "fileFescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtualMemory": {"total": 4294967296}
          },
          "engine": {
            "clusterName": "fess",
            "numberOfNodes": 1,
            "numberOfDataNodes": 1,
            "activePrimaryShards": 10,
            "activeShards": 10,
            "activeShardsPercent": 100.0,
            "relocatingShards": 0,
            "initializingShards": 0,
            "unassignedShards": 0,
            "delayedUnassignedShards": 0,
            "numberOfPendingTasks": 0,
            "numberOfInFlightFetch": 0,
            "status": "green"
          },
          "fs": [
            {
              "path": "/",
              "total": 107374182400,
              "free": 53687091200,
              "usable": 53687091200,
              "used": 53687091200,
              "percent": 50
            }
          ]
        }
      }
    }

Champs de la reponse
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Champ
     - Description
   * - ``jvm``
     - Statistiques de la JVM. Contient ``memory`` (``heap`` / ``nonHeap``), ``pools`` (pools de tampons), ``gc`` (GC), ``threads``, ``classes``, ``uptime`` (en millisecondes).
   * - ``os``
     - Statistiques du systeme d'exploitation. Contient ``memory`` (``physical`` / ``swapSpace``), ``cpu``, ``loadAverages`` (tableau des charges moyennes).
   * - ``process``
     - Statistiques du processus. Contient ``fileFescriptor`` (nombre de descripteurs de fichiers ouverts/maximum), ``cpu``, ``virtualMemory``.
   * - ``engine``
     - Etat du cluster du moteur de recherche (OpenSearch). Contient ``clusterName``, le nombre de noeuds, le nombre de shards, ``status``, etc. Si le cluster est inaccessible, ``status`` vaut ``"red"`` et ``exception`` contient le message d'erreur.
   * - ``fs``
     - Tableau des statistiques du systeme de fichiers. Pour chaque racine, contient ``path``, ``total``, ``free``, ``usable``, ``used`` (en octets), ``percent`` (taux d'utilisation).

.. note::

   Le nom de cle ``process.fileFescriptor`` respecte l'implementation du code source (ce n'est pas l'orthographe ``fileDescriptor``).

Exemples d'utilisation
======================

Obtention des statistiques systeme
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verification du taux d'utilisation du heap JVM
----------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Verification de l'etat du cluster du moteur de recherche
--------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API d'informations systeme
- :doc:`api-admin-searchlist` - API de recherche et de gestion des documents
