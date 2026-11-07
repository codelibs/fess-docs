========================================================
Partie 4 : Recherche unifiée dans des fichiers dispersés
========================================================

Introduction
============

Dans l'article précédent, nous avons présenté comment intégrer la fonction de recherche de Fess dans un site Web existant.
Cependant, dans un environnement d'entreprise réel, les informations ne se trouvent pas uniquement sur des sites Web, mais sont dispersées dans divers emplacements tels que des serveurs de fichiers et des services de stockage cloud.

Dans cet article, nous allons intégrer plusieurs sources de données dans Fess et construire un environnement permettant aux utilisateurs d'effectuer une recherche transversale sur tous les documents depuis une seule barre de recherche.

Public cible
============

- Personnes dont les documents internes sont répartis dans plusieurs emplacements
- Personnes insatisfaites de la recherche sur les serveurs de fichiers ou le stockage cloud
- Avoir Fess en cours d'exécution selon la procédure de la Partie 2

Scénario
========

Nous supposons une entreprise de taille moyenne. Dans cette entreprise, les documents sont dispersés dans les emplacements suivants :

- **Site Web interne** : portail interne, blog interne
- **Serveur de fichiers** : dossiers partagés par département (SMB/CIFS)
- **Fichiers locaux** : répertoires spécifiques sur le serveur

Lorsqu'un employé se demande "où est ce document ?", il doit effectuer des recherches séparées dans chaque outil.
Nous allons centraliser cela avec Fess afin de permettre une recherche transversale depuis une seule barre de recherche.

Conception des sources de données
==================================

Lors de la construction d'une recherche transversale, la première étape importante est de concevoir "quoi indexer et comment".

Organisation des cibles de recherche
-------------------------------------

Commencez par organiser les sources de données à indexer.

.. list-table:: Organisation des sources de données
   :header-rows: 1
   :widths: 20 25 25 30

   * - Source de données
     - Type
     - Estimation du volume
     - Fréquence de mise à jour
   * - Portail interne
     - Exploration Web
     - Quelques centaines de pages
     - Hebdomadaire
   * - Blog technique
     - Exploration Web
     - De quelques dizaines a quelques centaines de pages
     - Irrégulière
   * - Dossier partagé
     - Exploration de fichiers
     - Dizaines de milliers de fichiers
     - Quotidienne
   * - Archives
     - Exploration de fichiers
     - Quelques milliers de fichiers
     - Mensuelle

Conception de la classification par libellés
---------------------------------------------

La fonction "Libellé" de Fess permet de catégoriser les cibles de recherche.
Les utilisateurs peuvent sélectionner un libellé lors de la recherche pour affiner les résultats à une catégorie spécifique.

Dans ce scénario, nous configurons les libellés suivants :

- **Portail** : informations du portail interne et du blog
- **Fichiers partagés** : documents du serveur de fichiers
- **Archives** : documents anciens

Configuration des libellés
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Dans l'écran d'administration, sélectionnez [Exploration] > [Libellés]
2. Créez un libellé avec [Nouveau]

Définissez un "Nom" et une "Valeur" pour chaque libellé.
La valeur doit être en caractères alphanumériques et sert à associer le libellé à la configuration d'exploration.

Construction de la configuration d'exploration
================================================

Configuration de l'exploration Web
------------------------------------

Voici la configuration d'exploration pour le portail interne.

1. [Exploration] > [Web] > [Nouveau]
2. Configurez les éléments suivants :

   - URL : ``https://portal.example.com/``
   - URL à explorer : ``https://portal.example.com/.*``
   - URL à exclure de l'exploration : ``https://portal.example.com/admin/.*``
   - Nombre maximum d'accès : ``500``
   - Nombre de threads : ``3``
   - Intervalle : ``5000``
   - Libellé : Portail

3. Cliquez sur [Créer]

En définissant des URL d'exclusion, vous pouvez exclure les pages que vous ne souhaitez pas indexer, comme les écrans d'administration.

Configuration de l'exploration de fichiers
-------------------------------------------

Voici la configuration d'exploration pour le dossier partagé.

1. [Exploration] > [Système de fichiers] > [Nouveau]
2. Configurez les éléments suivants :

   - Chemin : ``smb://fileserver.example.com/shared/``
   - Chemin à explorer : ``smb://fileserver.example.com/shared/.*``
   - Chemin à exclure de l'exploration : ``.*\\.tmp$``
   - Nombre maximum d'accès : ``10000``
   - Nombre de threads : ``5``
   - Intervalle : ``1000``
   - Libellé : Fichiers partagés

3. Cliquez sur [Créer]

**Configuration de l'authentification SMB**

Si le serveur de fichiers nécessite une authentification, la configuration de l'authentification de fichiers est nécessaire.

1. [Exploration] > [Authentification de fichiers] > [Nouveau]
2. Configurez les éléments suivants :

   - Nom d'hôte : ``fileserver.example.com``
   - Schéma : ``Samba``
   - Nom d'utilisateur : nom d'utilisateur du compte de service
   - Mot de passe : mot de passe du compte de service

3. Cliquez sur [Créer]

Exploration de fichiers locaux
-------------------------------

Pour explorer un répertoire spécifique sur le serveur, spécifiez directement le chemin du fichier.

1. [Exploration] > [Système de fichiers] > [Nouveau]
2. Configurez les éléments suivants :

   - Chemin : ``file:///data/archive/``
   - Chemin à explorer : ``file:///data/archive/.*``
   - Chemin à exclure de l'exploration : ``.*\\.(log|bak)$``
   - Nombre maximum d'accès : ``5000``
   - Libellé : Archives

3. Cliquez sur [Créer]

Conception du calendrier d'exploration
=======================================

Lorsque vous explorez plusieurs sources de données, la conception du calendrier est importante.
Exécuter toutes les explorations simultanément sollicite les ressources du serveur et impose une charge importante aux serveurs cibles.

Répartition du calendrier
--------------------------

Répartissez le calendrier d'exploration en fonction de la fréquence de mise à jour des sources de données.

.. list-table:: Exemple de calendrier d'exploration
   :header-rows: 1
   :widths: 25 25 50

   * - Source de données
     - Moment d'exécution
     - Raison
   * - Portail interne
     - Tous les jours à 2h00
     - Le nombre de pages étant faible, l'exécution se termine rapidement
   * - Dossier partagé
     - Tous les jours à 3h00
     - Le nombre de fichiers étant élevé, exécution pendant la nuit
   * - Archives
     - Chaque dimanche à 4h00
     - La fréquence de mise à jour étant faible, une exécution hebdomadaire suffit

Configuration du planificateur
-------------------------------

Depuis l'écran d'administration, [Système] > [Planificateur], vous pouvez configurer le moment d'exécution des tâches d'exploration.
La tâche "Default Crawler" par défaut exécute toutes les configurations d'exploration en une seule fois.

Rendre les résultats de recherche plus accessibles avec le mappage de chemins
==============================================================================

Les URL ou chemins de fichiers explorés peuvent être difficiles à comprendre pour les utilisateurs.
Le mappage de chemins permet de transformer les URL affichées dans les résultats de recherche.

Exemple de configuration
-------------------------

Transformez les chemins du serveur de fichiers en URL accessibles depuis un navigateur pour les utilisateurs.

1. [Exploration] > [Mappage de chemins] > [Nouveau]
2. Configurez les éléments suivants :

   - Expression régulière : ``smb://fileserver.example.com/shared/(.*)``
   - Remplacement : ``https://fileserver.example.com/shared/$1``

Ainsi, lorsque l'utilisateur clique sur un lien dans les résultats de recherche, il peut accéder directement au fichier depuis son navigateur.

Utilisation de la recherche transversale
=========================================

Recherche avec filtrage par libellé
------------------------------------

Une fois l'exploration terminée, testez la recherche transversale depuis l'écran de recherche.

L'écran de recherche affiche des onglets ou des menus déroulants pour les libellés.
Les utilisateurs peuvent sélectionner "Tous" pour une recherche transversale, ou choisir un libellé spécifique pour limiter la recherche à cette catégorie.

Par exemple, en recherchant "plan de projet", les résultats peuvent contenir un mélange d'articles du portail, de fichiers Word du dossier partagé et de PDF des archives.
En filtrant avec le libellé "Fichiers partagés", seuls les documents du serveur de fichiers sont affichés.

Ordre de tri des résultats de recherche
----------------------------------------

Par défaut, les résultats sont triés par pertinence (score) par rapport aux mots-clés de recherche.
Indépendamment du type de source de données, les documents les plus pertinents apparaissent en premier.

Résumé
======

Dans cet article, nous avons intégré plusieurs sources de données dans Fess et construit un environnement de recherche transversale.

- Configuration d'exploration pour trois types de sources : sites Web, serveurs de fichiers et fichiers locaux
- Classification par libellés et recherche avec filtrage
- Conception de la répartition du calendrier d'exploration
- Transformation d'URL par mappage de chemins

L'introduction de la recherche transversale permet de trouver les informations nécessaires sans se soucier de "où elles sont stockées".

Dans le prochain article, nous aborderons la conception de la recherche basée sur les rôles, permettant de contrôler les résultats de recherche en fonction des autorisations de chaque département.

Références
==========

- `Guide de l'administrateur Fess <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Configuration de l'exploration de fichiers Fess <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
