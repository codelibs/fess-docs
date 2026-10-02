===================================================
Configuration d'Amazon Bedrock (Recherche IA / RAG)
===================================================

Aperçu
======

Cette page explique comment configurer le plugin ``fess-llm-bedrock`` afin que |Fess| puisse utiliser Amazon Bedrock pour son **mode de recherche IA (RAG : Retrieval-Augmented Generation)** et comme fournisseur d'embedding pour les chunks de contenu.

Amazon Bedrock est le service AWS qui fournit, via une API unique, des modèles de fondation d'Amazon et d'autres fournisseurs de modèles.
Le plugin appelle l'API Bedrock Runtime dans la région AWS de votre choix :

- **Mode de recherche IA** : l'API Converse (``ConverseStream`` pour les réponses en streaming)
- **Embedding des chunks de contenu** : l'API InvokeModel avec Amazon Titan Text Embeddings V2 ou Cohere Embed

Modèles pris en charge
----------------------

Le mode de recherche IA fonctionne avec tout modèle prenant en charge l'API Converse dans votre région.
Le modèle par défaut est Amazon Nova 2 Lite via le profil d'inférence inter-régions des États-Unis, ``us.amazon.nova-2-lite-v1:0``.
``rag.llm.bedrock.model`` accepte un ID de modèle, un ID de profil d'inférence (par exemple avec le préfixe ``us.``, ``eu.`` ou ``global.``) ou un ARN.

L'embedding des chunks de contenu prend en charge les modèles suivants.

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - Modèle
     - ``content_chunker.embedding.dimension``
     - Textes par requête
   * - ``amazon.titan-embed-text-v2:0``
     - ``256``, ``512`` ou ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - jusqu'à 96, chacun de 2048 caractères au maximum
   * - ``cohere.embed-v4:0`` (également via un profil d'inférence)
     - ``256``, ``512``, ``1024`` ou ``1536``
     - jusqu'à 96

Le modèle d'embedding est reconnu par le nom du modèle de base contenu dans l'ID configuré : un ID de modèle de base, un ID de profil d'inférence inter-régions (``us.``, ``eu.``, ``global.`` ...) ou un ARN contenant l'un de ceux-ci.
Les profils d'inférence d'application ont des ID opaques et ne sont pas reconnus.

.. note::
   Pour les modèles disponibles dans chaque région, consultez `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__.

Prérequis
=========

1. **Compte AWS** avec Amazon Bedrock disponible dans la région que vous utilisez
2. **Accès aux modèles** : les modèles que vous configurez doivent être utilisables depuis votre compte dans cette région
3. **Identifiants** : soit une clé API Bedrock, soit des identifiants AWS autorisés à appeler les modèles (voir :ref:`bedrock-authentication`)

Installation du plugin
======================

L'intégration de Bedrock est fournie sous forme de plugin ``fess-llm-bedrock``.
Installez-le depuis « Système » > « Plugins » dans l'écran d'administration, ou placez manuellement le fichier JAR puis redémarrez |Fess|.

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   La version du plugin doit correspondre à la version de |Fess|.

Configuration de base
=====================

Le fournisseur LLM (``rag.llm.name``) se sélectionne depuis l'écran d'administration (Administration > Système > General) ou dans ``system.properties``.
L'activation du mode de recherche IA et les paramètres ``rag.llm.bedrock.*`` se définissent dans ``fess_config.properties``.

``system.properties`` (configurable également via Administration > Système > General) :

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` pour les installations par paquet), avec des identifiants AWS :

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

Avec une clé API Bedrock à la place des identifiants AWS :

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

Éléments de configuration
=========================

Toutes les options du client du mode de recherche IA. Elles se configurent dans ``fess_config.properties`` (ou sous forme d'options JVM ``-Dfess.config.<key>``).

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rag.llm.bedrock.api.key``
     - Clé API Bedrock. Si elle est vide, les requêtes sont signées avec les identifiants AWS (SigV4)
     - ``""``
   * - ``rag.llm.bedrock.region``
     - Région AWS du point de terminaison Bedrock Runtime et de la signature SigV4
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - URL du point de terminaison, par exemple un point de terminaison d'interface VPC. Si elle est vide, ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - ID de modèle, ID de profil d'inférence ou ARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - Timeout de la requête (en millisecondes)
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - Intervalle de vérification de disponibilité (en secondes)
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - ``false`` empêche l'envoi de ``temperature``, pour les modèles ou modes qui la rejettent
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - Objet JSON envoyé en tant que ``additionalModelRequestFields`` pour les paramètres spécifiques au modèle
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - Nombre maximum de requêtes simultanées
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - Délai d'attente des requêtes simultanées (millisecondes)
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - Nombre maximum de caractères du contexte récupéré pour la génération de réponse
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - Nombre maximum de caractères du document pour la génération de résumé
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - Nombre maximum de caractères du contexte récupéré pour la génération de FAQ
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - Nombre maximum de documents pertinents lors de l'évaluation
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - Nombre maximum de caractères pour la description du document lors de l'évaluation
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - Nombre maximum de caractères de l'historique de chat
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - Nombre maximum de messages d'historique pour la détermination d'intention
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - Nombre maximum de caractères d'historique pour la détermination d'intention
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - Nombre maximum de caractères de l'historique de l'assistant
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - Nombre maximum de caractères du résumé de l'historique de l'assistant
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429``, ``500``, ``502``, ``503`` et ``504``)
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - Délai de base du backoff exponentiel (en millisecondes)
     - ``2000``

.. _bedrock-authentication:

Authentification
================

Clé API
-------

Lorsque ``rag.llm.bedrock.api.key`` est définie, elle est envoyée sous la forme ``Authorization: Bearer <key>``.
Les clés API Bedrock à court terme expirent et ne sont valides que dans la région où elles ont été créées ; les clés à long terme sont rattachées à un utilisateur IAM.
La valeur est masquée dans Administration > Système > Informations système lorsqu'elle est définie dans ``fess_config.properties`` (ou, pour ``content_chunker.embedding.bedrock.api.key``, dans ``system.properties``).
Les variables d'environnement et les propriétés système JVM, y compris les options ``-Dfess.config.*`` et ``-Dfess.system.*``, y sont affichées sans masquage ; ne transmettez donc pas la clé de cette manière.

Identifiants AWS (SigV4)
------------------------

Lorsqu'aucune clé API n'est définie, chaque requête est signée avec AWS Signature Version 4.
Les identifiants sont pris dans la première des sources suivantes qui en fournit :

1. les propriétés système JVM ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken``
2. les variables d'environnement ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN``
3. l'identité web (``AWS_WEB_IDENTITY_TOKEN_FILE`` et ``AWS_ROLE_ARN``, comme sur Amazon EKS)
4. les fichiers partagés ``~/.aws/credentials`` et ``~/.aws/config`` (``AWS_PROFILE`` sélectionne le profil)
5. le point de terminaison d'identifiants de conteneur (Amazon ECS)
6. le service de métadonnées d'instance EC2 (profil d'instance)

Les propriétés système JVM (source 1) n'atteignent que le processus web de |Fess|.
L'embedding des chunks de contenu (documents) s'exécute dans une JVM enfant distincte ; utilisez donc pour lui des variables d'environnement, un profil d'identifiants partagé ou un rôle IAM, ou répétez les options ``-Daws.*`` dans ``jvm.chunk.options``.

La région provient toujours de ``rag.llm.bedrock.region`` ; ``AWS_REGION`` n'est pas lue.
Les profils qui utilisent IAM Identity Center (SSO) ne sont pas pris en charge.

.. warning::
   Privilégiez un rôle IAM (profil d'instance EC2, rôle de tâche ECS, identité web EKS) ou le fichier d'identifiants partagé de l'utilisateur qui exécute |Fess|.
   Les variables d'environnement et les propriétés système JVM sont affichées sans masquage sous Administration > Système > Informations système ; n'y placez donc pas de clés de longue durée.

Le principal IAM a besoin de ``bedrock:InvokeModel`` (Converse et InvokeModel) et de ``bedrock:InvokeModelWithResponseStream`` (ConverseStream) sur les modèles qu'il utilise.
Lorsque le modèle est un profil d'inférence, autorisez à la fois le profil d'inférence et les modèles de fondation vers lesquels il route les requêtes.

Comportement de réessai
=======================

Les requêtes sont réessayées en cas de ``429``, ``500``, ``502``, ``503`` et ``504``, ainsi que lorsque la connexion à Bedrock n'a pas pu être établie.
Les réessais attendent selon un backoff exponentiel (valeur de base ``rag.llm.bedrock.retry.base.delay.ms``, gigue de +/-20%, jusqu'à ``rag.llm.bedrock.retry.max`` tentatives) ; un en-tête ``Retry-After`` est prioritaire.
Pour les requêtes en streaming, seule la requête initiale est réessayée ; une erreur survenant après le début du streaming de la réponse, y compris un événement d'exception dans le flux, met fin à la requête.

Configuration par type de prompt
================================

``temperature`` et ``max.tokens`` peuvent être définis par type de prompt, comme pour les autres fournisseurs :

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` est l'un de ``intent``, ``evaluation``, ``unclear``, ``noresults``, ``docnotfound``, ``direct``, ``faq``, ``answer``, ``summary`` et ``queryregeneration``.
Un ``additional.model.request.fields`` défini pour un type de prompt remplace la valeur globale pour ce type de prompt.

Valeurs par défaut utilisées lorsqu'aucune configuration n'est définie :

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Type de prompt
     - temperature
     - max.tokens
   * - ``intent``, ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear``, ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct``, ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   ``rag.llm.bedrock.{promptType}.thinking.budget`` n'est pas pris en charge : les paramètres de raisonnement diffèrent selon le modèle sur Bedrock.
   Une valeur configurée n'est pas envoyée et un WARN est consigné. Utilisez plutôt ``additional.model.request.fields``.

Paramètres spécifiques au modèle
================================

``additional.model.request.fields`` transmet tel quel un objet JSON au modèle.
Une valeur qui n'est pas un objet JSON n'est pas envoyée, et un WARN indiquant la propriété est consigné.

Par exemple, pour utiliser la réflexion étendue (extended thinking) d'un modèle Anthropic Claude uniquement pour la génération de réponse :

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

Claude rejette ``temperature`` lorsque la réflexion est activée, et ``max.tokens`` doit être supérieur à ``budget_tokens``.
Le texte de raisonnement n'est jamais montré aux utilisateurs ; seul le texte de la réponse l'est.

Embedding des chunks de contenu
===============================

Pour utiliser Bedrock pour l'embedding des chunks de contenu, définissez ce qui suit dans ``app/WEB-INF/conf/system.properties`` (``/etc/fess/system.properties`` pour les paquets RPM/DEB, ``/opt/fess/system.properties`` sous Docker), ou sous forme d'options ``-Dfess.system.<key>``.
Contrairement à ``rag.llm.bedrock.*``, ces clés ne sont pas lues depuis ``fess_config.properties``.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``content_chunker.embedding.bedrock.api.key``
     - Clé API Bedrock. Si elle est vide, les identifiants AWS sont utilisés
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - Région AWS
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - URL du point de terminaison. Si elle est vide, elle est déduite de la région
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - Modèle d'embedding (voir `Modèles pris en charge`_)
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - Titan uniquement : indique si les vecteurs sont normalisés
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - Cohere uniquement : ``truncate`` (``NONE``/``START``/``END`` pour v3, ``NONE``/``LEFT``/``RIGHT`` pour v4). Non envoyé s'il est vide
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - Timeout de la requête (en millisecondes)
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - Timeout de connexion (en millisecondes)
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - Intervalle de vérification de disponibilité (en secondes)
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - Nombre maximum de tentatives HTTP (lors d'erreurs ``429``, ``500``, ``502``, ``503`` et ``504``)
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - Délai de base du backoff exponentiel (en millisecondes)
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - Borne supérieure d'une attente de backoff, ``Retry-After`` inclus (en millisecondes)
     - ``60000``

``content_chunker.embedding.dimension`` doit être une taille que le modèle produit (voir `Modèles pris en charge`_) ; sinon le fournisseur d'embedding est signalé comme indisponible par un journal ERROR.
Les documents sont vectorisés avec ``input_type=search_document`` de Cohere et les requêtes avec ``search_query``.
Cohere Embed v3 accepte au plus 2048 caractères par texte. Bedrock rejette un texte plus long avec ``400 ValidationException`` quelle que soit la valeur de ``truncate``, et le plugin ne raccourcit ni ne découpe les textes.
``truncate`` (``END`` lorsqu'il n'est pas défini) ne s'applique qu'à un texte de 2048 caractères au plus qui dépasse 512 tokens.

Utilisation via un proxy HTTP
=============================

Les requêtes vers Bedrock utilisent la configuration de proxy HTTP commune à |Fess| (``http.proxy.host``, ``http.proxy.port``, ``http.proxy.username`` et ``http.proxy.password`` dans ``fess_config.properties``).
Les recherches d'identifiants qui appellent des points de terminaison AWS (STS pour l'identité web, le point de terminaison d'identifiants de conteneur, le service de métadonnées d'instance) n'utilisent pas ces paramètres.
Pour atteindre Bedrock via un point de terminaison d'interface VPC, définissez ``rag.llm.bedrock.endpoint`` (et ``content_chunker.embedding.bedrock.endpoint``) sur son URL ; le paramètre de région sélectionne toujours la région de signature.

Dépannage
=========

Le mode de recherche IA n'est pas disponible
--------------------------------------------

Le client se déclare disponible lorsque le modèle et la région sont définis, que le point de terminaison est une URL valide, et que soit une clé API est définie, soit des identifiants AWS peuvent être résolus.
Une région ou un point de terminaison invalide est consigné au niveau ERROR. Pour savoir pourquoi les identifiants n'ont pas pu être résolus, activez DEBUG pour ``org.codelibs.fess.llm.bedrock``.
Un échec de recherche d'identifiants est mémorisé pendant 60 secondes ; des identifiants rendus disponibles ultérieurement sont donc pris en compte en moins d'une minute.

Accès refusé
------------

Un ``403`` avec ``type=AccessDeniedException`` dans le journal WARN signifie que la clé API ou le principal IAM n'est pas autorisé à invoquer le modèle.
Vérifiez les autorisations IAM ci-dessus, ainsi que le fait que le modèle est utilisable depuis votre compte dans la région configurée.

Erreurs de validation
---------------------

Un ``400`` avec ``type=ValidationException`` signifie généralement que l'ID de modèle n'est pas disponible dans la région (pour certains modèles, seul un ID de profil d'inférence peut être utilisé) ou que ``additional.model.request.fields`` contient des paramètres que le modèle n'accepte pas.

Configuration de débogage
-------------------------

Activez DEBUG pour ``org.codelibs.fess.llm.bedrock`` afin de consigner les corps des requêtes et des réponses du mode de recherche IA, ainsi que la raison pour laquelle les identifiants AWS n'ont pas pu être résolus.
DEBUG pour ``org.codelibs.fess.embedding.bedrock`` consigne la façon dont le texte de la requête a été normalisé ainsi que la même raison liée aux identifiants ; il ne consigne pas les requêtes d'embedding.
Les clés API, les identifiants AWS et les signatures ne sont jamais écrits par ces loggers.

.. warning::
   Deux autres loggers écrivent des identifiants au niveau DEBUG : la journalisation « wire » d'Apache HttpClient écrit l'en-tête ``Authorization``, et le signataire du SDK AWS (``software.amazon.awssdk.http.auth.aws.internal.signer``) écrit la requête canonique, y compris le ``x-amz-security-token`` des identifiants temporaires.
   Démarrer |Fess| avec le niveau de log racine à DEBUG active les deux ; maintenez ``org.apache.hc`` et ``software.amazon.awssdk`` au niveau INFO ou supérieur.

Informations de référence
=========================

- :doc:`llm-overview` - Aperçu de l'intégration LLM
- :doc:`rag-chat` - Détails du mode de recherche IA
- :doc:`search-semantic` - Recherche sémantique et embedding des chunks de contenu
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
