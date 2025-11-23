======================================
Architecture et Fonctionnalités de Fess
======================================

Vue d'ensemble
==============

Cette page décrit les principales fonctionnalités et l'architecture de Fess du point de vue des composants.
Fess utilise une conception modulaire pour faciliter la construction de systèmes de recherche.

Architecture Globale
====================

Fess se compose des composants principaux suivants :

.. figure:: ../resources/images/en/architecture-overview.png
   :scale: 100%
   :alt: Vue d'ensemble de l'architecture Fess
   :align: center

   Vue d'ensemble de l'architecture Fess

Composants Principaux
=====================

1. Sous-système de Crawl
-------------------------

Le sous-système de crawl est responsable de la collecte de documents à partir de diverses sources de données.

**Classes et Fonctionnalités Principales :**

Crawler
~~~~~~~

- **Rôle** : Classe centrale pour le traitement du crawl
- **Fonctionnalités Principales** :

  - Collecte de documents depuis des sites web, systèmes de fichiers et magasins de données
  - Sélection des cibles basée sur la configuration du crawl
  - Gestion de l'exécution des tâches de crawl
  - Gestion de session pour les résultats du crawl

- **Modes d'Exécution** :

  - Exécution périodique planifiée
  - Exécution manuelle depuis l'interface d'administration
  - Exécution en ligne de commande

WebCrawler
~~~~~~~~~~

- **Rôle** : Crawl de sites web
- **Fonctionnalités Principales** :

  - Récupération et analyse des pages HTML
  - Extraction et parcours des liens
  - Support des sites basés sur JavaScript
  - Support des sites avec authentification (BASIC/DIGEST/NTLM/FORM)
  - Respect de robots.txt

FileCrawler
~~~~~~~~~~~

- **Rôle** : Crawl de systèmes de fichiers
- **Fonctionnalités Principales** :

  - Parcours des systèmes de fichiers locaux
  - Accès aux lecteurs réseau (SMB/CIFS)
  - Détection du format de fichier et sélection du parseur approprié
  - Contrôle d'accès basé sur les permissions

DataStoreCrawler
~~~~~~~~~~~~~~~~

- **Rôle** : Crawl de magasins de données externes
- **Fonctionnalités Principales** :

  - Récupération de données depuis des bases de données
  - Intégration avec le stockage cloud (Google Drive, Dropbox, Box, etc.)
  - Intégration avec les groupwares (Office 365, Slack, Confluence, etc.)
  - Extensibilité via plugins

CrawlConfig
~~~~~~~~~~~

- **Rôle** : Gestion de la configuration du crawl
- **Fonctionnalités Principales** :

  - Définition des URLs ou chemins cibles pour le crawl
  - Limitation de la profondeur du crawl
  - Configuration de l'intervalle de crawl
  - Spécification des modèles d'exclusion
  - Attribution de labels

2. Sous-système d'Indexation
-----------------------------

Le sous-système d'indexation convertit les documents collectés en format consultable.

DocumentParser
~~~~~~~~~~~~~~

- **Rôle** : Analyse de documents et extraction de texte
- **Fonctionnalités Principales** :

  - Support de divers formats de fichiers via Apache Tika
  - Extraction de métadonnées
  - Détection automatique de l'encodage des caractères
  - Détection automatique de la langue

Indexer
~~~~~~~

- **Rôle** : Enregistrement d'index dans OpenSearch/Elasticsearch
- **Fonctionnalités Principales** :

  - Création d'index de documents
  - Indexation en masse pour améliorer les performances
  - Optimisation d'index
  - Suppression des anciens documents

FieldMapper
~~~~~~~~~~~

- **Rôle** : Définition du mapping des champs
- **Fonctionnalités Principales** :

  - Définition des champs de document
  - Ajout de champs personnalisés
  - Spécification du type de champ (text, keyword, date, etc.)
  - Configuration d'analyseurs multilingues

3. Sous-système de Recherche
-----------------------------

Le sous-système de recherche traite les requêtes de recherche des utilisateurs et renvoie les résultats.

SearchService
~~~~~~~~~~~~~

- **Rôle** : Cœur du traitement de recherche
- **Fonctionnalités Principales** :

  - Analyse et optimisation des requêtes
  - Exécution de requêtes sur OpenSearch/Elasticsearch
  - Classement des résultats de recherche
  - Support de la recherche à facettes
  - Surlignage

QueryProcessor
~~~~~~~~~~~~~~

- **Rôle** : Prétraitement des requêtes de recherche
- **Fonctionnalités Principales** :

  - Normalisation des requêtes
  - Expansion de synonymes
  - Traitement des mots vides
  - Correction de requêtes

SuggestService
~~~~~~~~~~~~~~

- **Rôle** : Fourniture de fonctionnalités de suggestion
- **Fonctionnalités Principales** :

  - Génération de candidats pour l'autocomplétion
  - Fourniture de mots-clés de recherche populaires
  - Utilisation de dictionnaires personnalisés

RankingService
~~~~~~~~~~~~~~

- **Rôle** : Ajustement du classement des résultats de recherche
- **Fonctionnalités Principales** :

  - Boosting de documents
  - Boosting de champs
  - Scoring personnalisé
  - Ajustement de la pertinence

4. Sous-système d'Administration
---------------------------------

Le sous-système d'administration gère la configuration et l'exploitation de Fess.

AdminConsole
~~~~~~~~~~~~

- **Rôle** : Interface d'administration web
- **Fonctionnalités Principales** :

  - Gestion de la configuration du crawl
  - Paramètres du planificateur
  - Gestion des utilisateurs et des rôles
  - Paramètres système
  - Consultation des journaux

Scheduler
~~~~~~~~~

- **Rôle** : Gestion des planifications de tâches
- **Fonctionnalités Principales** :

  - Exécution périodique des tâches de crawl
  - Exécution périodique de l'optimisation d'index
  - Rotation des journaux
  - Configuration de planification avec expressions Cron

BackupManager
~~~~~~~~~~~~~

- **Rôle** : Sauvegarde et restauration
- **Fonctionnalités Principales** :

  - Sauvegarde des données de configuration
  - Snapshots d'index
  - Fonctionnalité de restauration
  - Planification de sauvegardes automatiques

5. Sous-système d'Authentification et d'Autorisation
-----------------------------------------------------

Le sous-système d'authentification et d'autorisation gère la sécurité et le contrôle d'accès.

AuthenticationManager
~~~~~~~~~~~~~~~~~~~~~

- **Rôle** : Gestion de l'authentification des utilisateurs
- **Fonctionnalités Principales** :

  - Authentification locale
  - Intégration LDAP/Active Directory
  - Intégration SAML
  - Intégration OpenID Connect
  - Contrôle d'accès basé sur les rôles (RBAC)

RoleManager
~~~~~~~~~~~

- **Rôle** : Gestion des rôles et des permissions d'accès
- **Fonctionnalités Principales** :

  - Définition de rôles
  - Attribution de rôles aux utilisateurs
  - Contrôle d'accès au niveau des documents
  - Filtrage des résultats de recherche

6. Couche API
-------------

La couche API fournit une intégration avec des systèmes externes.

SearchAPI
~~~~~~~~~

- **Rôle** : Fourniture de l'API de recherche
- **Fonctionnalités Principales** :

  - Recherche basée sur API REST
  - Réponses au format JSON
  - Compatibilité OpenSearch
  - API compatible GSA (Google Search Appliance)

AdminAPI
~~~~~~~~

- **Rôle** : Fourniture de l'API d'administration
- **Fonctionnalités Principales** :

  - Opérations CRUD pour la configuration du crawl
  - Gestion d'index
  - Contrôle du planificateur
  - Récupération d'informations système

7. Stockage de Données
-----------------------

Le stockage de données gère la persistance des données pour Fess.

ConfigStore
~~~~~~~~~~~

- **Rôle** : Stockage des données de configuration
- **Fonctionnalités Principales** :

  - Persistance de la configuration du crawl
  - Stockage de la configuration système
  - Gestion des informations utilisateur et rôle
  - Utilisation de base de données H2 ou DB externe

SearchEngine
~~~~~~~~~~~~

- **Rôle** : Intégration avec le moteur de recherche
- **Fonctionnalités Principales** :

  - Communication avec OpenSearch/Elasticsearch
  - Gestion d'index
  - Exécution de requêtes
  - Support du clustering

Architecture de Plugins
========================

Fess peut être étendu via des plugins.

Plugins DataStore
-----------------

- **Rôle** : Connexion à des sources de données externes
- **Plugins Disponibles** :

  - Atlassian (Confluence/Jira)
  - Box
  - CSV
  - Database
  - Dropbox
  - Git/GitBucket
  - Google Drive
  - Office 365
  - S3
  - Slack
  - Autres

Plugins Theme
-------------

- **Rôle** : Personnalisation de l'interface de recherche
- **Plugins Disponibles** :

  - Simple Theme
  - Classic Theme

Plugins Ingester
----------------

- **Rôle** : Pré- et post-traitement des données d'index
- **Plugins Disponibles** :

  - Logger
  - NDJSON

Plugins Script
--------------

- **Rôle** : Personnalisation basée sur des scripts
- **Plugins Disponibles** :

  - Groovy
  - OGNL

Gestion de la Configuration
============================

FessConfig
----------

- **Rôle** : Gestion centralisée de la configuration système
- **Principaux Éléments de Configuration** :

  - Paramètres système généraux
  - Paramètres de crawl
  - Paramètres de recherche
  - Paramètres d'authentification
  - Paramètres de notification
  - Paramètres de performance

DynamicProperties
-----------------

- **Rôle** : Gestion de configuration dynamique
- **Fonctionnalités Principales** :

  - Modifications de configuration à l'exécution
  - Utilisation de variables d'environnement
  - Configuration spécifique au profil

Résumé
======

Fess réalise un système de recherche plein texte puissant grâce à la collaboration de ces composants.
Chaque composant est conçu avec un couplage lâche et peut être personnalisé ou étendu selon les besoins.

Pour des informations plus détaillées pour les développeurs, voir :

- `JavaDoc <https://fess.codelibs.org/apidocs/index.html>`__
- `XRef <https://fess.codelibs.org/xref/index.html>`__
- `Guide du Développeur <dev/index.html>`__
- `Dépôt GitHub <https://github.com/codelibs/fess>`__
