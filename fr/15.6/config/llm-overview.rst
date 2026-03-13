==========================
Apercu de l'integration LLM
==========================

Apercu
====

|Fess| 15.6 prend en charge la fonctionnalite de mode de recherche IA (RAG: Retrieval-Augmented Generation) utilisant
les grands modeles de langage (LLM). Cette fonctionnalite permet aux utilisateurs d'obtenir des informations
sous forme de dialogue avec un assistant IA base sur les resultats de recherche.

Dans |Fess| 15.6, la fonctionnalite d'integration LLM est fournie sous forme de plugins ``fess-llm-*``. Installez le plugin correspondant au fournisseur LLM que vous souhaitez utiliser.

Fournisseurs pris en charge
================

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
     - Serveur LLM open source fonctionnant en local. Permet d'executer des modeles comme Llama, Mistral, Gemma. Configuration par defaut.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - API cloud d'OpenAI. Permet d'utiliser des modeles comme GPT-4.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - API cloud de Google. Permet d'utiliser les modeles Gemini.

Installation du plugin
==============

Dans |Fess| 15.6, la fonctionnalite LLM est separee en plugins. Il est necessaire de placer le fichier JAR du plugin ``fess-llm-{provider}`` correspondant au fournisseur utilise dans le repertoire des plugins.

Par exemple, pour utiliser le fournisseur OpenAI, telechargez ``fess-llm-openai-15.6.0.jar`` et placez-le dans le repertoire suivant.

::

    app/WEB-INF/plugin/

Apres le placement, le plugin sera charge au redemarrage de |Fess|.

Architecture
==============

La fonctionnalite de mode de recherche IA fonctionne selon le flux suivant.

1. **Entree utilisateur** : L'utilisateur saisit une question dans l'interface de chat
2. **Analyse d'intention** : Le LLM analyse la question de l'utilisateur et extrait les mots-cles de recherche
3. **Execution de la recherche** : Recherche de documents pertinents avec le moteur de recherche |Fess|
4. **Evaluation des resultats** : Le LLM evalue la pertinence des resultats de recherche et selectionne les meilleurs documents
5. **Generation de reponse** : Le LLM genere une reponse basee sur les documents selectionnes
6. **Citation des sources** : La reponse inclut des liens vers les documents sources

Configuration de base
========

La configuration de la fonctionnalite LLM s'effectue dans deux emplacements.

Administration generale / system.properties
--------------------------------------

La configuration s'effectue dans l'administration generale ou dans ``system.properties``. Utilise pour la selection du fournisseur LLM.

::

    # Specifier le fournisseur LLM (ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
----------------------

La configuration s'effectue dans ``app/WEB-INF/conf/fess_config.properties``. Il s'agit des parametres charges au demarrage, permettant d'activer le mode de recherche IA, de configurer les sessions et l'historique, ainsi que les parametres specifiques au fournisseur (URL de connexion, cle API, parametres de generation, etc.).

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # Exemple de configuration specifique au fournisseur (cas OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

Pour la configuration detaillee de chaque fournisseur, consultez les documents suivants.

- :doc:`llm-ollama` - Configuration Ollama
- :doc:`llm-openai` - Configuration OpenAI
- :doc:`llm-gemini` - Configuration Google Gemini

Configuration commune
========

Elements de configuration communs a tous les fournisseurs LLM. Ces elements se configurent dans ``fess_config.properties``.

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
   * - ``rag.chat.content.fields``
     - Champs a recuperer des documents
     - ``title,url,content,...``

.. note::

   Le nombre maximum de caracteres du contexte (``context.max.chars``) a ete modifie en une configuration par fournisseur et par type de prompt. Configurez-le dans ``fess_config.properties`` sous la forme ``rag.llm.{provider}.{promptType}.context.max.chars``.

Prompt systeme
------------------

Dans |Fess| 15.6, les prompts systeme sont geres dans les fichiers DI XML de chaque plugin, et non dans les fichiers de proprietes.

Le prompt systeme est defini dans le fichier ``fess_llm++.xml`` inclus dans chaque plugin ``fess-llm-*``. Pour personnaliser les prompts, modifiez le fichier DI XML dans le repertoire des plugins.

Verification de disponibilite
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervalle de verification de disponibilite du LLM (secondes). 0 pour desactiver
     - ``60``

Cette configuration s'effectue dans ``fess_config.properties``. |Fess| verifie periodiquement l'etat de connexion au fournisseur LLM.

Gestion des sessions
==============

Configuration relative aux sessions de chat. Ces elements se configurent dans ``fess_config.properties``.

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

Controle de la concurrence
============

Configuration controlant le nombre de requetes simultanees vers le LLM. Se configure dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - Nombre maximum de requetes simultanees vers le fournisseur
     - ``5``

Par exemple, pour configurer la concurrence du fournisseur OpenAI :

::

    rag.llm.openai.max.concurrent.requests=10

Configuration d'evaluation
========

Configuration relative a l'evaluation des resultats de recherche. Se configure dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents a selectionner lors de la phase d'evaluation
     - ``3``

Configuration par type de prompt
======================

Dans |Fess| 15.6, les parametres de generation peuvent etre configures par type de prompt. Cela permet des ajustements fins selon l'usage. La configuration s'effectue dans ``fess_config.properties``.

Liste des types de prompt
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Type de prompt
     - Valeur de configuration
     - Description
   * - Analyse d'intention
     - ``intent``
     - Analyse la question de l'utilisateur et extrait les mots-cles de recherche
   * - Evaluation
     - ``evaluation``
     - Evalue la pertinence des resultats de recherche
   * - Question peu claire
     - ``unclear``
     - Genere une reponse lorsque la question est peu claire
   * - Aucun resultat
     - ``noresults``
     - Genere une reponse lorsqu'aucun resultat de recherche n'est trouve
   * - Document absent
     - ``docnotfound``
     - Genere une reponse lorsque le document correspondant n'existe pas
   * - Generation de reponse
     - ``answer``
     - Genere une reponse basee sur les resultats de recherche
   * - Resume
     - ``summary``
     - Genere un resume du document
   * - FAQ
     - ``faq``
     - Genere une reponse au format FAQ
   * - Reponse directe
     - ``direct``
     - Genere une reponse directe sans passer par la recherche

Patterns de configuration
------------

La configuration par type de prompt se specifie selon le pattern suivant.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Exemple de configuration (cas du fournisseur OpenAI) :

::

    # Configurer une temperature basse pour la generation de reponse
    rag.llm.openai.answer.temperature=0.5
    # Nombre maximum de tokens pour la generation de reponse
    rag.llm.openai.answer.max.tokens=4096
    # Configurer bas car une reponse courte suffit pour l'analyse d'intention
    rag.llm.openai.intent.max.tokens=256
    # Nombre maximum de caracteres du contexte pour le resume
    rag.llm.openai.summary.context.max.chars=8000

Etapes suivantes
============

- :doc:`llm-ollama` - Configuration detaillee d'Ollama
- :doc:`llm-openai` - Configuration detaillee d'OpenAI
- :doc:`llm-gemini` - Configuration detaillee de Google Gemini
- :doc:`rag-chat` - Configuration detaillee de la fonctionnalite de mode de recherche IA
- :doc:`rank-fusion` - Configuration du Rank Fusion (Fusion des resultats de recherche hybride)
