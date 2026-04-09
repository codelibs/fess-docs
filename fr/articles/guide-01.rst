============================================================
Partie 1 Pourquoi la recherche est-elle essentielle en entreprise -- Les défis de l'exploitation des connaissances à l'ère de la surcharge informationnelle
============================================================

Introduction
============

« Ce fichier, où est-ce qu'il était déjà ? »

C'est une question à laquelle de nombreux professionnels sont confrontés au quotidien.
Serveurs de fichiers internes, stockage cloud, outils de messagerie instantanée, wikis, systèmes de gestion de tickets -- les informations ne cessent de croître et sont dispersées dans une multitude d'emplacements.
Nous savons que l'information dont nous avons besoin existe quelque part, mais il faut parfois plusieurs minutes, voire des dizaines de minutes, pour la retrouver.
Ce « temps passé à chercher l'information » constitue l'un des défis majeurs auxquels les entreprises modernes sont confrontées.

Dans cette série « Stratégie d'exploitation des connaissances avec Fess », nous expliquerons de manière pratique comment résoudre ce problème à l'aide de Fess, un serveur de recherche plein texte open source.
Dans cette Partie 1, nous commencerons par clarifier « pourquoi une infrastructure de recherche est nécessaire en entreprise » et présenterons le positionnement de Fess en tant que logiciel.

Public cible
============

- Personnes confrontées à des difficultés d'exploitation de l'information en interne
- Personnes envisageant l'adoption d'une solution de recherche d'entreprise
- Personnes découvrant Fess pour la première fois

Les défis de l'ère de la surcharge informationnelle
=====================================================

L'explosion de l'information et le problème de la « non-trouvabilité »
------------------------------------------------------------------------

Les données numériques détenues par les entreprises augmentent d'année en année.
Rapports, comptes rendus de réunion, documents de conception, e-mails, journaux de messagerie, code source, données clients -- toutes ces informations constituent le savoir de l'organisation.
Cependant, plus la quantité d'informations augmente, plus il devient difficile de trouver celle dont on a besoin.

De nombreuses études indiquent que les travailleurs du savoir consacrent 20 à 30 % de leur temps de travail à la recherche d'informations.
Pour une organisation de 50 personnes, cela signifie que l'équivalent de 10 à 15 personnes-jours est consommé chaque jour par des « activités de recherche ».

Les silos d'information : un problème structurel
---------------------------------------------------

Si l'information est introuvable, ce n'est pas uniquement en raison de son volume.
Dans de nombreuses entreprises, des « silos d'information » se forment, où les données sont cloisonnées par département ou par outil.

- L'équipe commerciale utilise Salesforce et des dossiers partagés
- L'équipe de développement utilise Confluence et des dépôts Git
- Les services généraux utilisent le portail interne et le serveur de fichiers

Chaque outil dispose de sa propre fonction de recherche, mais il n'existe aucun moyen de rechercher de manière transversale entre les outils.
En conséquence, il arrive fréquemment que l'on ne trouve pas « le document créé par l'équipe voisine » et que l'on recrée un document similaire de zéro.

Résoudre le problème grâce à une infrastructure de recherche
---------------------------------------------------------------

La solution à ces défis est la « recherche d'entreprise (infrastructure de recherche interne) ».
La recherche d'entreprise fournit un mécanisme permettant de rechercher de manière transversale les différentes sources de données au sein de l'organisation.

L'adoption d'une solution de recherche d'entreprise permet d'obtenir les bénéfices suivants :

- **Réduction du temps de recherche d'information** : rechercher en un seul point les informations dispersées
- **Promotion de la réutilisation des connaissances** : faciliter la découverte des productions et expertises passées
- **Accélération de la prise de décision** : accéder rapidement à l'information nécessaire pour décider
- **Réduction de la dépendance aux individus** : diminuer les situations où « il faut demander à telle personne pour savoir »

Qu'est-ce que Fess ?
=====================

Fess est un serveur de recherche plein texte open source.
Distribué sous licence Apache, il peut être utilisé gratuitement, y compris pour un usage commercial.
Construit en Java, il utilise OpenSearch comme moteur de recherche.

Vue d'ensemble de Fess
------------------------

Fess n'est pas un simple moteur de recherche, mais un « système de recherche » complet intégrant toutes les fonctionnalités nécessaires.

**Robot d'indexation (crawler)**

Il collecte automatiquement les documents depuis diverses sources de données telles que les sites web, les serveurs de fichiers, le stockage cloud et les applications SaaS.
Il prend en charge plus de 100 formats de fichiers, notamment HTML, PDF, Word, Excel et PowerPoint.

**Moteur de recherche**

Il offre une recherche plein texte rapide avec OpenSearch en backend.
Il prend en charge plus de 20 langues, dont le japonais, et peut monter en charge pour de grands volumes de documents.

**Interface de recherche**

Une interface de recherche basée sur un navigateur est fournie en standard.
Elle offre une expérience de recherche conviviale avec la mise en surbrillance des résultats, les facettes (filtrage), et les suggestions (autocomplétion).

**Console d'administration**

La configuration du crawl, la gestion des utilisateurs, la gestion des dictionnaires et autres paramètres opérationnels peuvent être effectués depuis le navigateur.
Le système de recherche peut être administré depuis la console d'administration sans nécessiter de connaissances en ligne de commande.

**API**

Une API de recherche basée sur JSON est fournie, permettant d'intégrer des fonctionnalités de recherche dans les systèmes existants.

Pourquoi choisir Fess ?
-------------------------

Il existe plusieurs options en matière de recherche d'entreprise.
On peut utiliser directement OpenSearch ou Elasticsearch, ou opter pour des solutions de recherche commerciales.
Voici les raisons de choisir Fess parmi ces alternatives.

**Comparaison avec une solution développée en interne**

OpenSearch et Elasticsearch sont des moteurs de recherche puissants, mais ils ne suffisent pas à eux seuls pour constituer un système de recherche complet.
Il est nécessaire de développer soi-même de nombreuses fonctionnalités : implémentation du crawler, traitement de l'analyse des documents, développement de l'interface de recherche, mécanisme de gestion des droits, etc.
Fess fournit tout cela de manière intégrée, réduisant ainsi considérablement l'effort de développement nécessaire à la mise en place d'un système de recherche.

**Comparaison avec les produits commerciaux**

Les produits commerciaux de recherche d'entreprise sont riches en fonctionnalités, mais les coûts de licence tendent à être élevés.
Fess étant open source, il n'y a aucun coût logiciel.
De plus, le code source étant ouvert, il n'y a aucun risque de dépendance à un fournisseur (vendor lock-in).
Si des personnalisations sont nécessaires, elles peuvent être réalisées librement.

**Extensibilité par les plugins**

Fess adopte une architecture basée sur des plugins.
Des plugins sont disponibles pour diverses sources de données telles que Slack, SharePoint, Box, Dropbox, Confluence et Jira.
De plus, des extensions adaptées à l'ère de l'IA sont possibles, comme les plugins LLM permettant l'intégration avec des grands modèles de langage (LLM).

Scénarios de recherche réalisables avec Fess
===============================================

Quels types d'environnements de recherche peut-on concrètement construire avec Fess ?
Voici un aperçu des scénarios abordés dans cette série.

Recherche transversale de documents internes
----------------------------------------------

Il est possible de rechercher depuis un point unique des sources de données multiples telles que les serveurs de fichiers, le stockage cloud et les sites web.
Même si chaque département utilise des outils différents, les utilisateurs peuvent accéder à l'information dont ils ont besoin depuis une seule barre de recherche.

Contrôle d'accès par département
-----------------------------------

Les documents affichés dans les résultats de recherche peuvent être contrôlés en fonction de l'appartenance et des droits de l'utilisateur.
Les documents confidentiels du département des ressources humaines n'apparaîtront pas dans les résultats de recherche de l'équipe commerciale.
Il est également possible de s'intégrer aux services d'annuaire existants (Active Directory, LDAP) pour refléter automatiquement les informations de droits d'accès.

Ajout de fonctionnalités de recherche aux systèmes existants
---------------------------------------------------------------

Les fonctionnalités de recherche de Fess peuvent être intégrées dans les portails internes ou les systèmes métier.
Plusieurs approches sont disponibles, notamment FSS (Fess Site Search) qui s'intègre facilement en JavaScript, ou l'intégration personnalisée via l'API.

Expérience de recherche enrichie par l'IA
-------------------------------------------

Le RAG (Retrieval-Augmented Generation), qui suscite un intérêt croissant ces dernières années, peut être mis en œuvre avec Fess.
Lorsqu'un utilisateur pose une question en langage naturel, Fess recherche les informations pertinentes dans les documents internes et le LLM génère une réponse.
En tant qu'« assistant IA interne », il permet de faire évoluer encore davantage l'exploitation des connaissances.

Structure de la série
=======================

Cette série est composée de 23 parties au total.
Elle est conçue pour permettre une compréhension progressive, des débutants aux utilisateurs avancés.

**Partie fondamentale (Parties 1 à 5)**

Les cinq premières parties, dont le présent article, couvrent l'installation de Fess et les scénarios de base.
Vous apprendrez le démarrage rapide avec Docker Compose, l'ajout de fonctionnalités de recherche à un site web, la construction d'une recherche multi-sources et le contrôle d'accès basé sur les droits.

**Partie solutions pratiques (Parties 6 à 12)**

Cette section couvre des sujets pratiques basés sur des scénarios métier réels : construction d'un hub de connaissances pour les équipes de développement, recherche transversale dans le stockage cloud, optimisation de la qualité de recherche, support multilingue, gestion opérationnelle et intégration API.

**Partie architecture et mise à l'échelle (Parties 13 à 17)**

Cette section aborde des sujets d'architecture avancés : conception multi-tenant, mise à l'échelle pour les environnements de grande taille, architecture de sécurité, automatisation opérationnelle de type DevOps et développement de plugins.

**Partie IA et recherche de nouvelle génération (Parties 18 à 22)**

Cette section couvre les dernières technologies de recherche, depuis les bases de la recherche sémantique jusqu'à la construction d'un assistant IA par RAG, l'utilisation en tant que serveur MCP, la recherche multimodale et l'analytique de recherche.

**Conclusion (Partie 23)**

La dernière partie synthétise les enseignements de l'ensemble de la série et présente une architecture de référence pour une plateforme de connaissances centrée sur Fess.

Résumé
======

Dans cet article, nous avons présenté la nécessité d'une infrastructure de recherche en entreprise et le positionnement de Fess.

- La surcharge informationnelle et les silos d'information sont des défis communs à de nombreuses entreprises
- La recherche d'entreprise permet de rechercher de manière transversale les informations dispersées
- Fess est open source et fournit un ensemble complet de fonctionnalités nécessaires à un système de recherche
- Il prend en charge l'extensibilité par plugins et l'intégration avec l'IA

Dans la prochaine partie, nous présenterons comment démarrer Fess avec Docker Compose et tester l'expérience de recherche le plus rapidement possible.

Références
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `OpenSearch <https://opensearch.org/>`__

- `GitHub - codelibs/fess <https://github.com/codelibs/fess>`__
