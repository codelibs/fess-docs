======================================================================
Vue d'ensemble du mode de recherche IA (RAG) et de l'intégration LLM
======================================================================

Vue d'ensemble
==============

|Fess| prend en charge la fonctionnalité de mode de recherche IA (RAG : Retrieval-Augmented Generation) utilisant
les grands modèles de langage (LLM). Cette fonctionnalité permet aux utilisateurs d'obtenir des informations
sous forme de dialogue avec un assistant IA basé sur les résultats de recherche, en répondant à des questions en langage naturel directement à partir de votre index de recherche d'entreprise, avec citation des sources.

La fonctionnalité d'intégration LLM est fournie sous forme de plugins ``fess-llm-*``. Installez le plugin correspondant au fournisseur LLM que vous souhaitez utiliser.

Le mode de recherche IA récupère les documents via le pipeline de recherche standard de |Fess| (rank fusion), et non via un index vectoriel dédié ; par défaut, il s'agit d'une recherche par mots-clés (BM25). Comme ce pipeline standard est réutilisé, si vous activez la recherche sémantique intégrée au cœur (chunking de contenu + recherche vectorielle), son moteur de recherche sémantique participe au rank fusion pour toutes les recherches, y compris l'étape de récupération du mode de recherche IA ; aucune configuration spécifique au mode de recherche IA n'est nécessaire pour que le moteur de recherche sémantique y participe. Vous pouvez toutefois ajuster le nombre de chunks transmis à la génération de la réponse via ``content_chunker.chat.top_k``. Pour plus de détails, consultez :doc:`rank-fusion` et :doc:`search-semantic`.

Fournisseurs pris en charge
============================

|Fess| prend en charge les fournisseurs LLM suivants.

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Fournisseur
     - Valeur de configuration
     - Plugin
     - Description
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - Serveur LLM open source fonctionnant en local. Permet d'exécuter des modèles tels que Llama, Mistral, Gemma. Configuration par défaut.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - API cloud d'OpenAI. Permet d'utiliser des modèles comme GPT-5.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - API cloud de Google. Permet d'utiliser les modèles Gemini.

Comparaison des fournisseurs
------------------------------

.. list-table::
   :header-rows: 1

   * - Fournisseur (``rag.llm.name``)
     - Modèle par défaut
     - Point de terminaison
     - Authentification
     - Emplacement des données
   * - Ollama (``ollama``)
     - ``gemma4:e4b``
     - ``http://localhost:11434``
     - Aucune (local)
     - Local / auto-hébergé — la question et les documents restent sur votre hôte
   * - OpenAI (``openai``)
     - ``gpt-5-mini``
     - ``https://api.openai.com/v1``
     - ``Authorization: Bearer`` (``rag.llm.openai.api.key``)
     - Cloud — la question et les documents récupérés sont envoyés à OpenAI
   * - Google Gemini (``gemini``)
     - ``gemini-3.1-flash-lite-preview``
     - ``https://generativelanguage.googleapis.com/v1beta``
     - ``x-goog-api-key`` (``rag.llm.gemini.api.key``)
     - Cloud — la question et les documents récupérés sont envoyés à Google

.. note::

   La valeur par défaut de ``rag.llm.name`` est ``ollama``. Cette valeur permet de déterminer le nom du composant DI à charger ( ``{rag.llm.name}LlmClient`` ).
   Ainsi, si vous laissez ``rag.llm.name`` à sa valeur par défaut tout en installant uniquement un plugin autre que ``fess-llm-ollama``, aucun client LLM ne sera actif.
   Dans ce cas, le journal affiche l'avertissement ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` et le mode de recherche IA n'est pas disponible.
   Veillez à toujours configurer ``rag.llm.name`` en fonction du plugin installé. La valeur ``none`` permet de désactiver explicitement l'intégration LLM.

Installation du plugin
=======================

La fonctionnalité LLM est fournie sous forme de plugins. Installez le plugin ``fess-llm-{provider}`` correspondant au fournisseur utilisé.

Vous pouvez l'installer depuis la page « Système > Plugin » de l'interface d'administration. Les plugins ``fess-llm-*`` apparaissent dans la liste des plugins installables.

Pour une installation manuelle, placez le fichier JAR correspondant (par exemple ``fess-llm-openai-15.8.0.jar`` pour le fournisseur OpenAI) dans le répertoire suivant.

::

    app/WEB-INF/plugin/

Quelle que soit la méthode utilisée, le plugin sera chargé au redémarrage de |Fess| après l'installation.

Architecture
=============

La fonctionnalité de mode de recherche IA fonctionne selon le flux suivant.

1. **Saisie utilisateur** : L'utilisateur saisit une question dans l'interface de chat
2. **Analyse d'intention (intent)** : Le LLM analyse la question de l'utilisateur et extrait les mots-clés de recherche
3. **Exécution de la recherche (search)** : Recherche de documents pertinents avec le moteur de recherche |Fess|
4. **Évaluation des résultats (evaluate)** : Le LLM évalue la pertinence des résultats de recherche et sélectionne les meilleurs documents
5. **Regénération de requête (si nécessaire)** : Lorsqu'aucun résultat n'est trouvé ou qu'aucun document pertinent n'est identifié lors de l'évaluation, le LLM régénère la requête et relance la recherche
6. **Récupération du contenu (fetch)** : Récupération du corps des documents sélectionnés
7. **Génération de réponse (answer)** : Le LLM génère une réponse à partir des documents récupérés (avec rendu Markdown)
8. **Citation des sources** : La réponse inclut des liens vers les documents sources

.. note::

   Le traitement interne est composé de cinq phases : ``intent``, ``search``, ``evaluate``, ``fetch`` et ``answer``. La progression de chaque phase est notifiée au client par streaming (SSE).
   La regénération de requête n'est pas une phase indépendante ; elle est notifiée comme un repli de la phase ``search``, après quoi la phase ``search`` est réexécutée.

.. note::

   Le déroulement décrit ci-dessus correspond au cas où l'API de streaming détermine que l'intention est « recherche ». Le chemin suivi varie selon le résultat de la détection d'intention.
   Si la question est jugée peu claire, une réponse est générée sans effectuer de recherche ; si un résumé d'URL est demandé, une recherche d'URL est effectuée sans exécuter la phase d'évaluation.
   Par ailleurs, l'API non-streaming ``POST /api/v2/chat`` n'exécute pas la phase d'évaluation et ne notifie pas non plus la progression phase par phase.

Configuration de base
======================

La configuration de la fonctionnalité LLM s'effectue dans deux emplacements.

Configuration générale de l'administration / system.properties
---------------------------------------------------------------

La configuration s'effectue dans la configuration générale de l'administration, ou dans ``system.properties``. Utilisé pour la sélection du fournisseur LLM.

::

    # Spécifier le fournisseur LLM (ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
-----------------------

La configuration s'effectue dans ``app/WEB-INF/classes/fess_config.properties`` (dans la version paquet : ``/etc/fess/fess_config.properties`` ).
Ce fichier permet d'activer le mode de recherche IA, de configurer les sessions et l'historique de conversation, ainsi que les paramètres spécifiques au fournisseur (URL de connexion, clé API, paramètres de génération, etc.).

::

    # Activer la fonctionnalité de mode de recherche IA (par défaut : false)
    rag.chat.enabled=true

    # Exemple de configuration spécifique au fournisseur (cas OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

Pour la configuration détaillée de chaque fournisseur, consultez les documents suivants.

- :doc:`llm-ollama` - Configuration d'Ollama
- :doc:`llm-openai` - Configuration d'OpenAI
- :doc:`llm-gemini` - Configuration de Google Gemini

Configuration commune
======================

Éléments de configuration communs à tous les fournisseurs LLM. Ces éléments se configurent dans ``fess_config.properties``.

Configuration du contexte
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.chat.context.max.documents``
     - Nombre maximum de documents à inclure dans le contexte
     - ``5``
   * - ``rag.chat.content.fields``
     - Champs à récupérer depuis les documents
     - ``title,url,content,doc_id,content_title,content_description``

.. note::

   Le nombre maximum de caractères du contexte (``context.max.chars``) a été remplacé par une configuration par fournisseur et par type de prompt. Configurez-le dans ``fess_config.properties`` sous la forme ``rag.llm.{provider}.{promptType}.context.max.chars``.

Prompt système
---------------

Les prompts système sont gérés dans les fichiers DI XML de chaque plugin, et non dans les fichiers de propriétés.

Le prompt système est défini dans le fichier ``fess_llm++.xml`` inclus dans le JAR de chaque plugin ``fess-llm-*``.
Il n'est pas nécessaire d'extraire le fichier JAR pour le modifier afin de personnaliser les prompts. Grâce au mécanisme de redéfinition de composant de LastaDi,
placer dans ``app/WEB-INF/classes/`` un fichier nommé ``fess_llm+{nom du composant}.xml`` permet de remplacer la définition de composant fournie par le plugin.

Le nom du composant varie selon le fournisseur, comme indiqué ci-dessous.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Fournisseur
     - Nom du composant
   * - Ollama
     - ``ollamaLlmClient``
   * - OpenAI
     - ``openaiLlmClient``
   * - Google Gemini
     - ``geminiLlmClient``

Par exemple, pour modifier le prompt de génération de réponse du fournisseur OpenAI, créez ``app/WEB-INF/classes/fess_llm+openaiLlmClient.xml``.

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="openaiLlmClient" class="org.codelibs.fess.llm.openai.OpenAiLlmClient">
            <postConstruct name="register"/>
            <postConstruct name="init"/>
            <preDestroy name="destroy"/>
            <property name="answerGenerationSystemPrompt">"Mon prompt personnalisé de génération de réponse"</property>
            <!-- Incluez également toutes les propriétés de prompt que vous ne modifiez pas -->
        </component>
    </components>

.. warning::

   Le fichier de redéfinition remplace la définition de composant. Vous devez donc y inclure l'intégralité du contenu défini dans le ``fess_llm++.xml``
   d'origine (nom de classe, ``postConstruct``, ``preDestroy``, ainsi que les propriétés de prompt que vous ne modifiez pas). Toute propriété omise reviendra à un état non défini.

.. warning::

   Ne copiez pas ``fess_llm++.xml`` tel quel dans ``app/WEB-INF/classes/``.
   Les fichiers DI XML dont le nom se termine par ``++`` sont tous chargés comme des « ajouts » sur le classpath ; le même composant se retrouve alors enregistré deux fois,
   ce qui provoque une ``TooManyRegistrationComponentException`` et empêche |Fess| de démarrer.

Vérification de disponibilité
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervalle de vérification périodique de la disponibilité du LLM (secondes)
     - ``60``

Cette configuration s'effectue dans ``fess_config.properties``. |Fess| vérifie périodiquement l'état de connexion au fournisseur LLM.

.. note::

   Si vous spécifiez pour cette propriété une valeur inférieure ou égale à ``0`` ou une valeur non numérique, cette valeur est ignorée et la valeur par défaut ( ``60`` ) est utilisée.
   Cette propriété ne permet pas de désactiver la vérification de disponibilité.
   Notez également que la vérification de disponibilité n'est pas exécutée lorsque ``rag.chat.enabled`` vaut ``false``, ni pour les fournisseurs non sélectionnés via ``rag.llm.name``.

Gestion des sessions
=====================

Configuration relative aux sessions de chat. Ces éléments se configurent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.chat.session.timeout.minutes``
     - Délai d'expiration de la session (minutes)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Nombre maximum de sessions
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique de conversation
     - ``30``

Contrôle de la concurrence
============================

Configuration contrôlant le nombre de requêtes simultanées vers le LLM. Se configure dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - Nombre maximum de requêtes simultanées vers le fournisseur
     - ``5``
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - Temps d'attente maximum (millisecondes) lorsque la limite de concurrence est atteinte. Si aucun créneau ne se libère dans ce délai, une erreur de limitation de débit est renvoyée
     - ``30000``

Par exemple, pour configurer la concurrence du fournisseur OpenAI :

::

    rag.llm.openai.max.concurrent.requests=10

Configuration de l'évaluation
================================

Configuration relative à l'évaluation des résultats de recherche. Se configure dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents à sélectionner lors de la phase d'évaluation
     - ``3``

Configuration par type de prompt
==================================

Les paramètres de génération peuvent être configurés par type de prompt. Cela permet des ajustements fins selon l'usage. La configuration s'effectue dans ``fess_config.properties``.

Liste des types de prompt
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Type de prompt
     - Valeur de configuration
     - Description
   * - Analyse d'intention
     - ``intent``
     - Analyse la question de l'utilisateur et extrait les mots-clés de recherche
   * - Évaluation
     - ``evaluation``
     - Évalue la pertinence des résultats de recherche
   * - Question peu claire
     - ``unclear``
     - Génère une réponse lorsque la question est peu claire
   * - Aucun résultat
     - ``noresults``
     - Génère une réponse lorsqu'aucun résultat de recherche n'est trouvé
   * - Document absent
     - ``docnotfound``
     - Génère une réponse lorsque le document correspondant n'existe pas
   * - Génération de réponse
     - ``answer``
     - Génère une réponse basée sur les résultats de recherche
   * - Résumé
     - ``summary``
     - Génère un résumé du document
   * - FAQ
     - ``faq``
     - Génère une réponse au format FAQ
   * - Réponse directe
     - ``direct``
     - Génère une réponse directe sans passer par la recherche (non appelé dans la version actuelle)
   * - Regénération de requête
     - ``queryregeneration``
     - Regénère la requête lorsqu'aucun résultat de recherche n'est trouvé

Modèles de configuration
-------------------------

La configuration par type de prompt se spécifie selon le modèle suivant.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Exemple de configuration (cas du fournisseur OpenAI) :

::

    # Configurer une température basse pour la génération de réponse
    rag.llm.openai.answer.temperature=0.5
    # Nombre maximum de tokens pour la génération de réponse
    rag.llm.openai.answer.max.tokens=4096
    # Configurer bas car une réponse courte suffit pour l'analyse d'intention
    rag.llm.openai.intent.max.tokens=256
    # Nombre maximum de caractères du contexte pour le résumé
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature``, ``max.tokens`` et ``context.max.chars`` sont utilisables avec tous les fournisseurs. Toutefois, leurs valeurs par défaut varient selon le fournisseur et le type de prompt.

En outre, chaque fournisseur prend en charge des paramètres qui lui sont propres. Le tableau suivant indique leur prise en charge.

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - Paramètre
     - Ollama
     - OpenAI
     - Gemini
   * - ``thinking.budget``
     - Pris en charge
     - Non pris en charge
     - Pris en charge
   * - ``thinking.level``
     - Pris en charge
     - Non pris en charge
     - Non pris en charge
   * - ``top.p``
     - Pris en charge
     - Pris en charge
     - Non pris en charge
   * - ``top.k``, ``num.ctx``
     - Pris en charge
     - Non pris en charge
     - Non pris en charge
   * - ``reasoning.effort``
     - Non pris en charge
     - Pris en charge
     - Non pris en charge
   * - ``frequency.penalty``, ``presence.penalty``
     - Non pris en charge
     - Pris en charge
     - Non pris en charge

.. note::

   Spécifier un paramètre « Non pris en charge » ne provoque pas d'erreur ; il est simplement ignoré. Pour la signification de chaque paramètre et les valeurs possibles, consultez la documentation de chaque fournisseur.

.. note::

   Seul le fournisseur Ollama dispose d'un repli sur ``rag.llm.ollama.default.{paramètre}`` lorsqu'aucune configuration par type de prompt n'existe
   (à l'exception de ``context.max.chars``). Les fournisseurs OpenAI et Gemini ne disposent pas de ce repli ;
   en l'absence de configuration par type de prompt, la valeur par défaut intégrée au plugin est utilisée.

Étapes suivantes
=================

- :doc:`llm-ollama` - Configuration détaillée d'Ollama
- :doc:`llm-openai` - Configuration détaillée d'OpenAI
- :doc:`llm-gemini` - Configuration détaillée de Google Gemini
- :doc:`rag-chat` - Configuration détaillée de la fonctionnalité de mode de recherche IA
- :doc:`rank-fusion` - Configuration du Rank Fusion (fusion des résultats de recherche hybride)
- :doc:`../user/chat-search` - Utilisation du mode de recherche IA
- :doc:`../api/api-chat` - Référence API Chat
