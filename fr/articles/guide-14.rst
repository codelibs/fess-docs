===========================================
Mettre Fess à l'échelle selon la croissance
===========================================

Introduction
============

Lorsque le nombre de documents et d'utilisateurs augmente, des problèmes apparaissent : « l'exploration n'est plus terminée le matin », « la recherche est devenue lente », « Fess s'est arrêté sur une OutOfMemoryError ».
Ajouter immédiatement des serveurs ne résout pas forcément ces problèmes.
Fess fonctionne sous la forme de plusieurs processus JVM, et c'est souvent un seul d'entre eux qui manque de ressources.

Cet article porte sur Fess 15.9 et décrit la mise à l'échelle dans l'ordre suivant.

1. Déterminer quel processus manque de quoi
2. Ajuster la mémoire et le parallélisme de l'exploration sur un seul serveur
3. Déplacer OpenSearch sur un serveur distinct
4. Passer OpenSearch à un cluster de trois nœuds
5. Exécuter plusieurs serveurs Fess

La mise en place de la surveillance (contrôles de santé, journaux, notifications) et les sauvegardes sont traitées dans :doc:`guide-10`.

Les processus qui composent Fess
================================

Même lorsque Fess fonctionne sur un seul serveur, ses paramètres de mémoire sont répartis comme suit.

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Processus
     - Rôle
     - Tas par défaut
     - Où le configurer
   * - Serveur Fess
     - Page de recherche, console d'administration, API, planificateur
     - Paquet ZIP : minimum 256m, maximum 2g ; paquets RPM/DEB et image Docker : 512m
     - Variable d'environnement ``FESS_HEAP_SIZE``
   * - Robot d'exploration
     - JVM distincte lancée pour chaque tâche d'exploration
     - Maximum 512m
     - ``jvm.crawler.options`` dans ``fess_config.properties``
   * - Génération des suggestions, génération des vignettes
     - JVM distincte lancée pour chaque tâche
     - Maximum 256m
     - ``jvm.suggest.options``, ``jvm.thumbnail.options``
   * - OpenSearch
     - Stocke l'index et exécute les recherches
     - 1g dans ``compose-opensearch3.yaml`` de docker-fess
     - ``OPENSEARCH_JAVA_OPTS`` ou ``config/jvm.options``

Le traitement des chunks utilisé par la recherche sémantique dispose aussi de sa propre JVM (``jvm.chunk.options``, maximum 1g) ; il est traité dans :doc:`guide-18`.

Si ``fess-crawler.log`` contient une OutOfMemoryError, c'est la JVM du robot d'exploration qui manque de mémoire.
Dans ce cas, augmenter ``FESS_HEAP_SIZE`` n'a aucun effet.

Déterminer ce qui manque
========================

Selon le symptôme, vérifiez les emplacements suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptôme
     - Où vérifier
   * - La recherche est lente
     - Dans l'onglet [Performances] de [Informations système] > [Journal de recherche], examinez les temps de réponse p95 et p99 ainsi que les termes de recherche lents. Distinguez si seuls certains termes sont lents ou si tout est lent.
   * - L'exploration ne se termine pas
     - Dans [Informations système] > [Journal des tâches], suivez l'évolution des heures de début et de fin des tâches d'exploration. Si ``fess-crawler.log`` affiche en continu ``Cpu Load XX% is greater than 50%``, l'exploration est mise en attente par le contrôle de charge décrit plus loin.
   * - Le robot d'exploration s'arrête
     - Recherchez ``OutOfMemoryError`` dans ``fess-crawler.log``.
   * - Le serveur Fess s'arrête ou la console d'administration est lente
     - Recherchez ``OutOfMemoryError`` dans ``fess.log`` et consultez ``response.stats.jvm.memory.heap.percent`` dans ``/api/admin/stats``.
   * - OpenSearch est lent
     - Consultez ``response.stats.engine.status`` dans ``/api/admin/stats`` et l'utilisation du tas dans ``_cat/nodes`` d'OpenSearch. Une ``circuit_breaker_exception`` est le signe d'un tas insuffisant.

``/api/admin/stats`` renvoie l'état de la JVM et du système d'exploitation du serveur Fess qui a reçu la requête, ainsi que l'état du cluster OpenSearch.
La JVM du robot d'exploration et le tas de chaque nœud OpenSearch n'y figurent pas.
L'appel nécessite un jeton d'accès disposant de la permission ``admin-api``.
Pour le créer, consultez `Vue d'ensemble de l'API Admin <https://fess.codelibs.org/fr/stable/api/admin/api-admin-overview.html>`__ ; pour les champs de la réponse, consultez `API Stats <https://fess.codelibs.org/fr/stable/api/admin/api-admin-stats.html>`__.

Pour le tas de chaque nœud OpenSearch, interrogez directement OpenSearch.

::

    $ curl -s 'http://localhost:9200/_cat/nodes?v&h=name,heap.max,heap.percent,ram.percent,cpu'

La commande suivante permet de vérifier le nombre de documents et la taille de l'index.
``fess.search`` est l'alias de l'index utilisé pour la recherche.

::

    $ curl -s 'http://localhost:9200/_cat/indices/fess.search?v&h=index,docs.count,pri.store.size,store.size'

Ajuster un seul serveur
=======================

Modifier le tas du serveur Fess
-------------------------------

Avec Docker, ajoutez ``FESS_HEAP_SIZE`` à ``environment`` de ``fess01`` dans ``compose.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_HEAP_SIZE=2g"

Si vous modifiez ``environment`` ou ``volumes`` de ``fess01`` dans ``compose.yaml`` et exécutez ``docker compose ... up -d``, le conteneur ``fess01`` est recréé.
Les paramètres modifiés dans [Système] > [Général] se trouvent dans ``system.properties`` à l'intérieur du conteneur ; ils sont donc perdus lors de la recréation.
Il en va de même chaque fois qu'une autre étape de cet article modifie ``compose.yaml``.
Effectuez d'abord une sauvegarde en suivant la procédure de :doc:`guide-10`.

Pour le paquet RPM, modifiez ``FESS_HEAP_SIZE=512m`` dans ``/etc/sysconfig/fess`` ; pour le paquet DEB, dans ``/etc/default/fess``. Redémarrez ensuite Fess.
Pour le paquet ZIP, exportez ``FESS_HEAP_SIZE`` dans l'environnement qui lance Fess.

Vérifiez que la modification est prise en compte à l'aide des arguments des processus en cours d'exécution.
Avec Docker, procédez comme suit.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -T fess01 sh -c 'cat /proc/[0-9]*/cmdline 2>/dev/null' | tr '\0' '\n' | grep -e '^-Xmx' -e 'FessBoot' -e 'exec.Crawler'
    -Xmx2g
    org.codelibs.fess.FessBoot

La ligne qui suit ``-Xmx`` indique le type de processus.
``FessBoot`` est le serveur Fess, ``exec.Crawler`` le robot d'exploration.
Pour les paquets RPM/DEB et ZIP, exécutez directement sur le serveur Fess la commande située à l'intérieur de ``sh -c`` ainsi que tout ce qui suit.

Modifier le tas du robot d'exploration
--------------------------------------

``jvm.crawler.options`` est une valeur unique qui énumère des options JVM séparées par ``\n``.
Comme la valeur entière est remplacée, n'écrire que ``-Xmx1g`` supprime toutes les options par défaut, comme G1GC.
Conservez la valeur par défaut et ne modifiez que la ligne ``-Xmx512m``.

::

    -Xms128m\n\
    -Xmx1g\n\

Le fichier de configuration se trouve dans ``/etc/fess/fess_config.properties`` pour les paquets RPM/DEB et dans ``app/WEB-INF/classes/fess_config.properties`` pour le paquet ZIP.
Avec Docker, copiez ``fess_config.properties`` de l'image sur votre machine, modifiez-le, puis montez-le dans le conteneur sur ``/opt/fess/fess_config.properties``.
``/opt/fess`` est lu en priorité sur ``/etc/fess``.
Cette valeur s'étendant sur plusieurs lignes, elle ne se prête pas à une définition par ``-Dfess.config.`` dans ``FESS_JAVA_OPTS``.
Pour la procédure, consultez « Comment appliquer les fichiers de configuration » dans `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__.

Après le redémarrage de Fess, vérifiez dans « Propriétés de l'application » de [Informations système] > [Informations de configuration] que ``jvm.crawler.options`` contient ``-Xmx1g``.
La modification s'applique à partir du prochain robot d'exploration lancé.
Si vous exécutez la commande de la section précédente pendant une exploration, ``-Xmx1g`` apparaît sur la ligne qui précède ``org.codelibs.fess.exec.Crawler``.

Une JVM de robot d'exploration est lancée par tâche d'exploration.
La tâche « Default Crawler » traite toutes les configurations d'exploration dans un seul robot d'exploration.
Si vous créez une tâche par configuration avec [Créer une nouvelle tâche] sur la page de détails d'une configuration d'exploration, chacune est lancée comme un robot d'exploration distinct et utilise de la mémoire jusqu'à son ``-Xmx``.
Pour limiter le nombre de robots d'exploration exécutés simultanément, utilisez ``job.max.crawler.processes`` dans ``fess_config.properties`` (la valeur par défaut ``0`` signifie illimité).
Une tâche d'exploration lancée au-delà de cette limite n'attend pas son tour : elle se termine en erreur.

Pour les JVM de génération des suggestions et des vignettes, modifiez de la même manière la ligne ``-Xmx256m`` de ``jvm.suggest.options`` et ``jvm.thumbnail.options``.

Modifier le tas d'OpenSearch
----------------------------

Dans docker-fess, ``search01`` dans ``compose-opensearch3.yaml`` contient la ligne suivante.

::

    - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"

Remplacez ces deux valeurs par une même nouvelle valeur.
Pour un OpenSearch installé à partir d'un ZIP ou d'un RPM, modifiez ``-Xms`` et ``-Xmx`` dans ``config/jvm.options`` puis redémarrez-le.

En règle générale, la limite supérieure est d'au plus la moitié de la mémoire physique et de moins de 32GB.
La mémoire restante sert de cache de fichiers au système d'exploitation et contribue à la vitesse de recherche ; n'en attribuez donc pas trop au tas.
À partir de 32GB, les Compressed OOPs de la JVM sont désactivés et l'efficacité diminue même.
Si une telle taille ne suffit pas, ajoutez des nœuds.

Des repères sur la correspondance entre taille d'index et tas figurent dans `Configuration de la mémoire <https://fess.codelibs.org/fr/stable/config/setup-memory.html>`__.
Partez de ces repères, puis ajustez en observant l'utilisation du tas dans ``_cat/nodes`` mentionnée plus haut et les temps de réponse des recherches.

Si Fess et OpenSearch fonctionnent sur le même serveur, veillez à ce que la somme des tas du serveur Fess, du robot d'exploration et d'OpenSearch tienne dans la mémoire physique.

Modifier le parallélisme de l'exploration
-----------------------------------------

La vitesse d'exploration dépend des trois paramètres suivants.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Paramètre
     - Valeur par défaut
     - Emplacement
   * - Nombre de threads
     - Web 1, système de fichiers 5
     - Chaque configuration d'exploration ([Robot d'exploration] > [Web], [Système de fichiers])
   * - Intervalle
     - Web 10000 ms, système de fichiers 1000 ms
     - Idem. Temps d'attente de chaque thread après chaque récupération d'URL
   * - Configuration du robot d'exploration simultané
     - 5
     - [Système] > [Général]. Nombre de configurations d'exploration traitées simultanément par un robot d'exploration

Augmenter le nombre de threads accélère la récupération pour la configuration d'exploration concernée, mais augmente aussi l'utilisation mémoire du robot d'exploration et la charge des serveurs explorés.
Lorsque vous explorez des sites externes ou des serveurs utilisés en production, ne réduisez pas trop l'intervalle.

Sur un seul serveur, un paramètre est facile à négliger : ``adaptive.load.control`` dans ``fess_config.properties`` (valeur par défaut ``50``).
Tant que l'utilisation CPU du serveur qui exécute Fess est supérieure ou égale à cette valeur, les threads d'exploration et d'indexation attendent.
Si OpenSearch, sur le même serveur, utilise le CPU pour écrire dans l'index ou exécuter des recherches, l'exploration peut quasiment ne plus avancer.
Dans ce cas, ``fess-crawler.log`` affiche ``Cpu Load XX% is greater than 50%``.
Vous pouvez augmenter la valeur, mais si le CPU manque de façon chronique, la solution de fond consiste à déplacer OpenSearch sur un serveur distinct, comme décrit dans la section suivante.
Pour plus de détails, consultez `Configuration du contrôle de charge <https://fess.codelibs.org/fr/stable/config/load-control.html>`__.

Déplacer OpenSearch sur un serveur distinct
===========================================

En plaçant OpenSearch sur un serveur distinct, l'exploration et la recherche ne se disputent plus le CPU, la mémoire et les E/S disque.

Ce dont OpenSearch a besoin
---------------------------

L'OpenSearch utilisé par Fess a besoin des deux éléments suivants.

- Les quatre plugins pour Fess (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash``, ``opensearch-configsync``). Leur version doit correspondre à celle d'OpenSearch (Fess 15.9 utilise OpenSearch 3.9.0)
- ``configsync.config_path`` dans ``opensearch.yml``. Indiquez, sous forme de chemin absolu, un répertoire destiné aux fichiers de dictionnaire, situé sous le répertoire de configuration d'OpenSearch

Les commandes d'installation se trouvent dans `Installation sur Linux (Procédure détaillée) <https://fess.codelibs.org/fr/stable/install/install-linux.html>`__.
L'image ``ghcr.io/codelibs/fess-opensearch`` de docker-fess inclut tout cela dès le départ.

Lorsque OpenSearch est placé sur un serveur distinct, le port 9200 est exposé sur le réseau.
Ne l'utilisez pas en production avec le plugin de sécurité désactivé.
Pour la configuration, consultez :doc:`guide-15` et `Configuration de la sécurité <https://fess.codelibs.org/fr/stable/install/security.html>`__.

Ce qu'il faut configurer dans Fess
----------------------------------

Dans Fess, indiquez la destination de connexion et l'emplacement des dictionnaires à l'aide de deux variables d'environnement.

- ``SEARCH_ENGINE_HTTP_URL`` : l'URL d'OpenSearch
- ``FESS_DICTIONARY_PATH`` : le même chemin que ``configsync.config_path`` côté OpenSearch

``FESS_DICTIONARY_PATH`` est un chemin sur le serveur OpenSearch.
Fess écrit les fichiers de dictionnaire par l'intermédiaire du plugin ``configsync`` ; le serveur Fess n'a donc pas besoin de monter ce répertoire.
Si elle n'est pas définie, Fess ne peut pas créer ses index et ne démarre pas.

Ces variables se définissent dans ``/etc/sysconfig/fess`` pour le paquet RPM, dans ``/etc/default/fess`` pour le paquet DEB et dans ``bin/fess.in.sh`` pour le paquet ZIP.
Avec Docker, n'utilisez pas ``compose-opensearch3.yaml`` ; indiquez-les dans ``environment`` de ``fess01`` dans ``compose.yaml``.
Dans la v15.9.0, ``fess01`` dans ``compose.yaml`` possède un ``depends_on`` qui attend ``search01`` ; une configuration qui ne définit pas ``search01`` ne démarre donc pas et échoue avec l'erreur ``service "fess01" depends on undefined service "search01"``.
Supprimez les trois lignes allant de ``depends_on`` à ``condition: service_healthy``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://opensearch1.example.com:9200"
          - "FESS_DICTIONARY_PATH=/etc/opensearch/dictionary/"

Dans ce cas, exécutez toutes les commandes ``docker compose`` suivantes avec ``-f compose.yaml`` uniquement.

Avec le paquet ZIP, vous pouvez, avant de démarrer Fess, vérifier avec ``bin/fess-setup check`` la connexion, les quatre plugins et la réponse de ``configsync``.

::

    $ bin/fess-setup check --url http://opensearch1.example.com:9200

Changer la destination de connexion ne transfère pas les index existants vers le nouvel OpenSearch.
Pour conserver les documents existants, migrez-les à l'aide de snapshots (« Migration de données » dans `Gestion des index <https://fess.codelibs.org/fr/stable/config/admin-index-backup.html>`__).
S'il suffit d'explorer à nouveau, il est plus simple de se connecter à un OpenSearch vide et de relancer l'exploration.

Passer OpenSearch à un cluster de trois nœuds
=============================================

Tant qu'OpenSearch fonctionne sur un seul serveur, la recherche s'arrête dès que ce serveur s'arrête.
Lorsque la redondance devient nécessaire, passez OpenSearch en cluster.

Composition des nœuds
---------------------

L'élection du nœud chargé de gérer le cluster (cluster manager) requiert l'accord d'une majorité.
Avec un ou deux nœuds seulement pouvant devenir cluster manager, l'arrêt d'un seul nœud rend l'élection impossible.
Prévoyez donc trois nœuds pouvant devenir cluster manager.
La configuration minimale consiste à faire en sorte que les trois portent aussi des données.

Voici un exemple des paramètres liés au cluster dans ``opensearch.yml`` de chaque nœud (modifiez ``node.name`` pour chaque nœud).
Ajoutez les paramètres réseau comme ``network.host`` et les paramètres de sécurité selon votre environnement.

.. code-block:: yaml

    cluster.name: fess-search
    node.name: search01
    node.roles: [ cluster_manager, data, ingest ]
    discovery.seed_hosts: [ "search01", "search02", "search03" ]
    cluster.initial_cluster_manager_nodes: [ "search01", "search02", "search03" ]
    configsync.config_path: /etc/opensearch/dictionary/

Installez les quatre plugins pour Fess sur les trois nœuds, dans la même version.
Utilisez aussi le même chemin pour ``configsync.config_path`` sur les trois nœuds.
En effet, Fess n'écrit qu'une seule valeur de ``FESS_DICTIONARY_PATH`` dans les paramètres de l'index, et chaque nœud lit les dictionnaires à ce chemin.

``compose/snapshot/compose-cluster.yaml`` de docker-fess contient un exemple de construction de plusieurs nœuds avec Docker.
Ce fichier est conçu pour être combiné avec une version de développement de l'image Fess ; servez-vous-en comme référence pour l'écriture des variables d'environnement d'OpenSearch.

Connexion depuis Fess
---------------------

Dans ``SEARCH_ENGINE_HTTP_URL``, énumérez les URL des nœuds séparées par des virgules.
Même si certains nœuds sont arrêtés, Fess se connecte aux nœuds restants.

::

    SEARCH_ENGINE_HTTP_URL=http://search01:9200,http://search02:9200,http://search03:9200

Shards et répliques
-------------------

Fess crée l'index des documents avec ``index.number_of_shards`` de ``fess_config.properties`` (valeur par défaut ``5``, nombre de shards primaires) et ``index.auto_expand_replicas`` (valeur par défaut ``0-1``, qui ajuste automatiquement les répliques entre 0 et 1 selon le nombre de nœuds de données).
Avec la valeur par défaut ``0-1``, dès qu'il y a deux nœuds de données ou plus, une réplique est créée pour chaque shard sans modifier les paramètres de Fess.
Lorsque l'état du cluster passe à ``green``, toutes les répliques sont allouées.

Le nombre de shards est fixé à la création de l'index ; modifier ensuite ``index.number_of_shards`` n'a pas d'effet sur l'index existant.
Pour le changer, utilisez « Réindexation » dans [Informations système] > [Maintenance].
Si vous indiquez « Nombre de partitions » et « Développer automatiquement les répliques », activez « Remplacer les alias » puis démarrez, Fess crée un nouvel index, y copie les documents et déplace les alias ``fess.search`` et ``fess.update`` vers le nouvel index.

La réindexation appelle les remarques suivantes.

- Les documents sont copiés depuis l'index vers lequel pointe ``fess.update`` au moment du démarrage. Exécutez-la à un moment où aucune exploration ne tourne
- L'ancien index n'est pas supprimé automatiquement. Le disque doit pouvoir contenir à la fois l'ancien et le nouvel index

Pour les éléments de l'écran, consultez `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__.

Vérifier le cluster
-------------------

::

    $ curl -s 'http://search01:9200/_cat/nodes?v&h=name,node.role,cluster_manager,heap.percent'
    $ curl -s 'http://search01:9200/_cluster/health?pretty'

Si les trois nœuds s'affichent et que ``status`` vaut ``green``, le cluster est prêt.
Vous pouvez vérifier la même chose dans ``/api/admin/stats`` de Fess avec ``response.stats.engine.number_of_nodes`` et ``response.stats.engine.status``.

Exécuter plusieurs serveurs Fess
================================

Lorsque les utilisateurs de la recherche augmentent et que le serveur Fess manque de CPU, ou lorsque vous voulez rendre Fess lui-même redondant, connectez plusieurs serveurs Fess au même OpenSearch.
Notez que ``compose/multi-instance/`` de docker-fess est une configuration qui juxtapose des services de recherche indépendants, chaque Fess utilisant ses propres index ; elle diffère de la configuration décrite ici (pour séparer par organisation, consultez :doc:`guide-13`).

Les configurations d'exploration, les utilisateurs, les tâches et les journaux des tâches sont stockés dans OpenSearch ; ils sont donc identiques quel que soit le Fess consulté.
En revanche, les éléments suivants existent séparément sur chaque serveur Fess et doivent être harmonisés sur tous les serveurs.

- Les paramètres de [Système] > [Général] (``system.properties`` de chaque serveur). Les modifier dans l'écran de paramétrage ne change que la valeur de ce serveur
- ``fess_config.properties`` et les variables d'environnement comme ``FESS_HEAP_SIZE``
- Les plugins installés
- ``app.cipher.key`` dans ``fess_config.properties``. Parmi les paramètres des configurations d'exploration et des configurations de magasin de données, les valeurs dont le nom se termine par ``password``, ``key``, ``token``, ``secret``, etc. sont chiffrées avec cette clé et stockées dans OpenSearch. Si la clé diffère d'un serveur à l'autre, les valeurs enregistrées sur un autre serveur ne peuvent pas être déchiffrées

Choisir le serveur chargé de l'exploration
------------------------------------------

La « Cible » de toutes les tâches par défaut est ``all``.
``all`` correspond à tous les Fess ; en l'état, « Default Crawler » s'exécute donc sur tous les serveurs à la même heure.

Pour confier l'exploration à un seul serveur, effectuez les deux opérations suivantes.

1. Sur le serveur chargé de l'exploration uniquement, écrivez un identifiant dans ``fess_config.properties``, par exemple ``scheduler.target.name=crawler``, puis redémarrez. Avec Docker, vous pouvez indiquer ``-Dfess.config.scheduler.target.name=crawler`` dans ``FESS_JAVA_OPTS``. Laissez la valeur vide sur les autres serveurs
2. Dans [Système] > [Planificateur], ouvrez « Default Crawler », remplacez la « Cible » ``all`` par ``crawler`` et enregistrez. Modifiez de la même manière les tâches d'exploration créées avec [Créer une nouvelle tâche]

La « Cible » accepte plusieurs identifiants séparés par des virgules.
Avec l'étape 1 seule, les tâches continuent de s'exécuter sur tous les serveurs.
Avec l'étape 2 seule, aucun serveur ne possède d'identifiant correspondant, et l'exploration ne s'exécute nulle part.
Pour vérifier que l'étape 1 est prise en compte, consultez la valeur de ``scheduler.target.name`` dans « Propriétés de l'application » de [Informations système] > [Informations de configuration] sur le serveur chargé de l'exploration.

Pour les tâches autres que l'exploration (agrégation des journaux, suppression des anciens documents, etc.), laissez la « Cible » à ``all``.

Une fois l'exploration attribuée, cliquez aussi sur [Démarrer maintenant] depuis la console d'administration du serveur chargé de l'exploration.
Si vous cliquez sur un autre serveur, l'écran indique que la tâche a démarré, mais elle ne s'exécute pas sur ce serveur ; seul ``Ignoring job`` est enregistré dans ``fess.log``.
Si les serveurs se trouvent derrière un répartiteur de charge, prévoyez un chemin permettant d'atteindre directement le serveur chargé de l'exploration.

Configuration du répartiteur de charge
--------------------------------------

Dans Fess 15.9, les sessions de connexion sont stockées dans la mémoire de chaque Fess.
Si un répartiteur de charge distribue la page de recherche ou la console d'administration utilisées avec connexion, activez les sessions persistantes (sticky sessions) afin que le même utilisateur soit toujours dirigé vers le même serveur.
Le stockage des sessions dans OpenSearch pour les partager entre serveurs est disponible à partir de 15.10.

Pour le contrôle de santé du répartiteur de charge, vous pouvez utiliser ``/api/v2/health``.
Il renvoie 503 lorsque le cluster OpenSearch est ``RED`` et lorsqu'il ne peut pas se connecter à OpenSearch.

Exclusion mutuelle des opérations de maintenance
------------------------------------------------

« Réindexation », « Recharger l'index des documents », « Supprimer l'index du robot d'exploration » et « Reconstruire l'index de configuration » dans [Informations système] > [Maintenance] sont protégés par une exclusion mutuelle afin que plusieurs serveurs Fess ne les exécutent pas simultanément.
Si l'opération est déjà en cours sur un autre serveur, le message « L'opération est déjà en cours d'exécution sur <nom d'hôte>. » s'affiche.
Cette exclusion ne concerne que les opérations de maintenance ; elle ne coordonne pas les tâches ni les paramètres de [Général] entre les serveurs.

À propos des repères de dimensionnement
=======================================

Le nombre de documents ou d'utilisateurs ne suffit pas à déterminer la configuration nécessaire.
La mémoire et le CPU requis varient fortement selon la longueur du texte par document, la proportion de pièces jointes, la nature des termes recherchés et le fait que les utilisateurs se connectent ou non.

Décidez à partir de valeurs mesurées, comme suit.

- À partir du ``store.size`` de l'index, déterminez le tas d'OpenSearch à l'aide du tableau de repères de `Configuration de la mémoire <https://fess.codelibs.org/fr/stable/config/setup-memory.html>`__
- Si le p95 du journal de recherche se dégrade et que l'utilisation du tas ou le CPU dans ``_cat/nodes`` reste élevé, augmentez le tas d'OpenSearch ou ajoutez des nœuds
- Si la durée des explorations dans le journal des tâches s'allonge et que des messages ``Cpu Load`` apparaissent, déplacez OpenSearch sur un serveur distinct
- Si OpenSearch dispose de marge mais que le CPU du serveur Fess est élevé, exécutez plusieurs serveurs Fess

Pour aller plus loin
====================

- Exploiter Fess en production avec surveillance, journaux et sauvegardes : :doc:`guide-10`
- Protéger l'accès, y compris l'exposition d'OpenSearch et la connexion des utilisateurs : :doc:`guide-15`
- Gérer sous forme de code l'harmonisation des paramètres entre plusieurs serveurs : :doc:`guide-16`
- Utiliser un seul Fess de façon distincte pour chaque organisation : :doc:`guide-13`
- Organiser les points à vérifier à chaque étape du déploiement : :doc:`guide-23`

Références
==========

- `Configuration de la mémoire <https://fess.codelibs.org/fr/stable/config/setup-memory.html>`__
- `Configuration du port et du réseau <https://fess.codelibs.org/fr/stable/config/setup-port-network.html>`__
- `Configuration du contrôle de charge <https://fess.codelibs.org/fr/stable/config/load-control.html>`__
- `Installation sur Linux (Procédure détaillée) <https://fess.codelibs.org/fr/stable/install/install-linux.html>`__
- `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__
- `Commande fess-setup <https://fess.codelibs.org/fr/stable/install/fess-setup.html>`__
- `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__
- `Planificateur de tâches <https://fess.codelibs.org/fr/stable/admin/scheduler-guide.html>`__
- `Journal de recherche <https://fess.codelibs.org/fr/stable/admin/searchlog-guide.html>`__
- `API Stats <https://fess.codelibs.org/fr/stable/api/admin/api-admin-stats.html>`__
- `Gestion des index <https://fess.codelibs.org/fr/stable/config/admin-index-backup.html>`__
