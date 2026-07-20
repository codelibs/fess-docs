==========================
API Stats
==========================

Vue d'ensemble
==============

L'API Stats est une API permettant d'obtenir les métriques système du serveur sur lequel |Fess| s'exécute.
Elle permet de consulter les statistiques de la JVM, du système d'exploitation, du processus, du cluster du moteur de recherche (OpenSearch) et du système de fichiers.

.. note::

   Cette API ne retourne pas de données d'analyse de recherche telles que les requêtes de recherche ou les clics.
   Pour la recherche et la gestion des documents dans l'index, consultez :doc:`api-admin-searchlist`.

URL de base
===========

::

    /api/admin/stats

L'accès à cette API nécessite un jeton d'accès disposant de la permission ``Radmin-api``.
Pour plus de détails sur l'authentification, consultez :doc:`api-admin-overview`.

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Méthode
     - Chemin
     - Description
   * - GET
     - /
     - Obtention des statistiques système

Obtention des statistiques système
===================================

Requête
-------

::

    GET /api/admin/stats

Cet endpoint n'accepte pas de paramètres de requête.

Réponse
-------

La réponse contient ``version`` indiquant la version du produit, ``status`` indiquant
le résultat du traitement, et un objet ``stats`` contenant les métriques système.
``stats`` possède cinq clés : ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. note::

   Les noms de champs des objets sous ``stats`` sont écrits en snake_case (mots en minuscules séparés par des tirets bas, par exemple ``non_heap``).
   Les champs dont la valeur est ``null`` sont omis de la réponse.

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
              "non_heap": {
                "used": 134217728,
                "committed": 268435456,
                "max": 0,
                "percent": 0
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
              "swap_space": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "load_averages": [0.5, 0.4, 0.3]
          },
          "process": {
            "file_fescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtual_memory": {"total": 4294967296}
          },
          "engine": {
            "cluster_name": "fess",
            "number_of_nodes": 1,
            "number_of_data_nodes": 1,
            "active_primary_shards": 10,
            "active_shards": 10,
            "active_shards_percent": 100.0,
            "relocating_shards": 0,
            "initializing_shards": 0,
            "unassigned_shards": 0,
            "delayed_unassigned_shards": 0,
            "number_of_pending_tasks": 0,
            "number_of_in_flight_fetch": 0,
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

Champs de la réponse (niveau supérieur)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Champ
     - Description
   * - ``version``
     - La version du produit |Fess| (par exemple ``15.7.0``).
   * - ``status``
     - Un code indiquant le résultat du traitement. ``0`` indique un succès.
   * - ``stats``
     - Un objet contenant les métriques système. Il possède cinq clés : ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

``jvm`` : Statistiques JVM
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``memory.heap.used``
     - Mémoire heap utilisée (octets).
   * - ``memory.heap.committed``
     - Mémoire heap allouée (octets).
   * - ``memory.heap.max``
     - Mémoire heap maximale (octets).
   * - ``memory.heap.percent``
     - Pourcentage d'utilisation de la mémoire heap (%).
   * - ``memory.non_heap.used``
     - Mémoire non-heap utilisée (octets).
   * - ``memory.non_heap.committed``
     - Mémoire non-heap allouée (octets).
   * - ``memory.non_heap.max``
     - Mémoire non-heap maximale (octets). Dans l'implémentation actuelle, cette valeur n'est pas définie et retourne toujours ``0``.
   * - ``memory.non_heap.percent``
     - Pourcentage d'utilisation de la mémoire non-heap (%). Dans l'implémentation actuelle, cette valeur n'est pas définie et retourne toujours ``0``.
   * - ``pools``
     - Tableau des pools de tampons. Chaque élément contient ``key`` (nom du pool), ``count`` (nombre de tampons), ``used`` (mémoire utilisée, octets) et ``capacity`` (capacité totale, octets).
   * - ``gc``
     - Tableau des ramasse-miettes. Chaque élément contient ``key`` (nom du collecteur), ``count`` (nombre de collections) et ``time`` (temps de collection cumulé, millisecondes).
   * - ``threads.count``
     - Nombre actuel de threads.
   * - ``threads.peak``
     - Nombre maximal de threads atteint.
   * - ``classes.loaded``
     - Nombre de classes actuellement chargées.
   * - ``classes.total_loaded``
     - Nombre total de classes chargées depuis le démarrage de la JVM.
   * - ``classes.unloaded``
     - Nombre total de classes déchargées.
   * - ``uptime``
     - Durée de fonctionnement de la JVM (millisecondes).

``os`` : Statistiques du système d'exploitation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``memory.physical.free``
     - Mémoire physique disponible (octets).
   * - ``memory.physical.total``
     - Mémoire physique totale (octets).
   * - ``memory.swap_space.free``
     - Espace d'échange disponible (octets).
   * - ``memory.swap_space.total``
     - Espace d'échange total (octets).
   * - ``cpu.percent``
     - Pourcentage d'utilisation globale du processeur (%).
   * - ``load_averages``
     - Tableau des charges moyennes (1, 5 et 15 minutes). Les valeurs qui ne peuvent pas être obtenues peuvent valoir ``-1``.

``process`` : Statistiques du processus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``file_fescriptor.open``
     - Nombre de descripteurs de fichiers actuellement ouverts.
   * - ``file_fescriptor.max``
     - Nombre maximal de descripteurs de fichiers pouvant être ouverts.
   * - ``cpu.percent``
     - Pourcentage d'utilisation du processeur par le processus (%).
   * - ``cpu.total``
     - Temps CPU cumulé utilisé par le processus (millisecondes).
   * - ``virtual_memory.total``
     - Taille totale de la mémoire virtuelle du processus (octets).

.. note::

   Le nom de clé ``process.file_fescriptor`` est la conversion en snake_case du nom de champ du code source
   ``fileFescriptor`` (qui provient d'une faute d'orthographe de ``fileDescriptor``). Il correspond à
   l'implémentation et n'est pas une erreur dans ce document.

``engine`` : Statistiques du cluster du moteur de recherche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Informations sur l'état de santé du cluster du moteur de recherche (OpenSearch).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``cluster_name``
     - Nom du cluster.
   * - ``number_of_nodes``
     - Nombre total de noeuds dans le cluster.
   * - ``number_of_data_nodes``
     - Nombre de noeuds de données.
   * - ``active_primary_shards``
     - Nombre de shards primaires actifs.
   * - ``active_shards``
     - Nombre de shards actifs.
   * - ``active_shards_percent``
     - Pourcentage de shards actifs (%).
   * - ``relocating_shards``
     - Nombre de shards en cours de déplacement.
   * - ``initializing_shards``
     - Nombre de shards en cours d'initialisation.
   * - ``unassigned_shards``
     - Nombre de shards non assignés.
   * - ``delayed_unassigned_shards``
     - Nombre de shards non assignés avec délai.
   * - ``number_of_pending_tasks``
     - Nombre de tâches en attente.
   * - ``number_of_in_flight_fetch``
     - Nombre d'opérations de récupération en cours.
   * - ``status``
     - État de santé du cluster (``green`` / ``yellow`` / ``red``).
   * - ``exception``
     - Message d'erreur inclus uniquement en cas d'erreur, par exemple lorsque le cluster est inaccessible. Dans ce cas, ``status`` prend la valeur ``red``.

``fs`` : Statistiques du système de fichiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tableau des statistiques pour chaque racine (les racines obtenues par ``File.listRoots()``).

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``path``
     - Chemin absolu de la racine.
   * - ``total``
     - Capacité totale (octets).
   * - ``free``
     - Capacité disponible (octets).
   * - ``usable``
     - Capacité utilisable (octets).
   * - ``used``
     - Capacité utilisée (octets). Correspond à ``total`` moins ``usable``.
   * - ``percent``
     - Pourcentage d'utilisation (%).

Exemples d'utilisation
======================

Obtention des statistiques système
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Vérification du taux d'utilisation du heap JVM
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Vérification de l'état du cluster du moteur de recherche
---------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Informations complémentaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API d'informations système
- :doc:`api-admin-searchlist` - API de recherche et de gestion des documents
