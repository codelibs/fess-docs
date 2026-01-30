==========================
Configuration OpenAI
==========================

Apercu
====

OpenAI est un service cloud fournissant des grands modeles de langage (LLM) haute performance,
dont GPT-4. |Fess| peut utiliser l'API OpenAI pour realiser la fonctionnalite de chat RAG.

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

- ``gpt-4o`` - Dernier modele haute performance
- ``gpt-4o-mini`` - Version allegee de GPT-4o (bon rapport cout-efficacite)
- ``gpt-4-turbo`` - Version rapide de GPT-4
- ``gpt-3.5-turbo`` - Modele avec excellent rapport cout-performance

.. note::
   Pour les derniers modeles disponibles, consultez `OpenAI Models <https://platform.openai.com/docs/models>`__.

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

Configuration de base
========

Ajoutez les parametres suivants dans ``app/WEB-INF/conf/system.properties``.

Configuration minimale
--------

::

    # Activer la fonctionnalite de chat RAG
    rag.chat.enabled=true

    # Definir le fournisseur LLM sur OpenAI
    rag.llm.type=openai

    # Cle API OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modele a utiliser
    rag.llm.openai.model=gpt-4o-mini

Configuration recommandee (environnement de production)
--------------------

::

    # Activer la fonctionnalite de chat RAG
    rag.chat.enabled=true

    # Configuration du fournisseur LLM
    rag.llm.type=openai

    # Cle API OpenAI
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Configuration du modele (utiliser un modele haute performance)
    rag.llm.openai.model=gpt-4o

    # Point de terminaison API (generalement pas besoin de modifier)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Configuration du timeout
    rag.llm.openai.timeout=60000

Elements de configuration
========

Tous les elements de configuration disponibles pour le client OpenAI.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rag.llm.openai.api.key``
     - Cle API OpenAI
     - (Requis)
   * - ``rag.llm.openai.model``
     - Nom du modele a utiliser
     - ``gpt-5-mini``
   * - ``rag.llm.openai.api.url``
     - URL de base de l'API
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - Timeout de la requete (millisecondes)
     - ``60000``

Configuration via variables d'environnement
================

Pour des raisons de securite, il est recommande de configurer la cle API via des variables d'environnement.

Environnement Docker
----------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-4o-mini

Environnement systemd
-----------

``/etc/systemd/system/fess.service.d/override.conf`` :

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

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
   * - ``gpt-3.5-turbo``
     - Bas
     - Bonne
     - Questions-reponses generales, priorite au cout
   * - ``gpt-4o-mini``
     - Moyen
     - Elevee
     - Usage equilibre (recommande)
   * - ``gpt-4o``
     - Eleve
     - Maximale
     - Raisonnement complexe, haute qualite requise
   * - ``gpt-4-turbo``
     - Eleve
     - Maximale
     - Reponse rapide requise

Estimation des couts
------------

L'API OpenAI est facturee a l'usage. Voici les prix de reference pour 2024.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modele
     - Entree (1K tokens)
     - Sortie (1K tokens)
   * - gpt-3.5-turbo
     - $0.0005
     - $0.0015
   * - gpt-4o-mini
     - $0.00015
     - $0.0006
   * - gpt-4o
     - $0.005
     - $0.015

.. note::
   Pour les derniers prix, consultez `OpenAI Pricing <https://openai.com/pricing>`__.

Limitation de debit
==========

L'API OpenAI a des limites de debit. Configurez-les de maniere appropriee en combinaison avec la fonction de limitation de debit de |Fess|.

::

    # Configuration de limitation de debit Fess
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Limites par niveau OpenAI
------------------

Les limites varient selon le niveau de votre compte OpenAI :

- **Free** : 3 RPM (requetes/minute)
- **Tier 1** : 500 RPM
- **Tier 2** : 5,000 RPM
- **Tier 3+** : Limites plus elevees

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

1. Configurer une limitation de debit plus stricte dans |Fess| ::

    rag.chat.rate.limit.requests.per.minute=5

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

    rag.llm.openai.timeout=120000

2. Envisager un modele plus rapide (gpt-3.5-turbo, etc.)

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
- :doc:`rag-chat` - Details de la fonctionnalite de chat RAG
