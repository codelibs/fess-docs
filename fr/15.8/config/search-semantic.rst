=====================================================================
Recherche sémantique (chunking de contenu + recherche vectorielle)
=====================================================================

Aperçu
======

Dans |Fess| 15.8, la **fonctionnalité de chunking de contenu** — qui découpe le corps des
documents en chunks et génère puis stocke un vecteur d'embedding pour chaque chunk — a été
intégrée au cœur du produit. Les vecteurs générés sont utilisés à deux fins :

- **Recherche sémantique** : une recherche hybride qui combine la recherche par mots-clés (BM25)
  et la recherche vectorielle via le Rank Fusion. Les documents sémantiquement proches de la
  requête peuvent correspondre même sans chevauchement exact de mots-clés.
- **Mode de recherche IA (RAG)** : lors de la génération d'une réponse, seuls les chunks
  sémantiquement les plus proches de la question sont sélectionnés comme contexte du LLM, ce qui
  améliore la qualité de la réponse et l'efficacité en tokens.

Tout ceci est désactivé par défaut. Tant que vous ne l'activez pas, |Fess| continue de fonctionner
exactement comme avant, en utilisant uniquement la recherche par mots-clés. Si vous mettez à
niveau |Fess| depuis la version 15.7 ou antérieure, ou si vous utilisiez le plugin
``fess-webapp-semantic-search``, consultez :ref:`semantic-search-migration`.

Flux de traitement
--------------------

1. Le crawler indexe les documents comme d'habitude (aucun chunk n'existe à ce stade).
2. La tâche du planificateur **Content Chunk Vector Indexer** recherche les documents non
   traités, découpe leur contenu (le champ ``content``) en chunks, génère les vecteurs
   d'embedding et les stocke dans le champ ``content_chunk_vector``. À cette occasion, le champ
   ``content`` lui-même est réécrit sous la forme du tableau des chunks (``content_length``
   conserve sa valeur d'origine).
3. Le résultat de ce traitement est enregistré dans le champ ``content_chunk_status`` (décrit
   ci-dessous).
4. Lorsque ``content_chunker.search.enabled=true``, le moteur de recherche sémantique participe
   au Rank Fusion au moment de la recherche.

Prérequis
=========

- **OpenSearch avec le plugin k-NN** : dans |Fess| 15.8, le mapping de l'index de recherche
  (``fess.search``) inclut toujours le champ ``content_chunk_vector`` (de type ``nested``, dont
  la sous-propriété ``vector`` est le ``knn_vector`` utilisé pour l'ANN), que la fonctionnalité
  de chunking de contenu soit activée ou non, et les réglages de l'index incluent toujours
  ``index.knn: true``. Par conséquent, si OpenSearch n'a pas le plugin k-NN installé, la création
  d'un nouvel index échoue purement et simplement et |Fess| ne peut pas démarrer.

  .. list-table::
     :header-rows: 1
     :widths: 35 65

     * - Configuration
       - Prise en charge du plugin k-NN
     * - OpenSearch intégré (``bin/fess``, ou les paquets TAR.GZ/ZIP avec ``SEARCH_ENGINE_HTTP_URL``
         laissé non défini — la valeur par défaut)
       - Livré avec le plugin k-NN. Il n'inclut cependant pas les bibliothèques natives JNI ;
         le seul moteur ANN pris en charge est donc ``lucene``. ``content_chunker.search.knn.engine``
         accepte aussi ``faiss`` comme valeur, et le définir ici crée quand même le mapping avec
         succès — mais **les documents sont silencieusement perdus à chaque écriture et les
         recherches ne renvoient plus aucun résultat**. (|Fess| consigne un avertissement au
         démarrage lorsque cette combinaison est détectée.)
     * - Docker (``ghcr.io/codelibs/fess-opensearch``), les paquets RPM/DEB (qui se connectent
         toujours à un OpenSearch externe installé séparément), ou un autre OpenSearch externe
         (distribution standard)
       - Entièrement pris en charge, y compris ``faiss``.
     * - La **distribution minimale** d'un OpenSearch externe
       - **Non prise en charge.** Elle n'inclut pas le plugin k-NN, donc la création d'un
         nouvel index échoue.

  ``nmslib`` n'est jamais une valeur acceptée pour ``content_chunker.search.knn.engine``, quelle
  que soit la configuration ci-dessus : ``content_chunk_vector`` est un champ ``nested``, et le
  plugin k-NN ne prend en charge les champs nested qu'avec les moteurs ``lucene``/``faiss``
  (``nmslib`` est en outre déprécié et restreint depuis OpenSearch 3.0). Le définir entraîne un
  retour à ``lucene`` avec un avertissement ; consultez la Référence de configuration ci-dessous
  pour les autres valeurs acceptées des réglages ANN.

- **Version d'OpenSearch pour un cluster externe** : les réglages d'index ``fess.search``
  fournis envoient toujours ``index.knn`` et ``knn.derived_source.enabled`` (dans
  ``fess_indices/fess.json`` et ses variantes AWS/cloud). Ce dernier est un réglage relativement
  récent du plugin k-NN : un OpenSearch plus ancien qui ne le reconnaît pas fait échouer la
  création de l'index, que le plugin k-NN lui-même soit installé ou non. Pour connaître les
  versions d'OpenSearch prises en charge par |Fess| 15.8, consultez
  :doc:`../install/prerequisites`.

- **Fournisseur d'embedding** : utilisez l'un des suivants.

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Valeur de configuration
     - Fourni par
     - Description
   * - ``opensearch``
     - Cœur de |Fess| (intégré)
     - Utilise un modèle d'embedding déployé sur OpenSearch ML Commons. Aucun plugin
       supplémentaire requis. Réglage par défaut.
   * - ``ollama``
     - Plugin ``fess-llm-ollama``
     - Utilise un modèle d'embedding Ollama (par ex. ``nomic-embed-text``).
   * - ``openai``
     - Plugin ``fess-llm-openai``
     - Utilise l'API d'embeddings d'OpenAI.
   * - ``gemini``
     - Plugin ``fess-llm-gemini``
     - Utilise l'API d'embeddings de Google Gemini.
   * - ``none``
     - Cœur de |Fess| (intégré)
     - Découpe les documents en chunks uniquement ; aucun vecteur n'est généré (mode chunking
       seul).

Référence de configuration
============================

Tous les réglages ``content_chunker.*`` résident dans un canal unique : les **propriétés
système** (``system.properties``). Définissez-les dans
``app/WEB-INF/conf/system.properties`` (``/etc/fess/system.properties`` pour les paquets RPM/DEB,
``/opt/fess/system.properties`` sous Docker), ou fournissez une valeur initiale via l'option de
démarrage ``-Dfess.system.<key>``. Les valeurs sont rechargées à l'exécution, de sorte que la
plupart des réglages prennent effet immédiatement après leur modification. La seule exception est
l'activation de ``content_chunker.search.enabled`` (``false`` → ``true``) : le moteur de
recherche sémantique n'étant enregistré qu'au démarrage, **ce changement nécessite un redémarrage
pour prendre effet**.

.. note::

   La liste des clés ``content_chunker.*`` figure également sous forme de commentaires dans
   ``fess_config.properties``, mais ces clés ne sont lues que depuis le canal
   ``system.properties``. Les écrire dans ``fess_config.properties`` ou via
   ``-Dfess.config.<key>`` reste sans effet : définissez-les impérativement dans
   ``system.properties``. Notez par ailleurs que l'écran d'administration **Informations système
   > Informations de configuration** affiche les valeurs courantes **en lecture seule** ; il ne
   permet pas d'y définir les réglages ``content_chunker.*``.

Réglages dans system.properties
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - Propriété
     - Défaut
     - Description
   * - ``content_chunker.enabled``
     - ``false``
     - Interrupteur principal de toute la fonctionnalité de chunking de contenu
   * - ``content_chunker.chunker.name``
     - ``length``
     - Méthode de chunking
   * - ``content_chunker.length.chunk_size``
     - ``800``
     - Nombre de caractères par chunk (valeur cible, voir la note ci-dessous)
   * - ``content_chunker.length.overlap``
     - ``0``
     - Nombre de caractères de chevauchement entre les chunks
   * - ``content_chunker.length.boundary.enabled``
     - ``true``
     - Déplace chaque coupure vers la rupture la plus appropriée dans la fenêtre de recherche, en
       donnant la priorité à un saut de ligne ou une fin de phrase sur un séparateur de
       proposition ou un espace, puis à ceux-ci sur un changement d'écriture, au lieu de couper
       exactement à ``chunk_size`` caractères
   * - ``content_chunker.length.boundary.lookback_percent``
     - ``20``\ (0-50)
     - Jusqu'où, avant le point de coupure idéal et en pourcentage de ``chunk_size``, la
       recherche de rupture peut remonter
   * - ``content_chunker.length.boundary.lookahead_percent``
     - ``5``\ (0-25)
     - Jusqu'où, après le point de coupure idéal et en pourcentage de ``chunk_size``, la
       recherche de rupture peut avancer
   * - ``content_chunker.max_chunks_per_document``
     - ``1000``
     - Nombre maximal de chunks par document. Les documents qui dépassent cette limite sont
       marqués ``skipped``
   * - ``content_chunker.embedding.name``
     - ``opensearch``
     - Fournisseur d'embedding (``opensearch`` / ``ollama`` / ``openai`` / ``gemini`` / ``none``)
   * - ``content_chunker.embedding.dimension``
     - ``768``
     - Dimension du vecteur d'embedding. Cette valeur est utilisée lors de la création du
       mapping, elle **doit** donc correspondre à la dimension du modèle d'embedding utilisé.
       Elle est lue par deux chemins distincts, au comportement différent. Lors de la création du
       mapping de l'index, une valeur non définie, non numérique, nulle ou négative, ou
       supérieure à ``16000`` (le maximum propre au plugin k-NN) entraîne l'utilisation de
       ``768`` avec un avertissement. À l'exécution du processus d'embedding, en revanche, il n'y
       a aucun repli : une valeur non définie, non numérique, nulle ou négative provoque une
       erreur. Une valeur supérieure à ``16000`` n'est pas rejetée à l'exécution, de sorte que
       seul le mapping est créé avec ``768``, ce qui aboutit à une incohérence de dimension
   * - ``content_chunker.job.concurrency``
     - ``2``
     - Nombre de workers parallèles pour la tâche d'indexation
   * - ``content_chunker.job.bulk_size``
     - ``20``
     - Nombre de documents récupérés et écrits par lot
   * - ``content_chunker.job.max_documents_per_run``
     - ``-1``\ (illimité)
     - Nombre maximal de documents traités par exécution de la tâche. Toute valeur ``0`` ou
       inférieure est traitée comme illimitée
   * - ``content_chunker.job.retry_failed``
     - ``false``
     - Lorsque défini sur ``true``, les documents dont l'exécution précédente s'est terminée
       avec ``content_chunk_status=fail`` sont également inclus dans la cible de traitement de
       l'exécution suivante. Il n'y a ni nouvelle tentative automatique ni suivi du nombre de
       tentatives ; le flux de travail prévu consiste à corriger la cause sous-jacente, puis à
       activer temporairement ce réglage pour réessayer
   * - ``content_chunker.chat.top_k``
     - ``3``
     - Nombre de chunks sélectionnés lorsque le mode de recherche IA génère une réponse
   * - ``content_chunker.search.enabled``
     - ``false``
     - Intégration au Rank Fusion pour la recherche sémantique (**l'activation nécessite un
       redémarrage**)
   * - ``content_chunker.search.min_score``
     - (non défini)
     - Similarité cosinus minimale (0-1) requise pour qu'un résultat soit inclus. Aucune coupure
       si non défini. En mode ``ann``, lorsque ``search.knn.space_type`` vaut autre chose que
       ``cosinesimil``, aucun seuil fondé sur le cosinus ne peut être défini : la coupure est
       ignorée avec un avertissement
   * - ``content_chunker.search.knn.method``
     - ``hnsw``
     - Méthode d'index ANN. ``hnsw`` est actuellement la seule valeur acceptée ; toute autre
       valeur entraîne un retour à ``hnsw`` avec un avertissement (reflétée dans le mapping ; la
       modifier nécessite de recréer l'index)
   * - ``content_chunker.search.knn.engine``
     - ``lucene``
     - Moteur ANN. Seuls ``lucene`` ou ``faiss`` sont acceptés (voir Prérequis ci-dessus) ; toute
       autre valeur entraîne un retour à ``lucene`` avec un avertissement (reflété dans le
       mapping ; le modifier nécessite de recréer l'index)
   * - ``content_chunker.search.knn.space_type``
     - ``cosinesimil``
     - Espace de distance. Seuls ``cosinesimil``, ``innerproduct`` ou ``l2`` sont acceptés ; toute
       autre valeur entraîne un retour à ``cosinesimil`` avec un avertissement (reflété dans le
       mapping ; le modifier nécessite de recréer l'index)
   * - ``content_chunker.search.knn.k``
     - ``100``
     - Nombre de voisins récupérés par requête ANN (agrandi automatiquement pour la pagination
       profonde)
   * - ``content_chunker.search.knn.param.ef_search``
     - (non défini)
     - Le paramètre ``ef_search`` pour les requêtes ANN

.. note::

   Avec ``content_chunker.length.boundary.enabled=true`` (valeur par défaut),
   ``content_chunker.length.chunk_size`` devient un objectif plutôt qu'un plafond strict : chaque
   coupure se déplace vers la rupture la plus appropriée dans la fenêtre de recherche, en donnant
   la priorité à un saut de ligne ou une fin de phrase sur un séparateur de proposition ou un
   espace, puis à ceux-ci sur un changement d'écriture. Seul le point de coupure est déplacé ;
   aucun caractère n'est perdu, si bien que la concaténation des chunks d'un document reproduit
   toujours son contenu exact. La recherche vers l'avant peut dépasser ``chunk_size`` d'au plus
   ``content_chunker.length.boundary.lookahead_percent``. Un second dépassement, indépendant,
   pouvant aller jusqu'à 32 caractères peut se produire lorsqu'une coupure tomberait autrement au
   milieu d'un cluster de graphèmes (une marque combinante, un sélecteur de variante ou une
   séquence d'emojis liée par un jointeur de largeur nulle ; ZWJ) — celui-ci ignore
   ``lookahead_percent`` et peut survenir même lorsqu'il vaut ``0``. Les deux types de
   dépassement ne se produisent jamais sur la même coupure ; le pire cas avec les valeurs par
   défaut est d'environ 841 caractères. Les chunks peuvent aussi être plus courts d'au plus
   ``lookback_percent``, si bien qu'un document peut produire légèrement plus de chunks qu'avant
   (voir ``content_chunker.max_chunks_per_document``). Définissez
   ``content_chunker.length.boundary.enabled=false``, ou les deux pourcentages à ``0``, pour
   restaurer le comportement précédent à longueur fixe exacte.

.. note::

   Les paramètres HNSW ``m`` et ``ef_construction`` sont codés en dur dans ``doc.json``
   (``m=16`` / ``ef_construction=100``) et ne peuvent pas être modifiés via la configuration.

Réglages de connexion pour le fournisseur opensearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Réglages de connexion pour le fournisseur intégré ``opensearch`` (OpenSearch ML Commons).
Ceux-ci sont définis dans le même fichier ``system.properties`` que ci-dessus.

.. list-table::
   :header-rows: 1
   :widths: 50 20 30

   * - Propriété
     - Défaut
     - Description
   * - ``content_chunker.embedding.opensearch.model.id``
     - (requis)
     - ID du modèle déjà déployé sur ML Commons
   * - ``content_chunker.embedding.opensearch.api.url``
     - Adresse du moteur de recherche
     - Point de terminaison de l'API ML Commons. Si non défini, utilise par défaut le moteur de
       recherche déjà utilisé par |Fess| (par ex. ``http://localhost:9200``)
   * - ``content_chunker.embedding.opensearch.username`` / ``password``
     - Identifiants du moteur de recherche
     - Si non défini, utilise par défaut les identifiants employés pour la connexion au moteur
       de recherche — mais uniquement tant que ``api.url`` n'est pas configuré (c'est-à-dire que
       la cible est le même cluster que celui déjà utilisé par |Fess|). Une fois ``api.url``
       défini, ce repli ne s'applique plus.
   * - ``content_chunker.embedding.opensearch.timeout``
     - ``60000``
     - Délai d'expiration de la requête (ms)
   * - ``content_chunker.embedding.opensearch.connect.timeout``
     - ``5000``
     - Délai d'expiration de connexion (ms)
   * - ``content_chunker.embedding.opensearch.retry.max``
     - ``3``
     - Nombre de nouvelles tentatives pour les erreurs transitoires (429, 5xx, etc.)
   * - ``content_chunker.embedding.opensearch.retry.base.delay.ms``
     - ``2000``
     - Délai de base entre les tentatives (ms)
   * - ``content_chunker.embedding.opensearch.availability.check.interval``
     - ``60``
     - Intervalle entre les vérifications de disponibilité du fournisseur (secondes)
   * - ``content_chunker.embedding.opensearch.document.prefix`` / ``query.prefix``
     - (vide)
     - Préfixe ajouté au texte du document/de la requête avant l'embedding

.. warning::

   Le contenu de ``system.properties`` est consultable sur l'écran d'administration
   **Informations système > Informations de configuration**, dans le panneau **Propriétés de
   l'application**. ``content_chunker.embedding.opensearch.password`` y est masqué sous la forme
   ``XXXXXXXX``, mais ``username`` s'affiche tel quel. De plus, les valeurs fournies via
   ``-Dfess.system.<key>`` apparaissent **sans masquage** dans le panneau **Propriétés du
   système** du même écran : renseignez donc les identifiants dans ``system.properties`` plutôt
   que dans les options de démarrage.

Autres fournisseurs (ollama / openai / gemini)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le fournisseur ``ollama`` (plugin ``fess-llm-ollama``) utilise le même style de réglages sous le
préfixe ``content_chunker.embedding.ollama.`` (``api.url`` vaut par défaut
``http://localhost:11434``, ``model`` vaut par défaut ``embeddinggemma``, et
``document.prefix`` / ``query.prefix`` valent par défaut respectivement ``title: none | text:`` /
``task: search result | query:``). Si vous utilisez un modèle de la famille
``nomic-embed-text``, définissez explicitement ``document.prefix`` / ``query.prefix`` sur
``search_document:`` / ``search_query:``. Ces préfixes sont concaténés tels quels au texte à
vectoriser (les espaces environnants ne sont pas supprimés) : les valeurs par défaut ci-dessus
comme ``search_document:`` / ``search_query:`` comportent donc toutes **une espace finale**.
Pensez à cette espace de séparation si vous définissez un préfixe vous-même.
Les fournisseurs ``openai`` et ``gemini`` se
configurent de la même manière, sous les préfixes ``content_chunker.embedding.openai.`` et
``content_chunker.embedding.gemini.`` respectivement. Consultez la documentation de chaque plugin
pour la liste complète des réglages.

Procédure de configuration (exemple avec le fournisseur opensearch)
========================================================================

Cette section présente un exemple de configuration utilisant le fournisseur intégré
``opensearch`` (ML Commons).

1. Déployer le modèle d'embedding
------------------------------------

Enregistrez et déployez un modèle d'embedding sur OpenSearch ML Commons. Sur un cluster à nœud
unique, vous devez d'abord appliquer le réglage suivant.

.. code-block:: bash

    curl -XPUT "http://localhost:9200/_cluster/settings" \
         -H "Content-Type: application/json" -d '
    {"persistent": {"plugins.ml_commons.only_run_on_ml_node": false}}'

Enregistrez et déployez le modèle (exemple : un modèle d'embedding de phrases à 384
dimensions) :

.. code-block:: bash

    # Enregistrer le modèle (récupérer model_id depuis le task_id de la réponse)
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/_register" \
         -H "Content-Type: application/json" -d '
    {
      "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
      "version": "1.0.2",
      "model_format": "TORCH_SCRIPT"
    }'

    # Vérifier l'achèvement de la tâche et récupérer model_id (model_id est renvoyé une fois que state vaut COMPLETED)
    curl "http://localhost:9200/_plugins/_ml/tasks/<task_id>"

    # Déployer
    curl -XPOST "http://localhost:9200/_plugins/_ml/models/<model_id>/_deploy"

    # Vérifier le statut : model_state doit être DEPLOYED
    curl "http://localhost:9200/_plugins/_ml/models/<model_id>"

.. note::

   Un modèle encore au statut ``REGISTERED`` ne peut pas être utilisé. Assurez-vous de le
   déployer et de confirmer que ``model_state`` passe à ``DEPLOYED``.

2. Configurer |Fess|
-----------------------

``app/WEB-INF/conf/system.properties`` (``/etc/fess/system.properties`` pour les paquets RPM/DEB,
``/opt/fess/system.properties`` sous Docker ; tout ce qui suit va dans le même fichier) ::

    content_chunker.enabled=true
    content_chunker.embedding.name=opensearch
    content_chunker.embedding.dimension=384
    content_chunker.embedding.opensearch.model.id=<model_id>

Si vous souhaitez également utiliser la recherche sémantique, ajoutez aussi ce qui suit ::

    content_chunker.search.enabled=true

Redémarrez |Fess| après avoir effectué ces changements.

3. Recréer l'index (lors de l'activation sur un déploiement existant)
----------------------------------------------------------------------

Le mapping du champ ``content_chunk_vector`` — y compris la dimension et les réglages de méthode
ANN que vous avez configurés — est appliqué **au moment où l'index** ``fess.search`` **est
recréé**.

- **Nouvelles installations** : si vous appliquez les réglages ci-dessus à
  ``system.properties`` avant de démarrer |Fess| pour la première fois, le mapping correct est
  appliqué automatiquement lors de la première création de l'index ; cette étape est donc
  inutile.
- **Si un index existe déjà** (c'est-à-dire si vous avez déjà démarré |Fess| au moins une
  fois) : l'index en cours d'exécution n'adopte pas automatiquement le nouveau mapping, et un
  mapping existant ne peut pas être modifié après coup. Recréez l'index comme suit :

  Ouvrez **Informations système > Maintenance**, et sous **Réindexation**, exécutez-la avec
  l'option **Remplacer les alias** activée.

  Vous pouvez ensuite confirmer que l'index recréé comporte ``index.knn: true`` dans ses réglages
  d'index, ainsi qu'un mapping ``content_chunk_vector`` portant la dimension et les réglages de
  méthode ANN configurés (``index.knn`` est un réglage d'index alors que les réglages de méthode
  ANN font partie du mapping : les deux ne s'appliquent pas au même endroit).

.. warning::

   La réindexation s'exécute comme une opération asynchrone en arrière-plan, et l'interface
   d'administration n'affiche aucune notification de fin. ``_cat/indices`` montre seulement que le
   nouvel index existe (état, nombre de documents, etc.) — pas vers quel index pointent les alias.
   Avant de passer à la tâche d'indexation décrite ci-dessous, consultez plutôt ``_cat/aliases`` et
   vérifiez que ``fess.search`` et ``fess.update`` pointent tous deux vers le nouvel index ; le
   journal de |Fess| ne consigne un avertissement qu'en cas d'échec, donc un journal silencieux
   n'est pas une preuve de réussite, seulement l'absence d'un échec connu. L'ancien index (l'index
   physique vers lequel pointait auparavant l'alias ``fess.search``, nommé ``fess.<timestamp>``)
   n'est pas supprimé automatiquement ; supprimez-le manuellement une fois que vous n'en avez plus
   besoin. Tant que les deux index existent, prévoyez une utilisation disque des index environ
   deux fois plus importante que d'habitude.

4. Activer la tâche d'indexation
-------------------------------------

Le chunking et la génération des embeddings sont effectués par la tâche du planificateur
**Content Chunk Vector Indexer** (ID : ``content-chunk-vector-indexer`` ; désactivée par défaut ;
planifiée à ``0 13 * * *``).

Activez cette tâche dans **Système > Planificateur**, puis exécutez-la une fois avec **Démarrer
maintenant**. Ensuite, les documents non traités sont pris en charge selon la planification
configurée (par défaut tous les jours à 13:00), indépendamment de la fin du crawl. Cette tâche
n'étant pas chaînée à la tâche de crawl, si vous souhaitez que le traitement suive immédiatement
un crawl, planifiez-la après l'heure de fin prévue de la tâche de crawl.

.. note::

   Dans un déploiement multi-nœuds, nous recommandons d'épingler cette tâche pour qu'elle
   s'exécute sur exactement un nœud. L'exécuter sur chaque nœud simultanément ne compromet pas
   l'exactitude, mais chaque nœud traite et embed les mêmes documents de manière redondante, ce
   qui multiplie la charge et le coût chez votre fournisseur d'embedding par le nombre de nœuds.

   L'épinglage nécessite **les deux** réglages suivants — l'un sans l'autre n'épingle pas la
   tâche.

   1. **Sur le nœud où vous souhaitez exécuter la tâche** : définissez
      ``scheduler.target.name=<un identifiant>`` dans
      ``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` pour
      les paquets RPM/DEB, ou via ``-Dfess.config.scheduler.target.name=<un identifiant>``), puis
      redémarrez ce nœud. (La valeur par défaut est vide ; laissez tous les autres nœuds à la
      valeur par défaut.)
   2. Dans l'interface d'administration, sous **Système > Planificateur**, ouvrez la tâche
      Content Chunk Vector Indexer et changez son champ **Cible** de ``all`` vers le même
      identifiant que celui défini à l'étape 1, puis enregistrez.

   Consultez :doc:`../admin/scheduler-guide` pour savoir ce que signifie le champ **Cible**.
   Définir uniquement ``scheduler.target.name`` n'épingle pas la tâche si le champ **Cible**
   reste sur ``all`` : **elle ne sera pas épinglée**. ``all`` est traité comme une valeur
   spéciale qui correspond toujours ; l'étape 1 seule ou l'étape 2 seule ne suffit donc pas —
   vous devez effectuer les deux.

.. warning::

   Une fois la tâche épinglée, **Démarrer maintenant** doit lui aussi être déclenché **depuis
   l'interface d'administration du nœud sur lequel vous avez défini l'identifiant à l'étape 1**.
   Si vous cliquez sur **Démarrer maintenant** depuis un autre nœud, l'écran affiche bien un
   message indiquant que la tâche a démarré, mais celle-ci n'est pas exécutée en raison de la
   non-correspondance du champ **Cible** (le journal de ce nœud se contente d'une ligne
   ``Ignoring job`` au niveau INFO).

5. Vérifier l'état du traitement
-------------------------------------

Vous pouvez vérifier le résultat pour chaque document dans son champ ``content_chunk_status``.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Valeur
     - Signification
   * - (champ absent)
     - Pas encore traité (sera pris en charge lors de la prochaine exécution de la tâche). Les
       documents reviennent également à cet état après un nouveau crawl
   * - ``done``
     - Chunking et génération de vecteurs terminés
   * - ``chunked``
     - Chunking seul terminé (mode chunking seul). Cet état survient lorsque
       ``embedding.name=none``, mais aussi lorsque le plugin du fournisseur indiqué dans
       ``embedding.name`` n'est pas installé
   * - ``skipped``
     - Traitement ignoré (par ex. ``max_chunks_per_document`` dépassé)
   * - ``fail``
     - Échec du traitement (vérifiez les journaux)

Vous pouvez vérifier la répartition des statuts en interrogeant directement le moteur de
recherche ::

    curl -XPOST "http://localhost:9200/fess.search/_search" \
         -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

Grâce à l'option ``missing``, les documents dépourvus de ``content_chunk_status`` (autrement dit
non traités) sont regroupés dans un bucket portant la clé ``pending``.

Comportement de la recherche sémantique
==========================================

Définir ``content_chunker.search.enabled=true`` enregistre le moteur de recherche sémantique
auprès du Rank Fusion, qui fusionne ensuite les résultats de la recherche par mots-clés avec ceux
de la recherche vectorielle. (Voir :doc:`rank-fusion` pour le fonctionnement du Rank Fusion.)
Au moment de la recherche, ``content_chunker.enabled`` est également consulté : si
``content_chunker.enabled=false`` ou ``content_chunker.embedding.name=none``, la recherche
sémantique n'est pas exécutée, même lorsque le moteur est enregistré (cette évaluation ayant lieu
à chaque requête, aucun redémarrage n'est nécessaire).

.. warning::

   Le moteur de recherche sémantique étant enregistré au démarrage, **l'activation nécessite un
   redémarrage**. La désactivation (remettre la valeur à ``false``) est évaluée par requête et
   prend donc effet immédiatement.

Mode exact et mode ann
-------------------------

La méthode de recherche est choisie automatiquement en fonction de l'état de l'index.

.. list-table::
   :header-rows: 1
   :widths: 12 44 44

   * - Mode
     - Condition
     - Caractéristiques
   * - ``ann``
     - Un index disposant des réglages ``index.knn`` et de méthode ANN
     - Recherche approximative du plus proche voisin utilisant HNSW. Adapté aux grands index
   * - ``exact``
     - Tout le reste (un index auquel il manque soit ``index.knn``, soit les réglages de méthode
       ANN, y compris lorsque la détection de l'état de l'index échoue)
     - Calcul exact de similarité cosinus sur chaque vecteur. Adapté aux index de petite à
       moyenne taille

Tout index ``fess.search`` nouvellement créé sous |Fess| 15.8 dispose toujours des réglages
``index.knn`` et de méthode ANN, quelle que soit la valeur de
``content_chunker.search.enabled`` — le mode ``ann`` est donc normalement toujours utilisé. Le
mode ``exact`` est un repli pour les index plus anciens créés avant l'existence de ce mécanisme.
Les réglages k-NN ne pouvant pas être ajoutés a posteriori à un index existant, faire passer un
index en mode ``exact`` au mode ``ann`` nécessite de recréer l'index (voir
:ref:`semantic-search-migration`). Le résultat de cette détection étant mis en cache pendant
60 secondes, il faut compter jusqu'à 60 secondes après la recréation de l'index pour que le
changement soit pris en compte.

Seuil de score
-----------------

Définir ``content_chunker.search.min_score`` sur une similarité cosinus (0-1) exclut des
résultats de la recherche sémantique les documents dont même le chunk le plus similaire
n'atteint pas cette valeur (le score d'un document étant celui de son meilleur chunk, la coupure
s'applique au niveau du document et non du chunk). Utilisez ce réglage pour maîtriser le nombre
de résultats lorsque des requêtes sans chevauchement de vocabulaire correspondent de manière trop
large ::

    content_chunker.search.min_score=0.4

La valeur configurée est interprétée comme une similarité cosinus dans les deux modes, ``exact``
comme ``ann`` (elle est convertie en interne vers l'échelle de score propre à chaque mode).

.. note::

   Cette coupure ne s'applique que lorsque ``content_chunker.search.knn.space_type`` vaut
   ``cosinesimil`` (la valeur par défaut). Sur un index en mode ``ann`` configuré avec
   ``innerproduct`` ou ``l2``, aucune similarité cosinus ne peut être définie : la coupure est
   ignorée après consignation d'un unique avertissement dans le journal.

Limitations
-------------

- **La recherche sémantique est ignorée pour les requêtes contenant une syntaxe de recherche**,
  et seule la recherche par mots-clés est exécutée. La détection porte sur la chaîne de requête
  **après** son assemblage, et se déclenche dès que celle-ci contient l'un des éléments
  suivants : ``"`` ``(`` ``)`` ``:`` ``[`` ``]`` ``{`` ``}`` ``^`` ``~`` ``*`` ``?`` ``\``,
  ``&&``, ``||``, un ``+`` ou un ``-`` en début de chaîne ou juste après une espace, ou encore
  les mots en majuscules ``AND`` / ``OR`` / ``NOT`` / ``TO``. Les opérations suivantes sont donc
  elles aussi ignorées, même si l'utilisateur n'a saisi aucune syntaxe de recherche.

  - La sélection d'un label (``label:"..."`` est ajouté en interne)
  - La définition d'un critère de tri (``sort:...`` est ajouté en interne)
  - Le filtrage par facette (``filetype:...`` et similaires sont ajoutés en interne)
  - La recherche de phrase, les termes exclus, le type de fichier, le site et la plage de dates
    de la recherche avancée
  - Un terme de recherche auquel des requêtes associées sont attachées (développé en interne en
    ``("A" OR "B")``)

  Le ``?`` ASCII faisant partie des caractères détectés, une phrase en langage naturel qui se
  termine par un point d'interrogation ASCII est elle aussi ignorée (le point d'interrogation
  pleine chasse ``？`` n'est pas concerné).
- Elle est également ignorée lorsqu'elle est combinée à une recherche par géolocalisation (un
  filtre géo) ou à une recherche de documents similaires.
- Sur les pages profondes, le Rank Fusion lui-même est désactivé et les résultats proviennent
  uniquement de la recherche par mots-clés. La limite est déterminée par
  ``rank.fusion.window_size`` (par défaut ``200``), ce qui correspond, avec les valeurs par
  défaut, aux résultats à partir du 101e.
- Si le fournisseur d'embedding est inaccessible ou qu'une erreur de recherche survient, |Fess|
  bascule automatiquement vers des résultats basés uniquement sur les mots-clés (la recherche
  elle-même n'échoue jamais de ce fait).
- Le contrôle d'accès basé sur les rôles et les hôtes virtuels s'applique également aux résultats
  de la recherche sémantique.

Intégration avec le mode de recherche IA
============================================

Lorsque le mode de recherche IA (:doc:`rag-chat`, ``rag.chat.enabled=true``) est activé, pour les
documents dont le ``content_chunk_status`` est ``done``, la génération de réponse calcule la
similarité avec chaque chunk et n'utilise que les ``content_chunker.chat.top_k`` chunks les plus
pertinents (par défaut : ``3``) comme contexte du LLM.

Le texte qui fait alors l'objet de l'embedding n'est pas l'énoncé de l'utilisateur, mais **la
requête de recherche générée par le LLM lors de la phase de détermination de l'intention** (en
cas de nouvelle recherche, c'est la requête régénérée qui est utilisée). Lorsqu'aucune requête de
recherche n'est générée — par exemple lorsque l'utilisateur demande le résumé d'un document —,
aucune sélection de chunks n'a lieu.

Ainsi, même pour les documents longs, seules les parties pertinentes sont transmises au LLM, ce
qui peut améliorer la précision des réponses et réduire l'utilisation de tokens. Pour les
documents dont le ``content_chunk_status`` est ``chunked`` (les chunks existent, mais pas les
vecteurs), la sélection des chunks s'appuie sur la correspondance de mots-clés (surlignage) au
lieu du calcul de similarité. Les documents en ``skipped`` / ``fail`` ainsi que les documents non
traités continuent d'utiliser le corps complet (ou un extrait surligné) comme auparavant.

Ce comportement est indépendant de ``content_chunker.search.enabled``, mais il nécessite que
``content_chunker.enabled`` soit activé. Notez également que le texte obtenu en concaténant les
chunks sélectionnés est lui aussi tronqué à ``rag.chat.content.fulltext.max.length`` (par défaut
``3000``) : augmenter ``content_chunker.chat.top_k`` ou ``content_chunker.length.chunk_size`` ne
permet donc pas de dépasser cette limite dans ce qui est transmis au LLM.

.. _semantic-search-migration:

Migration depuis la version 15.7 ou antérieure
==================================================

Si vous mettez à niveau |Fess| depuis la version 15.7 ou antérieure, votre situation correspond à
l'un des quatre cas ci-dessous, selon la façon dont vous utilisez actuellement ces
fonctionnalités. Suivez les instructions correspondant à votre cas.

Nouvelles installations
--------------------------

Aucun travail supplémentaire n'est nécessaire. Si vous souhaitez utiliser la recherche
vectorielle, configurez simplement ``system.properties`` selon la section *Référence de
configuration* de cette page avant de démarrer |Fess| pour la première fois ; le mapping correct
est appliqué automatiquement lors de la première création de l'index. (Voir *Procédure de
configuration* ci-dessus pour les étapes concrètes.)

.. note::

   Si vous avez déjà démarré |Fess| au moins une fois (c'est-à-dire que l'index existe déjà),
   suivez plutôt l'un des cas *utilisateurs existants* ci-dessous.

Utilisateurs existants ne souhaitant pas la recherche vectorielle
-----------------------------------------------------------------------

Aucune action n'est nécessaire. ``content_chunker.enabled`` et
``content_chunker.search.enabled`` valent tous deux ``false`` par défaut, de sorte que vos
résultats de recherche et le comportement de l'index existant restent inchangés après la mise à
niveau. La nouvelle tâche du planificateur **Content Chunk Vector Indexer** est enregistrée
automatiquement au démarrage, mais comme elle est désactivée par défaut, elle ne s'exécute
jamais, et le moteur de recherche sémantique n'est jamais enregistré auprès du Rank Fusion.
(Cette tâche étant enregistrée à chaque démarrage, la supprimer depuis l'interface
d'administration la recrée, désactivée, au démarrage suivant.)

.. note::

   Même si vous n'utilisez pas la recherche vectorielle, toute **création** d'index sous |Fess|
   15.8 ou ultérieur (réindexation comprise) applique le mapping contenant
   ``content_chunk_vector`` (de type ``knn_vector``) ainsi que ``index.knn: true``. Sur une
   configuration où OpenSearch n'a pas le plugin k-NN installé, la création de l'index échoue à
   ce moment-là. Voir *Prérequis* sur cette page pour plus de détails.

Utilisateurs existants souhaitant activer la recherche vectorielle
------------------------------------------------------------------------

L'index en cours d'exécution n'adopte pas automatiquement le nouveau mapping, les étapes
suivantes sont donc requises.

1. Appliquez les réglages à ``system.properties`` comme décrit dans *Référence de configuration*
   sur cette page (voir *Procédure de configuration* ci-dessus pour les étapes concrètes avec le
   fournisseur opensearch).
2. Redémarrez |Fess|.
3. Dans l'interface d'administration, exécutez la **Réindexation** sous **Informations système >
   Maintenance** avec l'option **Remplacer les alias** activée. Cette opération s'exécute en
   arrière-plan sans notification de fin. ``_cat/indices`` montre seulement que le nouvel index
   existe, pas si les alias ont basculé — consultez plutôt ``_cat/aliases`` et vérifiez que
   ``fess.search``/``fess.update`` pointent vers le nouvel index (le journal de |Fess| n'avertit
   qu'en cas d'échec, le silence n'est donc pas une preuve de réussite). L'ancien index n'est pas
   supprimé automatiquement (supprimez-le manuellement une fois que vous n'en avez plus besoin),
   et l'utilisation disque des index double environ jusqu'à ce que vous le fassiez.
4. Une fois seulement que vous avez confirmé que le remplacement des alias ci-dessus est terminé,
   activez et exécutez la tâche Content Chunk Vector Indexer sous **Système > Planificateur**
   (inutile de relancer un crawl : la tâche lit ``content`` depuis le ``_source`` de l'index
   existant pour le découper en chunks et l'embedder).

.. note::

   Si vous appliquez dès l'étape 1 le réglage ``content_chunker.search.enabled=true``, alors
   entre le redémarrage de l'étape 2 et l'achèvement de l'étape 4, chaque recherche calcule
   l'embedding de la requête sans que cela se répercute sur les résultats. Avec un fournisseur
   facturé à l'usage comme ``openai`` ou ``gemini``, appliquez
   ``content_chunker.search.enabled=true`` et redémarrez seulement une fois l'étape 4 terminée.

Si vous utilisiez le plugin fess-webapp-semantic-search
------------------------------------------------------------

Le plugin ``fess-webapp-semantic-search``, qui fournissait la recherche sémantique dans |Fess|
15.7 et versions antérieures, a été intégré au cœur en 15.8 et est désormais **inutile
(obsolète)**. En plus des étapes décrites dans *Utilisateurs existants souhaitant activer la
recherche vectorielle* ci-dessus, vous devez également effectuer ce qui suit.

1. **Supprimer le plugin** : supprimez ``fess-webapp-semantic-search-*.jar`` de
   ``app/WEB-INF/plugin/`` (sous Docker, excluez-le de ``FESS_PLUGINS``).

2. **Supprimer les anciens réglages** : supprimez chaque option de démarrage
   ``-Dfess.semantic_search.*``. De plus, si vous aviez spécifié
   ``-Drank.fusion.searchers=default,semantic`` pour l'ancien plugin, supprimez-le également. Le
   laisser en place exclut le nouveau moteur de recherche sémantique (``semantic_chunk``) du Rank
   Fusion et consigne un avertissement au démarrage.

3. **Détacher l'ancien pipeline d'ingestion** : lorsque ``-Dfess.semantic_search.pipeline``
   était configuré, l'ancien plugin inscrivait ``default_pipeline`` (un pipeline d'ingestion pour
   la recherche neuronale) dans les réglages de l'index au moment de la création de celui-ci.
   **Supprimer le plugin ne supprime pas le pipeline** — il reste attaché à l'index et continue
   de s'exécuter —, vous devez donc le détacher **avant** la réindexation décrite dans
   *Utilisateurs existants souhaitant activer la recherche vectorielle*. Le nouvel index issu de
   la réindexation ne porte pas ce réglage : l'exécuter après coup n'aurait aucun effet. Repérez
   avec ``_cat/aliases`` l'index ``fess.<timestamp>`` vers lequel pointe ``fess.search``, et
   ciblez l'index physique plutôt que l'alias ::

       curl -XPUT "http://localhost:9200/fess.<timestamp>/_settings" \
            -H "Content-Type: application/json" -d '
       {"index": {"default_pipeline": "_none"}}'

   Détacher le réglage de l'index ne supprime pas le pipeline d'ingestion lui-même, qui reste
   présent côté moteur de recherche. Supprimez-le si vous ne comptez plus l'utiliser ::

       curl -XDELETE "http://localhost:9200/_ingest/pipeline/<nom_du_pipeline>"

4. **Ajouter les nouveaux réglages** : configurez ``content_chunker.*`` dans
   ``system.properties`` comme décrit dans *Référence de configuration* sur cette page. Si vous
   continuez à utiliser votre modèle ML Commons existant, définissez
   ``content_chunker.embedding.name=opensearch`` et placez son ``model_id`` existant dans
   ``content_chunker.embedding.opensearch.model.id``.

5. **Recréer l'index et exécuter la tâche** : le champ vectoriel que stockait l'ancien plugin
   (``content_vector`` dans la configuration par défaut) et le champ ``content_chunk_vector``
   qu'utilise la nouvelle fonctionnalité du cœur sont des champs distincts ; les anciens vecteurs
   ne peuvent donc pas être exploités par la nouvelle fonctionnalité. En revanche, la
   réindexation recopiant ``_source`` tel quel, ces anciens vecteurs sont bel et bien dupliqués
   dans le nouvel index, où ils continuent de consommer de l'espace disque via le mapping
   dynamique. Nous recommandons de les supprimer **avant** la réindexation (adaptez le nom du
   champ si vous l'aviez modifié) ::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_vector"}},
         "script": {"source": "ctx._source.remove(\"content_vector\")"}
       }'

   Exécutez ensuite la **Réindexation** sous **Informations système > Maintenance**, puis activez
   et exécutez la tâche Content Chunk Vector Indexer pour régénérer les vecteurs.

Remarques
===========

Changer de modèle d'embedding (dimension)
--------------------------------------------

Pour passer à un modèle d'embedding avec une dimension différente, suivez cet ordre.

1. Supprimez les anciens vecteurs existants. Si des vecteurs de l'ancienne dimension subsistent
   au moment de la réindexation, le nouveau mapping ne peut pas les accepter et les documents
   concernés ne sont pas copiés dans le nouvel index, sans que le traitement s'interrompe pour
   autant. |Fess| ne vérifiant que le statut HTTP de la réindexation, aucune erreur n'apparaît
   dans l'interface d'administration alors même que des documents ont disparu ::

       curl -XPOST "http://localhost:9200/fess.search/_update_by_query" \
            -H "Content-Type: application/json" -d '
       {
         "query": {"exists": {"field": "content_chunk_status"}},
         "script": {"source": "ctx._source.remove(\"content_chunk_vector\"); ctx._source.remove(\"content_chunk_status\")"}
       }'

   .. note::

      Vous pouvez tout aussi bien cibler ``fess.update`` (l'alias de mise à jour depuis lequel la
      réindexation lit les documents). Notez par ailleurs que cette opération laisse le champ
      ``content`` sous la forme d'un tableau de chunks. Celui-ci sera reconcaténé puis redécoupé
      lors de la prochaine exécution de la tâche : si ``content_chunker.length.overlap`` est
      différent de 0, les parties chevauchantes se retrouveront comptées deux fois dans le
      nouveau découpage. Si cela vous pose problème, relancez un crawl sur les documents
      concernés.

2. Modifiez ``content_chunker.embedding.dimension`` et le réglage du modèle pour votre
   fournisseur.
3. Recréez l'index en suivant *3. Recréer l'index (lors de l'activation sur un déploiement
   existant)* dans *Procédure de configuration*, puis relancez la tâche d'indexation.

Utilisation du disque
------------------------

Les vecteurs de chunks sont conservés dans ``_source`` en plus des structures de l'index de
recherche, de sorte que chaque document consomme un espace disque supplémentaire proportionnel à
son nombre de chunks multiplié par la dimension du vecteur. Si l'espace disque devient un
problème, ajustez ``content_chunker.length.chunk_size`` ou
``content_chunker.max_chunks_per_document``.

Mode chunking seul
---------------------

Définir ``content_chunker.embedding.name=none`` effectue uniquement le chunking, sans générer de
vecteurs d'embedding (``content_chunk_status`` devient ``chunked``). Cela vous permet d'exécuter
le chunking à l'avance, avant que votre fournisseur d'embedding ne soit prêt ; une fois qu'un
fournisseur est configuré ultérieurement et que la tâche est relancée, des vecteurs sont générés
pour les chunks déjà stockés, sans les re-découper.

Réglages mémoire pour les corpus volumineux
------------------------------------------------

La JVM enfant de la tâche d'indexation est démarrée avec ``jvm.chunk.options`` dans
``fess_config.properties`` (options JVM incluant par défaut ``-Xms128m -Xmx1g``). Comme
``content_chunker.job.max_documents_per_run`` est illimité par défaut, une seule exécution
conserve tous les ID de documents en attente en mémoire. Un ID de document est un condensat
SHA-512 (128 caractères) et occupe environ 200 octets dans le tas ; le traitement des chunks
lui-même consomme en outre de 200 à 250 Mo. Le seuil réel se situe donc **au-delà de 1 à
2 millions de documents** : augmentez alors la valeur de ``-Xmx`` dans ``jvm.chunk.options``, ou
donnez une valeur finie à ``content_chunker.job.max_documents_per_run`` pour découper le
traitement en plusieurs exécutions. ``jvm.chunk.options`` se redéfinit dans
``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` pour les
paquets RPM/DEB) ; voir :doc:`setup-memory` pour la configuration des options JVM.

Cette même valeur par défaut illimitée a aussi une conséquence financière avec un fournisseur
d'embedding facturé à l'usage (``openai``, ``gemini``) : la première exécution de la tâche
d'indexation génère les embeddings de tout le corpus existant en une seule fois et facture le
tout d'un coup. Définissez une valeur finie pour ``content_chunker.job.max_documents_per_run``
afin de répartir ce coût sur plusieurs exécutions.

Références
============

- :doc:`rank-fusion` - Configuration du Rank Fusion (recherche hybride)
- :doc:`rag-chat` - Configuration du mode de recherche IA
- :doc:`llm-overview` - Aperçu de l'intégration LLM
- :doc:`llm-ollama` - Configuration d'Ollama
- :doc:`setup-memory` - Réglages mémoire de la JVM
- :doc:`../install/upgrade` - Procédure de mise à niveau
