==========================
Configuration Google Gemini
==========================

Apercu
====

Google Gemini est un grand modele de langage (LLM) de pointe fourni par Google.
|Fess| peut utiliser l'API Google AI (Generative Language API) pour realiser la fonctionnalite de mode de recherche IA avec les modeles Gemini.

L'utilisation de Gemini permet de generer des reponses de haute qualite en tirant parti de la derniere technologie IA de Google.

Caracteristiques principales
--------

- **Prise en charge multimodale** : Peut traiter les images en plus du texte
- **Long contexte** : Fenetre de contexte longue permettant de traiter de grandes quantites de documents a la fois
- **Efficacite des couts** : Le modele Flash est rapide et peu couteux
- **Integration Google** : Integration facile avec les services Google Cloud

Modeles pris en charge
----------

Principaux modeles disponibles avec Gemini :

- ``gemini-3.1-flash-lite-preview`` - Modele rapide leger et a faible cout (par defaut)
- ``gemini-3-flash-preview`` - Modele Flash standard
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - Modeles de raisonnement avance
- ``gemini-2.5-flash`` - Version stable du modele rapide
- ``gemini-2.5-pro`` - Version stable du modele de raisonnement

.. note::
   Pour les derniers modeles disponibles, consultez `Google AI for Developers <https://ai.google.dev/models/gemini>`__.

Prerequis
========

Avant d'utiliser Gemini, preparez les elements suivants.

1. **Compte Google** : Un compte Google est requis
2. **Acces Google AI Studio** : Accedez a `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **Cle API** : Generez une cle API dans Google AI Studio

Obtention de la cle API
-------------

1. Accedez a `Google AI Studio <https://aistudio.google.com/>`__
2. Cliquez sur "Get API key"
3. Selectionnez "Create API key"
4. Selectionnez ou creez un projet
5. Enregistrez la cle API generee en lieu sur

.. warning::
   La cle API est une information confidentielle. Faites attention aux points suivants :

   - Ne pas la commiter dans un systeme de gestion de versions
   - Ne pas l'afficher dans les logs
   - La gerer via des variables d'environnement ou des fichiers de configuration securises

Installation du plugin
========================

Dans |Fess| 15.6, la fonctionnalite d'integration Gemini est fournie sous forme de plugin ``fess-llm-gemini``.
Pour utiliser Gemini, l'installation du plugin est necessaire.

1. Telechargez `fess-llm-gemini-15.6.0.jar`
2. Placez-le dans le repertoire ``app/WEB-INF/plugin/`` de |Fess|
3. Redemarrez |Fess|

::

    # Exemple de placement du plugin
    cp fess-llm-gemini-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   La version du plugin doit correspondre a la version de |Fess|.

Configuration de base
========

Dans |Fess| 15.6, l'activation de la fonctionnalite de mode de recherche IA et les parametres specifiques a Gemini s'effectuent dans ``fess_config.properties``, et la selection du fournisseur LLM (``rag.llm.name``) s'effectue via l'administration ou dans ``system.properties``.

Configuration de fess_config.properties
----------------------------

Ajoutez la configuration d'activation de la fonctionnalite de mode de recherche IA dans ``app/WEB-INF/conf/fess_config.properties``.

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

Configuration du fournisseur LLM
---------------------

Le fournisseur LLM se configure via l'administration (Administration > Systeme > General) ou dans ``system.properties``.

Configuration minimale (fess_config.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Activer la fonctionnalite de mode de recherche IA
    rag.chat.enabled=true

    # Cle API Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modele a utiliser
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

Configuration minimale (system.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Definir le fournisseur LLM sur Gemini
    rag.llm.name=gemini

Configuration recommandee (environnement de production, fess_config.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Configuration recommandee (environnement de production, system.properties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Definir le fournisseur LLM sur Gemini
    rag.llm.name=gemini

Elements de configuration
========

Tous les elements de configuration disponibles pour le client Gemini. Tous se configurent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.gemini.api.key``
     - Cle API Google AI (doit etre definie pour utiliser l'API Gemini)
     - ``""``
   * - ``rag.llm.gemini.model``
     - Nom du modele a utiliser
     - ``gemini-3.1-flash-lite-preview``
   * - ``rag.llm.gemini.api.url``
     - URL de base de l'API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Timeout de la requete (millisecondes)
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - Intervalle de verification de disponibilite (secondes)
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - Nombre maximum de requetes simultanees
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents lors de l'evaluation
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - Nombre maximum de caracteres pour la description du document lors de l'evaluation
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - Delai d'attente des requetes simultanees (millisecondes)
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - Nombre maximum de caracteres de l'historique de chat
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - Nombre maximum de messages d'historique pour la determination d'intention
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - Nombre maximum de caracteres d'historique pour la determination d'intention
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - Nombre maximum de caracteres de l'historique de l'assistant
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - Nombre maximum de caracteres du resume de l'historique de l'assistant
     - ``1000``
   * - ``rag.llm.gemini.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429`` et ``5xx``)
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - Delai de base du backoff exponentiel (millisecondes)
     - ``2000``

Methode d'authentification
==========================

Depuis |Fess| 15.6.1, la cle API est transmise via l'en-tete HTTP ``x-goog-api-key`` (methode recommandee par Google).
Elle n'est plus ajoutee a l'URL en tant que parametre de requete ``?key=...`` comme auparavant ; la cle API ne reste donc plus dans les journaux d'acces.

Comportement de reessai
=======================

Les requetes vers l'API Gemini sont automatiquement reessayees pour les codes de statut HTTP suivants :

- ``429`` Resource Exhausted (depassement de quota / limitation de debit)
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Lors d'un reessai, |Fess| attend selon un backoff exponentiel (valeur de base ``rag.llm.gemini.retry.base.delay.ms`` millisecondes, jusqu'a ``rag.llm.gemini.retry.max`` tentatives, avec une gigue de +/-20%).
Pour les requetes en streaming, seule la connexion initiale est sujette aux reessais ; les erreurs survenant apres le debut de la reception du corps de la reponse sont propagees immediatement.

Configuration par type de prompt
======================

Dans |Fess|, les parametres du LLM peuvent etre configures finement par type de prompt.
La configuration par type de prompt s'ecrit dans ``fess_config.properties``.

Format de configuration
----------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

Types de prompt disponibles
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type de prompt
     - Description
   * - ``intent``
     - Prompt pour determiner l'intention de l'utilisateur
   * - ``evaluation``
     - Prompt pour evaluer la pertinence des documents
   * - ``unclear``
     - Prompt pour le cas ou la question est peu claire
   * - ``noresults``
     - Prompt pour le cas ou il n'y a pas de resultats de recherche
   * - ``docnotfound``
     - Prompt pour le cas ou le document n'est pas trouve
   * - ``answer``
     - Prompt de generation de reponse
   * - ``summary``
     - Prompt de generation de resume
   * - ``faq``
     - Prompt de generation de FAQ
   * - ``direct``
     - Prompt de reponse directe
   * - ``queryregeneration``
     - Prompt de regeneration de requete

Valeurs par defaut par type de prompt
--------------------------------------

Valeurs par defaut pour chaque type de prompt. Ces valeurs sont utilisees lorsqu'aucune configuration explicite n'est definie.

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - Type de prompt
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``256``
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
     - ``256``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``4096``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

Exemple de configuration
------

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
   La valeur par defaut de ``context.max.chars`` varie selon le type de prompt.
   ``answer`` et ``summary`` sont a 16000, ``faq`` est a 10000, et les autres types de prompt sont a 10000.

Prise en charge des modeles de reflexion
==============

Gemini prend en charge les modeles de reflexion (Thinking Model).
L'utilisation de modeles de reflexion permet au modele d'executer un processus de raisonnement interne avant de generer une reponse, produisant ainsi des reponses plus precises.

Le budget de reflexion se configure par type de prompt dans ``fess_config.properties``. |Fess| convertit automatiquement la valeur entiere (nombre de tokens) de ``rag.llm.gemini.{promptType}.thinking.budget`` vers le champ d'API approprie en fonction de la generation du modele resolue lors de la requete.

::

    # Budget de reflexion pour la generation de reponse
    rag.llm.gemini.answer.thinking.budget=1024

    # Budget de reflexion pour la generation de resume
    rag.llm.gemini.summary.thinking.budget=1024

Mappage selon la generation du modele
-------------------------------------

- **Gemini 2.x** (par exemple ``gemini-2.5-flash``) : la valeur entiere configuree est envoyee telle quelle en tant que ``thinkingConfig.thinkingBudget``. Specifier ``0`` desactive completement la reflexion.
- **Gemini 3.x** (par exemple ``gemini-3.1-flash-lite-preview``) : la valeur entiere est regroupee en compartiments et envoyee comme valeur enumeree de ``thinkingConfig.thinkingLevel`` (``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH``).

Le mappage des compartiments pour Gemini 3.x est le suivant :

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Valeur du budget
     - thinkingLevel
     - Remarques
   * - ``<=0``
     - ``MINIMAL`` ou ``LOW``
     - ``MINIMAL`` pour les modeles Flash / Flash-Lite ; ``LOW`` pour les modeles de la famille Pro qui ne prennent pas en charge ``MINIMAL`` (``gemini-3-pro`` / ``gemini-3.1-pro``)
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x consomme toujours un certain nombre de tokens de reflexion, quel que soit le compartiment (meme avec ``thinkingLevel=MINIMAL``, plusieurs centaines de tokens peuvent etre consommes).
   Pour cette raison, lors de l'utilisation d'un modele Gemini 3.x, |Fess| ajoute automatiquement une marge supplementaire (1024 tokens) a la valeur ``maxOutputTokens`` par defaut, afin d'eviter une troncature de la reponse due a ``finishReason=MAX_TOKENS``.
   Avec Gemini 2.x, ``thinkingBudget=0`` desactive la reflexion elle-meme, donc aucune marge supplementaire n'est ajoutee.

.. note::
   Configurer un budget de reflexion eleve peut allonger le temps de reponse.
   Configurez une valeur appropriee selon l'usage.

Configuration via options JVM
=============================

Pour des raisons de securite, il est recommande de configurer la cle API via
l'environnement d'execution (options JVM) plutot que via des fichiers versionnes.

Environnement Docker
--------------------

Le depot officiel `docker-fess <https://github.com/codelibs/docker-fess>`__
fournit un overlay Gemini (``compose-gemini.yaml``). Etapes minimales :

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Contenu de ``compose-gemini.yaml`` (reference pour un setup equivalent) :

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

Notes :

- ``FESS_PLUGINS=fess-llm-gemini:15.6.0`` fait que ``run.sh`` du conteneur telecharge et installe automatiquement le plugin dans ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` active le mode IA
- ``-Dfess.config.rag.llm.gemini.api.key=...`` definit la cle API, ``-Dfess.config.rag.llm.gemini.model=...`` choisit le modele
- ``-Dfess.system.rag.llm.name=gemini`` n'agit que comme valeur par defaut initiale avant qu'une valeur ne soit persistee dans OpenSearch. Apres demarrage, le parametre peut aussi etre modifie sous Administration > Systeme > General (section RAG)

Si l'acces Internet passe par un proxy, specifiez la configuration ``http.proxy.*`` de |Fess| via ``FESS_JAVA_OPTS`` (voir la section "Utilisation via un proxy HTTP" ci-dessous).

Environnement systemd
---------------------

Ajouter a ``FESS_JAVA_OPTS`` dans ``/etc/sysconfig/fess`` (ou ``/etc/default/fess``) :

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

Utilisation via un proxy HTTP
=============================

Depuis |Fess| 15.6.1, le client Gemini partage la configuration de proxy HTTP commune a |Fess|. Specifiez les proprietes suivantes dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``http.proxy.host``
     - Nom d'hote du proxy (chaine vide pour ne pas utiliser de proxy)
     - ``""``
   * - ``http.proxy.port``
     - Numero de port du proxy
     - ``8080``
   * - ``http.proxy.username``
     - Nom d'utilisateur pour l'authentification du proxy (facultatif ; lorsqu'il est renseigne, l'authentification Basic est activee)
     - ``""``
   * - ``http.proxy.password``
     - Mot de passe pour l'authentification du proxy
     - ``""``

Dans un environnement Docker, specifiez ce qui suit dans ``FESS_JAVA_OPTS``::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   Cette configuration s'applique egalement a tous les acces HTTP de |Fess|, notamment ceux du crawler.
   Les proprietes systeme Java traditionnelles (``-Dhttps.proxyHost``, etc.) ne sont pas prises en compte par le client Gemini.

Utilisation via Vertex AI
===================

Si vous utilisez Google Cloud Platform, vous pouvez egalement utiliser Gemini via Vertex AI.
Pour Vertex AI, le point de terminaison API et la methode d'authentification different.

.. note::
   |Fess| actuel utilise l'API Google AI (generativelanguage.googleapis.com).
   Si l'utilisation via Vertex AI est necessaire, une implementation personnalisee peut etre requise.

Guide de selection des modeles
==================

Guide pour la selection du modele selon l'usage.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modele
     - Vitesse
     - Qualite
     - Usage
   * - ``gemini-3.1-flash-lite-preview``
     - Rapide
     - Elevee
     - Leger et a faible cout (par defaut, prend en charge ``thinkingLevel=MINIMAL``)
   * - ``gemini-3-flash-preview``
     - Rapide
     - Maximale
     - Usage general (prend en charge ``thinkingLevel=MINIMAL``)
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - Moyenne
     - Maximale
     - Raisonnement complexe (``MINIMAL`` non pris en charge ; au minimum ``LOW``)
   * - ``gemini-2.5-flash``
     - Rapide
     - Elevee
     - Version stable, priorite au cout
   * - ``gemini-2.5-pro``
     - Moyenne
     - Elevee
     - Version stable, long contexte

Fenetre de contexte
----------------------

Les modeles Gemini prennent en charge des fenetres de contexte tres longues :

- **Gemini 3 Flash / 2.5 Flash** : Maximum 1 million de tokens
- **Gemini 3.1 Pro / 2.5 Pro** : Maximum 1 million de tokens (3.1 Pro) / 2 millions de tokens (2.5 Pro)

Cette caracteristique permet d'inclure davantage de resultats de recherche dans le contexte.

::

    # Inclure davantage de documents dans le contexte (a configurer dans fess_config.properties)
    rag.llm.gemini.answer.context.max.chars=20000

Estimation des couts
------------

L'API Google AI est facturee a l'usage (avec une offre gratuite).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modele
     - Entree (1M caracteres)
     - Sortie (1M caracteres)
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

Controle des requetes simultanees
==================

Dans |Fess|, le nombre de requetes simultanees vers Gemini peut etre controle.
Configurez la propriete suivante dans ``fess_config.properties``.

::

    # Nombre maximum de requetes simultanees (par defaut : 5)
    rag.llm.gemini.max.concurrent.requests=5

Cette configuration permet d'eviter les requetes excessives vers l'API Google AI et de prevenir les erreurs de limitation de debit.

Limites de l'offre gratuite (a titre indicatif)
--------------------

L'API Google AI dispose d'une offre gratuite avec les limites suivantes :

- Requetes/minute : 15 RPM
- Tokens/minute : 1 million TPM
- Requetes/jour : 1,500 RPD

Lors de l'utilisation de l'offre gratuite, il est recommande de configurer ``rag.llm.gemini.max.concurrent.requests`` a une valeur basse.

Depannage
======================

Erreur d'authentification
----------

**Symptome** : Erreur liee a la cle API

**Points a verifier** :

1. Verifier si la cle API est correctement configuree
2. Verifier si la cle API est valide dans Google AI Studio
3. Verifier si la cle API a les permissions necessaires
4. Verifier si l'API est activee dans le projet

Erreur de limitation de debit
----------------

**Symptome** : Erreur "429 Resource has been exhausted"

**Solution** :

1. Reduire le nombre de requetes simultanees dans ``fess_config.properties``::

    rag.llm.gemini.max.concurrent.requests=3

2. Attendre quelques minutes avant de reessayer
3. Demander une augmentation de quota si necessaire

Restriction de region
--------------

**Symptome** : Erreur indiquant que le service n'est pas disponible

**Points a verifier** :

L'API Google AI n'est disponible que dans certaines regions. Consultez la documentation Google
pour les regions prises en charge.

Timeout
------------

**Symptome** : La requete expire

**Solution** :

1. Augmenter le temps de timeout ::

    rag.llm.gemini.timeout=120000

2. Envisager l'utilisation du modele Flash (plus rapide)

Configuration de debogage
------------

Pour investiguer les problemes, ajustez le niveau de log de |Fess| pour afficher des logs detailles lies a Gemini.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

Notes de securite
========================

Lors de l'utilisation de l'API Google AI, faites attention aux points de securite suivants.

1. **Confidentialite des donnees** : Le contenu des resultats de recherche est envoye aux serveurs Google
2. **Gestion des cles API** : La fuite de cles peut entrainer une utilisation non autorisee
3. **Conformite** : Si les donnees contiennent des informations confidentielles, verifiez les politiques de votre organisation
4. **Conditions d'utilisation** : Respectez les conditions d'utilisation et la Politique d'utilisation acceptable de Google

Informations de reference
========

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - Apercu de l'integration LLM
- :doc:`rag-chat` - Details de la fonctionnalite de mode de recherche IA
