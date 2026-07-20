==========================
Configuration Ollama
==========================

Aperçu
======

Ollama est une plateforme open source permettant d'exécuter des grands modèles de langage (LLM) en local.
La fonctionnalité d'intégration Ollama de |Fess| est fournie sous forme de plugin ``fess-llm-ollama``, et convient à une utilisation en environnement privé.

L'utilisation d'Ollama permet d'utiliser la fonctionnalité du mode de recherche IA sans envoyer de données à l'extérieur.

Caractéristiques principales
-----------------------------

- **Exécution locale** : Les données ne sont pas envoyées à l'extérieur, garantissant la confidentialité
- **Modèles variés** : Prise en charge de nombreux modèles dont Llama, Mistral, Gemma, CodeLlama
- **Efficacité des coûts** : Pas de coût API (seulement les coûts matériels)
- **Personnalisation** : Possibilité d'utiliser des modèles affinés indépendamment

Modèles pris en charge
-----------------------

Principaux modèles disponibles avec Ollama :

- ``llama3.3:70b`` - Llama 3.3 de Meta (70B paramètres)
- ``gemma4:e4b`` - Gemma 4 de Google (E4B paramètres, par défaut)
- ``mistral:7b`` - Mistral de Mistral AI (7B paramètres)
- ``codellama:13b`` - Code Llama de Meta (13B paramètres)
- ``phi3:3.8b`` - Phi-3 de Microsoft (3.8B paramètres)

.. note::
   Pour la dernière liste des modèles disponibles, consultez `Ollama Library <https://ollama.com/library>`__.

Prérequis
=========

Avant d'utiliser Ollama, vérifiez les points suivants.

1. **Installation d'Ollama** : Téléchargez et installez depuis `https://ollama.com/ <https://ollama.com/>`__
2. **Téléchargement du modèle** : Téléchargez le modèle à utiliser dans Ollama
3. **Démarrage du serveur Ollama** : Vérifiez qu'Ollama fonctionne

Installation d'Ollama
---------------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

Téléchargez et exécutez l'installateur depuis le site officiel.

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Téléchargement du modèle
------------------------

::

    # Télécharger le modèle par défaut (Gemma 4 E4B)
    ollama pull gemma4:e4b

    # Télécharger Llama 3.3
    ollama pull llama3.3:70b

    # Vérifier le fonctionnement du modèle
    ollama run gemma4:e4b "Hello, how are you?"

Installation du plugin
======================

La fonctionnalité d'intégration Ollama est fournie sous forme de plugin.
Pour utiliser Ollama, l'installation du plugin ``fess-llm-ollama`` est nécessaire.

1. Téléchargez `fess-llm-ollama-15.8.0.jar`.
2. Placez-le dans le répertoire ``app/WEB-INF/plugin/`` du répertoire d'installation de |Fess|.

::

    cp fess-llm-ollama-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Redémarrez |Fess|.

.. note::
   La version du plugin doit correspondre à la version de |Fess|.

Configuration de base
======================

Les configurations LLM sont réparties dans plusieurs fichiers de configuration.

Configuration minimale
------------------------

``system.properties``\ (configurable également via Administration > Système > Général) :

::

    # Définir le fournisseur LLM sur Ollama
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalité de mode de recherche IA
    rag.chat.enabled=true

    # URL d'Ollama (environnement local)
    rag.llm.ollama.api.url=http://localhost:11434

    # Modèle à utiliser
    rag.llm.ollama.model=gemma4:e4b

.. note::
   La configuration du fournisseur LLM peut également être effectuée via l'administration (Administration > Système > Général) en configurant ``rag.llm.name``.

Configuration recommandée (environnement de production)
-----------------------------------------------------------

``system.properties``\ (configurable également via Administration > Système > Général) :

::

    # Configuration du fournisseur LLM
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalité de mode de recherche IA
    rag.chat.enabled=true

    # URL d'Ollama
    rag.llm.ollama.api.url=http://localhost:11434

    # Configuration du modèle (utiliser un grand modèle)
    rag.llm.ollama.model=llama3.3:70b

    # Configuration du timeout (augmenté pour les grands modèles)
    rag.llm.ollama.timeout=120000

    # Contrôle du nombre de requêtes simultanées
    rag.llm.ollama.max.concurrent.requests=5

Éléments de configuration
==========================

Tous les éléments de configuration disponibles pour le client Ollama. Tous, sauf ``rag.llm.name``, se configurent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``rag.llm.ollama.api.url``
     - URL de base du serveur Ollama
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - Nom du modèle à utiliser (modèle déjà téléchargé dans Ollama)
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - Délai d'expiration des requêtes (millisecondes)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - Intervalle de vérification de disponibilité (secondes). Une valeur inférieure ou égale à ``0`` désactive la vérification périodique de disponibilité
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Nombre maximal de requêtes simultanées
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Nombre maximal de documents pertinents pour l'évaluation
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - Délai d'attente pour l'acquisition d'un permis de contrôle de concurrence (millisecondes)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - Délai d'expiration de la connexion TCP (millisecondes). Peut être spécifié séparément de ``rag.llm.ollama.timeout``
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - Nombre maximal de tentatives HTTP (en cas d'erreur ``429`` ou de la série ``5xx``)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - Délai de base du backoff exponentiel (millisecondes)
     - ``2000``

Configuration avancée
------------------------

Éléments de configuration avancés relatifs à l'historique et à la taille du contexte.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - Propriété
     - Description
     - Par défaut
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - Nombre maximal de caractères de la description lors de l'évaluation
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - Nombre maximal de caractères de l'historique de conversation
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - Nombre maximal de messages de l'historique lors de la détermination de l'intention
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - Nombre maximal de caractères de l'historique lors de la détermination de l'intention
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - Nombre maximal de caractères de l'historique des réponses de l'assistant
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - Nombre maximal de caractères de l'historique des résumés de l'assistant
     - ``500``

Contrôle de la concurrence
----------------------------

``rag.llm.ollama.max.concurrent.requests`` permet de contrôler le nombre de requêtes simultanées vers Ollama.
La valeur par défaut est 5. Ajustez-la en fonction des ressources du serveur Ollama.
Un nombre trop élevé de requêtes simultanées peut surcharger le serveur Ollama et réduire la vitesse de réponse.

Configuration par type de prompt
====================================

|Fess| permet de personnaliser les paramètres du LLM pour chaque type de prompt.
La configuration s'effectue dans ``fess_config.properties``.

Les paramètres suivants peuvent être définis par type de prompt :

- ``rag.llm.ollama.{promptType}.temperature`` - Température lors de la génération
- ``rag.llm.ollama.{promptType}.max.tokens`` - Nombre maximal de tokens (mappé sur ``num_predict`` de l'API Ollama)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Nombre maximal de caractères du contexte
- ``rag.llm.ollama.{promptType}.thinking.budget`` - Budget de réflexion (contrôle de la réflexion sous forme booléenne ; voir « Prise en charge des modèles de réflexion »)
- ``rag.llm.ollama.{promptType}.thinking.level`` - Niveau de réflexion (chaîne de caractères ``high`` / ``medium`` / ``low`` ; voir « Prise en charge des modèles de réflexion »)
- ``rag.llm.ollama.{promptType}.top.p`` - Valeur d'échantillonnage Top-P
- ``rag.llm.ollama.{promptType}.top.k`` - Valeur d'échantillonnage Top-K
- ``rag.llm.ollama.{promptType}.num.ctx`` - Taille de la fenêtre de contexte

Chaque paramètre est résolu dans l'ordre suivant : ``rag.llm.ollama.{promptType}.<param>`` (configuration spécifique au type de prompt) → ``rag.llm.ollama.default.<param>`` (repli commun à tous les types de prompt) → valeur par défaut codée en dur pour chaque type de prompt. Une valeur explicitement spécifiée dans la requête est toujours prioritaire.

Types de prompt disponibles :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type de prompt
     - Description
   * - ``intent``
     - Prompt pour déterminer l'intention de l'utilisateur
   * - ``evaluation``
     - Prompt d'évaluation des résultats de recherche
   * - ``unclear``
     - Prompt de réponse pour les requêtes peu claires
   * - ``noresults``
     - Prompt pour le cas où il n'y a aucun résultat de recherche
   * - ``docnotfound``
     - Prompt pour le cas où le document est introuvable
   * - ``answer``
     - Prompt de génération de réponse
   * - ``summary``
     - Prompt de génération de résumé
   * - ``faq``
     - Prompt de génération de FAQ
   * - ``direct``
     - Prompt de réponse directe
   * - ``queryregeneration``
     - Prompt de régénération de requête

Chaque type de prompt dispose de valeurs par défaut codées en dur, appliquées lorsque la configuration est omise.

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Type de prompt
     - temperature
     - max.tokens
     - thinking.budget
     - context.max.chars
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
     - ``6000``
   * - ``evaluation``
     - ``0.1``
     - ``512``
     - ``0``
     - ``6000``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - (non défini)
     - ``10000``
   * - ``summary``
     - ``0.3``
     - ``8192``
     - (non défini)
     - ``10000``
   * - ``faq``
     - ``0.7``
     - ``4096``
     - (non défini)
     - ``6000``
   * - ``direct``
     - ``0.7``
     - ``4096``
     - (non défini)
     - ``6000``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``
     - ``6000``

Exemple de configuration::

    # Définir la température lors de la génération de réponse
    rag.llm.ollama.answer.temperature=0.7

    # Définir le nombre maximal de tokens lors de la génération de résumé
    rag.llm.ollama.summary.max.tokens=2048

    # Définir le nombre maximal de caractères du contexte lors de la détermination de l'intention
    rag.llm.ollama.intent.context.max.chars=4000

Options du modèle Ollama
============================

Les paramètres du modèle Ollama peuvent être configurés dans ``fess_config.properties``.
En utilisant le format ``rag.llm.ollama.default.<param>``, la valeur est utilisée comme repli commun à tous les types de prompt.
Le repli via ``default`` s'applique non seulement à ``top.p`` / ``top.k`` / ``num.ctx``, mais aussi à ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Par défaut
   * - ``rag.llm.ollama.default.top.p``
     - Valeur d'échantillonnage Top-P (0.0 à 1.0). Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.top.p``
     - (non défini)
   * - ``rag.llm.ollama.default.top.k``
     - Valeur d'échantillonnage Top-K. Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.top.k``
     - (non défini)
   * - ``rag.llm.ollama.default.num.ctx``
     - Taille de la fenêtre de contexte. Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.num.ctx``
     - (non défini)
   * - ``rag.llm.ollama.default.temperature``
     - Valeur de repli de la température de génération. Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.temperature``
     - (non défini)
   * - ``rag.llm.ollama.default.max.tokens``
     - Valeur de repli du nombre maximal de tokens. Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.max.tokens``
     - (non défini)
   * - ``rag.llm.ollama.default.thinking.budget``
     - Valeur de repli du budget de réflexion. Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.thinking.budget``
     - (non défini)
   * - ``rag.llm.ollama.default.thinking.level``
     - Valeur de repli du niveau de réflexion (``high`` / ``medium`` / ``low``). Peut être remplacée par type de prompt avec ``rag.llm.ollama.{promptType}.thinking.level``
     - (non défini)
   * - ``rag.llm.ollama.options.*``
     - Options globales transmises directement à l'API Ollama. Le suffixe est utilisé comme nom d'option (exemple : ``rag.llm.ollama.options.repeat_penalty=1.1``). Les valeurs sont automatiquement converties en Integer, Double, Boolean ou String
     - (non défini)

Exemple de configuration::

    # Échantillonnage Top-P par défaut (commun à tous les types de prompt)
    rag.llm.ollama.default.top.p=0.9

    # Échantillonnage Top-K par défaut
    rag.llm.ollama.default.top.k=40

    # Taille de la fenêtre de contexte par défaut
    rag.llm.ollama.default.num.ctx=4096

    # Modifier Top-P uniquement pour la génération de réponse
    rag.llm.ollama.answer.top.p=0.95

    # Option globale (transmise directement à l'API Ollama)
    rag.llm.ollama.options.repeat_penalty=1.1

Prise en charge des modèles de réflexion
============================================

Lors de l'utilisation de modèles de réflexion (thinking model) tels que gemma4 ou qwen3, |Fess| prend en charge la configuration du budget de réflexion (thinking budget).

Le budget de réflexion se configure par type de prompt dans ``fess_config.properties`` :

::

    # Configuration du budget de réflexion lors de la génération de réponse
    rag.llm.ollama.answer.thinking.budget=1024

    # Configuration du budget de réflexion lors de la génération de résumé
    rag.llm.ollama.summary.thinking.budget=1024

La configuration du budget de réflexion permet de contrôler le nombre de tokens alloués à l'étape de « réflexion » du modèle avant la génération de la réponse.

.. note::
   Avec Ollama, le budget de réflexion est converti en indicateur booléen (``think: true`` si la valeur est supérieure à 0, ``think: false`` si elle vaut 0). Le contrôle fin par nombre de tokens n'est pas disponible en raison des contraintes de l'API Ollama.

Niveau de réflexion (thinking level)
----------------------------------------

Certains modèles, comme gpt-oss, ignorent l'indicateur booléen ``think`` et nécessitent la spécification du niveau de réflexion sous forme de chaîne de caractères ``high`` / ``medium`` / ``low``.
Pour ces modèles, utilisez ``rag.llm.ollama.{promptType}.thinking.level``.

::

    # Configuration du niveau de réflexion lors de la génération de réponse
    rag.llm.ollama.answer.thinking.level=high

    # Configuration du niveau de réflexion lors de la génération de résumé
    rag.llm.ollama.summary.thinking.level=medium

Les valeurs acceptées pour ``thinking.level`` sont ``high`` / ``medium`` / ``low`` (la casse n'est pas prise en compte). Une valeur non valide est ignorée et un avertissement est écrit dans les journaux.

.. note::
   Si ``thinking.level`` (forme chaîne de caractères) et ``thinking.budget`` (forme booléenne) sont tous deux définis, ``thinking.level`` est prioritaire. Utilisez ``thinking.level`` pour les modèles de la famille GPT-OSS, et ``thinking.budget`` pour les autres modèles de réflexion.

Configuration réseau
========================

Configuration Docker
------------------------

Le dépôt officiel `docker-fess <https://github.com/codelibs/docker-fess>`__ de |Fess| inclut un overlay Ollama ``compose-ollama.yaml``. Voici les étapes minimales.

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` est configuré pour utiliser un GPU NVIDIA (NVIDIA Container Toolkit requis). Son contenu est le suivant.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        container_name: ollama01
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama
        networks:
          - search_net
        restart: unless-stopped
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

    volumes:
      ollama-data:
        driver: local

Points importants :

- ``FESS_PLUGINS=fess-llm-ollama:15.8.0`` permet au script de démarrage de récupérer automatiquement le JAR du plugin et de le placer dans ``app/WEB-INF/plugin/`` (adaptez la version à votre installation de |Fess|)
- ``-Dfess.config.rag.chat.enabled=true`` active le mode de recherche IA
- ``-Dfess.config.rag.llm.ollama.api.url=...`` spécifie l'URL du serveur Ollama (dans le réseau Docker Compose, elle est résolue via le nom de service, par exemple ``ollama01``)
- Le fournisseur LLM (``rag.llm.name``) ayant ``ollama`` comme valeur par défaut, aucune spécification explicite n'est nécessaire si Ollama est le seul fournisseur utilisé. Pour basculer depuis un autre fournisseur, ajoutez ``-Dfess.system.rag.llm.name=ollama`` dans ``FESS_JAVA_OPTS``, ou configurez-le après le démarrage dans la section RAG de la page « Système > Général » de la console d'administration
- Le bloc ``deploy.resources.reservations.devices`` sert à l'utilisation du GPU. Si vous n'utilisez pas de GPU (exécution en CPU uniquement), supprimez ce bloc

.. note::
   Les variables d'environnement en majuscules avec underscores, telles que ``RAG_CHAT_ENABLED`` ou ``RAG_LLM_NAME``, ne sont pas reconnues directement par |Fess|. Les valeurs de configuration doivent impérativement être transmises dans ``FESS_JAVA_OPTS`` sous la forme ``-Dfess.config.<key>`` (famille ``fess_config.properties``) ou ``-Dfess.system.<key>`` (famille ``system.properties``).

Serveur Ollama distant
------------------------

Si Ollama s'exécute sur un serveur distinct de celui de Fess :

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama ne dispose pas de fonctionnalité d'authentification par défaut. Si vous le rendez accessible depuis
   l'extérieur, envisagez des mesures de sécurité au niveau réseau (pare-feu, VPN, etc.).

Utilisation via un proxy HTTP
====================================

Le client Ollama partage la configuration de proxy HTTP globale de |Fess|. Si la connexion au serveur Ollama doit passer par un proxy (par exemple lors de l'utilisation d'un serveur Ollama distant), spécifiez les propriétés suivantes dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Par défaut
   * - ``http.proxy.host``
     - Nom d'hôte du proxy (chaîne vide pour ne pas utiliser de proxy)
     - ``""``
   * - ``http.proxy.port``
     - Numéro de port du proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nom d'utilisateur pour l'authentification du proxy (facultatif ; s'il est renseigné, l'authentification Basic est activée)
     - ``""``
   * - ``http.proxy.password``
     - Mot de passe pour l'authentification du proxy
     - ``""``

.. note::
   Ollama s'exécutant généralement en local ou sur un réseau interne, la configuration d'un proxy n'est nécessaire que dans des cas limités (par exemple, l'utilisation d'un serveur Ollama distant accessible uniquement via un proxy d'entreprise).
   Ce paramétrage s'applique aussi à l'ensemble des accès HTTP de |Fess|, y compris ceux du robot d'exploration.

Guide de sélection des modèles
====================================

Guide de sélection du modèle selon l'usage.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modèle
     - Taille
     - VRAM requise
     - Usage
   * - ``phi3:3.8b``
     - Petite
     - 4 Go ou plus
     - Environnement léger, questions-réponses simples
   * - ``gemma4:e4b``
     - Petite à moyenne
     - 8 Go ou plus
     - Usage général équilibré, prise en charge du mode réflexion (par défaut)
   * - ``mistral:7b``
     - Moyenne
     - 8 Go ou plus
     - Lorsqu'une réponse de haute qualité est nécessaire
   * - ``llama3.3:70b``
     - Grande
     - 48 Go ou plus
     - Réponses de la meilleure qualité, raisonnement complexe

Prise en charge GPU
------------------------

Ollama prend en charge l'accélération GPU. L'utilisation d'un GPU NVIDIA
améliore considérablement la vitesse d'inférence.

::

    # Vérification de la prise en charge GPU
    ollama run gemma4:e4b --verbose

Dépannage
============

Erreur de connexion
------------------------

**Symptôme** : Une erreur survient dans la fonctionnalité de chat, le LLM est indiqué comme indisponible

**Points à vérifier** :

1. Vérifier qu'Ollama fonctionne::

    curl http://localhost:11434/api/tags

2. Vérifier que le modèle est téléchargé::

    ollama list

3. Vérifier la configuration du pare-feu

4. Vérifier que le plugin ``fess-llm-ollama`` est bien placé dans ``app/WEB-INF/plugin/``

Modèle introuvable
------------------------

**Symptôme** : Le journal affiche « Configured model not found »

**Solution** :

1. Vérifier que le nom du modèle est exact (le tag ``:latest`` peut être requis)::

    # Vérifier la liste des modèles
    ollama list

2. Télécharger le modèle nécessaire::

    ollama pull gemma4:e4b

Délai d'expiration
------------------------

**Symptôme** : La requête expire (timeout)

**Solution** :

1. Augmenter le délai d'expiration::

    rag.llm.ollama.timeout=120000

2. Utiliser un modèle plus petit ou envisager un environnement GPU

Configuration du débogage
------------------------------

Pour investiguer un problème, ajustez le niveau de log de |Fess| afin d'afficher des journaux détaillés liés à Ollama.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Informations de référence
==============================

- `Site officiel Ollama <https://ollama.com/>`__
- `Bibliothèque de modèles Ollama <https://ollama.com/library>`__
- `Ollama sur GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Aperçu de l'intégration LLM
- :doc:`rag-chat` - Détails de la fonctionnalité de mode de recherche IA
