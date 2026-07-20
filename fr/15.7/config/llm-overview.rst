======================================================================
Vue d'ensemble du mode de recherche IA (RAG) et de l'intégration LLM
======================================================================

Vue d'ensemble
==============

|Fess| prend en charge la fonctionnalité de mode de recherche IA (RAG : Retrieval-Augmented Generation) utilisant
les grands modèles de langage (LLM). Cette fonctionnalité permet aux utilisateurs d'obtenir des informations
sous forme de dialogue avec un assistant IA basé sur les résultats de recherche.

La fonctionnalité d'intégration LLM est fournie sous forme de plugins ``fess-llm-*``. Installez le plugin correspondant au fournisseur LLM que vous souhaitez utiliser.

Le mode de recherche IA récupère les documents via le pipeline de recherche standard de |Fess| (rank fusion), et non via un index vectoriel dédié ; par défaut, il s'agit d'une recherche par mots-clés (BM25). Comme ce pipeline standard est réutilisé, si vous installez et configurez le plugin Semantic Search, son moteur de recherche sémantique (vectoriel) participe au rank fusion pour toutes les recherches, y compris l'étape de récupération du mode de recherche IA ; aucune configuration spécifique au mode de recherche IA n'est nécessaire. Pour plus de détails, consultez :doc:`rank-fusion`.

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
     - API cloud d'OpenAI. Permet d'utiliser des modèles comme GPT-4.
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

   Si ``rag.llm.name`` n'est pas défini, seul le client Ollama est actif par défaut ; installez et sélectionnez le fournisseur souhaité avec ``rag.llm.name``.

Installation du plugin
=======================

La fonctionnalité LLM est fournie sous forme de plugins. Il est nécessaire de placer le fichier JAR du plugin ``fess-llm-{provider}`` correspondant au fournisseur utilisé dans le répertoire des plugins.

Par exemple, pour utiliser le fournisseur OpenAI, téléchargez ``fess-llm-openai-15.7.0.jar`` et placez-le dans le répertoire suivant.

::

    app/WEB-INF/plugin/

Après le placement, le plugin sera chargé au redémarrage de |Fess|.

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

La configuration s'effectue dans ``app/WEB-INF/conf/fess_config.properties``. Ce fichier permet d'activer le mode de recherche IA, de configurer les sessions et l'historique de conversation, ainsi que les paramètres spécifiques au fournisseur (URL de connexion, clé API, paramètres de génération, etc.).

::

    # Activer la fonctionnalité de mode de recherche IA
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

Le prompt système est défini dans le fichier ``fess_llm++.xml`` inclus dans le JAR de chaque plugin ``fess-llm-*``. Ce fichier est une ressource classpath intégrée au JAR du plugin ; pour personnaliser les prompts, il est nécessaire de modifier le fichier DI XML à l'intérieur du JAR.

Vérification de disponibilité
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervalle de vérification de disponibilité du LLM (secondes). 0 pour désactiver
     - ``60``

Cette configuration s'effectue dans ``fess_config.properties``. |Fess| vérifie périodiquement l'état de connexion au fournisseur LLM.

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
     - Génère une réponse directe sans passer par la recherche
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

   ``temperature``, ``max.tokens`` et ``context.max.chars`` sont utilisables avec tous les fournisseurs. En outre, chaque fournisseur prend en charge des paramètres qui lui sont propres, tels que ``thinking.budget``, ``top.p`` ou ``reasoning.effort``. Consultez la documentation de chaque fournisseur pour plus de détails.

Étapes suivantes
=================

- :doc:`llm-ollama` - Configuration détaillée d'Ollama
- :doc:`llm-openai` - Configuration détaillée d'OpenAI
- :doc:`llm-gemini` - Configuration détaillée de Google Gemini
- :doc:`rag-chat` - Configuration détaillée de la fonctionnalité de mode de recherche IA
- :doc:`rank-fusion` - Configuration du Rank Fusion (fusion des résultats de recherche hybride)
