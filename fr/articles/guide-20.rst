==================================================
Partie 20 : Connecter les agents IA à la recherche
==================================================

Introduction
============

Dans l'article précédent, nous avons construit un assistant IA en utilisant le mode de recherche IA intégré de Fess.
Cependant, ce n'est pas la seule façon d'exploiter l'IA.
Il existe une méthode pour utiliser Fess comme « outil de recherche » depuis Claude Desktop et d'autres agents IA.

Dans cet article, nous allons configurer Fess en tant que serveur MCP (Model Context Protocol) et mettre en place un environnement permettant aux outils IA externes de rechercher de manière transparente dans les documents internes.

Public cible
============

- Les personnes intéressées par l'intégration des agents IA avec les systèmes de recherche
- Les personnes souhaitant comprendre le concept de MCP
- Les personnes utilisant des outils IA tels que Claude Desktop dans leurs activités professionnelles

Qu'est-ce que MCP ?
====================

MCP (Model Context Protocol) est un protocole permettant aux applications IA d'accéder à des sources de données et des outils externes.
Il permet aux modèles IA d'effectuer des opérations telles que « rechercher », « lire un fichier » et « appeler une API » de manière standardisée.

En exposant Fess en tant que serveur MCP, les agents IA peuvent exécuter des opérations comme « rechercher dans les documents internes » dans un contexte naturel.

Un changement de paradigme
---------------------------

La recherche traditionnelle suivait le modèle « un humain saisit des mots-clés et lit les résultats ».
Avec MCP, un nouveau modèle se concrétise : « un agent IA recherche de manière autonome, interprète les résultats et les intègre dans ses réponses ».

Il s'agit d'un passage de « les humains recherchent » à « l'IA recherche à la place des humains ».

Construction du serveur MCP de Fess
=====================================

Installation du plugin
------------------------

La fonctionnalité de serveur MCP de Fess est fournie sous forme de plugin webapp.

1. Dans le panneau d'administration, allez dans [Système] > [Plugins]
2. Installez ``fess-webapp-mcp``
3. Redémarrez Fess

Fonctionnalités fournies par le serveur MCP
---------------------------------------------

Le serveur MCP de Fess fournit les fonctionnalités suivantes aux agents IA.

**Tools**

- **search** : Recherche en texte intégral dans les documents internes
- **get_index_stats** : Récupération du nombre de documents de l'index et des informations mémoire JVM

Les agents IA peuvent appeler ces outils pour rechercher dans l'index de Fess ou vérifier l'état du système.

**Resources**

- **fess://index/stats** : Statistiques de l'index (nombre de documents, informations de configuration, mémoire JVM)

**Prompts**

- **basic_search** : Génération de requêtes de recherche de base
- **advanced_search** : Génération de requêtes de recherche détaillées incluant l'ordre de tri et le nombre de résultats

Intégration avec Claude Desktop
=================================

Configuration de Claude Desktop
---------------------------------

Pour connecter le serveur MCP de Fess à Claude Desktop, ajoutez les informations du serveur MCP au fichier de configuration de Claude Desktop.

Ajoutez la configuration suivante au fichier de configuration (claude_desktop_config.json).

.. code-block:: json

    {
      "mcpServers": {
        "fess": {
          "url": "http://localhost:8080/mcp"
        }
      }
    }

Exemples d'utilisation
-----------------------

Une fois que Fess est connecté en tant que serveur MCP dans Claude Desktop, des interactions comme les suivantes deviennent possibles.

**Exemple 1 : Recherche dans les documents internes**

    Utilisateur : « Veuillez m'informer sur la procédure de remboursement des frais de déplacement professionnel. »

    Claude : (Appelle l'outil de recherche de Fess)
    J'ai recherché dans les documents internes concernant le remboursement des frais de déplacement.
    La procédure de remboursement est la suivante :
    1. Rédiger un rapport de déplacement...
    [Tiré du Manuel de remboursement des frais de déplacement (portal/manual/travel-expense.html)]

**Exemple 2 : Recherche transversale dans plusieurs documents**

    Utilisateur : « Veuillez résumer les dispositions relatives aux mots de passe dans notre politique de sécurité. »

    Claude : (Recherche dans Fess « mot de passe politique de sécurité » et intègre plusieurs résultats)
    Les dispositions relatives aux mots de passe sont documentées dans les documents suivants :
    - Politique de base de sécurité de l'information : Les mots de passe doivent comporter au moins 12 caractères...
    - Règlement de gestion des comptes : Un changement tous les 90 jours est requis...
    - Règlement d'accès à distance : L'authentification multifacteur est obligatoire...

Les agents IA interprètent les résultats de recherche et génèrent des réponses intégrant les informations provenant de plusieurs documents.

Intégration avec d'autres outils IA
=====================================

MCP étant un protocole standard, Fess peut être utilisé depuis des outils IA compatibles MCP autres que Claude Desktop.

Utilisation depuis des agents IA personnalisés
------------------------------------------------

Il est également possible de se connecter à Fess via le protocole MCP depuis des agents IA développés en interne.
Vous pouvez appeler les fonctionnalités de recherche de Fess de manière programmatique à l'aide de bibliothèques clientes MCP.

Considérations de sécurité
============================

Voici les points de sécurité à prendre en compte lors de l'exposition du serveur MCP.

Contrôle d'accès
-----------------

- Restreindre l'accès au serveur MCP aux seuls clients de confiance
- Restrictions au niveau du réseau (pare-feu, VPN)
- Authentification par jetons d'API

Contrôle des permissions sur les résultats de recherche
--------------------------------------------------------

La recherche basée sur les rôles de Fess (traitée dans la Partie 5) s'applique également aux recherches via MCP.
En associant des rôles aux jetons d'API, vous pouvez contrôler l'étendue des documents auxquels les agents IA peuvent accéder.

Gestion des données
--------------------

Lors de l'intégration avec des services IA basés sur le cloud, sachez que le texte des résultats de recherche est envoyé à l'extérieur.
Si des documents hautement confidentiels sont inclus, envisagez la combinaison avec un LLM local (Ollama) ou le filtrage des résultats de recherche.

Résumé
======

Dans cet article, nous avons expliqué comment exposer Fess en tant que serveur MCP et l'intégrer avec des agents IA.

- Le concept du protocole MCP et le paradigme « l'IA recherche »
- Installation et configuration du plugin fess-webapp-mcp
- Exemples d'intégration avec Claude Desktop
- Considérations de sécurité (contrôle d'accès, permissions, gestion des données)

En permettant aux agents IA d'accéder directement aux connaissances internes, les possibilités d'exploitation des connaissances s'élargissent considérablement.

Dans le prochain article, nous aborderons la recherche multimodale.

Références
==========

- `Fess MCP Server <https://github.com/codelibs/fess-webapp-mcp>`__

- `Model Context Protocol <https://modelcontextprotocol.io/>`__
