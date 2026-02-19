==========================
Apercu de l'integration LLM
==========================

Apercu
====

|Fess| 15.5 prend en charge la fonctionnalite de mode IA (RAG: Retrieval-Augmented Generation) utilisant
les grands modeles de langage (LLM). Cette fonctionnalite permet aux utilisateurs d'obtenir des informations
sous forme de dialogue avec un assistant IA base sur les resultats de recherche.

Fournisseurs pris en charge
================

|Fess| prend en charge les fournisseurs LLM suivants.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Fournisseur
     - Valeur de configuration
     - Description
   * - Ollama
     - ``ollama``
     - Serveur LLM open source fonctionnant en local. Permet d'executer des modeles comme Llama, Mistral, Gemma. Configuration par defaut.
   * - OpenAI
     - ``openai``
     - API cloud d'OpenAI. Permet d'utiliser des modeles comme GPT-4.
   * - Google Gemini
     - ``gemini``
     - API cloud de Google. Permet d'utiliser les modeles Gemini.

Architecture
==============

La fonctionnalite de mode IA fonctionne selon le flux suivant.

1. **Entree utilisateur** : L'utilisateur saisit une question dans l'interface de chat
2. **Analyse d'intention** : Le LLM analyse la question de l'utilisateur et extrait les mots-cles de recherche
3. **Execution de la recherche** : Recherche de documents pertinents avec le moteur de recherche |Fess|
4. **Evaluation des resultats** : Le LLM evalue la pertinence des resultats de recherche et selectionne les meilleurs documents
5. **Generation de reponse** : Le LLM genere une reponse basee sur les documents selectionnes
6. **Citation des sources** : La reponse inclut des liens vers les documents sources

Configuration de base
========

Pour activer la fonctionnalite LLM, ajoutez les parametres suivants dans ``app/WEB-INF/conf/fess_config.properties``.

Activation du mode IA
-------------------

::

    # Activer la fonctionnalite de mode IA
    rag.chat.enabled=true

Selection du fournisseur LLM
---------------------

::

    # Specifier le fournisseur LLM (ollama, openai, gemini)
    rag.llm.type=ollama

Pour la configuration detaillee de chaque fournisseur, consultez les documents suivants.

- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini

Configuration commune
========

Elements de configuration communs a tous les fournisseurs LLM.

Parametres de generation
----------------

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
     - Aleatoire de la generation (0.0-1.0). Plus bas = reponses plus deterministes
     - ``0.7``

Configuration du contexte
----------------

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

Prompt systeme
------------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Ce prompt definit le comportement de base du LLM. Personnalisable selon les besoins.

Verification de disponibilite
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.availability.check.interval``
     - Intervalle de verification de disponibilite du LLM (secondes). 0 pour desactiver
     - ``60``

Ce parametre permet a |Fess| de verifier regulierement l'etat de connexion au fournisseur LLM.

Gestion des sessions
==============

Configuration relative aux sessions de chat.

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
     - Nombre maximum de sessions
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Nombre maximum de messages dans l'historique de conversation
     - ``20``

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

Configuration d'evaluation
========

Configuration relative a l'evaluation des resultats de recherche.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents a selectionner lors de la phase d'evaluation
     - ``3``

Etapes suivantes
============

- :doc:`llm-ollama` - Configuration detaillee d'Ollama
- :doc:`llm-openai` - Configuration detaillee d'OpenAI
- :doc:`llm-gemini` - Configuration detaillee de Google Gemini
- :doc:`rag-chat` - Configuration detaillee de la fonctionnalite de mode IA
