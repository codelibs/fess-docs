=================================================
Interroger les documents internes avec l'IA (RAG)
=================================================

Introduction
============

Plutôt que d'ouvrir les résultats de recherche un par un pour les comparer, on souhaite souvent poser une question comme « Quelle est la date limite des notes de frais ? » et obtenir une réponse fondée sur les documents internes.
Le mode de recherche IA de Fess (chat RAG) fait rechercher par Fess lui-même les documents liés à la question, transmet leur contenu à un LLM (grand modèle de langage) pour qu'il rédige une réponse, puis renvoie cette réponse accompagnée de liens vers les documents sur lesquels elle s'appuie.

Cet article explique comment faire fonctionner le mode de recherche IA avec Fess 15.9, restreindre les personnes qui peuvent l'utiliser et les documents qu'il consulte, puis vérifier son fonctionnement dans la page de recherche et via l'API.
À l'issue des étapes de cet article, vous saurez :

- Choisir l'un des quatre fournisseurs de LLM et installer le plugin et les paramètres correspondants
- Connecter un LLM à Fess sous Docker à l'aide des fichiers Compose de superposition fournis par docker-fess
- Restreindre les utilisateurs autorisés à utiliser le chat et les documents sur lesquels les réponses s'appuient
- Vérifier le fonctionnement dans la page de recherche, via ``/api/v2/chat`` et dans le journal de recherche

Au préalable, Fess doit être démarré et des documents doivent déjà avoir été explorés.
Si ce n'est pas le cas, préparez-les en suivant les étapes de :doc:`guide-02`.
La recherche sémantique, qui trouve des documents de sens proche, est traitée dans :doc:`guide-18`, et MCP, qui permet à des agents IA d'effectuer des recherches dans Fess, dans :doc:`guide-20`.

Fonctionnement du mode de recherche IA
======================================

Le mode de recherche IA n'utilise pas d'index vectoriel dédié.
Il trouve les documents avec le même traitement que la recherche ordinaire (recherche par mots-clés par défaut) ; vous pouvez donc commencer sans préparer de modèle d'embedding ni de découpage en chunks.
Si la recherche sémantique est activée, elle est automatiquement intégrée aux recherches du mode de recherche IA.

Le déroulement du traitement dépend du point de terminaison appelé.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Point de terminaison
     - Déroulement du traitement
   * - ``POST /api/v2/chat/stream`` (utilisé par la recherche IA de la page de recherche)
     - Détection de l'intention → recherche → évaluation de la pertinence par le LLM → récupération du contenu des documents → génération de la réponse. La progression de chaque étape et les fragments de la réponse sont renvoyés au fur et à mesure sous forme de Server-Sent Events
   * - ``POST /api/v2/chat``
     - Détection de l'intention → recherche → génération de la réponse. Il n'y a pas d'évaluation de la pertinence, et le résultat est renvoyé dans un seul JSON

Dans les deux cas, lorsqu'une recherche ne renvoie aucun résultat, le LLM reformule les termes de recherche et relance la recherche (jusqu'à 2 fois par défaut, ``rag.chat.query.regeneration.max.count``).
Comme une seule question appelle le LLM plusieurs fois, les réponses prennent plus de temps qu'une recherche ordinaire, et avec un LLM dans le cloud, chaque appel est facturé.

Le LLM reçoit la question de l'utilisateur ainsi que le contenu ou des extraits des documents trouvés par la recherche.
Lors du choix d'un fournisseur, vérifiez où ces données sont envoyées.

Les conversations sont identifiées par ``session_id`` et conservées dans la mémoire de Fess.
Par défaut, une conversation est supprimée après 30 minutes d'inactivité (``rag.chat.session.timeout.minutes``), et chaque conversation conserve au maximum 30 messages (``rag.chat.history.max.messages``).
Les conversations sont également perdues lors d'un redémarrage de Fess.

Choisir un fournisseur de LLM
=============================

Dans Fess 15.9, la connexion à un LLM est fournie par un plugin ``fess-llm-*`` propre à chaque fournisseur.
Le fournisseur à utiliser est indiqué par ``rag.llm.name``.

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - Fournisseur
     - ``rag.llm.name``
     - Plugin
     - Modèle par défaut
     - Paramètres nécessaires à la connexion, et destination des questions et des documents
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url`` (par défaut ``http://localhost:11434``). Les données sont envoyées au serveur Ollama que vous exploitez vous-même
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``. Les données sont envoyées à OpenAI
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``. Les données sont envoyées à Google
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region`` (par défaut ``us-east-1``), ainsi que ``rag.llm.bedrock.api.key`` ou des identifiants AWS. Les données sont envoyées à Amazon Bedrock dans la région indiquée

Le modèle peut être changé avec ``rag.llm.<fournisseur>.model``.

Avec OpenAI et Gemini, une clé d'API suffit pour démarrer, mais les questions et les documents sont envoyés au service concerné.
Ollama ne fait pas sortir les questions et les documents de vos propres serveurs, mais il faut un serveur pour exécuter le modèle.
Le fichier Compose de docker-fess pour Ollama suppose un GPU NVIDIA.
Bedrock nécessite des identifiants AWS et le choix d'une région.
Pour la configuration, consultez `Configuration d'Amazon Bedrock <https://fess.codelibs.org/fr/stable/config/llm-bedrock.html>`__.

Trois éléments à configurer
===========================

Le mode de recherche IA ne fonctionne que si les trois éléments suivants sont réunis.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Paramètre
     - Où le définir
     - Comment le transmettre sous Docker
   * - ``rag.chat.enabled=true`` (par défaut ``false``)
     - ``fess_config.properties``. L'interface d'administration ne propose aucun champ pour ce paramètre
     - ``-Dfess.config.rag.chat.enabled=true`` dans ``FESS_JAVA_OPTS``
   * - Un plugin ``fess-llm-*``
     - [Système] > [Plugin], ou ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0``, etc.
   * - ``rag.llm.name`` et les paramètres de connexion propres à chaque fournisseur
     - ``rag.llm.name`` dans [Système] > [Général], les paramètres de connexion (``rag.llm.<fournisseur>.*``) dans ``fess_config.properties``
     - ``-Dfess.system.rag.llm.name=openai``, ``-Dfess.config.rag.llm.openai.api.key=...``, etc.

La valeur par défaut de ``rag.llm.name`` est ``ollama``.
Si vous n'installez que le plugin OpenAI sans modifier ``rag.llm.name``, Fess continue de chercher un client Ollama inexistant, et le mode de recherche IA est inutilisable.
Dans ce cas, l'avertissement ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` apparaît dans le journal.

``-Dfess.system.rag.llm.name`` est une valeur initiale utilisée uniquement lorsque ``system.properties`` ne contient pas de valeur.
Dès qu'une valeur enregistrée dans [Général] est écrite dans ``system.properties``, c'est elle qui prévaut.

Exécuter sous Docker (OpenAI et Gemini)
=======================================

docker-fess fournit des fichiers Compose de superposition pour connecter un LLM.
Dans le répertoire où vous avez placé les fichiers Compose dans :doc:`guide-02`, téléchargez le fichier de la v15.9.0.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

Placez la clé d'API dans une variable d'environnement du shell, puis démarrez en indiquant les trois fichiers.

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` ajoute les variables d'environnement suivantes à ``fess01``.
La clé d'API et le nom du modèle proviennent des variables ``OPENAI_API_KEY`` et ``OPENAI_MODEL`` du shell (``gpt-5-mini`` si elle n'est pas définie) ; vous n'avez donc pas à écrire la clé dans le fichier.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Les plugins de ``FESS_PLUGINS`` sont installés au démarrage du conteneur, avant Fess lui-même ; aucun redémarrage supplémentaire n'est donc nécessaire.
Si ``fess01`` est déjà en cours d'exécution, cette commande recrée ``fess01``, et les paramètres que vous aviez modifiés dans [Général] disparaissent avec le conteneur.
Indiquez également les trois mêmes fichiers pour les commandes suivantes, comme ``ps``, ``logs`` et ``down``.

Pour Gemini, téléchargez ``compose-gemini.yaml``, définissez ``GEMINI_API_KEY`` et indiquez-le de la même façon comme troisième fichier.
Ce fichier définit le modèle à partir de ``GEMINI_MODEL`` (``gemini-2.5-flash`` si elle n'est pas définie) ; c'est donc ``gemini-2.5-flash`` qui est utilisé, et non le modèle par défaut du plugin.

.. note::

   Si vous indiquez deux fichiers de superposition ou plus qui définissent ``FESS_JAVA_OPTS`` (par exemple en combinaison avec des paramètres pour l'OCR), seule la valeur du dernier fichier est utilisée.
   Dans ce cas, préparez votre propre fichier Compose qui regroupe toutes les options ``-D`` nécessaires dans un seul ``FESS_JAVA_OPTS``.
   ``FESS_JAVA_OPTS`` est découpé sur les espaces ; il est donc impossible d'y écrire des options dont la valeur contient des espaces.

Une clé d'API transmise comme ``-Dfess.config.rag.llm.openai.api.key`` est affichée masquée dans [Informations système] > [Informations de configuration].
Si vous devez passer par un proxy interne pour sortir vers l'extérieur, ajoutez ``-Dfess.config.http.proxy.host=...`` et ``-Dfess.config.http.proxy.port=...``.
Les plugins LLM utilisent les paramètres de proxy communs de Fess.

Exécuter sous Docker (Ollama)
=============================

``compose-ollama.yaml`` ajoute un conteneur Ollama, ``ollama01``, et y connecte ``fess01``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Cible
     - Ce qui est configuré
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``, ``-Dfess.config.rag.chat.enabled=true``, ``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - Image ``ollama/ollama:latest``, réseau ``search_net``, port 11434, volume ``ollama-data`` et attribution d'un GPU NVIDIA

``rag.llm.name`` et le modèle ne sont pas définis ; les valeurs par défaut ``ollama`` et ``gemma4:e4b`` sont donc utilisées.
L'URL pointe vers ``ollama01``, car la valeur par défaut ``http://localhost:11434`` désignerait le conteneur ``fess01`` lui-même.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

Ce fichier nécessite un environnement où NVIDIA Container Toolkit est installé.
Pour essayer dans un environnement sans GPU, supprimez la section ``deploy:`` de ``ollama01`` dans le fichier téléchargé.
Le modèle s'exécute alors sur le CPU, et les réponses prennent du temps.

Fess ne considère Ollama comme disponible que si le modèle configuré figure dans la liste des modèles d'Ollama (``/api/tags``), et il effectue cette vérification toutes les 60 secondes par défaut.
C'est pourquoi le mode de recherche IA devient utilisable environ une minute après le téléchargement du modèle.
Les commentaires en tête du fichier mentionnent un autre nom de fichier et une procédure de téléchargement de ``gpt-oss:20b``, mais suivez la procédure ci-dessus.
Pour utiliser un autre modèle, téléchargez-le avec ``ollama pull``, puis ajoutez ``-Dfess.config.rag.llm.ollama.model=<nom-du-modèle>`` à ``FESS_JAVA_OPTS``.

Configurer sans Docker (ZIP, RPM et DEB)
========================================

1. Installez le plugin. Sélectionnez-le dans [Système] > [Plugin] > [Installer], ou installez-le en ligne de commande

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. Ajoutez les paramètres à ``fess_config.properties``. Il s'agit de ``app/WEB-INF/classes/fess_config.properties`` pour le paquet ZIP et de ``/etc/fess/fess_config.properties`` pour les paquets RPM/DEB

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. Redémarrez Fess. Le plugin comme les modifications de ``fess_config.properties`` sont chargés au redémarrage
4. Ouvrez [Système] > [Général], sélectionnez ``openai`` dans « Fournisseur LLM » de la section « Recherche IA », puis cliquez sur [Mettre à jour]

La section « Recherche IA » n'est affichée que si ``rag.chat.enabled=true`` est défini et qu'au moins un plugin LLM est chargé.
Les choix proposés dans « Fournisseur LLM » se limitent aux fournisseurs des plugins installés.
Si vous ne trouvez pas la section, revoyez les étapes 1 à 3.

Vérifier le fonctionnement
==========================

Vérifier dans la page de recherche
----------------------------------

1. Ouvrez ``http://localhost:8080/``. [Recherche IA], accompagné d'une icône de robot, apparaît dans la barre de navigation en haut
2. Cliquez sur [Recherche IA] pour ouvrir la page de chat (``/chat``)
3. Saisissez une question à laquelle les documents explorés devraient pouvoir répondre. Si vous avez exploré le Guide de recherche dans :doc:`guide-02`, vous pouvez essayer par exemple « Quels caractères puis-je utiliser dans une recherche avec caractères génériques ? »

Pendant la génération de la réponse, les étapes Analyse, Recherche, Évaluation, Récupération et Réponse s'affichent successivement.
Sous la réponse, les documents sur lesquels elle s'appuie sont listés et numérotés sous « Sources », et ces numéros correspondent aux renvois tels que ``[1]`` dans le texte.
Pour changer de sujet, cliquez sur [Nouvelle conversation] : l'historique de la conversation est effacé.

Si [Recherche IA] n'apparaît pas, consultez la section « Pièges courants » plus bas.

Vérifier via l'API
------------------

Pour vérifier sans passer par la page, appelez ``/api/v2/ui/config``.
Si ``response.features.rag_chat_enabled`` vaut ``true``, cet utilisateur peut utiliser le mode de recherche IA.

Les requêtes qui modifient un état, comme ``/api/v2/chat``, doivent envoyer un jeton CSRF lié à la session dans l'en-tête ``X-Fess-CSRF-Token``.
La réponse de ``/api/v2/ui/config`` contient ce jeton : récupérez-le en enregistrant les cookies, puis effectuez l'appel avec les mêmes cookies (l'exemple utilise ``jq``).

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"Quels caractères puis-je utiliser dans une recherche avec caractères génériques ?"}' | jq '.response'

Dans la réponse, ``content`` est la réponse, ``sources`` liste les documents sur lesquels elle s'appuie (``rank``, ``title``, ``url``, etc.) et ``session_id`` est l'identifiant de la conversation.
Pour poser une question de suivi, renvoyez le ``session_id``, par exemple ``{"message":"...","session_id":"<session_id précédent>"}``.

Cet exemple appelle l'API en tant qu'utilisateur anonyme non connecté ; seuls les documents portant ``{role}guest`` sont donc recherchés.
Pour savoir comment appeler l'API en tant qu'utilisateur connecté, quels événements renvoie la version en streaming ``/api/v2/chat/stream`` et quels sont les codes d'erreur, consultez `Chat API <https://fess.codelibs.org/fr/stable/api/api-chat.html>`__ et `Vue d'ensemble de l'API <https://fess.codelibs.org/fr/stable/api/api-overview.html>`__.
``/api/v1/chat`` est une API d'ancien format, disponible uniquement si le plugin ``fess-webapp-v1-api`` est installé.
Pour toute nouvelle intégration, utilisez ``/api/v2/chat``.

Vérifier dans l'interface d'administration et les journaux
----------------------------------------------------------

L'onglet [Chat IA] de [Informations système] > [Journal de recherche] affiche le nombre de requêtes, le nombre d'utilisateurs, le nombre total de jetons, le temps de réponse moyen et le taux d'erreur, ainsi que les décomptes par utilisateur, par intention et par modèle.
Cet enregistrement est activé par ``rag.chat.log.enabled`` (par défaut ``true``), et le texte des questions et des réponses n'est pas enregistré.
Le nombre de jetons n'est enregistré que si le plugin LLM le communique.

Sous Docker, vous pouvez vérifier dans le journal du conteneur si le plugin a été installé.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

Si ``Installing fess-llm-openai-15.9.0.jar`` apparaît, le plugin est installé.
Si ``[LLM] LlmClient not found`` apparaît ensuite de façon répétée, ``rag.llm.name`` ne correspond pas au plugin installé.

Restreindre les utilisateurs et les documents consultés
=======================================================

Les recherches du mode de recherche IA sont filtrées par rôle, comme la recherche ordinaire.
Les documents qu'un utilisateur ne peut pas voir dans les résultats de recherche ne servent ni de fondement aux réponses ni de sources.
Les documents visibles par chacun sont déterminés par les « Autorisations » de la configuration d'exploration.
Pour la démarche de conception, consultez :doc:`guide-05`.

En complément, vous pouvez restreindre l'utilisation du chat lui-même dans la section « Recherche IA » de [Système] > [Général].

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Champ
     - Description
   * - « Autorisations du chat » (``rag.chat.permissions``)
     - Indique les utilisateurs autorisés à utiliser le chat, sous forme de liste séparée par des virgules, par exemple ``{role}rag_user,{group}sales,{user}taro``. Si le champ est vide, tout le monde peut l'utiliser. Pour l'ouvrir aussi aux utilisateurs non connectés, incluez ``{role}guest``
   * - « Libellés du chat » (``rag.chat.labels``)
     - Limite les documents sur lesquels s'appuient les réponses à ceux qui portent l'une des valeurs d'étiquette indiquées. Indiquez-les sous forme de liste séparée par des virgules, par exemple ``faq,policy`` ; si le champ est vide, tous les documents visibles par l'utilisateur sont pris en compte

Les utilisateurs non couverts par « Autorisations du chat » ne voient pas [Recherche IA], et l'API renvoie 401 s'ils ne sont pas connectés, ou 403 s'ils le sont.
Les utilisateurs connectés ne possèdent pas ``{role}guest`` ; si vous n'indiquez que ``{role}guest``, les utilisateurs connectés ne peuvent donc plus utiliser le chat.
Si vous enregistrez une valeur sans aucune entrée valide (``{role}`` seul, par exemple), plus personne ne peut utiliser le chat.

« Libellés du chat » sert lorsque vous voulez que les réponses proviennent uniquement de documents jugés fiables comme fondement, par exemple les règlements internes et les FAQ, auxquels vous avez attribué une étiquette au préalable.
Pour créer et attribuer des étiquettes, consultez :doc:`guide-04`.

Pièges courants
===============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptôme
     - Points à vérifier
   * - [Recherche IA] n'apparaît pas
     - Vérifiez dans l'ordre suivant. (1) ``rag.chat.enabled=true`` est-il bien transmis ? (2) Le plugin est-il installé (``Installing`` dans le journal) ? (3) ``rag.llm.name`` correspond-il au plugin installé (avertissement ``LlmClient not found``) ? (4) La clé d'API est-elle renseignée et, pour Ollama, le modèle a-t-il été téléchargé ? (5) N'êtes-vous pas exclu des « Autorisations du chat » ?
   * - La section « Recherche IA » est absente de [Général]
     - Soit ``rag.chat.enabled`` est resté à ``false``, soit aucun plugin LLM n'est chargé. Vérifiez que vous avez redémarré Fess après avoir défini le paramètre et installé le plugin
   * - « Fournisseur LLM » est revenu à l'ancienne valeur après ``down`` et ``up -d``
     - Les valeurs de [Général] sont enregistrées dans ``system.properties`` à l'intérieur du conteneur ``fess01`` et disparaissent lorsque le conteneur est recréé. Indiquez la valeur avec ``-Dfess.system.rag.llm.name`` dans ``FESS_JAVA_OPTS``
   * - L'API renvoie ``403``
     - Vérifiez que vous envoyez le jeton CSRF dans ``X-Fess-CSRF-Token`` et que vous envoyez les cookies obtenus lors de la récupération du jeton. Un utilisateur connecté exclu des « Autorisations du chat » reçoit également 403
   * - L'API renvoie ``429``
     - Chaque utilisateur est limité à 30 requêtes par minute (``api.chat.rate.limit.per.user.per.minute``)
   * - Impossible de se connecter à un LLM dans le cloud
     - Vérifiez que le conteneur peut accéder à l'extérieur et, si un proxy est nécessaire, définissez ``http.proxy.host`` et ``http.proxy.port``

Pour améliorer la qualité des réponses, vérifiez d'abord la qualité de la recherche.
Le mode de recherche IA s'appuie sur les documents les mieux classés d'une recherche ordinaire (5 par défaut, ``rag.chat.context.max.documents``) ; si une recherche avec les mots de la question fait remonter des documents sans rapport, la réponse en sera elle aussi affectée.
L'amélioration de la recherche est traitée dans :doc:`guide-08`.
Pour la température et le nombre maximal de jetons par type de prompt, ainsi que pour le remplacement des prompts, consultez `Vue d'ensemble du mode de recherche IA (RAG) et de l'intégration LLM <https://fess.codelibs.org/fr/stable/config/llm-overview.html>`__.

Pour aller plus loin
====================

- Ajouter aux résultats des documents de sens proche même lorsque les mots-clés ne correspondent pas : :doc:`guide-18`
- Permettre à des agents IA comme Claude d'effectuer des recherches dans Fess : :doc:`guide-20`
- Séparer les documents consultables selon le service ou le rôle : :doc:`guide-05`
- Améliorer la qualité de la recherche à partir du journal de recherche : :doc:`guide-08`
- Faire se connecter les utilisateurs par SSO et adapter les documents affichés à chacun : :doc:`guide-15`

Références
==========

- `Configuration du mode de recherche IA <https://fess.codelibs.org/fr/stable/config/rag-chat.html>`__
- `Vue d'ensemble du mode de recherche IA (RAG) et de l'intégration LLM <https://fess.codelibs.org/fr/stable/config/llm-overview.html>`__
- `Configuration Ollama <https://fess.codelibs.org/fr/stable/config/llm-ollama.html>`__
- `Configuration OpenAI <https://fess.codelibs.org/fr/stable/config/llm-openai.html>`__
- `Configuration Google Gemini <https://fess.codelibs.org/fr/stable/config/llm-gemini.html>`__
- `Configuration d'Amazon Bedrock <https://fess.codelibs.org/fr/stable/config/llm-bedrock.html>`__
- `Chat API <https://fess.codelibs.org/fr/stable/api/api-chat.html>`__
- `Mode de recherche IA (pour les utilisateurs) <https://fess.codelibs.org/fr/stable/user/chat-search.html>`__
- `Plugins <https://fess.codelibs.org/fr/stable/admin/plugin-guide.html>`__
- `Répertoire compose de docker-fess (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
