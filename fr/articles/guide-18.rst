===========================================
Recherche sémantique : chercher par le sens
===========================================

Introduction
============

Si un utilisateur cherche « je veux que ma paie arrive sur une autre banque » alors que le règlement interne s'intitule « Procédure de changement du compte de versement du salaire », la recherche par mots-clés ne le trouvera pas.
Dans Fess 15.9, la « recherche sémantique », qui convertit le texte en vecteurs représentant son sens et effectue la recherche avec ces vecteurs, est intégrée au cœur du produit et fonctionne sans plugin (selon l'endroit où s'exécute le modèle d'embedding, vous ajoutez un plugin).

En suivant les étapes de cet article, vous saurez :

- Distinguer les cas où la recherche sémantique est utile de ceux où la recherche par mots-clés suffit
- Lancer immédiatement avec Docker un environnement où la recherche sémantique est déjà configurée
- Configurer ``content_chunker.*`` sur un Fess existant et générer les vecteurs avec la tâche d'indexation
- Vérifier avec le champ ``searcher`` si un résultat de recherche a été trouvé par la recherche vectorielle

La configuration du mode de recherche IA (RAG) est traitée dans :doc:`guide-19`.

Quand la recherche sémantique est utile
=======================================

La recherche sémantique de Fess ne remplace pas la recherche par mots-clés (BM25).
Elle fonctionne comme une « recherche hybride » : la recherche par mots-clés et la recherche vectorielle sont toutes deux exécutées, et leurs résultats sont fusionnés en un seul classement par Rank Fusion (RRF).

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - La recherche sémantique est utile
     - La recherche par mots-clés suffit
   * - Les utilisateurs et les documents emploient des mots différents (« banque pour ma paie » et « compte de versement du salaire », « travailler depuis chez soi » et « télétravail »)
     - Recherche de la même chaîne que dans le document : références de produits, codes d'erreur, noms de personnes, etc.
   * - Poser une question sous forme de phrase (« Comment demander un nouveau PC »)
     - Les reformulations sont peu nombreuses et tiennent entièrement dans un dictionnaire de synonymes
   * - Chercher en français pour trouver des documents en anglais (nécessite un modèle d'embedding multilingue)
     - Utilisation d'une syntaxe de recherche comme les phrases ou les caractères génériques (dans ce cas, la recherche vectorielle elle-même n'est pas exécutée)

Si les reformulations sont en nombre limité, il est plus simple d'essayer d'abord un dictionnaire de synonymes.
Pour enregistrer des synonymes à partir des termes sans résultat du journal de recherche, consultez :doc:`guide-08`.

Déroulement du traitement dans Fess
===================================

#. Le robot d'exploration enregistre les documents dans l'index comme d'habitude. À ce stade, il n'y a pas encore de vecteurs.
#. La tâche planifiée ``Content Chunk Vector Indexer`` repère les documents non traités, découpe le texte en chunks (fragments), crée un vecteur d'embedding pour chaque chunk et l'enregistre dans le champ ``content_chunk_vector``. Le résultat est consigné dans le champ ``content_chunk_status``.
#. Lorsque ``content_chunker.search.enabled=true``, chaque recherche exécute la recherche par mots-clés (searcher ``default``) et la recherche vectorielle (searcher ``semantic_chunk``), puis les fusionne par RRF.

Cette tâche est désactivée par défaut et n'est pas liée à l'exploration.
Notez que l'ajout des paramètres seul ne crée pas de vecteurs et que les résultats restent ceux de la seule recherche par mots-clés.

Prérequis
=========

**OpenSearch avec le plugin k-NN**

L'index de recherche créé par Fess 15.9 contient un champ de type ``knn_vector``, que vous utilisiez ou non la recherche sémantique.
L'image Docker ``ghcr.io/codelibs/fess-opensearch`` et la distribution standard d'OpenSearch incluent le plugin k-NN.
Avec la distribution minimal, qui ne contient pas le plugin k-NN, l'index ne peut pas être créé et Fess ne démarre pas.

**Fournisseur d'embedding**

Choisissez avec ``content_chunker.embedding.name`` où s'exécute le modèle qui convertit le texte en vecteurs.

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - Valeur
     - Prérequis
     - Description
   * - ``opensearch`` (par défaut)
     - Aucun plugin supplémentaire
     - Utilise un modèle déployé dans OpenSearch ML Commons
   * - ``ollama``
     - Plugin ``fess-llm-ollama``
     - Utilise un modèle d'embedding d'Ollama (modèle par défaut : ``embeddinggemma``)
   * - ``openai``
     - Plugin ``fess-llm-openai``
     - Utilise l'API d'embeddings d'OpenAI (modèle par défaut : ``text-embedding-3-small``)
   * - ``gemini``
     - Plugin ``fess-llm-gemini``
     - Utilise l'API d'embeddings de Google Gemini
   * - ``bedrock``
     - Plugin ``fess-llm-bedrock``
     - Utilise un modèle d'embedding d'Amazon Bedrock

Installez le plugin dans la même version mineure que Fess (15.9.x), puis redémarrez Fess après l'installation.
OpenAI, Gemini et Bedrock sont facturés à l'usage : la première exécution de la tâche entraîne en une seule fois les frais pour tous les documents existants.

La méthode la plus rapide : essayer avec docker-semanticsearch
==============================================================

Le dépôt docker-semanticsearch démarre avec Docker Compose un Fess 15.9 où la recherche sémantique est déjà configurée.
Il déploie automatiquement un modèle d'embedding multilingue (``paraphrase-multilingual-MiniLM-L12-v2``, 384 dimensions) dans OpenSearch ML Commons et va jusqu'à activer la tâche d'indexation.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh`` récupère le thème ``semanticlens`` de la page de recherche depuis le dépôt ``fess-themes``.
Le thème présent sur ``main``, la source par défaut de ``v15.9.0``, est destiné à Fess 15.10 et versions ultérieures (``minFessVersion: 15.10``) ; c'est pourquoi ``FESS_THEMES_REF`` désigne la branche ``15.9.x``, qui contient le thème pour 15.9.

Au premier démarrage, le téléchargement du modèle (environ 490MB) prend quelques minutes.
L'environnement est prêt lorsque ``docker compose ps -a`` indique ``fess01`` comme healthy et ``init-semantic`` et ``init-fess-chunk`` comme ``Exited (0)``.

Ensuite, comme pour un Fess ordinaire, créez une configuration d'exploration dans la console d'administration (``http://localhost:8080/admin``) et lancez l'exploration.
Dans cet environnement, la tâche d'indexation s'exécute toutes les heures.
Pour créer les vecteurs immédiatement, ouvrez ``Content Chunk Vector Indexer`` dans [Système] > [Planificateur] et cliquez sur [Démarrer maintenant].

En plus des paramètres expliqués plus loin dans cet article, cet environnement utilise les valeurs suivantes :

- La fusion est effectuée côté OpenSearch (``rank.fusion.engine.enabled=true``)
- La longueur des chunks est de 250 caractères (car la limite d'entrée du modèle est de 128 jetons)
- Seuil minimal de similarité ``content_chunker.search.min_score=0.5``
- Le thème ``semanticlens``, qui indique pour chaque résultat s'il a été trouvé par mots-clés, par recherche sémantique ou par les deux

Pour modifier ces valeurs, consultez la section Configuration du README du dépôt.

Activer la recherche sémantique sur un Fess existant
====================================================

Les étapes sont présentées ici avec l'exemple d'``embeddinggemma`` d'Ollama (768 dimensions, multilingue).
Pour utiliser le fournisseur intégré ``opensearch``, à la place des étapes 1 et 2, déployez un modèle dans ML Commons et définissez ``content_chunker.embedding.name=opensearch`` et ``content_chunker.embedding.opensearch.model.id``.
La procédure se trouve dans « Procédure de configuration (exemple avec le fournisseur opensearch) » de `Recherche sémantique <https://fess.codelibs.org/fr/stable/config/search-semantic.html>`__.

Étape 1 : installer le plugin
-----------------------------

Dans [Système] > [Plugin] > [Installer], sélectionnez ``fess-llm-ollama`` en version 15.9.x, installez-le, puis redémarrez Fess.
Avec Docker, indiquez ``FESS_PLUGINS=fess-llm-ollama:15.9.0`` pour ``fess01`` dans ``compose.yaml``.

Étape 2 : préparer le modèle d'embedding
----------------------------------------

Récupérez le modèle sur le serveur qui exécute Ollama.

::

    $ ollama pull embeddinggemma

Étape 3 : écrire les paramètres dans system.properties
------------------------------------------------------

Les paramètres ``content_chunker.*`` sont lus uniquement depuis ``system.properties``.
Ils sont ignorés s'ils sont écrits dans ``fess_config.properties`` ou passés avec ``-Dfess.config.``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type d'installation
     - Emplacement
   * - Version ZIP
     - ``app/WEB-INF/conf/system.properties``
   * - Version RPM/DEB
     - ``/etc/fess/system.properties``
   * - Docker (docker-fess)
     - Indiquer sous la forme ``-Dfess.system.<clé>=<valeur>`` dans ``FESS_JAVA_OPTS`` de ``compose.yaml``

``/opt/fess/system.properties`` dans le conteneur Docker est également lu, mais ``fess01`` de docker-fess n'a pas de volume : le fichier disparaît avec ``docker compose down``.

Écrivez le contenu suivant :

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url`` est l'adresse d'Ollama vue depuis Fess.
Si Fess s'exécute dans Docker, ``localhost`` désigne le conteneur lui-même : remplacez-la par une adresse joignable depuis le conteneur.

``content_chunker.embedding.dimension`` doit impérativement correspondre à la dimension de sortie du modèle.
Cette valeur est inscrite dans le mapping au moment de la création de l'index et ne peut pas être modifiée ensuite.

Étape 4 : redémarrer Fess
-------------------------

Le passage de ``content_chunker.search.enabled`` à ``true`` ne prend effet qu'après un redémarrage (les autres ``content_chunker.*`` sont relus pendant l'exécution).

Étape 5 : reconstruire l'index existant
---------------------------------------

Dans un environnement où Fess a déjà été démarré au moins une fois, le mapping avec la nouvelle dimension n'est pas appliqué à l'index.
Dans [Informations système] > [Maintenance], activez « Remplacer les alias » dans « Réindexation », puis cliquez sur [Démarrer].
Ce n'est pas nécessaire dans un nouvel environnement où vous avez effectué l'étape 3 avant le premier démarrage.

La réindexation s'exécute de manière asynchrone en arrière-plan, et l'écran n'en affiche pas la fin.
Avant de passer à l'étape suivante, vérifiez que les alias ``fess.search`` et ``fess.update`` pointent tous deux vers le nouvel index (``fess.<horodatage>``).

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

L'ancien index n'est pas supprimé automatiquement : supprimez-le manuellement une fois la vérification faite.
Il n'est pas nécessaire de relancer l'exploration.
La tâche d'indexation crée les vecteurs à partir du texte déjà enregistré.

Étape 6 : activer et exécuter la tâche d'indexation
---------------------------------------------------

#. Dans [Système] > [Planificateur], ouvrez ``Content Chunk Vector Indexer`` et cliquez sur [Modifier].
#. Cochez « Activé » pour « Statut », modifiez la planification si nécessaire, puis cliquez sur [Mettre à jour]. La planification par défaut est ``0 13 * * *`` (tous les jours à 13:00).
#. De retour sur l'écran de détails, [Démarrer maintenant] s'affiche : cliquez dessus pour exécuter la tâche une fois.

La tâche n'étant pas liée à l'exploration, les documents explorés sont aussitôt trouvables par mots-clés, mais ne deviennent cibles de la recherche vectorielle qu'après la prochaine exécution de cette tâche.
Planifiez-la à une heure postérieure à la fin de vos tâches d'exploration.

Vérifier le fonctionnement
==========================

Vérifier que les vecteurs ont été créés
---------------------------------------

Demandez à OpenSearch d'agréger le résultat du traitement de chaque document.

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valeur
     - Signification
   * - ``pending``
     - Non traité (sera traité à la prochaine exécution de la tâche). Les documents explorés à nouveau reviennent aussi à cet état
   * - ``done``
     - Découpage en chunks et génération des vecteurs terminés
   * - ``chunked``
     - Découpage en chunks uniquement. Les documents sont aussi dans cet état lorsque le plugin du fournisseur n'est pas installé
   * - ``skipped``
     - Le texte est vide, ou le nombre de chunks a dépassé la limite (1000 par défaut)
   * - ``fail``
     - Échec. Vérifiez la cause dans le fichier journal ``fess-chunk.log``

Si ``pending`` diminue et ``done`` augmente à chaque exécution de la tâche, tout se déroule correctement.

Vérifier si un résultat a été trouvé par la recherche vectorielle
-----------------------------------------------------------------

Le champ ``searcher`` d'un résultat de recherche contient les noms des searchers qui ont trouvé le document.
Par défaut, il n'est pas inclus dans la réponse de l'API de recherche : ajoutez la ligne suivante à ``fess_config.properties`` et redémarrez (avec Docker, ``-Dfess.config.query.additional.api.response.fields=searcher``).

::

    query.additional.api.response.fields=searcher

Cherchez avec une reformulation dont les mots-clés ne correspondent pas au document.
S'il existe un document qui explique la « Procédure de changement du compte de versement du salaire », cherchez comme suit :

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=je veux que ma paie arrive sur une autre banque" \
      | jq '.response.data[] | {title, searcher}'

Un résultat dont ``searcher`` vaut ``["semantic_chunk"]`` a été trouvé uniquement par la recherche vectorielle, et ``["default", "semantic_chunk"]`` par les deux.
Si tous les résultats n'ont que ``["default"]``, la recherche vectorielle ne renvoie aucun résultat.
Consultez la section suivante.

Points d'achoppement courants
=============================

**Le paramètre rank.fusion.searchers de l'époque de l'ancien plugin est toujours présent**

Avec le plugin ``fess-webapp-semantic-search`` de la version 15.7 et antérieures, on indiquait ``-Drank.fusion.searchers=default,semantic``.
En 15.9, le searcher s'appelle ``semantic_chunk`` : si ce paramètre subsiste, la recherche sémantique n'est pas exécutée et seuls les résultats de la recherche par mots-clés sont renvoyés.
Au démarrage, le journal WARN ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'`` est émis.
Vérifiez à la fois les options JVM et le champ « Propriété système » de [Système] > [Général], et supprimez ce paramètre (s'il n'est pas indiqué, tous les searchers sont utilisés).
Pour la migration depuis l'ancien plugin, consultez « Migration depuis la version 15.7 ou antérieure » de `Recherche sémantique <https://fess.codelibs.org/fr/stable/config/search-semantic.html>`__.

**La recherche vectorielle n'est pas exécutée pour les requêtes contenant une syntaxe de recherche**

Les requêtes suivantes sont traitées uniquement par la recherche par mots-clés :

- Phrases (``"..."``), caractères génériques, recherche floue et plages
- Phrases se terminant par un ``?`` ASCII (par exemple « Qu'est-ce que ...? »). Le « ？ » pleine chasse utilisé en japonais et en chinois n'est pas concerné
- Exclusions (``-mot``, ``NOT mot``) et pondérations (``mot^2``)
- Recherches qui spécifient un tri

Le filtrage par ``label:``, ``site:`` ou par facettes ne pose pas de problème, car il est aussi appliqué à la recherche vectorielle comme filtre.

**La dimension ne correspond pas, ou l'index a été créé sans la définir**

Si l'index est créé sans définir ``content_chunker.embedding.dimension``, le mapping passe à 768 dimensions et la tâche marque les documents en ``fail``.
Si la dimension du modèle n'est pas 768, définissez la bonne valeur, puis refaites la réindexation de l'étape 5.
Les documents ``fail`` et ``skipped`` ne sont pas retraités lorsque la tâche est relancée.
Après avoir corrigé la cause, définissez temporairement ``content_chunker.job.retry_failed=true`` et exécutez la tâche.

**Le modèle d'embedding a été changé**

Les vecteurs enregistrés ont été créés avec l'ancien modèle : changer seulement de modèle dégrade la précision de la recherche (aucune erreur n'apparaît, même si la dimension est identique).
La procédure pour supprimer ``content_chunk_vector`` et ``content_chunk_status`` puis relancer la tâche figure dans la section « Remarques » de la référence.

**Des documents peu pertinents remontent en tête**

La recherche vectorielle renvoie les documents par ordre de proximité, même ceux dont la similarité est faible.
En définissant dans ``content_chunker.search.min_score`` un seuil minimal de similarité cosinus (de 0 à 1), vous excluez les documents qui ne l'atteignent pas.
La valeur appropriée dépend du modèle et des documents : ajustez-la en cherchant à la fois avec des termes qui n'obtenaient aucun résultat et avec des termes sans rapport.

**La nature des résultats change dans la seconde moitié de la page 2 et au-delà**

Dans la configuration par défaut, où la fusion se fait côté Fess, seuls les 200 premiers résultats de chaque searcher (``rank.fusion.window_size``) sont fusionnés, et à partir du 101e résultat, il ne s'agit plus que de résultats de la recherche par mots-clés.
Le nombre de résultats augmente aussi du nombre de documents trouvés uniquement par la recherche vectorielle.
Pour le fonctionnement de la fusion et les options de réglage (``rank.fusion.rank_constant``, fusion côté OpenSearch), consultez `Recherche hybride et Rank Fusion <https://fess.codelibs.org/fr/stable/config/rank-fusion.html>`__.

Relation avec le mode de recherche IA et la recherche multimodale
=================================================================

Le mode de recherche IA (RAG) peut être utilisé sans activer la recherche sémantique.
Pour les documents dont les vecteurs ont été créés avec ``content_chunker.enabled=true``, le texte utilisé pour la réponse est restreint aux chunks les plus proches de la question, ce qui permet de transmettre au LLM les passages pertinents même pour de longs documents.
Pour la configuration du mode de recherche IA, consultez :doc:`guide-19`.

La recherche multimodale (``fess-webapp-multimodal``), qui recherche à la fois dans les images et le texte, ne peut pas être utilisée en même temps que la recherche sémantique textuelle de cet article sur le même Fess.
Pour plus de détails, consultez :doc:`guide-21`.

Articles suivants
=================

- Améliorer les termes sans résultat du journal de recherche avec des synonymes et la Correspondance de clé : :doc:`guide-08`
- Faire répondre une IA générative à partir des documents internes : :doc:`guide-19`
- Rechercher en incluant les images : :doc:`guide-21`
- Rechercher depuis des systèmes métier via l'API de recherche : :doc:`guide-11`

Références
==========

- `Recherche sémantique (chunking de contenu + recherche vectorielle) <https://fess.codelibs.org/fr/stable/config/search-semantic.html>`__
- `Recherche hybride et Rank Fusion (sémantique + mots-clés) <https://fess.codelibs.org/fr/stable/config/rank-fusion.html>`__
- `Configuration Ollama (LLM local / RAG) <https://fess.codelibs.org/fr/stable/config/llm-ollama.html>`__
- `Planificateur de tâches <https://fess.codelibs.org/fr/stable/admin/scheduler-guide.html>`__
- `Maintenance <https://fess.codelibs.org/fr/stable/admin/maintenance-guide.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch (GitHub) <https://github.com/codelibs/docker-semanticsearch>`__
