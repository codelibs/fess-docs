============================================================
Partie 20 : Connecter les agents IA a la recherche -- Integrer Fess dans des outils IA externes via le serveur MCP
============================================================

Introduction
============

Dans l'article precedent, nous avons construit un assistant IA en utilisant le mode de recherche IA integre de Fess.
Cependant, ce n'est pas la seule facon d'exploiter l'IA.
Il existe une methode pour utiliser Fess comme « outil de recherche » depuis Claude Desktop et d'autres agents IA.

Dans cet article, nous allons configurer Fess en tant que serveur MCP (Model Context Protocol) et mettre en place un environnement permettant aux outils IA externes de rechercher de maniere transparente dans les documents internes.

Public cible
============

- Les personnes interessees par l'integration des agents IA avec les systemes de recherche
- Les personnes souhaitant comprendre le concept de MCP
- Les personnes utilisant des outils IA tels que Claude Desktop dans leurs activites professionnelles

Qu'est-ce que MCP ?
====================

MCP (Model Context Protocol) est un protocole permettant aux applications IA d'acceder a des sources de donnees et des outils externes.
Il permet aux modeles IA d'effectuer des operations telles que « rechercher », « lire un fichier » et « appeler une API » de maniere standardisee.

En exposant Fess en tant que serveur MCP, les agents IA peuvent executer des operations comme « rechercher dans les documents internes » dans un contexte naturel.

Un changement de paradigme
---------------------------

La recherche traditionnelle suivait le modele « un humain saisit des mots-cles et lit les resultats ».
Avec MCP, un nouveau modele se concretise : « un agent IA recherche de maniere autonome, interprete les resultats et les integre dans ses reponses ».

Il s'agit d'un passage de « les humains recherchent » a « l'IA recherche a la place des humains ».

Construction du serveur MCP de Fess
=====================================

Installation du plugin
------------------------

La fonctionnalite de serveur MCP de Fess est fournie sous forme de plugin webapp.

1. Dans le panneau d'administration, allez dans [Systeme] > [Plugins]
2. Installez ``fess-webapp-mcp``
3. Redemarrez Fess

Fonctionnalites fournies par le serveur MCP
---------------------------------------------

Le serveur MCP de Fess fournit les fonctionnalites suivantes aux agents IA.

**Tools**

- **search** : Recherche en texte integral dans les documents internes
- **get_index_stats** : Recuperation du nombre de documents de l'index et des informations memoire JVM

Les agents IA peuvent appeler ces outils pour rechercher dans l'index de Fess ou verifier l'etat du systeme.

**Resources**

- **fess://index/stats** : Statistiques de l'index (nombre de documents, informations de configuration, memoire JVM)

**Prompts**

- **basic_search** : Generation de requetes de recherche de base
- **advanced_search** : Generation de requetes de recherche detaillees incluant l'ordre de tri et le nombre de resultats

Integration avec Claude Desktop
=================================

Configuration de Claude Desktop
---------------------------------

Pour connecter le serveur MCP de Fess a Claude Desktop, ajoutez les informations du serveur MCP au fichier de configuration de Claude Desktop.

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

Une fois que Fess est connecte en tant que serveur MCP dans Claude Desktop, des interactions comme les suivantes deviennent possibles.

**Exemple 1 : Recherche dans les documents internes**

    Utilisateur : « Veuillez m'informer sur la procedure de remboursement des frais de deplacement professionnel. »

    Claude : (Appelle l'outil de recherche de Fess)
    J'ai recherche dans les documents internes concernant le remboursement des frais de deplacement.
    La procedure de remboursement est la suivante :
    1. Rediger un rapport de deplacement...
    [Tire du Manuel de remboursement des frais de deplacement (portal/manual/travel-expense.html)]

**Exemple 2 : Recherche transversale dans plusieurs documents**

    Utilisateur : « Veuillez resumer les dispositions relatives aux mots de passe dans notre politique de securite. »

    Claude : (Recherche dans Fess « mot de passe politique de securite » et integre plusieurs resultats)
    Les dispositions relatives aux mots de passe sont documentees dans les documents suivants :
    - Politique de base de securite de l'information : Les mots de passe doivent comporter au moins 12 caracteres...
    - Reglement de gestion des comptes : Un changement tous les 90 jours est requis...
    - Reglement d'acces a distance : L'authentification multifacteur est obligatoire...

Les agents IA interpretent les resultats de recherche et generent des reponses integrant les informations provenant de plusieurs documents.

Integration avec d'autres outils IA
=====================================

MCP etant un protocole standard, Fess peut etre utilise depuis des outils IA compatibles MCP autres que Claude Desktop.

Utilisation depuis des agents IA personnalises
------------------------------------------------

Il est egalement possible de se connecter a Fess via le protocole MCP depuis des agents IA developpes en interne.
Vous pouvez appeler les fonctionnalites de recherche de Fess de maniere programmatique a l'aide de bibliotheques clientes MCP.

Considerations de securite
============================

Voici les points de securite a prendre en compte lors de l'exposition du serveur MCP.

Controle d'acces
-----------------

- Restreindre l'acces au serveur MCP aux seuls clients de confiance
- Restrictions au niveau du reseau (pare-feu, VPN)
- Authentification par jetons d'API

Controle des permissions sur les resultats de recherche
--------------------------------------------------------

La recherche basee sur les roles de Fess (traitee dans la Partie 5) s'applique egalement aux recherches via MCP.
En associant des roles aux jetons d'API, vous pouvez controler l'etendue des documents auxquels les agents IA peuvent acceder.

Gestion des donnees
--------------------

Lors de l'integration avec des services IA bases sur le cloud, sachez que le texte des resultats de recherche est envoye a l'exterieur.
Si des documents hautement confidentiels sont inclus, envisagez la combinaison avec un LLM local (Ollama) ou le filtrage des resultats de recherche.

Resume
======

Dans cet article, nous avons explique comment exposer Fess en tant que serveur MCP et l'integrer avec des agents IA.

- Le concept du protocole MCP et le paradigme « l'IA recherche »
- Installation et configuration du plugin fess-webapp-mcp
- Exemples d'integration avec Claude Desktop
- Considerations de securite (controle d'acces, permissions, gestion des donnees)

En permettant aux agents IA d'acceder directement aux connaissances internes, les possibilites d'exploitation des connaissances s'elargissent considerablement.

Dans le prochain article, nous aborderons la recherche multimodale.

References
==========

- `Fess MCP Server <https://github.com/codelibs/fess-webapp-mcp>`__

- `Model Context Protocol <https://modelcontextprotocol.io/>`__
