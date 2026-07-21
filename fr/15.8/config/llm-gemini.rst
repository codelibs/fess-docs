==================================================
Configuration Google Gemini (Recherche IA / RAG)
==================================================

Aperçu
======

Cette page explique comment configurer le plugin ``fess-llm-gemini`` afin que |Fess| puisse utiliser Google Gemini pour son **mode de recherche IA (RAG : Retrieval-Augmented Generation)** — qui répond à des questions en langage naturel à partir de votre index de recherche d'entreprise, avec citation des sources. |Fess| appelle l'API Google AI (Generative Language API) pour exécuter le RAG sur vos documents explorés avec les modèles Gemini.

Google Gemini est un grand modèle de langage (LLM) de pointe fourni par Google.
|Fess| peut utiliser l'API Google AI (Generative Language API) pour réaliser la fonctionnalité de mode de recherche IA avec les modèles Gemini.

L'utilisation de Gemini permet de générer des réponses de haute qualité en tirant parti de la dernière technologie IA de Google.

Caractéristiques principales
-----------------------------

- **Prise en charge multimodale** : Peut traiter les images en plus du texte
- **Long contexte** : Fenêtre de contexte longue permettant de traiter de grandes quantités de documents à la fois
- **Efficacité des coûts** : Le modèle Flash est rapide et peu coûteux
- **Intégration Google** : Intégration facile avec les services Google Cloud

Modèles pris en charge
-----------------------

Principaux modèles disponibles avec Gemini :

- ``gemini-3.1-flash-lite-preview`` - Modèle rapide léger et à faible coût (par défaut)
- ``gemini-3-flash-preview`` - Modèle Flash standard
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - Modèles de raisonnement avancé
- ``gemini-2.5-flash`` - Version stable du modèle rapide
- ``gemini-2.5-pro`` - Version stable du modèle de raisonnement

.. note::
   Pour les derniers modèles disponibles, consultez `Google AI for Developers <https://ai.google.dev/models/gemini>`__.

Prérequis
=========

Avant d'utiliser Gemini, préparez les éléments suivants.

1. **Compte Google** : Un compte Google est requis
2. **Accès Google AI Studio** : Accédez à `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **Clé API** : Générez une clé API dans Google AI Studio

Obtention de la clé API
------------------------

1. Accédez à `Google AI Studio <https://aistudio.google.com/>`__
2. Cliquez sur "Get API key"
3. Sélectionnez "Create API key"
4. Sélectionnez ou créez un projet
5. Enregistrez la clé API générée en lieu sûr

.. warning::
   La clé API est une information confidentielle. Faites attention aux points suivants :

   - Ne pas la commiter dans un système de gestion de versions
   - Ne pas l'afficher dans les logs
   - La gérer via des variables d'environnement ou des fichiers de configuration sécurisés

Installation du plugin
======================

La fonctionnalité d'intégration Gemini est fournie sous forme de plugin ``fess-llm-gemini``.
Pour utiliser Gemini, l'installation du plugin est nécessaire.

1. Téléchargez `fess-llm-gemini-15.8.0.jar`
2. Placez-le dans le répertoire ``app/WEB-INF/plugin/`` de |Fess|
3. Redémarrez |Fess|

::

    # Exemple de placement du plugin
    cp fess-llm-gemini-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   La version du plugin doit correspondre à la version de |Fess|.

Configuration de base
=====================

La sélection du fournisseur LLM ( ``rag.llm.name`` ) s'effectue via l'administration ou dans ``system.properties``, et l'activation de la fonctionnalité de mode de recherche IA ainsi que les paramètres spécifiques à Gemini s'effectuent dans ``fess_config.properties``.

Configuration de fess_config.properties
-----------------------------------------

Ajoutez la configuration d'activation de la fonctionnalité de mode de recherche IA dans ``app/WEB-INF/conf/fess_config.properties``.

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

Configuration du fournisseur LLM
----------------------------------

Le nom du fournisseur LLM ( ``rag.llm.name`` ) se configure via l'administration (Administration > Système > General) ou dans ``system.properties``. Les paramètres spécifiques à Gemini se décrivent dans ``fess_config.properties``.

Configuration minimale
~~~~~~~~~~~~~~~~~~~~~~~

``system.properties`` (configurable également via Administration > Système > General) :

::

    # Definir le fournisseur LLM sur Gemini
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # Cle API Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modele a utiliser
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

Configuration recommandée (environnement de production)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``system.properties`` (configurable également via Administration > Système > General) :

::

    # Definir le fournisseur LLM sur Gemini
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # Cle API Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuration du modele (utiliser le modele rapide)
    rag.llm.gemini.model=gemini-3-flash-preview

    # Point de terminaison API (generalement pas besoin de modifier)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Configuration du timeout
    rag.llm.gemini.timeout=60000

Éléments de configuration
=========================

Tous les éléments de configuration disponibles pour le client Gemini. Tous sauf ``rag.llm.name`` se configurent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.gemini.api.key``
     - Clé API Google AI (doit être définie pour utiliser l'API Gemini)
     - ``""``
   * - ``rag.llm.gemini.model``
     - Nom du modèle à utiliser
     - ``gemini-3.1-flash-lite-preview``
   * - ``rag.llm.gemini.api.url``
     - URL de base de l'API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Timeout de la requête (millisecondes)
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - Intervalle de vérification de disponibilité (secondes)
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - Nombre maximum de requêtes simultanées
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents lors de l'évaluation
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - Nombre maximum de caractères pour la description du document lors de l'évaluation
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - Délai d'attente des requêtes simultanées (millisecondes)
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - Nombre maximum de caractères de l'historique de chat
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - Nombre maximum de messages d'historique pour la détermination d'intention
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - Nombre maximum de caractères d'historique pour la détermination d'intention
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - Nombre maximum de caractères de l'historique de l'assistant
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - Nombre maximum de caractères du résumé de l'historique de l'assistant
     - ``1000``
   * - ``rag.llm.gemini.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429`` et ``5xx``)
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - Délai de base du backoff exponentiel (millisecondes)
     - ``2000``

Méthode d'authentification
===========================

La clé API est transmise via l'en-tête HTTP ``x-goog-api-key`` (méthode recommandée par Google).
Elle n'est plus ajoutée à l'URL en tant que paramètre de requête ``?key=...`` comme auparavant ; la clé API ne reste donc plus dans les journaux d'accès.

Comportement de réessai
========================

Les requêtes vers l'API Gemini sont automatiquement réessayées pour les codes de statut HTTP suivants :

- ``429`` Resource Exhausted (dépassement de quota / limitation de débit)
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Lors d'un réessai, |Fess| attend selon un backoff exponentiel (valeur de base ``rag.llm.gemini.retry.base.delay.ms`` millisecondes, jusqu'à ``rag.llm.gemini.retry.max`` tentatives, avec une gigue de +/-20%).
Pour les requêtes en streaming, seule la connexion initiale est sujette aux réessais ; les erreurs survenant après le début de la réception du corps de la réponse sont propagées immédiatement.

Configuration par type de prompt
==================================

Dans |Fess|, les paramètres du LLM peuvent être configurés finement par type de prompt.
La configuration par type de prompt s'écrit dans ``fess_config.properties``.

Format de configuration
------------------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

Types de prompt disponibles
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type de prompt
     - Description
   * - ``intent``
     - Prompt pour déterminer l'intention de l'utilisateur
   * - ``evaluation``
     - Prompt pour évaluer la pertinence des documents
   * - ``unclear``
     - Prompt pour le cas où la question est peu claire
   * - ``noresults``
     - Prompt pour le cas où il n'y a pas de résultats de recherche
   * - ``docnotfound``
     - Prompt pour le cas où le document n'est pas trouvé
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

Valeurs par défaut par type de prompt
---------------------------------------

Valeurs par défaut pour chaque type de prompt. Ces valeurs sont utilisées lorsqu'aucune configuration explicite n'est définie.

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - Type de prompt
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``512``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - ``0``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``0``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

Exemple de configuration
-------------------------

::

    # Configuration de la temperature pour la generation de reponse
    rag.llm.gemini.answer.temperature=0.7

    # Nombre maximum de tokens pour la generation de resume
    rag.llm.gemini.summary.max.tokens=2048

    # Nombre maximum de caracteres du contexte pour la generation de reponse
    rag.llm.gemini.answer.context.max.chars=16000

    # Nombre maximum de caracteres du contexte pour la generation de resume
    rag.llm.gemini.summary.context.max.chars=16000

    # Nombre maximum de caracteres du contexte pour la generation de FAQ
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   La valeur par défaut de ``context.max.chars`` varie selon le type de prompt.
   ``answer`` et ``summary`` sont à 16000, ``faq`` est à 10000, et les autres types de prompt sont à 10000.

Prise en charge des modèles de réflexion
==========================================

Gemini prend en charge les modèles de réflexion (Thinking Model).
L'utilisation de modèles de réflexion permet au modèle d'exécuter un processus de raisonnement interne avant de générer une réponse, produisant ainsi des réponses plus précises.

Le budget de réflexion se configure par type de prompt dans ``fess_config.properties``. |Fess| convertit automatiquement la valeur entière (nombre de tokens) de ``rag.llm.gemini.{promptType}.thinking.budget`` vers le champ d'API approprié en fonction de la génération du modèle résolue lors de la requête.

::

    # Budget de reflexion pour la generation de reponse
    rag.llm.gemini.answer.thinking.budget=1024

    # Budget de reflexion pour la generation de resume
    rag.llm.gemini.summary.thinking.budget=1024

Mappage selon la génération du modèle
---------------------------------------

- **Gemini 2.x** (par exemple ``gemini-2.5-flash``) : la valeur entière configurée est envoyée telle quelle en tant que ``thinkingConfig.thinkingBudget``. Spécifier ``0`` désactive complètement la réflexion.
- **Gemini 3.x** (par exemple ``gemini-3.1-flash-lite-preview``) : la valeur entière est regroupée en compartiments et envoyée comme valeur énumérée de ``thinkingConfig.thinkingLevel`` (``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH``).

Le mappage des compartiments pour Gemini 3.x est le suivant :

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Valeur du budget
     - thinkingLevel
     - Remarques
   * - ``<=0``
     - ``MINIMAL`` ou ``LOW``
     - ``MINIMAL`` pour les modèles Flash / Flash-Lite ; ``LOW`` pour les modèles de la famille Pro qui ne prennent pas en charge ``MINIMAL`` (``gemini-3-pro`` / ``gemini-3.1-pro``)
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x consomme toujours un certain nombre de tokens de réflexion, quel que soit le compartiment (même avec ``thinkingLevel=MINIMAL``, plusieurs centaines de tokens peuvent être consommés).
   Pour cette raison, lors de l'utilisation d'un modèle Gemini 3.x, |Fess| ajoute automatiquement une marge supplémentaire (1024 tokens) à la valeur ``maxOutputTokens`` par défaut, afin d'éviter une troncature de la réponse due à ``finishReason=MAX_TOKENS``.
   Avec Gemini 2.x, ``thinkingBudget=0`` désactive la réflexion elle-même, donc aucune marge supplémentaire n'est ajoutée.

.. note::
   Configurer un budget de réflexion élevé peut allonger le temps de réponse.
   Configurez une valeur appropriée selon l'usage.

Configuration via options JVM
==============================

Pour des raisons de sécurité, il est recommandé de configurer la clé API via
l'environnement d'exécution (options JVM) plutôt que via des fichiers de configuration.

Environnement Docker
---------------------

Le dépôt officiel `docker-fess <https://github.com/codelibs/docker-fess>`__
inclut un overlay Gemini (``compose-gemini.yaml``). Étapes minimales :

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Contenu de ``compose-gemini.yaml`` (référence pour un setup équivalent) :

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

Points clés :

- ``FESS_PLUGINS=fess-llm-gemini:15.8.0`` fait que ``run.sh`` télécharge automatiquement le plugin JAR et le place dans ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` active le mode de recherche IA
- ``-Dfess.config.rag.llm.gemini.api.key=...`` définit la clé API, ``-Dfess.config.rag.llm.gemini.model=...`` choisit le modèle
- ``-Dfess.system.rag.llm.name=gemini`` n'agit que comme valeur par défaut initiale avant qu'une valeur ne soit persistée dans OpenSearch. Après démarrage, le paramètre peut aussi être modifié sous Administration > Système > General (section RAG)

Si l'accès Internet passe par un proxy, spécifiez la configuration ``http.proxy.*`` de |Fess| via ``FESS_JAVA_OPTS`` (voir la section "Utilisation via un proxy HTTP" ci-dessous).

Environnement systemd
----------------------

Ajouter à ``FESS_JAVA_OPTS`` dans ``/etc/sysconfig/fess`` (ou ``/etc/default/fess``) :

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

Utilisation via un proxy HTTP
==============================

Le client Gemini partage la configuration de proxy HTTP commune à |Fess|. Spécifiez les propriétés suivantes dans ``fess_config.properties``.

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
   Les propriétés système Java traditionnelles (``-Dhttps.proxyHost``, etc.) ne sont pas prises en compte par le client Gemini.

Utilisation via Vertex AI
==========================

Si vous utilisez Google Cloud Platform, vous pouvez également utiliser Gemini via Vertex AI.
Pour Vertex AI, le point de terminaison API et la méthode d'authentification diffèrent.

.. note::
   |Fess| actuel utilise l'API Google AI (generativelanguage.googleapis.com).
   Si l'utilisation via Vertex AI est nécessaire, une implémentation personnalisée peut être requise.

Guide de sélection des modèles
================================

Guide pour la sélection du modèle selon l'usage.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modèle
     - Vitesse
     - Qualité
     - Usage
   * - ``gemini-3.1-flash-lite-preview``
     - Rapide
     - Élevée
     - Léger et à faible coût (par défaut, prend en charge ``thinkingLevel=MINIMAL``)
   * - ``gemini-3-flash-preview``
     - Rapide
     - Maximale
     - Usage général (prend en charge ``thinkingLevel=MINIMAL``)
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - Moyenne
     - Maximale
     - Raisonnement complexe (``MINIMAL`` non pris en charge ; au minimum ``LOW``)
   * - ``gemini-2.5-flash``
     - Rapide
     - Élevée
     - Version stable, priorité au coût
   * - ``gemini-2.5-pro``
     - Moyenne
     - Élevée
     - Version stable, long contexte

Fenêtre de contexte
--------------------

Les modèles Gemini prennent en charge des fenêtres de contexte très longues :

- **Gemini 3 Flash / 2.5 Flash** : Maximum 1 million de tokens
- **Gemini 3.1 Pro / 2.5 Pro** : Maximum 1 million de tokens (3.1 Pro) / 2 millions de tokens (2.5 Pro)

Cette caractéristique permet d'inclure davantage de résultats de recherche dans le contexte.

::

    # Inclure davantage de documents dans le contexte (a configurer dans fess_config.properties)
    rag.llm.gemini.answer.context.max.chars=20000

Estimation des coûts
---------------------

L'API Google AI est facturée à l'usage (avec une offre gratuite).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modèle
     - Entrée (1M caractères)
     - Sortie (1M caractères)
   * - Gemini 3 Flash Preview
     - $0.50
     - $3.00
   * - Gemini 3.1 Pro Preview
     - $2.00
     - $12.00
   * - Gemini 2.5 Flash
     - $0.075
     - $0.30
   * - Gemini 2.5 Pro
     - $1.25
     - $5.00

.. note::
   Pour les derniers prix et informations sur l'offre gratuite, consultez `Google AI Pricing <https://ai.google.dev/pricing>`__.

Contrôle des requêtes simultanées
===================================

Dans |Fess|, le nombre de requêtes simultanées vers Gemini peut être contrôlé.
Configurez la propriété suivante dans ``fess_config.properties``.

::

    # Nombre maximum de requetes simultanees (par defaut : 5)
    rag.llm.gemini.max.concurrent.requests=5

Cette configuration permet d'éviter les requêtes excessives vers l'API Google AI et de prévenir les erreurs de limitation de débit.

Limites de l'offre gratuite (à titre indicatif)
-------------------------------------------------

L'API Google AI dispose d'une offre gratuite avec les limites suivantes :

- Requêtes/minute : 15 RPM
- Tokens/minute : 1 million TPM
- Requêtes/jour : 1,500 RPD

Lors de l'utilisation de l'offre gratuite, il est recommandé de configurer ``rag.llm.gemini.max.concurrent.requests`` à une valeur basse.

Dépannage
==========

Erreur d'authentification
--------------------------

**Symptôme** : Erreur liée à la clé API

**Points à vérifier** :

1. Vérifier si la clé API est correctement configurée
2. Vérifier si la clé API est valide dans Google AI Studio
3. Vérifier si la clé API a les permissions nécessaires
4. Vérifier si l'API est activée dans le projet

Erreur de limitation de débit
-------------------------------

**Symptôme** : Erreur "429 Resource has been exhausted"

**Solution** :

1. Réduire le nombre de requêtes simultanées dans ``fess_config.properties``::

    rag.llm.gemini.max.concurrent.requests=3

2. Attendre quelques minutes avant de réessayer
3. Demander une augmentation de quota si nécessaire

Restriction de région
----------------------

**Symptôme** : Erreur indiquant que le service n'est pas disponible

**Points à vérifier** :

L'API Google AI n'est disponible que dans certaines régions. Consultez la documentation Google
pour les régions prises en charge.

Timeout
--------

**Symptôme** : La requête expire

**Solution** :

1. Augmenter le temps de timeout ::

    rag.llm.gemini.timeout=120000

2. Envisager l'utilisation du modèle Flash (plus rapide)

Configuration de débogage
--------------------------

Pour investiguer les problèmes, ajustez le niveau de log de |Fess| pour afficher des logs détaillés liés à Gemini.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

Notes de sécurité
==================

Lors de l'utilisation de l'API Google AI, faites attention aux points de sécurité suivants.

1. **Confidentialité des données** : Le contenu des résultats de recherche est envoyé aux serveurs Google
2. **Gestion des clés API** : La fuite de clés peut entraîner une utilisation non autorisée
3. **Conformité** : Si les données contiennent des informations confidentielles, vérifiez les politiques de votre organisation
4. **Conditions d'utilisation** : Respectez les conditions d'utilisation et la Politique d'utilisation acceptable de Google

Informations de référence
==========================

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - Aperçu de l'intégration LLM
- :doc:`rag-chat` - Détails de la fonctionnalité de mode de recherche IA
- :doc:`rank-fusion` - Recherche hybride : combiner recherche par mots-clés et recherche sémantique (vectorielle)
- :doc:`../user/chat-search` - Utilisation du mode de recherche IA (guide utilisateur)
