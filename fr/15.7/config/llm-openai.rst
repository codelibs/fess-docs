==========================
Configuration OpenAI
==========================

Aperçu
====

OpenAI est un service cloud fournissant des grands modèles de langage (LLM) haute performance,
dont GPT-4. |Fess| peut utiliser l'API OpenAI pour réaliser la fonctionnalité de mode de recherche IA.

L'utilisation d'OpenAI permet de générer des réponses de haute qualité avec les modèles d'IA les plus avancés.

Caractéristiques principales
--------

- **Réponses de haute qualité** : Génération de réponses précises avec les derniers modèles GPT
- **Évolutivité** : Mise à l'échelle facile grâce au service cloud
- **Amélioration continue** : Performances améliorées grâce aux mises à jour régulières des modèles
- **Fonctionnalités riches** : Prise en charge de diverses tâches comme la génération de texte, le résumé, la traduction

Modèles pris en charge
----------

Principaux modèles disponibles avec OpenAI :

- ``gpt-5`` - Dernier modèle haute performance
- ``gpt-5-mini`` - Version allégée de GPT-5 (bon rapport coût-efficacité)
- ``gpt-4o`` - Modèle multimodal haute performance
- ``gpt-4o-mini`` - Version allégée de GPT-4o
- ``o3-mini`` - Modèle léger spécialisé dans le raisonnement
- ``o4-mini`` - Modèle léger de nouvelle génération spécialisé dans le raisonnement

.. note::
   Pour les derniers modèles disponibles, consultez `OpenAI Models <https://platform.openai.com/docs/models>`__.

.. note::
   Lors de l'utilisation de modèles de la série o1/o3/o4 ou de la série gpt-5, |Fess| utilise automatiquement le paramètre ``max_completion_tokens`` de l'API OpenAI. Aucune modification de configuration n'est nécessaire.

Prérequis
========

Avant d'utiliser OpenAI, préparez les éléments suivants.

1. **Compte OpenAI** : Créez un compte sur `https://platform.openai.com/ <https://platform.openai.com/>`__
2. **Clé API** : Générez une clé API dans le tableau de bord OpenAI
3. **Configuration de facturation** : Configurez les informations de facturation car l'utilisation de l'API est payante

Obtention de la clé API
-------------

1. Connectez-vous à `OpenAI Platform <https://platform.openai.com/>`__
2. Accédez à la section "API keys"
3. Cliquez sur "Create new secret key"
4. Entrez un nom pour la clé et créez-la
5. Enregistrez la clé affichée en lieu sûr (elle ne sera affichée qu'une seule fois)

.. warning::
   La clé API est une information confidentielle. Faites attention aux points suivants :

   - Ne pas la commiter dans un système de gestion de versions
   - Ne pas l'afficher dans les logs
   - La gérer via des variables d'environnement ou des fichiers de configuration sécurisés

Installation du plugin
========================

La fonctionnalité d'intégration OpenAI est fournie sous forme de plugin. Pour l'utiliser, l'installation du plugin ``fess-llm-openai`` est nécessaire.

1. Téléchargez `fess-llm-openai-15.7.0.jar`
2. Placez le fichier JAR dans le répertoire ``app/WEB-INF/plugin/`` du répertoire d'installation de |Fess|::

    cp fess-llm-openai-15.7.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Redémarrez |Fess|

.. note::
   La version du plugin doit correspondre à la version de |Fess|.

Configuration de base
========

Les éléments de configuration sont répartis dans les deux fichiers suivants selon leur usage.

- ``app/WEB-INF/conf/fess_config.properties`` - Configuration principale de |Fess| et configuration spécifique au fournisseur LLM
- ``system.properties`` - Sélection du fournisseur LLM (``rag.llm.name``), à configurer via l'administration (Administration > Système > Général) ou directement dans le fichier

Configuration minimale
--------

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # Cle API OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modele a utiliser
    rag.llm.openai.model=gpt-5-mini

``system.properties`` (configurable également via Administration > Système > Général) :

::

    # Definir le fournisseur LLM sur OpenAI
    rag.llm.name=openai

Configuration recommandée (environnement de production)
--------------------

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # Cle API OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuration du modele (utiliser un modele haute performance)
    rag.llm.openai.model=gpt-4o

    # Point de terminaison API (generalement pas besoin de modifier)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Configuration du timeout
    rag.llm.openai.timeout=120000

    # Limite du nombre de requetes simultanees
    rag.llm.openai.max.concurrent.requests=5

``system.properties`` (configurable également via Administration > Système > Général) :

::

    # Configuration du fournisseur LLM
    rag.llm.name=openai

Éléments de configuration
========

Tous les éléments de configuration disponibles pour le client OpenAI. Sauf ``rag.llm.name``, tous se configurent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - Propriété
     - Description
     - Valeur par défaut
     - Emplacement
   * - ``rag.llm.name``
     - Nom du fournisseur LLM (spécifier ``openai``)
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - Clé API OpenAI
     - (Requis)
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - Nom du modèle à utiliser
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - URL de base de l'API
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - Timeout de la requête (millisecondes)
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - Intervalle de vérification de disponibilité (secondes)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - Nombre maximum de requêtes simultanées
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents lors de l'évaluation
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - Timeout d'attente des requêtes simultanées (ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - Multiplicateur de max tokens pour les modèles de raisonnement
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429`` et ``5xx``)
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - Délai de base du backoff exponentiel (millisecondes)
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - Envoyer ``stream_options.include_usage=true`` en streaming et recevoir les informations d'utilisation des tokens dans le dernier chunk
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - Nombre maximum de caractères pour l'historique de conversation
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - Nombre maximum de messages d'historique pour la détection d'intention
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - Nombre maximum de caractères d'historique pour la détection d'intention
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - Nombre maximum de caractères pour les messages de l'assistant
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - Nombre maximum de caractères pour le résumé de l'assistant
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - Nombre maximum de caractères pour la description de document en évaluation
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - Activation de la fonctionnalité de mode de recherche IA
     - ``false``
     - fess_config.properties

Configuration par type de prompt
======================

Dans |Fess|, des paramètres individuels peuvent être configurés pour chaque type de prompt. La configuration s'effectue dans ``fess_config.properties``.

Patterns de configuration
------------

La configuration par type de prompt se spécifie selon les patterns suivants :

- ``rag.llm.openai.{promptType}.temperature`` - Caractère aléatoire de la génération (0.0 à 2.0). Ignoré pour les modèles de raisonnement (série o1/o3/o4/gpt-5)
- ``rag.llm.openai.{promptType}.max.tokens`` - Nombre maximum de tokens
- ``rag.llm.openai.{promptType}.context.max.chars`` - Nombre maximum de caractères du contexte (défaut : ``16000`` pour answer/summary, ``10000`` pour les autres)

Types de prompt
----------------

Types de prompt disponibles :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type de prompt
     - Description
   * - ``intent``
     - Prompt pour déterminer l'intention de l'utilisateur
   * - ``evaluation``
     - Prompt pour évaluer la pertinence des résultats de recherche
   * - ``unclear``
     - Prompt de réponse pour les requêtes peu claires
   * - ``noresults``
     - Prompt de réponse lorsqu'il n'y a pas de résultats de recherche
   * - ``docnotfound``
     - Prompt de réponse lorsque le document n'est pas trouvé
   * - ``answer``
     - Prompt pour générer une réponse
   * - ``summary``
     - Prompt pour générer un résumé
   * - ``faq``
     - Prompt pour générer une FAQ
   * - ``direct``
     - Prompt pour répondre directement
   * - ``queryregeneration``
     - Prompt de régénération de requêtes

Valeurs par défaut
------------------

Valeurs par défaut pour chaque type de prompt. La configuration de température est ignorée pour les modèles de raisonnement (série o1/o3/o4/gpt-5).

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Type de prompt
     - Température
     - Max Tokens
     - Remarques
   * - ``intent``
     - 0.1
     - 256
     - Détection d'intention déterministe
   * - ``evaluation``
     - 0.1
     - 256
     - Évaluation de pertinence déterministe
   * - ``unclear``
     - 0.7
     - 512
     -
   * - ``noresults``
     - 0.7
     - 512
     -
   * - ``docnotfound``
     - 0.7
     - 256
     -
   * - ``direct``
     - 0.7
     - 1024
     -
   * - ``faq``
     - 0.7
     - 1024
     -
   * - ``answer``
     - 0.5
     - 2048
     - Génération de réponse principale
   * - ``summary``
     - 0.3
     - 2048
     - Génération de résumé
   * - ``queryregeneration``
     - 0.3
     - 256
     - Régénération de requêtes

Exemple de configuration
------

::

    # Configuration de la temperature pour le prompt answer
    rag.llm.openai.answer.temperature=0.7

    # Nombre maximum de tokens pour le prompt answer
    rag.llm.openai.answer.max.tokens=2048

    # Configuration de la temperature pour le prompt summary (configurer bas pour le resume)
    rag.llm.openai.summary.temperature=0.3

    # Configuration de la temperature pour le prompt intent (configurer bas pour la determination d'intention)
    rag.llm.openai.intent.temperature=0.1

Comportement de réessai
=======================

Les requêtes vers l'API OpenAI sont automatiquement réessayées pour les codes de statut HTTP suivants :

- ``429`` Too Many Requests (limitation de débit)
- ``500`` Internal Server Error
- ``502`` Bad Gateway (qu'OpenAI peut renvoyer en cas de surcharge en amont)
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Lors d'un réessai, |Fess| attend selon un backoff exponentiel (valeur de base ``rag.llm.openai.retry.base.delay.ms`` millisecondes, jusqu'à ``rag.llm.openai.retry.max`` tentatives, avec une gigue de +/-20%).
Si le serveur renvoie un en-tête ``Retry-After`` (en secondes entières, plafonné à ``600`` secondes), cette valeur prend le pas sur le backoff exponentiel. Cela suit les recommandations officielles d'OpenAI.

À noter, les ``IOException`` (timeouts de connexion, réinitialisations de socket, échecs DNS) ne sont pas réessayées. Si la requête a pu atteindre le serveur, un réessai pourrait entraîner une double facturation.
Pour les requêtes en streaming, seule la connexion initiale est sujette aux réessais ; les erreurs survenant après le début de la réception du corps de la réponse sont propagées immédiatement.

.. note::
   Avec les valeurs par défaut (10 tentatives maximum, base de 2 secondes), le pire cas pour la somme des 9 backoffs est ``2 + 4 + 8 + ... + 512 ~= 1022 secondes (environ 17 minutes)``. Lorsque ``Retry-After`` (jusqu'à 600 secondes) est renvoyé à chaque tentative, le pire cas atteint ``9 x 600 secondes = 90 minutes``. Pour un contrôle plus strict de la latence, réduisez ``rag.llm.openai.retry.max``.

Streaming et informations d'utilisation
=======================================

Par défaut, ``stream_options.include_usage=true`` est ajouté aux requêtes, ce qui permet de recevoir l'objet ``usage`` (incluant ``completion_tokens_details.reasoning_tokens`` pour les modèles de raisonnement et ``prompt_tokens_details.cached_tokens`` lorsque la mise en cache du prompt est utilisée) dans le dernier chunk SSE de la réponse en streaming.

Pour les backends qui n'acceptent pas le champ ``stream_options.include_usage`` (par exemple vLLM ou certaines passerelles compatibles Azure OpenAI), désactivez cette option ainsi::

    rag.llm.openai.stream.include.usage=false

Logs et détection d'anomalies
=============================

Le client OpenAI émet les logs structurés suivants. Cela permet de surveiller l'utilisation des tokens et les anomalies de réponse sans activer le niveau ``DEBUG``.

- ``[LLM:OPENAI] Stream completed.`` (INFO) - émis à la fin d'une réponse en streaming, avec le nombre de chunks, le délai jusqu'au premier chunk et les informations d'utilisation des tokens
- ``[LLM:OPENAI] Chat response received.`` (INFO) - émis à la fin d'une réponse non-streaming, avec des informations équivalentes
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` (WARN) - émis lorsque ``finish_reason`` est autre que ``stop`` (``length`` : troncature par max_tokens ; ``content_filter`` : modération ; ``tool_calls`` / ``function_call`` : configuration d'appel d'outil non intentionnelle, etc.)
- ``[LLM:OPENAI] Stream refusal.`` (WARN) - émis lorsque ``delta.refusal`` est renvoyé par une sortie structurée

Ces logs WARN peuvent être exploités pour ajuster ``max_tokens``, auditer le filtre de contenu et détecter une mauvaise configuration de ``extra_params``.

Masquage des informations d'authentification dans les URL des logs
------------------------------------------------------------------

Les URL émises dans les logs voient automatiquement leurs paramètres de requête contenant des informations d'authentification (``api_key``, ``apikey``, ``api-key``, ``key``, ``token``, ``access_token``, ``access-token``, sans distinction de casse) masqués par ``***``.

Le point de terminaison officiel OpenAI (``https://api.openai.com``) s'authentifie via l'en-tête ``Authorization: Bearer`` et n'inclut donc pas d'informations d'authentification dans l'URL. Toutefois, si vous configurez ``rag.llm.openai.api.url`` vers un proxy personnalisé qui accepte les informations d'authentification en tant que paramètres de requête (certains déploiements Azure, passerelles vLLM, etc.), cela empêche également la fuite de la clé API dans les logs.

Prise en charge des modèles de raisonnement
==============

Lors de l'utilisation de modèles de raisonnement de la série o1/o3/o4 ou de la série gpt-5, |Fess| utilise automatiquement le paramètre ``max_completion_tokens`` de l'API OpenAI à la place de ``max_tokens``. Aucune modification de configuration supplémentaire n'est nécessaire.

.. note::
   Les modèles de raisonnement (série o1/o3/o4/gpt-5) ignorent le paramètre ``temperature`` et utilisent une valeur fixe (1). De plus, lors de l'utilisation de modèles de raisonnement, le ``max_tokens`` par défaut est multiplié par ``reasoning.token.multiplier`` (défaut : 4).

Paramètres supplémentaires pour les modèles de raisonnement
----------------------------

Lors de l'utilisation de modèles de raisonnement, les paramètres supplémentaires suivants peuvent être configurés dans ``fess_config.properties`` :

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - Paramètre d'effort de raisonnement pour les modèles de série o (``low``, ``medium``, ``high``)
     - ``low`` (intent/evaluation/docnotfound/unclear/noresults/queryregeneration), non défini (autres)
   * - ``rag.llm.openai.{promptType}.top.p``
     - Seuil de probabilité pour la sélection de tokens (0.0 à 1.0)
     - (Non défini)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - Pénalité de fréquence (-2.0 à 2.0)
     - (Non défini)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - Pénalité de présence (-2.0 à 2.0)
     - (Non défini)

``{promptType}`` peut être ``intent``, ``evaluation``, ``answer``, ``summary``, etc.

Exemple de configuration
------

::

    # Configurer l'effort de raisonnement sur high pour la generation de reponse avec o3-mini
    rag.llm.openai.model=o3-mini
    rag.llm.openai.answer.reasoning.effort=high

    # Configurer top_p et les penalites pour la generation de reponse avec gpt-5
    rag.llm.openai.model=gpt-5
    rag.llm.openai.answer.top.p=0.9
    rag.llm.openai.answer.frequency.penalty=0.5

Configuration via options JVM
=============================

Pour des raisons de sécurité, il est recommandé de configurer la clé API via
l'environnement d'exécution (options JVM) plutôt que via des fichiers versionnés.

Environnement Docker
--------------------

Le dépôt officiel `docker-fess <https://github.com/codelibs/docker-fess>`__
fournit un overlay OpenAI (``compose-openai.yaml``). Étapes minimales :

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

Contenu de ``compose-openai.yaml`` (référence pour un setup équivalent) :

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.7.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Notes :

- ``FESS_PLUGINS=fess-llm-openai:15.7.0`` fait que ``run.sh`` du conteneur télécharge et installe automatiquement le plugin dans ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` active le mode IA
- ``-Dfess.config.rag.llm.openai.api.key=...`` définit la clé API, ``-Dfess.config.rag.llm.openai.model=...`` choisit le modèle
- ``-Dfess.system.rag.llm.name=openai`` n'agit que comme valeur par défaut initiale avant qu'une valeur ne soit persistée dans OpenSearch. Après démarrage, le paramètre peut aussi être modifié sous Administration > Système > Général (section RAG)

Si l'accès Internet passe par un proxy, spécifiez la configuration ``http.proxy.*`` de |Fess| via ``FESS_JAVA_OPTS`` (voir la section "Utilisation via un proxy HTTP" ci-dessous).

Environnement systemd
---------------------

Ajouter à ``FESS_JAVA_OPTS`` dans ``/etc/sysconfig/fess`` (ou ``/etc/default/fess``) :

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

Utilisation via un proxy HTTP
=============================

Le client OpenAI partage la configuration de proxy HTTP commune à |Fess|. Spécifiez les propriétés suivantes dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``http.proxy.host``
     - Nom d'hôte du proxy (chaîne vide pour ne pas utiliser de proxy)
     - ``""``
   * - ``http.proxy.port``
     - Numéro de port du proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nom d'utilisateur pour l'authentification du proxy (facultatif ; lorsqu'il est renseigné, l'authentification Basic est activée)
     - ``""``
   * - ``http.proxy.password``
     - Mot de passe pour l'authentification du proxy
     - ``""``

Dans un environnement Docker, spécifiez ce qui suit dans ``FESS_JAVA_OPTS``::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   Cette configuration s'applique également à tous les accès HTTP de |Fess|, notamment ceux du crawler.
   Les propriétés système Java traditionnelles (``-Dhttps.proxyHost``, etc.) ne sont pas prises en compte par le client OpenAI.

Utilisation d'Azure OpenAI
==================

Pour utiliser les modèles OpenAI via Microsoft Azure, modifiez le point de terminaison API.

::

    # Point de terminaison Azure OpenAI
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Cle API Azure
    rag.llm.openai.api.key=your-azure-api-key

    # Nom du deploiement (specifie comme nom de modele)
    rag.llm.openai.model=your-deployment-name

.. note::
   Lors de l'utilisation d'Azure OpenAI, le format des requêtes API peut différer légèrement.
   Consultez la documentation Azure OpenAI pour plus de détails.

Guide de sélection des modèles
==================

Guide pour la sélection du modèle selon l'usage.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modèle
     - Coût
     - Qualité
     - Usage
   * - ``gpt-5-mini``
     - Moyen
     - Élevée
     - Usage équilibré (recommandé)
   * - ``gpt-4o-mini``
     - Bas-Moyen
     - Élevée
     - Usage prioritaire au coût
   * - ``gpt-5``
     - Élevé
     - Maximale
     - Raisonnement complexe, haute qualité requise
   * - ``gpt-4o``
     - Moyen-Élevé
     - Maximale
     - Lorsque la prise en charge multimodale est requise
   * - ``o3-mini`` / ``o4-mini``
     - Moyen
     - Maximale
     - Tâches de raisonnement comme les mathématiques et la programmation

Estimation des coûts
------------

L'API OpenAI est facturée à l'usage.

.. note::
   Pour les derniers prix, consultez `OpenAI Pricing <https://openai.com/pricing>`__.

Contrôle des requêtes simultanées
==================

Dans |Fess|, le nombre de requêtes simultanées vers l'API OpenAI peut être contrôlé via ``rag.llm.openai.max.concurrent.requests`` dans ``fess_config.properties``. La valeur par défaut est ``5``.

::

    # Configurer le nombre maximum de requetes simultanees
    rag.llm.openai.max.concurrent.requests=5

Cette configuration permet d'éviter les requêtes excessives vers l'API OpenAI et de prévenir les erreurs de limitation de débit.

Limites par niveau OpenAI
------------------

Les limites varient selon le niveau de votre compte OpenAI :

- **Free** : 3 RPM (requêtes/minute)
- **Tier 1** : 500 RPM
- **Tier 2** : 5,000 RPM
- **Tier 3+** : Limites plus élevées

Ajustez ``rag.llm.openai.max.concurrent.requests`` de manière appropriée selon le niveau de votre compte OpenAI.

Dépannage
======================

Erreur d'authentification
----------

**Symptôme** : Erreur "401 Unauthorized"

**Points à vérifier** :

1. Vérifier si la clé API est correctement configurée
2. Vérifier si la clé API est valide (vérifier dans le tableau de bord OpenAI)
3. Vérifier si la clé API a les permissions nécessaires

Erreur de limitation de débit
----------------

**Symptôme** : Erreur "429 Too Many Requests"

**Solution** :

1. Réduire la valeur de ``rag.llm.openai.max.concurrent.requests``::

    rag.llm.openai.max.concurrent.requests=3

2. Mettre à niveau le niveau de votre compte OpenAI

Dépassement de quota
------------

**Symptôme** : Erreur "You exceeded your current quota"

**Solution** :

1. Vérifier l'usage dans le tableau de bord OpenAI
2. Vérifier les paramètres de facturation et augmenter la limite si nécessaire

Timeout
------------

**Symptôme** : La requête expire

**Solution** :

1. Augmenter le temps de timeout ::

    rag.llm.openai.timeout=180000

2. Envisager un modèle plus rapide (gpt-5-mini, etc.)

Configuration de débogage
------------

Pour investiguer les problèmes, ajustez le niveau de log de |Fess| pour afficher des logs détaillés liés à OpenAI.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

Notes de sécurité
========================

Lors de l'utilisation de l'API OpenAI, faites attention aux points de sécurité suivants.

1. **Confidentialité des données** : Le contenu des résultats de recherche est envoyé aux serveurs OpenAI
2. **Gestion des clés API** : La fuite de clés peut entraîner une utilisation non autorisée
3. **Conformité** : Si les données contiennent des informations confidentielles, vérifiez les politiques de votre organisation
4. **Politique d'utilisation** : Respectez les conditions d'utilisation d'OpenAI

Informations de référence
========

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - Aperçu de l'intégration LLM
- :doc:`rag-chat` - Détails de la fonctionnalité de mode de recherche IA
