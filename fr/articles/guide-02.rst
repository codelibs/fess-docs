===============================================
Lancer Fess avec Docker et faire des recherches
===============================================

Introduction
============

Lorsque l'on commence à évaluer Fess, la première chose que l'on veut savoir est : « quelles recherches puis-je faire si je le fais tourner moi-même ? »
Dans cet article, nous démarrons Fess 15.9 avec Docker, explorons une vingtaine de pages Web, puis essayons la syntaxe de recherche, étape par étape.

Comme sujet, nous utilisons le « Guide de recherche » en français du site officiel de Fess (un ensemble de pages qui expliquent la recherche AND, la recherche avec caractères génériques, etc.).
Comme la cible se limite à un seul endroit, l'exploration se termine en quelques minutes et vous pouvez lire le contenu des résultats pour les vérifier.

En suivant les étapes de cet article telles quelles, vous saurez :

- Démarrer Fess et OpenSearch avec Docker Compose, puis les arrêter et les redémarrer
- Effectuer la première connexion de l'administrateur et le changement de mot de passe demandé
- Créer une configuration d'exploration Web, lancer l'exploration et vérifier qu'elle est terminée
- Essayer les recherches AND, OR, par exclusion, par phrase et par champ

Les paramètres destinés aux environnements de production (supervision, sauvegarde, SSO, montée en charge) ne sont pas traités.
Depuis « Pour aller plus loin » à la fin, passez à l'article qui correspond à votre objectif.

L'environnement construit dans cet article
==========================================

Les fichiers Compose du dépôt docker-fess démarrent les deux conteneurs suivants.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Service
     - Rôle
     - Emplacement des données
   * - ``fess01``
     - Fess lui-même (image ``ghcr.io/codelibs/fess:15.9.0``). Fournit la page de recherche et la console d'administration sur le port 8080
     - Aucun volume (dans le conteneur)
   * - ``search01``
     - OpenSearch (image ``ghcr.io/codelibs/fess-opensearch``). Le port 9200 est également publié
     - Volumes ``search01_data`` et ``search01_dictionary``

L'index, les configurations d'exploration, les utilisateurs, les journaux des tâches, etc. sont tous stockés dans OpenSearch et restent donc dans le volume ``search01_data``.
En revanche, les paramètres modifiés dans [Système] > [Général] de la console d'administration sont enregistrés dans ``system.properties`` à l'intérieur du conteneur ``fess01``.
Cette différence aura son importance plus loin, dans « Arrêt et redémarrage ».

.. warning::

   Dans cette configuration, OpenSearch fonctionne avec son plugin de sécurité désactivé et est publié sur le port 9200 de l'hôte.
   Utilisez-la pour faire des essais sur votre propre PC ; si vous la faites tourner sur un serveur partagé, consultez d'abord :doc:`guide-10` et :doc:`guide-15`.

Prérequis
=========

- Docker et Docker Compose (la commande ``docker compose``) sont disponibles
- Docker dispose d'au moins 4 Go de mémoire (le tas d'OpenSearch occupe à lui seul 1 Go)
- Vous avez accès à Internet (pour récupérer les images et pour l'exploration)

Sous Linux ou WSL2, augmentez ``vm.max_map_count``, nécessaire au démarrage d'OpenSearch.

::

    $ sudo sysctl -w vm.max_map_count=262144

Cette valeur est réinitialisée au redémarrage du système d'exploitation.
Si vous continuez à utiliser l'environnement, ajoutez-la aussi à ``/etc/sysctl.conf``.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

Démarrer Fess
=============

Récupérer les fichiers Compose pour 15.9.0
------------------------------------------

Les fichiers Compose de la branche par défaut de docker-fess sont mis à jour à chaque nouvelle version.
Pour figer la version à 15.9.0, récupérez les fichiers du tag ``v15.9.0``.

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

``compose.yaml`` ne définit que ``fess01`` ; ``search01``, dont dépend ``fess01``, se trouve dans ``compose-opensearch3.yaml``.
C'est pourquoi toutes les commandes ``docker compose`` qui suivent indiquent à chaque fois les deux fichiers avec ``-f``.
Si vous n'en indiquez qu'un seul, ni le démarrage ni l'arrêt ne fonctionnent correctement.

Démarrer et attendre que Fess soit prêt
---------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

La première fois, cela prend quelques minutes, car les images doivent être récupérées.
Vérifiez l'état avec la commande suivante.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

``fess01`` démarre une fois que ``search01`` est healthy.
Fess est prêt lorsque le STATUS de ``fess01`` indique ``(healthy)``.
Le contrôle de santé de ``fess01`` appelle ``/api/v2/health``, et les 120 premières secondes après le démarrage sont traitées comme un délai de grâce.

Si le conteneur tarde à devenir healthy, consultez les journaux.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

Si le port 8080 est utilisé par une autre application, modifiez ``ports`` dans ``compose.yaml``, par exemple en ``"9080:8080"``.
Pour les autres problèmes de démarrage, consultez le `dépannage de l'installation <https://fess.codelibs.org/fr/stable/install/troubleshooting.html>`__.

Ouvrez ``http://localhost:8080/`` dans votre navigateur : la page de recherche de Fess s'affiche.
Comme rien n'a encore été exploré, une recherche ne renvoie aucun résultat à ce stade.

Se connecter à la console d'administration
==========================================

Ouvrez ``http://localhost:8080/admin/`` et connectez-vous avec le nom d'utilisateur ``admin`` et le mot de passe ``admin``.

Le mot de passe initial ``admin`` est configuré pour ne pas pouvoir être conservé ; après la connexion, vous arrivez donc sur un écran indiquant « Vous devez mettre à jour votre mot de passe ».

1. Saisissez le même mot de passe dans « Nouveau mot de passe » et « Confirmer le nouveau mot de passe » (8 caractères minimum)
2. Cliquez sur [Mettre à jour]

Une fois la mise à jour effectuée, le tableau de bord de la console d'administration s'ouvre.
Désormais, connectez-vous avec le nouveau mot de passe.
Ce mot de passe est enregistré dans OpenSearch ; il est donc conservé même si vous recréez les conteneurs (si vous supprimez aussi les volumes, il redevient ``admin``).

Créer une configuration d'exploration
=====================================

Choisir la cible
----------------

Cette fois, nous explorons le « Guide de recherche » en français du site officiel de Fess.
Il s'agit d'une vingtaine de pages sous ``https://fess.codelibs.org/fr/stable/user/`` ; ``stable`` désigne la documentation de la version stable actuelle (15.9).

Enregistrer une configuration d'exploration Web
-----------------------------------------------

1. Dans le menu de gauche de la console d'administration, ouvrez [Robot d'exploration] > [Web]
2. Cliquez sur [Créer nouveau]
3. Saisissez les champs suivants. Laissez tous les autres champs à leur valeur par défaut

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Champ
        - Valeur
      * - Nom
        - ``Guide de recherche Fess``
      * - URL
        - ``https://fess.codelibs.org/fr/stable/user/index.html``
      * - URL incluses
        - ``https://fess.codelibs.org/fr/stable/user/.*``
      * - Nombre d'accès maximum
        - ``50``

4. Cliquez sur [Créer]

Les champs ont la signification suivante.

- « Nom » est obligatoire. Tant qu'il est vide, la configuration ne peut pas être créée
- « URL » est le point de départ de l'exploration
- « URL incluses » est une expression régulière ; les liens vers des URL qui ne la vérifient pas ne sont pas suivis. Si vous laissez ce champ vide, le robot suit les liens des pages vers d'autres versions, d'autres langues et même des sites externes
- « Nombre d'accès maximum » est une limite supérieure au cas où l'expression régulière serait mal écrite

Parmi les champs laissés à leur valeur par défaut, « Nombre de threads » vaut ``1`` et « Intervalle » vaut ``10000`` millisecondes.
Comme le robot attend 10 secondes pour chaque page, la charge sur le site cible reste faible.
« Autorisations » contient ``{role}guest`` : les utilisateurs non connectés peuvent donc aussi voir les résultats de recherche.
La manière d'afficher des résultats différents selon le service est traitée dans :doc:`guide-05`.

.. note::

   Si vous ciblez des URL comportant un numéro de version, comme ``/fr/15.9/``, aucune page n'est enregistrée.
   Ces pages contiennent un ``<link rel="canonical">`` qui pointe vers ``/fr/stable/``.
   Le robot d'exploration de Fess n'enregistre pas une telle page et suit à la place l'URL canonique.
   Cette URL ne correspond pas à l'expression régulière de « URL incluses », si bien que rien n'est enregistré.
   Si vous ciblez le site de votre entreprise, vérifiez aussi que les URL canoniques sont couvertes par l'expression régulière.

.. tip::

   Avec [Système] > [Assistant], vous pouvez aussi créer une configuration d'exploration en saisissant simplement « Nom », « Chemin d'exploration », « Nombre d'accès maximum » et « Profondeur », puis passer directement à [Démarrer l'exploration].
   Cependant, une configuration créée avec l'assistant ne renseigne pas « URL incluses » ; vous ne pouvez donc pas restreindre l'étendue des liens suivis.
   Si vous voulez restreindre la cible comme ici, créez la configuration depuis [Robot d'exploration] > [Web] comme décrit ci-dessus.

Lancer l'exploration et vérifier qu'elle est terminée
=====================================================

Démarrer l'exploration
----------------------

L'enregistrement de la configuration ne démarre pas l'exploration.

1. Ouvrez [Système] > [Planificateur]
2. Cliquez sur « Default Crawler » dans la liste
3. Cliquez sur [Démarrer maintenant]

« Default Crawler » est la tâche qui exécute ensemble toutes les configurations d'exploration Web, de système de fichiers et de magasin de données activées.
Par défaut, cette tâche a l'expression cron ``0 0 * * *`` et s'exécute aussi automatiquement une fois par jour.
Si vous laissez les conteneurs tourner, les mêmes configurations sont explorées à nouveau les jours suivants.

Avec cette configuration, une vingtaine de pages sont récupérées à 10 secondes d'intervalle ; comptez donc quelques minutes.

Vérifier que l'exploration est terminée
---------------------------------------

Vérifiez dans l'ordre suivant.

1. Ouvrez [Informations système] > [Journal des tâches]. Lorsque le « Statut » de la ligne « Default Crawler » passe de « En cours d'exécution » à « OK », la tâche est terminée. En cas d'« Échec », cliquez sur la ligne pour en ouvrir les détails et consultez le « Résultat »
2. Ouvrez [Informations système] > [Informations sur l'exploration] et cliquez sur la session située tout en haut de la liste (la plus récente). « Taille de l'index (Web/Fichier) » est le nombre de documents enregistrés par cette exploration. Cette fois, il sera d'environ 20
3. Si le nombre est inférieur à vos attentes, ouvrez [Informations système] > [URL d'échec]. Les URL qui n'ont pas pu être récupérées, à cause d'erreurs de connexion par exemple, y sont enregistrées avec leur cause

Même si la tâche indique « OK », le nombre de documents enregistrés peut être 0.
Les URL qui ne correspondent pas à l'expression régulière de « URL incluses » sont traitées comme hors cible et non comme des erreurs ; elles ne sont donc pas non plus enregistrées dans URL d'échec.
Si le nombre est 0 et que URL d'échec est également vide, vérifiez l'écriture de l'URL et de l'expression régulière (``https`` ou ``http``, présence du ``.*`` final, etc.).

Essayer quelques recherches
===========================

Ouvrez ``http://localhost:8080/`` et lancez une recherche.
La page de recherche utilise ``bootstrap``, le thème fourni avec Fess.

Commencez par saisir ``génériques`` et lancez la recherche.
Des pages comme « Recherche avec caractères génériques » et « Caractères spéciaux » apparaissent dans les résultats.
Un clic sur le titre d'un résultat ouvre la page d'origine (fess.codelibs.org).

Ensuite, saisissez l'un après l'autre les termes de recherche suivants.
Vous pouvez vérifier le résultat de chacun d'eux sur les pages que vous venez d'explorer.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Termes de recherche à saisir
     - Signification
   * - ``champ URL``
     - Des termes séparés par une espace forment une recherche AND : seules les pages contenant les deux apparaissent
   * - ``génériques OR floue``
     - Les pages contenant l'un ou l'autre terme apparaissent. ``OR`` s'écrit en majuscules, avec une espace avant et après
   * - ``recherche -étiquette``
     - Exclut des résultats les pages contenant « étiquette ». Placez ``-`` juste avant le terme à exclure
   * - ``"recherche par plage"``
     - Recherche les pages qui contiennent l'expression entre guillemets exactement dans cet ordre (recherche par phrase)
   * - ``title:tri``
     - Recherche uniquement les pages dont le titre contient « tri » (recherche par champ)

Si vous écrivez ``or`` ou ``and`` en minuscules, ils ne sont pas traités comme des opérateurs, mais comme des termes de recherche ordinaires.

La syntaxe utilisée ici, ainsi que le reste de la syntaxe, comme la recherche avec caractères génériques, la recherche floue ou la recherche par plage, est expliquée dans le `Guide de recherche <https://fess.codelibs.org/fr/stable/user/index.html>`__ que vous venez d'explorer.
Vous pouvez aussi rechercher dans votre propre Fess une syntaxe qui vous intéresse, puis ouvrir et lire la page correspondante.

Arrêt et redémarrage
====================

Ce qui est conservé dépend de la manière dont vous arrêtez les conteneurs.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Opération
     - Ce qui est conservé
     - Ce qui est perdu
   * - ``stop`` → ``start``
     - Tout
     - Rien
   * - ``down`` → ``up -d``
     - Ce qui est stocké dans OpenSearch (index, configurations d'exploration, utilisateurs et mots de passe, journaux des tâches, etc.)
     - Ce qui est stocké dans le conteneur ``fess01`` (paramètres modifiés dans [Système] > [Général], etc.)
   * - ``down -v``
     - Rien
     - Tout (le mot de passe administrateur redevient lui aussi ``admin``)

Pour un arrêt courant, utilisez ``stop`` ; pour redémarrer, ``start``.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

``down`` supprime les conteneurs.
Les données d'OpenSearch restent dans les volumes, mais les paramètres de [Général] sont écrits dans ``system.properties`` à l'intérieur du conteneur ``fess01`` et disparaissent donc avec le conteneur.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Lorsque vous avez fini vos essais et voulez tout nettoyer, données comprises, ajoutez ``-v``.
Les volumes sont également supprimés, sans retour en arrière possible.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Certains des paramètres modifiés dans [Général] sont conservés même après la recréation des conteneurs si vous les indiquez dans ``FESS_JAVA_OPTS`` de ``compose.yaml`` (certains éléments, comme les paramètres de connexion SSO, ne peuvent pas être indiqués de cette façon).
Pour la procédure, consultez `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__.

Pour aller plus loin
====================

Passez à l'article qui correspond à votre objectif.

- Comprendre l'architecture de Fess et l'ordre de lecture des articles : :doc:`guide-01`
- Placer une zone de recherche sur un site intranet ou un portail existant : :doc:`guide-03`
- Rechercher à la fois dans les sites Web internes et les serveurs de fichiers : :doc:`guide-04`
- Modifier les résultats de recherche visibles selon le service ou le poste : :doc:`guide-05`
- Rechercher aussi les données de Slack, Confluence, de bases de données, etc. : d'abord :doc:`datastore-basics`, puis :doc:`guide-06`, :doc:`guide-07` et :doc:`guide-12`
- Faire répondre une IA générative à partir des documents internes : :doc:`guide-19`
- Trouver des documents de sens proche même quand les mots-clés ne correspondent pas : :doc:`guide-18`
- Mettre en place la supervision et les sauvegardes pour l'exploitation en production : :doc:`guide-10`
- Configurer le SSO et la protection des accès : :doc:`guide-15`
- Monter en charge à mesure que les documents et les utilisateurs augmentent : :doc:`guide-14`

Références
==========

- `Installation avec Docker (Détails) <https://fess.codelibs.org/fr/stable/install/install-docker.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `Configuration de l'exploration Web <https://fess.codelibs.org/fr/stable/admin/webconfig-guide.html>`__
- `Journal des tâches <https://fess.codelibs.org/fr/stable/admin/joblog-guide.html>`__
- `Guide de recherche <https://fess.codelibs.org/fr/stable/user/index.html>`__
