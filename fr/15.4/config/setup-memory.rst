==================
Configuration de la mémoire
==================

Vue d'ensemble
====

Pour les applications Java, il est nécessaire de configurer la mémoire heap maximale utilisée par chaque processus.
Dans |Fess|, les paramètres de mémoire sont configurés pour les trois composants suivants.

- Application web Fess
- Processus de crawl
- OpenSearch

Une configuration mémoire appropriée permet d'améliorer les performances et d'assurer un fonctionnement stable.

Configuration de la mémoire de l'application web Fess
======================================

Quand configurer
----------------

Envisagez d'ajuster la taille de la mémoire dans les cas suivants.

- Les erreurs OutOfMemory sont enregistrées dans ``fess.log``
- Vous devez traiter un grand nombre d'accès simultanés
- Les opérations de l'interface d'administration sont lentes ou expirent

La taille de mémoire par défaut est suffisante pour une utilisation générale, mais une augmentation est nécessaire dans les environnements à forte charge.

Configuration par variable d'environnement
------------------

Définissez la variable d'environnement ``FESS_HEAP_SIZE``.

::

    export FESS_HEAP_SIZE=2g

Unités :

- ``m`` : mégaoctets
- ``g`` : gigaoctets

Pour les packages RPM/DEB
------------------------

Si vous avez installé avec le package RPM, éditez ``/etc/sysconfig/fess``.

::

    FESS_HEAP_SIZE=2g

Pour le package DEB, éditez ``/etc/default/fess``.

::

    FESS_HEAP_SIZE=2g

.. warning::
   Après avoir modifié la taille de la mémoire, vous devez redémarrer le service |Fess|.

Tailles de mémoire recommandées
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Environnement
     - Taille heap recommandée
     - Remarques
   * - Environnement de développement/test
     - 512m〜1g
     - Index de petite taille
   * - Environnement de production à petite échelle
     - 1g〜2g
     - Dizaines à centaines de milliers de documents
   * - Environnement de production à moyenne échelle
     - 2g〜4g
     - Centaines de milliers à millions de documents
   * - Environnement de production à grande échelle
     - 4g〜8g
     - Plusieurs millions de documents et plus

Configuration de la mémoire du crawler
======================

Quand configurer
----------------

Vous devez augmenter la taille de mémoire du crawler dans les cas suivants.

- Lorsque vous augmentez le nombre de crawls parallèles
- Lors du crawl de fichiers volumineux
- Lorsque des erreurs OutOfMemory se produisent pendant l'exécution du crawl

Méthode de configuration
--------

Éditez ``app/WEB-INF/classes/fess_config.properties`` ou ``/etc/fess/fess_config.properties``.

::

    jvm.crawler.options=-Xmx512m

Par exemple, pour passer à 1 Go :

::

    jvm.crawler.options=-Xmx1g

.. note::
   Ce paramètre est appliqué par processus de crawl (par tâche du planificateur).
   Si vous exécutez plusieurs tâches de crawl simultanément, chaque tâche utilisera la mémoire spécifiée.

Paramètres recommandés
--------

- **Crawl web normal** : 512m〜1g
- **Crawl parallèle intensif** : 1g〜2g
- **Crawl de fichiers volumineux** : 2g〜4g

Options JVM détaillées
------------------

Les options JVM détaillées pour le crawler peuvent être configurées avec ``jvm.crawler.options``.
Les paramètres par défaut incluent les optimisations suivantes.

**Options principales :**

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Option
     - Description
   * - ``-Xms128m -Xmx512m``
     - Taille heap initiale et maximale
   * - ``-XX:MaxMetaspaceSize=128m``
     - Taille maximale du Metaspace
   * - ``-XX:+UseG1GC``
     - Utilisation du collecteur de déchets G1
   * - ``-XX:MaxGCPauseMillis=60000``
     - Temps d'arrêt GC cible (60 secondes)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Désactivation du dump heap lors d'OutOfMemory

Configuration de la mémoire OpenSearch
=======================

Considérations importantes
--------------

Pour OpenSearch, vous devez configurer la mémoire en tenant compte des deux points suivants.

1. **Mémoire heap Java** : Utilisée par le processus OpenSearch
2. **Cache du système de fichiers OS** : Important pour les performances de recherche

.. warning::
   Si vous augmentez trop la mémoire heap Java, la mémoire disponible pour
   le cache du système de fichiers OS diminue, ce qui peut dégrader les performances de recherche.

Méthode de configuration
--------

Environnement Linux
~~~~~~~~~

La mémoire heap OpenSearch est spécifiée via une variable d'environnement ou le fichier de configuration OpenSearch.

Configuration par variable d'environnement :

::

    export OPENSEARCH_HEAP_SIZE=2g

Ou éditez ``config/jvm.options`` :

::

    -Xms2g
    -Xmx2g

.. note::
   Il est recommandé de définir la taille heap minimale (``-Xms``) et maximale (``-Xmx``) à la même valeur.

Environnement Windows
~~~~~~~~~~~

Éditez le fichier ``config\jvm.options``.

::

    -Xms2g
    -Xmx2g

Tailles de mémoire recommandées
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Taille de l'index
     - Taille heap recommandée
     - Mémoire totale recommandée
   * - 〜10GB
     - 2g
     - 4 Go ou plus
   * - 10GB〜50GB
     - 4g
     - 8 Go ou plus
   * - 50GB〜100GB
     - 8g
     - 16 Go ou plus
   * - 100 Go et plus
     - 16g〜31g
     - 32 Go ou plus

.. warning::
   Ne configurez pas la mémoire heap OpenSearch au-delà de 32 Go.
   Au-delà de 32 Go, Compressed OOP est désactivé, ce qui réduit l'efficacité de la mémoire.

Bonnes pratiques
------------------

1. **Allouer 50% de la mémoire physique au heap**

   Allouez environ 50% de la mémoire physique du serveur au heap OpenSearch.
   Le reste est utilisé pour l'OS et le cache du système de fichiers.

2. **Maximum 31 Go**

   La taille heap doit être limitée à 31 Go maximum. Si vous avez besoin de plus, augmentez le nombre de nœuds.

3. **Vérification en production**

   Consultez la documentation officielle OpenSearch pour optimiser la configuration selon votre environnement.

Configuration de la mémoire pour les processus de suggestion et de miniature
======================================

Processus de génération de suggestions
----------------------

Les paramètres de mémoire pour le processus de génération de suggestions sont configurés avec ``jvm.suggest.options``.

::

    jvm.suggest.options=-Xmx256m

Par défaut, les paramètres suivants sont utilisés :

- Heap initial : 128 Mo
- Heap maximal : 256 Mo
- Metaspace maximal : 128 Mo

Processus de génération de miniatures
----------------------

Les paramètres de mémoire pour le processus de génération de miniatures sont configurés avec ``jvm.thumbnail.options``.

::

    jvm.thumbnail.options=-Xmx256m

Par défaut, les paramètres suivants sont utilisés :

- Heap initial : 128 Mo
- Heap maximal : 256 Mo
- Metaspace maximal : 128 Mo

.. note::
   Si vous traitez de grandes images lors de la génération de miniatures, vous devrez augmenter la mémoire.

Surveillance et optimisation de la mémoire
========================

Vérification de l'utilisation de la mémoire
--------------------

Utilisation de la mémoire Fess
~~~~~~~~~~~~~~~~~~~~~

Vous pouvez vérifier dans « Informations système » de l'interface d'administration.

Ou utilisez les outils de surveillance JVM :

::

    jps -l  # Vérifier le processus Fess
    jstat -gcutil <PID> 1000  # Afficher les statistiques GC toutes les secondes

Utilisation de la mémoire OpenSearch
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X GET "localhost:9201/_nodes/stats/jvm?pretty"
    curl -X GET "localhost:9201/_cat/nodes?v&h=heap.percent,ram.percent"

Signes de manque de mémoire
----------------

Si les symptômes suivants apparaissent, il peut y avoir un manque de mémoire.

**Application web Fess :**

- Réponses lentes
- ``OutOfMemoryError`` enregistré dans les journaux
- Arrêt inattendu du processus

**Crawler :**

- Le crawl s'arrête en cours d'exécution
- ``OutOfMemoryError`` enregistré dans ``fess_crawler.log``
- Échec du crawl de fichiers volumineux

**OpenSearch :**

- Recherche lente
- Création d'index lente
- Erreurs ``circuit_breaker_exception``

Procédure d'optimisation
----------------

1. **Vérifier l'utilisation actuelle de la mémoire**

   Surveillez l'utilisation de la mémoire de chaque composant.

2. **Identifier les goulots d'étranglement**

   Identifiez quel composant manque de mémoire.

3. **Augmenter progressivement**

   N'augmentez pas de manière excessive en une fois, augmentez de 25-50% et vérifiez l'effet.

4. **Considérer l'équilibre global du système**

   Assurez-vous que la mémoire totale de tous les composants ne dépasse pas la mémoire physique.

5. **Surveillance continue**

   Surveillez en continu l'utilisation de la mémoire et ajustez si nécessaire.

Prévention des fuites mémoire
----------------

En cas de suspicion de fuite mémoire :

1. **Obtenir un dump heap**

::

    jmap -dump:format=b,file=heap.bin <PID>

2. **Analyser le dump heap**

   Analysez avec des outils comme Eclipse Memory Analyzer (MAT).

3. **Signaler le problème**

   Si vous découvrez une fuite mémoire, signalez-la sur GitHub Issues.

Dépannage
======================

OutOfMemoryError se produit
---------------------------

**Application web Fess :**

1. Augmentez ``FESS_HEAP_SIZE``.
2. Limitez le nombre d'accès simultanés.
3. Réduisez le niveau de journalisation pour diminuer l'utilisation de la mémoire par les journaux.

**Crawler :**

1. Augmentez ``-Xmx`` dans ``jvm.crawler.options``.
2. Réduisez le nombre de crawls parallèles.
3. Ajustez la configuration du crawl pour exclure les fichiers volumineux.

**OpenSearch :**

1. Augmentez la taille heap (jusqu'à 31 Go maximum).
2. Revoyez le nombre de shards de l'index.
3. Vérifiez la complexité des requêtes.

Temps d'arrêt GC prolongé
----------------------

1. Ajustez les paramètres G1GC.
2. Configurez correctement la taille heap (un GC fréquent se produit si elle est trop grande ou trop petite).
3. Envisagez de mettre à jour vers une version Java plus récente.

Les performances ne s'améliorent pas après la configuration de la mémoire
------------------------------

1. Vérifiez d'autres ressources comme le CPU, les E/S disque et le réseau.
2. Optimisez l'index.
3. Revoyez les paramètres de requête et de crawl.

Informations de référence
========

- :doc:`setup-port-network` - Configuration du port et du réseau
- :doc:`crawler-advanced` - Configuration avancée du crawler
- :doc:`admin-logging` - Configuration des journaux
- `OpenSearch Memory Settings <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/index/#important-settings>`_
- `Java GC Tuning <https://docs.oracle.com/en/java/javase/11/gctuning/>`_
