==============
Guide de construction rapide
==============

Introduction
============

Fess est un serveur de recherche en texte intégral open source qui explore les sites web et les serveurs de fichiers, permettant une recherche transversale du contenu collecté.

Cette explication est destinée aux personnes qui souhaitent rapidement découvrir Fess.
Elle décrit les étapes minimales pour utiliser Fess.

Quelle methode utiliser ?
==========================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - Docker (Recommandé)
     - Package ZIP
   * - Prérequis
     - Docker et Docker Compose
     - Java 21, OpenSearch
   * - Facilité de démarrage
     - ◎ Seulement quelques commandes
     - △ Plusieurs logiciels à installer
   * - Idéal pour
     - Ceux qui veulent d'abord essayer
     - Ceux dans des environnements où Docker n'est pas disponible

Démarrage rapide avec Docker (recommandé)
==========================================

Temps estimé : **5 à 10 minutes au premier démarrage** (y compris le téléchargement de l'image Docker)

La méthode la plus simple pour essayer Fess est d'utiliser Docker.

**Étape 1 : Télécharger les fichiers Docker Compose**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Étape 2 : Démarrer les conteneurs**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Étape 3 : Vérifier le démarrage**

Attendez quelques minutes que les services s'initialisent, puis accédez à :

- **Interface de recherche :** http://localhost:8080/
- **Panneau d'administration :** http://localhost:8080/admin
- **Identifiants par défaut :** admin / admin

.. warning::

   Veuillez obligatoirement modifier le mot de passe par défaut.
   En environnement de production, il est fortement recommandé de changer le mot de passe immédiatement après la première connexion.

**Étape 4 : Arrêter**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

Pour plus de détails sur le déploiement Docker, consultez le :doc:`Guide d'installation Docker <15.6/install/install-docker>`.

----

Démarrage avec le package ZIP
==============================

Temps estimé : **20 à 30 minutes au premier démarrage** (y compris l'installation de Java et OpenSearch)

La procédure décrite ici est une méthode de démarrage à des fins d'essai. Pour les procédures de construction en environnement de production, veuillez consulter la :doc:`procédure d'installation <setup>`.
(Le Fess démarré avec cette procédure est destiné à une simple vérification de fonctionnement et l'utilisation de cet environnement en production n'est pas recommandée)

Préparation préalable
---------------------

Veuillez installer les logiciels suivants avant de démarrer Fess.

**1. Installer Java 21**

`Eclipse Temurin <https://adoptium.net/temurin>`__ est recommandé pour Java 21.

**2. Installer et démarrer OpenSearch**

OpenSearch est nécessaire pour stocker les données de Fess.
Veuillez vous référer à la :doc:`procédure d'installation <setup>` pour l'installer et le démarrer.

Téléchargement
--------------

Téléchargez le package ZIP de la dernière version de Fess depuis le `site de version GitHub <https://github.com/codelibs/fess/releases>`__.

Installation
------------

Extrayez le fichier fess-x.y.z.zip téléchargé.

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

Démarrage de Fess
-----------------

Exécutez le script fess pour démarrer Fess.
(Sur Windows, veuillez exécuter fess.bat)

::

    $ ./bin/fess

Accès à l'interface d'administration
-------------------------------------

Accédez à \http://localhost:8080/admin.
Le nom d'utilisateur/mot de passe par défaut du compte administrateur est admin/admin.

.. warning::

   Veuillez obligatoirement modifier le mot de passe par défaut.
   En environnement de production, il est fortement recommandé de changer le mot de passe immédiatement après la première connexion.

Arrêt de Fess (ZIP)
--------------------

Arrêtez le processus fess avec Ctrl-C ou la commande kill, etc.

----

Configuration du crawl et recherche
=====================================

**1. Création de la configuration de crawl**

Après la connexion, cliquez sur « Crawler » > « Web » dans le menu de gauche.
Cliquez sur le bouton « Nouvelle création » pour créer les informations de configuration du crawl web.

Veuillez saisir les informations suivantes :

- **Nom** : Nom de la configuration de crawl (exemple : Site Web de l'entreprise)
- **URL** : URL cible du crawl (exemple : https://www.example.com/)
- **Nombre maximum d'accès** : Limite du nombre de pages à crawler (pour les débutants, une valeur de ``10`` est recommandée)
- **Intervalle** : Intervalle de crawl en millisecondes (la valeur par défaut ``1000`` ms est recommandée)

.. warning::

   Un nombre maximum d'accès trop élevé peut surcharger le site cible.
   Commencez toujours avec une petite valeur (environ 10 à 100) pour la vérification.
   Lors du crawl de sites que vous ne gérez pas, veuillez respecter les paramètres robots.txt.

**2. Exécution du crawl**

Cliquez sur « Système » > « Planificateur » dans le menu de gauche.
Cliquez sur le bouton « Démarrer maintenant » du job « Default Crawler » pour démarrer immédiatement le crawl.

Pour une exécution planifiée, sélectionnez « Default Crawler » et configurez le planning.
Si l'heure de début est 10:35 am, entrez ``35 10 * * ?`` (le format est « minute heure jour mois jour_de_semaine »).
Une fois mis à jour, le crawl démarrera à partir de cette heure.

Vous pouvez vérifier si le crawl a démarré dans « Informations de crawl ».
Après la fin du crawl, les informations WebIndexSize s'affichent dans les informations de session.

**3. Recherche**

Après la fin du crawl, accédez à \http://localhost:8080/ et effectuez une recherche pour afficher les résultats.

Pour en savoir plus
===================

Veuillez consulter les documents suivants, etc.

* :doc:`Liste des documents <documentation>`
* `[Série] Introduction facile ! Introduction au serveur de recherche plein texte OSS Fess <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* :doc:`Informations pour les développeurs <development>`
* `Forum de discussion <https://discuss.codelibs.org/c/fessja/>`__
