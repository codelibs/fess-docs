==========================
Configuration du mode de recherche IA
==========================

Apercu
====

Le mode de recherche IA (RAG: Retrieval-Augmented Generation) est une fonctionnalite qui enrichit les resultats de recherche de |Fess|
avec un LLM (grand modele de langage) pour fournir des informations sous forme de dialogue.
Les utilisateurs peuvent poser des questions en langage naturel et obtenir des reponses detaillees basees sur les resultats de recherche.

Dans |Fess| 15.6, la fonctionnalite LLM a ete separee en plugins ``fess-llm-*``.
La configuration principale et la configuration specifique au fournisseur LLM s'effectuent dans ``fess_config.properties``,
et la selection du fournisseur LLM (``rag.llm.name``) s'effectue dans ``system.properties`` ou via l'administration.

Fonctionnement du mode de recherche IA
================

Le mode de recherche IA fonctionne selon un flux en plusieurs etapes.

1. **Phase d'analyse d'intention** : Analyse la question de l'utilisateur et extrait les mots-cles optimaux pour la recherche
2. **Phase de recherche** : Recherche des documents avec les mots-cles extraits en utilisant le moteur de recherche |Fess|
3. **Phase d'evaluation** : Evalue la pertinence des resultats de recherche et selectionne les documents les plus appropries
4. **Phase de generation** : Le LLM genere une reponse basee sur les documents selectionnes
5. **Phase de sortie** : Retourne la reponse et les informations sources a l'utilisateur

Ce flux permet des reponses de haute qualite comprenant le contexte, superieur a la simple recherche par mots-cles.

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
     - ``20``
   * - ``rag.chat.intent.history.max.messages``
     - Nombre maximum de messages de l'historique de conversation utilises pour l'analyse d'intention
     - ``4``
   * - ``rag.chat.content.fields``
     - Champs a recuperer des documents
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Nombre maximum de caracteres du message utilisateur
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Taille du fragment pour l'affichage en surbrillance
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Nombre de fragments pour l'affichage en surbrillance
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - Type de contenu a inclure dans l'historique de l'assistant
     - ``source_titles``
   * - ``rag.chat.history.assistant.max.chars``
     - Nombre maximum de caracteres de l'historique de l'assistant
     - ``500``
   * - ``rag.chat.history.assistant.summary.max.chars``
     - Nombre maximum de caracteres du resume de l'historique de l'assistant
     - ``500``
   * - ``rag.chat.history.max.chars``
     - Nombre maximum de caracteres de l'historique de conversation
     - ``2000``

Parametres de generation
================

Dans |Fess| 15.6, les parametres de generation (nombre maximum de tokens, temperature, etc.) se configurent par fournisseur
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
``{promptType}`` contient le type de prompt tel que ``chat``, ``intent_analysis``, ``evaluation``, etc.

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

Dans |Fess| 15.6, les prompts systeme sont definis dans le DI XML (``fess_llm++.xml``) de chaque plugin ``fess-llm-*``
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
     - ``20``

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

    # Nombre maximum de requetes simultanees par fournisseur
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

Considerations sur le controle de la concurrence
-----------------------

- Tenez compte egalement des limitations de debit cote fournisseur LLM
- Dans les environnements a forte charge, il est recommande de configurer des valeurs plus petites
- Lorsque la limite de concurrence est atteinte, les requetes entrent dans une file d'attente et sont traitees sequentiellement

Utilisation de l'API
=========

La fonctionnalite de mode de recherche IA est accessible via API REST.

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
