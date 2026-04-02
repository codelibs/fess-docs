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

|Fess| prend en charge l'algorithme RRF (Reciprocal Rank Fusion).

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calcule les scores en additionnant l'inverse du rang de chaque resultat.

Formule ::

    score(d) = Σ 1 / (k + rank(d))

- ``k`` : Parametre constant (par defaut : 20)
- ``rank(d)`` : Rang du document d dans chaque resultat de recherche

Configuration
==============

fess_config.properties
----------------------

Configuration de base ::

    # Taille de la fenetre (nombre de resultats pour la fusion)
    rank.fusion.window_size=200

    # Constante de classement RRF (parametre k)
    rank.fusion.rank_constant=20

    # Nombre de threads pour le traitement parallele (-1 par defaut)
    rank.fusion.threads=-1

    # Nom du champ de score
    rank.fusion.score_field=rf_score

Integration avec la recherche hybride
=======================================

Le Rank Fusion est particulierement efficace dans la recherche hybride combinant
la recherche par mots-cles et la recherche semantique.

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

Considerations de performance
================================

- L'utilisation memoire augmente car plusieurs resultats de recherche sont conserves
- Le temps de reponse augmente car plusieurs recherches sont executees

Depannage
==========

Les resultats de recherche different des attentes
---------------------------------------------------

**Symptome** : Les resultats apres Rank Fusion different des attentes

**Verifications** :

1. Verifier les resultats de chaque type de recherche individuellement
2. Ajuster la valeur de ``rank.fusion.rank_constant``
3. Ajuster la valeur de ``rank.fusion.window_size``

La recherche est lente
-----------------------

**Symptome** : La recherche devient lente lorsque le Rank Fusion est active

**Solutions** :

1. Reduire ``rank.fusion.window_size`` ::

       rank.fusion.window_size=100

2. Ajuster ``rank.fusion.threads`` ::

       rank.fusion.threads=4

Memoire insuffisante
---------------------

**Symptome** : Une erreur OutOfMemoryError se produit

**Solutions** :

1. Reduire ``rank.fusion.window_size``
2. Augmenter la taille du tas JVM

Reference
==========

- :doc:`scripting-overview` - Apercu du scripting
- :doc:`search-advanced` - Configuration avancée de la recherche
- :doc:`llm-overview` - Guide d'integration LLM (Recherche semantique)
