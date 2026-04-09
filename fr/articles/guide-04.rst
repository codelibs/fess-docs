============================================================
Partie 4 : Recherche unifiee dans des fichiers disperses -- Construire une recherche transversale dans un environnement multi-sources
============================================================

Introduction
============

Dans l'article precedent, nous avons presente comment integrer la fonction de recherche de Fess dans un site Web existant.
Cependant, dans un environnement d'entreprise reel, les informations ne se trouvent pas uniquement sur des sites Web, mais sont dispersees dans divers emplacements tels que des serveurs de fichiers et des services de stockage cloud.

Dans cet article, nous allons integrer plusieurs sources de donnees dans Fess et construire un environnement permettant aux utilisateurs d'effectuer une recherche transversale sur tous les documents depuis une seule barre de recherche.

Public cible
============

- Personnes dont les documents internes sont repartis dans plusieurs emplacements
- Personnes insatisfaites de la recherche sur les serveurs de fichiers ou le stockage cloud
- Avoir Fess en cours d'execution selon la procedure de la Partie 2

Scenario
========

Nous supposons une entreprise de taille moyenne. Dans cette entreprise, les documents sont disperses dans les emplacements suivants :

- **Site Web interne** : portail interne, blog interne
- **Serveur de fichiers** : dossiers partages par departement (SMB/CIFS)
- **Fichiers locaux** : repertoires specifiques sur le serveur

Lorsqu'un employe se demande "ou est ce document ?", il doit effectuer des recherches separees dans chaque outil.
Nous allons centraliser cela avec Fess afin de permettre une recherche transversale depuis une seule barre de recherche.

Conception des sources de donnees
==================================

Lors de la construction d'une recherche transversale, la premiere etape importante est de concevoir "quoi indexer et comment".

Organisation des cibles de recherche
-------------------------------------

Commencez par organiser les sources de donnees a indexer.

.. list-table:: Organisation des sources de donnees
   :header-rows: 1
   :widths: 20 25 25 30

   * - Source de donnees
     - Type
     - Estimation du volume
     - Frequence de mise a jour
   * - Portail interne
     - Exploration Web
     - Quelques centaines de pages
     - Hebdomadaire
   * - Blog technique
     - Exploration Web
     - De quelques dizaines a quelques centaines de pages
     - Irreguliere
   * - Dossier partage
     - Exploration de fichiers
     - Dizaines de milliers de fichiers
     - Quotidienne
   * - Archives
     - Exploration de fichiers
     - Quelques milliers de fichiers
     - Mensuelle

Conception de la classification par libelles
---------------------------------------------

La fonction "Libelle" de Fess permet de categoriser les cibles de recherche.
Les utilisateurs peuvent selectionner un libelle lors de la recherche pour affiner les resultats a une categorie specifique.

Dans ce scenario, nous configurons les libelles suivants :

- **Portail** : informations du portail interne et du blog
- **Fichiers partages** : documents du serveur de fichiers
- **Archives** : documents anciens

Configuration des libelles
^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Dans l'ecran d'administration, selectionnez [Exploration] > [Libelles]
2. Creez un libelle avec [Nouveau]

Definissez un "Nom" et une "Valeur" pour chaque libelle.
La valeur doit etre en caracteres alphanumeriques et sert a associer le libelle a la configuration d'exploration.

Construction de la configuration d'exploration
================================================

Configuration de l'exploration Web
------------------------------------

Voici la configuration d'exploration pour le portail interne.

1. [Exploration] > [Web] > [Nouveau]
2. Configurez les elements suivants :

   - URL : ``https://portal.example.com/``
   - URL a explorer : ``https://portal.example.com/.*``
   - URL a exclure de l'exploration : ``https://portal.example.com/admin/.*``
   - Nombre maximum d'acces : ``500``
   - Nombre de threads : ``3``
   - Intervalle : ``5000``
   - Libelle : Portail

3. Cliquez sur [Creer]

En definissant des URL d'exclusion, vous pouvez exclure les pages que vous ne souhaitez pas indexer, comme les ecrans d'administration.

Configuration de l'exploration de fichiers
-------------------------------------------

Voici la configuration d'exploration pour le dossier partage.

1. [Exploration] > [Systeme de fichiers] > [Nouveau]
2. Configurez les elements suivants :

   - Chemin : ``smb://fileserver.example.com/shared/``
   - Chemin a explorer : ``smb://fileserver.example.com/shared/.*``
   - Chemin a exclure de l'exploration : ``.*\\.tmp$``
   - Nombre maximum d'acces : ``10000``
   - Nombre de threads : ``5``
   - Intervalle : ``1000``
   - Libelle : Fichiers partages

3. Cliquez sur [Creer]

**Configuration de l'authentification SMB**

Si le serveur de fichiers necessite une authentification, la configuration de l'authentification de fichiers est necessaire.

1. [Exploration] > [Authentification de fichiers] > [Nouveau]
2. Configurez les elements suivants :

   - Nom d'hote : ``fileserver.example.com``
   - Schema : ``Samba``
   - Nom d'utilisateur : nom d'utilisateur du compte de service
   - Mot de passe : mot de passe du compte de service

3. Cliquez sur [Creer]

Exploration de fichiers locaux
-------------------------------

Pour explorer un repertoire specifique sur le serveur, specifiez directement le chemin du fichier.

1. [Exploration] > [Systeme de fichiers] > [Nouveau]
2. Configurez les elements suivants :

   - Chemin : ``file:///data/archive/``
   - Chemin a explorer : ``file:///data/archive/.*``
   - Chemin a exclure de l'exploration : ``.*\\.(log|bak)$``
   - Nombre maximum d'acces : ``5000``
   - Libelle : Archives

3. Cliquez sur [Creer]

Conception du calendrier d'exploration
=======================================

Lorsque vous explorez plusieurs sources de donnees, la conception du calendrier est importante.
Executer toutes les explorations simultanement sollicite les ressources du serveur et impose une charge importante aux serveurs cibles.

Repartition du calendrier
--------------------------

Repartissez le calendrier d'exploration en fonction de la frequence de mise a jour des sources de donnees.

.. list-table:: Exemple de calendrier d'exploration
   :header-rows: 1
   :widths: 25 25 50

   * - Source de donnees
     - Moment d'execution
     - Raison
   * - Portail interne
     - Tous les jours a 2h00
     - Le nombre de pages etant faible, l'execution se termine rapidement
   * - Dossier partage
     - Tous les jours a 3h00
     - Le nombre de fichiers etant eleve, execution pendant la nuit
   * - Archives
     - Chaque dimanche a 4h00
     - La frequence de mise a jour etant faible, une execution hebdomadaire suffit

Configuration du planificateur
-------------------------------

Depuis l'ecran d'administration, [Systeme] > [Planificateur], vous pouvez configurer le moment d'execution des taches d'exploration.
La tache "Default Crawler" par defaut execute toutes les configurations d'exploration en une seule fois.

Rendre les resultats de recherche plus accessibles avec le mappage de chemins
==============================================================================

Les URL ou chemins de fichiers explores peuvent etre difficiles a comprendre pour les utilisateurs.
Le mappage de chemins permet de transformer les URL affichees dans les resultats de recherche.

Exemple de configuration
-------------------------

Transformez les chemins du serveur de fichiers en URL accessibles depuis un navigateur pour les utilisateurs.

1. [Exploration] > [Mappage de chemins] > [Nouveau]
2. Configurez les elements suivants :

   - Expression reguliere : ``smb://fileserver.example.com/shared/(.*)``
   - Remplacement : ``https://fileserver.example.com/shared/$1``

Ainsi, lorsque l'utilisateur clique sur un lien dans les resultats de recherche, il peut acceder directement au fichier depuis son navigateur.

Utilisation de la recherche transversale
=========================================

Recherche avec filtrage par libelle
------------------------------------

Une fois l'exploration terminee, testez la recherche transversale depuis l'ecran de recherche.

L'ecran de recherche affiche des onglets ou des menus deroulants pour les libelles.
Les utilisateurs peuvent selectionner "Tous" pour une recherche transversale, ou choisir un libelle specifique pour limiter la recherche a cette categorie.

Par exemple, en recherchant "plan de projet", les resultats peuvent contenir un melange d'articles du portail, de fichiers Word du dossier partage et de PDF des archives.
En filtrant avec le libelle "Fichiers partages", seuls les documents du serveur de fichiers sont affiches.

Ordre de tri des resultats de recherche
----------------------------------------

Par defaut, les resultats sont tries par pertinence (score) par rapport aux mots-cles de recherche.
Independamment du type de source de donnees, les documents les plus pertinents apparaissent en premier.

Resume
======

Dans cet article, nous avons integre plusieurs sources de donnees dans Fess et construit un environnement de recherche transversale.

- Configuration d'exploration pour trois types de sources : sites Web, serveurs de fichiers et fichiers locaux
- Classification par libelles et recherche avec filtrage
- Conception de la repartition du calendrier d'exploration
- Transformation d'URL par mappage de chemins

L'introduction de la recherche transversale permet de trouver les informations necessaires sans se soucier de "ou elles sont stockees".

Dans le prochain article, nous aborderons la conception de la recherche basee sur les roles, permettant de controler les resultats de recherche en fonction des autorisations de chaque departement.

References
==========

- `Guide de l'administrateur Fess <https://fess.codelibs.org/ja/15.5/admin/index.html>`__

- `Configuration de l'exploration de fichiers Fess <https://fess.codelibs.org/ja/15.5/admin/filecrawl.html>`__
