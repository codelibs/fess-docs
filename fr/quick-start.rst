==============
Guide de construction rapide
==============

Introduction
========

Cette explication est destinée aux personnes qui souhaitent rapidement découvrir Fess.
Elle décrit les étapes minimales pour utiliser Fess.

La procédure décrite ici est une méthode de démarrage à des fins d'essai. Pour les procédures de construction en environnement de production, veuillez consulter la :doc:`procédure d'installation <setup>` utilisant Docker, etc.
(Le Fess démarré avec cette procédure est destiné à une simple vérification de fonctionnement et l'utilisation de cet environnement en production n'est pas recommandée)

Démarrage rapide avec Docker (recommandé)
==========================================

La méthode la plus simple pour essayer Fess est d'utiliser Docker.

**Étape 1 : Télécharger les fichiers Docker Compose**

.. code-block:: bash

    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Étape 2 : Démarrer les conteneurs**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Étape 3 : Vérifier le démarrage**

Accédez à http://localhost:8080/ dans votre navigateur. (L'initialisation peut prendre 1 à 2 minutes)

**Étape 4 : Arrêter**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. note::

   Pour plus de détails sur le déploiement Docker, consultez le `Guide d'installation Docker <15.5/install/install-docker.html>`__.

----

Démarrage avec le package ZIP
==============================

Préparation préalable
========

Avant de démarrer Fess, veuillez installer Java 21.
Pour Java 21, `Eclipse Temurin <https://adoptium.net/temurin>`__ est recommandé.

Téléchargement
============

Téléchargez le package ZIP de la dernière version de Fess depuis le `site de version GitHub <https://github.com/codelibs/fess/releases>`__.

Installation
============

Extrayez le fichier fess-x.y.z.zip téléchargé.

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

Démarrage de Fess
===========

Exécutez le script fess pour démarrer Fess.
(Sur Windows, veuillez exécuter fess.bat)

::

    $ ./bin/fess

Accès à l'interface d'administration
==================

Accédez à \http://localhost:8080/admin.
Le nom d'utilisateur/mot de passe par défaut du compte administrateur est admin/admin.

.. warning::

   Veuillez obligatoirement modifier le mot de passe par défaut.
   En environnement de production, il est fortement recommandé de changer le mot de passe immédiatement après la première connexion.

Création de la configuration de crawl
================

Après la connexion, cliquez sur «Crawler» > «Web» dans le menu de gauche.
Cliquez sur le bouton «Nouvelle création» pour créer les informations de configuration du crawl web.

Veuillez saisir les informations suivantes :

- **Nom** : Nom de la configuration de crawl (exemple : Site Web de l'entreprise)
- **URL** : URL cible du crawl (exemple : https://www.example.com/)
- **Nombre maximum d'accès** : Limite du nombre de pages à crawler
- **Intervalle** : Intervalle de crawl (en millisecondes)

Exécution du crawl
============

Cliquez sur «Système» > «Planificateur» dans le menu de gauche.
Cliquez sur le bouton «Démarrer maintenant» du job «Default Crawler» pour démarrer immédiatement le crawl.

Pour une exécution planifiée, sélectionnez «Default Crawler» et configurez le planning.
Si l'heure de début est 10:35 am, entrez 35 10 \* \* ? (le format est «minute heure jour mois jour_de_semaine année»).
Une fois mis à jour, le crawl démarrera à partir de cette heure.

Vous pouvez vérifier si le crawl a démarré dans «Informations de crawl».
Après la fin du crawl, les informations WebIndexSize s'affichent dans les informations de session.

Recherche
====

Après la fin du crawl, accédez à \http://localhost:8080/ et effectuez une recherche pour afficher les résultats.

Arrêt de Fess
===========

Arrêtez le processus fess avec Ctrl-C ou la commande kill, etc.

Pour en savoir plus
==================

Veuillez consulter les documents suivants, etc.

* `Liste des documents <documentation>`__
* `[Série] Introduction facile ! Introduction au serveur de recherche plein texte OSS Fess <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* `Informations pour les développeurs <development>`__
* `Forum de discussion <https://discuss.codelibs.org/c/fessja/>`__

