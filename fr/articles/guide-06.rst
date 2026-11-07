=================================================================
Partie 6 : Hub de connaissances pour les équipes de développement
=================================================================

Introduction
============

Les équipes de développement logiciel utilisent quotidiennement divers outils dans leur travail.
Le code se trouve dans des repositories Git, les spécifications dans Confluence, les tâches dans Jira, et les échanges quotidiens dans Slack.
Chaque outil dispose de sa propre fonction de recherche, mais pour répondre à la question "Où avait-on discuté de cela ?", effectuer des recherches séparées dans chaque outil est inefficace.

Dans cet article, nous construisons un hub de connaissances qui centralise dans Fess les informations des outils utilisés quotidiennement par l'équipe de développement et permet une recherche unifiée.

Public cible
============

- Responsables d'équipes de développement logiciel et administrateurs d'infrastructure
- Personnes souhaitant effectuer des recherches transversales sur les outils de développement
- Personnes souhaitant apprendre les bases de l'utilisation des plugins de datastore

Scénario
========

Nous allons rendre les informations d'une équipe de développement (20 personnes) accessibles via une recherche unifiée.

.. list-table:: Sources de données cibles
   :header-rows: 1
   :widths: 20 30 50

   * - Outil
     - Usage
     - Informations à rechercher
   * - Repository Git
     - Gestion du code source
     - Code, README, fichiers de configuration
   * - Confluence
     - Gestion documentaire
     - Documents de conception, comptes rendus de réunion, procédures
   * - Jira
     - Gestion des tickets
     - Rapports de bugs, tâches, stories
   * - Slack
     - Communication
     - Discussions techniques, historique des décisions

Qu'est-ce que le crawl de datastore ?
=====================================

Le crawl Web et le crawl de fichiers collectent les documents en parcourant les URL ou les chemins de fichiers.
En revanche, pour collecter les informations des outils SaaS, on utilise le "crawl de datastore".

Le crawl de datastore récupère les données via l'API de chaque outil et les enregistre dans l'index de Fess.
Dans Fess, un plugin de datastore est disponible pour chaque outil.

Installation des plugins
========================

Les plugins de datastore peuvent être installés depuis l'interface d'administration de Fess.

1. Sélectionnez [Système] > [Plugins] dans l'interface d'administration
2. Consultez la liste des plugins installés
3. Accédez à l'écran d'installation via le bouton [Installer], puis installez les plugins nécessaires depuis l'onglet [Distant]

Pour le scénario de cet article, nous utilisons les plugins suivants.

- ``fess-ds-git`` : Crawl de repositories Git
- ``fess-ds-atlassian`` : Crawl de Confluence / Jira
- ``fess-ds-slack`` : Crawl des messages Slack

Configuration des sources de données
=====================================

Configuration du repository Git
---------------------------------

Crawlez le repository Git pour rendre le code et les documents disponibles à la recherche.

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : sélectionnez GitDataStore
3. Configuration des paramètres

**Exemple de configuration des paramètres**

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

Spécifiez l'URL du repository dans ``uri``, et les informations d'authentification dans ``username`` / ``password``. Pour les repositories privés, définissez le jeton d'accès dans ``password``. ``include_pattern`` permet de filtrer les extensions de fichiers à crawler à l'aide d'une expression régulière.

Configuration de Confluence
-----------------------------

Rendez les pages et articles de blog Confluence disponibles à la recherche.

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : sélectionnez ConfluenceDataStore
3. Configuration des paramètres

**Exemple de configuration des paramètres**

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

Spécifiez l'URL de Confluence dans ``home`` et choisissez la méthode d'authentification avec ``auth_type``. Pour Confluence Cloud, utilisez l'authentification ``basic`` et définissez le jeton API dans ``basic.password``.

Configuration de Jira
----------------------

Rendez les tickets (Issues) Jira disponibles à la recherche.

Le handler JiraDataStore est inclus dans le même plugin ``fess-ds-atlassian``.
Vous pouvez utiliser JQL (Jira Query Language) pour filtrer les tickets à crawler.
Par exemple, vous pouvez cibler uniquement les tickets d'un projet spécifique ou uniquement les tickets ayant un statut particulier (autre que Closed).

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : sélectionnez JiraDataStore
3. Configuration des paramètres

**Exemple de configuration des paramètres**

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

Spécifiez la requête JQL dans ``issue.jql`` pour filtrer les tickets à crawler.

Configuration de Slack
-----------------------

Rendez les messages Slack disponibles à la recherche.

1. [Crawler] > [Datastore] > [Nouveau]
2. Nom du handler : sélectionnez SlackDataStore
3. Configuration des paramètres

**Exemple de configuration des paramètres**

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

Spécifiez le jeton OAuth du Bot Slack dans ``token``. Vous pouvez spécifier les canaux à crawler avec ``channels`` ; pour cibler tous les canaux, définissez ``*all``. Pour inclure les canaux privés, définissez ``include_private=true`` et assurez-vous que le Bot a été invité dans ces canaux.

Utilisation des labels
======================

Différencier les sources d'information avec des labels
-------------------------------------------------------

En définissant des labels pour chaque source de données, vous permettez aux utilisateurs de filtrer par source lors de la recherche.

- ``code`` : Code provenant des repositories Git
- ``docs`` : Documents de Confluence
- ``tickets`` : Tickets de Jira
- ``discussions`` : Messages de Slack

Les utilisateurs peuvent effectuer une recherche transversale avec "Tout", puis affiner les résultats par label si nécessaire.

Amélioration de la qualité de recherche
========================================

Utilisation du boost de documents
----------------------------------

Dans un hub de connaissances pour équipe de développement, tous les documents n'ont pas la même importance.
Par exemple, on peut envisager les priorités suivantes.

1. Documents Confluence (spécifications officielles, procédures)
2. Tickets Jira (problèmes actuels, tâches en cours)
3. Repositories Git (code, README)
4. Messages Slack (historique des discussions)

Le boost de documents permet d'augmenter le score de recherche des documents correspondant à certains critères.
Depuis l'interface d'administration, sous [Crawler] > [Boost de documents], vous pouvez définir des valeurs de boost basées sur les patterns d'URL ou les labels.

Utilisation du contenu associé
-------------------------------

En affichant du "contenu associé" dans les résultats de recherche, vous aidez les utilisateurs à trouver les informations qu'ils recherchent.
Par exemple, lors de la recherche d'un document de conception dans Confluence, il est pratique de voir les tickets Jira associés affichés comme "contenu associé".

Considérations opérationnelles
===============================

Planification du crawl
-----------------------

Définissez une fréquence de crawl appropriée pour chaque source de données.

.. list-table:: Exemple de planification
   :header-rows: 1
   :widths: 25 25 50

   * - Source de données
     - Fréquence recommandée
     - Raison
   * - Confluence
     - Toutes les 4 heures
     - La fréquence de mise à jour des documents est modérée
   * - Jira
     - Toutes les 2 heures
     - Les mises à jour des tickets sont fréquentes
   * - Git
     - Quotidien
     - Aligné sur le cycle de release
   * - Slack
     - Toutes les 4 heures
     - Le temps réel n'est pas nécessaire, mais la fraîcheur est importante

Gestion des limites de débit API
---------------------------------

Les API des outils SaaS sont soumises à des limites de débit.
Configurez un intervalle de crawl adéquat pour ne pas dépasser les limites de débit de l'API.
L'API Slack en particulier a des limites de débit strictes, il est donc important de prévoir une marge suffisante dans l'intervalle de crawl.

Gestion des jetons d'accès
---------------------------

La configuration des plugins de datastore nécessite les jetons d'accès API de chaque outil.
Du point de vue de la sécurité, veuillez tenir compte des points suivants.

- Principe du moindre privilège : utilisez des jetons d'accès en lecture seule
- Rotation régulière : renouvelez périodiquement les jetons
- Utilisation de comptes dédiés : utilisez des comptes de service plutôt que des comptes personnels

Conclusion
==========

Dans cet article, nous avons construit un hub de connaissances qui centralise dans Fess les informations des outils utilisés quotidiennement par l'équipe de développement et permet une recherche unifiée.

- Collecte des données de Git, Confluence, Jira et Slack avec les plugins de datastore
- Labels offrant une expérience de recherche conviviale pour les développeurs
- Boost de documents pour contrôler la priorité des informations
- Considérations opérationnelles telles que les limites de débit API et la gestion des jetons

Avec un hub de connaissances pour l'équipe de développement, vous pouvez répondre rapidement aux questions telles que "Où a eu lieu cette discussion ?" ou "Où est cette spécification ?".

Le prochain article traitera de la recherche transversale dans les services de stockage cloud.

Références
==========

- `Configuration des datastores Fess <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Gestion des plugins Fess <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
