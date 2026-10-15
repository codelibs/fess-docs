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
     - Java 21 (OpenSearch est installé avec la commande ``fess-setup``)
   * - Facilité de démarrage
     - ◎ Seulement quelques commandes
     - △ Installer Java, puis exécuter quelques commandes de configuration
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
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose-opensearch3.yaml

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

Pour plus de détails sur le déploiement Docker, consultez le :doc:`Guide d'installation Docker <15.9/install/install-docker>`.

----

Démarrage avec le package ZIP
==============================

Temps estimé : **20 à 30 minutes au premier démarrage** (y compris l'installation de Java et le téléchargement d'OpenSearch)

La procédure décrite ici est une méthode de démarrage à des fins d'essai. Pour les procédures de construction en environnement de production, veuillez consulter la :doc:`procédure d'installation <setup>`.
(Le Fess démarré avec cette procédure est destiné à une simple vérification de fonctionnement et l'utilisation de cet environnement en production n'est pas recommandée)

Fess n'inclut pas de moteur de recherche : la commande ``fess-setup`` fournie dans le package ZIP
télécharge OpenSearch et installe les plugins nécessaires à Fess.

Préparation préalable
---------------------

Installez Java 21 avant de commencer. `Eclipse Temurin <https://adoptium.net/temurin>`__ est recommandé pour Java 21.
Il n'est pas nécessaire d'installer OpenSearch au préalable : l'étape 2 s'en charge.

.. note::

   OpenSearch ne publie de versions officielles que pour Linux et Windows. Sur macOS,
   ``fess-setup install opensearch`` se termine par une erreur ; utilisez Docker (méthode 1), ou consultez
   :doc:`15.9/install/install-linux` pour installer OpenSearch avec Homebrew.

Étape 1 : Téléchargement et extraction
--------------------------------------

Téléchargez le package ZIP de la dernière version de Fess depuis le `site de version GitHub <https://github.com/codelibs/fess/releases>`__,
extrayez-le, puis placez-vous dans le répertoire :

.. code-block:: bash

    unzip fess-x.y.z.zip
    cd fess-x.y.z

Étape 2 : Installation d'OpenSearch
-----------------------------------

Exécutez ``fess-setup`` en tant qu'utilisateur ordinaire, et non en tant que ``root`` : OpenSearch refuse de démarrer en tant que ``root``.

.. code-block:: bash

    # Linux
    bin/fess-setup install opensearch

    # Windows
    bin\fess-setup.bat install opensearch

Cette commande télécharge la version d'OpenSearch prise en charge par ce Fess dans le répertoire ``opensearch/`` de Fess,
installe les quatre plugins nécessaires à Fess et ajoute à ``config/opensearch.yml`` les paramètres dont Fess a besoin.
``bin/fess`` trouve de lui-même cet OpenSearch : aucun fichier de configuration n'a besoin d'être modifié
tant qu'OpenSearch s'exécute sur le même hôte.

.. warning::

   La commande définit ``plugins.security.disabled: true`` ; OpenSearch accepte donc les requêtes sans
   authentification. Par défaut, il n'écoute que sur l'adresse de bouclage (loopback) ; ne l'exposez pas
   sur un réseau. Consultez :doc:`15.9/install/security` pour les paramètres de production.

Pour l'ensemble des commandes (installation de Node.js et des plugins, ``check``), consultez :doc:`15.9/install/fess-setup`.

Étape 3 : Démarrage d'OpenSearch et de Fess
-------------------------------------------

Démarrez d'abord OpenSearch, puis Fess :

.. code-block:: bash

    # Linux
    opensearch/opensearch-3.9.0/bin/opensearch -d
    bin/fess

.. code-block:: bat

    :: Windows (exécutez chacune dans sa propre invite de commandes)
    opensearch\opensearch-3.9.0\bin\opensearch.bat
    bin\fess.bat

Attendez environ 30 secondes que Fess démarre, puis accédez à :

- http://localhost:8080/ (Recherche)
- http://localhost:8080/admin (Administration - identifiants : admin/admin)

Pour vérifier l'installation, exécutez ``bin/fess-setup check`` (``bin\fess-setup.bat check`` sous Windows).
La commande indique si OpenSearch est joignable et dispose des plugins nécessaires à Fess.

.. warning::

   Veuillez obligatoirement modifier le mot de passe par défaut.
   En environnement de production, il est fortement recommandé de changer le mot de passe immédiatement après la première connexion.

Arrêt de Fess (ZIP)
--------------------

Arrêtez le processus fess avec Ctrl-C ou la commande kill, etc.
Arrêtez ensuite OpenSearch de la même manière (``kill`` sur son processus, ou Ctrl-C s'il s'exécute au premier plan).

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
- **Intervalle** : Intervalle de crawl en millisecondes (la valeur par défaut ``10000`` ms est recommandée)

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
