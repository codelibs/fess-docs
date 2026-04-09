============================================================
Partie 2 : Decouvrir la recherche en 5 minutes -- Premier contact avec Fess via Docker Compose
============================================================

Introduction
============

Dans l'article precedent, nous avons presente la necessite d'une plateforme de recherche en entreprise ainsi qu'une vue d'ensemble de Fess.
Dans cet article, nous vous proposons la procedure la plus rapide pour demarrer Fess et experimenter la recherche.

L'objectif est de comprendre rapidement quel type d'experience de recherche Fess peut offrir.
En utilisant Docker Compose, nous allons mettre en place un environnement Fess en quelques lignes de commande, crawler un site Web et effectuer une recherche.

Public cible
============

- Les personnes qui decouvrent Fess pour la premiere fois
- Celles qui souhaitent realiser rapidement une PoC (preuve de concept) en vue d'une adoption
- Celles qui maitrisent les operations de base de Docker

Environnement requis
=====================

- Un environnement dans lequel Docker et Docker Compose sont disponibles
- Au moins 4 Go de memoire (8 Go ou plus recommandes)
- Une connexion Internet

Preparation prealable (Linux / WSL2)
-------------------------------------

OpenSearch, utilise par Fess, necessite un grand nombre de zones de mappage memoire au demarrage.
Dans les environnements Linux ou WSL2, augmentez la valeur de ``vm.max_map_count`` avec la commande suivante.

::

    $ sudo sysctl -w vm.max_map_count=262144

Ce parametre est reinitialise au redemarrage du systeme d'exploitation. Pour le rendre persistant, ajoutez-le au fichier ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

.. note::

   Si vous utilisez Docker Desktop sur macOS, ce parametre n'est pas necessaire.

Demarrer Fess
==============

Obtenir le fichier Docker Compose
-----------------------------------

Le fichier Docker Compose de Fess est disponible dans le depot GitHub.
Recuperez-le avec les commandes suivantes.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Le repertoire compose contient plusieurs fichiers de configuration.
Commencons par demarrer avec une configuration simple.

Demarrage
---------

Demarrez Fess et OpenSearch avec la commande suivante.

::

    $ docker compose up -d

Lors du premier demarrage, le telechargement des images Docker peut prendre plusieurs minutes.
Vous pouvez verifier l'etat du demarrage avec la commande suivante.

::

    $ docker compose ps

Lorsque tous les conteneurs affichent l'etat "running", le demarrage est termine.

Acceder a l'ecran de recherche
-------------------------------

Ouvrez ``http://localhost:8080/`` dans votre navigateur.
Si la page d'accueil de recherche Fess s'affiche, le demarrage s'est effectue correctement.

A ce stade, l'index est encore vide, donc aucune recherche ne renverra de resultats.
Dans l'etape suivante, nous allons enregistrer une cible de crawl pour rendre la recherche operationnelle.

Acceder a l'ecran d'administration
====================================

Connexion a l'ecran d'administration
--------------------------------------

Accedez a ``http://localhost:8080/admin/`` pour vous connecter a l'ecran d'administration.
Les identifiants par defaut sont les suivants.

- Nom d'utilisateur : ``admin``
- Mot de passe : ``admin``

Le tableau de bord de l'ecran d'administration permet de visualiser l'etat du systeme d'un seul coup d'oeil.

Structure de l'ecran d'administration
--------------------------------------

Le menu lateral gauche de l'ecran d'administration regroupe les principales fonctions d'administration de Fess.
Passons-les brievement en revue.

**Crawler**

C'est la zone ou l'on enregistre les cibles de recherche. Elle permet de gerer les configurations de crawl pour trois types de sources : Web, systeme de fichiers et magasin de donnees.

**Systeme**

Fonctions d'administration a l'echelle du systeme, telles que le planificateur, le design et les dictionnaires. Les dictionnaires permettent de gerer les parametres lies a la qualite de la recherche, comme les synonymes et les mots vides.

**Informations systeme**

Fournit divers journaux et fonctions de maintenance : journaux de recherche, journaux de taches, informations de crawl, sauvegardes, etc.

Crawler un site Web
====================

Enregistrement d'une cible de crawl
-------------------------------------

Effectuons un crawl d'un site Web pour le rendre disponible a la recherche.
Nous utiliserons ici le site officiel de Fess comme cible.

1. Dans le menu de gauche de l'ecran d'administration, selectionnez [Crawler] > [Web]
2. Cliquez sur [Creer]
3. Saisissez les informations suivantes

   - URL : ``https://fess.codelibs.org/ja/``
   - URL cible du crawl : ``https://fess.codelibs.org/ja/.*``
   - Nombre maximum d'acces : ``50``
   - Nombre de threads : ``2``
   - Intervalle : ``10000``

4. Cliquez sur [Enregistrer] pour sauvegarder

La configuration pour crawler le site officiel de Fess (pages en japonais), avec un maximum de 50 pages et un intervalle de 10 secondes, est maintenant terminee.

Execution du crawl
-------------------

Le simple fait de sauvegarder la configuration ne declenche pas le crawl.
Pour lancer le crawl, executez la tache depuis le planificateur.

1. Selectionnez [Systeme] > [Planificateur]
2. Selectionnez "Default Crawler"
3. Cliquez sur [Demarrer maintenant]

Le crawl demarre.
Vous pouvez suivre la progression depuis [Informations systeme] > [Informations de crawl].
Pour environ 50 pages, le crawl se termine en quelques minutes.

Experimenter la recherche
==========================

Effectuer une recherche
------------------------

Une fois le crawl termine, revenez a l'ecran de recherche ``http://localhost:8080/`` et essayez une recherche.

Par exemple, en saisissant "インストール" (installation) et en lancant la recherche, les pages du site Fess relatives a l'installation s'affichent dans les resultats.

Elements de l'ecran de resultats
---------------------------------

L'ecran de resultats de recherche affiche les elements suivants.

**Liste des resultats**

Chaque resultat comprend un titre, une URL et un extrait du contenu (snippet).
Les parties correspondant aux mots-cles de recherche sont mises en surbrillance.

**Nombre de resultats et temps de traitement**

En haut des resultats de recherche, le nombre de resultats et le temps de recherche sont affiches.

**Pagination**

Lorsque les resultats s'etendent sur plusieurs pages, une navigation de pagination s'affiche.

Fonctions de recherche avancees
--------------------------------

Fess offre diverses fonctions de recherche au-dela de la simple recherche par mots-cles.

**Recherche AND/OR**

La separation des mots-cles par des espaces effectue une recherche AND.
L'utilisation de ``OR`` permet d'effectuer une recherche OR.

::

    インストール Docker       # Recherche AND (contient les deux termes)
    インストール OR Docker    # Recherche OR (contient l'un ou l'autre)

**Recherche par phrase**

En encadrant les termes par des guillemets doubles, vous recherchez les documents correspondant dans cet ordre exact.

::

    "全文検索サーバー"

**Recherche par exclusion**

Pour rechercher des resultats ne contenant pas un mot-cle specifique, utilisez le signe moins.

::

    インストール -Windows    # Resultats ne contenant pas "Windows"

Arret et reprise de l'environnement
=====================================

Arret
-----

Une fois l'experience de recherche terminee, arretez l'environnement avec la commande suivante.

::

    $ docker compose down

L'arret conserve les donnees (index), de sorte que vous retrouverez le meme etat au redemarrage.

Nettoyage complet incluant les donnees
---------------------------------------

Pour supprimer egalement les volumes, executez la commande suivante.

::

    $ docker compose down -v

Dans ce cas, les index crees par le crawl seront egalement supprimes.

Ce que l'experience de recherche revele
========================================

Grace a cette experience, vous avez pu verifier le fonctionnement de base de Fess.
En envisageant une utilisation en situation reelle, plusieurs questions peuvent se poser.

- "Peut-on egalement rechercher dans les serveurs de fichiers internes ?" --> traite dans la **Partie 4**
- "Peut-on integrer une barre de recherche dans un site interne existant ?" --> traite dans la **Partie 3**
- "Peut-on controler les informations visibles par departement ?" --> traite dans la **Partie 5**
- "Je veux aussi rechercher dans Slack et Confluence" --> traite dans la **Partie 6**
- "Je voudrais que l'IA reponde a mes questions" --> traite dans la **Partie 19**

Fess peut repondre a tous ces scenarios.
Tout au long de cette serie, nous presenterons progressivement les methodes pour les realiser.

Resume
======

Dans cet article, nous avons demarre Fess avec Docker Compose et experimente le processus complet, du crawl d'un site Web a la recherche.

- Demarrage de Fess + OpenSearch en une seule commande avec Docker Compose
- Enregistrement des cibles de crawl depuis l'ecran d'administration et execution via le planificateur
- Experience de la recherche par mots-cles, de la recherche AND/OR et de la recherche par phrase sur l'ecran de recherche
- Arret et reprise de l'environnement en toute simplicite

Le prochain article presentera comment integrer la fonction de recherche de Fess dans un site Web ou un portail existant.

References
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__

- `Guide d'installation de Fess <https://fess.codelibs.org/ja/15.5/install/index.html>`__
