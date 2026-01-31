==========================
Configuration Google Gemini
==========================

Apercu
====

Google Gemini est un grand modele de langage (LLM) de pointe fourni par Google.
|Fess| peut utiliser l'API Google AI (Generative Language API) pour realiser la fonctionnalite de chat RAG avec les modeles Gemini.

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

- ``gemini-2.5-flash`` - Modele rapide et efficace (recommande)
- ``gemini-2.5-pro`` - Modele avec capacites de raisonnement superieures
- ``gemini-1.5-flash`` - Version stable du modele Flash
- ``gemini-1.5-pro`` - Version stable du modele Pro

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

Configuration de base
========

Ajoutez les parametres suivants dans ``app/WEB-INF/conf/system.properties``.

Configuration minimale
--------

::

    # Activer la fonctionnalite de chat RAG
    rag.chat.enabled=true

    # Definir le fournisseur LLM sur Gemini
    rag.llm.type=gemini

    # Cle API Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modele a utiliser
    rag.llm.gemini.model=gemini-2.5-flash

Configuration recommandee (environnement de production)
--------------------

::

    # Activer la fonctionnalite de chat RAG
    rag.chat.enabled=true

    # Configuration du fournisseur LLM
    rag.llm.type=gemini

    # Cle API Gemini
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuration du modele (utiliser le modele rapide)
    rag.llm.gemini.model=gemini-2.5-flash

    # Point de terminaison API (generalement pas besoin de modifier)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Configuration du timeout
    rag.llm.gemini.timeout=60000

Elements de configuration
========

Tous les elements de configuration disponibles pour le client Gemini.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.gemini.api.key``
     - Cle API Google AI
     - (Requis)
   * - ``rag.llm.gemini.model``
     - Nom du modele a utiliser
     - ``gemini-2.5-flash``
   * - ``rag.llm.gemini.api.url``
     - URL de base de l'API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Timeout de la requete (millisecondes)
     - ``60000``

Configuration via variables d'environnement
================

Pour des raisons de securite, il est recommande de configurer la cle API via des variables d'environnement.

Environnement Docker
----------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-2.5-flash

Environnement systemd
-----------

``/etc/systemd/system/fess.service.d/override.conf`` :

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

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
   * - ``gemini-2.5-flash``
     - Rapide
     - Elevee
     - Usage general, equilibre (recommande)
   * - ``gemini-2.5-pro``
     - Moyenne
     - Maximale
     - Raisonnement complexe, haute qualite requise
   * - ``gemini-1.5-flash``
     - Rapide
     - Bonne
     - Priorite au cout, stabilite
   * - ``gemini-1.5-pro``
     - Moyenne
     - Elevee
     - Long contexte requis

Fenetre de contexte
----------------------

Les modeles Gemini prennent en charge des fenetres de contexte tres longues :

- **Gemini 1.5/2.5 Flash** : Maximum 1 million de tokens
- **Gemini 1.5/2.5 Pro** : Maximum 2 millions de tokens

Cette caracteristique permet d'inclure davantage de resultats de recherche dans le contexte.

::

    # Inclure plus de documents dans le contexte
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

Estimation des couts
------------

L'API Google AI est facturee a l'usage (avec une offre gratuite).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modele
     - Entree (1M caracteres)
     - Sortie (1M caracteres)
   * - Gemini 1.5 Flash
     - $0.075
     - $0.30
   * - Gemini 1.5 Pro
     - $1.25
     - $5.00
   * - Gemini 2.5 Flash
     - Les prix peuvent varier
     - Les prix peuvent varier

.. note::
   Pour les derniers prix et informations sur l'offre gratuite, consultez `Google AI Pricing <https://ai.google.dev/pricing>`__.

Limitation de debit
==========

L'API Google AI a des limites de debit. Configurez-les de maniere appropriee en combinaison avec la fonction de limitation de debit de |Fess|.

::

    # Configuration de limitation de debit Fess
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Limites de l'offre gratuite
------------

L'API Google AI a une offre gratuite avec les limites suivantes :

- Requetes/minute : 15 RPM
- Tokens/minute : 1 million TPM
- Requetes/jour : 1,500 RPD

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

1. Configurer une limitation de debit plus stricte dans |Fess| ::

    rag.chat.rate.limit.requests.per.minute=5

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
- :doc:`rag-chat` - Details de la fonctionnalite de chat RAG
