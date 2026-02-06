===============================
Cas d'utilisation de Fess
===============================

Introduction
============

Fess est utilisé par des organisations de divers secteurs et de toutes tailles.
Cette page présente des cas d'utilisation représentatifs et des exemples pratiques de déploiement de Fess.

.. note::

   Les exemples suivants illustrent les modèles de déploiement courants de Fess.
   Pour des études de cas concrètes, veuillez contacter le `support commercial <../support-services.html>`__.

----

Cas d'utilisation par secteur
==============================

Fabrication
-----------

**Défi** : Les dessins de conception, les documents techniques et les documents de gestion de la qualité sont dispersés sur plusieurs serveurs de fichiers, ce qui rend la recherche d'informations chronophage.

**Solution Fess** :

- Recherche unifiée des dessins CAO, des documents techniques PDF et des documents Office sur les serveurs de fichiers
- Recherche croisée par numéros de modèle de produit, numéros de dessin et noms de projet
- Affichage des résultats de recherche basé sur les permissions d'accès (recherche basée sur les rôles)

**Exemple d'architecture** :

.. code-block:: text

    [Serveurs de fichiers]  →  [Fess]  →  [Portail interne]
         │                      │
         ├─ Dessins              ├─ Cluster OpenSearch
         ├─ Docs techniques      └─ Intégration Active Directory
         └─ Registres QC

**Fonctionnalités associées** :

- `Exploration de serveurs de fichiers <https://fess.codelibs.org/fr/15.5/config/config-filecrawl.html>`__
- `Recherche basée sur les rôles <https://fess.codelibs.org/fr/15.5/config/config-role.html>`__
- `Affichage des miniatures <https://fess.codelibs.org/fr/15.5/admin/admin-general.html>`__

Finance et assurance
--------------------

**Défi** : Les documents de conformité, les contrats et les réglementations internes sont volumineux, ce qui rend les réponses aux audits et le traitement des demandes chronophages.

**Solution Fess** :

- Recherche croisée des réglementations internes, manuels et FAQ
- Recherche textuelle des contrats et documents de demande
- Recherche dans la base de connaissances à partir de l'historique des demandes passées

**Fonctionnalités de sécurité** :

- Authentification via l'intégration LDAP/Active Directory
- Authentification unique via SAML
- Authentification API via des jetons d'accès

**Fonctionnalités associées** :

- `Authentification LDAP <https://fess.codelibs.org/fr/15.5/config/config-security.html>`__
- `Authentification SAML <https://fess.codelibs.org/fr/15.5/config/config-saml.html>`__

Éducation
---------

**Défi** : Les articles de recherche, les supports de cours et les documents du campus sont répartis sur les serveurs de différents départements, ce qui rend le partage d'informations difficile.

**Solution Fess** :

- Recherche unifiée depuis le portail du campus
- Recherche dans le dépôt d'articles de recherche
- Recherche de supports de cours et de programmes

**Exemples d'architecture** :

- Exploration du site web du campus
- Intégration avec des dépôts d'articles (DSpace, etc.)
- Recherche de documents sur Google Drive / SharePoint

**Fonctionnalités associées** :

- `Exploration web <https://fess.codelibs.org/fr/15.5/config/config-webcrawl.html>`__
- `Exploration Google Drive <https://fess.codelibs.org/fr/15.5/config/config-crawl-gsuite.html>`__

IT et logiciel
--------------

**Défi** : Le code source, la documentation, les wikis et les informations du système de gestion des tickets sont dispersés, ce qui réduit l'efficacité du développement.

**Solution Fess** :

- Recherche de code dans les dépôts GitHub/GitLab
- Recherche de pages Confluence/Wiki
- Recherche de messages Slack/Teams

**Fonctionnalités pour les développeurs** :

- Intégration avec les systèmes existants via l'API de recherche
- Mise en évidence du code
- Filtrage par type de fichier

**Fonctionnalités associées** :

- `Exploration de dépôts Git <https://fess.codelibs.org/fr/15.5/config/config-crawl-git.html>`__
- `Exploration Confluence <https://fess.codelibs.org/fr/15.5/config/config-crawl-atlassian.html>`__
- `Exploration Slack <https://fess.codelibs.org/fr/15.5/config/config-crawl-slack.html>`__

----

Cas d'utilisation par taille d'entreprise
==========================================

PME (jusqu'à 100 employés)
---------------------------

**Caractéristiques** : Souhaitent un déploiement et une exploitation faciles avec des ressources informatiques limitées.

**Configuration recommandée** :

- Déploiement facile via Docker Compose
- Configuration sur un seul serveur (Fess + OpenSearch)
- Mémoire requise : 8 Go ou plus

**Étapes de déploiement** :

.. code-block:: bash

    # Déploiement en 5 minutes
    mkdir fess && cd fess
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml
    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Coût** :

- Logiciel : Gratuit (Open Source)
- Seuls les coûts du serveur (Cloud ou sur site)

Moyennes entreprises (100-1000 employés)
-----------------------------------------

**Caractéristiques** : Utilisation multi-départements, nécessite une disponibilité raisonnable.

**Configuration recommandée** :

- 2 serveurs Fess (redondance)
- Cluster OpenSearch à 3 noeuds
- Répartiteur de charge pour la distribution du trafic
- Intégration Active Directory

**Lignes directrices de capacité** :

- Documents : jusqu'à 5 millions
- Utilisateurs de recherche simultanés : jusqu'à 100

**Fonctionnalités associées** :

- `Configuration en cluster <https://fess.codelibs.org/fr/15.5/install/clustering.html>`__
- `Sauvegarde et restauration <https://fess.codelibs.org/fr/15.5/admin/admin-backup.html>`__

Grandes entreprises (plus de 1000 employés)
--------------------------------------------

**Caractéristiques** : Données à grande échelle, haute disponibilité, exigences de sécurité strictes.

**Configuration recommandée** :

- Plusieurs serveurs Fess (exécutés sur Kubernetes)
- Cluster OpenSearch (configuration de noeuds dédiés)
- Serveurs d'exploration dédiés
- Intégration avec l'infrastructure de surveillance et de collecte de journaux

**Évolutivité** :

- Documents : des centaines de millions possibles
- Mise à l'échelle horizontale via le partitionnement OpenSearch

**Fonctionnalités entreprise** :

- Gestion des étiquettes par département
- Journalisation détaillée des accès
- Intégration avec d'autres systèmes via l'API

.. note::

   Pour les déploiements à grande échelle, nous recommandons d'utiliser le `support commercial <../support-services.html>`__.

----

Cas d'utilisation techniques
=============================

Recherche de wiki interne / base de connaissances
---------------------------------------------------

**Aperçu** : Permettre la recherche croisée de Confluence, MediaWiki et des wikis internes.

**Avantages** :

- Recherche unifiée à travers plusieurs systèmes de wiki
- Exploration automatique basée sur la fréquence de mise à jour
- Les pièces jointes des pages wiki sont incluses dans le périmètre de recherche

**Mise en oeuvre** :

1. Installer le plugin Confluence Data Store
2. Configurer les paramètres de connexion depuis le panneau d'administration
3. Définir le calendrier d'exploration (par exemple, quotidien)

Recherche unifiée de serveurs de fichiers
------------------------------------------

**Aperçu** : Rechercher des documents sur les serveurs de fichiers Windows et les NAS.

**Protocoles pris en charge** :

- SMB/CIFS (dossiers partagés Windows)
- NFS
- Système de fichiers local

**Sécurité** :

- Contrôle d'accès basé sur l'authentification NTLM
- Les ACL des fichiers sont reflétées dans les résultats de recherche

**Points de configuration** :

- Créer un compte d'exploration dédié
- Exploration par phases pour les grands volumes de fichiers
- Prendre en compte la bande passante réseau

Recherche de site web (Site Search)
-------------------------------------

**Aperçu** : Ajouter une fonctionnalité de recherche aux sites web publics.

**Méthodes de déploiement** :

1. **Intégration JavaScript**

   Utilisez Fess Site Search (FSS) pour ajouter une boîte de recherche avec seulement quelques lignes de JavaScript

2. **Intégration API**

   Construisez une interface de recherche personnalisée en utilisant l'API de recherche

**Exemple FSS** :

.. code-block:: html

    <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      fess.src = 'https://your-fess-server/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      fess.setAttribute('fess-url', 'https://your-fess-server/json');
      document.body.appendChild(fess);
    })();
    </script>
    <fess:search></fess:search>

Recherche de base de données
------------------------------

**Aperçu** : Rendre les données des bases de données relationnelles recherchables.

**Bases de données prises en charge** :

- MySQL / MariaDB
- PostgreSQL
- Oracle
- SQL Server

**Cas d'utilisation** :

- Recherche de fichiers clients
- Recherche dans le catalogue de produits
- Recherche dans la base de données FAQ

**Mise en oeuvre** :

1. Configurer le plugin Database Data Store
2. Spécifier la cible d'exploration avec une requête SQL
3. Configurer le mappage des champs

----

Résumé
=======

Fess, grâce à sa conception flexible, peut répondre aux besoins de divers secteurs, échelles et cas d'utilisation.

**Pour ceux qui envisagent un déploiement** :

1. Commencez par essayer Fess avec le `Guide de démarrage rapide <../quick-start.html>`__
2. Vérifiez les fonctionnalités requises dans la `Documentation <../documentation.html>`__
3. Pour un déploiement en production, consultez le `support commercial <../support-services.html>`__

**Ressources associées** :

- `Liste des articles <../articles.html>`__ - Articles techniques détaillés
- `Forum de discussion <https://discuss.codelibs.org/c/fessen/>`__ - Support communautaire
- `GitHub <https://github.com/codelibs/fess>`__ - Code source et suivi des problèmes
