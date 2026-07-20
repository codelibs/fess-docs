==========================
Configuration du mode de recherche IA
==========================

Aperçu
====

Le mode de recherche IA (RAG: Retrieval-Augmented Generation) est une fonctionnalité qui enrichit les résultats de recherche de |Fess|
avec un LLM (grand modèle de langage) pour fournir des informations sous forme de dialogue.
Les utilisateurs peuvent poser des questions en langage naturel et obtenir des réponses détaillées basées sur les résultats de recherche.

Dans |Fess| 15.8, la fonctionnalité LLM a été séparée en plugins ``fess-llm-*``.
La configuration principale et la configuration spécifique au fournisseur LLM s'effectuent dans ``fess_config.properties``,
et la sélection du fournisseur LLM (``rag.llm.name``) s'effectue dans ``system.properties`` ou via l'administration.

Pipeline de recherche
======================

Le mode de recherche IA récupère ses documents source via le pipeline de recherche standard de |Fess| (rank fusion), avec le contrôle d'accès habituel de |Fess| par rôle et par étiquette (label). Par défaut, il s'agit d'une recherche par mots-clés (BM25) ; le LLM ne recherche, ne classe ni n'effectue lui-même d'embedding des documents.

Deux types de requêtes exécutent des pipelines légèrement différents :

- ``POST /api/v2/chat/stream`` (utilisé par l'interface Web) exécute le flux complet : **analyse d'intention -> recherche -> évaluation de pertinence par le LLM -> récupération du contenu -> génération de réponse** (en streaming).
- ``POST /api/v2/chat`` (non-streaming) exécute un flux plus court : **analyse d'intention -> recherche -> génération de réponse** (sans phase d'évaluation de pertinence ni phase distincte de récupération du contenu).

Dans le flux en streaming, un appel LLM supplémentaire **évalue les résultats de recherche** et ne conserve que les documents jugés pertinents avant que la réponse ne soit générée.

Fonctionnement du mode de recherche IA
================

Le mode de recherche IA fonctionne selon un flux en plusieurs étapes.

1. **Phase d'analyse d'intention** : Analyse la question de l'utilisateur et extrait les mots-clés optimaux pour la recherche
2. **Phase de recherche** : Recherche des documents avec les mots-clés extraits en utilisant le moteur de recherche |Fess|
3. **Fallback de régénération de requête** : Lorsqu'aucun résultat n'est trouvé, le LLM régénère la requête et réessaie
4. **Phase d'évaluation** : Évalue la pertinence des résultats de recherche et sélectionne les documents les plus appropriés
5. **Phase de génération** : Le LLM génère une réponse basée sur les documents sélectionnés
6. **Phase de sortie** : Retourne la réponse et les informations sources à l'utilisateur (avec rendu Markdown)

Ce flux permet des réponses de haute qualité comprenant le contexte, supérieur à la simple recherche par mots-clés.
La régénération de requête améliore la couverture des réponses lorsque la requête initiale n'est pas optimale.

Configuration de base
========

La configuration de la fonctionnalité de mode de recherche IA est divisée en configuration principale et en configuration du fournisseur.

Configuration principale (fess_config.properties)
----------------------------------

Configuration de base pour activer la fonctionnalité de mode de recherche IA.
À configurer dans ``app/WEB-INF/conf/fess_config.properties``.

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

Configuration du fournisseur (system.properties / administration)
-------------------------------------------------

La sélection du fournisseur LLM s'effectue via l'administration ou les propriétés système.

**Via l'administration** :

Depuis l'écran de configuration Administration > Système > General, sélectionnez le fournisseur LLM à utiliser.

**Via system.properties** :

::

    # Selectionner le fournisseur LLM (ollama, openai, gemini)
    rag.llm.name=ollama

Pour la configuration détaillée des fournisseurs LLM, consultez :

- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini

Référence rapide des chemins de configuration
=============================================

Dans |Fess| 15.8, les paramètres sont séparés en deux familles : la famille FessConfig
(``fess_config.properties``) et la famille SystemProperty (``system.properties``,
persistée dans OpenSearch). Les chemins de configuration diffèrent ; ne pas les confondre.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - Propriété
     - Famille
     - Passage via Docker / options JVM
     - UI Admin
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - Non
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (défaut initial uniquement)
     - Oui (paramètres généraux)
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - Non
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - Non
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - Non
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - Non
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - Non

.. note::

   ``rag.llm.type`` est l'ancien nom de propriété dans |Fess| 15.5 et antérieur.
   Dans 15.8 et supérieur il est renommé en ``rag.llm.name`` ; les valeurs écrites
   sous ``rag.llm.type`` ne sont pas lues.

Liste des configurations principales
============

Liste des configurations principales disponibles dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.chat.enabled``
     - Activer la fonctionnalité de mode de recherche IA
     - ``false``
   * - ``rag.chat.context.max.documents``
     - Nombre maximum de documents à inclure dans le contexte
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - Délai d'expiration de la session (minutes)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Nombre maximum de sessions pouvant être maintenues simultanément
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique de conversation
     - ``30``
   * - ``rag.chat.content.fields``
     - Champs à récupérer des documents
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Nombre maximum de caractères du message utilisateur. Cette valeur est lue en tant que System Property ; l'entrée dans ``fess_config.properties`` n'est pas utilisée. Définissez-la via les System Properties ou ``-Dfess.system.rag.chat.message.max.length``.
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Taille du fragment pour le surlignage de recherche
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Nombre de fragments pour le surlignage de recherche
     - ``3``
   * - ``rag.chat.content.fulltext.max.length``
     - Seuil de ``content_length`` au-delà duquel les documents utilisent des extraits en surbrillance plutôt que le texte intégral dans le contexte de réponse
     - ``3000``
   * - ``rag.chat.answer.highlight.fragment.size``
     - Taille du fragment de surlignage lors de l'extraction d'extraits de grands documents pour le contexte de réponse
     - ``1000``
   * - ``rag.chat.answer.highlight.number.of.fragments``
     - Nombre de fragments de surlignage lors de l'extraction d'extraits de grands documents pour le contexte de réponse
     - ``5``
   * - ``rag.chat.history.assistant.content``
     - Type de contenu à inclure dans l'historique de l'assistant ( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``
   * - ``rag.chat.history.titles.max.count``
     - Nombre maximum de titres de documents référencés conservés par tour en mode ``smart_summary``
     - ``5``

Paramètres de génération
================

Dans |Fess| 15.8, les paramètres de génération (nombre maximum de tokens, température, etc.) se configurent par fournisseur
et par type de prompt. Ces configurations sont gérées comme paramètres de chaque plugin ``fess-llm-*``
et non comme configurations principales.

Pour les détails, consultez la documentation de chaque fournisseur :

- :doc:`llm-ollama` - Paramètres de génération Ollama
- :doc:`llm-openai` - Paramètres de génération OpenAI
- :doc:`llm-gemini` - Paramètres de génération Google Gemini

Configuration du contexte
================

Configuration du contexte passé au LLM depuis les résultats de recherche.

Configuration principale
--------

Les configurations suivantes s'effectuent dans ``fess_config.properties``.

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
     - Champs à récupérer des documents
     - ``title,url,content,doc_id,content_title,content_description``

Configuration spécifique au fournisseur
-----------------------

Les configurations suivantes s'effectuent dans ``fess_config.properties`` pour chaque fournisseur.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - Nombre maximum de caractères du contexte
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - Nombre maximum de documents pertinents à sélectionner lors de la phase d'évaluation

``{provider}`` contient le nom du fournisseur tel que ``ollama``, ``openai``, ``gemini``, etc.
``{promptType}`` contient le type de prompt tel que ``intent``, ``evaluation``, ``answer``, ``summary``, ``faq``, ``queryregeneration``,
``unclear``, ``noresults``, ``docnotfound``, ``direct``, etc.
La liste des types de prompt pris en charge est définie dans l'implémentation ``*LlmClient`` de chaque plugin.

Pour les détails, consultez la documentation de chaque fournisseur.

Champs de contenu
--------------------

Champs spécifiables dans ``rag.chat.content.fields`` :

- ``title`` - Titre du document
- ``url`` - URL du document
- ``content`` - Corps du document
- ``doc_id`` - ID du document
- ``content_title`` - Titre du contenu
- ``content_description`` - Description du contenu

Prompt système
==================

Dans |Fess| 15.8, les prompts système sont définis dans le DI XML (``fess_llm++.xml``) de chaque plugin ``fess-llm-*``
et non dans les fichiers de propriétés.

Personnalisation des prompts
-------------------------

Pour personnaliser les prompts système, surchargez le fichier ``fess_llm++.xml`` dans le JAR du plugin.

1. Récupérez ``fess_llm++.xml`` dans le fichier JAR du plugin utilisé
2. Apportez les modifications nécessaires
3. Placez-le dans l'emplacement approprié sous ``app/WEB-INF/`` pour le surcharger

Des prompts système différents sont définis pour chaque type de prompt (analyse d'intention, évaluation, génération),
avec une optimisation adaptée à chaque usage.

Pour les détails, consultez la documentation de chaque fournisseur :

- :doc:`llm-ollama` - Configuration des prompts Ollama
- :doc:`llm-openai` - Configuration des prompts OpenAI
- :doc:`llm-gemini` - Configuration des prompts Google Gemini

Gestion des sessions
==============

Configuration de la gestion des sessions de chat.

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
     - Nombre maximum de sessions pouvant être maintenues simultanément
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique de conversation
     - ``30``

Comportement des sessions
----------------

- Lorsqu'un utilisateur commence un nouveau chat, une nouvelle session est créée
- L'historique de conversation est sauvegardé dans la session, permettant un dialogue contextuel
- Les sessions sont automatiquement supprimées après expiration du délai
- Lorsque l'historique dépasse le nombre maximum de messages, les anciens messages sont supprimés

Contrôle de la concurrence
============

Le nombre de requêtes simultanées vers le LLM est contrôlé par fournisseur dans ``fess_config.properties``.

::

    # Nombre maximum de requetes simultanees par fournisseur (defaut : 5)
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=5
    rag.llm.gemini.max.concurrent.requests=5

    # Timeout d'attente pour l'obtention d'un permis de concurrence (millisecondes, defaut : 30000)
    rag.llm.ollama.concurrency.wait.timeout=30000

Considérations sur le contrôle de la concurrence
-----------------------

- Tenez compte également des limitations de débit côté fournisseur LLM
- Dans les environnements à forte charge, il est recommandé de configurer des valeurs plus petites
- Lorsque la limite de concurrence est atteinte, les requêtes entrent dans une file d'attente et sont traitées séquentiellement
- Si l'attente d'un permis dépasse ``concurrency.wait.timeout``, la requête échoue avec une erreur de timeout

Mode d'historique de conversation
=================================

``rag.chat.history.assistant.content`` contrôle la manière dont les réponses de l'assistant sont stockées dans l'historique de conversation.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Mode
     - Description
   * - ``smart_summary``
     - (Par défaut) Le corps de la réponse de l'assistant est omis de l'historique ; seuls la requête de recherche passée et les titres des documents référencés (au maximum ``rag.chat.history.titles.max.count`` éléments) sont conservés par tour
   * - ``full``
     - Préserve la réponse entière telle quelle
   * - ``source_titles``
     - Préserve uniquement les titres des sources
   * - ``source_titles_and_urls``
     - Préserve les titres et URLs des sources
   * - ``truncated``
     - Tronque la réponse à la limite maximale de caractères
   * - ``none``
     - Ne préserve pas l'historique

.. note::

   En mode ``smart_summary``, le corps de la réponse est remplacé par la requête de recherche et les titres référencés, ce qui préserve le contexte efficacement tout en réduisant l'utilisation des tokens.
   Les paires de messages utilisateur et assistant sont groupées en tours et empaquetées de manière optimale dans un budget de caractères.
   Les limites maximales de caractères pour l'historique et le résumé sont contrôlées par l'implémentation ``LlmClient`` de chaque plugin ``fess-llm-*``.

Régénération de requête
=======================

Lorsqu'aucun résultat de recherche n'est trouvé ou qu'aucun résultat pertinent n'est identifié, le LLM régénère automatiquement la requête et relance la recherche.

- Avec zéro résultats de recherche : Régénération de requête avec raison ``no_results``
- Lorsqu'aucun document pertinent n'est trouvé : Régénération de requête avec raison ``no_relevant_results``
- Retombe sur la requête originale si la régénération échoue

Cette fonctionnalité est activée par défaut et intégrée dans les flux RAG synchrones et en streaming.
Les prompts de régénération de requête sont définis dans chaque plugin ``fess-llm-*``.

Rendu Markdown
==============

Les réponses du mode de recherche IA sont rendues au format Markdown.

- Les réponses du LLM sont analysées en Markdown et converties en HTML
- Le HTML converti est assaini, n'autorisant que les balises et attributs sûrs
- Prend en charge les titres, listes, blocs de code, tableaux, liens et autres syntaxes Markdown
- Côté client, ``marked.js`` et ``DOMPurify`` sont utilisés ; côté serveur, le sanitizer OWASP

Utilisation de l'API
=========

La fonctionnalité de mode de recherche IA est accessible via API REST (API v2).
L'URL de base est ``http://<nom du serveur>/api/v2/``.

La Chat API fournit les trois points de terminaison suivants.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Point de terminaison
     - Description
   * - ``POST /api/v2/chat``
     - Complétion RAG groupée (non-streaming)
   * - ``POST /api/v2/chat/stream``
     - Complétion RAG en streaming (Server-Sent Events)
   * - ``DELETE /api/v2/chat/sessions/{session_id}``
     - Effacer l'historique de conversation d'une session

Les requêtes sont envoyées avec un corps JSON de type ``Content-Type: application/json``.
Les requêtes modifiant l'état (``POST`` / ``DELETE``) nécessitent un jeton CSRF (en-tête ``X-Fess-CSRF-Token``).
Les réponses sont encapsulées dans l'enveloppe commune ``response``.

.. note::

   Les points de terminaison ``/api/v1/chat`` au format paramètres de formulaire disponibles dans |Fess| 15.5 et antérieur ont été supprimés.
   Dans 15.8, utilisez l'API JSON sous ``/api/v2/``.

API non-streaming
-------------------

Point de terminaison : ``POST /api/v2/chat``

Corps de la requête (JSON) :

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Requis
     - Description
   * - ``message``
     - Oui
     - Message de l'utilisateur
   * - ``session_id``
     - Non
     - ID de session (pour continuer la conversation). Si omis, le serveur le crée et le retourne dans la réponse
   * - ``fields``
     - Non
     - Champs de filtre optionnels pour l'étape de récupération (objet)
   * - ``fields.label``
     - Non
     - Filtre de recherche par étiquette
   * - ``extra_queries``
     - Non
     - Expressions de requête supplémentaires pour les filtres de facettes

Exemple de requête :

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Comment installer Fess ?"}'

Exemple de réponse :

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123",
        "content": "La methode d'installation de Fess est...",
        "sources": [
          {
            "rank": 1,
            "title": "Guide d'installation",
            "url": "https://...",
            "doc_id": "...",
            "snippet": "..."
          }
        ]
      }
    }

API streaming
-----------------

Point de terminaison : ``POST /api/v2/chat/stream``

Le corps de la requête est identique à ``POST /api/v2/chat`` (JSON).
Les réponses sont streamées au format Server-Sent Events (SSE).

Exemple de requête :

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Quelles sont les caracteristiques de Fess ?"}'

Événements SSE :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Événement
     - Description (charge utile)
   * - ``phase``
     - Transition de phase du pipeline (``intent``, ``search``, ``evaluate``, ``fetch``, ``answer``). ``{ phase, status, message?, keywords?, hit_count?, ... }``
   * - ``chunk``
     - Fragment de texte généré (``{ content }``)
   * - ``retry``
     - Notifie lorsqu'une requête LLM est réessayée (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``)
   * - ``waiting``
     - Progression d'une phase longue telle que l'attente d'un permis de concurrence (``{ phase, reason, elapsed_ms, timeout_ms }``)
   * - ``fallback``
     - Notifie lorsque la requête est régénérée suite à l'absence de résultats ou de résultats pertinents (``{ phase, reason, original_query?, new_query? }``, raison : ``no_results`` ou ``no_relevant_results``)
   * - ``warning``
     - Notifie lors d'un avertissement récupérable (``{ phase, code, detail? }``, ex. épuisement des tokens d'un modèle de raisonnement)
   * - ``sources``
     - Informations sur les documents sources (``{ sources: [...] }``)
   * - ``done``
     - Traitement terminé (``{ session_id, html_content? }``). ``html_content`` contient la chaîne HTML rendue depuis Markdown
   * - ``error``
     - Échec terminal en cours de stream (``{ phase?, message, error_code }``). Timeout, dépassement de la longueur de contexte, modèle introuvable, réponse invalide, erreur de connexion, etc.

Effacer une session
--------------------

Point de terminaison : ``DELETE /api/v2/chat/sessions/{session_id}``

Efface l'historique de conversation de la session spécifiée. En cas de succès, ``cleared: true`` est retourné.

Pour la documentation API complète (authentification, CSRF, limites de débit, codes HTTP), consultez :doc:`../api/api-chat`.

Interface Web
===================

La fonctionnalité de mode de recherche IA est accessible depuis l'écran de recherche de l'interface Web |Fess|.

Démarrer un chat
--------------

1. Accédez à l'écran de recherche |Fess|
2. Cliquez sur l'icône de chat
3. Le panneau de chat s'affiche

Utiliser le chat
--------------

1. Entrez votre question dans la zone de texte
2. Cliquez sur le bouton d'envoi ou appuyez sur Entrée
3. La réponse de l'assistant IA s'affiche
4. La réponse inclut des liens vers les sources

Continuer la conversation
----------

- Vous pouvez continuer la conversation dans la même session de chat
- Les réponses tiennent compte du contexte des questions précédentes
- Cliquez sur "Nouveau chat" pour réinitialiser la session

Dépannage
======================

Le bouton mode IA n'apparaît pas sur l'écran de recherche
---------------------------------------------------------

**Symptôme** : Le bouton mode IA ne s'affiche pas dans l'en-tête des résultats
de recherche, et accéder à ``/chat`` redirige vers la page d'accueil.

**Liste de vérifications** : vérifier les points suivants dans l'ordre.

1. ``rag.chat.enabled=true`` est-il défini ?

   - Docker : ``-Dfess.config.rag.chat.enabled=true`` est-il inclus dans ``FESS_JAVA_OPTS`` ?
   - Installation par paquet : est-il écrit dans ``app/WEB-INF/conf/fess_config.properties`` ?

2. Le plugin ``fess-llm-*`` correspondant est-il installé ?

   - Docker : ``FESS_PLUGINS=fess-llm-gemini:15.8.0`` (ou ``fess-llm-openai`` / ``fess-llm-ollama``) doit être défini
   - Installation par paquet : le JAR doit être placé dans ``app/WEB-INF/plugin/``
   - Le journal de démarrage doit inclure ``Installing fess-llm-XXX-15.8.0.jar``

3. ``rag.llm.name`` correspond-il à un plugin installé ?

   - La valeur par défaut est ``ollama``. Si seul le plugin Gemini est installé, vous devez explicitement le définir à ``gemini`` (de même ``openai`` pour le plugin OpenAI)
   - Méthode (a) : modifier ``rag.llm.name`` depuis Administration > Système > General (section RAG) et enregistrer
   - Méthode (b) : inclure ``-Dfess.system.rag.llm.name=gemini`` dans ``FESS_JAVA_OPTS`` au démarrage. N'agit que comme valeur par défaut initiale avant qu'une valeur ne soit persistée dans OpenSearch

4. Un WARN comme ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` se répète-t-il dans le journal ?

   - Symptôme typique quand ``rag.llm.name`` est encore ``ollama`` mais que le plugin Ollama n'est pas installé
   - Définir ``rag.llm.name`` au fournisseur réellement utilisé résout le problème
   - De même, ``componentName=geminiLlmClient`` indique que ``rag.llm.name=gemini`` est défini mais que le plugin ``fess-llm-gemini`` n'est pas installé

5. La clé d'API spécifique au fournisseur est-elle configurée ?

   - Quand ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` est vide, ``checkAvailabilityNow`` retourne ``false`` et le mode IA est désactivé
   - Activer DEBUG sur ``org.codelibs.fess.llm.gemini`` dans ``log4j2.xml`` fait apparaître des messages comme ``[LLM:GEMINI] Gemini is not available. apiKey is blank``

6. L'hôte Fess peut-il atteindre le fournisseur LLM ?

   - Pour les API cloud (Gemini / OpenAI), le conteneur doit avoir un accès sortant à Internet
   - En cas de proxy, définissez ``http.proxy.host`` / ``http.proxy.port`` (et au besoin ``http.proxy.username`` / ``http.proxy.password``) dans ``fess_config.properties``. Dans un environnement Docker, ajoutez ``-Dfess.config.http.proxy.host=... -Dfess.config.http.proxy.port=...`` à ``FESS_JAVA_OPTS`` (depuis |Fess| 15.8, les clients LLM partagent la configuration de proxy commune à |Fess|)

.. note::

   La page "General" n'expose pas de case à cocher pour ``rag.chat.enabled`` (par conception).
   Cette propriété de la famille FessConfig ne peut être définie qu'à travers
   ``fess_config.properties`` ou ``-Dfess.config.rag.chat.enabled=true``.

Le mode de recherche IA ne s'active pas
------------------------

**Points à vérifier** :

1. Vérifier si ``rag.chat.enabled=true`` est configuré
2. Vérifier si le fournisseur LLM est correctement configuré dans ``rag.llm.name``
3. Vérifier si le plugin ``fess-llm-*`` correspondant est installé
4. Vérifier si la connexion au fournisseur LLM est possible

Qualité des réponses insuffisante
----------------

**Améliorations** :

1. Utiliser un modèle LLM plus performant
2. Augmenter ``rag.chat.context.max.documents``
3. Personnaliser le prompt système dans le DI XML
4. Ajuster les paramètres de température spécifiques au fournisseur (consultez la documentation de chaque plugin ``fess-llm-*``)

Réponses lentes
----------------

**Améliorations** :

1. Utiliser un modèle LLM plus rapide (ex : Gemini Flash)
2. Réduire les paramètres max.tokens spécifiques au fournisseur (consultez la documentation de chaque plugin ``fess-llm-*``)
3. Réduire ``rag.chat.context.max.documents``

Sessions non maintenues
------------------------

**Points à vérifier** :

1. Vérifier si le ``session_id`` est correctement envoyé côté client
2. Vérifier le paramètre ``rag.chat.session.timeout.minutes``
3. Vérifier la capacité de stockage des sessions

Configuration de débogage
------------

Pour investiguer les problèmes, ajustez le niveau de log pour afficher des logs détaillés.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.v2.handlers" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Les messages de log utilisent le préfixe ``[RAG]``, avec des sous-préfixes tels que ``[RAG:INTENT]``, ``[RAG:EVAL]`` et ``[RAG:ANSWER]`` pour chaque phase.
Au niveau INFO, les logs de fin de chat (durée, nombre de sources) sont émis. Au niveau DEBUG, les détails d'utilisation des tokens, de contrôle de concurrence et d'empaquetage de l'historique sont émis.

Journal de recherche et type d'accès
-------------------------------------

Les recherches via le mode de recherche IA sont enregistrées avec le nom du fournisseur LLM (par ex. ``ollama``, ``openai``, ``gemini``) comme type d'accès dans les journaux de recherche. Cela permet de distinguer les recherches du mode IA des recherches web ou API régulières dans les analyses.

Informations de référence
========

- :doc:`llm-overview` - Aperçu de l'intégration LLM
- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini
- :doc:`../api/api-chat` - Référence API Chat
- :doc:`../user/chat-search` - Guide de recherche par chat pour les utilisateurs
