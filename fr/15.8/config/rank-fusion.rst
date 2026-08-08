=============================================================
Recherche hybride et Rank Fusion (sémantique + mots-clés)
=============================================================

Aperçu
======

La **recherche hybride** dans |Fess| combine la recherche traditionnelle par mots-clés (BM25) avec la **recherche sémantique (vectorielle)**, puis fusionne les deux ensembles de résultats grâce au **Rank Fusion** afin de produire des classements plus précis et plus pertinents. Le Rank Fusion intègre les résultats de plusieurs moteurs de recherche en un classement unique optimisé.

Dans |Fess| 15.8, la recherche sémantique (chunking de contenu + recherche vectorielle) est
fournie comme une fonctionnalité du cœur. Une fois activée, le moteur de recherche sémantique est
enregistré automatiquement auprès du Rank Fusion. Voir :doc:`search-semantic` pour sa
configuration.

La fonctionnalité Rank Fusion de |Fess| intègre plusieurs résultats de recherche pour
fournir des résultats de recherche plus précis.

Qu'est-ce que le Rank Fusion
==============================

Le Rank Fusion est une technique qui combine les résultats de plusieurs algorithmes
de recherche ou méthodes de notation (par exemple mots-clés/BM25 et recherche sémantique/vectorielle) pour générer un classement unique optimisé.

Principaux avantages :

- Combine les forces de différents algorithmes
- Améliore la précision de la recherche
- Fournit des résultats de recherche diversifiés

Algorithmes pris en charge
===========================

|Fess| prend en charge l'algorithme RRF (Reciprocal Rank Fusion) pour le Rank Fusion.

RRF (Reciprocal Rank Fusion)
----------------------------

RRF calcule un score en additionnant l'inverse du rang de chaque document dans chaque
résultat de recherche. Lorsqu'un document est récupéré par plusieurs moteurs de recherche,
ses scores sont cumulés.

Formule ::

    score(d) = Σ 1 / (k + rank(d))

- ``k`` : Paramètre constant qui contrôle l'influence du rang (par défaut : 20)
- ``rank(d)`` : Rang du document d dans chaque résultat de recherche (base 0)
- ``Σ`` : Somme sur tous les moteurs de recherche dans lesquels le document d apparaît

Configuration
=============

fess_config.properties
----------------------

Configuration de base ::

    # Taille de la fenêtre (nombre de résultats à fusionner)
    # Remarque : doit être >= paging.search.page.max.size × 2.
    # Si la valeur est inférieure à ce minimum, le minimum est utilisé automatiquement.
    rank.fusion.window_size=200

    # Constante de rang (paramètre k pour RRF)
    rank.fusion.rank_constant=20

    # Nombre de threads pour le traitement parallèle
    # (si 0 ou moins, availableProcessors × 1.5 + 1 est utilisé)
    rank.fusion.threads=-1

    # Nom du champ de score (champ stockant le score fusionné)
    rank.fusion.score_field=rf_score

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Propriété
     - Défaut
     - Description
   * - ``rank.fusion.window_size``
     - ``200``
     - Nombre maximum de résultats récupérés depuis chaque moteur de recherche pour la fusion. Doit être >= ``paging.search.page.max.size × 2`` (``200`` par défaut) ; si une valeur inférieure est définie, elle est automatiquement relevée à ce minimum.
   * - ``rank.fusion.rank_constant``
     - ``20``
     - La constante ``k`` dans la formule RRF. Une valeur plus élevée réduit la différence de score entre les résultats mieux et moins bien classés.
   * - ``rank.fusion.threads``
     - ``-1``
     - Nombre de threads utilisés lors de l'exécution parallèle de plusieurs moteurs de recherche. Si ``0`` ou moins est spécifié, ``availableProcessors × 1.5 + 1`` est utilisé automatiquement.
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Nom du champ du document résultat utilisé pour stocker le score fusionné.

Propriétés système JVM
----------------------

Les moteurs de recherche à utiliser sont spécifiés en tant que propriété système JVM. Ajoutez la ligne
suivante dans ``fess.in.sh`` (ou ``fess.in.bat``) ::

    # Spécifier les moteurs de recherche (séparés par des virgules)
    -Drank.fusion.searchers=default,semantic_chunk

Ce paramètre se comporte comme suit :

- Il est défini en tant qu'option JVM, et non dans ``fess_config.properties``.
- ``default`` est le moteur qui effectue la recherche standard par mots-clés ; il est toujours disponible.
- Le nom d'un moteur de recherche est dérivé du nom de sa classe d'implémentation : on en retire
  le suffixe ``Searcher``, puis on convertit le reste en snake_case minuscule
  (``SemanticChunkSearcher`` → ``semantic_chunk``). Le moteur de recherche sémantique intégré au
  cœur (:doc:`search-semantic`) est enregistré sous le nom ``semantic_chunk``.
- Si ce paramètre n'est pas spécifié, tous les moteurs enregistrés sont utilisés. Si aucun des noms spécifiés ne correspond à un moteur enregistré, seul le moteur ``default`` est utilisé. Si vous utilisez le moteur de recherche sémantique intégré au cœur (:doc:`search-semantic`), vous n'avez normalement pas besoin de définir ce paramètre du tout.
- La fusion des résultats n'est effectuée que lorsque deux moteurs de recherche ou plus sont disponibles. Lorsqu'un seul moteur est disponible, aucune fusion n'est effectuée et les résultats de recherche normaux sont retournés.

.. warning::

   Si vous utilisiez auparavant le plugin ``fess-webapp-semantic-search`` de |Fess| 15.7 ou
   antérieur, il vous a peut-être été indiqué de définir ce paramètre sur
   ``-Drank.fusion.searchers=default,semantic``. Ce plugin enregistrait son moteur de recherche
   sous le nom ``semantic``, qui est un **moteur de recherche différent** du nom du moteur
   intégré au cœur, ``semantic_chunk``, introduit en 15.8. Si vous reportez ce réglage datant de
   la 15.7 tel quel dans la 15.8, la liste blanche n'inclut jamais ``semantic_chunk``, de sorte
   que la recherche sémantique intégrée au cœur (chunking de contenu + recherche vectorielle) **ne
   fonctionne pas du tout** — |Fess| continue de renvoyer silencieusement des résultats de
   recherche par mots-clés ordinaires (un avertissement est consigné au démarrage, mais
   l'exclusion par requête elle-même n'est consignée qu'au niveau DEBUG). Si votre configuration
   spécifie ``default,semantic``, supprimez ce réglage ou ajoutez-y ``semantic_chunk``. Voir
   « Migration depuis la version 15.7 ou antérieure » dans :doc:`search-semantic` pour plus de
   détails.

Intégration avec la recherche hybride
=======================================

Le Rank Fusion est particulièrement efficace pour la recherche hybride, qui combine la
recherche par mots-clés et la recherche sémantique. Pour utiliser la recherche sémantique,
configurez la fonctionnalité de chunking de contenu et définissez
``content_chunker.search.enabled=true``. Voir :doc:`search-semantic` pour plus de détails.

Exemples d'utilisation
=======================

Recherche hybride de base
--------------------------

1. Calculer le score BM25 avec la recherche par mots-clés
2. Calculer la similarité vectorielle avec la recherche sémantique
3. Fusionner les deux résultats avec RRF
4. Générer le classement final

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

Considérations de performance
==============================

Utilisation de la mémoire
--------------------------

- L'utilisation de la mémoire augmente car plusieurs résultats de recherche sont conservés.
- Utilisez ``rank.fusion.window_size`` pour limiter le nombre maximum de résultats à fusionner. Le moteur principal (le moteur ``default`` en tête de liste) récupère jusqu'à ``window_size`` résultats, tandis que chacun des autres moteurs récupère ``window_size ÷ nombre de moteurs`` résultats.

::

    # Taille de la fenêtre pour la fusion
    rank.fusion.window_size=200

Temps de traitement
--------------------

- Le temps de réponse augmente car plusieurs recherches sont exécutées.
- Utilisez ``rank.fusion.threads`` pour définir le nombre de threads pour l'exécution parallèle.

::

    # Nombre de threads pour l'exécution parallèle
    # (si 0 ou moins, availableProcessors × 1.5 + 1)
    rank.fusion.threads=-1

Dépannage
=========

Les résultats de recherche diffèrent des attentes
--------------------------------------------------

**Symptôme** : Les résultats après Rank Fusion diffèrent des attentes

**Vérifications** :

1. Vérifier les résultats de chaque type de recherche individuellement
2. Ajuster la valeur de ``rank.fusion.rank_constant``
3. Ajuster la valeur de ``rank.fusion.window_size``
4. Sur les pages profondes (où ``position de début × 2`` est supérieur ou égal à ``rank.fusion.window_size``), la fusion n'est pas effectuée et seul le moteur principal est utilisé. Pour obtenir des résultats fusionnés sur davantage de pages, augmentez ``rank.fusion.window_size``.

La recherche est lente
-----------------------

**Symptôme** : La recherche devient lente lorsque le Rank Fusion est activé

**Solutions** :

1. Réduire ``rank.fusion.window_size`` ::

       rank.fusion.window_size=100

2. Ajuster ``rank.fusion.threads`` ::

       rank.fusion.threads=4

Mémoire insuffisante
---------------------

**Symptôme** : Une erreur OutOfMemoryError se produit

**Solutions** :

1. Réduire ``rank.fusion.window_size``
2. Augmenter la taille du tas JVM

Référence
=========

- :doc:`scripting-overview` - Aperçu du scripting
- :doc:`search-advanced` - Configuration avancée de la recherche
- :doc:`llm-overview` - Guide d'intégration LLM (Recherche sémantique)
