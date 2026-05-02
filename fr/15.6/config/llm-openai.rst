==========================
Configuration OpenAI
==========================

Apercu
====

OpenAI est un service cloud fournissant des grands modeles de langage (LLM) haute performance,
dont GPT-4. |Fess| peut utiliser l'API OpenAI pour realiser la fonctionnalite de mode de recherche IA.

L'utilisation d'OpenAI permet de generer des reponses de haute qualite avec les modeles d'IA les plus avances.

Caracteristiques principales
--------

- **Reponses de haute qualite** : Generation de reponses precises avec les derniers modeles GPT
- **Evolutivite** : Mise a l'echelle facile grace au service cloud
- **Amelioration continue** : Performances ameliorees grace aux mises a jour regulieres des modeles
- **Fonctionnalites riches** : Prise en charge de diverses taches comme la generation de texte, le resume, la traduction

Modeles pris en charge
----------

Principaux modeles disponibles avec OpenAI :

- ``gpt-5`` - Dernier modele haute performance
- ``gpt-5-mini`` - Version allegee de GPT-5 (bon rapport cout-efficacite)
- ``gpt-4o`` - Modele multimodal haute performance
- ``gpt-4o-mini`` - Version allegee de GPT-4o
- ``o3-mini`` - Modele leger specialise dans le raisonnement
- ``o4-mini`` - Modele leger de nouvelle generation specialise dans le raisonnement

.. note::
   Pour les derniers modeles disponibles, consultez `OpenAI Models <https://platform.openai.com/docs/models>`__.

.. note::
   Lors de l'utilisation de modeles de la serie o1/o3/o4 ou de la serie gpt-5, |Fess| utilise automatiquement le parametre ``max_completion_tokens`` de l'API OpenAI. Aucune modification de configuration n'est necessaire.

Prerequis
========

Avant d'utiliser OpenAI, preparez les elements suivants.

1. **Compte OpenAI** : Creez un compte sur `https://platform.openai.com/ <https://platform.openai.com/>`__
2. **Cle API** : Generez une cle API dans le tableau de bord OpenAI
3. **Configuration de facturation** : Configurez les informations de facturation car l'utilisation de l'API est payante

Obtention de la cle API
-------------

1. Connectez-vous a `OpenAI Platform <https://platform.openai.com/>`__
2. Accedez a la section "API keys"
3. Cliquez sur "Create new secret key"
4. Entrez un nom pour la cle et creez-la
5. Enregistrez la cle affichee en lieu sur (elle ne sera affichee qu'une seule fois)

.. warning::
   La cle API est une information confidentielle. Faites attention aux points suivants :

   - Ne pas la commiter dans un systeme de gestion de versions
   - Ne pas l'afficher dans les logs
   - La gerer via des variables d'environnement ou des fichiers de configuration securises

Installation du plugin
========================

Dans |Fess| 15.6, la fonctionnalite d'integration OpenAI est fournie sous forme de plugin. Pour l'utiliser, l'installation du plugin ``fess-llm-openai`` est necessaire.

1. Telechargez `fess-llm-openai-15.6.0.jar`
2. Placez le fichier JAR dans le repertoire ``app/WEB-INF/plugin/`` du repertoire d'installation de |Fess|::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Redemarrez |Fess|

.. note::
   La version du plugin doit correspondre a la version de |Fess|.

Configuration de base
========

Dans |Fess| 15.6, les elements de configuration sont repartis dans les deux fichiers suivants selon leur usage.

- ``app/WEB-INF/conf/fess_config.properties`` - Configuration principale de |Fess| et configuration specifique au fournisseur LLM
- ``system.properties`` - Selection du fournisseur LLM (``rag.llm.name``), a configurer via l'administration (Administration > Systeme > General) ou directement dans le fichier

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

``system.properties`` (configurable egalement via Administration > Systeme > General) :

::

    # Definir le fournisseur LLM sur OpenAI
    rag.llm.name=openai

Configuration recommandee (environnement de production)
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

``system.properties`` (configurable egalement via Administration > Systeme > General) :

::

    # Configuration du fournisseur LLM
    rag.llm.name=openai

Elements de configuration
========

Tous les elements de configuration disponibles pour le client OpenAI. Sauf ``rag.llm.name``, tous se configurent dans ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - Propriete
     - Description
     - Valeur par defaut
     - Emplacement
   * - ``rag.llm.name``
     - Nom du fournisseur LLM (specifier ``openai``)
     - ``ollama``
     - system.properties
   * - ``rag.llm.openai.api.key``
     - Cle API OpenAI
     - (Requis)
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - Nom du modele a utiliser
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - URL de base de l'API
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - Timeout de la requete (millisecondes)
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - Intervalle de verification de disponibilite (secondes)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - Nombre maximum de requetes simultanees
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents lors de l'evaluation
     - ``3``
     - fess_config.properties
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - Timeout d'attente des requetes simultanees (ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - Multiplicateur de max tokens pour les modeles de raisonnement
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429`` et ``5xx``)
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - Delai de base du backoff exponentiel (millisecondes)
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - Envoyer ``stream_options.include_usage=true`` en streaming et recevoir les informations d'utilisation des tokens dans le dernier chunk
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - Nombre maximum de caracteres pour l'historique de conversation
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - Nombre maximum de messages d'historique pour la detection d'intention
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - Nombre maximum de caracteres d'historique pour la detection d'intention
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - Nombre maximum de caracteres pour les messages de l'assistant
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - Nombre maximum de caracteres pour le resume de l'assistant
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - Nombre maximum de caracteres pour la description de document en evaluation
     - ``500``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - Activation de la fonctionnalite de mode de recherche IA
     - ``false``
     - fess_config.properties

Configuration par type de prompt
======================

Dans |Fess|, des parametres individuels peuvent etre configures pour chaque type de prompt. La configuration s'effectue dans ``fess_config.properties``.

Patterns de configuration
------------

La configuration par type de prompt se specifie selon les patterns suivants :

- ``rag.llm.openai.{promptType}.temperature`` - Caractere aleatoire de la generation (0.0 a 2.0). Ignore pour les modeles de raisonnement (serie o1/o3/o4/gpt-5)
- ``rag.llm.openai.{promptType}.max.tokens`` - Nombre maximum de tokens
- ``rag.llm.openai.{promptType}.context.max.chars`` - Nombre maximum de caracteres du contexte (defaut : ``16000`` pour answer/summary, ``10000`` pour les autres)

Types de prompt
----------------

Types de prompt disponibles :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Type de prompt
     - Description
   * - ``intent``
     - Prompt pour determiner l'intention de l'utilisateur
   * - ``evaluation``
     - Prompt pour evaluer la pertinence des resultats de recherche
   * - ``unclear``
     - Prompt de reponse pour les requetes peu claires
   * - ``noresults``
     - Prompt de reponse lorsqu'il n'y a pas de resultats de recherche
   * - ``docnotfound``
     - Prompt de reponse lorsque le document n'est pas trouve
   * - ``answer``
     - Prompt pour generer une reponse
   * - ``summary``
     - Prompt pour generer un resume
   * - ``faq``
     - Prompt pour generer une FAQ
   * - ``direct``
     - Prompt pour repondre directement
   * - ``queryregeneration``
     - Prompt de regeneration de requetes

Valeurs par defaut
------------------

Valeurs par defaut pour chaque type de prompt. La configuration de temperature est ignoree pour les modeles de raisonnement (serie o1/o3/o4/gpt-5).

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Type de prompt
     - Temperature
     - Max Tokens
     - Remarques
   * - ``intent``
     - 0.1
     - 256
     - Detection d'intention deterministe
   * - ``evaluation``
     - 0.1
     - 256
     - Evaluation de pertinence deterministe
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
     - Generation de reponse principale
   * - ``summary``
     - 0.3
     - 2048
     - Generation de resume
   * - ``queryregeneration``
     - 0.3
     - 256
     - Regeneration de requetes

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

Comportement de reessai
=======================

Les requetes vers l'API OpenAI sont automatiquement reessayees pour les codes de statut HTTP suivants :

- ``429`` Too Many Requests (limitation de debit)
- ``500`` Internal Server Error
- ``502`` Bad Gateway (qu'OpenAI peut renvoyer en cas de surcharge en amont)
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Lors d'un reessai, |Fess| attend selon un backoff exponentiel (valeur de base ``rag.llm.openai.retry.base.delay.ms`` millisecondes, jusqu'a ``rag.llm.openai.retry.max`` tentatives, avec une gigue de +/-20%).
Si le serveur renvoie un en-tete ``Retry-After`` (en secondes entieres, plafonne a ``600`` secondes), cette valeur prend le pas sur le backoff exponentiel. Cela suit les recommandations officielles d'OpenAI.

A noter, les ``IOException`` (timeouts de connexion, reinitialisations de socket, echecs DNS) ne sont pas reessayees. Si la requete a pu atteindre le serveur, un reessai pourrait entrainer une double facturation.
Pour les requetes en streaming, seule la connexion initiale est sujette aux reessais ; les erreurs survenant apres le debut de la reception du corps de la reponse sont propagees immediatement.

.. note::
   Avec les valeurs par defaut (10 tentatives maximum, base de 2 secondes), le pire cas pour la somme des 9 backoffs est ``2 + 4 + 8 + ... + 512 ~= 1022 secondes (environ 17 minutes)``. Lorsque ``Retry-After`` (jusqu'a 600 secondes) est renvoye a chaque tentative, le pire cas atteint ``9 x 600 secondes = 90 minutes``. Pour un controle plus strict de la latence, reduisez ``rag.llm.openai.retry.max``.

Streaming et informations d'utilisation
=======================================

Par defaut, ``stream_options.include_usage=true`` est ajoute aux requetes, ce qui permet de recevoir l'objet ``usage`` (incluant ``completion_tokens_details.reasoning_tokens`` pour les modeles de raisonnement et ``prompt_tokens_details.cached_tokens`` lorsque la mise en cache du prompt est utilisee) dans le dernier chunk SSE de la reponse en streaming.

Pour les backends qui n'acceptent pas le champ ``stream_options.include_usage`` (par exemple vLLM ou certaines passerelles compatibles Azure OpenAI), desactivez cette option ainsi::

    rag.llm.openai.stream.include.usage=false

Logs et detection d'anomalies
=============================

Depuis |Fess| 15.6.1, le client OpenAI emet les logs structures suivants. Cela permet de surveiller l'utilisation des tokens et les anomalies de reponse sans activer le niveau ``DEBUG``.

- ``[LLM:OPENAI] Stream completed.`` (INFO) - emis a la fin d'une reponse en streaming, avec le nombre de chunks, le delai jusqu'au premier chunk et les informations d'utilisation des tokens
- ``[LLM:OPENAI] Chat response received.`` (INFO) - emis a la fin d'une reponse non-streaming, avec des informations equivalentes
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` (WARN) - emis lorsque ``finish_reason`` est autre que ``stop`` (``length`` : troncature par max_tokens ; ``content_filter`` : moderation ; ``tool_calls`` / ``function_call`` : configuration d'appel d'outil non intentionnelle, etc.)
- ``[LLM:OPENAI] Stream refusal.`` (WARN) - emis lorsque ``delta.refusal`` est renvoye par une sortie structuree

Ces logs WARN peuvent etre exploites pour ajuster ``max_tokens``, auditer le filtre de contenu et detecter une mauvaise configuration de ``extra_params``.

Masquage des informations d'authentification dans les URL des logs
------------------------------------------------------------------

Les URL emises dans les logs voient automatiquement leurs parametres de requete contenant des informations d'authentification (``api_key``, ``apikey``, ``api-key``, ``key``, ``token``, ``access_token``, ``access-token``, sans distinction de casse) masques par ``***``.

Le point de terminaison officiel OpenAI (``https://api.openai.com``) s'authentifie via l'en-tete ``Authorization: Bearer`` et n'inclut donc pas d'informations d'authentification dans l'URL. Toutefois, si vous configurez ``rag.llm.openai.api.url`` vers un proxy personnalise qui accepte les informations d'authentification en tant que parametres de requete (certains deploiements Azure, passerelles vLLM, etc.), cela empeche egalement la fuite de la cle API dans les logs.

Prise en charge des modeles de raisonnement
==============

Lors de l'utilisation de modeles de raisonnement de la serie o1/o3/o4 ou de la serie gpt-5, |Fess| utilise automatiquement le parametre ``max_completion_tokens`` de l'API OpenAI a la place de ``max_tokens``. Aucune modification de configuration supplementaire n'est necessaire.

.. note::
   Les modeles de raisonnement (serie o1/o3/o4/gpt-5) ignorent le parametre ``temperature`` et utilisent une valeur fixe (1). De plus, lors de l'utilisation de modeles de raisonnement, le ``max_tokens`` par defaut est multiplie par ``reasoning.token.multiplier`` (defaut : 4).

Parametres supplementaires pour les modeles de raisonnement
----------------------------

Lors de l'utilisation de modeles de raisonnement, les parametres supplementaires suivants peuvent etre configures dans ``fess_config.properties`` :

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - Parametre d'effort de raisonnement pour les modeles de serie o (``low``, ``medium``, ``high``)
     - ``low`` (intent/evaluation/docnotfound/unclear/noresults/queryregeneration), non defini (autres)
   * - ``rag.llm.openai.{promptType}.top.p``
     - Seuil de probabilite pour la selection de tokens (0.0 a 1.0)
     - (Non defini)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - Penalite de frequence (-2.0 a 2.0)
     - (Non defini)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - Penalite de presence (-2.0 a 2.0)
     - (Non defini)

``{promptType}`` peut etre ``intent``, ``evaluation``, ``answer``, ``summary``, etc.

Exemple de configuration
------

::

    # Configurer l'effort de raisonnement sur high avec o3-mini
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # Configurer top_p et les penalites avec gpt-5
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

Configuration via options JVM
=============================

Pour des raisons de securite, il est recommande de configurer la cle API via
l'environnement d'execution (options JVM) plutot que via des fichiers versionnes.

Environnement Docker
--------------------

Le depot officiel `docker-fess <https://github.com/codelibs/docker-fess>`__
fournit un overlay OpenAI (``compose-openai.yaml``). Etapes minimales :

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

Contenu de ``compose-openai.yaml`` (reference pour un setup equivalent) :

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Notes :

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` fait que ``run.sh`` du conteneur telecharge et installe automatiquement le plugin dans ``app/WEB-INF/plugin/``
- ``-Dfess.config.rag.chat.enabled=true`` active le mode IA
- ``-Dfess.config.rag.llm.openai.api.key=...`` definit la cle API, ``-Dfess.config.rag.llm.openai.model=...`` choisit le modele
- ``-Dfess.system.rag.llm.name=openai`` n'agit que comme valeur par defaut initiale avant qu'une valeur ne soit persistee dans OpenSearch. Apres demarrage, le parametre peut aussi etre modifie sous Administration > Systeme > General (section RAG)

Si l'acces Internet passe par un proxy, specifiez la configuration ``http.proxy.*`` de |Fess| via ``FESS_JAVA_OPTS`` (voir la section "Utilisation via un proxy HTTP" ci-dessous).

Environnement systemd
---------------------

Ajouter a ``FESS_JAVA_OPTS`` dans ``/etc/sysconfig/fess`` (ou ``/etc/default/fess``) :

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

Utilisation via un proxy HTTP
=============================

Depuis |Fess| 15.6.1, le client OpenAI partage la configuration de proxy HTTP commune a |Fess|. Specifiez les proprietes suivantes dans ``fess_config.properties``.

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
   Les proprietes systeme Java traditionnelles (``-Dhttps.proxyHost``, etc.) ne sont pas prises en compte par le client OpenAI.

Utilisation d'Azure OpenAI
==================

Pour utiliser les modeles OpenAI via Microsoft Azure, modifiez le point de terminaison API.

::

    # Point de terminaison Azure OpenAI
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Cle API Azure
    rag.llm.openai.api.key=your-azure-api-key

    # Nom du deploiement (specifie comme nom de modele)
    rag.llm.openai.model=your-deployment-name

.. note::
   Lors de l'utilisation d'Azure OpenAI, le format des requetes API peut differer legerement.
   Consultez la documentation Azure OpenAI pour plus de details.

Guide de selection des modeles
==================

Guide pour la selection du modele selon l'usage.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modele
     - Cout
     - Qualite
     - Usage
   * - ``gpt-5-mini``
     - Moyen
     - Elevee
     - Usage equilibre (recommande)
   * - ``gpt-4o-mini``
     - Bas-Moyen
     - Elevee
     - Usage prioritaire au cout
   * - ``gpt-5``
     - Eleve
     - Maximale
     - Raisonnement complexe, haute qualite requise
   * - ``gpt-4o``
     - Moyen-Eleve
     - Maximale
     - Lorsque la prise en charge multimodale est requise
   * - ``o3-mini`` / ``o4-mini``
     - Moyen
     - Maximale
     - Taches de raisonnement comme les mathematiques et la programmation

Estimation des couts
------------

L'API OpenAI est facturee a l'usage.

.. note::
   Pour les derniers prix, consultez `OpenAI Pricing <https://openai.com/pricing>`__.

Controle des requetes simultanees
==================

Dans |Fess|, le nombre de requetes simultanees vers l'API OpenAI peut etre controle via ``rag.llm.openai.max.concurrent.requests`` dans ``fess_config.properties``. La valeur par defaut est ``5``.

::

    # Configurer le nombre maximum de requetes simultanees
    rag.llm.openai.max.concurrent.requests=5

Cette configuration permet d'eviter les requetes excessives vers l'API OpenAI et de prevenir les erreurs de limitation de debit.

Limites par niveau OpenAI
------------------

Les limites varient selon le niveau de votre compte OpenAI :

- **Free** : 3 RPM (requetes/minute)
- **Tier 1** : 500 RPM
- **Tier 2** : 5,000 RPM
- **Tier 3+** : Limites plus elevees

Ajustez ``rag.llm.openai.max.concurrent.requests`` de maniere appropriee selon le niveau de votre compte OpenAI.

Depannage
======================

Erreur d'authentification
----------

**Symptome** : Erreur "401 Unauthorized"

**Points a verifier** :

1. Verifier si la cle API est correctement configuree
2. Verifier si la cle API est valide (verifier dans le tableau de bord OpenAI)
3. Verifier si la cle API a les permissions necessaires

Erreur de limitation de debit
----------------

**Symptome** : Erreur "429 Too Many Requests"

**Solution** :

1. Reduire la valeur de ``rag.llm.openai.max.concurrent.requests``::

    rag.llm.openai.max.concurrent.requests=3

2. Mettre a niveau le niveau de votre compte OpenAI

Depassement de quota
------------

**Symptome** : Erreur "You exceeded your current quota"

**Solution** :

1. Verifier l'usage dans le tableau de bord OpenAI
2. Verifier les parametres de facturation et augmenter la limite si necessaire

Timeout
------------

**Symptome** : La requete expire

**Solution** :

1. Augmenter le temps de timeout ::

    rag.llm.openai.timeout=180000

2. Envisager un modele plus rapide (gpt-5-mini, etc.)

Configuration de debogage
------------

Pour investiguer les problemes, ajustez le niveau de log de |Fess| pour afficher des logs detailles lies a OpenAI.

``app/WEB-INF/classes/log4j2.xml`` :

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

Notes de securite
========================

Lors de l'utilisation de l'API OpenAI, faites attention aux points de securite suivants.

1. **Confidentialite des donnees** : Le contenu des resultats de recherche est envoye aux serveurs OpenAI
2. **Gestion des cles API** : La fuite de cles peut entrainer une utilisation non autorisee
3. **Conformite** : Si les donnees contiennent des informations confidentielles, verifiez les politiques de votre organisation
4. **Politique d'utilisation** : Respectez les conditions d'utilisation d'OpenAI

Informations de reference
========

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - Apercu de l'integration LLM
- :doc:`rag-chat` - Details de la fonctionnalite de mode de recherche IA
