==========================
Configuration du mode IA
==========================

Apercu
====

Le mode IA (RAG: Retrieval-Augmented Generation) est une fonctionnalite qui enrichit les resultats de recherche de |Fess|
avec un LLM (grand modele de langage) pour fournir des informations sous forme de dialogue.
Les utilisateurs peuvent poser des questions en langage naturel et obtenir des reponses detaillees basees sur les resultats de recherche.

Fonctionnement du mode IA
=========================

Le mode IA fonctionne selon un flux en plusieurs etapes.

1. **Phase d'analyse d'intention** : Analyse la question de l'utilisateur et extrait les mots-cles optimaux pour la recherche
2. **Phase de recherche** : Recherche des documents avec les mots-cles extraits en utilisant le moteur de recherche |Fess|
3. **Phase d'evaluation** : Evalue la pertinence des resultats de recherche et selectionne les documents les plus appropries
4. **Phase de generation** : Le LLM genere une reponse basee sur les documents selectionnes
5. **Phase de sortie** : Retourne la reponse et les informations sources a l'utilisateur

Ce flux permet des reponses de haute qualite comprenant le contexte, superieur a la simple recherche par mots-cles.

Configuration de base
========

Configuration de base pour activer la fonctionnalite de mode IA.

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode IA
    rag.chat.enabled=true

    # Selectionner le fournisseur LLM (ollama, openai, gemini)
    rag.llm.type=ollama

Pour la configuration detaillee des fournisseurs LLM, consultez :

- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini

Parametres de generation
================

Parametres controlant le comportement de generation du LLM.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.max.tokens``
     - Nombre maximum de tokens a generer
     - ``4096``
   * - ``rag.chat.temperature``
     - Aleatoire de la generation (0.0-1.0)
     - ``0.7``

Configuration de temperature
---------------

- **0.0** : Reponses deterministes (toujours la meme reponse pour la meme entree)
- **0.3-0.5** : Reponses coherentes (appropriees pour les questions factuelles)
- **0.7** : Reponses equilibrees (par defaut)
- **1.0** : Reponses creatives (appropriees pour le brainstorming, etc.)

Configuration du contexte
================

Configuration du contexte passe au LLM depuis les resultats de recherche.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.context.max.documents``
     - Nombre maximum de documents a inclure dans le contexte
     - ``5``
   * - ``rag.chat.context.max.chars``
     - Nombre maximum de caracteres du contexte
     - ``4000``
   * - ``rag.chat.content.fields``
     - Champs a recuperer des documents
     - ``title,url,content,...``
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents a selectionner lors de l'evaluation
     - ``3``

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

Le prompt systeme definit le comportement de base du LLM.

Configuration par defaut
--------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Exemple de personnalisation
--------------

Pour prioriser les reponses en francais :

::

    rag.chat.system.prompt=Vous etes un assistant IA pour le moteur de recherche Fess. Repondez aux questions en vous basant sur les resultats de recherche fournis. Citez toujours vos sources en utilisant [1], [2], etc.

Personnalisation pour domaine specialise :

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

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
     - Nombre maximum de sessions simultanees
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique
     - ``20``

Comportement des sessions
----------------

- Lorsqu'un utilisateur commence un nouveau chat, une nouvelle session est creee
- L'historique de conversation est sauvegarde dans la session, permettant un dialogue contextuel
- Les sessions sont automatiquement supprimees apres expiration du delai
- Lorsque l'historique depasse le nombre maximum de messages, les anciens messages sont supprimes

Limitation de debit
==========

Configuration de limitation de debit pour prevenir la surcharge de l'API.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.rate.limit.enabled``
     - Activer la limitation de debit
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - Nombre maximum de requetes par minute
     - ``10``

Considerations sur la limitation de debit
--------------------

- Tenez compte egalement des limitations de debit cote fournisseur LLM
- Dans les environnements a forte charge, configurez des limites plus strictes
- Lorsque la limite est atteinte, un message d'erreur est affiche a l'utilisateur

Utilisation de l'API
=========

La fonctionnalite de mode IA est accessible via API REST.

API non-streaming
-------------------

Point de terminaison : ``POST /api/v1/chat``

Parametres :

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parametre
     - Requis
     - Description
   * - ``message``
     - Oui
     - Message de l'utilisateur
   * - ``sessionId``
     - Non
     - ID de session (pour continuer la conversation)
   * - ``clear``
     - Non
     - ``true`` pour effacer la session

Exemple de requete :

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Comment installer Fess ?"

Exemple de reponse :

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "La methode d'installation de Fess est...",
      "sources": [
        {"title": "Guide d'installation", "url": "https://..."}
      ]
    }

API streaming
-----------------

Point de terminaison : ``POST /api/v1/chat/stream``

Envoie les reponses en streaming au format Server-Sent Events (SSE).

Parametres :

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parametre
     - Requis
     - Description
   * - ``message``
     - Oui
     - Message de l'utilisateur
   * - ``sessionId``
     - Non
     - ID de session (pour continuer la conversation)

Exemple de requete :

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Quelles sont les caracteristiques de Fess ?" \
         -H "Accept: text/event-stream"

Evenements SSE :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Evenement
     - Description
   * - ``session``
     - Information de session (sessionId)
   * - ``phase``
     - Debut/fin de phase de traitement (intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - Fragment de texte genere
   * - ``sources``
     - Information sur les documents sources
   * - ``done``
     - Traitement termine (sessionId, htmlContent)
   * - ``error``
     - Information d'erreur

Pour la documentation API detaillee, consultez :doc:`../api/api-chat`.

Interface Web
===================

La fonctionnalite de mode IA est accessible depuis l'ecran de recherche de l'interface Web |Fess|.

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

Le mode IA ne s'active pas
--------------------------

**Points a verifier** :

1. Verifier si ``rag.chat.enabled=true`` est configure
2. Verifier si le fournisseur LLM est correctement configure
3. Verifier si la connexion au fournisseur LLM est possible

Qualite des reponses insuffisante
----------------

**Ameliorations** :

1. Utiliser un modele LLM plus performant
2. Augmenter ``rag.chat.context.max.documents``
3. Personnaliser le prompt systeme
4. Ajuster ``rag.chat.temperature``

Reponses lentes
----------------

**Ameliorations** :

1. Utiliser un modele LLM plus rapide (ex: Gemini Flash)
2. Reduire ``rag.chat.max.tokens``
3. Reduire ``rag.chat.context.max.chars``

Sessions non maintenues
------------------------

**Points a verifier** :

1. Verifier si le sessionId est correctement envoye cote client
2. Verifier le parametre ``rag.chat.session.timeout.minutes``
3. Verifier la capacite de stockage des sessions

Configuration de debogage
------------

Pour investiguer les problemes, ajustez le niveau de log pour afficher des logs detailles.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Informations de reference
========

- :doc:`llm-overview` - Apercu de l'integration LLM
- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini
- :doc:`../api/api-chat` - Reference API Chat
- :doc:`../user/chat-search` - Guide de recherche par chat pour les utilisateurs
