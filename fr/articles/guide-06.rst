============================================================
Partie 6 : Hub de connaissances pour les equipes de developpement -- Recherche unifiee dans le code, les wikis et les tickets
============================================================

Introduction
============

Les equipes de developpement logiciel utilisent quotidiennement divers outils dans leur travail.
Le code se trouve dans des repositories Git, les specifications dans Confluence, les taches dans Jira, et les echanges quotidiens dans Slack.
Chaque outil dispose de sa propre fonction de recherche, mais pour repondre a la question "Ou avait-on discute de cela ?", effectuer des recherches separees dans chaque outil est inefficace.

Dans cet article, nous construisons un hub de connaissances qui centralise dans Fess les informations des outils utilises quotidiennement par l'equipe de developpement et permet une recherche unifiee.

Public cible
============

- Responsables d'equipes de developpement logiciel et administrateurs d'infrastructure
- Personnes souhaitant effectuer des recherches transversales sur les outils de developpement
- Personnes souhaitant apprendre les bases de l'utilisation des plugins de datastore

Scenario
========

Nous allons rendre les informations d'une equipe de developpement (20 personnes) accessibles via une recherche unifiee.

.. list-table:: Sources de donnees cibles
   :header-rows: 1
   :widths: 20 30 50

   * - Outil
     - Usage
     - Informations a rechercher
   * - Repository Git
     - Gestion du code source
     - Code, README, fichiers de configuration
   * - Confluence
     - Gestion documentaire
     - Documents de conception, comptes rendus de reunion, procedures
   * - Jira
     - Gestion des tickets
     - Rapports de bugs, taches, stories
   * - Slack
     - Communication
     - Discussions techniques, historique des decisions

Qu'est-ce que le crawl de datastore ?
=====================================

Le crawl Web et le crawl de fichiers collectent les documents en parcourant les URL ou les chemins de fichiers.
En revanche, pour collecter les informations des outils SaaS, on utilise le "crawl de datastore".

Le crawl de datastore recupere les donnees via l'API de chaque outil et les enregistre dans l'index de Fess.
Dans Fess, un plugin de datastore est disponible pour chaque outil.

Installation des plugins
========================

Les plugins de datastore peuvent etre installes depuis l'interface d'administration de Fess.

1. Selectionnez [Systeme] > [Plugins] dans l'interface d'administration
2. Consultez la liste des plugins installes
3. Accedez a l'ecran d'installation via le bouton [Installer], puis installez les plugins necessaires depuis l'onglet [Distant]

Pour le scenario de cet article, nous utilisons les plugins suivants.

- ``fess-ds-git`` : Crawl de repositories Git
- ``fess-ds-atlassian`` : Crawl de Confluence / Jira
- ``fess-ds-slack`` : Crawl des messages Slack

Configuration des sources de donnees
=====================================

Configuration du repository Git
---------------------------------

Crawlez le repository Git pour rendre le code et les documents disponibles a la recherche.

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : selectionnez GitDataStore
3. Configuration des parametres

**Exemple de configuration des parametres**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**Exemple de configuration des scripts**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

Specifiez l'URL du repository dans ``uri``, et les informations d'authentification dans ``username`` / ``password``. Pour les repositories prives, definissez le jeton d'acces dans ``password``. ``include_pattern`` permet de filtrer les extensions de fichiers a crawler a l'aide d'une expression reguliere.

Configuration de Confluence
-----------------------------

Rendez les pages et articles de blog Confluence disponibles a la recherche.

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : selectionnez ConfluenceDataStore
3. Configuration des parametres

**Exemple de configuration des parametres**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**Exemple de configuration des scripts**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

Specifiez l'URL de Confluence dans ``home`` et choisissez la methode d'authentification avec ``auth_type``. Pour Confluence Cloud, utilisez l'authentification ``basic`` et definissez le jeton API dans ``basic.password``.

Configuration de Jira
----------------------

Rendez les tickets (Issues) Jira disponibles a la recherche.

Le handler JiraDataStore est inclus dans le meme plugin ``fess-ds-atlassian``.
Vous pouvez utiliser JQL (Jira Query Language) pour filtrer les tickets a crawler.
Par exemple, vous pouvez cibler uniquement les tickets d'un projet specifique ou uniquement les tickets ayant un statut particulier (autre que Closed).

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : selectionnez JiraDataStore
3. Configuration des parametres

**Exemple de configuration des parametres**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**Exemple de configuration des scripts**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

Specifiez la requete JQL dans ``issue.jql`` pour filtrer les tickets a crawler.

Configuration de Slack
-----------------------

Rendez les messages Slack disponibles a la recherche.

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : selectionnez SlackDataStore
3. Configuration des parametres

**Exemple de configuration des parametres**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**Exemple de configuration des scripts**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

Specifiez le jeton OAuth du Bot Slack dans ``token``. Vous pouvez specifier les canaux a crawler avec ``channels`` ; pour cibler tous les canaux, definissez ``*all``. Pour inclure les canaux prives, definissez ``include_private=true`` et assurez-vous que le Bot a ete invite dans ces canaux.

Utilisation des labels
======================

Differencier les sources d'information avec des labels
-------------------------------------------------------

En definissant des labels pour chaque source de donnees, vous permettez aux utilisateurs de filtrer par source lors de la recherche.

- ``code`` : Code provenant des repositories Git
- ``docs`` : Documents de Confluence
- ``tickets`` : Tickets de Jira
- ``discussions`` : Messages de Slack

Les utilisateurs peuvent effectuer une recherche transversale avec "Tout", puis affiner les resultats par label si necessaire.

Amelioration de la qualite de recherche
========================================

Utilisation du boost de documents
----------------------------------

Dans un hub de connaissances pour equipe de developpement, tous les documents n'ont pas la meme importance.
Par exemple, on peut envisager les priorites suivantes.

1. Documents Confluence (specifications officielles, procedures)
2. Tickets Jira (problemes actuels, taches en cours)
3. Repositories Git (code, README)
4. Messages Slack (historique des discussions)

Le boost de documents permet d'augmenter le score de recherche des documents correspondant a certains criteres.
Depuis l'interface d'administration, sous [Crawler] > [Boost de documents], vous pouvez definir des valeurs de boost basees sur les patterns d'URL ou les labels.

Utilisation du contenu associe
-------------------------------

En affichant du "contenu associe" dans les resultats de recherche, vous aidez les utilisateurs a trouver les informations qu'ils recherchent.
Par exemple, lors de la recherche d'un document de conception dans Confluence, il est pratique de voir les tickets Jira associes affiches comme "contenu associe".

Considerations operationnelles
===============================

Planification du crawl
-----------------------

Definissez une frequence de crawl appropriee pour chaque source de donnees.

.. list-table:: Exemple de planification
   :header-rows: 1
   :widths: 25 25 50

   * - Source de donnees
     - Frequence recommandee
     - Raison
   * - Confluence
     - Toutes les 4 heures
     - La frequence de mise a jour des documents est moderee
   * - Jira
     - Toutes les 2 heures
     - Les mises a jour des tickets sont frequentes
   * - Git
     - Quotidien
     - Aligne sur le cycle de release
   * - Slack
     - Toutes les 4 heures
     - Le temps reel n'est pas necessaire, mais la fraicheur est importante

Gestion des limites de debit API
---------------------------------

Les API des outils SaaS sont soumises a des limites de debit.
Configurez un intervalle de crawl adequat pour ne pas depasser les limites de debit de l'API.
L'API Slack en particulier a des limites de debit strictes, il est donc important de prevoir une marge suffisante dans l'intervalle de crawl.

Gestion des jetons d'acces
---------------------------

La configuration des plugins de datastore necessite les jetons d'acces API de chaque outil.
Du point de vue de la securite, veuillez tenir compte des points suivants.

- Principe du moindre privilege : utilisez des jetons d'acces en lecture seule
- Rotation reguliere : renouvelez periodiquement les jetons
- Utilisation de comptes dedies : utilisez des comptes de service plutot que des comptes personnels

Conclusion
==========

Dans cet article, nous avons construit un hub de connaissances qui centralise dans Fess les informations des outils utilises quotidiennement par l'equipe de developpement et permet une recherche unifiee.

- Collecte des donnees de Git, Confluence, Jira et Slack avec les plugins de datastore
- Labels offrant une experience de recherche conviviale pour les developpeurs
- Boost de documents pour controler la priorite des informations
- Considerations operationnelles telles que les limites de debit API et la gestion des jetons

Avec un hub de connaissances pour l'equipe de developpement, vous pouvez repondre rapidement aux questions telles que "Ou a eu lieu cette discussion ?" ou "Ou est cette specification ?".

Le prochain article traitera de la recherche transversale dans les services de stockage cloud.

References
==========

- `Configuration des datastores Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Gestion des plugins Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
