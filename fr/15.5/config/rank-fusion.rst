==================================
Configuration du Rank Fusion
==================================

Apercu
======

La fonctionnalite Rank Fusion de |Fess| integre plusieurs resultats de recherche
pour fournir des resultats de recherche plus precis.

Qu'est-ce que le Rank Fusion
==============================

Le Rank Fusion est une technique qui combine les resultats de plusieurs algorithmes
de recherche ou methodes de notation pour generer un classement unique optimise.

Principaux avantages :

- Combine les forces de differents algorithmes
- Ameliore la precision de la recherche
- Fournit des resultats de recherche diversifies

Algorithmes pris en charge
===========================

|Fess| prend en charge les algorithmes de Rank Fusion suivants :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Algorithme
     - Description
   * - RRF (Reciprocal Rank Fusion)
     - Algorithme de fusion utilisant l'inverse du rang
   * - Score Fusion
     - Fusion par normalisation des scores et moyenne ponderee
   * - Borda Count
     - Fusion de classement basee sur le vote

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calcule les scores en additionnant l'inverse du rang de chaque resultat.

Formule ::

    score(d) = Σ 1 / (k + rank(d))

- ``k`` : Parametre constant (par defaut : 60)
- ``rank(d)`` : Rang du document d dans chaque resultat de recherche

Configuration
==============

fess_config.properties
----------------------

Configuration de base ::

    # Activer le Rank Fusion
    rank.fusion.enabled=true

    # Algorithme a utiliser
    rank.fusion.algorithm=rrf

    # Parametre k de RRF
    rank.fusion.rrf.k=60

    # Types de recherche pour la fusion
    rank.fusion.search.types=keyword,semantic

Configuration par algorithme
-----------------------------

Configuration RRF ::

    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

Configuration Score Fusion ::

    rank.fusion.algorithm=score
    rank.fusion.score.normalize=true
    rank.fusion.score.weights=0.7,0.3

Configuration Borda Count ::

    rank.fusion.algorithm=borda
    rank.fusion.borda.top_n=100

Integration avec la recherche hybride
=======================================

Le Rank Fusion est particulierement efficace dans la recherche hybride combinant
la recherche par mots-cles et la recherche semantique.

Exemple de configuration
--------------------------

::

    # Activer la recherche hybride
    search.hybrid.enabled=true

    # Fusionner les resultats de recherche par mots-cles et semantique
    rank.fusion.enabled=true
    rank.fusion.algorithm=rrf
    rank.fusion.rrf.k=60

    # Poids pour chaque type de recherche
    search.hybrid.keyword.weight=0.6
    search.hybrid.semantic.weight=0.4

Exemples d'utilisation
=======================

Recherche hybride de base
---------------------------

1. Calculer le score BM25 avec la recherche par mots-cles
2. Calculer la similarite vectorielle avec la recherche semantique
3. Fusionner les deux resultats avec RRF
4. Generer le classement final

Flux de recherche ::

    User Query
        ↓
    ┌──────────────────┬──────────────────┐
    │  Keyword Search  │ Semantic Search  │
    │    (BM25)        │  (Vector)        │
    └────────┬─────────┴────────┬─────────┘
             ↓                  ↓
         Rank List 1        Rank List 2
             └────────┬─────────┘
                      ↓
              Rank Fusion (RRF)
                      ↓
              Final Ranking

Notation personnalisee
-----------------------

Exemple de combinaison de plusieurs facteurs de notation ::

    # Score de recherche de base + Boost par date + Popularite
    rank.fusion.enabled=true
    rank.fusion.algorithm=score
    rank.fusion.score.factors=relevance,recency,popularity
    rank.fusion.score.weights=0.5,0.3,0.2

Considerations de performance
================================

Utilisation memoire
--------------------

- L'utilisation memoire augmente car plusieurs resultats de recherche sont conserves
- Limitez le nombre maximum de cibles de fusion avec ``rank.fusion.max.results``

::

    # Nombre maximum de resultats pour la fusion
    rank.fusion.max.results=1000

Temps de traitement
--------------------

- Le temps de reponse augmente car plusieurs recherches sont executees
- Envisagez l'optimisation par execution parallele

::

    # Activer l'execution parallele
    rank.fusion.parallel=true
    rank.fusion.thread.pool.size=4

Cache
------

- Utilisez le cache pour les requetes frequentes

::

    # Cache pour les resultats de Rank Fusion
    rank.fusion.cache.enabled=true
    rank.fusion.cache.size=1000
    rank.fusion.cache.expire=300

Depannage
==========

Les resultats de recherche different des attentes
---------------------------------------------------

**Symptome** : Les resultats apres Rank Fusion different des attentes

**Verifications** :

1. Verifier les resultats de chaque type de recherche individuellement
2. Verifier que la ponderation est appropriee
3. Ajuster la valeur du parametre k

La recherche est lente
-----------------------

**Symptome** : La recherche devient lente lorsque le Rank Fusion est active

**Solutions** :

1. Activer l'execution parallele ::

       rank.fusion.parallel=true

2. Limiter le nombre de resultats cibles de fusion ::

       rank.fusion.max.results=500

3. Activer le cache ::

       rank.fusion.cache.enabled=true

Memoire insuffisante
---------------------

**Symptome** : Une erreur OutOfMemoryError se produit

**Solutions** :

1. Reduire le nombre maximum de resultats cibles de fusion
2. Augmenter la taille du tas JVM
3. Desactiver les types de recherche inutiles

Reference
==========

- :doc:`scripting-overview` - Apercu du scripting
- :doc:`../admin/search-settings` - Guide de configuration de la recherche
- :doc:`llm-overview` - Guide d'integration LLM (Recherche semantique)
