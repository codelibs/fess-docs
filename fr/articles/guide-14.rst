====================================================================
Partie 14 : Stratégies de mise à l'échelle des systèmes de recherche
====================================================================

Introduction
=============

Lorsque vous déployez Fess à petite échelle, l'augmentation de l'utilisation engendre inévitablement des demandes telles que "plus de documents", "plus d'utilisateurs" et "des recherches plus rapides".

Cet article explique les stratégies et les critères de décision pour passer progressivement d'une configuration à serveur unique à petite échelle à une configuration en cluster à grande échelle.

Public cible
=============

- Personnes planifiant l'exploitation de Fess à grande échelle
- Personnes confrontées à des problèmes de performances
- Personnes souhaitant comprendre les concepts de base des clusters OpenSearch

Étapes de mise à l'échelle
===========================

La mise à l'échelle de Fess se fait généralement selon les étapes suivantes.

.. list-table:: Étapes de mise à l'échelle
   :header-rows: 1
   :widths: 15 20 25 20 20

   * - Étape
     - Configuration
     - Nombre de documents (env.)
     - Nombre d'utilisateurs (env.)
     - Coût
   * - S
     - Serveur unique
     - Jusqu'à 1 million
     - Jusqu'à 50
     - Faible
   * - M
     - Configuration séparée
     - Jusqu'à 1 million
     - Jusqu'à 500
     - Moyen
   * - L
     - Configuration en cluster
     - 1 million à 10 millions
     - Jusqu'à plusieurs milliers
     - Élevé
   * - XL
     - Multi-instances
     - 10 millions ou plus
     - Plusieurs milliers ou plus
     - Le plus élevé

Étape S : Configuration à serveur unique
==========================================

Cela correspond à la configuration Docker Compose construite dans la Partie 2.
Fess et OpenSearch fonctionnent sur le même serveur.

Cas d'utilisation
------------------

- Déploiement initial, PoC, organisations de petite à moyenne taille
- Nombre de documents de 1 million ou moins
- Peu d'utilisateurs effectuant des recherches simultanées

Points d'optimisation
----------------------

**Ajustement du tas JVM**

Configurez la taille du tas JVM de manière appropriée pour Fess et OpenSearch respectivement.

- Fess : Maximum 2 Go (par défaut ; le tas initial est de 256 Mo)
- OpenSearch : 50 % ou moins de la mémoire physique, mais pas plus de 32 Go

**Pool de threads**

Ajustez le nombre de threads de collecte en fonction du nombre de cœurs CPU du serveur.

Étape M : Configuration séparée
=================================

Séparez physiquement le serveur Fess et le serveur OpenSearch.

Cas d'utilisation
------------------

- Lorsque le nombre d'utilisateurs effectuant des recherches simultanées augmente et que les performances de recherche pendant la collecte deviennent problématiques
- Lorsque la mémoire ou le CPU deviennent insuffisants à l'étape S

Configuration
--------------

::

    [Serveur Fess] <-> [Serveur OpenSearch]

Modifiez la destination de connexion OpenSearch dans les paramètres de Fess vers le serveur externe.

Avantages
----------

- Élimination des conflits de ressources entre Fess (traitement de collecte) et OpenSearch (traitement de recherche)
- Attribution optimale des ressources (CPU, mémoire) pour chaque serveur possible
- Les E/S disque du serveur OpenSearch deviennent indépendantes

Étape L : Configuration en cluster
====================================

Configurez OpenSearch en cluster pour améliorer la redondance et les performances de recherche.

Cas d'utilisation
------------------

- Nombre de documents de 1 million à 10 millions
- Lorsque la haute disponibilité est requise
- Lorsque l'amélioration du temps de réponse de recherche est nécessaire

Exemple de configuration
--------------------------

::

    [Serveur Fess]
          |
    [Noeud OpenSearch 1] (Maitre/Donnees)
    [Noeud OpenSearch 2] (Donnees)
    [Noeud OpenSearch 3] (Donnees)

Le cluster OpenSearch distribue et réplique les données en utilisant les concepts de shards et de replicas.

**Shards** : Division de l'index et distribution sur plusieurs nœuds (traitement plus rapide par parallélisation)

**Replicas** : Conservation de copies des shards sur d'autres nœuds (redondance en cas de panne + parallélisation de la recherche)

Points de configuration
-------------------------

- Nombre de shards : À définir en fonction du nombre de documents et des performances de recherche (référence : 10-50 Go par shard)
- Nombre de replicas : Au moins 1 (pour assurer la redondance)
- Nombre de nœuds : Au moins 3 (quorum pour l'élection du maître)

Étape XL : Configuration multi-instances
==========================================

Configurez plusieurs instances Fess pour distribuer le traitement de collecte et de recherche.

Cas d'utilisation
------------------

- Le nombre de documents dépasse 10 millions
- Nécessite d'exécuter des tâches de collecte massives en parallèle
- Requêtes de recherche à haute fréquence

Exemple de configuration
--------------------------

::

    [Repartiteur de charge]
      +-- [Instance Fess 1] (Recherche + Administration)
      +-- [Instance Fess 2] (Recherche)
      +-- [Instance Fess 3] (Collecte uniquement)
              |
    [Cluster OpenSearch]
      +-- [Noeud 1] (Maitre)
      +-- [Noeud 2] (Donnees)
      +-- [Noeud 3] (Donnees)
      +-- [Noeud 4] (Donnees)

À partir de Fess 15.6, la fonctionnalité de coordinateur distribué permet le contrôle exclusif des opérations de maintenance (telles que la reconstruction et le vidage de l'index) entre plusieurs instances Fess.

Organigramme de décision pour la mise à l'échelle
===================================================

Lorsque des problèmes de performances surviennent, identifiez la cause et envisagez des mesures correctives dans l'ordre suivant.

**1. Lorsque la recherche est lente**

- Vérifiez l'état du cluster OpenSearch
- Vérifiez l'utilisation du tas JVM
- Vérifiez la taille de l'index
- -> Envisagez l'étape M (séparation) ou l'étape L (mise en cluster)

**2. Lorsque la collecte est lente ou ne se termine pas**

- Vérifiez le nombre de documents à collecter
- Ajustez le nombre de threads et l'intervalle
- Vérifiez l'impact sur la recherche pendant la collecte
- -> Envisagez l'étape M (séparation) ou l'étape XL (instance dédiée à la collecte)

**3. Lorsqu'il y a de nombreux accès simultanés**

- Surveillez le temps de réponse de recherche
- Vérifiez l'utilisation du CPU du serveur Fess
- -> Envisagez l'étape XL (répartiteur de charge + plusieurs instances)

Optimisation de la JVM
========================

À chaque étape, l'optimisation de la JVM a un impact significatif sur les performances.

Paramètres principaux
----------------------

.. list-table:: Paramètres JVM
   :header-rows: 1
   :widths: 25 35 40

   * - Paramètre
     - Description
     - Valeur recommandée
   * - ``-Xmx``
     - Taille maximale du tas
     - 50 % ou moins de la mémoire physique
   * - ``-Xms``
     - Taille initiale du tas
     - Même valeur que ``-Xmx``
   * - Paramètres GC
     - Méthode de ramasse-miettes
     - G1GC (par défaut)

Référence pour la taille du tas
---------------------------------

- 1 million ou moins : 2-4 Go
- 1 million à 5 millions : 8 Go
- 5 millions à 10 millions : 16 Go
- 10 millions ou plus : 32 Go ou plus (côté OpenSearch)

Résumé
=======

Cet article a présenté les stratégies de mise à l'échelle progressive de Fess.

- **Étape S** : Serveur unique (jusqu'à 1 million de documents)
- **Étape M** : Séparation Fess / OpenSearch (jusqu'à 1 million de documents, prise en charge multi-utilisateurs)
- **Étape L** : Mise en cluster OpenSearch (1 million à 10 millions de documents)
- **Étape XL** : Multi-instances Fess (10 millions de documents ou plus)
- Organigramme de décision pour la mise à l'échelle et optimisation de la JVM

Avec l'approche "commencer petit et grandir selon les besoins", il est possible de mettre à l'échelle en fonction des exigences tout en maîtrisant les coûts.

Le prochain article traitera de l'architecture de sécurité.

Références
===========

- `Guide d'installation de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `Configuration des clusters OpenSearch <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
