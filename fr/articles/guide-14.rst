============================================================
Partie 14 : Strategies de mise a l'echelle des systemes de recherche -- Extension progressive de la petite a la grande echelle
============================================================

Introduction
=============

Lorsque vous deployez Fess a petite echelle, l'augmentation de l'utilisation engendre inevitablement des demandes telles que "plus de documents", "plus d'utilisateurs" et "des recherches plus rapides".

Cet article explique les strategies et les criteres de decision pour passer progressivement d'une configuration a serveur unique a petite echelle a une configuration en cluster a grande echelle.

Public cible
=============

- Personnes planifiant l'exploitation de Fess a grande echelle
- Personnes confrontees a des problemes de performances
- Personnes souhaitant comprendre les concepts de base des clusters OpenSearch

Etapes de mise a l'echelle
===========================

La mise a l'echelle de Fess se fait generalement selon les etapes suivantes.

.. list-table:: Etapes de mise a l'echelle
   :header-rows: 1
   :widths: 15 20 25 20 20

   * - Etape
     - Configuration
     - Nombre de documents (env.)
     - Nombre d'utilisateurs (env.)
     - Cout
   * - S
     - Serveur unique
     - Jusqu'a 1 million
     - Jusqu'a 50
     - Faible
   * - M
     - Configuration separee
     - Jusqu'a 1 million
     - Jusqu'a 500
     - Moyen
   * - L
     - Configuration en cluster
     - 1 million a 10 millions
     - Jusqu'a plusieurs milliers
     - Eleve
   * - XL
     - Multi-instances
     - 10 millions ou plus
     - Plusieurs milliers ou plus
     - Le plus eleve

Etape S : Configuration a serveur unique
==========================================

Cela correspond a la configuration Docker Compose construite dans la Partie 2.
Fess et OpenSearch fonctionnent sur le meme serveur.

Cas d'utilisation
------------------

- Deploiement initial, PoC, organisations de petite a moyenne taille
- Nombre de documents de 1 million ou moins
- Peu d'utilisateurs effectuant des recherches simultanees

Points d'optimisation
----------------------

**Ajustement du tas JVM**

Configurez la taille du tas JVM de maniere appropriee pour Fess et OpenSearch respectivement.

- Fess : Maximum 2 Go (par defaut ; le tas initial est de 256 Mo)
- OpenSearch : 50 % ou moins de la memoire physique, mais pas plus de 32 Go

**Pool de threads**

Ajustez le nombre de threads de collecte en fonction du nombre de coeurs CPU du serveur.

Etape M : Configuration separee
=================================

Separez physiquement le serveur Fess et le serveur OpenSearch.

Cas d'utilisation
------------------

- Lorsque le nombre d'utilisateurs effectuant des recherches simultanees augmente et que les performances de recherche pendant la collecte deviennent problematiques
- Lorsque la memoire ou le CPU deviennent insuffisants a l'etape S

Configuration
--------------

::

    [Serveur Fess] <-> [Serveur OpenSearch]

Modifiez la destination de connexion OpenSearch dans les parametres de Fess vers le serveur externe.

Avantages
----------

- Elimination des conflits de ressources entre Fess (traitement de collecte) et OpenSearch (traitement de recherche)
- Attribution optimale des ressources (CPU, memoire) pour chaque serveur possible
- Les E/S disque du serveur OpenSearch deviennent independantes

Etape L : Configuration en cluster
====================================

Configurez OpenSearch en cluster pour ameliorer la redondance et les performances de recherche.

Cas d'utilisation
------------------

- Nombre de documents de 1 million a 10 millions
- Lorsque la haute disponibilite est requise
- Lorsque l'amelioration du temps de reponse de recherche est necessaire

Exemple de configuration
--------------------------

::

    [Serveur Fess]
          |
    [Noeud OpenSearch 1] (Maitre/Donnees)
    [Noeud OpenSearch 2] (Donnees)
    [Noeud OpenSearch 3] (Donnees)

Le cluster OpenSearch distribue et replique les donnees en utilisant les concepts de shards et de replicas.

**Shards** : Division de l'index et distribution sur plusieurs noeuds (traitement plus rapide par parallelisation)

**Replicas** : Conservation de copies des shards sur d'autres noeuds (redondance en cas de panne + parallelisation de la recherche)

Points de configuration
-------------------------

- Nombre de shards : A definir en fonction du nombre de documents et des performances de recherche (reference : 10-50 Go par shard)
- Nombre de replicas : Au moins 1 (pour assurer la redondance)
- Nombre de noeuds : Au moins 3 (quorum pour l'election du maitre)

Etape XL : Configuration multi-instances
==========================================

Configurez plusieurs instances Fess pour distribuer le traitement de collecte et de recherche.

Cas d'utilisation
------------------

- Le nombre de documents depasse 10 millions
- Necessite d'executer des taches de collecte massives en parallele
- Requetes de recherche a haute frequence

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

A partir de Fess 15.6, la fonctionnalite de coordinateur distribue permet le controle exclusif des operations de maintenance (telles que la reconstruction et le vidage de l'index) entre plusieurs instances Fess.

Organigramme de decision pour la mise a l'echelle
===================================================

Lorsque des problemes de performances surviennent, identifiez la cause et envisagez des mesures correctives dans l'ordre suivant.

**1. Lorsque la recherche est lente**

- Verifiez l'etat du cluster OpenSearch
- Verifiez l'utilisation du tas JVM
- Verifiez la taille de l'index
- -> Envisagez l'etape M (separation) ou l'etape L (mise en cluster)

**2. Lorsque la collecte est lente ou ne se termine pas**

- Verifiez le nombre de documents a collecter
- Ajustez le nombre de threads et l'intervalle
- Verifiez l'impact sur la recherche pendant la collecte
- -> Envisagez l'etape M (separation) ou l'etape XL (instance dediee a la collecte)

**3. Lorsqu'il y a de nombreux acces simultanees**

- Surveillez le temps de reponse de recherche
- Verifiez l'utilisation du CPU du serveur Fess
- -> Envisagez l'etape XL (repartiteur de charge + plusieurs instances)

Optimisation de la JVM
========================

A chaque etape, l'optimisation de la JVM a un impact significatif sur les performances.

Parametres principaux
----------------------

.. list-table:: Parametres JVM
   :header-rows: 1
   :widths: 25 35 40

   * - Parametre
     - Description
     - Valeur recommandee
   * - ``-Xmx``
     - Taille maximale du tas
     - 50 % ou moins de la memoire physique
   * - ``-Xms``
     - Taille initiale du tas
     - Meme valeur que ``-Xmx``
   * - Parametres GC
     - Methode de ramasse-miettes
     - G1GC (par defaut)

Reference pour la taille du tas
---------------------------------

- 1 million ou moins : 2-4 Go
- 1 million a 5 millions : 8 Go
- 5 millions a 10 millions : 16 Go
- 10 millions ou plus : 32 Go ou plus (cote OpenSearch)

Resume
=======

Cet article a presente les strategies de mise a l'echelle progressive de Fess.

- **Etape S** : Serveur unique (jusqu'a 1 million de documents)
- **Etape M** : Separation Fess / OpenSearch (jusqu'a 1 million de documents, prise en charge multi-utilisateurs)
- **Etape L** : Mise en cluster OpenSearch (1 million a 10 millions de documents)
- **Etape XL** : Multi-instances Fess (10 millions de documents ou plus)
- Organigramme de decision pour la mise a l'echelle et optimisation de la JVM

Avec l'approche "commencer petit et grandir selon les besoins", il est possible de mettre a l'echelle en fonction des exigences tout en maitrisant les couts.

Le prochain article traitera de l'architecture de securite.

References
===========

- `Guide d'installation de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__

- `Configuration des clusters OpenSearch <https://opensearch.org/docs/latest/tuning-your-cluster/>`__
