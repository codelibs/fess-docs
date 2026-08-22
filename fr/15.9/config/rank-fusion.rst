=============================================================
Recherche hybride et Rank Fusion (sémantique + mots-clés)
=============================================================

Aperçu
======

La **recherche hybride** dans |Fess| combine la recherche traditionnelle par mots-clés (BM25) avec la **recherche sémantique (vectorielle)**, puis fusionne les deux ensembles de résultats grâce au **Rank Fusion** afin de produire des classements plus précis et plus pertinents. Le Rank Fusion intègre les résultats de plusieurs moteurs de recherche en un classement unique optimisé.

Dans |Fess| 15.9, la recherche sémantique (chunking de contenu + recherche vectorielle) est
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

.. note::

   L'algorithme de fusion est fixé à RRF : aucun réglage ne permet de basculer vers un autre
   algorithme. La pondération par moteur de recherche n'est pas non plus prise en charge — la
   contribution de chaque moteur est additionnée avec le même poids. Le seul paramètre permettant
   d'ajuster la tendance du classement est ``rank.fusion.rank_constant``.

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
    # (si 0 ou moins, availableProcessors × 3 ÷ 2 + 1 est utilisé)
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
     - Nombre maximum de résultats récupérés depuis chaque moteur de recherche pour la fusion. Doit être >= ``paging.search.page.max.size × 2`` (``200`` par défaut) ; si une valeur inférieure est définie, elle est automatiquement relevée à ce minimum (un avertissement WARN est alors consigné au démarrage).
   * - ``rank.fusion.rank_constant``
     - ``20``
     - La constante ``k`` dans la formule RRF. Une valeur plus élevée réduit la différence de score entre les résultats mieux et moins bien classés.
   * - ``rank.fusion.threads``
     - ``-1``
     - Nombre de threads du pool de threads fixe utilisé pour exécuter plusieurs moteurs de recherche en parallèle. Si ``0`` ou moins est spécifié, ``availableProcessors × 3 ÷ 2 + 1`` est utilisé automatiquement (le calcul étant effectué en arithmétique entière, la partie décimale est tronquée ; par exemple : 4 cœurs → 7, 5 cœurs → 8).
   * - ``rank.fusion.score_field``
     - ``rf_score``
     - Nom du champ du document résultat utilisé pour stocker le score fusionné.

.. note::

   **Moment de prise en compte des réglages**

   Les quatre réglages ci-dessus nécessitent tous un redémarrage de |Fess| pour que leur
   modification prenne effet. Les valeurs lues depuis ``fess_config.properties`` sont mises en
   cache dans la JVM : modifier le fichier pendant que |Fess| est en cours d'exécution reste donc
   sans effet.

   À titre indicatif, ``rank.fusion.window_size`` n'est lu qu'une seule fois au démarrage, et
   ``rank.fusion.threads`` au moment de la création du pool de threads. Le pool de threads étant
   créé lorsqu'un moteur de recherche autre que ``default`` (le moteur de recherche sémantique,
   par exemple) est enregistré, aucun pool n'est créé lorsque la recherche sémantique est
   désactivée.

Propriétés système JVM
----------------------

Les moteurs de recherche à utiliser sont spécifiés en tant que propriété système JVM. Ajoutez la
ligne suivante dans ``fess.in.sh`` ::

    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Drank.fusion.searchers=default,semantic_chunk"

Pour ``fess.in.bat``, écrivez plutôt ::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Drank.fusion.searchers=default,semantic_chunk

Ce paramètre se comporte comme suit :

- Il est défini en tant qu'option JVM, et non dans ``fess_config.properties``. Le nom de la clé
  doit être exactement ``rank.fusion.searchers``. Les formes préfixées couramment employées pour
  les autres réglages, ``-Dfess.config.`` ou ``-Dfess.system.`` (par exemple
  ``-Dfess.config.rank.fusion.searchers``), ne sont pas reconnues.
- À la place d'une option JVM, vous pouvez également le saisir sur une seule ligne, sous la forme
  ``rank.fusion.searchers=default,semantic_chunk``, dans le champ « Propriétés système » de la
  page « Système > Général » de l'interface d'administration. Notez que la valeur de ce champ
  n'est appliquée que si aucune propriété système du même nom n'est déjà définie. Une option
  ``-D`` est donc prioritaire, et modifier une valeur déjà appliquée nécessite un redémarrage de
  |Fess|.
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
   intégré au cœur, ``semantic_chunk``, introduit en 15.9. Si vous reportez ce réglage datant de
   la 15.7 tel quel dans la 15.9, la liste blanche n'inclut jamais ``semantic_chunk``, de sorte
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
configurez la fonctionnalité de chunking de contenu, puis définissez
``content_chunker.search.enabled=true``.

.. warning::

   Les réglages ``content_chunker.*``, tels que ``content_chunker.enabled`` ou
   ``content_chunker.search.enabled``, sont des **propriétés système** et non des réglages de
   ``fess_config.properties``. Définissez-les dans ``conf/system.properties``, ou fournissez-les
   en tant qu'option JVM sous la forme ``-Dfess.system.content_chunker.search.enabled=true``.
   Les écrire dans ``fess_config.properties`` reste sans effet. Par ailleurs,
   ``content_chunker.search.enabled`` n'étant évalué qu'au démarrage, un redémarrage de |Fess|
   est nécessaire après son activation.

Voir :doc:`search-semantic` pour plus de détails.

Vérification des résultats de fusion
======================================

Deux champs ajoutés aux résultats de recherche permettent de vérifier que le Rank Fusion est
réellement à l'œuvre.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Champ
     - Contenu
   * - ``searcher``
     - Tableau des noms des moteurs de recherche ayant récupéré le document (par exemple ``["default", "semantic_chunk"]``). Lorsque les deux y figurent, le document a été trouvé à la fois par la recherche par mots-clés et par la recherche sémantique.
   * - ``rf_score``
     - Score fusionné calculé par RRF. Le nom du champ peut être modifié via ``rank.fusion.score_field``.

Ces deux valeurs sont ajoutées dynamiquement au moment de la recherche et ne sont pas stockées
dans l'index. Elles ne figurent pas non plus par défaut dans la réponse de ``/api/v2/search`` :
pour les consulter, ajoutez la ligne suivante dans ``fess_config.properties``, puis redémarrez
|Fess| ::

    query.additional.api.response.fields=rf_score,searcher

.. note::

   ``query.additional.api.response.fields`` ajoute des entrées à la liste blanche des champs
   autorisés dans la réponse de l'API de recherche v2. N'y ajoutez pas de champs de contrôle
   d'accès tels que ``role`` ou ``virtual_host`` : les informations de contrôle d'accès seraient
   alors exposées dans la réponse de l'API de recherche.

Impact sur le nombre de résultats
===================================

Lorsque le Rank Fusion est exécuté, le nombre total de résultats retourné n'est pas celui du
moteur principal (le moteur ``default``, enregistré en tête de liste) tel quel : il est corrigé
comme suit ::

    nombre total de résultats = nombre total de résultats du moteur principal + correction

La correction correspond au nombre de documents figurant parmi les ``window_size ÷ 2`` premiers
résultats fusionnés, mais absents des ``window_size ÷ 2`` premiers résultats du moteur principal.
Autrement dit, le nombre de résultats augmente du nombre de documents trouvés uniquement par la
recherche sémantique. Pour une même requête, le nombre de résultats peut donc varier selon que la
recherche hybride est activée ou non.

À noter : lorsque le nombre total de résultats du moteur principal est retourné sous forme de
valeur approchée (borne inférieure), cette correction n'est pas appliquée.

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
- Utilisez ``rank.fusion.window_size`` pour limiter le nombre maximum de résultats à fusionner. Le moteur principal (le moteur ``default`` en tête de liste) récupère jusqu'à ``window_size`` résultats, tandis que chacun des autres moteurs récupère ``window_size ÷ nombre de moteurs`` résultats (le ``nombre de moteurs`` correspond au total, moteur principal inclus, et la division est tronquée).
- Par exemple, avec deux moteurs (``default`` et ``semantic_chunk``) et ``window_size=200``, le moteur principal récupère 200 résultats et le moteur sémantique 100 : au maximum 300 documents sont donc conservés.

::

    # Taille de la fenêtre pour la fusion
    rank.fusion.window_size=200

.. warning::

   ``rank.fusion.window_size`` ne peut pas descendre en dessous de
   ``paging.search.page.max.size × 2``. Lorsque ``paging.search.page.max.size`` conserve sa valeur
   par défaut ``100``, la borne inférieure vaut ``200``, soit exactement la valeur par défaut de
   ``rank.fusion.window_size``. Autrement dit, **dans la configuration par défaut, window_size ne
   peut pas être réduit en dessous de sa valeur par défaut**. Si une valeur plus petite est
   définie, un avertissement WARN est consigné au démarrage et la valeur est relevée à ``200``.
   Pour la réduire réellement, il faut d'abord abaisser ``paging.search.page.max.size``, ce qui
   réduit du même coup le nombre maximum de résultats qu'un client peut demander par page dans
   l'écran de recherche comme dans l'API.

Temps de traitement
--------------------

- Le temps de réponse augmente car plusieurs recherches sont exécutées.
- Utilisez ``rank.fusion.threads`` pour définir le nombre de threads pour l'exécution parallèle.

::

    # Nombre de threads pour l'exécution parallèle
    # (si 0 ou moins, availableProcessors × 3 ÷ 2 + 1)
    rank.fusion.threads=-1

.. note::

   Aucun délai d'expiration n'est appliqué à l'exécution des moteurs de recherche. Si l'un d'eux
   ne répond pas, la requête de recherche attend qu'il ait terminé.

Comportement en cas d'échec d'un moteur de recherche
======================================================

Lorsqu'un moteur de recherche échoue sur une exception, ses résultats sont traités comme vides :
un avertissement WARN est consigné, puis la fusion se poursuit avec les seuls résultats des autres
moteurs. La requête de recherche elle-même n'échoue pas.

Font toutefois exception les erreurs de syntaxe de requête (``InvalidQueryException``) et les
dépassements de la limite de pagination (``ResultOffsetExceededException``) : celles-ci sont
retournées telles quelles en tant qu'erreurs. Par ailleurs, sur les pages profondes où la fusion
n'est pas effectuée (où ``position de début × 2`` est supérieur ou égal à
``rank.fusion.window_size``), une exception levée par le moteur principal est retournée telle
quelle en tant qu'erreur de la requête de recherche.

Le moteur de recherche sémantique retourne des résultats vides lorsqu'il ne parvient pas à joindre
le fournisseur d'embedding ou que le calcul des embeddings échoue. Là encore, aucune erreur n'est
levée : seuls les résultats de la recherche par mots-clés sont retournés.

Dépannage
=========

Les résultats de recherche diffèrent des attentes
--------------------------------------------------

**Symptôme** : Les résultats après Rank Fusion diffèrent des attentes

**Vérifications** :

1. Vérifier le champ ``searcher`` (voir « Vérification des résultats de fusion »). Si tous les
   documents ne contiennent que ``["default"]``, le moteur de recherche sémantique ne retourne
   aucun résultat.
2. Vérifier que la recherche sémantique n'est pas ignorée. Outre les requêtes contenant une
   syntaxe de recherche (``"``, ``:``, ``AND``, etc.), le filtrage par label, par tri ou par
   facette, la recherche par géolocalisation et la recherche de documents similaires font que le
   moteur de recherche sémantique ne retourne aucun résultat : seuls les résultats de la
   recherche par mots-clés sont alors renvoyés. Voir :doc:`search-semantic` pour le détail des
   conditions d'exclusion.
3. Vérifier les résultats de chaque type de recherche individuellement
4. Ajuster la valeur de ``rank.fusion.rank_constant``
5. Sur les pages profondes (où ``position de début × 2`` est supérieur ou égal à
   ``rank.fusion.window_size``, soit à partir du 101e résultat avec les valeurs par défaut), la
   fusion n'est pas effectuée et seul le moteur principal est utilisé. Pour obtenir des résultats
   fusionnés sur davantage de pages, augmentez ``rank.fusion.window_size``.

La recherche est lente
-----------------------

**Symptôme** : La recherche devient lente lorsque le Rank Fusion est activé

**Solutions** :

1. Ajuster ``rank.fusion.threads`` ::

       rank.fusion.threads=4

2. Réduire ``rank.fusion.window_size``. Cette valeur ne pouvant pas descendre en dessous de sa
   borne inférieure (``paging.search.page.max.size × 2``), les deux réglages suivants doivent être
   définis ensemble dans la configuration par défaut ::

       paging.search.page.max.size=50
       rank.fusion.window_size=100

   Notez que le nombre maximum de résultats pouvant être demandés par page diminue lui aussi. Un
   redémarrage est nécessaire après ces modifications.

Mémoire insuffisante
---------------------

**Symptôme** : Une erreur OutOfMemoryError se produit

**Solutions** :

1. Réduire ``rank.fusion.window_size`` en suivant la même procédure que dans « La recherche est
   lente »
2. Augmenter la taille du tas JVM

Référence
=========

- :doc:`search-semantic` - Configuration de la recherche sémantique (chunking de contenu)
- :doc:`scripting-overview` - Aperçu du scripting
- :doc:`search-advanced` - Configuration avancée de la recherche
- :doc:`llm-overview` - Guide d'intégration LLM (Recherche sémantique)
