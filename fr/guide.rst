==============
Guide Pratique
==============

Valoriser les connaissances avec Fess
=====================================

Ce guide pratique explique comment rendre les informations de votre organisation consultables avec Fess et en faire une plateforme de recherche que l'on continue d'utiliser.
Chaque article porte sur Fess 15.9 et décrit concrètement les champs des écrans de configuration, les clés de configuration et la manière de vérifier que tout a fonctionné.
Les fonctionnalités disponibles uniquement à partir de la version 15.10 sont signalées explicitement dans les articles.

Choisir selon votre objectif
============================

- **Je veux d'abord essayer Fess** : :doc:`articles/guide-01` → :doc:`articles/guide-02`
- **Je veux rechercher dans des serveurs de fichiers** : :doc:`articles/file-server-search` → :doc:`articles/guide-04` → :doc:`articles/guide-05`
- **Je veux rechercher des données du cloud et de services SaaS** : :doc:`articles/datastore-basics` → :doc:`articles/guide-07` / :doc:`articles/guide-06` / :doc:`articles/guide-12`
- **Je veux intégrer la recherche à un site ou un système existant** : :doc:`articles/guide-03` → :doc:`articles/guide-11`
- **Je veux afficher des informations différentes selon le service ou l'utilisateur** : :doc:`articles/guide-05` → :doc:`articles/guide-15` → :doc:`articles/guide-13`
- **Je veux améliorer la recherche avec l'IA** : :doc:`articles/guide-18` → :doc:`articles/guide-19` → :doc:`articles/guide-20`
- **Je commence l'exploitation en production** : :doc:`articles/guide-10` → :doc:`articles/guide-16` → :doc:`articles/guide-14`

Premiers pas
============

- :doc:`articles/guide-01` - L'architecture de Fess, la répartition des rôles entre Fess et les plugins, et les parcours de lecture par objectif
- :doc:`articles/guide-02` - Démarrer Fess avec Docker Compose et essayer tout le parcours, de l'exploration à la recherche

Collecter les informations
==========================

- :doc:`articles/guide-04` - Explorer des sites web et des serveurs de fichiers, et permettre de filtrer les résultats par étiquette
- :doc:`articles/datastore-basics` - Paramètres des plugins de magasin de données, autorisations, étiquettes, planification et vérification des résultats
- :doc:`articles/guide-07` - Rendre consultables les fichiers de Google Drive, SharePoint Online / OneDrive et Box
- :doc:`articles/guide-06` - Rendre consultables les dépôts Git, Confluence, Jira et Slack
- :doc:`articles/guide-12` - Rendre consultables les données de bases de données, de fichiers CSV et de Salesforce

Intégrer la recherche et modifier son apparence
===============================================

- :doc:`articles/guide-03` - Placer une zone de recherche sur un site existant et ajuster l'apparence de la page de recherche avec des thèmes
- :doc:`articles/guide-11` - Rechercher et enregistrer des documents depuis des applications métier avec l'API de recherche et des jetons d'accès

Contrôler l'accès
=================

- :doc:`articles/guide-05` - Différencier les résultats de recherche selon les rôles et les groupes, et s'intégrer à LDAP / Active Directory
- :doc:`articles/guide-15` - Mettre en place le SSO (OIDC / SAML / Entra ID / SPNEGO) et protéger l'accès depuis l'extérieur
- :doc:`articles/guide-13` - Partager une seule instance de Fess entre plusieurs organisations grâce aux hôtes virtuels et aux rôles

Améliorer la qualité de la recherche
====================================

- :doc:`articles/guide-08` - Repérer les problèmes dans les écrans d'analyse des journaux de recherche et les corriger avec les synonymes et les correspondances de clé
- :doc:`articles/guide-09` - Comprendre comment les documents multilingues sont indexés et recherchés, et ajuster chaque langue
- :doc:`articles/guide-22` - Agréger et visualiser les journaux de recherche à votre façon avec OpenSearch Dashboards

Exploitation
============

- :doc:`articles/guide-10` - Contrôles d'état, journaux, notifications, sauvegarde et restauration, et traitement des URL d'échec
- :doc:`articles/guide-16` - Gérer la configuration sous forme de code avec fessctl et l'API d'administration, et reproduire les environnements
- :doc:`articles/guide-14` - Paramètres mémoire, cluster OpenSearch externe et exécution de Fess sur plusieurs serveurs
- :doc:`articles/guide-17` - Ajouter des fonctionnalités en écrivant vos propres plugins de magasin de données et ingesters

Améliorer la recherche avec l'IA
================================

- :doc:`articles/guide-18` - Utiliser la recherche vectorielle et la fusion de classements pour trouver les documents même lorsqu'ils sont formulés différemment
- :doc:`articles/guide-19` - Connecter un LLM et utiliser le mode de recherche IA, qui répond en s'appuyant sur les documents internes
- :doc:`articles/guide-20` - Permettre à des agents IA d'effectuer des recherches dans Fess via le plugin de serveur MCP
- :doc:`articles/guide-21` - Mettre en place une recherche multimodale qui couvre à la fois les images et le texte

Planifier un déploiement à l'échelle de l'entreprise
====================================================

- :doc:`articles/guide-23` - Ce qu'il faut configurer et vérifier à chaque étape, de l'introduction au déploiement à l'échelle de l'entreprise

Cas d'utilisation et comparaisons
=================================

- :doc:`articles/use-cases` - Cas d'utilisation par secteur et par taille, et les articles utiles pour chacun
- :doc:`articles/comparison` - Comparaison de Fess avec d'autres solutions de recherche (OpenSearch seul, Solr, produits commerciaux, etc.)
- :doc:`articles/file-server-search` - Ce qu'il faut vérifier avant de mettre en place la recherche plein texte sur des serveurs de fichiers

.. toctree::
   :hidden:

   articles/guide-01
   articles/guide-02
   articles/guide-04
   articles/datastore-basics
   articles/guide-07
   articles/guide-06
   articles/guide-12
   articles/guide-03
   articles/guide-11
   articles/guide-05
   articles/guide-15
   articles/guide-13
   articles/guide-08
   articles/guide-09
   articles/guide-22
   articles/guide-10
   articles/guide-16
   articles/guide-14
   articles/guide-17
   articles/guide-18
   articles/guide-19
   articles/guide-20
   articles/guide-21
   articles/guide-23
   articles/use-cases
   articles/comparison
   articles/file-server-search
