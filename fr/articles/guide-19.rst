==================================================
Partie 19 : Construction d'un assistant IA interne
==================================================

Introduction
============

Dans l'article précédent, nous avons organisé les concepts de la recherche sémantique.
Dans cet article, en tant qu'évolution de cette approche, nous construisons un assistant IA interne en utilisant RAG (Retrieval-Augmented Generation).

RAG est un mécanisme qui « trouve des documents pertinents via la recherche, puis un LLM (grand modèle de langage) génère des réponses basées sur leur contenu ».
Comme les réponses sont générées à partir de documents internes, RAG peut répondre à des questions spécifiques à l'entreprise auxquelles une IA de chat générique ne peut pas répondre.

Public cible
============

- Les personnes intéressées par la construction d'un assistant IA interne
- Les personnes souhaitant apprendre comment implémenter RAG
- Les personnes souhaitant comprendre les options d'intégration LLM

Fonctionnement de RAG
======================

Pipeline RAG
-------------

Le mode de recherche IA de Fess fonctionne via le pipeline suivant :

1. **Analyse d'intention (Intent)** : Analyse la question de l'utilisateur et classifie l'intention (recherche, résumé, FAQ, ambiguë)
2. **Recherche (Search)** : Récupère les documents pertinents depuis l'index de Fess (régénère automatiquement les requêtes et relance la recherche en cas de zéro résultat)
3. **Évaluation (Evaluate)** : Le LLM évalue la pertinence des documents récupérés
4. **Récupération du texte intégral (Fetch)** : Récupère le texte complet des documents hautement pertinents
5. **Génération de réponse (Answer)** : Le LLM génère une réponse en streaming avec citations basées sur le contenu du document

Ce pipeline atténue les « réponses plausibles mais inexactes (hallucinations) » du LLM et fournit des réponses étayées par des documents internes.

Le mode de recherche IA de Fess ne nécessite pas de recherche vectorielle (modèles d'embeddings).
Il exploite les index de recherche en texte intégral existants tels quels, le LLM se chargeant de l'évaluation des résultats de recherche et de la génération des réponses.
Cela signifie que vous pouvez introduire la recherche IA basée sur RAG immédiatement, sans préparation d'infrastructure supplémentaire telle que la sélection de modèles d'embeddings ou la construction de bases de données vectorielles.

Choix d'un fournisseur LLM
============================

Fess prend en charge trois backends LLM.
Voici un résumé des caractéristiques et des critères de sélection de chaque fournisseur.

.. list-table:: Comparaison des fournisseurs LLM
   :header-rows: 1
   :widths: 15 25 25 35

   * - Fournisseur
     - Plugin
     - Coût
     - Caractéristiques
   * - OpenAI
     - fess-llm-openai
     - Facturation à l'usage de l'API
     - Haute qualité de réponse, support GPT-4o, facile à démarrer
   * - Google Gemini
     - fess-llm-gemini
     - Facturation à l'usage de l'API
     - Support de la réflexion étendue, contexte long
   * - Ollama
     - fess-llm-ollama
     - Coûts matériels
     - Exécution locale, les données restent internes, axé sur la confidentialité

Critères de sélection
---------------------

**Quand choisir une API cloud (OpenAI / Gemini)**

- Vous souhaitez minimiser les coûts initiaux
- Vous ne pouvez pas préparer un serveur GPU
- Vous privilégiez la qualité des réponses avant tout
- L'envoi de données vers des services externes est acceptable

**Quand choisir l'exécution locale (Ollama)**

- L'envoi de données internes vers des services externes n'est pas autorisé
- Les exigences de sécurité et de confidentialité sont strictes
- Vous pouvez préparer un serveur GPU
- Vous souhaitez réduire les coûts opérationnels (pour une utilisation à haut volume)

Configuration du mode de recherche IA
========================================

Installation du plugin
-----------------------

Installez le plugin correspondant au fournisseur LLM choisi.

1. Accédez à [Système] > [Plugins] dans la console d'administration
2. Installez le plugin correspondant (par exemple, ``fess-llm-openai``)

Activation du mode de recherche IA
------------------------------------

Activez le mode de recherche IA dans les paramètres de Fess.

Définissez ``rag.chat.enabled=true`` dans les paramètres de la console d'administration ou dans le fichier de configuration.

Configuration de la connexion LLM
-----------------------------------

Configurez les informations de connexion pour votre fournisseur LLM choisi.

**Pour OpenAI**

- Clé API
- Modèle à utiliser (gpt-4o, gpt-4o-mini, etc.)
- Nombre maximal de tokens

**Pour Ollama**

- URL du serveur Ollama
- Nom du modèle à utiliser
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

L'expérience du chat IA
=========================

Interface de chat
------------------

Lorsque le mode de recherche IA est activé, le mode de recherche IA est ajouté à l'écran de recherche de Fess.
Les utilisateurs peuvent basculer entre la recherche par mots-clés et le chat IA.

Exemple de question et réponse
-------------------------------

**Question** : « Comment puis-je demander un congé payé ? »

**Réponse de l'IA** :

    Pour demander un congé payé, suivez ces étapes :

    1. Accédez à la page « Gestion des présences » sur le portail interne
    2. Sélectionnez « Congé payé » dans le menu « Demande d'absence »
    3. Saisissez les dates, sélectionnez votre supérieur et soumettez la demande

    Veuillez soumettre votre demande au moins 3 jours ouvrables avant la date du congé.

    Référence : [Règlement intérieur, Article 15](https://portal/rules/chapter15.html)

La réponse inclut des liens vers les sources, permettant aux utilisateurs de vérifier les documents originaux.

Utilisation de la Chat API (SSE)
==================================

Pour utiliser le mode de recherche IA depuis un programme, utilisez la Chat API.
La Chat API renvoie des réponses en streaming via Server-Sent Events (SSE).

Pour les réponses en streaming (SSE) :

::

    GET /api/v1/chat/stream?message=Comment demander un conge paye

Pour les réponses JSON sans streaming :

::

    POST /api/v1/chat
    Content-Type: application/x-www-form-urlencoded

    message=Comment demander un conge paye

Avec SSE, les réponses sont envoyées au client en temps réel au fur et à mesure de leur génération.
Les utilisateurs peuvent commencer à lire la réponse affichée progressivement sans attendre que la réponse complète soit générée.

Historique de conversation
---------------------------

La Chat API prend en charge l'historique de conversation basé sur les sessions.
Les questions de suivi basées sur le contexte des questions précédentes sont possibles.

Exemple :

- Q1 : « Comment puis-je demander un congé payé ? »
- R1 : (Réponse comme ci-dessus)
- Q2 : « Que dois-je faire si j'ai dépassé le délai de demande ? »
- R2 : (Réponse basée sur le contexte de Q1)

Réglage de RAG
================

Amélioration de la qualité des réponses
-----------------------------------------

La qualité des réponses de RAG est influencée par les facteurs suivants :

**Qualité de la recherche**

Comme RAG génère des réponses basées sur les résultats de recherche, la qualité de la recherche affecte directement la qualité des réponses.
L'amélioration de la qualité de la recherche grâce au cycle de réglage décrit dans la Partie 8 conduit également à une amélioration de la qualité de RAG.

**Qualité des documents**

Si les documents recherchés sont obsolètes, inexacts ou ambigus, la qualité des réponses de RAG diminuera également.
Les mises à jour régulières et la gestion de la qualité des documents sont importantes.

**Configuration des prompts**

Le réglage des prompts (textes d'instructions) envoyés au LLM vous permet d'ajuster le style et la précision des réponses.

Considérations de sécurité
============================

Contre-mesures contre l'injection de prompts
----------------------------------------------

La fonctionnalité RAG de Fess dispose de défenses intégrées contre l'injection de prompts.
Elle protège contre les attaques qui tentent de manipuler le comportement du LLM par des entrées malveillantes.

Prévention des fuites d'informations
--------------------------------------

Comme RAG génère des réponses basées sur les résultats de recherche, sa combinaison avec la recherche basée sur les rôles (Partie 5) garantit que seules des réponses appropriées aux autorisations de l'utilisateur sont générées.
Le contenu des documents auxquels l'utilisateur n'a pas accès autorisé n'est pas inclus dans les réponses de RAG.

Résumé
======

Dans cet article, nous avons expliqué comment construire un assistant IA interne en utilisant le mode de recherche IA de Fess.

- Fonctionnement du pipeline RAG (analyse d'intention -> recherche -> évaluation -> génération de réponse)
- Critères de sélection pour trois fournisseurs LLM (OpenAI, Gemini, Ollama)
- Configuration et expérience du mode de recherche IA
- Utilisation de la Chat API (SSE) depuis des programmes
- Réglage de la qualité des réponses et considérations de sécurité

Avec un assistant IA basé sur des documents internes, l'utilisation des connaissances passe de « chercher » à « demander ».

Dans le prochain article, nous aborderons comment intégrer Fess en tant que serveur MCP dans des agents IA.

Références
==========

- `Fess AI Search Mode Settings <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Fess Chat API <https://fess.codelibs.org/ja/15.5/api/api-chat.html>`__
