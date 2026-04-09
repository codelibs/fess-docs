============================================================
Partie 19 : Construction d'un assistant IA interne -- Un systeme de questions-reponses base sur la recherche avec RAG
============================================================

Introduction
============

Dans l'article precedent, nous avons organise les concepts de la recherche semantique.
Dans cet article, en tant qu'evolution de cette approche, nous construisons un assistant IA interne en utilisant RAG (Retrieval-Augmented Generation).

RAG est un mecanisme qui « trouve des documents pertinents via la recherche, puis un LLM (grand modele de langage) genere des reponses basees sur leur contenu ».
Comme les reponses sont generees a partir de documents internes, RAG peut repondre a des questions specifiques a l'entreprise auxquelles une IA de chat generique ne peut pas repondre.

Public cible
============

- Les personnes interessees par la construction d'un assistant IA interne
- Les personnes souhaitant apprendre comment implementer RAG
- Les personnes souhaitant comprendre les options d'integration LLM

Fonctionnement de RAG
======================

Pipeline RAG
-------------

Le mode de recherche IA de Fess fonctionne via le pipeline suivant :

1. **Analyse d'intention (Intent)** : Analyse la question de l'utilisateur et classifie l'intention (recherche, resume, FAQ, ambigue)
2. **Recherche (Search)** : Recupere les documents pertinents depuis l'index de Fess (regenere automatiquement les requetes et relance la recherche en cas de zero resultat)
3. **Evaluation (Evaluate)** : Le LLM evalue la pertinence des documents recuperes
4. **Recuperation du texte integral (Fetch)** : Recupere le texte complet des documents hautement pertinents
5. **Generation de reponse (Answer)** : Le LLM genere une reponse en streaming avec citations basees sur le contenu du document

Ce pipeline attenue les « reponses plausibles mais inexactes (hallucinations) » du LLM et fournit des reponses etayees par des documents internes.

Le mode de recherche IA de Fess ne necessite pas de recherche vectorielle (modeles d'embeddings).
Il exploite les index de recherche en texte integral existants tels quels, le LLM se chargeant de l'evaluation des resultats de recherche et de la generation des reponses.
Cela signifie que vous pouvez introduire la recherche IA basee sur RAG immediatement, sans preparation d'infrastructure supplementaire telle que la selection de modeles d'embeddings ou la construction de bases de donnees vectorielles.

Choix d'un fournisseur LLM
============================

Fess prend en charge trois backends LLM.
Voici un resume des caracteristiques et des criteres de selection de chaque fournisseur.

.. list-table:: Comparaison des fournisseurs LLM
   :header-rows: 1
   :widths: 15 25 25 35

   * - Fournisseur
     - Plugin
     - Cout
     - Caracteristiques
   * - OpenAI
     - fess-llm-openai
     - Facturation a l'usage de l'API
     - Haute qualite de reponse, support GPT-4o, facile a demarrer
   * - Google Gemini
     - fess-llm-gemini
     - Facturation a l'usage de l'API
     - Support de la reflexion etendue, contexte long
   * - Ollama
     - fess-llm-ollama
     - Couts materiels
     - Execution locale, les donnees restent internes, axe sur la confidentialite

Criteres de selection
---------------------

**Quand choisir une API cloud (OpenAI / Gemini)**

- Vous souhaitez minimiser les couts initiaux
- Vous ne pouvez pas preparer un serveur GPU
- Vous privilegiez la qualite des reponses avant tout
- L'envoi de donnees vers des services externes est acceptable

**Quand choisir l'execution locale (Ollama)**

- L'envoi de donnees internes vers des services externes n'est pas autorise
- Les exigences de securite et de confidentialite sont strictes
- Vous pouvez preparer un serveur GPU
- Vous souhaitez reduire les couts operationnels (pour une utilisation a haut volume)

Configuration du mode de recherche IA
========================================

Installation du plugin
-----------------------

Installez le plugin correspondant au fournisseur LLM choisi.

1. Accedez a [Systeme] > [Plugins] dans la console d'administration
2. Installez le plugin correspondant (par exemple, ``fess-llm-openai``)

Activation du mode de recherche IA
------------------------------------

Activez le mode de recherche IA dans les parametres de Fess.

Definissez ``rag.chat.enabled=true`` dans les parametres de la console d'administration ou dans le fichier de configuration.

Configuration de la connexion LLM
-----------------------------------

Configurez les informations de connexion pour votre fournisseur LLM choisi.

**Pour OpenAI**

- Cle API
- Modele a utiliser (gpt-4o, gpt-4o-mini, etc.)
- Nombre maximal de tokens

**Pour Ollama**

- URL du serveur Ollama
- Nom du modele a utiliser
- Ajout d'un service via Docker Compose

.. code-block:: yaml

    services:
      ollama:
        image: ollama/ollama
        volumes:
          - ollama-data:/root/.ollama
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

L'experience du chat IA
=========================

Interface de chat
------------------

Lorsque le mode de recherche IA est active, le mode de recherche IA est ajoute a l'ecran de recherche de Fess.
Les utilisateurs peuvent basculer entre la recherche par mots-cles et le chat IA.

Exemple de question et reponse
-------------------------------

**Question** : « Comment puis-je demander un conge paye ? »

**Reponse de l'IA** :

    Pour demander un conge paye, suivez ces etapes :

    1. Accedez a la page « Gestion des presences » sur le portail interne
    2. Selectionnez « Conge paye » dans le menu « Demande d'absence »
    3. Saisissez les dates, selectionnez votre superieur et soumettez la demande

    Veuillez soumettre votre demande au moins 3 jours ouvrables avant la date du conge.

    Reference : [Reglement interieur, Article 15](https://portal/rules/chapter15.html)

La reponse inclut des liens vers les sources, permettant aux utilisateurs de verifier les documents originaux.

Utilisation de la Chat API (SSE)
==================================

Pour utiliser le mode de recherche IA depuis un programme, utilisez la Chat API.
La Chat API renvoie des reponses en streaming via Server-Sent Events (SSE).

Pour les reponses en streaming (SSE) :

::

    GET /api/v1/chat/stream?message=Comment demander un conge paye

Pour les reponses JSON sans streaming :

::

    POST /api/v1/chat
    Content-Type: application/x-www-form-urlencoded

    message=Comment demander un conge paye

Avec SSE, les reponses sont envoyees au client en temps reel au fur et a mesure de leur generation.
Les utilisateurs peuvent commencer a lire la reponse affichee progressivement sans attendre que la reponse complete soit generee.

Historique de conversation
---------------------------

La Chat API prend en charge l'historique de conversation base sur les sessions.
Les questions de suivi basees sur le contexte des questions precedentes sont possibles.

Exemple :

- Q1 : « Comment puis-je demander un conge paye ? »
- R1 : (Reponse comme ci-dessus)
- Q2 : « Que dois-je faire si j'ai depasse le delai de demande ? »
- R2 : (Reponse basee sur le contexte de Q1)

Reglage de RAG
================

Amelioration de la qualite des reponses
-----------------------------------------

La qualite des reponses de RAG est influencee par les facteurs suivants :

**Qualite de la recherche**

Comme RAG genere des reponses basees sur les resultats de recherche, la qualite de la recherche affecte directement la qualite des reponses.
L'amelioration de la qualite de la recherche grace au cycle de reglage decrit dans la Partie 8 conduit egalement a une amelioration de la qualite de RAG.

**Qualite des documents**

Si les documents recherches sont obsoletes, inexacts ou ambigus, la qualite des reponses de RAG diminuera egalement.
Les mises a jour regulieres et la gestion de la qualite des documents sont importantes.

**Configuration des prompts**

Le reglage des prompts (textes d'instructions) envoyes au LLM vous permet d'ajuster le style et la precision des reponses.

Considerations de securite
============================

Contre-mesures contre l'injection de prompts
----------------------------------------------

La fonctionnalite RAG de Fess dispose de defenses integrees contre l'injection de prompts.
Elle protege contre les attaques qui tentent de manipuler le comportement du LLM par des entrees malveillantes.

Prevention des fuites d'informations
--------------------------------------

Comme RAG genere des reponses basees sur les resultats de recherche, sa combinaison avec la recherche basee sur les roles (Partie 5) garantit que seules des reponses appropriees aux autorisations de l'utilisateur sont generees.
Le contenu des documents auxquels l'utilisateur n'a pas acces autorise n'est pas inclus dans les reponses de RAG.

Resume
======

Dans cet article, nous avons explique comment construire un assistant IA interne en utilisant le mode de recherche IA de Fess.

- Fonctionnement du pipeline RAG (analyse d'intention -> recherche -> evaluation -> generation de reponse)
- Criteres de selection pour trois fournisseurs LLM (OpenAI, Gemini, Ollama)
- Configuration et experience du mode de recherche IA
- Utilisation de la Chat API (SSE) depuis des programmes
- Reglage de la qualite des reponses et considerations de securite

Avec un assistant IA base sur des documents internes, l'utilisation des connaissances passe de « chercher » a « demander ».

Dans le prochain article, nous aborderons comment integrer Fess en tant que serveur MCP dans des agents IA.

References
==========

- `Fess AI Search Mode Settings <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Fess Chat API <https://fess.codelibs.org/ja/15.5/api/api-chat.html>`__
