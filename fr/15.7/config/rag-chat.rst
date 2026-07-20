==========================
Configuration du mode de recherche IA
==========================

Apercu
====

Le mode de recherche IA (RAG: Retrieval-Augmented Generation) est une fonctionnalite qui enrichit les resultats de recherche de |Fess|
avec un LLM (grand modele de langage) pour fournir des informations sous forme de dialogue.
Les utilisateurs peuvent poser des questions en langage naturel et obtenir des reponses detaillees basees sur les resultats de recherche.

Dans |Fess| 15.7, la fonctionnalite LLM a ete separee en plugins ``fess-llm-*``.
La configuration principale et la configuration specifique au fournisseur LLM s'effectuent dans ``fess_config.properties``,
et la selection du fournisseur LLM (``rag.llm.name``) s'effectue dans ``system.properties`` ou via l'administration.

Pipeline de recherche
======================

Le mode de recherche IA recupere ses documents source via le pipeline de recherche standard de |Fess| (rank fusion), avec le controle d'acces habituel de |Fess| par role et par etiquette (label). Par defaut, il s'agit d'une recherche par mots-cles (BM25) ; le LLM ne recherche, ne classe ni n'effectue lui-meme d'embedding des documents.

Deux types de requetes executent des pipelines legerement differents :

- ``POST /api/v2/chat/stream`` (utilise par l'interface Web) execute le flux complet : **analyse d'intention -> recherche -> evaluation de pertinence par le LLM -> recuperation du contenu -> generation de reponse** (en streaming).
- ``POST /api/v2/chat`` (non-streaming) execute un flux plus court : **analyse d'intention -> recherche -> generation de reponse** (sans phase d'evaluation de pertinence ni phase distincte de recuperation du contenu).

Dans le flux en streaming, un appel LLM supplementaire **evalue les resultats de recherche** et ne conserve que les documents juges pertinents avant que la reponse ne soit generee.

Fonctionnement du mode de recherche IA
================

Le mode de recherche IA fonctionne selon un flux en plusieurs etapes.

1. **Phase d'analyse d'intention** : Analyse la question de l'utilisateur et extrait les mots-cles optimaux pour la recherche
2. **Phase de recherche** : Recherche des documents avec les mots-cles extraits en utilisant le moteur de recherche |Fess|
3. **Fallback de regeneration de requete** : Lorsqu'aucun resultat n'est trouve, le LLM regenere la requete et reessaie
4. **Phase d'evaluation** : Evalue la pertinence des resultats de recherche et selectionne les documents les plus appropries
5. **Phase de generation** : Le LLM genere une reponse basee sur les documents selectionnes
6. **Phase de sortie** : Retourne la reponse et les informations sources a l'utilisateur (avec rendu Markdown)

Ce flux permet des reponses de haute qualite comprenant le contexte, superieur a la simple recherche par mots-cles.
La regeneration de requete ameliore la couverture des reponses lorsque la requete initiale n'est pas optimale.

Configuration de base
========

La configuration de la fonctionnalite de mode de recherche IA est divisee en configuration principale et en configuration du fournisseur.

Configuration principale (fess_config.properties)
----------------------------------

Configuration de base pour activer la fonctionnalite de mode de recherche IA.
A configurer dans ``app/WEB-INF/conf/fess_config.properties``.

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

Configuration du fournisseur (system.properties / administration)
-------------------------------------------------

La selection du fournisseur LLM s'effectue via l'administration ou les proprietes systeme.

**Via l'administration** :

Depuis l'ecran de configuration Administration > Systeme > General, selectionnez le fournisseur LLM a utiliser.

**Via system.properties** :

::

    # Selectionner le fournisseur LLM (ollama, openai, gemini)
    rag.llm.name=ollama

Pour la configuration detaillee des fournisseurs LLM, consultez :

- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini

Reference rapide des chemins de configuration
=============================================

Dans |Fess| 15.7, les parametres sont separes en deux familles : la famille FessConfig
(``fess_config.properties``) et la famille SystemProperty (``system.properties``,
persistee dans OpenSearch). Les chemins de configuration different ; ne pas les confondre.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - Propriete
     - Famille
     - Passage via Docker / options JVM
     - UI Admin
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - Non
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (defaut initial uniquement)
     - Oui (parametres generaux)
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

   ``rag.llm.type`` est l'ancien nom de propriete dans |Fess| 15.5 et anterieur.
   Dans 15.7 et superieur il est renomme en ``rag.llm.name`` ; les valeurs ecrites
   sous ``rag.llm.type`` ne sont pas lues.

Liste des configurations principales
============

Liste des configurations principales disponibles dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.enabled``
     - Activer la fonctionnalite de mode de recherche IA
     - ``false``
   * - ``rag.chat.context.max.documents``
     - Nombre maximum de documents a inclure dans le contexte
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - Delai d'expiration de la session (minutes)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Nombre maximum de sessions pouvant etre maintenues simultanement
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique de conversation
     - ``30``
   * - ``rag.chat.content.fields``
     - Champs a recuperer des documents
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Nombre maximum de caracteres du message utilisateur. Cette valeur est lue en tant que System Property ; l'entree dans ``fess_config.properties`` n'est pas utilisee. Definissez-la via les System Properties ou ``-Dfess.system.rag.chat.message.max.length``.
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Taille du fragment pour le surlignage de recherche
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Nombre de fragments pour le surlignage de recherche
     - ``3``
   * - ``rag.chat.content.fulltext.max.length``
     - Seuil de ``content_length`` au-dela duquel les documents utilisent des extraits en surbrillance plutot que le texte integral dans le contexte de reponse
     - ``3000``
   * - ``rag.chat.answer.highlight.fragment.size``
     - Taille du fragment de surlignage lors de l'extraction d'extraits de grands documents pour le contexte de reponse
     - ``1000``
   * - ``rag.chat.answer.highlight.number.of.fragments``
     - Nombre de fragments de surlignage lors de l'extraction d'extraits de grands documents pour le contexte de reponse
     - ``5``
   * - ``rag.chat.history.assistant.content``
     - Type de contenu a inclure dans l'historique de l'assistant ( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``
   * - ``rag.chat.history.titles.max.count``
     - Nombre maximum de titres de documents references conserves par tour en mode ``smart_summary``
     - ``5``

Parametres de generation
================

Dans |Fess| 15.7, les parametres de generation (nombre maximum de tokens, temperature, etc.) se configurent par fournisseur
et par type de prompt. Ces configurations sont gerees comme parametres de chaque plugin ``fess-llm-*``
et non comme configurations principales.

Pour les details, consultez la documentation de chaque fournisseur :

- :doc:`llm-ollama` - Parametres de generation Ollama
- :doc:`llm-openai` - Parametres de generation OpenAI
- :doc:`llm-gemini` - Parametres de generation Google Gemini

Configuration du contexte
================

Configuration du contexte passe au LLM depuis les resultats de recherche.

Configuration principale
--------

Les configurations suivantes s'effectuent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.context.max.documents``
     - Nombre maximum de documents a inclure dans le contexte
     - ``5``
   * - ``rag.chat.content.fields``
     - Champs a recuperer des documents
     - ``title,url,content,doc_id,content_title,content_description``

Configuration specifique au fournisseur
-----------------------

Les configurations suivantes s'effectuent dans ``fess_config.properties`` pour chaque fournisseur.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - Nombre maximum de caracteres du contexte
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - Nombre maximum de documents pertinents a selectionner lors de la phase d'evaluation

``{provider}`` contient le nom du fournisseur tel que ``ollama``, ``openai``, ``gemini``, etc.
``{promptType}`` contient le type de prompt tel que ``intent``, ``evaluation``, ``answer``, ``summary``, ``faq``, ``queryregeneration``,
``unclear``, ``noresults``, ``docnotfound``, ``direct``, etc.
La liste des types de prompt pris en charge est definie dans l'implementation ``*LlmClient`` de chaque plugin.

Pour les details, consultez la documentation de chaque fournisseur.

Champs de contenu
--------------------

Champs specifiables dans ``rag.chat.content.fields`` :

- ``title`` - Titre du document
- ``url`` - URL du document
- ``content`` - Corps du document
- ``doc_id`` - ID du document
- ``content_title`` - Titre du contenu
- ``content_description`` - Description du contenu

Prompt systeme
==================

Dans |Fess| 15.7, les prompts systeme sont definis dans le DI XML (``fess_llm++.xml``) de chaque plugin ``fess-llm-*``
et non dans les fichiers de proprietes.

Personnalisation des prompts
-------------------------

Pour personnaliser les prompts systeme, surchargez le fichier ``fess_llm++.xml`` dans le JAR du plugin.

1. Recuperez ``fess_llm++.xml`` dans le fichier JAR du plugin utilise
2. Apportez les modifications necessaires
3. Placez-le dans l'emplacement approprie sous ``app/WEB-INF/`` pour le surcharger

Des prompts systeme differents sont definis pour chaque type de prompt (analyse d'intention, evaluation, generation),
avec une optimisation adaptee a chaque usage.

Pour les details, consultez la documentation de chaque fournisseur :

- :doc:`llm-ollama` - Configuration des prompts Ollama
- :doc:`llm-openai` - Configuration des prompts OpenAI
- :doc:`llm-gemini` - Configuration des prompts Google Gemini

Gestion des sessions
==============

Configuration de la gestion des sessions de chat.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.session.timeout.minutes``
     - Delai d'expiration de la session (minutes)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Nombre maximum de sessions pouvant etre maintenues simultanement
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique de conversation
     - ``30``

Comportement des sessions
----------------

- Lorsqu'un utilisateur commence un nouveau chat, une nouvelle session est creee
- L'historique de conversation est sauvegarde dans la session, permettant un dialogue contextuel
- Les sessions sont automatiquement supprimees apres expiration du delai
- Lorsque l'historique depasse le nombre maximum de messages, les anciens messages sont supprimes

Controle de la concurrence
============

Le nombre de requetes simultanees vers le LLM est controle par fournisseur dans ``fess_config.properties``.

::

    # Nombre maximum de requetes simultanees par fournisseur (defaut : 5)
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=5
    rag.llm.gemini.max.concurrent.requests=5

    # Timeout d'attente pour l'obtention d'un permis de concurrence (millisecondes, defaut : 30000)
    rag.llm.ollama.concurrency.wait.timeout=30000

Considerations sur le controle de la concurrence
-----------------------

- Tenez compte egalement des limitations de debit cote fournisseur LLM
- Dans les environnements a forte charge, il est recommande de configurer des valeurs plus petites
- Lorsque la limite de concurrence est atteinte, les requetes entrent dans une file d'attente et sont traitees sequentiellement
- Si l'attente d'un permis depasse ``concurrency.wait.timeout``, la requete echoue avec une erreur de timeout

Mode d'historique de conversation
=================================

``rag.chat.history.assistant.content`` controle la maniere dont les reponses de l'assistant sont stockees dans l'historique de conversation.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Mode
     - Description
   * - ``smart_summary``
     - (Par defaut) Le corps de la reponse de l'assistant est omis de l'historique ; seuls la requete de recherche passee et les titres des documents references (au maximum ``rag.chat.history.titles.max.count`` elements) sont conserves par tour
   * - ``full``
     - Preserve la reponse entiere telle quelle
   * - ``source_titles``
     - Preserve uniquement les titres des sources
   * - ``source_titles_and_urls``
     - Preserve les titres et URLs des sources
   * - ``truncated``
     - Tronque la reponse a la limite maximale de caracteres
   * - ``none``
     - Ne preserve pas l'historique

.. note::

   En mode ``smart_summary``, le corps de la reponse est remplace par la requete de recherche et les titres references, ce qui preserve le contexte efficacement tout en reduisant l'utilisation des tokens.
   Les paires de messages utilisateur et assistant sont groupees en tours et empaquetees de maniere optimale dans un budget de caracteres.
   Les limites maximales de caracteres pour l'historique et le resume sont controlees par l'implementation ``LlmClient`` de chaque plugin ``fess-llm-*``.

Regeneration de requete
=======================

Lorsqu'aucun resultat de recherche n'est trouve ou qu'aucun resultat pertinent n'est identifie, le LLM regenere automatiquement la requete et relance la recherche.

- Avec zero resultats de recherche : Regeneration de requete avec raison ``no_results``
- Lorsqu'aucun document pertinent n'est trouve : Regeneration de requete avec raison ``no_relevant_results``
- Retombe sur la requete originale si la regeneration echoue

Cette fonctionnalite est activee par defaut et integree dans les flux RAG synchrones et en streaming.
Les prompts de regeneration de requete sont definis dans chaque plugin ``fess-llm-*``.

Rendu Markdown
==============

Les reponses du mode de recherche IA sont rendues au format Markdown.

- Les reponses du LLM sont analysees en Markdown et converties en HTML
- Le HTML converti est assaini, n'autorisant que les balises et attributs surs
- Prend en charge les titres, listes, blocs de code, tableaux, liens et autres syntaxes Markdown
- Cote client, ``marked.js`` et ``DOMPurify`` sont utilises ; cote serveur, le sanitizer OWASP

Utilisation de l'API
=========

La fonctionnalite de mode de recherche IA est accessible via API REST (API v2).
L'URL de base est ``http://<nom du serveur>/api/v2/``.

La Chat API fournit les trois points de terminaison suivants.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Point de terminaison
     - Description
   * - ``POST /api/v2/chat``
     - Completion RAG groupee (non-streaming)
   * - ``POST /api/v2/chat/stream``
     - Completion RAG en streaming (Server-Sent Events)
   * - ``DELETE /api/v2/chat/sessions/{session_id}``
     - Effacer l'historique de conversation d'une session

Les requetes sont envoyees avec un corps JSON de type ``Content-Type: application/json``.
Les requetes modifiant l'etat (``POST`` / ``DELETE``) necessitent un jeton CSRF (en-tete ``X-Fess-CSRF-Token``).
Les reponses sont encapsulees dans l'enveloppe commune ``response``.

.. note::

   Les points de terminaison ``/api/v1/chat`` au format parametres de formulaire disponibles dans |Fess| 15.5 et anterieur ont ete supprimes.
   Dans 15.7, utilisez l'API JSON sous ``/api/v2/``.

API non-streaming
-------------------

Point de terminaison : ``POST /api/v2/chat``

Corps de la requete (JSON) :

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
     - ID de session (pour continuer la conversation). Si omis, le serveur le cree et le retourne dans la reponse
   * - ``fields``
     - Non
     - Champs de filtre optionnels pour l'etape de recuperation (objet)
   * - ``fields.label``
     - Non
     - Filtre de recherche par etiquette
   * - ``extra_queries``
     - Non
     - Expressions de requete supplementaires pour les filtres de facettes

Exemple de requete :

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Comment installer Fess ?"}'

Exemple de reponse :

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

Le corps de la requete est identique a ``POST /api/v2/chat`` (JSON).
Les reponses sont streamees au format Server-Sent Events (SSE).

Exemple de requete :

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Quelles sont les caracteristiques de Fess ?"}'

Evenements SSE :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Evenement
     - Description (charge utile)
   * - ``phase``
     - Transition de phase du pipeline (``intent``, ``search``, ``evaluate``, ``fetch``, ``answer``). ``{ phase, status, message?, keywords?, hit_count?, ... }``
   * - ``chunk``
     - Fragment de texte genere (``{ content }``)
   * - ``retry``
     - Notifie lorsqu'une requete LLM est reessayee (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``)
   * - ``waiting``
     - Progression d'une phase longue telle que l'attente d'un permis de concurrence (``{ phase, reason, elapsed_ms, timeout_ms }``)
   * - ``fallback``
     - Notifie lorsque la requete est regeneree suite a l'absence de resultats ou de resultats pertinents (``{ phase, reason, original_query?, new_query? }``, raison : ``no_results`` ou ``no_relevant_results``)
   * - ``warning``
     - Notifie lors d'un avertissement recuperable (``{ phase, code, detail? }``, ex. epuisement des tokens d'un modele de raisonnement)
   * - ``sources``
     - Informations sur les documents sources (``{ sources: [...] }``)
   * - ``done``
     - Traitement termine (``{ session_id, html_content? }``). ``html_content`` contient la chaine HTML rendue depuis Markdown
   * - ``error``
     - Echec terminal en cours de stream (``{ phase?, message, error_code }``). Timeout, depassement de la longueur de contexte, modele introuvable, reponse invalide, erreur de connexion, etc.

Effacer une session
--------------------

Point de terminaison : ``DELETE /api/v2/chat/sessions/{session_id}``

Efface l'historique de conversation de la session specifiee. En cas de succes, ``cleared: true`` est retourne.

Pour la documentation API complete (authentification, CSRF, limites de debit, codes HTTP), consultez :doc:`../api/api-chat`.

Interface Web
===================

La fonctionnalite de mode de recherche IA est accessible depuis l'ecran de recherche de l'interface Web |Fess|.

Demarrer un chat
--------------

1. Accedez a l'ecran de recherche |Fess|
2. Cliquez sur l'icone de chat
3. Le panneau de chat s'affiche

Utiliser le chat
--------------

1. Entrez votre question dans la zone de texte
2. Cliquez sur le bouton d'envoi ou appuyez sur Entree
3. La reponse de l'assistant IA s'affiche
4. La reponse inclut des liens vers les sources

Continuer la conversation
----------

- Vous pouvez continuer la conversation dans la meme session de chat
- Les reponses tiennent compte du contexte des questions precedentes
- Cliquez sur "Nouveau chat" pour reinitialiser la session

Depannage
======================

Le bouton mode IA n'apparait pas sur l'ecran de recherche
---------------------------------------------------------

**Symptome** : Le bouton mode IA ne s'affiche pas dans l'en-tete des resultats
de recherche, et acceder a ``/chat`` redirige vers la page d'accueil.

**Liste de verifications** : verifier les points suivants dans l'ordre.

1. ``rag.chat.enabled=true`` est-il defini ?

   - Docker : ``-Dfess.config.rag.chat.enabled=true`` est-il inclus dans ``FESS_JAVA_OPTS`` ?
   - Installation par paquet : est-il ecrit dans ``app/WEB-INF/conf/fess_config.properties`` ?

2. Le plugin ``fess-llm-*`` correspondant est-il installe ?

   - Docker : ``FESS_PLUGINS=fess-llm-gemini:15.7.0`` (ou ``fess-llm-openai`` / ``fess-llm-ollama``) doit etre defini
   - Installation par paquet : le JAR doit etre place dans ``app/WEB-INF/plugin/``
   - Le journal de demarrage doit inclure ``Installing fess-llm-XXX-15.7.0.jar``

3. ``rag.llm.name`` correspond-il a un plugin installe ?

   - La valeur par defaut est ``ollama``. Si seul le plugin Gemini est installe, vous devez explicitement le definir a ``gemini`` (de meme ``openai`` pour le plugin OpenAI)
   - Methode (a) : modifier ``rag.llm.name`` depuis Administration > Systeme > General (section RAG) et enregistrer
   - Methode (b) : inclure ``-Dfess.system.rag.llm.name=gemini`` dans ``FESS_JAVA_OPTS`` au demarrage. N'agit que comme valeur par defaut initiale avant qu'une valeur ne soit persistee dans OpenSearch

4. Un WARN comme ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` se repete-t-il dans le journal ?

   - Symptome typique quand ``rag.llm.name`` est encore ``ollama`` mais que le plugin Ollama n'est pas installe
   - Definir ``rag.llm.name`` au fournisseur reellement utilise resout le probleme
   - De meme, ``componentName=geminiLlmClient`` indique que ``rag.llm.name=gemini`` est defini mais que le plugin ``fess-llm-gemini`` n'est pas installe

5. La cle d'API specifique au fournisseur est-elle configuree ?

   - Quand ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` est vide, ``checkAvailabilityNow`` retourne ``false`` et le mode IA est desactive
   - Activer DEBUG sur ``org.codelibs.fess.llm.gemini`` dans ``log4j2.xml`` fait apparaitre des messages comme ``[LLM:GEMINI] Gemini is not available. apiKey is blank``

6. L'hote Fess peut-il atteindre le fournisseur LLM ?

   - Pour les API cloud (Gemini / OpenAI), le conteneur doit avoir un acces sortant a Internet
   - En cas de proxy, definissez ``http.proxy.host`` / ``http.proxy.port`` (et au besoin ``http.proxy.username`` / ``http.proxy.password``) dans ``fess_config.properties``. Dans un environnement Docker, ajoutez ``-Dfess.config.http.proxy.host=... -Dfess.config.http.proxy.port=...`` a ``FESS_JAVA_OPTS`` (depuis |Fess| 15.7, les clients LLM partagent la configuration de proxy commune a |Fess|)

.. note::

   La page "General" n'expose pas de case a cocher pour ``rag.chat.enabled`` (par conception).
   Cette propriete de la famille FessConfig ne peut etre definie qu'a travers
   ``fess_config.properties`` ou ``-Dfess.config.rag.chat.enabled=true``.

Le mode de recherche IA ne s'active pas
------------------------

**Points a verifier** :

1. Verifier si ``rag.chat.enabled=true`` est configure
2. Verifier si le fournisseur LLM est correctement configure dans ``rag.llm.name``
3. Verifier si le plugin ``fess-llm-*`` correspondant est installe
4. Verifier si la connexion au fournisseur LLM est possible

Qualite des reponses insuffisante
----------------

**Ameliorations** :

1. Utiliser un modele LLM plus performant
2. Augmenter ``rag.chat.context.max.documents``
3. Personnaliser le prompt systeme dans le DI XML
4. Ajuster les parametres de temperature specifiques au fournisseur (consultez la documentation de chaque plugin ``fess-llm-*``)

Reponses lentes
----------------

**Ameliorations** :

1. Utiliser un modele LLM plus rapide (ex : Gemini Flash)
2. Reduire les parametres max.tokens specifiques au fournisseur (consultez la documentation de chaque plugin ``fess-llm-*``)
3. Reduire ``rag.chat.context.max.documents``

Sessions non maintenues
------------------------

**Points a verifier** :

1. Verifier si le ``session_id`` est correctement envoye cote client
2. Verifier le parametre ``rag.chat.session.timeout.minutes``
3. Verifier la capacite de stockage des sessions

Configuration de debogage
------------

Pour investiguer les problemes, ajustez le niveau de log pour afficher des logs detailles.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.v2.handlers" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Les messages de log utilisent le prefixe ``[RAG]``, avec des sous-prefixes tels que ``[RAG:INTENT]``, ``[RAG:EVAL]`` et ``[RAG:ANSWER]`` pour chaque phase.
Au niveau INFO, les logs de fin de chat (duree, nombre de sources) sont emis. Au niveau DEBUG, les details d'utilisation des tokens, de controle de concurrence et d'empaquetage de l'historique sont emis.

Journal de recherche et type d'acces
-------------------------------------

Les recherches via le mode de recherche IA sont enregistrees avec le nom du fournisseur LLM (par ex. ``ollama``, ``openai``, ``gemini``) comme type d'acces dans les journaux de recherche. Cela permet de distinguer les recherches du mode IA des recherches web ou API regulieres dans les analyses.

Informations de reference
========

- :doc:`llm-overview` - Apercu de l'integration LLM
- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini
- :doc:`../api/api-chat` - Reference API Chat
- :doc:`../user/chat-search` - Guide de recherche par chat pour les utilisateurs
