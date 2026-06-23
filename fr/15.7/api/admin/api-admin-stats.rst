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

L'acces a cette API necessite un jeton d'acces disposant de la permission ``Radmin-api``.
Pour plus de details sur l'authentification, consultez :doc:`api-admin-overview`.

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
===================================

Requete
-------

::

    GET /api/admin/stats

Cet endpoint n'accepte pas de parametres de requete.

Reponse
-------

La reponse contient ``version`` indiquant la version du produit, ``status`` indiquant
le resultat du traitement, et un objet ``stats`` contenant les metriques systeme.
``stats`` possede cinq cles : ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

.. note::

   Les noms de champs des objets sous ``stats`` sont ecrits en snake_case (mots en minuscules separes par des tirets bas, par exemple ``non_heap``).
   Les champs dont la valeur est ``null`` sont omis de la reponse.

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

Champs de la reponse (niveau superieur)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Champ
     - Description
   * - ``version``
     - La version du produit |Fess| (par exemple ``15.7.0``).
   * - ``status``
     - Un code indiquant le resultat du traitement. ``0`` indique un succes.
   * - ``stats``
     - Un objet contenant les metriques systeme. Il possede cinq cles : ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs``.

``jvm`` : Statistiques JVM
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``memory.heap.used``
     - Memoire heap utilisee (octets).
   * - ``memory.heap.committed``
     - Memoire heap allouee (octets).
   * - ``memory.heap.max``
     - Memoire heap maximale (octets).
   * - ``memory.heap.percent``
     - Pourcentage d'utilisation de la memoire heap (%).
   * - ``memory.non_heap.used``
     - Memoire non-heap utilisee (octets).
   * - ``memory.non_heap.committed``
     - Memoire non-heap allouee (octets).
   * - ``memory.non_heap.max``
     - Memoire non-heap maximale (octets). Dans l'implementation actuelle, cette valeur n'est pas definie et retourne toujours ``0``.
   * - ``memory.non_heap.percent``
     - Pourcentage d'utilisation de la memoire non-heap (%). Dans l'implementation actuelle, cette valeur n'est pas definie et retourne toujours ``0``.
   * - ``pools``
     - Tableau des pools de tampons. Chaque element contient ``key`` (nom du pool), ``count`` (nombre de tampons), ``used`` (memoire utilisee, octets) et ``capacity`` (capacite totale, octets).
   * - ``gc``
     - Tableau des ramasse-miettes. Chaque element contient ``key`` (nom du collecteur), ``count`` (nombre de collections) et ``time`` (temps de collection cumule, millisecondes).
   * - ``threads.count``
     - Nombre actuel de threads.
   * - ``threads.peak``
     - Nombre maximal de threads atteint.
   * - ``classes.loaded``
     - Nombre de classes actuellement chargees.
   * - ``classes.total_loaded``
     - Nombre total de classes chargees depuis le demarrage de la JVM.
   * - ``classes.unloaded``
     - Nombre total de classes dechargees.
   * - ``uptime``
     - Duree de fonctionnement de la JVM (millisecondes).

``os`` : Statistiques du systeme d'exploitation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Champ
     - Description
   * - ``memory.physical.free``
     - Memoire physique disponible (octets).
   * - ``memory.physical.total``
     - Memoire physique totale (octets).
   * - ``memory.swap_space.free``
     - Espace d'echange disponible (octets).
   * - ``memory.swap_space.total``
     - Espace d'echange total (octets).
   * - ``cpu.percent``
     - Pourcentage d'utilisation globale du processeur (%).
   * - ``load_averages``
     - Tableau des charges moyennes (1, 5 et 15 minutes). Les valeurs qui ne peuvent pas etre obtenues peuvent valoir ``-1``.

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
     - Nombre maximal de descripteurs de fichiers pouvant etre ouverts.
   * - ``cpu.percent``
     - Pourcentage d'utilisation du processeur par le processus (%).
   * - ``cpu.total``
     - Temps CPU cumule utilise par le processus (millisecondes).
   * - ``virtual_memory.total``
     - Taille totale de la memoire virtuelle du processus (octets).

.. note::

   Le nom de cle ``process.file_fescriptor`` est la conversion en snake_case du nom de champ du code source
   ``fileFescriptor`` (qui provient d'une faute d'orthographe de ``fileDescriptor``). Il correspond a
   l'implementation et n'est pas une erreur dans ce document.

``engine`` : Statistiques du cluster du moteur de recherche
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Informations sur l'etat de sante du cluster du moteur de recherche (OpenSearch).

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
     - Nombre de noeuds de donnees.
   * - ``active_primary_shards``
     - Nombre de shards primaires actifs.
   * - ``active_shards``
     - Nombre de shards actifs.
   * - ``active_shards_percent``
     - Pourcentage de shards actifs (%).
   * - ``relocating_shards``
     - Nombre de shards en cours de deplacement.
   * - ``initializing_shards``
     - Nombre de shards en cours d'initialisation.
   * - ``unassigned_shards``
     - Nombre de shards non assignes.
   * - ``delayed_unassigned_shards``
     - Nombre de shards non assignes avec delai.
   * - ``number_of_pending_tasks``
     - Nombre de taches en attente.
   * - ``number_of_in_flight_fetch``
     - Nombre d'operations de recuperation en cours.
   * - ``status``
     - Etat de sante du cluster (``green`` / ``yellow`` / ``red``).
   * - ``exception``
     - Message d'erreur inclus uniquement en cas d'erreur, par exemple lorsque le cluster est inaccessible. Dans ce cas, ``status`` prend la valeur ``red``.

``fs`` : Statistiques du systeme de fichiers
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
     - Capacite totale (octets).
   * - ``free``
     - Capacite disponible (octets).
   * - ``usable``
     - Capacite utilisable (octets).
   * - ``used``
     - Capacite utilisee (octets). Correspond a ``total`` moins ``usable``.
   * - ``percent``
     - Pourcentage d'utilisation (%).

Exemples d'utilisation
======================

Obtention des statistiques systeme
-----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

Verification du taux d'utilisation du heap JVM
------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

Verification de l'etat du cluster du moteur de recherche
---------------------------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-systeminfo` - API d'informations systeme
- :doc:`api-admin-searchlist` - API de recherche et de gestion des documents
