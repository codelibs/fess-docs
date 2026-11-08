==============================================
Partie 2 : Découvrir la recherche en 5 minutes
==============================================

Introduction
============

Dans l'article précédent, nous avons présenté la nécessité d'une plateforme de recherche en entreprise ainsi qu'une vue d'ensemble de Fess.
Dans cet article, nous vous proposons la procédure la plus rapide pour démarrer Fess et expérimenter la recherche.

L'objectif est de comprendre rapidement quel type d'expérience de recherche Fess peut offrir.
En utilisant Docker Compose, nous allons mettre en place un environnement Fess en quelques lignes de commande, crawler un site Web et effectuer une recherche.

Public cible
============

- Les personnes qui découvrent Fess pour la première fois
- Celles qui souhaitent réaliser rapidement une PoC (preuve de concept) en vue d'une adoption
- Celles qui maîtrisent les opérations de base de Docker

Environnement requis
=====================

- Un environnement dans lequel Docker et Docker Compose sont disponibles
- Au moins 4 Go de mémoire (8 Go ou plus recommandés)
- Une connexion Internet

Préparation préalable (Linux / WSL2)
-------------------------------------

OpenSearch, utilisé par Fess, nécessite un grand nombre de zones de mappage mémoire au démarrage.
Dans les environnements Linux ou WSL2, augmentez la valeur de ``vm.max_map_count`` avec la commande suivante.

::

    $ sudo sysctl -w vm.max_map_count=262144

Ce paramètre est réinitialisé au redémarrage du système d'exploitation. Pour le rendre persistant, ajoutez-le au fichier ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

.. note::

   Si vous utilisez Docker Desktop sur macOS, ce paramètre n'est pas nécessaire.

Démarrer Fess
==============

Obtenir le fichier Docker Compose
-----------------------------------

Le fichier Docker Compose de Fess est disponible dans le dépôt GitHub.
Récupérez-le avec les commandes suivantes.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Le répertoire compose contient plusieurs fichiers de configuration.
Commençons par démarrer avec une configuration simple.

Démarrage
---------

Démarrez Fess et OpenSearch avec la commande suivante.

::

    $ docker compose up -d

Lors du premier démarrage, le téléchargement des images Docker peut prendre plusieurs minutes.
Vous pouvez vérifier l'état du démarrage avec la commande suivante.

::

    $ docker compose ps

Lorsque tous les conteneurs affichent l'état "running", le démarrage est terminé.

Accéder à l'écran de recherche
-------------------------------

Ouvrez ``http://localhost:8080/`` dans votre navigateur.
Si la page d'accueil de recherche Fess s'affiche, le démarrage s'est effectué correctement.

À ce stade, l'index est encore vide, donc aucune recherche ne renverra de résultats.
Dans l'étape suivante, nous allons enregistrer une cible de crawl pour rendre la recherche opérationnelle.

Accéder à l'écran d'administration
====================================

Connexion à l'écran d'administration
--------------------------------------

Accédez à ``http://localhost:8080/admin/`` pour vous connecter à l'écran d'administration.
Les identifiants par défaut sont les suivants.

- Nom d'utilisateur : ``admin``
- Mot de passe : ``admin``

Le tableau de bord de l'écran d'administration permet de visualiser l'état du système d'un seul coup d'œil.

Structure de l'écran d'administration
--------------------------------------

Le menu latéral gauche de l'écran d'administration regroupe les principales fonctions d'administration de Fess.
Passons-les brièvement en revue.

**Crawler**

C'est la zone où l'on enregistre les cibles de recherche. Elle permet de gérer les configurations de crawl pour trois types de sources : Web, système de fichiers et magasin de données.

**Système**

Fonctions d'administration à l'échelle du système, telles que le planificateur, le design et les dictionnaires. Les dictionnaires permettent de gérer les paramètres liés à la qualité de la recherche, comme les synonymes et les mots vides.

**Informations système**

Fournit divers journaux et fonctions de maintenance : journaux de recherche, journaux de tâches, informations de crawl, sauvegardes, etc.

Crawler un site Web
====================

Enregistrement d'une cible de crawl
-------------------------------------

Effectuons un crawl d'un site Web pour le rendre disponible à la recherche.
Nous utiliserons ici le site officiel de Fess comme cible.

1. Dans le menu de gauche de l'écran d'administration, sélectionnez [Crawler] > [Web]
2. Cliquez sur [Créer]
3. Saisissez les informations suivantes

   - URL : ``https://fess.codelibs.org/ja/``
   - URL cible du crawl : ``https://fess.codelibs.org/ja/.*``
   - Nombre maximum d'accès : ``50``
   - Nombre de threads : ``2``
   - Intervalle : ``10000``

4. Cliquez sur [Enregistrer] pour sauvegarder

La configuration pour crawler le site officiel de Fess (pages en japonais), avec un maximum de 50 pages et un intervalle de 10 secondes, est maintenant terminée.

Exécution du crawl
-------------------

Le simple fait de sauvegarder la configuration ne déclenche pas le crawl.
Pour lancer le crawl, exécutez la tâche depuis le planificateur.

1. Sélectionnez [Système] > [Planificateur]
2. Sélectionnez "Default Crawler"
3. Cliquez sur [Démarrer maintenant]

Le crawl démarre.
Vous pouvez suivre la progression depuis [Informations système] > [Informations de crawl].
Pour environ 50 pages, le crawl se termine en quelques minutes.

Expérimenter la recherche
==========================

Effectuer une recherche
------------------------

Une fois le crawl terminé, revenez à l'écran de recherche ``http://localhost:8080/`` et essayez une recherche.

Par exemple, en saisissant "インストール" (installation) et en lançant la recherche, les pages du site Fess relatives à l'installation s'affichent dans les résultats.

Éléments de l'écran de résultats
---------------------------------

L'écran de résultats de recherche affiche les éléments suivants.

**Liste des résultats**

Chaque résultat comprend un titre, une URL et un extrait du contenu (snippet).
Les parties correspondant aux mots-clés de recherche sont mises en surbrillance.

**Nombre de résultats et temps de traitement**

En haut des résultats de recherche, le nombre de résultats et le temps de recherche sont affichés.

**Pagination**

Lorsque les résultats s'étendent sur plusieurs pages, une navigation de pagination s'affiche.

Fonctions de recherche avancées
--------------------------------

Fess offre diverses fonctions de recherche au-delà de la simple recherche par mots-clés.

**Recherche AND/OR**

La séparation des mots-clés par des espaces effectue une recherche AND.
L'utilisation de ``OR`` permet d'effectuer une recherche OR.

::

    インストール Docker       # Recherche AND (contient les deux termes)
    インストール OR Docker    # Recherche OR (contient l'un ou l'autre)

**Recherche par phrase**

En encadrant les termes par des guillemets doubles, vous recherchez les documents correspondant dans cet ordre exact.

::

    "全文検索サーバー"

**Recherche par exclusion**

Pour rechercher des résultats ne contenant pas un mot-clé spécifique, utilisez le signe moins.

::

    インストール -Windows    # Resultats ne contenant pas "Windows"

Arrêt et reprise de l'environnement
=====================================

Arrêt
-----

Une fois l'expérience de recherche terminée, arrêtez l'environnement avec la commande suivante.

::

    $ docker compose down

L'arrêt conserve les données (index), de sorte que vous retrouverez le même état au redémarrage.

Nettoyage complet incluant les données
---------------------------------------

Pour supprimer également les volumes, exécutez la commande suivante.

::

    $ docker compose down -v

Dans ce cas, les index créés par le crawl seront également supprimés.

Ce que l'expérience de recherche révèle
========================================

Grâce à cette expérience, vous avez pu vérifier le fonctionnement de base de Fess.
En envisageant une utilisation en situation réelle, plusieurs questions peuvent se poser.

- "Peut-on également rechercher dans les serveurs de fichiers internes ?" --> traité dans la **Partie 4**
- "Peut-on intégrer une barre de recherche dans un site interne existant ?" --> traité dans la **Partie 3**
- "Peut-on contrôler les informations visibles par département ?" --> traité dans la **Partie 5**
- "Je veux aussi rechercher dans Slack et Confluence" --> traité dans la **Partie 6**
- "Je voudrais que l'IA réponde à mes questions" --> traité dans la **Partie 19**

Fess peut répondre à tous ces scénarios.
Tout au long de cette série, nous présenterons progressivement les méthodes pour les réaliser.

Résumé
======

Dans cet article, nous avons démarré Fess avec Docker Compose et expérimenté le processus complet, du crawl d'un site Web à la recherche.

- Démarrage de Fess + OpenSearch en une seule commande avec Docker Compose
- Enregistrement des cibles de crawl depuis l'écran d'administration et exécution via le planificateur
- Expérience de la recherche par mots-clés, de la recherche AND/OR et de la recherche par phrase sur l'écran de recherche
- Arrêt et reprise de l'environnement en toute simplicité

Le prochain article présentera comment intégrer la fonction de recherche de Fess dans un site Web ou un portail existant.

Références
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__

- `Guide d'installation de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__
